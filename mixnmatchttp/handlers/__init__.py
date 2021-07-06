from .base import BaseHTTPRequestHandler
from .authenticator import AuthCookieHTTPRequestHandler, \
    AuthJWTHTTPRequestHandler
try:
    from .authenticator import AuthCookieDatabaseHTTPRequestHandler, \
        AuthJWTDatabaseHTTPRequestHandler
except ImportError:
    pass
from .cacher import CachingHTTPRequestHandler
from .proxy import ProxyingHTTPRequestHandler
