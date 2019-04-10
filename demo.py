#  from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import *
from future import standard_library
standard_library.install_aliases()
import re
import ssl
from http.server import HTTPServer
from mixnmatchttp.servers import ThreadingHTTPServer
from mixnmatchttp import endpoints
from mixnmatchttp.handlers import BaseHTTPRequestHandler,methodhandler
from mixnmatchttp.common import DictNoClobber

class MyHandler(BaseHTTPRequestHandler):
    _endpoints = endpoints.Endpoint(
            foobar={ }, # will use do_default handler
            refreshme={
                '$nargs': endpoints.ARGS_OPTIONAL,
                },
            debug={
                # these are for when /debug is called
                '$allowed_methods': {'GET', 'POST'},
                '$nargs': 1,
                'sub': { # will use do_debug handler
                    # these are for when /debug/sub is called
                    '$nargs': endpoints.ARGS_ANY,
                    '$raw_args': True, # don't canonicalize rest of path
                    }
                },
            )
    _template_pages = DictNoClobber(
        simpletxt={
            'data':'$CONTENT',
            'type':'text/html'
            },
        simplehtml={
            'data':'''
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8" />
    $HEAD
    <title>$TITLE</title>
    </head>
    <body>
    $BODY
    </body>
    </html>
    ''',
            'type':'text/html'
            },
        )
    _templates = DictNoClobber(
        refresh={
            'fields':{
                'HEAD':'<meta http-equiv="refresh" content="${interval}">',
                'TITLE':'Example',
                'BODY':'<h1>Example page, will refresh every ${interval}s.</h1>',
            },
            'page': 'simplehtml',
        },
        debug={
            'fields':{
                'CONTENT':'${info}You called endpoint $root ($sub) ($args)',
            },
            'page': 'simpletxt',
        },
    )

    def do_refreshme(self, ep):
        interval = ep.args
        if not interval:
            interval = '30'

        '''Handler for the endpoint /refreshme'''
        page = self.page_from_template(self.templates['refresh'],
                {'interval': interval})
        self.render(page)

    def do_debug(self, ep):
        '''Handler for the endpoint /debug'''
        # set a header just for this request
        self.headers_to_send['X-Debug'] = 'Foo'
        page = self.page_from_template(self.templates['debug'],
                {'root': ep.root, 'sub': ep.sub, 'args': ep.args})
        self.render(page)

    def do_default(self, ep):
        '''Default endpoints handler'''
        page = self.page_from_template(self.templates['debug'],
                {'info': 'This is do_default. ',
                    'root': ep.root, 'sub': ep.sub, 'args': ep.args})
        self.render(page)

    # Don't forget this decorator!
    @methodhandler
    def do_GET(self):
        # Do something here, then call parent's undecorated method
        super().do_GET.__wrapped__()

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

    def send_custom_headers(self):
      '''Send our custom headers'''
      self.send_header('X-Foo', 'Foobar')


if __name__ == "__main__":
    use_SSL = False
    keyfile = '' # path to PEM key, if use_SSL is True
    certfile = '' # path to PEM certificate, if use_SSL is True
    srv_cls = HTTPServer
    # srv_cls = ThreadingHTTPServer # if using multi-threading
    address = '127.0.0.1'
    port = 58080

    httpd = srv_cls((address, port), MyHandler)
    if use_SSL:
        httpd.socket = ssl.wrap_socket(
                httpd.socket,
                keyfile=keyfile,
                certfile=certfile,
                server_side=True)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
