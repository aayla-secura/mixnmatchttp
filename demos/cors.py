#!/usr/bin/env python3
# TO DO:
#  - colorful log
#  from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import super
from builtins import int
from builtins import filter
from builtins import str
from future import standard_library
standard_library.install_aliases()
import logging
import ssl
import re
import sys
import argparse
import urllib

from mixnmatchttp.handlers import BaseHTTPRequestHandler, \
        AuthHTTPRequestHandler, CachingHTTPRequestHandler, \
        ProxyingHTTPRequestHandler
from mixnmatchttp.servers import ThreadingHttpServer
from http.server import HTTPServer

logger = logging.getLogger('CORS Http Server')

class DebugStreamHandler(logging.StreamHandler):
    def emit(self, record):
        if not record.levelno == logging.DEBUG:
            return
        super(DebugStreamHandler, self).emit(record)

class CORSHttpsServer(AuthHTTPRequestHandler,
        CachingHTTPRequestHandler, ProxyingHTTPRequestHandler):

    def no_cache(self):
        return (not re.search('/jquery-[0-9\.]+(\.min)?\.js',
                self.pathname)) or super(CORSHttpsServer, self).no_cache()

def new_server(clsname, cors, headers, is_SSL, secrets):
    def send_custom_headers(self):

        for h in headers:
            self.send_header(*re.split(': *', h, maxsplit=1))

        # CORS, request path takes precedence
        # use origins=&creds=0 to disable CORS for this request
        allowed_origins = self.get_param('origin')
        if allowed_origins is None:
            allowed_origins = ', '.join(cors['origins'])
        allowed_origins = urllib.parse.unquote_plus(allowed_origins)
        if allowed_origins == '{ECHO}':
            allowed_origins = self.headers.get('Origin')
            if not allowed_origins: allowed_origins = '*'

        allowed_headers = ''
        if cors['headers']:
            allowed_headers = ', '.join(cors['headers'])

        allowed_methods = self.allowed_methods
        if not allowed_methods and cors['methods']:
            allowed_methods = cors['methods']
        if allowed_methods:
            allowed_methods = ', '.join(allowed_methods)

        allow_creds = self.get_param('creds')
        try:
            allow_creds = bool(int(allow_creds))
        except (ValueError,TypeError):
            # invalid or missing param
            allow_creds = cors['creds']

        if allowed_origins:
            self.send_header('Access-Control-Allow-Origin',
                allowed_origins)
        if allowed_headers:
            self.send_header('Access-Control-Allow-Headers',
                allowed_headers)
        if allowed_methods:
            self.send_header('Access-Control-Allow-Methods',
                allowed_methods)
        if allow_creds:
            self.send_header('Access-Control-Allow-Credentials',
                'true')

    return type(clsname, (CORSHttpsServer,), {
        '_is_SSL': is_SSL,
        '_secrets': tuple(filter(None, secrets)),
        'send_custom_headers': send_custom_headers})

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description='''Serve the current working directory over
            HTTPS and with custom headers. The CORS related options
            define the default behaviour. It can be overriden on
            a per-request basis using the origin and creds URL
            parameters. creds should be 0 or 1. origin is taken
            literally unless it is `{ECHO}`, then it is taken from the
            Origin header in the request.''')

    listen_parser = parser.add_argument_group('Listen options')
    listen_parser.add_argument('-a', '--address', dest='address',
            default='127.0.0.1', metavar='IP',
            help='''Address of interface to bind to.''')
    listen_parser.add_argument('-p', '--port', dest='port',
            metavar='PORT', type=int,
            help='''HTTP port to listen on. Default is 58080 if not
            over SSL or 58443 if over SSL.''')

    cors_parser = parser.add_argument_group('CORS options')
    ac_origin_parser = cors_parser.add_mutually_exclusive_group()
    ac_origin_parser.add_argument('-o', '--allowed-origins', dest='allowed_origins',
            default=[], metavar='Origin', nargs='*',
            help='''Allowed origins for CORS requests. Can be "*"''')
    ac_origin_parser.add_argument('-O', '--allow-all-origins',
            dest='allowed_origins', action='store_const', const=['{ECHO}'],
            help='''Allow all origins, i.e. echo the Origin in the
            request.''')
    cors_parser.add_argument('-x', '--allowed-headers', dest='allowed_headers',
            default=['Accept', 'Accept-Language', 'Content-Language',
                'Content-Type', 'Authorization'],
            metavar='Header: Value', nargs='*',
            help='''Headers allowed for CORS requests.''')
    cors_parser.add_argument('-m', '--allowed-methods', dest='allowed_methods',
            default=['POST', 'GET', 'OPTIONS', 'HEAD'], metavar='Method', nargs='*',
            help='''Methods allowed for CORS requests. OPTIONS to one
            of the special endpoints always return the allowed methods
            of that endpoint.''')
    cors_parser.add_argument('-c', '--allow-credentials', dest='allow_creds',
            default=False, action='store_true',
            help='''Allow sending credentials with CORS requests,
            i.e. add Access-Control-Allow-Credentials. Using this only
            makes sense if you are providing some list of origins (see
            -o and -O options), otherwise this option is ignored.''')

    ssl_parser = parser.add_argument_group('SSL options')
    ssl_parser.add_argument('-s', '--ssl', dest='ssl',
            default=False, action='store_true',
            help='''Use SSL.''')
    ssl_parser.add_argument('-C', '--cert', dest='certfile',
            default='./cert.pem', metavar='FILE',
            help='''PEM file containing the server certificate.''')
    ssl_parser.add_argument('-K', '--key', dest='keyfile',
            default='./key.pem', metavar='FILE',
            help='''PEM file containing the private key for the server
            certificate.''')

    misc_parser = parser.add_argument_group('Misc options')
    misc_parser.add_argument('-H', '--headers', dest='headers',
            default=[], metavar='Header: Value', nargs='*',
            help='''Additional headers to include in the response.''')
    misc_parser.add_argument('-S', '--secrets', dest='secrets',
            default=['secret'], metavar='DIR|FILE', nargs='*',
            help='''Directories or files which require a SESSION
            cookie. If no leading slash then it is matched anywhere in
            the path.''')
    misc_parser.add_argument('-l', '--logfile', dest='logfile',
            metavar='FILE',
            help='''File to write requests to. Will write to stdout if
            not given.''')
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

    if args.logfile is None:
        hnOUT = logging.StreamHandler(sys.stdout)
        hnOUT.setLevel(logging.INFO)
        hnDBG = DebugStreamHandler(sys.stderr)
        hnDBG.setLevel(logging.DEBUG)
        handlers = [hnOUT, hnDBG]
    else:
        logkwargs = {'filename': args.logfile}
        handlers = [logging.FileHandler(args.logfile)]
    logging.basicConfig(level=args.loglevel,
            format='%(name)s [%(threadName)s]: %(message)s',
            handlers=handlers)

    if args.port is None:
        args.port = 58443 if args.ssl else 58080

    httpd = args.srv_cls((args.address, args.port),
            new_server('CORSHttpsServerCustom', {
                    'origins': args.allowed_origins,
                    'methods': args.allowed_methods,
                    'headers': args.allowed_headers,
                    'creds': args.allow_creds},
                args.headers,
                args.ssl,
                args.secrets))
    if args.ssl:
        httpd.socket = ssl.wrap_socket(
                httpd.socket,
                keyfile=args.keyfile,
                certfile=args.certfile,
                server_side=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.socket.close()
