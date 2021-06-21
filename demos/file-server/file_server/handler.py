import logging
import re
import os
import errno

#  from sqlalchemy.orm.exc import NoResultFound

from mixnmatchttp import endpoints
from mixnmatchttp.handlers import methodhandler, \
    AuthJWTDatabaseHTTPRequestHandler
from mixnmatchttp.handlers.exc import InvalidRequestError
#  from mixnmatchttp.db import filter_results, \
#      object_from_dict, bulk_objects_from_dicts, \
#      update_from_dict
from mixnmatchttp.utils import is_seq_like, is_map_like, \
    datetime_from_timestamp, datetime_from_str, DictNoClobber


logger = logging.getLogger(__name__)
__all__ = ['Handler']


class Handler(AuthJWTDatabaseHTTPRequestHandler):
    user_conf = None  # to be set by App
    conf = DictNoClobber(
        can_create_users=[
            ('admin', ['#admin']),
            ('viewer', ['#admin'])],
        secrets=[
            ('^DELETE /api/', ['#admin']),
            ('^[A-Z]+ /api/', ['#viewer']),
            ('.*', [None])]
    )
    endpoints = endpoints.Endpoint(
        path={
            '$allowed_methods': {'GET', 'PUT', 'DELETE'},
            '$nargs': '*',
        }
    )

    def list_directory_raw(self, path):
        '''Returns a tuple of list of directories and files'''

        def _raise(e):
            raise e

        try:
            for root, dirs, files in os.walk(path, onerror=_raise):
                self.send_as_JSON({'dirs': dirs, 'files': files})
        except OSError as e:
            if e.errno == errno.ENOENT:
                self.send_error(404)
            elif e.errno == errno.EACCES:
                self.send_error(403)
            elif e.errno == errno.ENOTDIR:
                raise
            else:
                self.send_error(500)
            return None, None

    def do_GET_path(self):
        self.strip_path_prefix_re('path/?')
        logger.debug('Retrieving {}'.format(self.pathname))
        try:
            self.send_file(as_attachment=True)
        except IsADirectoryError:
            logger.debug("It's a directory")
            path = self.pathname[1:]
            if path == '':
                path = '.'  # will raise IsADirectoryError
            return self.list_directory_raw(path)

    def do_DELETE_path(self):
        # TODO
        self.strip_path_prefix_re('/path/?')
        logger.debug('Deleting {}'.format(self.pathname))
        self.send_error(405)

    def do_PUT_path(self):
        # TODO
        self.strip_path_prefix_re('/path/?')
        logger.debug('Modifying {}'.format(self.pathname))
        self.send_error(405)

    # Disable caching except for jquery
    def no_cache(self):
        return (not re.search('/jquery-[0-9\.]+(\.min)?\.js',
                              self.pathname)) or super().no_cache()

    def require_list_of_dicts(self, arg=None):
        if arg is None:
            arg = self.params
        if not is_seq_like(arg):
            raise InvalidRequestError(
                'Expected a list of dictionaries')
        for a in arg:
            self.require_dict(a)

    def require_dict(self, arg=None):
        if arg is None:
            arg = self.params
        if not is_map_like(arg):
            raise InvalidRequestError(
                'Expected a dictionary of key--value pairs')
