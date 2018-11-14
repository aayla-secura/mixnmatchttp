#!/usr/bin/env python3
import http.server, http.server
import ssl
import re
import argparse

AUTH_COOKIE = 'auth=1'

class CORSHttpsServer(http.server.SimpleHTTPRequestHandler):
    def send_custom_headers(self):
        pass
    
    def show(self):
        print("\n----- Request Start ----->\n")
        print(self.requestline)
        print(self.headers)
        try:
            length = int(self.headers.get('Content-Length'))
        except TypeError:
            pass
        else:
            print(self.rfile.read(length).decode('utf-8'))
        print("<----- Request End -----\n")
    
    def do_OPTIONS(self):
        self.do_HEAD()
    
    def do_HEAD(self):
        self.show()
        super().do_HEAD()
    
    def do_GET(self):
        self.show()
        if self.headers.get('Cookie') == AUTH_COOKIE:
            super().do_GET()
        else:
            super().send_error(401)
    
    def do_POST(self):
        self.do_GET()
    
    def end_headers(self):
        self.send_custom_headers()
        super().end_headers()

def new_server(clsname, origins, creds, headers):
    def send_custom_headers(self):
        for h in headers:
            self.send_header(*re.split(': *', h, maxsplit=1))
        if origins:
            allowed_origins = origins
            if allowed_origins == '%%ECHO%%':
                allowed_origins = self.headers.get('Origin')
                if not allowed_origins: allowed_origins = '*'
            self.send_header('Access-Control-Allow-Origin',
                allowed_origins)
            if creds:
                self.send_header('Access-Control-Allow-Credentials',
                    'True')
    
    return type(clsname, (CORSHttpsServer,), {
        'send_custom_headers': send_custom_headers})

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description='''Serve the current working directory over
            HTTPS and with custom headers.''')
    parser.add_argument('-a', '--address', dest='address',
            default='0.0.0.0', metavar='IP',
            help='''Address of interface to bind to.''')
    parser.add_argument('-p', '--port', dest='port',
            default='58081', metavar='PORT', type=int,
            help='''HTTP port to listen on.''')
    ac_origin_parser = parser.add_mutually_exclusive_group()
    ac_origin_parser.add_argument('-o', '--origins', dest='origins',
            metavar='"Allowed origins"',
            help='''"*" or a coma-separated whitelist of origins.''')
    ac_origin_parser.add_argument('-O', '--all-origins', dest='origins',
            action='store_const', const='%%ECHO%%',
            help='''Allow all origins, i.e. echo the Origin in the
            request.''')
    parser.add_argument('-c', '--cors-credentials', dest='creds',
            default=False, action='store_true',
            help='''Allow sending credentials with CORS requests,
            i.e. add Access-Control-Allow-Credentials. Using this only
            makes sense if you are providing some list of origins (see
            -o and -O options), otherwise this option is ignored.''')
    parser.add_argument('-H', '--headers', dest='headers',
            default=[], metavar='Header: Value', nargs='*',
            help='''Additional headers.''')
    parser.add_argument('-C', '--cert', dest='certfile',
            default='./cert.pem', metavar='FILE',
            help='''PEM file containing the server certificate.''')
    parser.add_argument('-K', '--key', dest='keyfile',
            default='./key.pem', metavar='FILE',
            help='''PEM file containing the private key for the server
            certificate.''')
    parser.add_argument('-S', '--no-ssl', dest='ssl',
            default=True, action='store_false',
            help='''Don't use SSL.''')
    args = parser.parse_args()
    
    httpd = http.server.HTTPServer((args.address, args.port),
            new_server('CORSHttpsServer',
                args.origins,
                args.creds,
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
