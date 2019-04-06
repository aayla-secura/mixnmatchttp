#  from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import super
from builtins import filter
from builtins import str
from future import standard_library
standard_library.install_aliases()
import logging
from functools import partial
from wrapt import ObjectProxy

from .common import iter_abspath, DictNoClobber

ARGS_OPTIONAL = '?' # 0 or 1
ARGS_ANY = '*'      # any number
ARGS_REQUIRED = '+' # 1 or more

_logger = logging.getLogger(__name__)

######################### EXCEPTIONS ########################

class EndpointError(Exception):
    '''Base class for exceptions related creation of endpoints'''

    pass

class EndpointTooDeepError(EndpointError):
    '''Exception raised when an endpoint is too deep in the hierarchy'''
    def __init__(self, root):
        super(EndpointTooDeepError, self).__init__(
                "{}'s level is too deep.".format(root))

class EndpointParseError(Exception):
    '''Base class for exceptions related parsing of endpoints'''

    pass

class NotAnEndpointError(EndpointParseError):
    '''Exception raised when the root path is unknown'''

    def __init__(self, root):
        super(NotAnEndpointError, self).__init__(
                '{} is not special.'.format(root))

class MethodNotAllowedError(EndpointParseError):
    '''Exception raised when the request method is not allowed'''

    def __init__(self):
        super(MethodNotAllowedError, self).__init__(
                'Method not allowed.')

class MissingArgsError(EndpointParseError):
    '''Exception raised when a required argument is not given'''

    def __init__(self):
        super(MissingArgsError, self).__init__(
                'Missing required argument.')

class ExtraArgsError(EndpointParseError):
    '''Exception raised when extra arguments are given'''

    def __init__(self, nargs):
        super(ExtraArgsError, self).__init__(
                'Extra arguments: {}.'.format(nargs))

############################################################

class Endpoint(DictNoClobber):
    '''Special endpoints
    
    The Endpoint constructor has the same signature as for
    a dictionary. For example you can define the endpoints like so:
        _endpoints = endpoints.Endpoints(
                some_sub={
                    '$allowed_methods': {'GET', 'POST'},
                    '$nargs': 1,
                    'some_sub_sub': {
                        '$nargs': endpoints.ARGS_ANY,
                        '$raw_args': True, # don't canonicalize path
                        }
                    },
                )
    Any keyword arguments or dictionary keys starting with
    $ correspond to an attribute (without the $). All other keyword
    arguments/keys become subpoints of the parent; their value
    should be either another Endpoint (in which case it is copied),
    or a plain dictionary.
    All child endpoints are enabled by default. The root endpoint is
    disabled by default; if you want it enabled, either manually
    change the 'disabled' attribute, or construct it like so:
        _endpoints = endpoint.Endpoints({
            'some_sub': { ... },
            '$disabled': False,
            })
    or like so:
        _endpoints = endpoint.Endpoints({
            '$disabled': False,
            },
            some_sub={ ... }
            )
    
    Recognized attributes:
        disabled: <bool>, defaults to True for the root, False otherwise
        allowed_methods: <set>, defaults to {'GET'}
        nargs: <number>|ARGS_*, defaults to 0
        raw_args: <bool>, defaults to False

    The class attribute _max_level defines the maximum depth of the
    endpoint hierarchy, and defaults to 20.
    '''

    _max_level = 20
    __curr_level = -1

    @property
    def disabled(self):
        '''Returns whether endpoint is disabled
        
        If not explicitly set, returns True. This should only happen
        for the root endpoint.'''

        try:
            return self._disabled
        except AttributeError:
            return True

    @disabled.setter
    def disabled(self, value):
        '''Sets the endpoint's disabled attribute'''

        self._disabled = bool(value)

    def __init__(self, *args, **kwargs):
        self.allowed_methods = {'GET'}
        self.nargs = 0
        self.raw_args = False

        try:
            self.__class__.__curr_level += 1
            super(Endpoint, self).__init__(*args, **kwargs)
            _logger.debug('Level: {}; list of subpoints: {}'.format(
                self.__curr_level, list(self.keys())))
            self.__class__.__curr_level -= 1
        except Exception as e:
            self.__class__.__curr_level = -1
            raise e

        if self.raw_args and self.nargs not in [ARGS_ANY, ARGS_REQUIRED]:
            _logger.warning(('Endpoint requires raw ' +
                'arguments, but is sensitive to the number ' +
                'of arguments; not reliable!'))
        if self.raw_args and self.keys():
            raise EndpointError(
                    "Endpoints expecting raw arguments cannot have subpoints.")

    def __setattr__(self, attr, value):
        if attr == 'allowed_methods':
            value |= {'HEAD', 'OPTIONS'}
        super(Endpoint, self).__setattr__(attr, value)

    def __setitem__(self, key, item):
        if self.__curr_level == self._max_level:
            raise EndpointTooDeepError(key)
        if not key:
            raise ValueError('Endpoint must be non-empty')

        if key[0] == '$':
            _logger.debug(
                    'Endpoint special key {}, setting as attribute'.format(key))
            getattr(self, key[1:]) # raise an exception if
                                   # attribute is unknown
            setattr(self, key[1:], item)
        else:
            _logger.debug('Creating endpoint {}'.format(key))
            if isinstance(item, Endpoint):
                super(Endpoint, self).__setitem__(key, item.copy())
            else:
                super(Endpoint, self).__setitem__(key, Endpoint(item))

            # Enable the subpoint, disabled was explicitly set
            try:
                self[key]._disabled
            except AttributeError:
                _logger.debug('Enabling endpoint {}'.format(key))
                self[key]._disabled = False

    def parse(self, httpreq):
        '''Selects an endpoint for the path
        
            httpreq: an instance of BaseHTTPRequestHandler
        
        If httpreq.raw_pathname resolves to an enpoint's path, returns
        a ParsedEndpoint initialized with the following attributes:
            httpreq: same as passed to this method
            handler: partial of the httpreq's method called
                'do_{root}' or 'do_default'; the first argument will be the ParsedEndpoint
            root: longest path of the endpoint corresponding to a defined handler
            sub: rest of the path of the endpoint
            args: everything following the endpoint's path (/root/sub/)
            argslen: actual number of arguments it was called with
        For example if an endpoint /cache/new/static accepts arguments,
        and httpreq has a method do_cache, but not
        do_cache_new_static, and not do_cache_new, a request for
        /cache/new/static/page will set ep.root to 'cache', ep.sub to
        'new/static', ep.handler to partial(httpreq.do_cache, ep),
        ep.args to 'page', and ep.argslen to 1.
        
        If path doesn't resolve to an enpoint's path raises an exception:
            NotAnEndpointError
            MethodNotAllowedError
            MissingArgsError
            ExtraArgsError
        '''

        path = httpreq.raw_pathname
        if not path or path[0] != '/':
            raise ValueError('Path for endpoint parsing must begin with a /')

        # we don't yet know if the endpoint wants the arguments raw or
        # canonicalized. So we check each absolute segment; if it's an
        # endpoint remember it, check next
        _logger.debug('Checking if endpoint takes raw arguments')
        ep = None
        handler = httpreq.do_default
        root = sub = args = ''
        for curr_path, curr_args in iter_abspath(path):
            _logger.debug('Current abspath segment: {}'.format(curr_path))
            curr_ep, curr_handler, curr_root, curr_sub = \
                    self._select_handler(curr_path, httpreq)

            if curr_ep is None:
                _logger.debug('No match on this level')
                continue

            ep = curr_ep
            handler = curr_handler
            root = curr_root
            sub = curr_sub
            args = curr_args
            _logger.debug(
                    'Match on this level: root: {}, sub: {}, args: {}'.format(
                        root, sub, args))

            if ep.raw_args:
                _logger.debug('{}({}) is "raw"; done'.format(root, sub))
                break # don't inspect rest of path

        if ep is None or ep.disabled:
            if ep is not None:
                _logger.debug('{} is disabled'.format(root))
            raise NotAnEndpointError(path)

        # either entire canonical path resolved to an endpoint, or
        # part of it resolved to an endpoint expecting raw arguments;
        # either way, we're done
        args_arr = list(filter(None, args.split('/')))

        ep = ParsedEndpoint(ep,
                httpreq,
                handler,
                root,
                sub,
                args,
                len(args_arr))

        _logger.debug(
                'API call: {}, root: {}, sub: {}, {} args: {}'.format(
                    ep, ep.root, ep.sub, ep.argslen, ep.args))

        if ep.nargs == ARGS_ANY:
            pass
        elif ep.nargs == ARGS_REQUIRED:
            if not ep.args:
                raise MissingArgsError
        elif ep.nargs == ARGS_OPTIONAL:
            if ep.argslen > 1:
                raise ExtraArgsError('/'.join(args_arr[1:]))
        elif ep.argslen > ep.nargs:
            raise ExtraArgsError('/'.join(
                args_arr[ep.nargs:]))
        elif ep.argslen < ep.nargs:
            raise MissingArgsError

        if httpreq.command not in ep.allowed_methods:
            raise MethodNotAllowedError

        return ep

    def iter_path(self, path):
        '''Returns a generator for list(endpoints, curr_path) for each path segment
        
        path must be canonical (no double //, no ./ or ../).
        '''

        _logger.debug('Getting endpoints from path {}'.format(path))
        ep = self
        curr_path = ''
        pref = ''
        if path[0] == '/':
            pref = '/'
            path = path[1:]
        suf = ''
        if path[-1] == '/':
            suf = '/'
            path = path[:-1]
        for p in path.split('/'):
            curr_path += '/' + p
            _logger.debug(
                    'Current list of subpoints: {}; trying {}'.format(
                        list(ep.keys()), p))
            try:
                ep = ep[p]
            except KeyError:
                return
            yield ep, pref + curr_path[1:] + suf

        _logger.debug('Final: {}'.format(pref + curr_path[1:] + suf))

    def get_from_path(self, path, httpreq=None):
        '''Returns an endpoint with the given path or None
        
        path must be canonical (no double //, no ./ or ../).
        '''

        for ep, ep_path in self.iter_path(path):
            _logger.debug('{} is an endpoint'.format(ep_path))
            if ep_path == path:
                return ep

        return None

    def _select_handler(self, path, httpreq):
        '''Selects the endpoint and handler for the given path
        
            path: <str>, the path to be parsed
            httpreq: an instance of BaseHTTPRequestHandler
        
        path must be canonical (no double //, no ./ or ../).
        
        Returns (ep, handler, root, sub) where
            ep: the last defined endpoint along the given path, e.g.
                if there's an endpoint at /a/b/c and it has no
                children, it will be selected for all paths beginning
                with /a/b/c
            handler: httpreq's endpoint handler with the most specific
                path matching the given path, e.g. if there's a handler 
                do_a_b but not do_a_b_*, do_a_b will be selected for
                all endpoints starting with /a/b; if no matching
                handler is defined, do_default is returned
            root: the beginning of the path which matched a handler,
                e.g. /a/b if do_a_b is defined, or '' if no matching
                handler
            sub: the rest of the path after root/ (leading / is
                stripped)
        '''

        ep = handler = None
        ep_path = root = sub = ''
        _logger.debug('Iterating over path {}'.format(path))
        for ep, ep_path in self.iter_path(path):
            _logger.debug('{} is an endpoint'.format(ep_path))
            try:
                curr_handler = getattr(
                        httpreq, 'do' + ep_path.replace('/', '_'))
            except AttributeError:
                _logger.debug('No handler for {}'.format(ep_path))
            else:
                _logger.debug('Found handler for {}'.format(ep_path))
                root = ep_path
                handler = curr_handler
        
        # skip leading slash of sub
        sub = path[len(root)+1:]

        if ep_path and ep_path != path and not ep.raw_args:
            # there was an endpoint corresponding to part, but not
            # the entire path, and it does not accept raw arguments
            return None, None, '', ''

        if handler is None:
            handler = httpreq.do_default
        return ep, handler, root, sub

class ParsedEndpoint(ObjectProxy):
    '''An instance of an Endpoint which has been parsed
    
    The following additional attributes are defined as given to the
    constructor:
        httpreq: the instance of BaseHTTPRequestHandler which it was
            parsed from
        handler: partial of the httpreq's method called 'do_{root}' or
            'do_default'; the first argument will be the ParsedEndpoint
        root: longest path of the endpoint corresponding to a defined handler
        sub: rest of the path of the endpoint
        args: everything following the endpoint's path (/root/sub/)
        argslen: number of path components in args
    '''

    def __init__(self, endpoint, httpreq, handler, root, sub, args, argslen):
        if not isinstance(endpoint, Endpoint):
            raise TypeError('ParsedEndpoint must be initialized from an Endpoint')

        super(ParsedEndpoint, self).__init__(endpoint.copy())
        self.httpreq = httpreq
        self.handler = partial(handler, self)
        self.root = root
        self.sub = sub
        self.args = args
        self.argslen = argslen

    def __repr__(self):
        # ObjectProxy's repr doesn't call wrapped's __repr__
        return self.__wrapped__.__repr__()