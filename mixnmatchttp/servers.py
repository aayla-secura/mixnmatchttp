import http.server
from socketserver import ThreadingMixIn


class ThreadingHTTPServer(ThreadingMixIn, http.server.HTTPServer):
    '''Multi-threaded HTTPServer'''

    pass
