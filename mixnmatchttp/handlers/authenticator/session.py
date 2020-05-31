from ..._py2 import *

import logging

# optional features
try:
    import jwt
except ImportError:
    pass
else:
    from jwt.exceptions import \
        InvalidTokenError as JWTInvalidTokenError, \
        InvalidKeyError as JWTInvalidKeyError
try:
    import cryptography
except ImportError:
    pass
else:
    from cryptography.hazmat.backends import \
        default_backend as crypto_default_backend
    from cryptography.hazmat.primitives.serialization import \
        load_pem_private_key
    from cryptography.hazmat.primitives import serialization

from ... import endpoints
from ...utils import is_str, param_dict, datetime_from_timestamp, \
    curr_timestamp, randhex
from .api import BaseAuthHTTPRequestHandler, Session
from .utils import cookie_expflag


logger = logging.getLogger(__name__)


class BaseAuthCookieHTTPRequestHandler(BaseAuthHTTPRequestHandler):
    '''Implements cookie-based authentication

    Incomplete, must be inherited, and the child class must define
    methods for storing/getting/updating users and sessions.

    Class attributes:
    - _is_SSL: sets the Secure cookie flag if True. Default is False.
    - _cookie_path: the cookie path. Default is '/'.
    - _cookie_name: the cookie name. Default is 'SESSION'.
    - _cookie_len: Number of characters in the cookie (random hex).
      Default is 20.
    - _cookie_lifetime: Lifetime in seconds.
      Default is None (session cookie)
    - _SameSite: SameSite cookie flag. Can be 'lax' or 'strict'.
      Default is None (do not set it).
    '''

    _is_SSL = False
    _cookie_path = '/'
    _cookie_name = 'SESSION'
    _cookie_len = 20
    _cookie_lifetime = None
    _SameSite = None

    def get_current_token(self):
        '''Returns the session cookie'''

        cookies = param_dict(self.headers.get('Cookie'))
        if not cookies:
            return None
        try:
            token = cookies[self.__class__._cookie_name]
        except KeyError:
            return None
        return token

    def set_session(self, session):
        '''Saves the cookie to be sent with this response'''

        flags = '{}{}HttpOnly; '.format(
            'Secure; ' if self.__class__._is_SSL else '',
            'SameSite={}; '.format(self.__class__._SameSite)
            if self.__class__._SameSite is not None else '')
        cookie = \
            '{name}={value}; path={path}; {expiry}{flags}'.format(
                name=self.__class__._cookie_name,
                path=self.__class__._cookie_path,
                value=session.token,
                expiry=cookie_expflag(session.expiry),
                flags=flags)
        self.save_header('Set-Cookie', cookie)

    def unset_session(self, session):
        '''Sets an empty cookie to be sent with this response'''

        cookie = '{name}=; path={path}; {expiry}'.format(
            name=self.__class__._cookie_name,
            path=self.__class__._cookie_path,
            expiry=cookie_expflag(0))
        self.save_header('Set-Cookie', cookie)

    @classmethod
    def generate_session(cls, user):
        '''Returns a new Session'''

        expiry = cls._cookie_lifetime
        if expiry is not None:
            expiry += curr_timestamp(to_utc=True)
        return Session(
            token=randhex(cls._cookie_len),
            user=user,
            expiry=expiry)

class BaseAuthJWTHTTPRequestHandler(BaseAuthHTTPRequestHandler):
    '''Implements JWT-based authentication with refresh tokens

    Incomplete, must be inherited, and the child class must define
    methods for storing/getting/updating users and sessions.

    - A JSON response is sent to a /login or /changepwd with an
      access_token (JWT) and a refresh_token.
    - Defines a new endpoint: /authtoken which takes a refresh_token
      parameter and issues a new access_token. If the
      _send_new_refresh_token class attribute is True, then a new
      refresh_token is also sent with a /authtoken (and the old one is
      expired).
    - If a refresh_token is given during /logout it is removed
      server-side.

    Class attributes:
    - _JSON_params: send access_token, refresh_token and error
    - _jwt_lifetime: JWT lifetime in minutes. Default is 15.
    - _send_new_refresh_token: Send a new refresh token after a JWT
      refresh (/authtoken request). Default is True.
    - _refresh_token_lifetime: refresh token lifetime in minutes.
        Default is 1440 (one day).
    - _refresh_token_len: Number of characters in the refresh token
      (random hex). Default is 100.
    - _decode_opts: PyJWT options to pass to the decode method.
      Default is:
        {'verify_signature': True,
         'require_exp': True,
         'verify_exp': True}
    - _algorithm: The algorithm to use. Default is 'HS256'.
    - _enc_key: The key used to sign the JWT. A passphrase (for
      symmetric algorithms) or a loaded and decrypted PEM private key
      (for asymmetric algorithms).
    - _dec_key: The key used to verify the JWT. The same passphrase as
      _enc_key (for symmetric algorithms), or the corresponding public
      key (for asymmetric algorithms).
    You can load public/private keys from a file by calling the
    set_JWT_keys class method.
    '''

    _JSON_params = ['access_token', 'refresh_token', 'error']
    _jwt_lifetime = 15
    _send_new_refresh_token = True
    _refresh_token_lifetime = 1440
    _refresh_token_len = 100
    _decode_opts = {
        'verify_signature': True,
        'require_exp': True,
        'verify_exp': True}
    _algorithm = 'HS256'
    _enc_key = None
    _dec_key = None
    _endpoints = endpoints.Endpoint(
        authtoken={
            '$allowed_methods': {'GET', 'POST'},
        },
    )

    def __init__(self, *args, **kargs):
        if self._enc_key is None or self._dec_key is None:
            raise RuntimeError('JWT key not set')
        super().__init__(*args, **kargs)

    @classmethod
    def set_JWT_keys(cls,
                     passphrase,
                     algorithm=None,
                     privkey=None):
        '''Set the passphrase or keys used to sign and verify JWTs

        - algortihm: The JWT algorithm, e.g. HS256. If not supplied,
          then it is taken from the _algorithm class attribute.
          If it is supplied, it sets that class attribute.
        - passphrase: The passphrase to use for symmetric algorithms,
          or the passphrase to use to decrypt a private key file (when
          loading it from a file). It must be supplied, even if the
          given privkey is unencrypted (in which case passphrase must
          be None).
        - privkey: The private PEM key to use for signing the JWT.
          Only for asymmetric algorithms. It can be a filename, an
          open file handle, or an already decrypted PEM key (as
          a string, should begin with "-----BEGIN"). It must be
          supplied asymmetric algorithms.
        '''

        def load_privkey(fh):
            _passphrase = passphrase
            if _passphrase is not None \
                    and not isinstance(_passphrase, bytes):
                _passphrase = _passphrase.encode('utf-8')
            return load_pem_private_key(
                fh.read(),
                password=_passphrase,
                backend=crypto_default_backend())

        def load_key(arg, loader):
            if is_str(arg):
                if not arg.startswith('-----BEGIN'):
                    with open(arg, 'rb') as f:
                        return loader(f)
            # it has to be an open file handle
            return loader(f)

        if algorithm is not None:
            cls._algorithm = algorithm
        if cls._algorithm.startswith('HS'):
            # symmetric algorithm
            setattr(cls, '_enc_key', passphrase)
            setattr(cls, '_dec_key', passphrase)
            return
        # asymmetric algorithm
        privkey_loaded = load_key(privkey, load_privkey)
        pubkey_pem = privkey_loaded.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo)
        privkey_pem = privkey_loaded.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption())
        setattr(cls, '_enc_key', privkey_pem)
        setattr(cls, '_dec_key', pubkey_pem)

    def denied(self):
        '''Returns 401 if resource is secret and no authentication

        Same as parent denied, but also whitelist /authtoken endpoint.
        '''

        if self.pathname == '/authtoken':
            return None
        return super().denied()

    def get_current_session(self):
        '''Returns a Session if the JWT or refresh_token is valid

        - If a refresh_token is given (as it should to /authtoken or
          /logout), then the Session.token is set to it.
        - Otherwise if the JWT is valid, Session.user and
          Session.expiry are taken from it and Session.token will be
          None.
        - Otherwise returns None.
        '''

        # see if refresh token is given and still valid
        session = super().get_current_session()
        if session is not None:
            return session  # OK
        # check the JWT
        jwtok = self._get_current_jwt()
        if jwtok is None:
            logger.debug('No JWT')
            return None
        jwtok_d = self._decode_jwt(jwtok)
        if jwtok_d is None:
            logger.debug('Invalid JWT')
            return None
        logger.debug('Found session for {}'.format(jwtok_d['sub']))
        return Session(token=None,
                       user=self.find_user(jwtok_d['sub']),
                       expiry=datetime_from_timestamp(
                           jwtok_d['exp'],
                           relative=False,
                           from_utc=False,
                           to_utc=True))

    def get_current_token(self):
        '''Returns the refresh token'''

        return self.get_param('refresh_token')

    def set_session(self, session):
        '''Saves a new JWT to be sent with this response'''

        jwtok = self._get_new_jwt(session.user)
        self.save_param('access_token', jwtok)
        if session.token is not None:
            self.save_param('refresh_token', session.token)

    def unset_session(self, session):
        '''Does nothing'''

        pass

    @classmethod
    def generate_session(cls, user):
        '''Returns a new Session; token is the refresh token'''

        token = randhex(cls._refresh_token_len)
        expiry = datetime_from_timestamp(
            cls._refresh_token_lifetime * 60,
            relative=True, to_utc=True)
        return Session(
            token=token,
            user=user,
            expiry=expiry)

    @classmethod
    def _get_new_jwt(cls, user):
        now = datetime_from_timestamp(0, relative=True, to_utc=True)
        exp = datetime_from_timestamp(
            cls._jwt_lifetime * 60, relative=True, to_utc=True)
        token_d = {
            'sub': user.username,
            'exp': exp,
            'nbf': now,
            'iat': exp}
        return jwt.encode(token_d,
                          cls._enc_key,
                          algorithm=cls._algorithm).decode('utf-8')

    def _get_current_jwt(self):
        auth = self.headers.get('Authorization')
        if not auth or not auth.startswith('Bearer '):
            return None
        return auth[len('Bearer '):]

    @classmethod
    def _decode_jwt(cls, token):
        try:
            res = jwt.decode(
                token,
                cls._dec_key,
                algorithms=[cls._algorithm],
                options=cls._decode_opts)
        except (JWTInvalidTokenError, JWTInvalidKeyError) as e:
            logger.debug(str(e))
            return None
        return res

    def do_authtoken(self):
        '''Sends a new access_token

        If the _send_new_refresh_token class attribute is True, then
        a new refresh_token is also sent.
        '''

        # see if refresh token is given and still valid
        session = super().get_current_session()
        if session is None:
            self.send_response_auth(
                error=(401, 'Missing or invalid refresh token'))
            return
        if self.__class__._send_new_refresh_token:
            session = self.new_session(session.user)
            self.set_session(session)
        else:
            self.set_session(Session(user=session.user))
        self.send_response_auth()
