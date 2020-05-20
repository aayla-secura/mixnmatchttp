import http.server
from socketserver import ThreadingMixIn

__all__ = [
    'ThreadingHTTPServer',
]

class ThreadingHTTPServer(ThreadingMixIn, http.server.HTTPServer):
    '''Multi-threaded HTTPServer'''

    pass
