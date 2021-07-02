import logging
import re
import sys
import argparse
from wrapt import decorator

class DebugStreamHandler(logging.StreamHandler):
    def emit(self, record):
        if not record.levelno == logging.DEBUG:
            return
        super().emit(record)


if __name__ == "__main__":
    from mixnmatchttp.log import get_loggers
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        '--color', dest='use_color', default=False,
        action='store_true', help='Use colorful log')
    parser.add_argument(
        '-d', '--debug', dest='loglevel',
        default=logging.INFO, action='store_const',
        const=logging.DEBUG)
    args, sys.argv[1:] = parser.parse_known_args()

    get_loggers(
        {
            'DEBUG': [('mixnmatchttp', None)]
            if args.loglevel is logging.DEBUG else [],
            'INFO': [('mixnmatchttp', None)]
        }, color=args.use_color)

from mixnmatchttp.handlers import BaseHTTPRequestHandler, \
    AuthCookieHTTPRequestHandler, CachingHTTPRequestHandler, \
    ProxyingHTTPRequestHandler, methodhandler
from mixnmatchttp.handlers.authenticator.api import User
from mixnmatchttp.endpoints import Endpoint, \
    ARGS_OPTIONAL, ARGS_REQUIRED, ARGS_ANY
from mixnmatchttp.conf import Conf

@decorator
def endpoint_debug_handler(handler, self, args, kwargs):
    handler()
    page = self.page_from_template(self.templates['testtemplate'],
                                   {'handler': handler.__name__,
                                    'root': self.ep.root,
                                    'sub': self.ep.sub,
                                    'args': self.ep.args})
    self.render(page)

class TestHTTPRequestHandler(AuthCookieHTTPRequestHandler,
                             CachingHTTPRequestHandler,
                             ProxyingHTTPRequestHandler):

    conf = Conf(
        secrets=('secret', '/topsecret'),
        password=Conf(
            min_len=3,
            min_charsets=1
        ))
    endpoints = Endpoint(
        dummylogin={},
        cookie={},
        modtest={},
        test={
            'post_one': Endpoint(
                {  # test passing an Endpoint instance
                    '$nargs': 1,
                    '$allowed_methods': {'POST'},
                }),
            'get_opt': {
                '$nargs': ARGS_OPTIONAL,
            },
            'get_req': {
                '$nargs': ARGS_REQUIRED,
            },
            'get_any': {
                '$nargs': ARGS_ANY,
            },
        },
        deep={
            '1': {
                '2': Endpoint({
                    '3': Endpoint(),
                    '4': {},
                }),
            },
        },
    )
    template_pages = dict(
        testpage={
            'data': '$BODY',
            'type': 'text/plain'
        },
    )
    templates = dict(
        testtemplate={
            'fields': {
                'BODY': 'This is $handler for $root @ $sub ($args)',
            },
            'page': 'testpage'
        },
    )

    @endpoint_debug_handler
    def do_dummylogin(self):
        self.new_session(User('dummy'))
        self.send_response_auth()

    @endpoint_debug_handler
    def do_modtest(self):
        # modify endpoint, should affect only current request
        self.endpoints['test'] = {}
        self.endpoints['test'].nargs = 1
        # set a header just for this request
        self.save_header('X-Mod', 'Test')
        self.do_GET.__wrapped__()

    @endpoint_debug_handler
    def do_default(self):
        pass

    @endpoint_debug_handler
    def do_cookie(self):
        self.save_cookie('foo', 'bar')
        self.save_cookie('Foo', 'bar')
        self.save_cookie('bar', 'bar')

    @endpoint_debug_handler
    def do_deep(self):
        pass

    @endpoint_debug_handler
    def do_deep_1_2_4(self):
        pass

    @endpoint_debug_handler
    def do_deep_1_2_3_4(self):
        # this one should never be called
        raise NotImplementedError

    def denied(self):
        '''Deny access to /forbidden'''
        if re.match('^/forbidden(/|$)', self.pathname):
            # return args are passed to
            # BaseHTTPRequestHandler.send_error in that order; both
            # messages are optional
            return (403, None, 'Access denied')
        return super().denied()

    def no_cache(self):
        '''Only allow caching of scripts'''

        return (not self.pathname.endswith('.js')) or super().no_cache()

    @methodhandler
    def do_GET(self):
        page = self.page_from_template(
            self.templates['testtemplate'],
            {'handler': 'do_GET'})
        self.render(page)

    def send_custom_headers(self):
        self.send_header('X-Foo', 'Foo')


if __name__ == "__main__":
    from mixnmatchttp.app import App
    webapp = App(
        TestHTTPRequestHandler,
        support_ssl=False,
        support_cors=False,
        support_daemon=False,
        auth_type='cookie')
    webapp.run()
