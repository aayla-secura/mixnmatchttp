from ..._py2 import *

from .api import BaseAuthHTTPRequestHandler, User


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
    def create_user(cls, username, password, roles=None):
        '''Creates and returns a new User'''

        u = User(username=username, password=password, roles=roles)
        cls.__users[username] = u
        return u

    @classmethod
    def update_user(cls, user, **kargs):
        '''Does nothing'''

        pass
