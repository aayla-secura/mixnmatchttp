from __future__ import division
#  from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from builtins import *
from future import standard_library
standard_library.install_aliases()
import logging
import re
from random import randint
try:
    # python2
    from collections import _abcoll
except ImportError:
    # python3
    from collections import abc as _abcoll

from .. import endpoints
from ..common import param_dict, date_from_timestamp, curr_timestamp
from .base import BaseHTTPRequestHandler

__all__ = [
    'AuthError',
    'UserAlreadyExistsError',
    'NoSuchUserError',
    'InvalidUsernameError',
    'BadPasswordError',
    'AuthHTTPRequestHandler',
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
    '''Exception raised when a user is created with an invalid username'''

    def __init__(self, username):
        super().__init__('Invalid username {}'.format(username))

class BadPasswordError(AuthError):
    '''Exception raised when new password is invalid'''

    def __init__(self, username):
        super().__init__('Bad password for user {}'.format(username))

class BaseAuthHTTPRequestHandler(BaseHTTPRequestHandler):
    # _secrets can be either an iterable of absolute or relative paths
    # which require any authentication (deprecated), or a more
    # fine-grained filter: a dictionary where each key is a regex for
    # {method} {path} and each value is a list of allowed usernames
    _secrets = ()
    _min_pwdlen = 10  # TODO complexity
    _endpoints = endpoints.Endpoint(
        changepwd={
            '$allowed_methods': {'GET', 'POST'},
        },
        login={
            '$allowed_methods': {'GET', 'POST'},
        },
        logout={},
    )
    __users = {}  # username-password key-value
    # in __sessions, each key is a session token, each value is
    # a dictionary of user={username} and expiry={timestamp}
    __sessions = {}

    def __init__(self, *args, **kwargs):
        # parent's __init__ must be called at the end, since
        # SimpleHTTPRequestHandler's __init__ processes the request
        # and calls the handlers
        self.prune_old_sessions()
        super().__init__(*args, **kwargs)

    def denied(self):
        '''Returns 401 if resource is secret and no authentication'''

        if self.pathname != '/login' and not self.is_authorized():
            return (401,)
        return super().denied()

    def is_authorized(self):
        '''Returns True or False if request is authorized'''

        user = self.get_logged_in_user()
        if isinstance(self._secrets, _abcoll.Sequence):
            return self._is_authorized_plain(user)
        for regex, users in self._secrets.items():
            logger.debug('{} is allowed for {}'.format(regex, users))
            if re.search(regex, '{} {}'.format(
                    self.command, self.pathname)):
                if user in users:
                    return True
                return False
        return True  # not authentication required

    def _is_authorized_plain(self, user):
        logger.warning(
            'Using an iterable for _secrets is deprecated. Use '
            'a dictionary of "{method} {path}" [{users}] instead.')
        for s in self._secrets:
            logger.debug('{} is secret'.format(s))
            if re.search('{}{}(/|$)'.format(
                ('^' if s[0] == '/' else '(/|^)'),
                    s), self.pathname):
                if user is None:
                    return False
                return True
        return True  # not authentication required

    def get_session(self):
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
        '''Ensures the token is sent in the response

        Child class should implement
        '''

        raise NotImplementedError

    def unset_session(self, user, session):
        '''Ensures the token is cleared client-side

        Child class should implement
        '''

        raise NotImplementedError

    @classmethod
    def get_user_from_session(cls, session):
        '''Returns the user for the given session

        Child class may override this to implement DB access.
        '''

        try:
            return cls.__sessions[session]['user']
        except KeyError:
            return None

    @classmethod
    def add_session(cls, user, session, expiry):
        '''Records the session

        Child class may override this to implement DB access.
        '''

        logger.debug('Session {} expires at {}'.format(
            session, expiry))
        cls.__sessions[session] = {
            'user': user,
            'expiry': expiry}

    def rm_session(self):
        '''Invalidate the session server-side

        Child class may override this to implement DB access.
        '''

        session = self.get_session()
        user = self.get_logged_in_user()
        try:
            del self.__sessions[session]
        except KeyError:
            return
        self.unset_session(user, session)

    def new_session(self, user):
        '''Invalidate the old session and generate a new one'''

        self.rm_session()
        session, expiry = self.new_session_token(user)
        self.add_session(user, session, expiry)
        self.set_session(user, session, expiry)
        return session

    @classmethod
    def new_session_token(cls, user):
        '''Should return a tuple of new session token, expiry

        Child class should implement
        '''

        raise NotImplementedError

    @classmethod
    def user_exists(cls, user):
        '''Returns True or False if user exists

        Child class may override this to implement DB access.
        '''

        return user in cls.__users

    @classmethod
    def load_users_from_file(cls, userfile):
        '''Adds users from the userfile

        userfile can be a string (filename) or a file handle
        - The file contains one username:password per line.
        - Neither username, nor password can be empty.
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
                    cls.create_user(username, password)
                except (UserAlreadyExistsError, InvalidUsernameError,
                        BadPasswordError) as e:
                    logger.debug('{}'.format(str(e)))

    @classmethod
    def prune_old_sessions(cls):
        '''Remove expired sessions'''

        logger.debug('Pruning old sessions')
        sessions = cls.__sessions.keys()
        for s in sessions:
            exp = cls.__sessions[s]['expiry']
            if exp is not None and exp <= curr_timestamp():
                logger.debug('Removing session {}'.format(s))
                del cls.__sessions[s]

    @classmethod
    def create_user(cls, username, password):
        '''Creates a user with the given password

        Returns True on success, False otherwise
        '''

        logger.debug('Creating user {}:{}'.format(
            username, password))
        if not username:
            raise InvalidUsernameError(username)
        if cls.user_exists(username):
            raise UserAlreadyExistsError(username)
        if not cls.is_password_good(password):
            raise BadPasswordError(username)
        return cls._create_user(username, password)

    @classmethod
    def change_password(cls, username, password):
        '''Changes the password of username. In memory only!

        Returns True on success, False otherwise
        '''

        if not cls.user_exists(username):
            raise NoSuchUserError(username)
        if not cls.is_password_good(password):
            raise BadPasswordError(username)
        return cls._change_password(username, password)

    @classmethod
    def _create_user(cls, username, password):
        '''Creates a new user with the given password

        Returns True
        Child class may override this to implement DB access.
        '''

        cls.__users[username] = password
        return True

    @classmethod
    def _change_password(cls, username, password):
        '''Sets the password of username (no check)

        Returns True
        Child class may override this to implement DB access.
        '''

        cls.__users[username] = password
        return True

    def authenticate(self):
        '''Returns True or False if username:password is valid

        username and password taken from request parameters
        '''

        username = self.get_param('username')
        password = self.get_param('password')
        return self.is_password_correct(username, password)

    @classmethod
    def is_password_correct(cls, username, password):
        '''Returns True or False if username:password is valid

        Child class may override this to implement DB access.
        '''

        try:
            if cls.__users[username] == password:
                return True
        except KeyError:
            logger.debug(
                'No such user {}'.format(username))
            return False

        logger.debug(
            'Wrong password for user {}'.format(username))
        return False

    @classmethod
    def is_password_good(cls, password):
        '''Simple password policy; only checks the length'''

        return password and len(password) >= cls._min_pwdlen

    def do_changepwd(self):
        '''Changes the password for the given username'''

        if not self.authenticate():
            self.send_error(401, explain='Username or password is wrong')
            return

        username = self.get_param('username')
        new_password = self.get_param('new_password')
        try:
            self.change_password(username, new_password)
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
            self.rm_session()
            self.send_error(
                401, explain='Username or password is wrong')

    def do_logout(self):
        '''Clears the cookie from the browser and the saved sessions'''

        self.rm_session()
        self.send_response_goto()

class AuthCookieHTTPRequestHandler(BaseAuthHTTPRequestHandler):
    '''username:password authentication and cookie-based session'''

    _is_SSL = False  # sets the Secure cookie flag if True
    _cookie_name = 'SESSION'
    _cookie_len = 20
    _cookie_lifetime = None  # in seconds; if unset, it's a session cookie
    _SameSite = None  # can be 'lax' or 'strict'

    def __init__(self, *args, **kwargs):
        self.__cookie = None
        super().__init__(*args, **kwargs)

    def get_logged_in_user(self):
        session = self.get_session()
        if session is None:
            return None
        return self.get_user_from_session(session)

    @classmethod
    def new_session_token(cls, user):
        expiry = cls._cookie_lifetime
        if expiry is not None:
            expiry += curr_timestamp()
        return ('{:02x}'.format(
            randint(0, 2**(4 * cls._cookie_len) - 1)), expiry)

    def get_session(self):
        '''Returns the session cookie'''

        cookies = param_dict(self.headers.get('Cookie'))
        if not cookies:
            logger.debug('No cookies given')
            session = None
        else:
            try:
                session = cookies[self._cookie_name]
            except KeyError:
                logger.debug('No {} cookie given'.format(
                    self._cookie_name))
                session = None
            else:
                logger.debug('Cookie is {}valid'.format(
                    '' if session in
                    self._BaseAuthHTTPRequestHandler__sessions
                    else 'not '))

        return session

    def set_session(self, user, session, expiry):
        '''Saves the cookie to be sent with this response'''

        flags = '{}{}HttpOnly; '.format(
            'Secure; ' if self._is_SSL else '',
            'SameSite={}; '.format(
                self._SameSite) if self._SameSite is not None else '')
        if expiry is not None:
            expiry = 'Expires={}; '.format(date_from_timestamp(
                expiry))
        self.__cookie = \
            '{name}={value}; path=/; {expiry}{flags}'.format(
                name=self._cookie_name,
                value=session,
                expiry=expiry,
                flags=flags)

    def unset_session(self, user=None, session=None):
        '''Sets an empty cookie to be sent with this response'''

        expiry = 'Expires={}'.format(date_from_timestamp(0))
        self.__cookie = '{name}=; path=/; {expiry}'.format(
            name=self._cookie_name, expiry=expiry)

    def end_headers(self):
        if self.__cookie is not None:
            self.send_header('Set-Cookie', self.__cookie)
        super().end_headers()

class AuthJWTHTTPRequestHandler(BaseAuthHTTPRequestHandler):
    '''username:password authentication and token-based session'''

    _jwt_lifetime = 15  # in minutes
    _refresh_token_lifetime = 1440  # in minutes
    pass

class AuthHTTPRequestHandler(AuthCookieHTTPRequestHandler):
    def __init__(self, *args, **kargs):
        logger.warning(
            'AuthHTTPRequestHandler is deprecated. '
            'Use AuthCookie HTTPRequestHandler or '
            'AuthJWTHTTPRequestHandler instead.')
        super().__init__(*args, **kargs)
