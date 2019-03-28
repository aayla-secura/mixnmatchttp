#!/usr/bin/env python3
#  from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import super
from builtins import int
from builtins import filter
from future import standard_library
standard_library.install_aliases()
import logging
import re
import sys
import argparse

from mixnmatchttp.handlers import BaseHTTPRequestHandler, \
        AuthHTTPRequestHandler, CachingHTTPRequestHandler, \
        ProxyingHTTPRequestHandler, methodhandler
from mixnmatchttp.servers import ThreadingHttpServer
from mixnmatchttp import endpoints
from mixnmatchttp.common import DictNoClobber
from http.server import HTTPServer

logger = logging.getLogger('Test Http Server')

class DebugStreamHandler(logging.StreamHandler):
    def emit(self, record):
        if not record.levelno == logging.DEBUG:
            return
        super(DebugStreamHandler, self).emit(record)

class TestHTTPRequestHandler(AuthHTTPRequestHandler,
        CachingHTTPRequestHandler, ProxyingHTTPRequestHandler):

    _secrets=('secret', '/topsecret')
    _userfile='users.txt'
    _min_pwdlen=3
    _endpoints = endpoints.Endpoints(
            dummylogin={},
            modtest={},
            test={
                'post_one': {
                    'args': 1,
                    'allowed_methods': {'POST'},
                    },
                'get_opt': {
                    'args': endpoints.ARGS_OPTIONAL,
                    },
                'get_req': {
                    'args': endpoints.ARGS_REQUIRED,
                    },
                'get_any': {
                    'args': endpoints.ARGS_ANY,
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
                'BODY': '$BODY: $sub ($args)',
            },
            'page': 'testpage'
        },
    )

    def do_dummylogin(self, sub, args):
        self.rm_session()
        cookie = self.new_session()
        self.send_response_goto(headers={'Set-Cookie':
            'SESSION={}; path=/; {}HttpOnly'.format(
                cookie, ('Secure; ' if self._is_SSL else ''))
            })
        
    def do_modtest(self, sub, args):
        # modify endpoint, should affect only current request
        self.endpoints['test'] = {}
        self.endpoints['test']['']['args'] = 1
        self.do_GET.__wrapped__()

    def do_test(self, sub, args):
        page = self.page_from_template(self.templates['testtemplate'],
                {'BODY': 'test', 'sub': sub, 'args': args})
        self.render(page)

    def denied(self):
        '''Deny access to /forbidden'''
        if re.match('^/forbidden(/|$)', self.pathname):
            # return args are passed to BaseHTTPRequestHandler.send_error
            # in that order; both messages are optional
            return (403, None, 'Access denied')
        return super(TestHTTPRequestHandler, self).denied()

    def no_cache(self):
      '''Only allow caching of scripts'''
      return (not self.pathname.endswith('.js')) or super(TestHTTPRequestHandler, self).no_cache()

    @methodhandler
    def do_GET(self):
        page = self.page_from_template(self.templates['testtemplate'],
                {'BODY': 'default'})
        self.render(page)

    def send_custom_headers(self):
        self.send_header('X-Foo', 'Foo')

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
    misc_parser.add_argument('-t', '--multithread', dest='srv_cls',
            default=HTTPServer, action='store_const',
            const=ThreadingHttpServer,
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

    httpd = args.srv_cls((args.address, args.port), TestHTTPRequestHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.socket.close()
