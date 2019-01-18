#!/usr/bin/env python3
import socketserver
import logging
import http.server
import ssl
import re
import sys
import argparse
import urllib

AUTH_COOKIE = 'auth=1'
logger = logging.getLogger('CORS Http Server')
logger.setLevel(logging.INFO)

class UnsupportedOperation(Exception):
    '''Exception raised when request body is read more than once'''

    def __init__(self):
        super().__init__(
            'Cannot read body data again, buffer not seekable')

class ThreadingCORSHttpsServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass

class CORSHttpsServer(http.server.SimpleHTTPRequestHandler):
    __can_read_body = False

    def send_custom_headers(self):
        '''The new_server factory overrides this'''
        pass

    def get_param(self, parname):
        '''Returns the value of parname given in the URL'''
        try:
            query = re.split('\?([^/]+)$', self.path)[1]
        except IndexError:
            return None
        try:
            params = dict(filter(lambda x: len(x) == 2,
                [p.split('=') for p in query.split('&')]))
        except ValueError:
            params = {}
        try:
            value = params[parname]
        except KeyError:
            return None
        return value

    def get_body(self):
        '''Returns the body data. Cannot be called more than once'''

        if not self.__can_read_body:
            raise UnsupportedOperation

        try:
            length = int(self.headers.get('Content-Length'))
        except TypeError:
            req_body = b''
        else:
            req_body = self.rfile.read(length)

        self.__can_read_body = False
        return req_body

    def show(self, req_body):
        '''Logs the request'''

        msg = "\n----- Request Start ----->\n\n{}\n{}".format(
            self.requestline, self.headers)

        try:
            req_body_dec = req_body.decode('utf-8')
        except UnicodeDecodeError:
            req_body_dec = '>> Cannot decode request body! <<'
        msg += "\n{}".format(req_body_dec)

        msg += "\n<----- Request End -----\n"
        logger.info(msg)
        return req_body

    def echo(self, post_data):
        '''Decodes the request and returns it as the response body'''

        try:
            post_data = post_data.decode('utf-8')
        except UnicodeDecodeError:
            self.send_error(400, explain='Cannot UTF-8 decode request body!')
            return

        try:
            req_params = dict([p.split('=') for p in post_data.split('&')])
        except ValueError:
            self.send_error(400, explain='Cannot load parameters from request!')
            return
        logger.debug('Request parameters: {}'.format(req_params))

        try:
            html_enc = req_params['data']
        except KeyError:
            self.send_error(400, explain='No "data" parameter present!')
            return
        logger.debug('Encoded HTML: {}'.format(html_enc))

        try:
            html = urllib.parse.unquote_plus(html_enc)
        except: # what exception does it throw???
            self.send_error(400, explain='Cannot URL decode request body!')
            return
        logger.debug('Decoded HTML: {}'.format(html))

        html = html.encode('utf-8')

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Content-Length', len(html))
        self.end_headers()
        self.wfile.write(html)

    def handle(self):
        self.__can_read_body = True
        super().handle()

    def end_headers(self):
        self.send_custom_headers()
        super().end_headers()

    def do_GET(self):
        req_data = self.get_body()
        self.show(req_data)
        if re.match('/echo(\?|$)', self.path) and self.command in ['OPTIONS', 'POST']:
            self.echo(req_data)
        elif self.headers.get('Cookie') == AUTH_COOKIE or not \
            re.match('/secret.txt(\?|$)', self.path):
            super().do_GET()
        else:
            self.send_error(401)

    def do_POST(self):
        self.do_GET()

    def do_OPTIONS(self):
        req_data = self.get_body()
        self.show(req_data)
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Content-Length', '0')
        self.end_headers()

    def do_HEAD(self):
        req_data = self.get_body()
        self.show(req_data)
        super().do_HEAD()

def new_server(clsname, cors, headers):
    def send_custom_headers(self):
        # Disable Cache
        if not re.search('/jquery-[0-9\.]+(\.min)?\.js$', self.path):
            self.send_header('Cache-Control',
                'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')

        for h in headers:
            self.send_header(*re.split(': *', h, maxsplit=1))

        # CORS, request path takes precedence
        # use origins=&creds=0 to disable CORS for this request
        allowed_origins = self.get_param('origin')
        if allowed_origins is None:
            allowed_origins = ', '.join(cors['origins'])
        if allowed_origins == '%%ECHO%%':
            allowed_origins = self.headers.get('Origin')
            if not allowed_origins: allowed_origins = '*'

        allowed_headers = ''
        if cors['headers']:
            # add a leading comma
            allowed_headers = ', '.join([''] + cors['headers'])

        allowed_methods = ''
        if cors['methods']:
            # add a leading comma
            allowed_methods = ', '.join([''] + cors['methods'])

        allow_creds = self.get_param('creds')
        try:
            allow_creds = bool(int(allow_creds))
        except (ValueError,TypeError):
            # invalid or missing param
            allow_creds = cors['creds']

        if allowed_origins:
            self.send_header('Access-Control-Allow-Origin',
                allowed_origins)
            self.send_header('Access-Control-Allow-Headers',
                'Accept, Accept-Language, Content-Language,' +
                'Content-Type, Authorization' + allowed_headers)
            self.send_header('Access-Control-Allow-Methods',
                'POST, GET, OPTIONS, HEAD' + allowed_methods)
            if allow_creds:
                self.send_header('Access-Control-Allow-Credentials',
                    'true')

    return type(clsname, (CORSHttpsServer,), {
        'send_custom_headers': send_custom_headers})

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description='''Serve the current working directory over
            HTTPS and with custom headers. The CORS related options
            (-o and -c) define the default behaviour. It can be
            overriden on a per-request basis using the origin and
            creds URL parameters. creds should be 0 or 1. origin is
            taken literally unless it is `%%ECHO%%`, then it is taken
            from the Origin header in the request.''')

    listen_parser = parser.add_argument_group('Listen options')
    listen_parser.add_argument('-a', '--address', dest='address',
            default='0.0.0.0', metavar='IP',
            help='''Address of interface to bind to.''')
    listen_parser.add_argument('-p', '--port', dest='port',
            default='58081', metavar='PORT', type=int,
            help='''HTTP port to listen on.''')

    cors_parser = parser.add_argument_group('CORS options (requires -o or -O)')
    ac_origin_parser = cors_parser.add_mutually_exclusive_group()
    ac_origin_parser.add_argument('-o', '--allowed-origins', dest='allowed_origins',
            default=[], metavar='Origin', nargs='*',
            help='''Allowed origins for CORS requests. Can be "*"''')
    ac_origin_parser.add_argument('-O', '--allow-all-origins',
            dest='allowed_origins', action='store_const', const=['%%ECHO%%'],
            help='''Allow all origins, i.e. echo the Origin in the
            request.''')
    cors_parser.add_argument('-x', '--allowed-headers', dest='allowed_headers',
            default=[], metavar='Header: Value', nargs='*',
            help='''Additional headers allowed for CORS requests.''')
    cors_parser.add_argument('-m', '--allowed-methods', dest='allowed_methods',
            default=[], metavar='Header: Value', nargs='*',
            help='''Additional methods allowed for CORS requests.''')
    cors_parser.add_argument('-c', '--allow-credentials', dest='allow_creds',
            default=False, action='store_true',
            help='''Allow sending credentials with CORS requests,
            i.e. add Access-Control-Allow-Credentials. Using this only
            makes sense if you are providing some list of origins (see
            -o and -O options), otherwise this option is ignored.''')

    ssl_parser = parser.add_argument_group('SSL options')
    ssl_parser.add_argument('-C', '--cert', dest='certfile',
            default='./cert.pem', metavar='FILE',
            help='''PEM file containing the server certificate.''')
    ssl_parser.add_argument('-K', '--key', dest='keyfile',
            default='./key.pem', metavar='FILE',
            help='''PEM file containing the private key for the server
            certificate.''')
    ssl_parser.add_argument('-S', '--no-ssl', dest='ssl',
            default=True, action='store_false',
            help='''Don't use SSL.''')

    misc_parser = parser.add_argument_group('Misc options')
    misc_parser.add_argument('-H', '--headers', dest='headers',
            default=[], metavar='Header: Value', nargs='*',
            help='''Additional headers to include in the response.''')
    misc_parser.add_argument('-l', '--logfile', dest='logfile',
            metavar='FILE',
            help='''File to write requests to. Will write to stdout if
            not given.''')
    misc_parser.add_argument('-d', '--debug', dest='loglevel',
            default=logging.INFO, action='store_const',
            const=logging.DEBUG,
            help='''Enable debugging output.''')
    args = parser.parse_args()

    if args.logfile is None:
        logger.addHandler(logging.StreamHandler(sys.stdout))
    else:
        logger.addHandler(logging.FileHandler(args.logfile))
    logger.setLevel(args.loglevel)

    httpd = ThreadingCORSHttpsServer((args.address, args.port),
            new_server('CORSHttpsServer', {
                    'origins': args.allowed_origins,
                    'methods': args.allowed_methods,
                    'headers': args.allowed_headers,
                    'creds': args.allow_creds},
                args.headers))
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
