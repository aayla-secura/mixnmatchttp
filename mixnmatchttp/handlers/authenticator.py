from __future__ import division
#  from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from builtins import int
from builtins import str
from future import standard_library
standard_library.install_aliases()
import logging
import re
from random import randint

from .. import endpoints
from ..common import param_dict
from .base import BaseHTTPRequestHandler

_logger = logging.getLogger(__name__)

class AuthHTTPRequestHandler(BaseHTTPRequestHandler):
    _secrets = () # immutable
    _is_SSL = False
    _cookie_len = 20
    _max_sessions = 10
    _endpoints = endpoints.Endpoints(
            login={ },
            logout={ },
            )
    __sessions = [] # mutable and must be a class attribute for
                    # sessions to persist

    def denied(self):
        '''Returns 401 if resource is secret and authentication is invalid'''

        if self.is_secret() and \
             self.get_session() not in self.__sessions:
            return (401,)
        return super(AuthHTTPRequestHandler, self).denied()

    def is_secret(self):
        '''Returns whether path requires authentication.'''

        _logger.debug('{} secrets'.format(len(self._secrets)))
        for s in self._secrets:
            _logger.debug('{} is secret'.format(s))
            if re.search('{}{}(/|$)'.format(
                ('^' if s[0] == '/' else '(/|^)'), s), self.pathname):
                return True

        return False

    def get_session(self):
        '''Returns the session cookie'''

        cookies = param_dict(self.headers.get('Cookie'))
        if not cookies:
            _logger.debug('No cookies given')
            session = None
        else:
            try:
                session = cookies['SESSION']
            except KeyError:
                _logger.debug('No SESSION cookie given')
                session = None
            else:
                _logger.debug('Cookie is {}valid'.format(
                    '' if session in self.__sessions else 'not '))

        return session

    def rm_session(self):
        '''Invalidate the session server-side'''

        session = self.get_session()
        try:
            self.__sessions.remove(session)
        except ValueError:
            pass

    def do_logout(self, sub, args):
        '''Clears the cookie from the browser and the saved sessions'''

        self.rm_session()
        self.send_response_goto(headers={'Set-Cookie': 'SESSION='})

    def do_login(self, sub, args):
        '''Issues a random cookie and saves it'''

        self.rm_session()
        cookie = '{:02x}'.format(
            randint(0, 2**(4*self._cookie_len)-1))
        if len(self.__sessions) >= self._max_sessions:
            # remove a third of the oldest sessions
            _logger.debug('Purging old sessions')
            del self.__sessions[int(self._max_sessions/3):]
        self.__sessions.append(cookie)

        self.send_response_goto(headers={'Set-Cookie':
            'SESSION={}; path=/; {}HttpOnly'.format(
                cookie, ('Secure; ' if self._is_SSL else ''))
            })

