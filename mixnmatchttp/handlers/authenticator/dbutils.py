from ..._py2 import *

from sqlalchemy.exc import DatabaseError

from functools import partial
from wrapt import decorator
from datetime import datetime
import logging

from ...utils import is_map_like, datetime_to_str
from ...db import DBConnection, is_mapper, object_to_dict
from ...db.exc import ServerDBError
from ..exc import ServerError, InvalidRequestError
from .dbapi import DBBase


logger = logging.getLogger(__name__)


def json_serializer(obj, **kargs):
    '''Supports mapper classes and dict-like objects

    - kargs are passed to object_to_dict
    '''

    if is_mapper(obj.__class__):
        return object_to_dict(obj, **kargs)
    elif is_map_like(obj):
        return dict(obj)
    elif isinstance(obj, datetime):
        return datetime_to_str(obj)
    return repr(obj)

def needs_db_response_handling(base,
                               poller=None,
                               poll_any=False,
                               send_None=True,
                               json_serializer=json_serializer):
    '''Passes a session and sends the returned object as JSON

    The wrapped method should be an endpoint handler and must not send
    anything, instead return the response body as an object.
    - If poller is given, it should be the name of a poller that has
      been enabled via
      BaseAuthSQLAlchemyORMHTTPRequestHandler.enable_client_cache;
      then we support If-None-Match request headers and ETag response
      header via the current tag of that poller
    - If poll_any is True, then we always inspect the If-None-Match.
      Otherwise, only in GET requests.
    - If send_None is True, then a 204 is sent if the wrapped method
      returns None. Otherwise nothing is sent, i.e. the wrapped method
      must send the response itself.
    - json_serializer is used to serialize the returned object.
    '''

    @decorator
    def _decorator(wrapped, self, args, kwargs):
        dconn = DBConnection.get(base)
        with dconn.session_context(reraise=False) as db:
            # check if client cache is up to date
            if poller is not None \
                    and (self.command == 'GET' or poll_any):
                current = self.headers.get('If-None-Match')
                if current is not None:
                    if self.pollers[poller].is_match(
                            current.strip('"')):
                        self.send_response_empty(304)
                        return
            try:
                result = wrapped(db, *args, **kwargs)
                # commit so that new objects get an ID
                db.commit()
            except InvalidRequestError as e:
                self.save_param('error', str(e))
                self.send_as_json(code=400)
                return
            except (DatabaseError, ServerError) as e:
                self.save_param('error', str(e))
                self.send_as_json(code=500)
                raise ServerDBError(e)  # so session_context cleans up

            if poller is not None:
                self.save_header(
                    'ETag', self.pollers[poller].latest)
            if result is None:
                if send_None:
                    self.send_response_empty(204)
            else:
                max_depth = self.get_param('max_depth', self.query)
                if max_depth is not None:
                    try:
                        max_depth = int(max_depth)
                        if max_depth < 0:
                            raise ValueError
                    except ValueError:
                        self.save_param(
                            'error',
                            ('max_depth must be a non-negative '
                             'integer'))
                        self.send_as_json(code=400)
                        return
                self.send_as_json(result, serializer=partial(
                    json_serializer, max_depth=max_depth))

    return _decorator

def needs_db_error_response_handling(base):
    '''Passes a session, catches a DB error and sends an error

    The wrapped method may or may not be an endpoint handler, but
    should send its own response except in case of a DB error.
    '''

    @decorator
    def _decorator(wrapped, self, args, kwargs):
        dconn = DBConnection.get(base)
        with dconn.session_context(reraise=False) as db:
            try:
                return wrapped(db, *args, **kwargs)
            except (DatabaseError, ServerError) as e:
                self.save_param('error', str(e))
                self.send_as_json(code=500)
                raise ServerDBError(e)  # so session_context cleans up

    return _decorator

def needs_db(base, reraise=False, close_at_end=False, **kargs):
    '''Passes a session of base to the wrapped method

    - The session is commited but not closed, unless close_at_end is
      True.
    - Any additional keyword arguments are passed to
      DBConnection.session_context
    '''

    @decorator
    def _decorator(wrapped, self, args, kwargs):
        dconn = DBConnection.get(base)
        with dconn.session_context(
                reraise=reraise,
                close_at_end=close_at_end, **kargs) as db:
            return wrapped(db, *args, **kwargs)

    return _decorator

def needs_db_conn(base):
    '''Passes a session connection of base to the wrapped method'''

    @decorator
    def _decorator(wrapped, self, args, kwargs):
        dconn = DBConnection.get(base)
        return wrapped(dconn, *args, **kwargs)

    return _decorator
