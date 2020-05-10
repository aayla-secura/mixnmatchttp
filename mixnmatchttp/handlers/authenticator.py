# TODO user roles support
# TODO check if jwt is used and all modules are present

from __future__ import division
#  from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from builtins import *
from future import standard_library
standard_library.install_aliases()
from future.utils import with_metaclass

import logging
import re
from datetime import datetime
from collections import OrderedDict
import hashlib
# optional features
try:
    from passlib import hash as unix_hash
except ImportError:
    pass
try:
    import jwt
except ImportError:
    pass
else:
    from jwt.exceptions import \
        InvalidTokenError as JWTInvalidTokenError
try:
    import cryptography
except ImportError:
    pass
else:
    from cryptography.hazmat.backends import \
        default_backend as crypto_default_backend
    from cryptography.hazmat.primitives.serialization import \
        load_pem_private_key

from .. import endpoints
from ..utils import is_str, is_seq_like, is_map_like, \
    param_dict, datetime_to_timestamp, datetime_from_timestamp, \
    date_from_timestamp, curr_timestamp, UTCTimeZone, randhex
from .base import BaseMeta, BaseHTTPRequestHandler

__all__ = [
    'AuthError',
    'UserAlreadyExistsError',
    'NoSuchUserError',
    'InvalidUsernameError',
    'BadPasswordError',
    'BaseAuthHTTPRequestHandler',
    'BaseAuthCookieHTTPRequestHandler',
    'BaseAuthJWTHTTPRequestHandler',
    'BaseAuthInMemoryHTTPRequestHandler',
    'AuthCookieHTTPRequestHandler',
    'AuthJWTHTTPRequestHandler',
]

logger = logging.getLogger(__name__)

class AuthError(Exception):
    '''Base class for exceptions related to request body read'''
    pass

class UserAlreadyExistsError(AuthError):
    '''Exception raised when a duplicate user is created'''

    def __init__(self, username):
        super().__init__('User {} already exists'.format(username))

class NoSuchUserError(AuthError):
    '''Exception raised when a non-existend user is accessed'''

    def __init__(self, username):
        super().__init__('No such user {}'.format(username))

class InvalidUsernameError(AuthError):
    '''Exception raised when an invalid username is created'''

    def __init__(self, username):
        super().__init__('Invalid username {}'.format(username))

class BadPasswordError(AuthError):
    '''Exception raised when new password is invalid'''

    def __init__(self, username):
        super().__init__('Bad password for user {}'.format(username))


############################################################
class User:
    '''Abstract class for a user'''

    # TODO roles
    def __init__(self, username=None, password=None, **kargs):
        self.username = username
        self.password = password

class Session:
    '''Abstract class for a session'''

    def __init__(self, user=None, token=None, expiry=None, **kargs):
        '''
        - user should be an instance of User
        - expiry should be one of:
        1) an int or float as UTC seconds since Unix epoch
        2) datetime object
        '''

        self.user = user
        self.token = token
        self.expiry = expiry

    def has_expired(self):
        expiry = self.expiry
        if expiry is None:
            return False
        if isinstance(expiry, datetime):
            expiry = datetime_to_timestamp(
                expiry, to_utc=True)
        return expiry <= curr_timestamp(to_utc=True)

class BaseAuthHTTPRequestHandlerMeta(BaseMeta):
    '''Metaclass for BaseAuthHTTPRequestHandler

    Check the validity of class attributes and ensures the required
    password hashing modules are present.
    '''

    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)
        for key, value in attrs.items():
            new_class.__check_attr(key, value)
        return new_class

    def __setattr__(self, key, value):
        self.__check_attr(key, value)
        # super() doesn't work here in python 2, see:
        # https://github.com/PythonCharmers/python-future/issues/267
        super(self.__class__, self).__setattr__(key, value)

    def __check_attr(cls, key, value):
        def isoneof(val, sequence):
            return val in sequence

        def isanytrue(val, checkers):
            for c in checkers:
                if c(val):
                    return True
            return False

        pwd_types = [None]
        prefT = '_transform_password_'
        prefV = '_verify_password_'
        for m in dir(cls):
            if callable(getattr(cls, m)) \
                    and m.startswith(prefT):
                ptype = m[len(prefT):]
                if hasattr(cls, '{}{}'.format(prefV, ptype)):
                    pwd_types.append(ptype)
        requirements = {
            '_pwd_type': (isoneof, pwd_types),
            '_secrets': (isanytrue, [is_seq_like, is_map_like]),
            '_pwd_min_len': (isinstance, int),
            '_pwd_min_charsets': (isinstance, int),
            '_is_SSL': (isinstance, bool),
            '_cookie_name': (isanytrue, [is_str]),
            '_cookie_len': (isinstance, int),
            '_cookie_lifetime': (isinstance, (int, type(None))),
            '_SameSite': (isoneof, [None, 'lax', 'strict']),
            '_jwt_lifetime': (isinstance, int),
            '_send_new_refresh_token': (isinstance, bool),
            '_refresh_token_lifetime': (isinstance, int),
            '_refresh_token_len': (isinstance, int),
        }

        if key in requirements:
            checker, req = requirements[key]
            if not checker(value, req):
                raise TypeError('{} must be {}{}'.format(
                    key,
                    'one of ' if isinstance(req, list) else '',
                    req))
        if key == '_pwd_type':
            if value is not None and value.endswith('crypt'):
                try:
                    unix_hash
                except NameError:
                    raise ImportError(
                        'The passlib module is required for '
                        'unix hashes (*crypt)')
                if value == 'bcrypt':
                    try:
                        import bcrypt
                    except ImportError:
                        raise ImportError(
                            'The bcrypt module is required for '
                            'bcrypt hashes')
                elif value == 'scrypt':
                    try:
                        hashlib.scrypt
                    except AttributeError:  # python2
                        try:
                            import scrypt
                        except ImportError:
                            raise ImportError(
                                'The scrypt module is required '
                                'for scrypt hashes')

class BaseAuthHTTPRequestHandler(
    with_metaclass(BaseAuthHTTPRequestHandlerMeta,
                   BaseHTTPRequestHandler, object)):
    '''Implements authentication in an abstract way

    Incomplete, must be inherited, and the child class must define
    methods for storing/getting/updating users and sessions as well as
    creating and sending tokens.

    Class attributes:
    - _secrets: can be either:
      1) A simple filter: an iterable of absolute or relative paths
         which require authentication:
         - A path filter that begins with / is matched at the
           beginning of the request path and must match until the end
           or until another /
         - Otherwise, the path filter is matched as a path component
           (i.e. following a /) and again must match until the end
           or until another /
         - If no value in the list of path filters matches the
           requested path, then anyone is granted access. Otherwise,
           only authenticated users are granted access.
      2) A more fine-grained filter: an OrderedDict (or equivalently,
         a list of two-item tuples) where each key is a regex for
         {method} {path} and each value is a list of allowed users.
         A user is one of:
           - a literal username, optionally preceded by '!' (to
             negate or deny access)
           - None (anyone, including unauthenticated)
           - '*' (any authenticated user)
         - If no value in the list of secret path regexes matches the
           requested path, then anyone is granted access. Otherwise,
           the first (in order) regex that matched the requested path
           determines if the user is allowed or not:
           - It is denied explicitly if !{user} is given in the list
             of users
           - It is denied implicitly if the user is not in the list
             and neither is '*' or None.
         Example:
        _secrets = [
            # all authenticated users, except service, can access /foo
            ('^[A-Z]+ /foo(/|$)', ['*', '!service']),
            # only admin can POST (POST /foo is still allowed for all
            # other than service
            ('^POST ', ['admin']),
            # anyone can fetch /bar
            ('^GET /bar(/|$)', [None]),
            # require authentication for all other pages
            ('.*', ['*']),
        ]
      Default _secrets is [], i.e. no authentication required.
    - _pwd_min_len: Minimum length of passwords. Default is 10.
    - _pwd_min_charsets: Minimum number of character sets in
      passwords. Default is 3.
    - _pwd_type: the type (usually hash algorithm) to store passwords
      in. Supported values are:
        unsalted ones:
          md5, sha1, sha256, sha512
        salted ones (UNIX passwords):
          md5_crypt, sha1_crypt, sha256_crypt, sha512_crypt, bcrypt,
          scrypt
      If a child class wants to extend these, it should define
      _transform_password_{type} and _verify_password_{type}.
      Default is None (plaintext).
    - _prune_sessions_every: Minumum number of seconds, before we will
      search for and remove expired sessions. It is checked before
      every request, so if it is 0, then old sessions are searched for
      before every request. If it is None, we never search for old
      sessions. Either way, we check if the requested session is
      expired either way, and if it is, it remove it.
    '''

    _secrets = []
    _pwd_min_len = 10
    _pwd_min_charsets = 3
    _pwd_type = None
    _prune_sessions_every = 0
    __last_prune = curr_timestamp()
    _endpoints = endpoints.Endpoint(
        changepwd={
            '$allowed_methods': {'GET', 'POST'},
        },
        login={
            '$allowed_methods': {'GET', 'POST'},
        },
        logout={},
    )

    def __init__(self, *args, **kwargs):
        # parent's __init__ must be called at the end, since
        # SimpleHTTPRequestHandler's __init__ processes the request
        # and calls the handlers
        if self.__class__._prune_sessions_every is not None:
            next_check = self.__class__._prune_sessions_every \
                + self.__class__.__last_prune
            if next_check <= curr_timestamp():
                self.prune_old_sessions()
                self.__class__.__last_prune = curr_timestamp()
        super().__init__(*args, **kwargs)

    ################### Methods specific to authentication type
    def get_current_token(self):
        '''Should return the current token

        Child class should implement
        '''

        raise NotImplementedError

    def set_session(self, session):
        '''Should ensure the token is sent in the response

        Child class should implement
        '''

        raise NotImplementedError

    def unset_session(self, session):
        '''Should ensure the token is cleared client-side

        session is guaranteed to exist
        Child class should implement
        '''

        raise NotImplementedError

    @classmethod
    def generate_session(cls, user):
        '''Should return a new Session

        Child class should implement
        '''

        raise NotImplementedError

    ################### Methods specific to storage type
    @classmethod
    def find_session(cls, token):
        '''Should return the Session corresponding to the token

        Child class should implement
        '''

        raise NotImplementedError

    @classmethod
    def get_all_sessions(cls):
        '''Should return a list of Sessions

        Child class should implement
        '''

        raise NotImplementedError

    @classmethod
    def add_session(cls, session):
        '''Should record the Session

        Child class should implement
        '''

        raise NotImplementedError

    @classmethod
    def rm_session(cls, session):
        '''Should delete the Session

        session is guaranteed to exist
        Child class should implement
        '''

        raise NotImplementedError

    @classmethod
    def find_user(cls, username):
        '''Should return the User for that username

        Child class should implement
        '''

        raise NotImplementedError

    @classmethod
    def add_user(cls, user):
        '''Should record the new User

        Child class should implement
        '''

        raise NotImplementedError

    @classmethod
    def update_user(cls, user):
        '''Called after changing user's attributes

        Should perform any necessary post-update actions
        Child class should implement
        '''

        raise NotImplementedError

    def send_response_changepwd(self):
        '''Sends the response to a change password request

        Here we send send_response_goto, child class may override.
        '''

        self.send_response_goto()

    def send_response_login(self):
        '''Sends the response to a login request

        Here we send send_response_goto, child class may override.
        '''

        self.send_response_goto()

    def send_response_logout(self):
        '''Sends the response to a logout request

        Here we send send_response_goto, child class may override.
        '''

        self.send_response_goto()

    def denied(self):
        '''Returns 401 if resource is secret and no authentication'''

        if self.pathname != '/login' \
                and self.pathname != '/logout' \
                and not self.is_authorized():
            return (401,)
        return super().denied()

    def is_authorized(self):
        '''Returns True or False if request is authorized'''

        session = self.get_current_session()
        checker = self._is_authorized_complex
        secrets = self.__class__._secrets
        requested = '{} {}'.format(self.command, self.pathname)
        try:
            secrets = OrderedDict(self.__class__._secrets)
        except ValueError:
            checker = self._is_authorized_plain
            requested = self.pathname
        return checker(requested,
                       None if session is None else session.user,
                       secrets)

    @staticmethod
    def _is_authorized_complex(cmd_path, user, secrets_map):
        for regex, users in secrets_map.items():
            logger.debug('{} is allowed for {}'.format(regex, users))
            if re.search(regex, cmd_path):
                # TODO roles
                if None in users:
                    logger.debug('Anyone allowed')
                    return True
                if user is None:
                    logger.debug('Unauth denied')
                    return False
                if '!{}'.format(user.username) in users:
                    logger.debug('Explicitly denied')
                    return False
                if user.username in users:
                    logger.debug('Explicitly allowed')
                    return True
                if '*' in users:
                    logger.debug('Implicitly allowed')
                    return True
                logger.debug('Implicitly denied')
                return False
        return True

    @staticmethod
    def _is_authorized_plain(path, user, secrets_list):
        if user is not None:
            return True
        for s in secrets_list:
            logger.debug('{} is secret'.format(s))
            if re.search('{}{}(/|$)'.format(
                ('^' if s[0] == '/' else '(/|^)'),
                    s), path):
                return False
        return True

    def get_current_session(self):
        '''Returns the current Session if still valid

        If it has expired, it removes it and returns None.
        This implementation relies on the session token in the request
        being saved by us. For authentication schemes which rely on
        stateless tokens (e.g. JWT), override this method and return
        a Session with a None token (but valid User and expiry).
        '''

        session = self.find_session(self.get_current_token())
        if session is None:
            logger.debug('No session')
            return None
        if session.has_expired():
            logger.debug('Session {} has expired'.format(
                session.token))
            self.rm_session(session)
            self.unset_session(session)
            return None
        logger.debug('Found session for {}'.format(
            session.user.username))
        return session

    def expire_current_session(self):
        '''Invalidates the session server-side'''

        session = self.get_current_session()
        if session is None or session.token is None:
            return
        self.rm_session(session)
        self.unset_session(session)

    def new_session(self, user):
        '''Invalidates the old session and generates a new one'''

        self.expire_current_session()
        session = self.generate_session(user)
        if session.expiry:
            logger.debug('Session {} expires at {}'.format(
                session.token, session.expiry))
        self.add_session(session)
        self.set_session(session)
        return session

    @classmethod
    def load_users_from_file(cls, userfile, plaintext=True):
        '''Adds users from the userfile

        - userfile can be a string (filename) or a file handle
          - The file contains one username:password per line.
          - Neither username, nor password can be empty.
        - If plaintext is True, then the password is checked against
          the policy and hashed according to the _pwd_type class
          attribute; otherwise it is saved as is (the hashing
          algorithm must correspond to _pwd_type)
        '''

        ufile = userfile
        if not hasattr(ufile, 'read'):
            # don't handle IOError here
            ufile = open(ufile, 'r')
        with ufile:
            for line in ufile:
                # TODO roles
                username, _, password = \
                    line.rstrip('\n').rstrip('\r').partition(':')
                try:
                    cls.create_user(username, password,
                                    plaintext=plaintext)
                except (UserAlreadyExistsError, InvalidUsernameError,
                        BadPasswordError) as e:
                    logger.error('{}'.format(str(e)))

    @classmethod
    def prune_old_sessions(cls):
        '''Removes expired sessions'''

        logger.debug('Pruning old sessions')
        sessions = cls.get_all_sessions()
        for s in sessions:
            if s.has_expired():
                logger.debug('Removing session {}'.format(s.token))
                cls.rm_session(s)

    @classmethod
    def create_user(cls, username, password, plaintext=True):
        '''Creates a user with the given password

        - If plaintext is True, then the password is checked against
          the policy and hashed according to the _pwd_type class
          attribute; otherwise it is saved as is (the hashing
          algorithm must correspond to _pwd_type)
        '''

        if not username:
            raise InvalidUsernameError(username)
        if cls.find_user(username):
            raise UserAlreadyExistsError(username)
        if plaintext:
            if not cls.password_is_strong(password):
                raise BadPasswordError(username)
            password = cls.transform_password(password)
        logger.debug('Creating user {}:{}'.format(
            username, password))
        cls.add_user(User(username=username, password=password))

    @classmethod
    def change_password(
            cls, user_or_username, password, plaintext=True):
        '''Changes the password of username (no validation of current)

        - user_or_username is an instance of User or a string
        - If plaintext is True, then the password is checked against
          the policy and hashed according to the _pwd_type class
          attribute; otherwise it is saved as is (the hashing
          algorithm must correspond to _pwd_type)
        '''

        user = user_or_username
        if not isinstance(user, User):
            user = cls.find_user(user)
            if user is None:
                raise NoSuchUserError(user.username)
        if plaintext:
            if not cls.password_is_strong(password):
                raise BadPasswordError(user.username)
            password = cls.transform_password(password)
        logger.debug('Changing password for user {}:{}'.format(
            user.username, password))
        user.password = password
        cls.update_user(user)

    def authenticate(self):
        '''Returns the User if successful login, otherwise None

        username and password taken from request parameters
        '''

        username = self.get_param('username')
        password = self.get_param('password')
        user = self.find_user(username)
        if user is None:
            logger.debug('No such user {}'.format(username))
            return None
        if self.verify_password(user, password):
            return user
        return None

    @classmethod
    def verify_password(cls, user, password):
        '''Returns True or False if user's password is as given

        Uses the algorithm is given in _pwd_type (class attribute)
        '''

        if cls._pwd_type is None:
            return user.password == password
        verifier = getattr(
            cls, '_verify_password_{}'.format(cls._pwd_type))
        return verifier(plain=password, hashed=user.password)

    @classmethod
    def transform_password(cls, password):
        '''Returns the password hashed according to the setting

        Uses the algorithm is given in _pwd_type (class attribute)
        '''

        if cls._pwd_type is None:
            return password
        transformer = getattr(
            cls, '_transform_password_{}'.format(cls._pwd_type))
        return transformer(password)

    @staticmethod
    def _verify_password_md5_crypt(plain, hashed):
        return unix_hash.md5_crypt.verify(plain, hashed)

    @staticmethod
    def _verify_password_sha1_crypt(plain, hashed):
        return unix_hash.sha1_crypt.verify(plain, hashed)

    @staticmethod
    def _verify_password_sha256_crypt(plain, hashed):
        return unix_hash.sha256_crypt.verify(plain, hashed)

    @staticmethod
    def _verify_password_sha512_crypt(plain, hashed):
        return unix_hash.sha512_crypt.verify(plain, hashed)

    @staticmethod
    def _verify_password_bcrypt(plain, hashed):
        return unix_hash.bcrypt.verify(plain, hashed)

    @staticmethod
    def _verify_password_scrypt(plain, hashed):
        return unix_hash.scrypt.verify(plain, hashed)

    @staticmethod
    def _verify_password_md5(plain, hashed):
        return hashlib.md5(
            plain.encode('utf-8')).hexdigest() == hashed

    @staticmethod
    def _verify_password_sha1(plain, hashed):
        return hashlib.sha1(
            plain.encode('utf-8')).hexdigest() == hashed

    @staticmethod
    def _verify_password_sha256(plain, hashed):
        return hashlib.sha256(
            plain.encode('utf-8')).hexdigest() == hashed

    @staticmethod
    def _verify_password_sha512(plain, hashed):
        return hashlib.sha512(
            plain.encode('utf-8')).hexdigest() == hashed

    @staticmethod
    def _transform_password_md5_crypt(password):
        return unix_hash.md5_crypt.hash(password)

    @staticmethod
    def _transform_password_sha1_crypt(password):
        return unix_hash.sha1_crypt.hash(password)

    @staticmethod
    def _transform_password_sha256_crypt(password):
        return unix_hash.sha256_crypt.hash(password)

    @staticmethod
    def _transform_password_sha512_crypt(password):
        return unix_hash.sha512_crypt.hash(password)

    @staticmethod
    def _transform_password_bcrypt(password):
        return unix_hash.bcrypt.hash(password)

    @staticmethod
    def _transform_password_scrypt(password):
        return unix_hash.scrypt.hash(password)

    @staticmethod
    def _transform_password_md5(password):
        return hashlib.md5(password.encode('utf-8')).hexdigest()

    @staticmethod
    def _transform_password_sha1(password):
        return hashlib.sha1(password.encode('utf-8')).hexdigest()

    @staticmethod
    def _transform_password_sha256(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    @staticmethod
    def _transform_password_sha512(password):
        return hashlib.sha512(password.encode('utf-8')).hexdigest()

    @classmethod
    def password_is_strong(cls, password):
        '''Returns True or False if password conforms to policy'''

        return (password is not None
                and len(password) >= cls._pwd_min_len
                and num_charsets(password) >= cls._pwd_min_charsets)

    def do_changepwd(self):
        '''Changes the password for the given username'''

        user = self.authenticate()
        if user is None:
            self.send_error(
                401, explain='Username or password is wrong')
            return

        new_password = self.get_param('new_password')
        try:
            self.change_password(user, new_password, plaintext=True)
        except (BadPasswordError, NoSuchUserError,
                InvalidUsernameError) as e:
            self.send_error(400, explain=str(e))
            return
        self.new_session(user)
        self.send_response_changepwd()

    def do_login(self):
        '''Issues a random cookie and saves it'''

        user = self.authenticate()
        if user is None:
            self.expire_current_session()
            self.send_error(
                401, explain='Username or password is wrong')
            return
        self.new_session(user)
        self.send_response_login()

    def do_logout(self):
        '''Clears the cookie from the browser and saved sessions'''

        self.expire_current_session()
        self.send_response_logout()

class BaseAuthCookieHTTPRequestHandler(BaseAuthHTTPRequestHandler):
    '''Implements cookie-based authentication

    Incomplete, must be inherited, and the child class must define
    methods for storing/getting/updating users and sessions.

    Class attributes:
    - _is_SSL: sets the Secure cookie flag if True. Default is False.
    - _cookie_name: the cookie name. Default is 'SESSION'.
    - _cookie_len: Number of characters in the cookie (random hex).
      Default is 20.
    - _cookie_lifetime: Lifetime in seconds.
      Default is None (session cookie)
    - _SameSite: SameSite cookie flag. Can be 'lax' or 'strict'.
      Default is None (do not set it).
    '''

    _is_SSL = False
    _cookie_name = 'SESSION'
    _cookie_len = 20
    _cookie_lifetime = None
    _SameSite = None

    def get_current_token(self):
        '''Returns the session cookie'''

        cookies = param_dict(self.headers.get('Cookie'))
        if not cookies:
            return None
        try:
            token = cookies[self.__class__._cookie_name]
        except KeyError:
            return None
        return token

    def set_session(self, session):
        '''Saves the cookie to be sent with this response'''

        flags = '{}{}HttpOnly; '.format(
            'Secure; ' if self.__class__._is_SSL else '',
            'SameSite={}; '.format(self.__class__._SameSite)
            if self.__class__._SameSite is not None else '')
        cookie = \
            '{name}={value}; path=/; {expiry}{flags}'.format(
                name=self.__class__._cookie_name,
                value=session.token,
                expiry=cookie_expflag(session.expiry),
                flags=flags)
        self.save_header('Set-Cookie', cookie)

    def unset_session(self, session):
        '''Sets an empty cookie to be sent with this response'''

        cookie = '{name}=; path=/; {expiry}'.format(
            name=self.__class__._cookie_name,
            expiry=cookie_expflag(0))
        self.save_header('Set-Cookie', cookie)

    @classmethod
    def generate_session(cls, user):
        '''Returns a new Session'''

        expiry = cls._cookie_lifetime
        if expiry is not None:
            expiry += curr_timestamp(to_utc=True)
        return Session(
            token=randhex(cls._cookie_len),
            user=user,
            expiry=expiry)

class BaseAuthJWTHTTPRequestHandler(BaseAuthHTTPRequestHandler):
    '''Implements JWT-based authentication with refresh tokens

    Incomplete, must be inherited, and the child class must define
    methods for storing/getting/updating users and sessions.

    - A JSON response is sent to a /login or /changepwd with an
      access_token (JWT) and a refresh_token.
    - Defines a new endpoint: /refresh which takes a refresh_token
      parameter and issues a new access_token. If the
      _send_new_refresh_token class attribute is True, then a new
      refresh_token is also sent with a /refresh (and the old one is
      expired).
    - If a refresh_token is given during /logout it is removed
      server-side.

    Class attributes:
    - _jwt_lifetime: JWT lifetime in minutes. Default is 15.
    - _send_new_refresh_token: Send a new refresh token after a JWT
      refresh (/refresh request). Default is True.
    - _refresh_token_lifetime: refresh token lifetime in minutes.
        Default is 1440 (one day).
    - _refresh_token_len: Number of characters in the refresh token
      (random hex). Default is 100.
    - _decode_opts: PyJWT options to pass to the decode method.
      Default is:
        {'verify_signature': True,
         'require_exp': True,
         'verify_exp': True}
    - _algorithm: The algorithm to use. Default is 'HS256'.
    - _enc_key: The key used to sign the JWT. A passphrase (for
      symmetric algorithms) or a loaded and decrypted PEM private key
      (for asymmetric algorithms).
    - _dec_key: The key used to verify the JWT. The same passphrase as
      _enc_key (for symmetric algorithms), or the corresponding public
      key (for asymmetric algorithms).
    You can load public/private keys from a file by calling the
    set_JWT_keys class method.
    '''

    _jwt_lifetime = 15
    _send_new_refresh_token = True
    _refresh_token_lifetime = 1440
    _refresh_token_len = 100
    _decode_opts = {
        'verify_signature': True,
        'require_exp': True,
        'verify_exp': True}
    _algorithm = 'HS256'
    _enc_key = None
    _dec_key = None
    _endpoints = endpoints.Endpoint(
        refresh={
            '$allowed_methods': {'GET', 'POST'},
        },
        logout={
            '$allowed_methods': {'GET', 'POST'},
        },
    )

    #  def __init__(self, *args, **kargs):
    #      pass  # XXX

    @classmethod
    def set_JWT_keys(cls,
                     passphrase,
                     algorithm=None,
                     privkey=None,
                     pubkey=None):
        '''Set the passphrase or keys used to sign and verify JWTs

        - algortihm: The JWT algorithm, e.g. HS256. If not supplied,
          then it is taken from the _algorithm class attribute.
          If it is supplied, it sets that class attribute.
        - passphrase: The passphrase to use for symmetric algorithms,
          or the passphrase to use to decrypt a private key file (when
          loading it from a file). It must be supplied, even if the
          given privkey is unencrypted (in which case passphrase must
          be None).
        - privkey: The private PEM key to use for signing the JWT. Only
          for asymmetric algorithms. It can be a filename, an open file
          handle, or an already decrypted PEM key (as a string, should
          begin with "-----BEGIN"). It must be supplied asymmetric
          algorithms.
        - pubkey: The public PEM key to use for verifying the JWT
          signature. It can be a filename, an open file handle, or a PEM
          key (as a string, should begin with "-----BEGIN"). It must
          be supplied for asymmetric algorithms.
        '''

        def load_privkey(fh):
            _passphrase = passphrase
            if not isinstance(_passphrase, bytes):
                _passphrase = _passphrase.encode('utf-8')
            return load_pem_private_key(
                fh.read(),
                password=_passphrase,
                backend=crypto_default_backend())

        def load_pubkey(fh):
            return fh.read()

        def load_key(arg, loader):
            if is_str(arg):
                if not arg.startswith('-----BEGIN'):
                    with open(arg, 'rb') as f:
                        return loader(f)
            # it has to be an open file handle
            return loader(f)

        if algorithm is not None:
            cls._algorithm = algorithm
        if cls._algorithm.startswith('HS'):
            # symmetric algorithm
            setattr(cls, '_enc_key', passphrase)
            setattr(cls, '_dec_key', passphrase)
            return
        # asymmetric algorithm
        privkey_loaded = load_key(privkey, load_privkey)
        pubkey_loaded = load_key(pubkey, load_pubkey)
        setattr(cls, '_enc_key', privkey_loaded)
        setattr(cls, '_dec_key', pubkey_loaded)

    def send_response_changepwd(self):
        '''Sends the response to a change password request

        Here we send a new access_token and refresh_token.
        '''

        self.send_as_json()

    def send_response_refresh(self):
        '''Sends the response to a refresh request

        Here we send a new access_token and possibly refresh_token.
        '''

        self.send_as_json()

    def send_response_login(self):
        '''Sends the response to a login request

        Here we send a new access_token and refresh_token.
        '''

        self.send_as_json()

    def denied(self):
        '''Returns 401 if resource is secret and no authentication

        Same as parent denied, but also whitelist /refresh endpoint.
        '''

        if self.pathname == '/refresh':
            return None
        return super().denied()

    def get_current_session(self):
        '''Returns a Session if the JWT or refresh_token is valid

        - If a refresh_token is given (as it should to /refresh or
          /logout), then the Session.token is set to it.
        - Otherwise if the JWT is valid, Session.user and
          Session.expiry are taken from it and Session.token will be
          None.
        - Otherwise returns None.
        '''

        # see if refresh token is given and still valid
        session = super().get_current_session()
        if session is not None:
            return session  # OK
        # check the JWT
        jwtok = self._get_current_jwt()
        if jwtok is None:
            logger.debug('No JWT')
            return None
        jwtok_d = self._decode_jwt(jwtok)
        if jwtok_d is None:
            logger.debug('Invalid JWT')
            return None
        logger.debug('Found session for {}'.format(jwtok_d['sub']))
        return Session(token=None,
                       user=self.find_user(jwtok_d['sub']),
                       expiry=datetime_from_timestamp(
                           jwtok_d['exp'],
                           relative=False,
                           from_utc=False,
                           to_utc=True))

    def get_current_token(self):
        '''Returns the refresh token'''

        return self.get_param('refresh_token')

    def set_session(self, session):
        '''Saves a new JWT to be sent with this response'''

        jwtok = self._get_new_jwt(session.user)
        self.save_response_param('access_token', jwtok)
        if session.token is not None:
            self.save_response_param('refresh_token', session.token)

    def unset_session(self, session):
        '''Does nothing'''

        pass

    @classmethod
    def generate_session(cls, user):
        '''Returns a new Session; token is the refresh token'''

        token = randhex(cls._refresh_token_len)
        expiry = datetime_from_timestamp(
            cls._refresh_token_lifetime * 60,
            relative=True, to_utc=True)
        return Session(
            token=token,
            user=user,
            expiry=expiry)

    @classmethod
    def _get_new_jwt(cls, user):
        now = datetime_from_timestamp(0, relative=True, to_utc=True)
        exp = datetime_from_timestamp(
            cls._jwt_lifetime * 60, relative=True, to_utc=True)
        token_d = {
            'sub': user.username,
            'exp': exp,
            'nbf': now,
            'iat': exp}
        return jwt.encode(token_d,
                          cls._enc_key,
                          algorithm=cls._algorithm).decode('utf-8')

    def _get_current_jwt(self):
        auth = self.headers.get('Authorization')
        if not auth or not auth.startswith('Bearer '):
            return None
        return auth[len('Bearer '):]

    @classmethod
    def _decode_jwt(cls, token):
        try:
            res = jwt.decode(
                token,
                cls._dec_key,
                algorithms=[cls._algorithm],
                options=cls._decode_opts)
        except JWTInvalidTokenError as e:
            logger.debug(str(e))
            return None
        return res

    def do_refresh(self):
        '''Sends a new access_token

        If the _send_new_refresh_token class attribute is True, then
        a new refresh_token is also sent.
        '''

        # see if refresh token is given and still valid
        session = super().get_current_session()
        if session is None:
            self.send_error(
                401, explain='Missing or invalid refresh token')
            return
        if self.__class__._send_new_refresh_token:
            session = self.new_session(session.user)
            self.set_session(session)
        else:
            self.set_session(Session(user=session.user))
        self.send_response_refresh()

class BaseAuthInMemoryHTTPRequestHandler(BaseAuthHTTPRequestHandler):
    '''Implements in-memory storage of users and sessions

    Incomplete, must be inherited, and the child class must define
    methods for creating and sending tokens.
    '''

    __users = {}  # username-User key-valuse
    __sessions = {}  # token--Session key-values

    @classmethod
    def find_session(cls, token):
        '''Returns the Session corresponding to the token

        Child class should implement
        '''

        try:
            return cls.__sessions[token]
        except KeyError:
            return None

    @classmethod
    def get_all_sessions(cls):
        '''Returns a list of Sessions'''

        return list(cls.__sessions.values())

    @classmethod
    def add_session(cls, session):
        '''Records the Session'''

        cls.__sessions[session.token] = session

    @classmethod
    def rm_session(cls, session):
        '''Deletes the Session'''

        del cls.__sessions[session.token]

    @classmethod
    def find_user(cls, username):
        '''Returns the User for that username'''

        try:
            return cls.__users[username]
        except KeyError:
            return None

    @classmethod
    def add_user(cls, user):
        '''Records the new User'''

        cls.__users[user.username] = user

    @classmethod
    def update_user(cls, user, **kargs):
        '''Does nothing'''

        pass

class AuthCookieHTTPRequestHandler(
        BaseAuthInMemoryHTTPRequestHandler,
        BaseAuthCookieHTTPRequestHandler):
    '''Cookie-based auth (in-memory storage)'''

    pass

class AuthJWTHTTPRequestHandler(
        BaseAuthInMemoryHTTPRequestHandler,
        BaseAuthJWTHTTPRequestHandler):
    '''JWT-based auth with refresh tokens (in-memory storage)'''

    pass


def num_charsets(arg):
    '''Returns the number of character sets in arg'''

    charsets = ['a-z', 'A-Z', '0-9']
    charsets += ['^{}'.format(''.join(charsets))]
    num = 0
    for c in charsets:
        if re.search('[{}]'.format(c), arg):
            num += 1
    return num

def cookie_expflag(expiry):
    '''Returns an "Expires={date} GMT" flag for cookies

    - expiry should be one of:
    1) an int or float as UTC seconds since Unix epoch
    2) datetime object
    '''

    if expiry is None:
        return ''
    fmt = '%a, %d %b %Y %H:%M:%S GMT'
    ts = expiry
    if isinstance(ts, datetime):
        ts = datetime_to_timestamp(ts, to_utc=True)
    return 'Expires={}; '.format(date_from_timestamp(
        ts, relative=False, from_utc=True, to_utc=True,
        datefmt=fmt))
