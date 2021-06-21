import logging
from http.server import HTTPServer
from socketserver import ThreadingMixIn


logger = logging.getLogger(__name__)


class Server(ThreadingMixIn, HTTPServer):
    user_conf = None  # to be set by App

    def server_activate(self):
        # do something
        super().server_activate()

    def shutdown(self):
        # do something
        super().shutdown()
