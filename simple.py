#!/usr/bin/env python3
# TO DO:
#  - write doc for all classes and methods
#  - colorful log
import logging
import http.server
import ssl
import re
import sys
import os.path
import argparse
import urllib
import json
import base64, binascii
import mimetypes
import uuid
from random import randint
from functools import wraps
from socketserver import ThreadingMixIn

logger = logging.getLogger('CORS Http Server')
logger.setLevel(logging.INFO)

############################################################
######################### EXCEPTIONS ########################
############################################################
class PageReadError(Exception):
    '''Base class for exceptions related to request body read'''
    pass

class UnsupportedOperationError(PageReadError):
    '''Exception raised when request body is read more than once'''

    def __init__(self):
        super().__init__(
            'Cannot read body data again, buffer not seekable')

class DecodingError(PageReadError):
    '''Exception raised when cannot decode sent data'''
    pass


class CacheError(Exception):
    '''Base class for exceptions related to the cache'''
    pass

class PageNotCachedError(CacheError):
    '''Exception raised when a non-existent page is requested'''

    def __init__(self):
        super().__init__(
            'This page has not been cached yet.')

class PageClearedError(CacheError):
    '''Exception raised when a deleted page is requested'''

    def __init__(self):
        super().__init__(
            'This page has been cleared.')

class MemoryError(CacheError):
    '''Exception raised when max data already stored in cache'''

    def __init__(self):
        super().__init__(
            'Cannot save any more pages, call /cache/clear or' +
            '/cache/clear/{page_name}')

class CacheOverwriteError(CacheError):
    '''Exception raised when attempted overwriting of page'''

    def __init__(self):
        super().__init__(
            'Cannot overwrite page, choose a different name')


class EndpointError(Exception):
    '''Base class for exceptions related to the special endpoints'''
    pass

class NotAnEndpointError(EndpointError):
    '''Exception raised when the root path is unknown'''

    def __init__(self, root):
        super().__init__('{} is not special.'.format(root))

class MethodNotAllowedError(EndpointError):
    '''Exception raised when the request method is not allowed'''

    def __init__(self):
        super().__init__('Method not allowed.')

class MissingArgsError(EndpointError):
    '''Exception raised when a required argument is not given'''

    def __init__(self):
        super().__init__('Missing required argument.')

class ExtraArgsError(EndpointError):
    '''Exception raised when extra arguments are given'''

    def __init__(self, args):
        super().__init__('Extra arguments: {}.'.format(args))

############################################################
########################## CLASSES #########################
############################################################
class Cache():
    __max_size = 2*1024*1024

    def __init__(self, max_size=None):
        if max_size is not None:
            self.__max_size = max_size
        self.__size = 0
        self.__pages = {}

    def save(self, name, page):
        '''Saves the page to the cache.
        
        name is the alphanumeric identifier
        page is a dictionary with the following items:
            - data: the content of the page
            - type: the content type
        '''

        #TODO Multi-thread safety!
        if self.size + len(page['data']) > self.max_size:
            raise MemoryError
        try:
            self.__pages[name]
        except KeyError:
            logger.debug('Caching page "{}"'.format(name))
            self.__pages[name] = page
            self.__size += len(page['data'])
            logger.debug('Cache size is: {}'.format(self.size))
        else:
            raise CacheOverwriteError

    def get(self, name):
        logger.debug('Trying to get page "{}"'.format(name))
        try:
            page = self.__pages[name]
        except KeyError:
            raise PageNotCachedError
        if page is None:
            raise PageClearedError
        return page

    def clear(self, name=None):
        '''Marks all pages as purged, but remembers page names'''

        try:
            self.__pages[name]
        except KeyError:
            if name is None:
                to_clear = [k for k,v in self.__pages.items() \
                        if v is not None]
            else:
                return # no such cached page
        else:
            to_clear = [name]

        logger.debug('Clearing from cache: {}'.format(
            ', '.join(to_clear)))

        for key in to_clear:
            if self.__pages[key] is not None:
                self.__size -= len(self.__pages[key]['data'])
            self.__pages[key] = None

        logger.debug('Cache size is: {}'.format(self.size))
        assert self.__size >= 0

    @property
    def max_size(self):
        return self.__max_size

    @property
    def size(self):
        return self.__size

############################################################
class Endpoints():
    '''Special endpoints
    
    Format for endpoints:
    '<root>': {
            '<subpoint>': {
                'allowed_methods': ['<method1>', ...], # GET, POST, etc
                'args': <number>|Endpoints.ARGS_*, # how many args,
                                                   # only reliable if
                                                   # raw_args is False
                'raw_args': True|False, # should we canonicalize
                }
            }
    
    'args' can be a number for exact number of arguments
    'allowed_methods defaults to ['GET']
    'args' defaults to 0
    'raw_args' defaults to False
    '''

    ARGS_OPTIONAL = '?' # 0 or 1
    ARGS_ANY = '*'      # any number
    ARGS_REQUIRED = '+' # 1 or more

    def __init__(self, **kwargs):
        self.__endpoints = kwargs.copy()
        for root, subs in self.__endpoints.items():
            if not subs:
                subs[''] = {}
            for sub in subs.values():
                try:
                    sub['allowed_methods']
                except KeyError:
                    sub['allowed_methods'] = ['GET']
                try:
                    sub['args']
                except KeyError:
                    sub['args'] = 0
                try:
                    sub['raw_args']
                except KeyError:
                    sub['raw_args'] = False
                sub['allowed_methods'] += ['OPTIONS']

    def get(self, root):
        try:
            return self.__endpoints[root]
        except KeyError:
            return None

    def parse(self, path, command):
        '''Selects an endpoint for the path
        
        Returns (root, sub, args) if an endpoint, or raises an
        exception:
            NotAnEndpointError
            MethodNotAllowedError
            MissingArgsError
            ExtraArgsError
        '''

        if not isinstance(path, str) or not path or path[0] != '/':
            pass #TODO Exception

        # we don't yet know if the endpoints or subpoint wants the
        # arguments raw or canonicalized. So we check the first
        # absolute segment
        # if it's an endpoint which expects raw arguments, we're done
        root, sub, args = self._parse_raw(abspath_up_to_nth(path, 1))
        if not root:
            # otherwise check for the second abs segment
            logger.debug('Checking if subpoint takes raw args')
            root, sub, args = self._parse_raw(abspath_up_to_nth(path, 2))

        if root:
            logger.debug(('Parsed endpoint with raw args: root: {}, ' +
                'sub: {}, args: {}').format(root, sub, args))
            if self.__endpoints[root][sub]['args'] not in \
                [self.ARGS_ANY, self.ARGS_REQUIRED]:
                logger.warning(('Endpoint {} requires non-canonical ' +
                    'arguments, but is sensitive to the number ' +
                    'of arguments; not reliable!').format(root))
        else:
            # finally canonicalize the whole path and take the root
            # endpoint and subpoint from there
            root, sub, args = self._unpacker(
                    *abspath(path).lstrip('/').split('/', 2))
            logger.debug(('Parsed endpoint: root: {}, sub: {}, args: {}'
                ).format(root, sub, args))

        if not self._is_endp(root, sub):
            args = '/'.join(filter(None, [sub, args])) # consume the sub into args
            sub = ''

        if not self._is_endp(root):
            raise NotAnEndpointError(root)

        logger.debug(
                'API call: root: {}, sub: {}, args: {}'.format(
                    root, sub, args))

        args_arr = list(filter(None, args.split('/')))
        endpoint = self.__endpoints[root]
        if endpoint[sub]['args'] == self.ARGS_ANY:
            pass
        elif endpoint[sub]['args'] == self.ARGS_REQUIRED:
            if not args:
                raise MissingArgsError
        elif endpoint[sub]['args'] == self.ARGS_OPTIONAL:
            if len(args_arr) > 1:
                raise ExtraArgsError('/'.join(args_arr[1:]))
        elif len(args_arr) > endpoint[sub]['args']:
            raise ExtraArgsError('/'.join(
                args_arr[endpoint[sub]['args']:]))
        elif len(args_arr) < endpoint[sub]['args']:
            raise MissingArgsError

        if command not in endpoint[sub]['allowed_methods']:
            raise MethodNotAllowedError

        return root, sub, args

    def _parse_raw(self, path):
        root, sub, args = self._unpacker(*path.lstrip('/').split('/', 2))
        if self._is_endp(root, sub) and \
                self.__endpoints[root][sub]['raw_args']:
            return root, sub, args

        return '', '', ''

    def _is_endp(self, root, sub=''):
        try:
            self.__endpoints[root][sub]
        except KeyError:
            return False

        return True

    @staticmethod
    def _unpacker(root, sub='',args=''):
        # handle case of not enough / in path during splitting
        return root, sub, args

############################################################
class ThreadingCORSHttpsServer(ThreadingMixIn, http.server.HTTPServer):
    pass

class CORSHttpsServer(http.server.SimpleHTTPRequestHandler):

    _secrets = []
    _is_SSL = False
    __cookie_len = 20
    __sessions = []
    __max_sessions = 10

    cache = Cache()
    # request path is checked against each endpoint's root;
    # if match, then the subpath after that is matched against the
    # endpoint's subpoint
    # if no match, then the default subpoint '' is used
    # the request method is checked against the list of allowed methods
    # then a handler called do_<root> is called, passing it the
    # subpoint that matched and the rest of the subpaths
    endpoints = Endpoints(
        echo={
            '': {
                'allowed_methods': ['POST'],
                },
            },
        goto={
            # call it as /goto?<params for this server>/<URI-decoded address>;
            # include the ? after /goto even if not giving parameters,
            # otherwise any parameters in the address would be
            # consumed
            '': {
                'allowed_methods': ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
                'args': Endpoints.ARGS_ANY,
                'raw_args': True,
                },
            },
        login={ },
        logout={ },
        cache={
            '': {
                'allowed_methods': ['GET', 'POST'],
                'args': 1,
                },
            'clear': {
                'args': Endpoints.ARGS_OPTIONAL,
                },
            'new': { },
            },
        )
    __templates = {
        'default':{
            'data':'''
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    {%HEAD%}
  </head>
  <body>
    {%BODY%}
  </body>
</html>
    ''',
            'type':'text/html'
            },
        }
    __template_pages = {
        'example': {
            'fields':{
                'HEAD':'<meta http-equiv="refresh" content="30">',
                'BODY':'Example "dynamic" page, will refresh every 30s.',
            },
        },
    }

    def __init__(self, *args, **kwargs):
        self.__pathname = ''
        self.__query = dict()
        self.__can_read_body = True
        self.__body = None
        self.__allowed_methods = None
        super().__init__(*args, **kwargs)

    def send_custom_headers(self):
        '''The new_server factory overrides this'''
        pass

    def is_secret(self):
        '''Returns whether path requires authentication.'''

        logger.debug('{} secrets'.format(len(self._secrets)))
        for s in self._secrets:
            logger.debug('{} is secret'.format(s))
            if re.search('{}{}(/|$)'.format(
                ('^' if s[0] == '/' else ''), s),
                self.__pathname):
                return True

        return False

    def get_param(self, parname):
        '''Returns the value of parname given in the URL'''

        try:
            value = self.__query[parname]
        except KeyError:
            return None

        return value

    def get_session(self):
        '''Returns the session cookie'''

        cookies = param_dict(self.headers.get('Cookie', failobj=''))
        if not cookies:
            logger.debug('No cookies given')
            session = None
        else:
            try:
                session = cookies['SESSION']
            except KeyError:
                logger.debug('No SESSION cookie given')
                session = None
            else:
                logger.debug('Cookie is {}valid'.format(
                    '' if session in self.__sessions else 'not '))

        return session

    def rm_session(self):
        '''Invalidate the session server-side'''

        session = self.get_session()
        try:
            self.__sessions.remove(session)
        except ValueError:
            pass

    def begin_response_goto(self, code=302, url=None):
        if url is None:
            url = self.get_param('goto')
        if url is not None:
            self.send_response(code)
            self.send_header('Location', urllib.parse.unquote_plus(url))
        else:
            self.send_response(200)

    def end_response_default(self):
        #  self.send_header('Content-type', 'text/plain')
        self.send_header('Content-Length', 0)
        self.end_headers()

    def show(self):
        '''Logs the request'''

        msg = "\n----- Request Start ----->\n\n{}\n{}".format(
            self.requestline, self.headers)

        try:
            req_body_dec = self.__body.decode('utf-8')
        except UnicodeDecodeError:
            logger.debug('Errors decoding request body')
            req_body_dec = self.__body.decode('utf-8',
                    errors='backslashreplace')
        msg += "\n{}".format(req_body_dec)

        msg += "\n<----- Request End -----\n"
        logger.info(msg)

    def render(self, page):
        '''Renders a page as a 200 OK.
        
        page is a dictionary with the following items:
            - data: the content of the page
            - type: the content type
        '''

        self.send_response(200)
        self.send_header('Content-type', page['type'])
        self.send_header('Content-Length', len(page['data']))
        self.end_headers()
        self.wfile.write(page['data'])

    def page_from_template(self, t_page, dynfields={}):
        try:
            t_name = t_page['template']
        except KeyError:
            logger.debug('Using default template for page')
            t_name = 'default'

        try:
            page = self.__templates[t_name]
        except KeyError:
            return {'data':
                b'No such template {}'.format(t_name)}

        try:
            fields = t_page['fields']
        except KeyError:
            logger.debug(
                'No fields for template page')
            fields = {}

        for f,v in fields.items():
            logger.debug('Replacing field {} with "{}"'.format(f,v))
            page['data'] = page['data'].replace('{%'+f+'%}', v)

        # those fields may be present in the original static fields
        # themselves, so we replace them at the end, after all static
        # ones
        for f,v in dynfields.items():
            logger.debug('Replacing field {} with "{}"'.format(f,v))
            page['data'] = page['data'].replace('{%'+f+'%}', v)

        # remove unused fields and encode
        page['data'] = re.sub('{%[^%]*%}', '', page['data'])
        try:
            page['data'] = page['data'].encode('utf-8')
        except UnicodeEncodeError:
            logger.debug('Errors encoding page body')
            page['data'] = page['data'].encode('utf-8',
                    errors='backslashreplace')

        return page

    def read_body(self):
        '''Returns the body data. Cannot be called more than once'''

        if not self.__can_read_body:
            raise UnsupportedOperationError

        try:
            length = int(self.headers.get('Content-Length'))
        except TypeError:
            self.__body = b''
        else:
            self.__body = self.rfile.read(length)

        logger.debug('Read {} bytes from body'.format(len(self.__body)))
        self.__can_read_body = False

    def decode_body(self):
        '''Decodes the body.
        
        Returns the Content-Type and the parameters'''

        post_type = self.headers.get('Content-Type')
        try:
            post_type = post_type.split(';',1)[0]
        except AttributeError:
            # No Content-Type
            post_type = None
        if post_type in ['application/json', 'text/json']:
            param_loader = self.JSON_params
            data_decoder = self.b64_data
            type_decoder = lambda x: x
        elif post_type == 'application/x-www-form-urlencoded':
            param_loader = self.form_params
            data_decoder = self.url_data
            type_decoder = self.url_data
        else:
            raise DecodingError(
                'Unknown Content-Type: {}'.format(post_type))
            return

        try:
            post_data = self.__body.decode('utf-8')
        except UnicodeDecodeError:
            logger.debug('Errors decoding request body')
            post_data = self.__body.decode('utf-8',
                    errors='backslashreplace')

        req_params = param_loader(post_data)
        logger.debug('Request parameters: {}'.format(req_params))
        return req_params, post_type

    def decode_page(self):
        '''Decodes the request.
        
        It must contain the following parameters:
            - data: the content of the page
            - type: the content type

        Returns the same data/type dictionary but with a decoded
        content'''

        req_params, post_type = self.decode_body()
        data_decoder = type_decoder = None
        if post_type in ['application/json', 'text/json']:
            data_decoder = self.b64_data
            type_decoder = lambda x: x
        elif post_type == 'application/x-www-form-urlencoded':
            data_decoder = self.url_data
            type_decoder = self.url_data
        # decode_body will raise DecodingError otherwise

        try:
            body_enc = req_params['data']
        except KeyError:
            raise DecodingError('No "data" parameter present!')
        logger.debug('Encoded body: {}'.format(body_enc))

        try:
            ctype = type_decoder(req_params['type']).split(';',1)[0]
            if ctype not in mimetypes.types_map.values():
                raise ValueError('Unsupported Content-type')
        except (KeyError, ValueError):
            ctype = 'text/plain'
        else:
            logger.debug('Echo Content-Type: {}'.format(ctype))

        try:
            body = data_decoder(body_enc).encode('utf-8')
        except UnicodeEncodeError:
            logger.debug('Errors encoding request data')
            body = data_decoder(body_enc).encode('utf-8',
                    errors='backslashreplace')
        logger.debug('Decoded body: {}'.format(body))

        return {'data': body, 'type': ctype}

    @staticmethod
    def form_params(post_data):
        '''Parameter loader.
        
        Returns a dictionary read from an
        application/x-www-form-urlencoded POST
        '''

        req_params = param_dict(post_data, itemsep='&')
        if not req_params:
            raise DecodingError('Cannot load parameters from request!')
        return req_params

    @staticmethod
    def JSON_params(post_data):
        '''Parameter loader.
        
        Returns a dictionary read from a JSON string
        '''

        try:
            req_params = json.loads(post_data)
        except JSONDecodeError:
            raise DecodingError('Cannot decode JSON!')
        return req_params

    @staticmethod
    def url_data(data_enc):
        '''Data decoder.
        
        Returns the percent-decoded data
        '''

        try:
            data = urllib.parse.unquote_plus(data_enc)
        except: # what exception does it throw???
            raise DecodingError('Cannot URL decode request data!')
        return data

    @staticmethod
    def b64_data(data_enc):
        '''Data decoder.
        
        Returns the base64-decoded data
        '''

        try:
            data = base64.b64decode(data_enc)
        except binascii.Error:
            raise DecodingError('Cannot Base64 decode request data!')
        try:
            return data.decode('utf-8')
        except UnicodeDecodeError:
            logger.debug('Errors decoding base64 data')
            return data.decode('utf-8', errors='backslashreplace')

    def end_headers(self):
        self.send_custom_headers()
        super().end_headers()

    def do_logout(self, cmd, args):
        '''Clears the cookie from the browser and the saved sessions'''

        self.rm_session()
        self.begin_response_goto()
        self.send_header('Set-Cookie', 'SESSION=')
        self.end_response_default()

    def do_login(self, cmd, args):
        '''Issues a random cookie and saves it'''

        self.rm_session()
        cookie = '{:02x}'.format(
            randint(0, 2**(4*self.__cookie_len)-1))
        if len(self.__sessions) >= self.__max_sessions:
            # remove a third of the oldest sessions
            logger.debug('Purging old sessions')
            del self.__sessions[int(self.__max_sessions/3):]
        self.__sessions.append(cookie)

        self.begin_response_goto()
        self.send_header('Set-Cookie',
            'SESSION={}; path=/; {}HttpOnly'.format(
                cookie, ('Secure; ' if self._is_SSL else '')))
        self.end_response_default()

    def do_goto(self, cmd, args):
        '''Redirects to the path following /goto/
        
        If the path does not include a domain, it is taken from the
        following headers, in this order:
        - Referer
        - Origin
        - X-Forwarded-Host
        - X-Forwarded-For
        - Forwarded
        '''

        # check if path includes domain
        if re.match('(https?:)?//[^/]', args):
            self.begin_response_goto(code=307, url=args)
            self.end_response_default()
            return

        def send_redir(host, proto='', pref='', **kwargs):
            if args[:1] == '/':
                # relative to root => ignore prefix path
                pref = ''
            elif pref[-1:] != '/':
                # otherwise make sure there's a trailing slash for prefix
                pref += '/'
            if proto and proto[-1] != ':':
                proto += ':'
            path = ''.join([proto, '//', host, pref, args])
            logger.debug('Redirecting to {}'.format(path))
            self.begin_response_goto(code=307, url=path)
            self.end_response_default()

        fwd = dict()
        # otherwise check Referer and Origin
        try:
            # a valid Origin shouldn't have a path, but nevermind
            fwd = re.fullmatch(
                    '(?P<proto>https?:|)//(?P<host>[^/]+)(?P<pref>/?.*)',
                    list(filter(None, [
                        self.headers.get('Referer'),
                        self.headers.get('Origin'),
                        ]))[0]).groupdict()
        except (IndexError, AttributeError):
            # otherwise check X-Forwarded-*
            logger.debug('Checking Origin and X-Forwarded-*')
            try:
                fwd['host'] = list(filter(None, [
                    self.headers.get('X-Forwarded-Host'),
                    self.headers.get('X-Forwarded-For')
                    ]))[0]
            except IndexError:
                # otherwise check Forwarded
                logger.debug('Checking Forwarded')
                fwd = param_dict(self.headers.get('Forwarded',
                    failobj='').replace('for=', 'host='))
            else:
                # one of X-Forwarded-* may have matched
                fwd['proto'] = self.headers.get('X-Forwarded-Proto',
                        failobj='')

        try:
            logger.debug('fwd: {}'.format(fwd))
            send_redir(**fwd)
        except TypeError:
            logger.debug("Couldn't figure out host to redirect to...")
            self.send_response(200)
            self.end_response_default()

    def do_echo(self, cmd, args):
        '''Decodes the request and returns it as the response body'''

        try:
            page = self.decode_page()
        except DecodingError as e:
            self.send_error(400, None, explain=str(e))
            return
        self.render(page)

    def do_cache(self, cmd, name):
        '''Saves, retrieves or clears a cached page'''

        if not name:
            name = None # cache.clear expects non-empty or None, not ''

        if cmd == 'clear':
            self.cache.clear(name)
            self.send_response(204)
            self.end_headers()
        elif cmd == 'new':
            self.render({
                'data': '{}'.format(
                    uuid.uuid4()).encode('utf-8'),
                'type': 'text/plain'})
        else:
            assert not cmd # did we forget to handle a command

            if self.command == 'GET':
                try:
                    page = self.cache.get(name)
                except (PageClearedError, PageNotCachedError) as e:
                    self.send_error(500, None, explain=str(e))
                else:
                    self.render(page)

            else:
                try:
                    page = self.decode_page()
                except DecodingError as e:
                    self.send_error(400, None, explain=str(e))
                    return
                try:
                    self.cache.save(name, page)
                except CacheError as e:
                    self.send_error(500, None, explain=str(e))
                else:
                    self.send_response(204)
                    self.end_headers()

    def methodhandler(realhandler):
        @wraps(realhandler)
        def wrapper(self):
            logger.debug('INIT for method handler')

            # split query from pathname
            # take only the first set of parameters (i.e. everything
            # between the first ? and the subsequent / or #
            m = re.match('(/[^\?]*)(?:\?([^/#]*))?(.*)', self.path)
            query_str = m.group(2) if m.group(2) else ''
            self.__pathname = m.group(1) + m.group(3)

            # decode path
            #TODO other encodings??
            logger.debug('Path is {}'.format(self.__pathname))
            self.__pathname = urllib.parse.unquote_plus(
                    self.__pathname)
            logger.debug('Decoded path is {}'.format(self.__pathname))
            assert self.__pathname[0] == '/'
            # canonicalize it
            raw_path = self.__pathname
            self.__pathname = abspath(self.__pathname)
            logger.debug('Real path is {}'.format(self.__pathname))

            # save query parameters
            self.__query = param_dict(query_str, itemsep='&',
                    values_are_opt=True)
            logger.debug('Query params are {}'.format(self.__query))

            self.__can_read_body = True
            self.__body = None
            self.__allowed_methods = None # use default
            self.read_body()
            self.show()

            # check if it's a special endpoint
            try:
                root, sub, args = self.endpoints.parse(
                        raw_path, self.command)
            except NotAnEndpointError as e:
                logger.debug('{}'.format(str(e)))
                realhandler(self)
            except MethodNotAllowedError as e:
                logger.debug('{}'.format(str(e)))
                self.send_error(405)
            except (MissingArgsError, ExtraArgsError) as e:
                logger.debug('{}'.format(str(e)))
                self.send_error(404, None, str(e))
            else:
                self.__allowed_methods = self.endpoints.get(
                        root)[sub]['allowed_methods']
                if self.command == 'OPTIONS':
                    logger.debug('Doing OPTIONS')
                    realhandler(self)
                else:
                    logger.debug('Calling endpoint handler')
                    handler = getattr(self, 'do_' + root)
                    handler(sub, args)

        return wrapper

    @methodhandler
    def do_GET(self):
        logger.debug('GETting {}'.format(self.__pathname))

        if not self.is_secret() or \
             self.get_session() in self.__sessions:
            super().do_GET()
        else:
            self.send_error(401)

    @methodhandler
    def do_POST(self):
        self.do_GET.__wrapped__(self)

    @methodhandler
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_response_default()

    @methodhandler
    def do_HEAD(self):
        super().do_HEAD()

    methodhandler = staticmethod(methodhandler)

def abspath(path):
    '''Canonicalize the path segment by segment
    
    Leading slash is preserved if present, but is not required.
    '''

    if not path:
        return ''

    # if path doesn't start with /, temporarily add it so that
    prefix = ''
    if path[0] != '/':
        prefix = '/'
    # os.path.abspath doesn't prepend cwd
    # os.path.abspath preserves two consecutive slashes at the
    # beginning, since they may indicate a URI with a default
    # protocol; we explicitly remove them here
    return os.path.abspath(prefix + path).replace(
            '//','/')[len(prefix):]

def abspath_up_to_nth(path, n=1):
    '''Canonicalize the path segment by segment
    
    Leading slash is preserved if present, but is not required.
    Returns the path canonicalized to the first n segments, followed
    by the rest of the segments.
    Stop as soon as we have n non-empty segments, i.e.
    /../foo/../bar/./baz/./ will return /foo/../bar/./baz/./ for n=1,
    but /bar/baz/./ for n=2. If we never reach n, return ''
    '''

    if not path:
        return ''

    # temporarily add a trailing /
    pathlen = len(path)
    if path[-1] != '/':
        path += '/'

    curr_index = 0
    skip = path.find('/')
    root = path[: skip if skip != -1 else None]
    while skip != -1:
        curr_index += skip + 1
        curr_abs = abspath(path[:curr_index])
        curr_abs_parts = list(filter(None, curr_abs.split('/')))
        # filter because leading or trailing / will result in ''
        # items
        if len(curr_abs_parts) == n:
            return '/'.join(filter(None, [curr_abs,
                path[curr_index:pathlen]]))
        skip = path[curr_index+1:].find('/')

    return ''

def param_dict(s, itemsep=' *; *', valsep='=', values_are_opt=False):
    '''itemsep is a regex, valsep is literal'''

    params = dict()
    sepfunc = lambda x: x.split(valsep)
    if values_are_opt:
        sepfunc = lambda x: x.partition(valsep)[0::2]

    try:
        params = dict([sepfunc(v) for v in re.split(itemsep, s)])
    except ValueError:
        pass

    logger.debug('Got params from {}: {}'.format(s, params))
    return params

def new_server(clsname, cors, headers, is_SSL, secrets):
    def send_custom_headers(self):
        # Disable Cache
        # if request if garbage, e.g. HTTPS talking to HTTP
        #try:
        #    self._CORSHttpsServer__pathname
        #except AttributeError:
        #    return

        if not re.search('/jquery-[0-9\.]+(\.min)?\.js',
                self._CORSHttpsServer__pathname):
            self.send_header('Cache-Control',
                'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')

        for h in headers:
            self.send_header(*re.split(': *', h, maxsplit=1))

        # CORS, request path takes precedence
        # use origins=&creds=0 to disable CORS for this request
        allowed_origins = self.get_param('origin')
        if allowed_origins is None:
            allowed_origins = ', '.join(cors['origins'])
        allowed_origins = urllib.parse.unquote_plus(allowed_origins)
        if allowed_origins == '{ECHO}':
            allowed_origins = self.headers.get('Origin')
            if not allowed_origins: allowed_origins = '*'

        allowed_headers = ''
        if cors['headers']:
            allowed_headers = ', '.join(cors['headers'])

        allowed_methods = self._CORSHttpsServer__allowed_methods
        if not allowed_methods and cors['methods']:
            allowed_methods = cors['methods']
        if allowed_methods:
            allowed_methods = ', '.join(allowed_methods)

        allow_creds = self.get_param('creds')
        try:
            allow_creds = bool(int(allow_creds))
        except (ValueError,TypeError):
            # invalid or missing param
            allow_creds = cors['creds']

        if allowed_origins:
            self.send_header('Access-Control-Allow-Origin',
                allowed_origins)
        if allowed_headers:
            self.send_header('Access-Control-Allow-Headers',
                allowed_headers)
        if allowed_methods:
            self.send_header('Access-Control-Allow-Methods',
                allowed_methods)
        if allow_creds:
            self.send_header('Access-Control-Allow-Credentials',
                'true')

    return type(clsname, (CORSHttpsServer,), {
        '_is_SSL': is_SSL,
        '_secrets': list(filter(None, secrets)),
        'send_custom_headers': send_custom_headers})

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description='''Serve the current working directory over
            HTTPS and with custom headers. The CORS related options
            define the default behaviour. It can be overriden on
            a per-request basis using the origin and creds URL
            parameters. creds should be 0 or 1. origin is taken
            literally unless it is `{ECHO}`, then it is taken from the
            Origin header in the request.''')

    listen_parser = parser.add_argument_group('Listen options')
    listen_parser.add_argument('-a', '--address', dest='address',
            default='0.0.0.0', metavar='IP',
            help='''Address of interface to bind to.''')
    listen_parser.add_argument('-p', '--port', dest='port',
            metavar='PORT', type=int,
            help='''HTTP port to listen on. Default is 58080 if not
            over SSL or 58443 if over SSL.''')

    cors_parser = parser.add_argument_group('CORS options')
    ac_origin_parser = cors_parser.add_mutually_exclusive_group()
    ac_origin_parser.add_argument('-o', '--allowed-origins', dest='allowed_origins',
            default=[], metavar='Origin', nargs='*',
            help='''Allowed origins for CORS requests. Can be "*"''')
    ac_origin_parser.add_argument('-O', '--allow-all-origins',
            dest='allowed_origins', action='store_const', const=['{ECHO}'],
            help='''Allow all origins, i.e. echo the Origin in the
            request.''')
    cors_parser.add_argument('-x', '--allowed-headers', dest='allowed_headers',
            default=['Accept', 'Accept-Language', 'Content-Language',
                'Content-Type', 'Authorization'],
            metavar='Header: Value', nargs='*',
            help='''Headers allowed for CORS requests.''')
    cors_parser.add_argument('-m', '--allowed-methods', dest='allowed_methods',
            default=['POST', 'GET', 'OPTIONS', 'HEAD'], metavar='Method', nargs='*',
            help='''Methods allowed for CORS requests. OPTIONS to one
            of the special endpoints always return the allowed methods
            of that endpoint.''')
    cors_parser.add_argument('-c', '--allow-credentials', dest='allow_creds',
            default=False, action='store_true',
            help='''Allow sending credentials with CORS requests,
            i.e. add Access-Control-Allow-Credentials. Using this only
            makes sense if you are providing some list of origins (see
            -o and -O options), otherwise this option is ignored.''')

    ssl_parser = parser.add_argument_group('SSL options')
    ssl_parser.add_argument('-s', '--ssl', dest='ssl',
            default=False, action='store_true',
            help='''Use SSL.''')
    ssl_parser.add_argument('-C', '--cert', dest='certfile',
            default='./cert.pem', metavar='FILE',
            help='''PEM file containing the server certificate.''')
    ssl_parser.add_argument('-K', '--key', dest='keyfile',
            default='./key.pem', metavar='FILE',
            help='''PEM file containing the private key for the server
            certificate.''')

    misc_parser = parser.add_argument_group('Misc options')
    misc_parser.add_argument('-H', '--headers', dest='headers',
            default=[], metavar='Header: Value', nargs='*',
            help='''Additional headers to include in the response.''')
    misc_parser.add_argument('-S', '--secrets', dest='secrets',
            default=['secret'], metavar='DIR|FILE', nargs='*',
            help='''Directories or files which require a SESSION
            cookie. If no leading slash then it is matched anywhere in
            the path.''')
    misc_parser.add_argument('-l', '--logfile', dest='logfile',
            metavar='FILE',
            help='''File to write requests to. Will write to stdout if
            not given.''')
    misc_parser.add_argument('-d', '--debug', dest='loglevel',
            default=logging.INFO, action='store_const',
            const=logging.DEBUG,
            help='''Enable debugging output.''')
    misc_parser.add_argument('-t', '--multithread', dest='srv_cls',
            default=http.server.HTTPServer, action='store_const',
            const=ThreadingCORSHttpsServer,
            help='''Enable multi-threading support. EXPERIMENTAL! The
            cache has not been implemented in an MT safe way yet.''')
    args = parser.parse_args()

    if args.logfile is None:
        logger.addHandler(logging.StreamHandler(sys.stdout))
    else:
        logger.addHandler(logging.FileHandler(args.logfile))
    logger.setLevel(args.loglevel)

    if args.port is None:
        args.port = 58443 if args.ssl else 58080

    httpd = args.srv_cls((args.address, args.port),
            new_server('CORSHttpsServerCustom', {
                    'origins': args.allowed_origins,
                    'methods': args.allowed_methods,
                    'headers': args.allowed_headers,
                    'creds': args.allow_creds},
                args.headers,
                args.ssl,
                args.secrets))
    if args.ssl:
        httpd.socket = ssl.wrap_socket(
                httpd.socket,
                keyfile=args.keyfile,
                certfile=args.certfile,
                server_side=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.socket.close()
