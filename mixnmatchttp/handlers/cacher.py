#  from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import str
from future import standard_library
standard_library.install_aliases()
import logging
import uuid
import mimetypes

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

    def decode_page(self):
        '''Decodes the request which contains a page
        
        It must contain the following parameters:
            - data: the content of the page
            - type: the content type

        Returns the same data/type dictionary but with a decoded
        content
        '''

        if self.ctype in ['application/json', 'text/json']:
            data_decoder = self.b64_data
            type_decoder = lambda x: x
        elif self.ctype == 'application/x-www-form-urlencoded':
            data_decoder = self.url_data
            type_decoder = self.url_data
        else:
            raise DecodingError(
                'Unknown Content-Type: {}'.format(self.ctype))
            return

        try:
            body_enc = self.params['data']
        except KeyError:
            raise DecodingError('No "data" parameter present!')
        _logger.debug('Encoded body: {}'.format(body_enc))

        try:
            page_ctype = type_decoder(self.params['type']).split(';',1)[0]
            if page_ctype not in mimetypes.types_map.values():
                raise ValueError('Unsupported Content-type')
        except (KeyError, ValueError):
            page_ctype = 'text/plain'
        else:
            _logger.debug('Content-Type: {}'.format(page_ctype))

        try:
            body = data_decoder(body_enc).encode('utf-8')
        except UnicodeEncodeError:
            _logger.debug('Errors encoding request data')
            body = data_decoder(body_enc).encode('utf-8',
                    errors='backslashreplace')
        _logger.debug('Decoded body: {}'.format(body))

        return {'data': body, 'type': page_ctype}

    def do_echo(self, sub, args):
        '''Decodes the request and returns it as the response body'''

        try:
            page = self.decode_page()
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
                    page = self.decode_page()
                except DecodingError as e:
                    self.send_error(400, explain=str(e))
                    return
                try:
                    self.cache.save(name, page)
                except cache.CacheError as e:
                    self.send_error(500, explain=str(e))
                else:
                    self.send_response_empty(204)
