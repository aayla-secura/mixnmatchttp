#  from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import *
from future import standard_library
standard_library.install_aliases()
from future.utils import with_metaclass

import logging
import http.server
import re
import os
from datetime import datetime
import shutil
import mimetypes
import urllib
import json
try:  # python3
    from json import JSONDecodeError
except ImportError:  # python2
    JSONDecodeError = ValueError
import base64
import binascii
from wrapt import decorator
from string import Template

from .. import endpoints
from ..utils import is_seq_like, abspath, param_dict, DictNoClobber

__all__ = [
    'methodhandler',
    'InvalidRequestError',
    'PageReadError',
    'UnsupportedOperationError',
    'DecodingError',
    'BaseMeta',
    'BaseHTTPRequestHandler',
]

logger = logging.getLogger(__name__)


@decorator
def methodhandler(realhandler, self, args, kwargs):
    '''Decorator for do_{HTTP METHOD} handlers

    Sets the canonical pathname, query and body; checks if the request
    is allowed, and if it's for an endpoint.
    Calls the endpoint's handler or the HTTP method handler
    '''

    logger.debug('INIT for method handler')
    logger.debug('Path is {}'.format(self.path))

    # split query from pathname and decode them
    # TODO other encodings??
    # take only the first set of parameters (i.e. everything
    # between the first ? and the subsequent / or #
    m = re.match('(/[^\?]*)(?:\?([^/#]*))?(.*)', self.path)
    query_str = urllib.parse.unquote_plus(m.group(2)) \
        if m.group(2) else ''
    self._BaseHTTPRequestHandler__raw_pathname = \
        self._BaseHTTPRequestHandler__pathname = \
        urllib.parse.unquote_plus(m.group(1) + m.group(3))

    logger.debug('Decoded path is {}'.format(self.pathname))
    # canonicalize the path
    self._BaseHTTPRequestHandler__pathname = abspath(self.pathname)
    logger.debug('Real path is {}'.format(self.pathname))
    assert self.pathname[0] == '/'

    # save query parameters
    self._BaseHTTPRequestHandler__query = param_dict(
        query_str, itemsep='&', values_are_opt=True)
    logger.debug('Query params are {}'.format(self.query))

    self._BaseHTTPRequestHandler__read_body()

    # save content-type and body parameters
    try:
        self._BaseHTTPRequestHandler__decode_body()
    except DecodingError as e:
        self.send_error(400, explain=str(e))
        return

    self.show()
    # check if it's forbidden
    err = self.denied()
    if err is not None:
        self.send_error(*err)
        return

    # check if it's a special endpoint
    try:
        self.ep = self.endpoints.parse(self)
    except endpoints.NotAnEndpointError as e:
        logger.debug('{}'.format(str(e)))
        realhandler(*args, **kwargs)
    except endpoints.MethodNotAllowedError as e:
        logger.debug('{}'.format(str(e)))
        self.save_header('Allow', ','.join(e.allowed_methods))
        if self.command == 'OPTIONS':
            logger.debug('Doing OPTIONS')
            realhandler(*args, **kwargs)
        else:
            self.send_error(405)
    except (endpoints.MissingArgsError,
            endpoints.ExtraArgsError) as e:
        logger.debug('{}'.format(str(e)))
        self.send_error(400, explain=str(e))
    else:
        logger.debug('Calling endpoint handler')
        self.ep.handler(*args, **kwargs)

######################### EXCEPTIONS ########################

class InvalidRequestError(Exception):
    '''Base class for exceptions raised when request is invalid'''

    pass

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

############################################################
class BaseMeta(type):
    '''Metaclass for BaseHTTPRequestHandler

    Adds each of the parents' endpoints, templates and template pages
    '''

    def __new__(cls, name, bases, attrs):
        # TODO check attributes set after class creation
        new_class = super().__new__(cls, name, bases, attrs)

        logger.debug('New class {}; bases: {}'.format(
            name, [b.__name__ for b in bases]))
        # every child gets it's own class attribute for _endpoints,
        # _template_pages and _templates, which combines all parents'
        # attributes
        required_classes = {
            '_endpoints': endpoints.Endpoint,
            '_template_pages': DictNoClobber,
            '_templates': DictNoClobber,
        }
        for attr in ['_endpoints', '_template_pages', '_templates']:
            try:
                dic = getattr(new_class, attr)
            except AttributeError:
                dic = required_classes[attr]()
                logger.debug('Initialized blank {}'.format(attr))
            if not isinstance(dic, required_classes[attr]):
                logger.debug('Converting {} to {}'.format(
                    attr, required_classes[attr].__name__))
                dic = required_classes[attr](dic)
            setattr(new_class, attr, dic)

            for bc in bases[::-1]:
                if hasattr(bc, attr):
                    dic.update_noclob(getattr(bc, attr))
            logger.debug('Final {} for {}: {}'.format(
                attr, name, list(getattr(new_class, attr).keys())))

        return new_class

class BaseHTTPRequestHandler(with_metaclass(
        BaseMeta, http.server.SimpleHTTPRequestHandler, object)):
    pollers = {}
    _endpoints = endpoints.Endpoint()
    _template_pages = DictNoClobber(
        default={
            'data': '''
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8" />
    $HEAD
    </head>
    <body>
    $BODY
    </body>
    </html>
    ''',
            'type': 'text/html'
        },
    )
    _templates = DictNoClobber()

    # copy the class attributes to instance ones, since Endpoint and
    # dicts are mutable
    # the alternative solution of setting it in __init__ would require
    # checking if such an attribute already exists (set by a child
    # class), then update_noclob, before calling the parent's __init__
    # method
    # we can't call parent's __init__ before updating endpoints, since
    # BaseHTTPRequestHandler's __init__ calls do_{METHOD} and all
    # attributes of child classes need to be set by that time
    @property
    def endpoints(self):
        '''Property the class' endpoints

        Copies the endpoints to an instance attribute the first time
        it is accessed so they can be modified for the instance
        '''

        if self._endpoints is self.__class__._endpoints:
            self._endpoints = self._endpoints.copy()
        return self._endpoints

    @endpoints.setter
    def endpoints(self, value):
        self._endpoints = value

    @property
    def templates(self):
        '''Property the class' template

        Copies the templates to an instance attribute the first time
        it is accessed so they can be modified for the instance
        '''

        if self._templates is self.__class__._templates:
            self._templates = self._templates.copy()
        return self._templates

    @templates.setter
    def templates(self, value):
        self._templates = value

    @property
    def template_pages(self):
        '''Property the class' template pages

        Copies the template pages to an instance attribute the first
        time it is accessed so they can be modified for the
        instance
        '''

        if self._template_pages is self.__class__._template_pages:
            self._template_pages = self._template_pages.copy()
        return self._template_pages

    @template_pages.setter
    def template_pages(self, value):
        self._template_pages = value

    def __init__(self, *args, **kwargs):
        logger.debug('INIT for {}'.format(self))
        self.__pathname = ''
        self.__raw_pathname = ''
        self.__query = dict()
        self.__can_read_body = True
        self.__body = None
        self.__ctype = None
        self.__params = None
        self.__headers_to_send = {}
        self.__params_to_send = {}
        super().__init__(*args, **kwargs)

    @property
    def raw_pathname(self):
        '''Property for the request's pathname pre-canonicalization'''

        return self.__raw_pathname

    @property
    def pathname(self):
        '''Property for the request's pathname'''

        return self.__pathname

    @property
    def body(self):
        '''Property for the decoded request's body

        Raises a UnicodeDecodeError if we can't decode
        '''

        try:
            body = self.__body.decode('utf-8')
        except UnicodeDecodeError:
            logger.debug('Errors decoding request body')
            body = self.__body.decode(
                'utf-8', errors='backslashreplace')
        return body

    @property
    def ctype(self):
        '''Property for the request's Content-Type'''

        return self.__ctype

    @property
    def params(self):
        '''Property for the request's body parameters'''

        return self.__params

    @property
    def query(self):
        '''Property for the request's query dictionary'''

        return self.__query

    def get_param(self, parname, dic=None):
        '''Returns the value of parname inside dic

        dic is a dictionary, if None, then the body paramaters are
        checked first, then the URL parameters
        '''

        if dic is None:
            dic = self.__query
            if isinstance(self.__params, dict):
                # for JSON data, it could be a list
                dic.update(self.__params)
        try:
            value = dic[parname]
        except KeyError:
            return None

        return value

    def form_params(self, post_data=None):
        '''Parameter loader

        Returns a dictionary read from an
        application/x-www-form-urlencoded form
        post_data defaults to the request body
        '''

        logger.debug('Loading parameters from form body')
        if post_data is None:
            post_data = self.body
        req_params = param_dict(post_data, itemsep='&',
                                decoder=urllib.parse.unquote_plus)
        if not req_params:
            raise DecodingError(
                'Cannot load parameters from request!')
        return req_params

    def JSON_params(self, post_data=None):
        '''Parameter loader

        Returns a dictionary read from a JSON string
        post_data defaults to the request body
        '''

        logger.debug('Loading parameters from JSON body')
        if post_data is None:
            post_data = self.body
        try:
            req_params = json.loads(post_data)
        except JSONDecodeError:
            raise DecodingError('Cannot decode JSON!')
        return req_params

    def denied(self):
        '''Child class overrides this

        Returns None if allowed or a tuple(code, message, explain)
        '''

        return None

    def no_cache(self):
        '''Child overrides this

        Returns True or False if the response should not be cached by
        the browser
        '''

        return False

    def send_cache_control(self):
        '''Sends a no-caching directive if no_cache returns True'''

        if self.no_cache():
            self.send_header('Cache-Control',
                             'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')

    def send_custom_headers(self):
        '''Called from end_headers; child overrides this'''

        pass

    def send_headers(self, headers):
        '''Sends multiple headers

        headers is a dictionary of header names as keys; each value is
        either a string, or a list of strings, in which case multiple
        headers are sent (one for each value)
        '''

        for h, v in headers.items():
            if is_seq_like(v):
                for i in v:
                    self.send_header(h, i)
            else:
                self.send_header(h, v)

    def begin_response_goto(self, code=302, url=None, headers={}):
        '''Starts a redirection response

        code: HTTP code
        url: Location header; if None, then the goto URL parameter is
        taken; if that one is missing, then the response code is 200
        headers: additional headers to send
        '''

        if url is None:
            url = self.get_param('goto')
        if url is not None:
            self.send_response(code)
            logger.debug('Redirecting to {}'.format(url))
            #  it's already been decoded once
            self.send_header('Location', url)
        else:
            self.send_response(200)
        self.send_headers(headers)

    def send_response_goto(self, *args, **kwargs):
        '''begin_response_goto and end_response_default'''

        self.begin_response_goto(*args, **kwargs)
        self.end_response_default()

    def send_response_default(self, *args, **kwargs):
        '''Alias for send_response_empty; child class may override'''

        return self.send_response_empty(*args, **kwargs)

    def send_response_empty(self, code=200, headers={}):
        '''Send an empty response

        headers: additional headers to send
        '''

        self.send_response(code)
        self.send_headers(headers)
        self.end_response_empty()

    def end_response_default(self):
        '''Alias for end_response_empty; child class may override'''

        return self.end_response_empty()

    def end_response_empty(self):
        '''Ends an empty response'''

        #  self.send_header('Content-type', 'text/plain')
        self.send_header('Content-Length', 0)
        self.end_headers()

    def show(self):
        '''Logs the request'''

        logger.log(1, '''
----- Request Start ----->

{}
{}
{}

<----- Request End -----
'''.format(self.requestline, self.headers, self.body))

    def render(self, page, code=200, headers={}):
        '''Renders a page

        page: a dictionary with the following items:
            - data: the content of the page
            - type: the content type
        headers: additional headers to send
        '''

        self.send_response(code)
        self.send_header('Content-Type', page['type'])
        self.send_header('Content-Length', len(page['data']))
        self.send_headers(headers)
        self.end_headers()
        self.wfile.write(page['data'])

    def send_file(self, path=None, as_attachment=False):
        '''Sends the file given in path

        - path defaults to the URL (minus the leading / of course)
        - If as_attachment is True, we add Content-Disposition:
          attachment
        '''

        if path is None:
            path = self.pathname[1:]
        try:
            f = open(path, 'rb')
        except FileNotFoundError:
            self.send_error(404)
            return
        except PermissionError:
            self.send_error(403)
            return
        fs = os.fstat(f.fileno())
        self.send_response(200)
        ctype = mimetypes.guess_type(path)[0]
        if ctype is None:
            ctype = 'application/octet-stream'
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(fs.st_size))
        self.send_header(
            'Last-Modified',
            datetime.utcfromtimestamp(fs.st_mtime).strftime(
                '%Y-%m-%d %H:%M:%S UTC'))
        disposition = 'filename={}'.format(os.path.basename(f.name))
        if as_attachment:
            disposition = 'attachment; {}'.format(disposition)
        self.send_header('Content-Disposition', disposition)
        self.end_headers()
        shutil.copyfileobj(f, self.wfile)
        f.close()

    def send_as_json(self,
                     obj=None,
                     serializer=None,
                     indent=None,
                     code=200,
                     headers={}):
        '''Sends an object as a JSON response

        - If obj is None, then the parameters saved by save_param will
          be sent.
        '''

        _obj = obj
        if _obj is None:
            _obj = self.__params_to_send
        self.render(
            {
                'data': json.dumps(_obj,
                                   default=serializer,
                                   indent=indent).encode('utf-8'),
                'type': 'application/json'},
            code=code,
            headers=headers)

    def page_from_template(self, template, dynfields={}):
        '''Returns a page from the given template'''

        try:
            page = self._template_pages[template['page']].copy()
        except KeyError:
            logger.debug('Using default template page')
            page = self._template_pages['default'].copy()

        try:
            fields = template['fields']
        except KeyError:
            logger.debug('No fields for template')
            fields = {}

        page['data'] = Template(page['data']).safe_substitute(fields)

        # it's allowed to have the same field in the template as well
        # as in the page's field values (e.g. fields['BODY'] also has
        # '$BODY' in there. The second one will be replaced with the
        # value from dynfields; so don't coalesce fields and dynfields
        # together
        page['data'] = Template(
            page['data']).safe_substitute(dynfields)

        # remove unused fields and encode
        page['data'] = re.sub('\$[a-zA-Z0-9_]+', '', page['data'])
        try:
            page['data'] = page['data'].encode('utf-8')
        except UnicodeEncodeError:
            logger.debug('Errors encoding page body')
            page['data'] = page['data'].encode(
                'utf-8', errors='backslashreplace')

        return page

    def __read_body(self):
        '''Sets __body to the body data

        methodhandler calls this and it cannot be called again
        '''

        logger.debug('Decoding body')
        if not self.__can_read_body:
            raise UnsupportedOperationError

        try:
            length = int(self.headers.get('Content-Length'))
        except TypeError:
            self.__body = b''
        else:
            self.__body = self.rfile.read(length)

        logger.debug(
            'Read {} bytes from body'.format(len(self.__body)))
        self.__can_read_body = False

    def __decode_body(self):
        '''Decodes the request, sets __ctype and __params

        __ctype is the Content-Type and __params is a dictionary of
        parameters. If Content-Type is neither JSON nor URL-encoded
        form, __params is empty
        raises DecodingError on failure
        '''

        if not self.__body:
            param_loader = lambda: {}
            ctype = None
        else:
            ctype = self.headers.get('Content-Type')
            if ctype is None:
                raise DecodingError(
                    'Missing Content-Type with non-empty body')
            ctype = ctype.split(';', 1)[0]
            if ctype in ['application/json', 'text/json']:
                param_loader = self.JSON_params
            elif ctype == 'application/x-www-form-urlencoded':
                param_loader = self.form_params
            else:
                logger.debug("Don't know how to read body parameters")
                param_loader = lambda: {}

        self.__params = param_loader()
        self.__ctype = ctype
        logger.debug('Request parameters: {}'.format(self.__params))

    @staticmethod
    def url_data(data_enc):
        '''Data decoder

        Returns the percent-decoded data
        '''

        try:
            data = urllib.parse.unquote_plus(data_enc)
        except (TypeError, AttributeError):
            raise DecodingError('Cannot URL decode request data!')
        return data

    @staticmethod
    def b64_data(data_enc):
        '''Data decoder

        Returns the base64-decoded data
        '''

        try:
            data = base64.b64decode(data_enc)
        except (TypeError, binascii.Error):
            raise DecodingError('Cannot Base64 decode request data!')
        try:
            return data.decode('utf-8')
        except UnicodeDecodeError:
            logger.debug('Errors decoding base64 data')
            return data.decode('utf-8', errors='backslashreplace')

    def save_header(self, header, value, append=True):
        '''Saves a header to be sent at the end

        end_headers will send those.
        - If append is True (default) a duplicate header may be added,
          common with Set-Cookie. Otherwise the given header replaces
          any currently saved ones by that name.
        '''

        new = []
        if append:
            new = self.__headers_to_send.get(header, [])
        new.append(value)
        self.__headers_to_send[header] = new

    def saved_headers(self):
        '''Returns the saved headers'''

        return self.__headers_to_send

    def save_param(self, key, value, is_list=False):
        '''Saves a key--value to be sent by send_as_json

        - If is_list is True, then the key is saved as a list, i.e.
          the first time key will be [value], and if key has already
          been given, then value is appended.
        '''

        if not is_list:
            self.__params_to_send[key] = value
            return
        if key not in self.__params_to_send:
            self.__params_to_send[key] = []
        elif not is_seq_like(self.__params_to_send[key]):
            self.__params_to_send[key] = [
                self.__params_to_send[key]]
        self.__params_to_send[key].append(value)

    def saved_params(self):
        '''Returns the saved parameters'''

        return self.__params_to_send

    def end_headers(self):
        '''Sends all custom headers and calls end_headers

        Calls send_custom_headers, send_cache_control and sends this
        requests's saved headers (added by save_headers).
        '''

        logger.debug(
            'Sending final headers; this request has {}'.format(
                self.__headers_to_send))
        self.send_headers(self.__headers_to_send)
        self.send_custom_headers()
        self.send_cache_control()
        super().end_headers()

    def send_error(self, code, message=None, explain=None):
        '''Calls parent's send_error with the correct signature

        In python2, send_error does not accept the explain keyword
        argument
        '''

        try:
            super().send_error(code, message=message, explain=explain)
        except TypeError:
            super().send_error(code, message=message)

    def do_default(self):
        '''Default handler for endpoints'''

        self.send_response_default()

    @methodhandler
    def do_GET(self):
        '''Decorated by methodhandler'''

        super().do_GET()

    @methodhandler
    def do_POST(self):
        '''Decorated by methodhandler'''

        super().do_GET()

    @methodhandler
    def do_OPTIONS(self):
        '''Decorated by methodhandler'''

        self.send_response_empty()

    @methodhandler
    def do_HEAD(self):
        '''Decorated by methodhandler'''

        super().do_HEAD()
