from http.server import HTTPServer
from socketserver import ThreadingMixIn as _ThreadingMixIn


class ThreadingHTTPServer(_ThreadingMixIn, HTTPServer):
    '''Multi-threaded HTTPServer'''

    pass
