import logging
import base64

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

from ...endpoints import Endpoint
from ...utils import is_str, param_dict, datetime_from_timestamp, \
    curr_timestamp, randhex, randstr, int_to_bytes
from ...conf import Conf
from .api import BaseAuthHTTPRequestHandler, Session
from .utils import cookie_expflag


logger = logging.getLogger(__name__)


class BaseAuthCookieHTTPRequestHandler(BaseAuthHTTPRequestHandler):
    '''Implements cookie-based authentication

    Incomplete, must be inherited, and the child class must define
    methods for storing/getting/updating users and sessions.

    Class attributes:
    - is_SSL: sets the Secure cookie flag if True. Default is False.
    - cookie_path: the cookie path. Default is '/'.
    - cookie_name: the cookie name. Default is 'SESSION'.
    - cookie_len: Number of characters in the cookie (random hex).
      Default is 20.
    - cookie_lifetime: Lifetime in seconds.
      Default is None (session cookie)
    - SameSite: SameSite cookie flag. Can be 'lax' or 'strict'.
      Default is None (do not set it).
    '''

    conf = Conf(
        is_SSL=False,
        # XXX make cookie conf a subdict
        cookie_path='/',
        cookie_name='SESSION',
        cookie_len=20,
        cookie_lifetime=None,
        SameSite=None,
    )

    def get_current_token(self):
        '''Returns the session cookie'''

        cookies = param_dict(self.headers.get('Cookie'))
        if not cookies:
            return None
        try:
            token = cookies[self.conf.cookie_name]
        except KeyError:
            return None
        return token

    def set_session(self, session):
        '''Saves the cookie to be sent with this response'''

        flags = '{}{}HttpOnly; '.format(
            'Secure; ' if self.conf.is_SSL else '',
            'SameSite={}; '.format(self.conf.SameSite)
            if self.conf.SameSite is not None else '')
        cookie = \
            '{name}={value}; path={path}; {expiry}{flags}'.format(
                name=self.conf.cookie_name,
                path=self.conf.cookie_path,
                value=session.token,
                expiry=cookie_expflag(session.expiry),
                flags=flags)
        self.save_header('Set-Cookie', cookie)

    def unset_session(self, session):
        '''Sets an empty cookie to be sent with this response'''

        cookie = '{name}=; path={path}; {expiry}'.format(
            name=self.conf.cookie_name,
            path=self.conf.cookie_path,
            expiry=cookie_expflag(0))
        self.save_header('Set-Cookie', cookie)

    @classmethod
    def generate_session(cls, user):
        '''Returns a new Session'''

        expiry = cls.conf.cookie_lifetime
        if expiry is not None:
            expiry += curr_timestamp(to_utc=True)
        return Session(
            token=randhex(cls.conf.cookie_len),
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
      send_new_refresh_token class attribute is True, then a new
      refresh_token is also sent with a /authtoken (and the old one is
      expired).
    - If a refresh_token is given during /logout it is removed
      server-side.

    Class attributes:
    - enable_JWKS: save a JWKS object in jwks. Coming soon:
      a /.well-known/jwks.json endpoint
    - JSON_params: send access_token, refresh_token and error
    - jwt_lifetime: JWT lifetime in minutes. Default is 15.
    - send_new_refresh_token: Send a new refresh token after a JWT
      refresh (/authtoken request). Default is True.
    - refresh_token_lifetime: refresh token lifetime in minutes.
        Default is 1440 (one day).
    - refresh_token_len: Number of characters in the refresh token
      (random hex). Default is 100.
    - decode_opts: PyJWT options to pass to the decode method.
      Default is:
        {'verify_signature': True,
         'require_exp': True,
         'verify_exp': True}
    - algorithm: The algorithm to use. Default is 'HS256'.
    - enc_key: The key used to sign the JWT. A passphrase (for
      symmetric algorithms) or a loaded and decrypted PEM private key
      (for asymmetric algorithms).
    - dec_key: The key used to verify the JWT. The same passphrase as
      enc_key (for symmetric algorithms), or the corresponding public
      key (for asymmetric algorithms).
    - jwks: If the jwks option is given to set_JWT_keys, then a JWKS
      object is saved in jwks with a random kid.
    You can load public/private keys from a file by calling the
    set_JWT_keys class method.
    '''

    conf = Conf(
        enable_JWKS=False,
        JSON_params=['access_token', 'refresh_token', 'error'],
        jwt_lifetime=15,
        send_new_refresh_token=True,
        refresh_token_lifetime=1440,
        refresh_token_len=100,
        decode_opts={'verify_signature': True,
                     'require_exp': True,
                     'verify_exp': True},
        algorithm='HS256',
        enc_key=None,
        dec_key=None,
        jwks=None,
    )
    endpoints = Endpoint(
        authtoken={
            '$allowed_methods': {'POST'},
        },
    )

    def __init__(self, *args, **kargs):
        if self.conf.enc_key is None or self.conf.dec_key is None:
            raise RuntimeError('JWT key not set')
        super().__init__(*args, **kargs)

    @classmethod
    def set_JWT_keys(cls,
                     passphrase,
                     algorithm=None,
                     jwks=None,
                     privkey=None):
        '''Set the passphrase or keys used to sign and verify JWTs

        - algortihm: The JWT algorithm, e.g. HS256. If not supplied,
          then it is taken from the algorithm class attribute.
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
        - jwks: Boolean specifying whether or not to user JWKS.
          If None, it is taken from the enable_JWKS class attribute.
          If it is supplied, it sets that class attribute.
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

        def get_jwks(pubkey):
            n = pubkey.public_numbers().n
            n_b64 = base64.urlsafe_b64encode(
                int_to_bytes(n)).decode('utf-8').strip('=')
            e = pubkey.public_numbers().e
            e_b64 = base64.urlsafe_b64encode(
                int_to_bytes(e)).decode('utf-8').strip('=')
            assert not cls.conf.algorithm.startswith('HS')
            kty = 'RSA'
            if cls.conf.algorithm.startswith('ES'):
                kty = 'EC'
            return {
                'keys': [
                    {
                        'alg': cls.conf.algorithm,
                        'kty': kty,
                        'use': 'sig',
                        'n': n_b64,
                        'e': e_b64,
                        'kid': randstr(40, use_punct=False),
                    }
                ]}

        if algorithm is not None:
            cls.conf.algorithm = algorithm
        if cls.conf.algorithm.startswith('HS'):
            # symmetric algorithm
            cls.conf['enc_key'] = passphrase
            cls.conf['dec_key'] = passphrase
            return
        # asymmetric algorithm
        privkey_loaded = load_key(privkey, load_privkey)
        pubkey = privkey_loaded.public_key()
        pubkey_pem = pubkey.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo)
        privkey_pem = privkey_loaded.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption())
        cls.conf['enc_key'] = privkey_pem
        cls.conf['dec_key'] = pubkey_pem
        if jwks is not None:
            cls.conf.enable_JWKS = jwks
        if cls.conf.enable_JWKS:
            cls.conf['jwks'] = get_jwks(pubkey)

    def denied(self):
        '''Returns 401 if resource is secret and no authentication

        Same as parent denied, but also whitelist /authtoken endpoint.
        '''

        if self.pathname == '{}/authtoken'.format(
                self.conf.api_prefix):
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

        token = randhex(cls.conf.refresh_token_len)
        expiry = datetime_from_timestamp(
            cls.conf.refresh_token_lifetime * 60,
            relative=True, to_utc=True)
        return Session(
            token=token,
            user=user,
            expiry=expiry)

    @classmethod
    def _get_new_jwt(cls, user):
        now = datetime_from_timestamp(0, relative=True, to_utc=True)
        exp = datetime_from_timestamp(
            cls.conf.jwt_lifetime * 60, relative=True, to_utc=True)
        token_d = {
            'sub': user.username,
            'exp': exp,
            'nbf': now,
            'iat': exp}
        return jwt.encode(token_d,
                          cls.conf.enc_key,
                          algorithm=cls.conf.algorithm).decode('utf-8')

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
                cls.conf.dec_key,
                algorithms=[cls.conf.algorithm],
                options=cls.conf.decode_opts)
        except (JWTInvalidTokenError, JWTInvalidKeyError) as e:
            logger.debug(str(e))
            return None
        return res

    def do_authtoken(self):
        '''Sends a new access_token

        If the send_new_refresh_token class attribute is True, then
        a new refresh_token is also sent.
        Returns the user on success and None on failure
        '''

        # see if refresh token is given and still valid
        session = super().get_current_session()
        if session is None:
            self.send_response_auth(
                error=(401, 'Missing or invalid refresh token'))
            return None
        if self.conf.send_new_refresh_token:
            session = self.new_session(session.user)
            self.set_session(session)
        else:
            self.set_session(Session(user=session.user))
        self.send_response_auth()
        return session.user
