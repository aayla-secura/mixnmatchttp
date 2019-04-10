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

from .. import endpoints
from ..common import param_dict
from .base import BaseHTTPRequestHandler, DecodingError

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
    '''Exception raised when a user is created with an existing username'''

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

class AuthHTTPRequestHandler(BaseHTTPRequestHandler):
    _secrets = () # immutable
    _userfile = None
    _is_SSL = False
    _cookie_name = 'SESSION'
    _cookie_len = 20
    _min_pwdlen = 10
    _max_sessions = 10
    _endpoints = endpoints.Endpoint(
            changepwd={
                '$allowed_methods': {'GET', 'POST'},
                },
            login={
                '$allowed_methods': {'GET', 'POST'},
                },
            logout={ },
            )
    __sessions = [] # mutable and must be a class attribute for
                    # sessions to persist
    __users = {}    # mutable, as __sessions

    def __init__(self, *args, **kwargs):
        '''Implements username:password authentication'''

        # parent's __init__ must be called at the end, since
        # SimpleHTTPRequestHandler's __init__ processes the request
        # and calls the handlers
        self.load_users()
        self.__cookie = None
        super().__init__(*args, **kwargs)

    def set_cookie(self, cookie=None):
        '''Saves the cookie to be sent with this response
        
        If cookie is None, creates a new session.'''

        if cookie is None:
            cookie = self.new_session()
        flags = '{}HttpOnly'.format(
                'Secure; ' if self._is_SSL else '')
        self.__cookie = '{}={}; path=/; {}'.format(
                self._cookie_name, cookie, flags)

    def clear_cookie(self):
        '''Sets an empty cookie to be sent with this response
        
        Also invalidates the session.'''

        self.rm_session()
        self.__cookie = '{}='.format(self._cookie_name)

    def end_headers(self):
        if self.__cookie is not None:
            self.send_header('Set-Cookie', self.__cookie)
        super().end_headers()

    def denied(self):
        '''Returns 401 if resource is secret and authentication is invalid'''

        if self.is_secret() and \
             self.get_session() not in self.__sessions:
            return (401,)
        return super().denied()

    def is_secret(self):
        '''Returns whether path requires authentication'''

        logger.debug('{} secrets'.format(len(self._secrets)))
        for s in self._secrets:
            logger.debug('{} is secret'.format(s))
            if re.search('{}{}(/|$)'.format(
                ('^' if s[0] == '/' else '(/|^)'), s), self.pathname):
                return True

        return False

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
                logger.debug('No {} cookie given'.format(self._cookie_name))
                session = None
            else:
                logger.debug('Cookie is {}valid'.format(
                    '' if session in self.__sessions else 'not '))

        return session

    def rm_session(self):
        '''Invalidate the session server-side'''

        session = self.get_session()
        try:
            self.__sessions.remove(session)
        except ValueError:
            pass

    def new_session(self):
        '''Invalidate old session and generates a new session cookie'''

        self.rm_session()
        cookie = '{:02x}'.format(randint(0, 2**(4*self._cookie_len)-1))
        if len(self.__sessions) >= self._max_sessions:
            # remove a third of the oldest sessions
            logger.debug('Purging old sessions')
            del self.__sessions[int(self._max_sessions/3):]
        self.__sessions.append(cookie)
        return cookie

    def load_users(self):
        '''Appends user credentials to the list stored in memory
        
        filename is a file containing one username:password per line.
        Neither username, nor password can be empty.
        '''

        if not self._userfile:
            return

        # don't handle IOError here
        with open(self._userfile, 'r') as f:
            for line in f:
                username, _, password = \
                        line.rstrip("\r\n").partition(':')
                try:
                    self.create_user(username, password)
                except (UserAlreadyExistsError, InvalidUsernameError,
                        BadPasswordError) as e:
                    logger.debug('{}'.format(str(e)))

    def purge_users(self, filename):
        '''Deletes all users from memory'''

        self.__users.clear()

    def authenticate(self):
        '''Returns True or False if username:password is valid'''

        if not self._userfile:
            return True

        username = self.get_param('username')
        password = self.get_param('password')
        try:
            if self.__users[username] != password:
                logger.debug(
                        'Wrong password for user {}'.format(username))
                raise ValueError
        except (KeyError, ValueError):
            return False

        return True

    def password_ok(self, password):
        '''Simple password policy; only checks the length'''

        return password and len(password) >= self._min_pwdlen

    def create_user(self, username, password):
        '''Creates a user with a given password
        
        Returns True on success, False otherwise
        '''

        self.__set_password(username, password, new_user=True)

    def change_password(self, username, password):
        '''Changes the password of username
        
        Returns True on success, False otherwise
        '''

        self.__set_password(username, password, new_user=False)

    def __set_password(self, username, password, new_user):
        '''Sets the password of username
        
        Returns True on success, False otherwise
        
        If new_user is True, then username must not exist.
        Othersie username must exist.
        '''

        try:
            self.__users[username]
            if new_user:
                raise UserAlreadyExistsError('{}'.format(username))
        except KeyError:
            if not new_user:
                raise NoSuchUserError('{}'.format(username))

        if not username:
            raise InvalidUsernameError('{}'.format(username))
        if not self.password_ok(password):
            raise BadPasswordError('{}'.format(username))

        self.__users[username] = password

    def do_changepwd(self, ep):
        '''Changes the password for the given username'''

        if self.authenticate():
            username = self.get_param('username')
            new_password = self.get_param('new_password')
            try:
                self.change_password(username, new_password)
            except (BadPasswordError, NoSuchUserError, InvalidUsernameError) as e:
                self.send_error(400, explain=str(e))
                return
            self.set_cookie()
            self.send_response_goto()
        else:
            self.clear_cookie()
            self.send_error(401, explain='Username or password is wrong')

    def do_logout(self, ep):
        '''Clears the cookie from the browser and the saved sessions'''

        self.clear_cookie()
        self.send_response_goto('')

    def do_login(self, ep):
        '''Issues a random cookie and saves it'''

        if self.authenticate():
            self.set_cookie()
            self.send_response_goto()
        else:
            self.clear_cookie()
            self.send_error(401,
                    explain='Username or password is wrong')
