import logging
import http.server
import re
import os
import errno
from datetime import datetime
import shutil
import mimetypes
import urllib
import json
from json import JSONDecodeError
import base64
import binascii
from wrapt import decorator
from string import Template

from ..dicts import CaseInsensitiveOrderedDict
from ..cookie import Cookie
from ..conf import Conf, ConfItem
from ..containers import DefaultDict
from ..endpoints import Endpoint
from ..endpoints.exc import NotAnEndpointError, \
    MethodNotAllowedError, MissingArgsError, ExtraArgsError
from ..utils import is_seq_like, abspath, param_dict, startswith
from .exc import DecodingError, UnsupportedOperationError


logger = logging.getLogger(__name__)


@decorator
def methodhandler(realhandler, self, args, kwargs):
    '''Decorator for do_{HTTP METHOD} handlers

    Sets the canonical pathname, query and body; checks if the request
    is allowed, and if it's for an endpoint.
    Calls the endpoint's handler or the HTTP method handler
    '''

    logger.debug(
        'INIT for method handler; path is {}'.format(self.path))

    # split query from pathname and decode them
    # take only the first set of parameters (i.e. everything
    # between the first ? and the subsequent #
    # TODO is that ^ right?
    m = re.match('^([^#\?]*)(?:\?([^#]+))?', self.path)
    query_str = urllib.parse.unquote_plus(m.group(2)) \
        if m.group(2) else ''
    self._BaseHTTPRequestHandler__raw_pathname = \
        self._BaseHTTPRequestHandler__pathname = \
        urllib.parse.unquote_plus(
            m.group(1) if m.group(1) else '/')

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
    except NotAnEndpointError as e:
        logger.debug(str(e))
        self._BaseHTTPRequestHandler__pathname = \
            self.pathname[len(self.conf.path_prefix):]
        logger.debug('Calling normal handler, path is {}'.format(
            self.pathname))
        realhandler(*args, **kwargs)
    except MethodNotAllowedError as e:
        logger.debug(str(e))
        self.save_header('Allow', ','.join(e.allowed_methods))
        if self.command == 'OPTIONS':
            logger.debug('Doing OPTIONS')
            realhandler(*args, **kwargs)
        else:
            self.send_error(405)
    except (MissingArgsError, ExtraArgsError) as e:
        logger.debug(str(e))
        self.send_error(400, explain=str(e))
    else:
        # strip the prefix before calling handler
        self._BaseHTTPRequestHandler__pathname = \
            self.pathname[len(self.conf.api_prefix):]
        logger.debug('Calling endpoint handler, path is {}'.format(
            self.pathname))
        self.ep.handler(*args, **kwargs)


############################################################
class BaseMeta(type):
    '''Metaclass for BaseHTTPRequestHandler

    Merges the configuration with that of the parents
    '''

    def __new__(cls, name, bases, attributes):
        new_class = super().__new__(cls, name, bases, attributes)

        # wrap method handlers
        for m in ['HEAD', 'GET', 'POST', 'PUT', 'PATCH', 'DELETE',
                  'TRACE', 'OPTIONS']:
            try:
                h = getattr(new_class, 'do_{}'.format(m))
            except AttributeError:
                continue

            try:
                # if we've already wrapped it, get the original one
                h = h.__wrapped__
            except AttributeError:
                pass

            setattr(new_class, 'do_{}'.format(m), methodhandler(h))

        # every child gets it's own class attribute for the following
        # ones, which combines the corresponding attribute of all parents
        attr_types = {
            'endpoints': Endpoint,
            'template_pages': DefaultDict,
            'templates': DefaultDict,
            'conf': Conf,
        }
        for attr, rcls in attr_types.items():
            new = rcls()
            for c in bases[::-1] + (new_class,):
                try:
                    curr = getattr(c, attr)
                except AttributeError:
                    continue
                new.update(curr)

            setattr(new_class, attr, new)
            logger.debug('Final {} for {}: {}'.format(
                attr, name, getattr(new_class, attr)))

        return new_class

class BaseHTTPRequestHandler(
        http.server.SimpleHTTPRequestHandler,
        metaclass=BaseMeta):
    conf = Conf(
        enable_directory_listing=False,
        path_prefix=ConfItem('', transformer=lambda s: s.rstrip('/')),
        api_prefix=ConfItem('', transformer=lambda s: s.rstrip('/')),
        api_is_JSON=True,
        send_software_info=False,
    )
    pollers = {}
    endpoints = Endpoint()

    def __init__(self, *args, **kwargs):
        self.__pathname = ''
        self.__raw_pathname = ''
        self.__query = dict()
        self.__can_read_body = True
        self.__body = None
        self.__ctype = None
        self.__params = None
        self.__headers_to_send = CaseInsensitiveOrderedDict()
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

    def set_path(self, value):
        self.path = self._BaseHTTPRequestHandler__pathname = value

    def lstrip_path(self, chars):
        self._path_strip(chars, func=str.lstrip)

    def rstrip_path(self, chars):
        self._path_strip(chars, func=str.rstrip)

    def strip_path(self, chars):
        self._path_strip(chars)

    def strip_path_prefix(self, prefix):
        self._path_substr(start=len(prefix))

    def strip_path_suffix(self, suffix):
        self._path_substr(end=-len(suffix))

    def strip_path_prefix_re(self, prefix_re):
        self._path_select_re('({})(.*)'.format(prefix_re), group=2)

    def strip_path_suffix_re(self, suffix_re):
        self._path_select_re('(.*)({})'.format(suffix_re), group=1)

    def _path_strip(self, chars, func=str.strip):
        path = self.pathname[1:]
        self.path = self._BaseHTTPRequestHandler__pathname = \
            '/' + func(path, chars)

    def _path_substr(self, start=0, end=-1):
        path = self.pathname[1:]
        self.path = self._BaseHTTPRequestHandler__pathname = \
            '/' + self._BaseHTTPRequestHandler__pathname[start, end]

    def _path_select_re(self, regex, group=1):
        path = self.pathname[1:]
        m = re.match(regex, path)
        if m is not None:
            self.path = self._BaseHTTPRequestHandler__pathname = \
                '/' + m.group(group)

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

    def begin_event_stream(self, headers={}):
        '''Begins a text/event-stream response'''

        self.send_response(200)
        self.send_header('Content-Type', 'text/event-stream')
        self.end_headers()

    def send_event(self, data, name=None, eid=None):
        '''Sends a single event

        The event stream must have been started
        - If name is given, an event: name is sent at the beginning
        - data can contain new lines, theses are properly handled by
          prepending data: at the start of each
        - If eid is given, an id: eid is sent at the end
        '''

        if name is not None:
            self.write('event: {}\n'.format(name))
        if isinstance(data, bytes):
            lines = data.split(b'\n')
        else:
            lines = data.split('\n')
        for line in lines:
            self.write('data: {}\n'.format(line))
        if eid is not None:
            self.write('id: {}\n'.format(eid))
        return self.write('\n')

    def send_response_goto(self, *args, **kwargs):
        '''begin_response_goto and end_response_default'''

        self.begin_response_goto(*args, **kwargs)
        self.end_response_default()

    def send_response_default(self, *args, **kwargs):
        '''Alias for send_response_empty; child class may override'''

        return self.send_response_empty(*args, **kwargs)

    def send_response_empty(self, code=204, headers={}):
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

        self.send_header('Content-Length', 0)
        self.end_headers()

    def show(self):
        '''Logs the request'''

        logger.trace('''
----- Request Start ----->

{}
{}
{}

<----- Request End -----
'''.format(self.requestline, self.headers, self.body))

    def render(self, page, code=200, message=None, headers={}):
        '''Renders a page

        page: a dictionary with the following items:
            - data: the content of the page
            - type: the content type
        headers: additional headers to send
        '''

        self.send_response(code, message=None)
        self.send_header('Content-Type', page['type'])
        self.send_header('Content-Length', len(page['data']))
        self.send_headers(headers)
        self.end_headers()
        self.write(page['data'])

    def write(self, data):
        if not isinstance(data, bytes):
            data = data.encode('utf-8')
        try:
            self.wfile.write(data)
        except BrokenPipeError:
            logger.debug('Client closed the connection')
            return False
        return True

    def send_file(self, path=None, as_attachment=False):
        '''Sends the file given in path

        - path defaults to the URL (minus the leading / of course)
        - If as_attachment is True, we add Content-Disposition:
          attachment
        If path is a directory, will raise IsADirectoryError
        '''

        if path is None:
            path = self.pathname[1:]
        if path == '':
            path = '.'  # will raise IsADirectoryError
        logger.debug('Requested file {}'.format(path))
        try:
            f = open(path, 'rb')
        except OSError as e:
            if e.errno == errno.ENOENT:
                self.send_error(404)
            elif e.errno == errno.EACCES:
                self.send_error(403)
            elif e.errno == errno.EISDIR:
                raise
            else:
                self.send_error(500)
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

    def send_as_file(self, content, filename=None, ctype=None):
        '''Send the content as an attachment.

        Content-Type is guessed from the filename if not given and
        defaults to application/octet-stream.
        '''

        self.send_response(200)
        if ctype is None and filename is not None:
            ctype = mimetypes.guess_type(filename)[0]
        if ctype is None:
            ctype = 'application/octet-stream'
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', len(content))
        disposition = 'attachment'
        if filename is not None:
            disposition += '; filename={}'.format(filename)
        self.send_header('Content-Disposition', disposition)
        self.end_headers()
        self.write(content)

    def send_as_JSON(self,
                     obj=None,
                     serializer=None,
                     indent=None,
                     code=200,
                     message=None,
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
            message=message,
            headers=headers)

    def page_from_template(self, template, dynfields={}):
        '''Returns a page from the given template'''

        try:
            page = self.template_pages[template['page']].copy()
        except KeyError:
            logger.debug('Using default template page')
            page = self.template_pages['default'].copy()

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
            page['data'] = page['data'].encode(
                'utf-8', errors='backslashreplace')

        return page

    def __read_body(self):
        '''Sets __body to the body data

        methodhandler calls this and it cannot be called again
        '''

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
            return data.decode('utf-8', errors='backslashreplace')

    def save_header(self, header, value, append=False):
        '''Saves a header to be sent by end_headers

        - If append is True (default) a duplicate header may be added,
          common with Content-Security-Policy for example. Otherwise
          the given header replaces any currently saved ones by that name.
        For cookies, use save_cookie instead.
        '''

        new = []
        if header.lower() == 'set-cookie':
            return self.save_cookie(*value.split('=', maxsplit=1))
        if append:
            new = self.__headers_to_send.get(header, [])
        new.append(value)
        self.__headers_to_send[header] = new

    def save_cookie(self, *args, **kwargs):
        '''Saves a Set-Cookie header to be sent by end_headers

        It overrides any previously saved cookies with that name.
        '''

        if len(args) == 1 and not kwargs:
            if isinstance(args[0], Cookie):
                cookie = args[0]
            else:
                cookie = Cookie.parse(args[0])
        else:
            cookie = Cookie(*args, **kwargs)

        new = list(filter(
            lambda c: c.name.lower() != cookie.name.lower(),
            self.__headers_to_send.get('Set-Cookie', [])))
        new.append(cookie)
        self.__headers_to_send['Set-Cookie'] = new

    def saved_headers(self):
        '''Returns the saved headers'''

        return self.__headers_to_send

    def save_param(self, key, value, is_list=False):
        '''Saves a key--value to be sent by send_as_JSON

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
        '''Calls parent's send_error with the correct signature'''

        if startswith(self.path, self.conf.api_prefix) \
                and self.conf.api_is_JSON:
            # TODO customize the error parameter name
            self.save_param('error', explain)
            self.send_as_JSON(code=code, message=message)
        else:
            super().send_error(code, message=message, explain=explain)

    def send_response(self, code, message=None):
        '''Makes the Server header optional'''

        self.log_request(code)
        self.send_response_only(code, message)
        if self.conf.send_software_info:
            self.send_header('Server', self.version_string())
        self.send_header('Date', self.date_time_string())

    def log_request(self, code='-', size='-'):
        '''Log an accepted request

        This is called by send_response().
        '''

        if isinstance(code, http.HTTPStatus):
            code = code.value
        self.log_message(
            '"{}" {!s} {!s}', self.requestline, code, size)

    def log_error(self, fmt, *args, **kwargs):
        self._log_message(logging.ERROR, fmt, *args, **kwargs)

    def log_message(self, fmt, *args, **kwargs):
        self._log_message(logging.INFO, fmt, *args, **kwargs)

    def _log_message(self, level, fmt, *args, **kwargs):
        '''Uses the logger'''

        logger.log(
            level,
            '{addr} - - [{date}] {rest}'.format(
                addr=self.address_string(),
                date=self.log_date_time_string(),
                rest=fmt.format(*args, **kwargs)))

    def do_default(self):
        '''Default handler for endpoints'''

        self.send_response_default()

    def do_GET(self):
        '''Decorated by methodhandler'''

        try:
            self.send_file()
        except IsADirectoryError:
            logger.debug("It's a directory")
            if self.conf.enable_directory_listing:
                super().do_GET()
            else:
                self.send_error(403)

    def do_POST(self):
        '''Decorated by methodhandler'''

        self.send_error(405)

    def do_HEAD(self):
        '''Decorated by methodhandler'''

        super().do_HEAD()

    def do_OPTIONS(self):
        '''Decorated by methodhandler'''

        self.send_response_empty()
