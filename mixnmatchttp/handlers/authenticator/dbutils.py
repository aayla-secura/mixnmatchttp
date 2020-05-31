from ..._py2 import *

from sqlalchemy.exc import DatabaseError

from functools import partial
from wrapt import decorator
from datetime import datetime
import logging

from ...utils import is_map_like, datetime_to_str
from ...db import DBConnection, is_mapper, object_to_dict
from ..base import ServerError, InvalidRequestError
from .dbapi import DBBase


logger = logging.getLogger(__name__)


def json_serializer(obj, short=False, short_mappings={}):
    '''Supports mapper classes and dict-like objects'''

    if is_mapper(obj.__class__):
        return object_to_dict(
            obj, short=short, short_mappings=short_mappings)
    elif is_map_like(obj):
        return dict(obj)
    elif isinstance(obj, datetime):
        return datetime_to_str(obj)
    return repr(obj)

def needs_db_response_handling(base,
                               poller=None,
                               json_serializer=json_serializer):
    '''Passes a session and sends the returned object as JSON

    The wrapped method should be an endpoint handler and must not send
    anything, instead return the response body as an object.
    - If poller is given, it should be the name of a poller that has
      been enabled via
      BaseAuthSQLAlchemyORMHTTPRequestHandler.enable_client_cache;
      then we support If-None-Match request headers and ETag response
      header via the current tag of that poller.
    - json_serializer is used to serialize the returned object.
    '''

    @decorator
    def _decorator(wrapped, self, args, kwargs):
        dconn = DBConnection.get(base)
        with dconn.session_context(reraise=False) as db:
            # check if client cache is up to date
            if poller is not None and self.command == 'GET':
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
                raise  # so session_context cleans up

            if poller is not None:
                self.save_header(
                    'ETag', self.pollers[poller].latest)
            if result is None:
                self.send_response_empty(204)
            else:
                short = self.get_param('short', self.query)
                if short is not None:
                    try:
                        short = int(short)
                    except ValueError:
                        if short.lower() in ['false', 'no']:
                            short = False
                        elif short == '':
                            short = True
                short = bool(short)
                self.send_as_json(result, serializer=partial(
                    json_serializer, short=short))

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
                raise  # so session_context cleans up

    return _decorator

def needs_db(base):
    '''Passes a session of base to the wrapped method

    The session is commited but not closed.
    '''

    @decorator
    def _decorator(wrapped, self, args, kwargs):
        db = DBConnection.get(base).session()
        result = wrapped(db, *args, **kwargs)
        db.commit()
        return result

    return _decorator
