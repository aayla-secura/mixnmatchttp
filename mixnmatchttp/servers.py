from http.server import HTTPServer as _HTTPServer
from socketserver import ThreadingMixIn as _ThreadingMixIn


class ThreadingHTTPServer(_ThreadingMixIn, _HTTPServer):
    '''Multi-threaded HTTPServer'''

    pass
