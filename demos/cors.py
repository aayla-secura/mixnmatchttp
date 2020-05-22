#!/usr/bin/env python3

import re
from mixnmatchttp import WebApp
from mixnmatchttp.handlers import BaseHTTPRequestHandler, \
    AuthCookieHTTPRequestHandler, CachingHTTPRequestHandler, \
    ProxyingHTTPRequestHandler


class CORSHTTPSServer(AuthCookieHTTPRequestHandler,
                      CachingHTTPRequestHandler,
                      ProxyingHTTPRequestHandler):
    def no_cache(self):
        return (not re.search('/jquery-[0-9\.]+(\.min)?\.js',
                self.pathname)) or super().no_cache()


webapp = WebApp(
    CORSHTTPSServer,
    description=(
        'Serve the current working directory over HTTPS and with '
        'custom headers. The CORS related options define the '
        'default behaviour. It can be overriden on a per-request '
        'basis using the origin and creds URL parameters. creds '
        'should be 0 or 1. origin is taken literally unless it '
        'is `{ECHO}`, then it is taken from the Origin header in '
        'the request.'),
    support_ssl=True,
    support_cors=True,
    support_daemon=False,
    auth_type='cookie')

webapp.parser.add_argument(
    '-S', '--secrets', dest='secrets',
    default=['secret'], metavar='DIR|FILE', nargs='+',
    help=('Directories or files which require a SESSION cookie. '
          'If no leading slash then it is matched anywhere in '
          'the path.'))
webapp.configure()
webapp.reqhandler._secrets = webapp.conf.secrets
webapp.run()
