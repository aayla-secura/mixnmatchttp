#!/usr/bin/env python3
#  from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import *
from future import standard_library
standard_library.install_aliases()
import logging
import re
import sys
import argparse
from wrapt import decorator
from http.server import HTTPServer

class DebugStreamHandler(logging.StreamHandler):
    def emit(self, record):
        if not record.levelno == logging.DEBUG:
            return
        super().emit(record)

logger = logging.getLogger('Test HTTP Server')
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description='Test')

    listen_parser = parser.add_argument_group('Listen options')
    listen_parser.add_argument('-a', '--address', dest='address',
            default='127.0.0.1', metavar='IP',
            help='''Address of interface to bind to.''')
    listen_parser.add_argument('-p', '--port', dest='port',
            default='58080', metavar='PORT', type=int,
            help='''HTTP port to listen on.''')

    misc_parser = parser.add_argument_group('Misc options')
    misc_parser.add_argument('-d', '--debug', dest='loglevel',
            default=logging.INFO, action='store_const',
            const=logging.DEBUG,
            help='''Enable debugging output.''')
    misc_parser.add_argument('-t', '--multithread', dest='multithread',
            default=False, action='store_true',
            help='''Enable multi-threading support. EXPERIMENTAL! The
            cache has not been implemented in an MT safe way yet.''')
    args = parser.parse_args()

    hnOUT = logging.StreamHandler(sys.stdout)
    hnOUT.setLevel(logging.INFO)
    hnDBG = DebugStreamHandler(sys.stderr)
    hnDBG.setLevel(logging.DEBUG)
    logging.basicConfig(level=args.loglevel,
            format='%(name)s [%(threadName)s]: %(message)s',
            handlers=[hnOUT, hnDBG])

from mixnmatchttp.handlers import BaseHTTPRequestHandler, \
        AuthHTTPRequestHandler, CachingHTTPRequestHandler, \
        ProxyingHTTPRequestHandler, methodhandler
from mixnmatchttp.servers import ThreadingHTTPServer
from mixnmatchttp import endpoints
from mixnmatchttp.common import DictNoClobber

@decorator
def endpoint_debug_handler(handler, self, args, kwargs):
    ep = args[0]
    handler(ep)
    page = self.page_from_template(self.templates['testtemplate'],
            {'handler': handler.__name__,
                'root': ep.root,
                'sub': ep.sub,
                'args': ep.args})
    self.render(page)

class TestHTTPRequestHandler(AuthHTTPRequestHandler,
        CachingHTTPRequestHandler, ProxyingHTTPRequestHandler):

    _secrets=('secret', '/topsecret')
    _userfile='test_users.txt'
    _min_pwdlen=3
    _endpoints = endpoints.Endpoint(
        dummylogin={},
        modtest={},
        test={
            'post_one': endpoints.Endpoint({ # test passing an Endpoint instance
                '$nargs': 1,
                '$allowed_methods': {'POST'},
                }),
            'get_opt': {
                '$nargs': endpoints.ARGS_OPTIONAL,
                },
            'get_req': {
                '$nargs': endpoints.ARGS_REQUIRED,
                },
            'get_any': {
                '$nargs': endpoints.ARGS_ANY,
                },
            },
        deep={
            '1': {
                '2': endpoints.Endpoint({
                    '3': endpoints.Endpoint(),
                    '4': {},
                    }),
                },
            },
        )
    _template_pages = DictNoClobber(
        testpage={
            'data': '$BODY',
            'type': 'text/plain'
            },
        )
    _templates = DictNoClobber(
        testtemplate={
            'fields': {
                'BODY': 'This is $handler for $root @ $sub ($args)',
                },
            'page': 'testpage'
            },
        )

    def do_dummylogin(self, ep):
        self.set_cookie()
        self.send_response_goto()
        
    @endpoint_debug_handler
    def do_modtest(self, ep):
        # modify endpoint, should affect only current request
        self.endpoints['test'] = {}
        self.endpoints['test'].args = 1
        # set a header just for this request
        self.headers_to_send['X-Mod'] = 'Test'
        self.do_GET.__wrapped__()

    @endpoint_debug_handler
    def do_default(self, ep):
        pass

    @endpoint_debug_handler
    def do_deep(self, ep):
        pass

    @endpoint_debug_handler
    def do_deep_1_2_4(self, ep):
        pass

    @endpoint_debug_handler
    def do_deep_1_2_3_4(self, ep):
        # this one should never be called
        raise NotImplemented

    def denied(self):
        '''Deny access to /forbidden'''
        if re.match('^/forbidden(/|$)', self.pathname):
            # return args are passed to BaseHTTPRequestHandler.send_error
            # in that order; both messages are optional
            return (403, None, 'Access denied')
        return super().denied()

    def no_cache(self):
      '''Only allow caching of scripts'''
      return (not self.pathname.endswith('.js')) or super().no_cache()

    @methodhandler
    def do_GET(self):
        page = self.page_from_template(self.templates['testtemplate'],
                {'handler': 'do_GET'})
        self.render(page)

    def send_custom_headers(self):
        self.send_header('X-Foo', 'Foo')

if __name__ == "__main__":
    srv_cls = HTTPServer
    if args.multithread:
        srv_cls = ThreadingHTTPServer
    httpd = srv_cls((args.address, args.port), TestHTTPRequestHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
