from .api import BaseAuthHTTPRequestHandler
from .session import \
    BaseAuthCookieHTTPRequestHandler, BaseAuthJWTHTTPRequestHandler
from .storage import BaseAuthInMemoryHTTPRequestHandler
try:  # optional database classes
    from .dbstorage import BaseAuthSQLAlchemyORMHTTPRequestHandler
    from .dbutils import needs_db_response_handling, \
        needs_db_error_response_handling, needs_db
except ImportError:  # no SQLAlchemy
    pass
else:
    class AuthCookieDatabaseHTTPRequestHandler(
            BaseAuthSQLAlchemyORMHTTPRequestHandler,
            BaseAuthCookieHTTPRequestHandler):
        '''Cookie-based auth (DB storage)'''

        pass

    class AuthJWTDatabaseHTTPRequestHandler(
            BaseAuthSQLAlchemyORMHTTPRequestHandler,
            BaseAuthJWTHTTPRequestHandler):
        '''JWT-based auth with refresh tokens (DB storage)'''

        pass

class AuthCookieHTTPRequestHandler(
        BaseAuthInMemoryHTTPRequestHandler,
        BaseAuthCookieHTTPRequestHandler):
    '''Cookie-based auth (in-memory storage)'''

    pass

class AuthJWTHTTPRequestHandler(
        BaseAuthInMemoryHTTPRequestHandler,
        BaseAuthJWTHTTPRequestHandler):
    '''JWT-based auth with refresh tokens (in-memory storage)'''

    pass
