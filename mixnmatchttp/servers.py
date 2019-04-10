#  from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import *
from future import standard_library
standard_library.install_aliases()
import http.server
from socketserver import ThreadingMixIn

__all__ = [
        'ThreadingHTTPServer',
        ]

class ThreadingHTTPServer(ThreadingMixIn, http.server.HTTPServer):
    '''Multi-threaded HTTPServer'''

    pass
