#  from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import str
from future import standard_library
standard_library.install_aliases()
import logging
import uuid

from .. import endpoints,cache
from .base import BaseHTTPRequestHandler, DecodingError

_logger = logging.getLogger(__name__)

class CachingHTTPRequestHandler(BaseHTTPRequestHandler):
    cache = cache.Cache()
    _endpoints = endpoints.Endpoints(
            echo={
                '': {
                    'allowed_methods': {'POST'},
                    },
                },
            cache={
                '': {
                    'allowed_methods': {'GET', 'POST'},
                    'args': 1,
                    },
                'clear': {
                    'args': endpoints.ARGS_OPTIONAL,
                    },
                'new': { },
                },
            )

    def do_echo(self, sub, args):
        '''Decodes the request and returns it as the response body'''

        try:
            page = self.decode_body()
        except DecodingError as e:
            self.send_error(400, explain=str(e))
            return
        self.render(page)

    def do_cache(self, sub, name):
        '''Saves, retrieves or clears a cached page'''

        if not name:
            name = None # cache.clear expects non-empty or None, not ''

        if sub == 'clear':
            self.cache.clear(name)
            self.send_response_empty(204)
        elif sub == 'new':
            self.render({
                'data': '{}'.format(
                    uuid.uuid4()).encode('utf-8'),
                'type': 'text/plain'})
        else:
            assert not sub # did we forget to handle a command

            if self.command == 'GET':
                try:
                    page = self.cache.get(name)
                except (cache.PageClearedError, cache.PageNotCachedError) as e:
                    self.send_error(500, explain=str(e))
                else:
                    self.render(page)

            else:
                try:
                    page = self.decode_body()
                except DecodingError as e:
                    self.send_error(400, explain=str(e))
                    return
                try:
                    self.cache.save(name, page)
                except cache.CacheError as e:
                    self.send_error(500, explain=str(e))
                else:
                    self.send_response_empty(204)
