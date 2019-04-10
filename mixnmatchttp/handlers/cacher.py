#  from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import *
from future import standard_library
standard_library.install_aliases()
import logging
import uuid
import mimetypes

from .. import endpoints,cache
from .base import BaseHTTPRequestHandler, DecodingError

__all__ = [
        'CachingHTTPRequestHandler',
        ]

logger = logging.getLogger(__name__)

class CachingHTTPRequestHandler(BaseHTTPRequestHandler):
    cache = cache.Cache()
    _endpoints = endpoints.Endpoint(
            echo={
                '$allowed_methods': {'POST'},
                },
            cache={
                '$allowed_methods': {'GET', 'POST'},
                '$nargs': 1,
                '$clear': {
                    '$nargs': endpoints.ARGS_OPTIONAL,
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
        logger.debug('Encoded body: {}'.format(body_enc))

        try:
            page_ctype = type_decoder(self.params['type']).split(';',1)[0]
            if page_ctype not in mimetypes.types_map.values():
                raise ValueError('Unsupported Content-type')
        except (KeyError, ValueError):
            page_ctype = 'text/plain'
        else:
            logger.debug('Content-Type: {}'.format(page_ctype))

        try:
            body = data_decoder(body_enc).encode('utf-8')
        except UnicodeEncodeError:
            logger.debug('Errors encoding request data')
            body = data_decoder(body_enc).encode('utf-8',
                    errors='backslashreplace')
        logger.debug('Decoded body: {}'.format(body))

        return {'data': body, 'type': page_ctype}

    def do_echo(self, ep):
        '''Decodes the request and returns it as the response body'''

        try:
            page = self.decode_page()
        except DecodingError as e:
            self.send_error(400, explain=str(e))
            return
        self.render(page)

    def do_cache_clear(self, ep):
        '''Clears a cached page'''

        name = ep.args
        if not name:
            # empty name should clear all pages; cache.clear will only
            # clear all pages if name is None and not if it's ''
            name = None
        self.cache.clear(name)
        self.send_response_empty(204)

    def do_cache_new(self, ep):
        '''Generates a new UUID'''

        self.render({
            'data': '{}'.format(
                uuid.uuid4()).encode('utf-8'),
            'type': 'text/plain'})

    def do_cache(self, ep):
        '''Saves or retrieves a cached page'''

        name = ep.args
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
