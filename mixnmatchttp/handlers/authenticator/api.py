# TODO check if jwt is used and all modules are present

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

from ...utils import is_str, is_seq_like, is_map_like, \
    datetime_to_timestamp, curr_timestamp, open_path, \
    num_charsets
from ...conf import Conf, ConfItem
from ...endpoints import Endpoint
from ..base import BaseMeta, BaseHTTPRequestHandler
from .exc import UserAlreadyExistsError, NoSuchUserError, \
    InvalidUsernameError, BadPasswordError


logger = logging.getLogger(__name__)


def _required_hashing_modules(htype):
    req = []
    if htype in [
            'bcrypt',
            'md5_crypt',
            'scrypt',
            'sha1_crypt',
            'sha256_crypt',
            'sha512_crypt']:
        req.append('passlib')
    if htype == 'bcrypt':
        req.append('bcrypt')
    if htype == 'scrypt':
        req.append('scrypt')
    return req


class ReadOnlyDict:
    def __contains__(self, key):
        return self._dict_data.__contains__(key)

    def __getitem__(self, key):
        return self._dict_data.__getitem__(key)

    def __iter__(self):
        return self._dict_data.__iter__()

    def __len__(self):
        return self._dict_data.__len__()

    def __str__(self):
        return self._dict_data.__str__()

    def __repr__(self):
        return self._dict_data.__repr__()

    def get(self, key, default=None):
        return self._dict_data.get(key, default)

    def items(self):
        return self._dict_data.items()

    def keys(self):
        return self._dict_data.keys()

    def values(self):
        return self._dict_data.values()

    @property
    def _dict_data(self):
        res = {}
        #  for a in dir(self):
        for a, v in self.__dict__.items():
            if a.startswith('_'):
                continue
            #  v = getattr(self, a)
            if callable(v):
                continue
            res[a] = v
        return res

class User(ReadOnlyDict):
    '''Abstract class for a user'''

    def __init__(self,
                 username=None,
                 password=None,
                 roles=None):
        '''
        - roles should be a list of Roles or a list of strings
        '''
        _roles = []
        if roles is not None:
            for r in roles:
                if is_str(r):
                    _roles.append(Role(r))
                else:
                    _roles.append(r)
        self.username = username
        self.password = password
        self.roles = _roles

class Role(ReadOnlyDict):
    '''Abstract class for a user role'''

    def __init__(self, name=None):
        self.name = name

class Session(ReadOnlyDict):
    '''Abstract class for a session'''

    def __init__(self,
                 user=None,
                 token=None,
                 expiry=None):
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
    '''Metaclass for BaseAuthHTTPRequestHandler'''

    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)
        new_class.supported_hashes = [None]
        prefT = '_transform_password_'
        prefV = '_verify_password_'

        for m in dir(new_class):
            if callable(getattr(new_class, m)) \
                    and m.startswith(prefT):
                # there is a _transform_password method for ptype
                ptype = m[len(prefT):]
                try:
                    vp = getattr(new_class, '{}{}'.format(prefV, ptype))
                except AttributeError:
                    continue

                if callable(vp):
                    # there is also a _verify_password method for ptype
                    new_class.supported_hashes.append(ptype)

        new_class.conf.password[
            'hash_type']._self_settings.allowed_values = \
            new_class.supported_hashes

        return new_class

class BaseAuthHTTPRequestHandler(
        BaseHTTPRequestHandler,
        metaclass=BaseAuthHTTPRequestHandlerMeta):
    '''Implements authentication in an abstract way

    Incomplete, must be inherited, and the child class must define
    methods for storing/getting/updating users and sessions as well as
    creating and sending tokens.

    Class attributes:
    - JSON_params: a list of keys to send with every JSON response.
      If any have not been set, they will be set as None (null).
      Default is None, meaning do not send a JSON response (but an
      HTML one)
    - secrets: can be either:
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
         {method} {path} and each value is a list of allowed users or
         roles (prefixed with '#').
         A user is one of:
           - a literal username, optionally preceded by '!' (to
             negate or deny access)
           - None (anyone, including unauthenticated)
           - '*' (any authenticated user)
         A role is a literal role name prefixed by '#', e.g. '#admin',
         optionally preceded by '!' (to negate access).
         - If no value in the list of secret path regexes matches the
           requested path, then anyone is granted access. Otherwise,
           the first (in order) regex that matched the requested path
           determines if the user is allowed or not:
           - It is allowed explicitly if {user} is given in the list
             of users or #{role} is given for any of the user's roles
           - It is denied explicitly if !{user} is given in the list
             of users or !#{role} is given for any of the user's roles
           - It is denied implicitly if the user is not in the list
             and neither is '*' or None, and neither is any of their
             roles.
           - Checks are in the following order:
             - Allowed implicitly by None (unauth)
             - Allowed explicitly by username
             - Denied explicitly by username
             - Allowed explicitly by role
             - Denied explicitly by role
             - Allowed implicitly by *
             - Denied implicitly (none of the above)
      Example:
      secrets = [
          # all authenticated users, except service, can access /foo
          ('^[A-Z]+ /foo(/|$)', ['*', '!service']),
          # only users in the admin group can POST (POST /foo is
          # still allowed for all other than service
          ('^POST ', ['#admin']),
          # anyone can fetch /bar
          ('^GET /bar(/|$)', [None]),
          # require authentication for all other pages
          ('.*', ['*']),
      ]
      Default secrets is [], i.e. no authentication required.
    - can_create_users: A dictionary, where every key is a user role
      (<new_role>) and every value is a list of users  or roles
      (prefixed with '#') who are able to register users with role
      <new_role>. As in secrets, a username or role can be negated
      with '!'.
      - The role None as a key means the new user is assigned no
        roles.
        None and '*' in the list have the same meaning as explained in
        secrets.
      - When a new user is to be registered with a set of roles, the
        currently logged in user should be authorized to create users of
        each of the given roles. Note that access to the /register
        endpoint still needs to be granted via secrets.
      - Unlike secrets, the keys (roles) are not regular expressions,
        but comapred for literal equality. Also, if a user is to be
        created with a role that isn't listed in can_create_users,
        access is denied, i.e. can_create_users should list all
        allowed roles and who is allowed to create users of that role.
      Example:
      can_create_users = {
          None: [None],  # self-register with no role assignment
          'service': ['admin'], # admins can create service accounts
          'admin': ['admin'],   # admins can create other admins
      }
      Default can_create_users is {None: [None]}, i.e. self-register.
    - password.min_len: Minimum length of passwords.
      Default is 10.
    - password.min_charsets: Minimum number of character sets
      in passwords. Default is 3.
    - password.hash_type: the type (usually hash algorithm) to
      store passwords in. If None, passwords are stored as plaintext.
      Otherwise, supported values are:
        unsalted ones:
          md5, sha1, sha256, sha512
        salted ones (UNIX passwords):
          md5_crypt, sha1_crypt, sha256_crypt, sha512_crypt, bcrypt,
          scrypt
      If a child class wants to extend these, it should define
      _transform_password_{type} and _verify_password_{type}.
      Default is None (plaintext).
    - prune_sessions_every: Minumum number of seconds, before we will
      search for and remove expired sessions. It is checked before
      every request, so if it is 0, then old sessions are searched for
      before every request. If it is None, we never search for old
      sessions. Either way, we check if the requested session is
      expired either way, and if it is, it remove it.
    '''

    conf = Conf(
        JSON_params=ConfItem(None, allowed_types=(list, type(None))),
        secrets=ConfItem([], allowed_types=(OrderedDict, list)),
        can_create_users=OrderedDict({None: [None]}),
        password=ConfItem(
            Conf(
                min_len=10,
                min_charsets=3,
                hash_type=ConfItem(
                    None,
                    allowed_values=[None],  # updated in Meta class
                    requires=_required_hashing_modules,
                    mergeable=True,
                ),
            ),
            mergeable=True),
        prune_sessions_every=ConfItem(
            0, allowed_types=(int, type(None))),
    )
    __last_prune = curr_timestamp()
    endpoints = Endpoint(
        register={
            '$allowed_methods': {'POST'},
        },
        changepwd={
            '$allowed_methods': {'POST'},
        },
        login={
            '$allowed_methods': {'POST'},
        },
        logout={
            '$allowed_methods': {'GET', 'POST'},
        },
    )

    def __init__(self, *args, **kwargs):
        # parent's __init__ must be called at the end, since
        # SimpleHTTPRequestHandler's __init__ processes the request
        # and calls the handlers
        if self.conf.prune_sessions_every is not None:
            next_check = self.conf.prune_sessions_every \
                + self.__last_prune
            if next_check <= curr_timestamp():
                self.prune_old_sessions()
                self.__last_prune = curr_timestamp()
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
    def create_user(cls, username, password, roles=None):
        '''Should create and return a new User

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

    def send_response_auth(self, error=None):
        '''Sends the response to a one of our endpoints

        - If error is given, it must be a tuple of (code, message)
        - If the JSON_params class attribute is set, we call
          send_as_JSON (if error is given the message is sent as an
          "error" key). TODO customise the error key?
        - Otherwise we call send_response_goto
        '''

        if self.conf.JSON_params is not None:
            for k in self.conf.JSON_params:
                if k not in self.saved_params():
                    self.save_param(k, None)
            self._send_response_auth_json(error)
        else:
            self._send_response_auth_plain(error)

    def _send_response_auth_plain(self, error):
        if error is not None:
            self.send_error(code=error[0], explain=error[1])
        else:
            self.send_response_goto()

    def _send_response_auth_json(self, error):
        code = 200
        if error is not None:
            self.save_param('error', error[1])
            code = error[0]
        self.send_as_JSON(code=code)

    def denied(self):
        '''Returns 401 if resource is secret and no authentication'''

        requested = '{} {}'.format(self.command, self.pathname)
        secrets = self.conf.secrets
        try:
            secrets = OrderedDict(self.conf.secrets)
        except ValueError:
            requested = self.pathname  # match against path only
            secrets = OrderedDict([(
                '{secrets}(/|$)'.format(
                    secrets='|'.join(
                        ['{pref}{secret}'.format(
                            pref=('^' if s.startswith('/') else '/'),
                            secret=s) for s in secrets]
                    )),
                ['*'])])
        if self.pathname != '{}/login'.format(self.conf.api_prefix) \
                and self.pathname != '{}/logout'.format(
                    self.conf.api_prefix) \
                and not self.is_authorized(
                    requested, secrets, default=True, is_regex=True):
            return (401,)
        return super().denied()

    def is_authorized(
            self, val, acl_map, default=False, is_regex=True):
        '''Returns True or False if val is allowed by acl_map

        - acl_map is a dict-like reference--list of user/roles pairs.
        - val is the value to be compared to each key in acl_map.
        - If is_regex is True, then reference is a regex for val,
          otherwise equality is checked.
        '''

        def is_equal(ref, val):
            return (ref is None and val is None) or ref == val

        logger.debug('Checking authorization for {}'.format(val))
        user = None
        session = self.get_current_session()
        if session is not None:
            user = session.user
        if is_regex:
            comparator = re.search
        else:
            comparator = is_equal
        for ref, acls in acl_map.items():
            logger.debug('{} is allowed for {}'.format(ref, acls))
            if comparator(ref, val):
                if None in acls:
                    logger.debug('Anyone allowed')
                    return True
                if user is None:
                    logger.debug('Unauth denied')
                    return False
                if '!{}'.format(user.username) in acls:
                    logger.debug('Explicitly denied')
                    return False
                if user.username in acls:
                    logger.debug('Explicitly allowed')
                    return True
                for r in user.roles:
                    if '!#{}'.format(r.name) in acls:
                        logger.debug('Explicitly denied by role')
                        return False
                    if '#{}'.format(r.name) in acls:
                        logger.debug('Explicitly allowed by role')
                        return True
                if '*' in acls:
                    logger.debug('Implicitly allowed')
                    return True
                logger.debug('Implicitly denied')
                return False
        logger.debug('No match, defaulting to {}'.format(default))
        return default

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
            self.unset_session(session)
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
        if session is not None and session.token is not None:
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
          - The file contains one username:password[:roles] per line.
          - If roles is given, it is comma-separated
          - Neither username, nor password can be empty.
        - If plaintext is True, then the password is checked against
          the policy and hashed according to the password.hash_type
          class attribute; otherwise it is saved as is (the hashing
          algorithm must correspond to password.hash_type)
        '''

        def process_line(line):
            user, pwd, roles, *_ = '{}::'.format(
                line.rstrip('\r\n')).split(':')
            return (user, pwd, [r.strip(' ')
                                for r in roles.split(',') if r != ''])

        with open_path(userfile) as (ufile, _):
            for line in ufile:
                username, password, roles = process_line(line)
                try:
                    cls.new_user(username, password, roles=roles,
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
    def new_user(
            cls, username, password, roles=None, plaintext=True):
        '''Creates a user with the given password and roles

        - If plaintext is True, then the password is checked against
          the policy and hashed according to the password.hash_type
          class attribute; otherwise it is saved as is (the hashing
          algorithm must correspond to password.hash_type)
        Returns the new user.
        '''

        if not username:
            raise InvalidUsernameError(username)
        if cls.find_user(username):
            raise UserAlreadyExistsError(username)
        if plaintext:
            if not cls.password_is_strong(password):
                raise BadPasswordError(username)
            password = cls.transform_password(password)
        logger.debug('Creating user {}:{} (roles: {})'.format(
            username, password, roles))
        return cls.create_user(username, password, roles)

    @classmethod
    def change_password(
            cls, user_or_username, password, plaintext=True):
        '''Changes the password of username (no validation of current)

        - user_or_username is an instance of User or a string
        - If plaintext is True, then the password is checked against
          the policy and hashed according to the password.hash_type
          class attribute; otherwise it is saved as is (the hashing
          algorithm must correspond to password.hash_type)
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
        if username is None:
            return
        user = self.find_user(username)

        password = self.get_param('password')
        if password is None:
            password = ''

        if user is None:
            logger.debug('No such user {}'.format(username))
            return
        if self.verify_password(user, password):
            return user
        return

    @classmethod
    def verify_password(cls, user, password):
        '''Returns True or False if user's password is as given

        Uses the algorithm is given in password.hash_type (class
        attribute)
        '''

        if cls.conf.password.hash_type is None:
            return user.password == password
        verifier = getattr(
            cls, '_verify_password_{}'.format(cls.conf.password.hash_type))
        return verifier(plain=password, hashed=user.password)

    @classmethod
    def transform_password(cls, password):
        '''Returns the password hashed according to the setting

        Uses the algorithm is given in password.hash_type (class attribute)
        '''

        if cls.conf.password.hash_type is None:
            return password
        transformer = getattr(
            cls, '_transform_password_{}'.format(
                cls.conf.password.hash_type))
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
                and len(password) >= cls.conf.password.min_len
                and num_charsets(password) >= cls.conf.password.min_charsets)

    def do_register(self):
        '''Creates a new user

        Returns the user on success and None on failure
        '''

        username = self.get_param('username')
        password = self.get_param('password')
        roles = self.get_param('roles')
        # for JSON requests roles could be a list already,
        # otherwise accept a comma-separated string
        if is_str(roles):
            roles = [r.strip(' ') for r in roles.split(',')]
        if roles is None:
            roles = []
        for r in roles:
            if not self.is_authorized(
                    r,
                    self.conf.can_create_users,
                    default=False,
                    is_regex=False):
                self.send_response_auth(
                    error=(401,
                           ('You cannot create '
                            'a user of role {}').format(r)))
                return None
        try:
            user = self.new_user(username, password, roles)
        except (UserAlreadyExistsError, InvalidUsernameError,
                BadPasswordError) as e:
            self.send_response_auth(error=(400, str(e)))
            return None
        self.new_session(user)
        self.send_response_auth()
        return user

    def do_changepwd(self):
        '''Changes the password for the given username

        Returns the user on success and None on failure
        '''

        user = self.authenticate()
        if user is None:
            self.send_response_auth(
                error=(401, 'Username or password is wrong'))
            return None

        new_password = self.get_param('new_password')
        try:
            self.change_password(user, new_password, plaintext=True)
        except BadPasswordError as e:
            self.send_response_auth(error=(400, str(e)))
            return None
        self.new_session(user)
        self.send_response_auth()
        return user

    def do_login(self):
        '''Issues a random cookie and saves it

        Returns the user on success and None on failure
        '''

        user = self.authenticate()
        if user is None:
            self.expire_current_session()
            self.send_response_auth(
                error=(401, 'Username or password is wrong'))
            return None
        self.new_session(user)
        self.send_response_auth()
        return user

    def do_logout(self):
        '''Clears the cookie from the browser and saved sessions

        Returns True
        '''

        self.expire_current_session()
        self.send_response_auth()
        return True
