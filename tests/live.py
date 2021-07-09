import logging
from copy import deepcopy
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
    from mixnmatchttp.log import get_loggers, clear_loggers
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        '-d', '--debug', dest='loglevel',
        default=logging.INFO, action='store_const',
        const=logging.DEBUG)
    args, sys.argv[1:] = parser.parse_known_args()

    loggers = get_loggers({
        'DEBUG': [('mixnmatchttp', None)]
        if args.loglevel is logging.DEBUG else [],
        'INFO': [('mixnmatchttp', None)]
    })

from mixnmatchttp.handlers import BaseHTTPRequestHandler, \
    AuthCookieHTTPRequestHandler, CachingHTTPRequestHandler, \
    ProxyingHTTPRequestHandler
from mixnmatchttp.handlers.authenticator.api import User
from mixnmatchttp.endpoints import Endpoint, \
    ARGS_OPTIONAL, ARGS_REQUIRED, ARGS_ANY
from mixnmatchttp.conf import Conf
from mixnmatchttp.pollers import Poller, TimePoller, uses_poller


deep_ep = Endpoint({  # test assigning to multiple parents
    '1': {
        '2': Endpoint({
            '3': Endpoint(),
            '4': {},
        }),
    },
})

@decorator
def foo(handler, self, args, kwargs):
    self.save_header('X-Bar', 'Bar')
    handler()

@decorator
def endpoint_debug_handler(handler, self, args, kwargs):
    handler()
    page = self.page_from_template('handler',
                                   handler=handler.__name__,
                                   root=self.ep.root,
                                   sub=self.ep.sub,
                                   args=self.ep.args)
    self.render(page)

class TestHTTPRequestHandler(AuthCookieHTTPRequestHandler,
                             CachingHTTPRequestHandler,
                             ProxyingHTTPRequestHandler):

    conf = Conf(
        verbose_errors=True,
        enable_directory_listing=True,
        send_software_info=True,
        secrets=('secret', '/topsecret'),
        password=Conf(
            min_len=3,
            min_charsets=1
        ))
    endpoints = Endpoint(
        dummylogin={},
        cookie={},
        template={},
        poll={
            'allow': {},
        },
        files={
            '$raw_args': True,
        },
        test={
            'post_one': Endpoint(
                {  # test passing an Endpoint instance
                    '$nargs': 1,
                    '$allow': {'POST'},
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
        deep=deepcopy(deep_ep),
        deepdup=deepcopy(deep_ep),
        err={},
    )
    templates = dict(
        handler={
            'data': 'This is $handler for $root @ $sub ($args)',
            'mimetype': 'text/plain'
        },
        dir='templates',
    )

    def do_dummylogin(self):
        self.new_session(User('dummy'))
        self.send_response_auth()

    @endpoint_debug_handler
    def do_default(self):
        pass

    @endpoint_debug_handler
    def do_err(self):
        raise RuntimeError('foo')

    @endpoint_debug_handler
    def do_cookie(self):
        self.save_cookie('foo', 'bar')
        self.save_cookie('Foo', 'bar')
        self.save_cookie('bar', 'bar')

    def do_template(self):
        page = self.page_from_template(
            'dir', 'foo.html',
            title='This is Foo',
            body='FOO')
        self.render(page)

    def do_files(self):
        super().do_GET()

    @endpoint_debug_handler
    def do_deep(self):
        pass

    @endpoint_debug_handler
    def do_deepdup(self):
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

    @foo
    def do_GET(self):
        page = self.page_from_template(
            'handler',
            handler='do_GET',
            root=self.pathname,
            args=[])
        self.render(page)

    def do_TRACE(self):
        raise RuntimeError  # test

    def send_custom_headers(self):
        self.send_header('X-Foo', 'Foo')


if __name__ == "__main__":
    clear_loggers(loggers)
    from mixnmatchttp.app import App
    webapp = App(
        TestHTTPRequestHandler,
        support_ssl=False,
        support_cors=False,
        support_daemon=False,
        auth_type='cookie')
    webapp.run()
