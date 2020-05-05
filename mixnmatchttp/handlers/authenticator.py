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
from random import randint
from collections import OrderedDict
try:
    # python2
    from collections import _abcoll
except ImportError:
    # python3
    from collections import abc as _abcoll
import hashlib
try:
    from passlib import hash as unix_hash
except ImportError:
    pass  # it's an optional feature

from .. import endpoints
from ..common import param_dict, date_from_timestamp, curr_timestamp
from .base import BaseMeta, BaseHTTPRequestHandler

__all__ = [
    'AuthError',
    'UserAlreadyExistsError',
    'NoSuchUserError',
    'InvalidUsernameError',
    'BadPasswordError',
    'BaseAuthHTTPRequestHandlerMeta',
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

class BaseAuthHTTPRequestHandlerMeta(BaseMeta):
    '''Metaclass to check validity of class attributes'''

    def __new__(cls, name, bases, attrs):
        def isoneof(val, sequence):
            return val in sequence

        new_class = super().__new__(cls, name, bases, attrs)
        pwd_types = [None]
        prefT = '_transform_password_'
        prefV = '_verify_password_'
        for m in dir(new_class):
            if callable(getattr(new_class, m)) \
                    and m.startswith(prefT):
                ptype = m[len(prefT):]
                if hasattr(new_class, '{}{}'.format(prefV, ptype)):
                    pwd_types.append(ptype)
        try:
            strtypes = basestring
        except NameError:  # python3
            strtypes = (str, bytes)
        requirements = {
            '_pwd_type': (isoneof, pwd_types),
            '_SameSite': (isoneof, [None, 'lax', 'strict']),
            '_secrets': (isinstance,
                         (_abcoll.Sequence, _abcoll.Mapping)),
            '_pwd_min_len': (isinstance, int),
            '_pwd_min_charsets': (isinstance, int),
            '_jwt_lifetime': (isinstance, int),
            '_refresh_token_lifetime': (isinstance, int),
            '_is_SSL': (isinstance, bool),
            '_cookie_name': (isinstance, strtypes),
            '_cookie_len': (isinstance, int)}

        for key, value in attrs.items():
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

        return new_class

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
    '''

    _secrets = []
    _pwd_min_len = 10
    _pwd_min_charsets = 3
    _pwd_type = None
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
        self.prune_old_sessions()
        super().__init__(*args, **kwargs)

    def get_current_session(self):
        '''Should return the session token in the request

        Child class should implement
        '''

        raise NotImplementedError

    def get_logged_in_user(self):
        '''Should return the logged in user

        Child class should implement
        '''

        raise NotImplementedError

    def set_session(self, user, session, expiry):
        '''Should ensure the token is sent in the response

        Child class should implement
        '''

        raise NotImplementedError

    def unset_session(self, user, session):
        '''Should ensure the token is cleared client-side

        Child class should implement
        '''

        raise NotImplementedError

    @classmethod
    def get_all_sessions(cls):
        '''Should return a list of (user, token, expiry)

        Child class should implement
        '''

        raise NotImplementedError

    @classmethod
    def get_user_password(cls, user):
        '''Should return the user for the given session

        Child class should implement
        '''

        raise NotImplementedError

    @classmethod
    def get_user_from_session(cls, session):
        '''Should return the user for the given session

        Child class should implement
        '''

        raise NotImplementedError

    @classmethod
    def add_session(cls, user, session, expiry):
        '''Should record the session

        Child class should implement
        '''

        raise NotImplementedError

    @classmethod
    def rm_session(cls, user, session):
        '''Deletes the session

        Child class should implement
        '''

        raise NotImplementedError

    @classmethod
    def new_session_token(cls, user):
        '''Should return a tuple of new session (token, expiry)

        Child class should implement
        '''

        raise NotImplementedError

    @classmethod
    def session_exists(cls, session, user=None):
        '''Should return True or False is session exists

        Child class should implement
        '''

        raise NotImplementedError

    @classmethod
    def user_exists(cls, user):
        '''Should return True or False if user exists

        Child class should implement
        '''

        raise NotImplementedError

    @classmethod
    def _create_user(cls, username, password):
        '''Should create a new user with the given password

        Should return True on success and False otherwise
        Child class should implement
        '''

        raise NotImplementedError

    @classmethod
    def _change_password(cls, username, password):
        '''Should set the password of username (no check)

        Should return True on success and False otherwise
        Child class should implement
        '''

        raise NotImplementedError

    def denied(self):
        '''Returns 401 if resource is secret and no authentication'''

        if self.pathname != '/login' and not self.is_authorized():
            return (401,)
        return super().denied()

    def is_authorized(self):
        '''Returns True or False if request is authorized'''

        user = self.get_logged_in_user()
        checker = self._is_authorized_complex
        secrets = self.__class__._secrets
        requested = '{} {}'.format(self.command, self.pathname)
        try:
            secrets = OrderedDict(self.__class__._secrets)
        except ValueError:
            checker = self._is_authorized_plain
            requested = self.pathname
        return checker(requested, user, secrets)

    @staticmethod
    def _is_authorized_complex(cmd_path, user, secrets_map):
        for regex, users in secrets_map.items():
            logger.debug('{} is allowed for {}'.format(regex, users))
            if re.search(regex, cmd_path):
                if user is not None:
                    if '!{}'.format(user) in users:
                        logger.debug('Explicitly denied')
                        return False
                    if '*' in users:
                        logger.debug('Implicitly allowed')
                        return True
                if user in users:
                    logger.debug('Explicitly allowed')
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

    def expire_session(self):
        '''Invalidate the session server-side'''

        session = self.get_current_session()
        user = self.get_logged_in_user()
        self.rm_session(user, session)
        self.unset_session(user, session)

    def new_session(self, user):
        '''Invalidate the old session and generate a new one'''

        self.expire_session()
        session, expiry = self.new_session_token(user)
        if expiry:
            logger.debug('Session {} expires at {}'.format(
                session, expiry))
        self.add_session(user, session, expiry)
        self.set_session(user, session, expiry)
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
        '''Remove expired sessions

        Child class may override this to implement DB access.
        '''

        logger.debug('Pruning old sessions')
        sessions = cls.get_all_sessions()
        for s in sessions:
            (user, tok, exp) = s
            if exp is not None and exp <= curr_timestamp():
                logger.debug('Removing session {}'.format(tok))
                cls.rm_session(user, tok)

    @classmethod
    def create_user(cls, username, password, plaintext=True):
        '''Creates a user with the given password

        Returns True on success, False otherwise
        - If plaintext is True, then the password is checked against
          the policy and hashed according to the _pwd_type class
          attribute; otherwise it is saved as is (the hashing
          algorithm must correspond to _pwd_type)
        '''

        if not username:
            raise InvalidUsernameError(username)
        if cls.user_exists(username):
            raise UserAlreadyExistsError(username)
        if plaintext:
            if not cls.password_is_strong(password):
                raise BadPasswordError(username)
            password = cls.transform_password(password)
        logger.debug('Creating user {}:{}'.format(
            username, password))
        return cls._create_user(username, password)

    @classmethod
    def change_password(cls, username, password, plaintext=True):
        '''Changes the password of username. In memory only!

        Returns True on success, False otherwise
        - If plaintext is True, then the password is checked against
          the policy and hashed according to the _pwd_type class
          attribute; otherwise it is saved as is (the hashing
          algorithm must correspond to _pwd_type)
        '''

        if not cls.user_exists(username):
            raise NoSuchUserError(username)
        if plaintext:
            if not cls.password_is_strong(password):
                raise BadPasswordError(username)
            password = cls.transform_password(password)
        logger.debug('Changing password for user {}:{}'.format(
            username, password))
        return cls._change_password(username, password)

    def authenticate(self):
        '''Returns True or False if username:password is valid

        username and password taken from request parameters
        '''

        username = self.get_param('username')
        password = self.get_param('password')
        return self.credentials_are_correct(username, password)

    @classmethod
    def credentials_are_correct(cls, username, password):
        '''Returns True or False if username:password is valid

        Child class may override this to implement DB access.
        '''

        if not cls.user_exists(username):
            logger.debug(
                'No such user {}'.format(username))
            return False
        if not cls.verify_password(username, password):
            logger.debug(
                'Wrong password for user {}'.format(username))
            return False
        return True

    @classmethod
    def verify_password(cls, user, password):
        '''Returns True or False if user's password is as given

        Uses the algorithm is given in _pwd_type (class attribute)
        '''

        curr_password = cls.get_user_password(user)
        if cls._pwd_type is None:
            return curr_password == password
        verifier = getattr(
            cls, '_verify_password_{}'.format(
                cls._pwd_type))
        return verifier(plain=password, hashed=curr_password)

    @classmethod
    def transform_password(cls, password):
        '''Returns the password hashed according to the setting

        Uses the algorithm is given in _pwd_type (class attribute)
        '''

        if cls._pwd_type is None:
            return password
        transformer = getattr(
            cls, '_transform_password_{}'.format(
                cls._pwd_type))
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

        if not self.authenticate():
            self.send_error(
                401, explain='Username or password is wrong')
            return

        username = self.get_param('username')
        new_password = self.get_param('new_password')
        try:
            self.change_password(username, new_password,
                                 plaintext=True)
        except (BadPasswordError, NoSuchUserError,
                InvalidUsernameError) as e:
            self.send_error(400, explain=str(e))
            return
        self.new_session(username)
        self.send_response_goto()

    def do_login(self):
        '''Issues a random cookie and saves it'''

        if self.authenticate():
            username = self.get_param('username')
            self.new_session(username)
            self.send_response_goto()
        else:
            self.expire_session()
            self.send_error(
                401, explain='Username or password is wrong')

    def do_logout(self):
        '''Clears the cookie from the browser and saved sessions'''

        self.expire_session()
        self.send_response_goto()

class BaseAuthCookieHTTPRequestHandler(BaseAuthHTTPRequestHandler):
    '''Implements cookie-based authentication

    Incomplete, must be inherited, and the child class must define
    methods for storing/getting/updating users and sessions.
    '''

    _is_SSL = False  # sets the Secure cookie flag if True
    _cookie_name = 'SESSION'
    _cookie_len = 20
    _cookie_lifetime = None  # in seconds; if None---session cookie
    _SameSite = None  # can be 'lax' or 'strict'

    def __init__(self, *args, **kwargs):
        self.__class__.__cookie = None
        super().__init__(*args, **kwargs)

    def get_current_session(self):
        '''Returns the session cookie'''

        cookies = param_dict(self.headers.get('Cookie'))
        if not cookies:
            logger.debug('No cookies given')
            session = None
        else:
            try:
                session = cookies[self.__class__._cookie_name]
            except KeyError:
                logger.debug('No {} cookie given'.format(
                    self.__class__._cookie_name))
                session = None
            else:
                logger.debug('Cookie is {}valid'.format(
                    '' if self.session_exists(session) else 'not '))

        return session

    def get_logged_in_user(self):
        session = self.get_current_session()
        if session is None:
            return None
        return self.get_user_from_session(session)

    def set_session(self, user, session, expiry):
        '''Saves the cookie to be sent with this response'''

        flags = '{}{}HttpOnly; '.format(
            'Secure; ' if self.__class__._is_SSL else '',
            'SameSite={}; '.format(self.__class__._SameSite)
            if self.__class__._SameSite is not None else '')
        if expiry is not None:
            expiry = 'Expires={}; '.format(date_from_timestamp(
                expiry))
        self.__class__.__cookie = \
            '{name}={value}; path=/; {expiry}{flags}'.format(
                name=self.__class__._cookie_name,
                value=session,
                expiry=expiry,
                flags=flags)

    def unset_session(self, user=None, session=None):
        '''Sets an empty cookie to be sent with this response'''

        expiry = 'Expires={}'.format(date_from_timestamp(0))
        self.__class__.__cookie = '{name}=; path=/; {expiry}'.format(
            name=self.__class__._cookie_name, expiry=expiry)

    @classmethod
    def new_session_token(cls, user):
        expiry = cls._cookie_lifetime
        if expiry is not None:
            expiry += curr_timestamp()
        return ('{:02x}'.format(
            randint(0, 2**(4 * cls._cookie_len) - 1)), expiry)

    def end_headers(self):
        if self.__class__.__cookie is not None:
            self.send_header('Set-Cookie', self.__class__.__cookie)
        super().end_headers()

class BaseAuthJWTHTTPRequestHandler(BaseAuthHTTPRequestHandler):
    '''Implements JWT-based authentication with refresh tokens

    Incomplete, must be inherited, and the child class must define
    methods for storing/getting/updating users and sessions.
    '''

    _jwt_lifetime = 15  # in minutes
    _refresh_token_lifetime = 1440  # in minutes
    pass

class BaseAuthInMemoryHTTPRequestHandler(BaseAuthHTTPRequestHandler):
    '''Implements in-memory storage of users and sessions

    Incomplete, must be inherited, and the child class must define
    methods for creating and sending tokens.
    '''

    __users = {}  # username-password key-value
    # in __sessions, each key is a session token, each value is
    # a dictionary of user={username} and expiry={timestamp}
    __sessions = {}

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    @classmethod
    def get_all_sessions(cls):
        '''Returns a list of (user, token, expiry)'''

        return [(None, t, s['expiry'])
                for t, s in cls.__sessions.items()]

    @classmethod
    def get_user_password(cls, user):
        '''Returns the user for the given session'''

        try:
            return cls.__users[user]
        except KeyError:
            return None

    @classmethod
    def get_user_from_session(cls, session):
        '''Returns the user for the given session'''

        try:
            return cls.__sessions[session]['user']
        except KeyError:
            return None

    @classmethod
    def add_session(cls, user, session, expiry):
        '''Records the session'''

        cls.__sessions[session] = {
            'user': user,
            'expiry': expiry}

    @classmethod
    def rm_session(cls, user, session):
        '''Deletes the session'''

        try:
            del cls.__sessions[session]
        except KeyError:
            pass

    @classmethod
    def session_exists(cls, session, user=None):
        '''Returns True or False is session exists

        - If user is given, it checks if the session belongs to that
          username
        '''

        try:
            u = cls.__sessions[session]
        except KeyError:
            return False
        if user is not None and user != u:
            return False
        return True

    @classmethod
    def user_exists(cls, user):
        '''Returns True or False if user exists'''

        return user in cls.__users

    @classmethod
    def _create_user(cls, username, password):
        '''Creates a new user with the given password

        Returns True
        '''

        cls.__users[username] = password
        return True

    @classmethod
    def _change_password(cls, username, password):
        '''Sets the password of username (no check)

        Returns True
        '''

        cls.__users[username] = password
        return True

class AuthCookieHTTPRequestHandler(
        BaseAuthInMemoryHTTPRequestHandler,
        BaseAuthCookieHTTPRequestHandler):
    pass

class AuthJWTHTTPRequestHandler(
        BaseAuthInMemoryHTTPRequestHandler,
        BaseAuthJWTHTTPRequestHandler):
    pass

def num_charsets(arg):
    charsets = ['a-z', 'A-Z', '0-9']
    charsets += ['^{}'.format(''.join(charsets))]
    num = 0
    for c in charsets:
        if re.search('[{}]'.format(c), arg):
            num += 1
    return num
