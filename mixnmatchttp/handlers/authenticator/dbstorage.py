from ..._py2 import *

import logging
from datetime import datetime

from sqlalchemy.orm.exc import NoResultFound

from ...poller import Poller
from ...utils import datetime_from_timestamp
from ...db import DBConnection, \
    filter_results, object_from_dict
from .api import BaseAuthHTTPRequestHandler, \
    User, Role, Session
from .dbapi import DBBase, DBUser, DBSession
from .dbutils import needs_db, needs_db_error_response_handling


logger = logging.getLogger(__name__)


class BaseAuthSQLAlchemyORMHTTPRequestHandler(
        BaseAuthHTTPRequestHandler):
    '''Implements database storage of users and sessions

    WARNING: If you match it with BaseAuthJWTHTTPRequestHandler, then
    in the MRO this class must take precedence, i.e. be first.
    Also, if any new endpoints that use the storage are defined, they
    must be decorated with the
    needs_db_error_response_handling(DBBase) decorator, see below.

    Incomplete, must be inherited, and the child class must define
    methods for creating and sending tokens.

    Default of _prune_sessions_every changed from 0 (every request) to
    300 (every 5 minutes).
    '''

    _prune_sessions_every = 300

    @needs_db(DBBase)
    @classmethod
    def find_session(cls, db, token, must_exist=False):
        '''Returns the Session corresponding to the token'''

        try:
            return filter_results(
                db, DBSession, {'token': token}, expect_one=True)
        except NoResultFound:
            if must_exist:
                raise
            return None

    @needs_db(DBBase)
    @classmethod
    def get_all_sessions(cls, db):
        '''Returns a list of Sessions'''

        return db.query(DBSession).all()

    @needs_db(DBBase)
    @classmethod
    def add_session(cls, db, session):
        '''Records the Session'''

        # session is an instance of Session; need to convert to
        # DBSession
        expiry = session.expiry
        user = cls.find_user(session.user.username, must_exist=True)
        token = session.token
        if expiry is not None and not isinstance(expiry, datetime):
            # SQLAlchemy loses information on the timezone, so we need
            # to create an object in the local timezone
            expiry = datetime_from_timestamp(
                expiry, to_utc=False, from_utc=True, relative=False)
        db.add(DBSession(user=user, token=token, expiry=expiry))

    @needs_db(DBBase)
    @classmethod
    def rm_session(cls, db, session):
        '''Deletes the Session'''

        db_session = cls.find_session(session.token, must_exist=True)
        db.delete(db_session)

    @needs_db(DBBase)
    @classmethod
    def find_user(cls, db, username, must_exist=False):
        '''Returns the User for that username'''

        try:
            return filter_results(
                db, DBUser, {'username': username}, expect_one=True)
        except NoResultFound:
            if must_exist:
                raise
            return None

    @needs_db(DBBase)
    @classmethod
    def create_user(cls, db, username, password, roles=None):
        '''Creates and returns a new User'''

        user = User(  # dummy that we can use as a dict
            username=username, password=password, roles=roles)
        db_user = object_from_dict(db, DBUser, user, add=True)
        return db_user

    @needs_db(DBBase)
    @classmethod
    def update_user(cls, db, user):
        '''Adds the user to the session to be commited'''

        db.add(user)

    # All methods which call our wrapped methods (defined in
    # BaseAuthSQLAlchemyORMHTTPRequestHandler) should close the
    # session and catch errors
    @needs_db_error_response_handling(DBBase)
    def denied(self, db):
        return super().denied()

    @needs_db_error_response_handling(DBBase)
    def do_register(self, db):
        return super().do_register()

    @needs_db_error_response_handling(DBBase)
    def do_changepwd(self, db):
        return super().do_changepwd()

    @needs_db_error_response_handling(DBBase)
    def do_login(self, db):
        return super().do_login()

    @needs_db_error_response_handling(DBBase)
    def do_logout(self, db):
        return super().do_logout()

    @needs_db_error_response_handling(DBBase)
    def do_authtoken(self, db):
        return super().do_authtoken()

    @classmethod
    def enable_client_cache(cls, name, base):
        '''Add a new Poller named <name> that monitors DB changes to base

        - base is a declarative base which must have been configured
          via DBConnection(base, url, ...).
        '''

        def before_commit(session):
            if not session._is_clean():
                logger.debug('DB changed')
                cls.pollers[name].update()

        cls.pollers[name] = Poller()
        DBConnection.get(base).listen(
            'before_commit', before_commit)
