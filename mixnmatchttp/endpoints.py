#  from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import *
from future import standard_library
standard_library.install_aliases()
import logging
from functools import partial
from wrapt import ObjectProxy

from .common import iter_abspath, DictNoClobber

ARGS_OPTIONAL = '?' # 0 or 1
ARGS_ANY = '*'      # any number
ARGS_REQUIRED = '+' # 1 or more

__all__ = [
        'ARGS_OPTIONAL',
        'ARGS_ANY',
        'ARGS_REQUIRED',
        'EndpointError',
        'EndpointParseError',
        'NotAnEndpointError',
        'MethodNotAllowedError',
        'MissingArgsError',
        'ExtraArgsError',
        'Endpoint',
        'ParsedEndpoint',
        ]

logger = logging.getLogger(__name__)

######################### EXCEPTIONS ########################

class EndpointError(Exception):
    '''Base class for exceptions related creation of endpoints'''

    pass

class EndpointParseError(Exception):
    '''Base class for exceptions related parsing of endpoints'''

    pass

class NotAnEndpointError(EndpointParseError):
    '''Exception raised when the root path is unknown'''

    def __init__(self, root):
        super().__init__('{} is not special.'.format(root))

class MethodNotAllowedError(EndpointParseError):
    '''Exception raised when the request method is not allowed
    
    Will have an "allowed_methods" attribute containing a set of
    allowed HTTP methods for this endpoint.
    '''

    def __init__(self, allowed_methods):
        self.allowed_methods = allowed_methods
        super().__init__('Method not allowed.')

class MissingArgsError(EndpointParseError):
    '''Exception raised when a required argument is not given'''

    def __init__(self):
        super().__init__('Missing required argument.')

class ExtraArgsError(EndpointParseError):
    '''Exception raised when extra arguments are given'''

    def __init__(self, nargs):
        super().__init__('Extra arguments: {}.'.format(nargs))

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
    Attempting to set another attribute (a key beginning with $) will
    result in AttributeError. If you want to add additional
    attributes, add them as keys to the instance's _defaultattrs
    dictionary (along with their default value).
    '''

    def __init__(self, *args, **kwargs):
        self._defaultattrs = {
                'disabled': True,
                'allowed_methods': {'GET', 'HEAD'},
                'nargs': 0,
                'raw_args': False,
                }

        super().__init__(*args, **kwargs)
        logger.debug('list of subpoints: {}'.format(list(self.keys())))

        if self.raw_args and self.nargs not in [ARGS_ANY, ARGS_REQUIRED]:
            logger.warning(('Endpoint requires raw ' +
                'arguments, but is sensitive to the number ' +
                'of arguments; not reliable!'))
        if self.raw_args and self.keys():
            raise EndpointError(
                    "Endpoints expecting raw arguments cannot have subpoints.")

    def __eq__(self, other):
        '''Compares endpoint to other taking into account attributes
        
        Attributes which have not been explicitly set are also
        compared.
        '''

        if not isinstance(other, Endpoint):
            return NotImplemented
        return (dict(self.items()) == dict(other.items()) and \
                self.getattrs(with_defaults=True).items() \
                == other.getattrs(with_defaults=True).items())
    def __ne__(self, other):
        return not self.__eq__(other)

    def __setattr__(self, attr, value):
        if attr == 'allowed_methods' and 'GET' in value:
            value |= {'HEAD'}
        super().__setattr__(attr, value)

    def __setitem__(self, key, item):
        if not key:
            raise ValueError('Endpoint must be non-empty')

        if key[0] == '$':
            logger.debug(
                    'Endpoint special key {}, setting as attribute'.format(key))
            getattr(self, key[1:]) # raise an exception if
                                   # attribute is unknown
            setattr(self, key[1:], item)
        else:
            logger.debug('Creating endpoint {}'.format(key))
            if isinstance(item, Endpoint):
                super().__setitem__(key, item.copy())
            else:
                super().__setitem__(key, Endpoint(item))

            # Enable the endpoint, unless disabled is explicitly set
            self[key]._defaultattrs['disabled'] = False

    def __getattr__(self, attr):
        return self._getattr(attr, None, True)

    def _getattr(self, attr, default=None, raise_None=False):
        '''Returns the given attribute, or the default value
        
        If default is None, it is taked from the endpoint's defaults
        (_defaultattrs). If it is not found there then AttributeError
        is raised if raise_None is True, otherwise None is returned.
        '''

        try:
            return self.__getattribute__(attr)
        except AttributeError as e:
            if attr == '_defaultattrs':
                # not initialized yet
                raise e

            if default is None:
                try:
                    default = self._defaultattrs[attr]
                except KeyError:
                    pass
            if default is not None or not raise_None:
                return default
            raise e

    def getattr(self, attr, default=None):
        '''Returns the given attribute, or the default value
        
        If default is None, it is taked from the endpoint's defaults
        (_defaultattrs).
        '''

        return self._getattr(attr, default, False)

    def getattrs(self, with_defaults=False, as_keys=False):
        '''Returns a dictionary with all endpoint attributes.
        
        By default only the attributes which have been explicitly set
        are returned. If with_defaults is True, then all attributes
        are returned.
        '''

        pref = ''
        if as_keys:
            pref = '$'
        attrs = {}
        for attr in self._defaultattrs:
            try:
                if not with_defaults:
                    value = self.__getattribute__(attr)
                else:
                    value = self.getattr(attr)
            except AttributeError:
                pass
            else:
                attrs[pref + attr] = value
        return attrs

    def setdefaultattr(self, attr, default=None):
        '''Sets the given attribute if not already set to the default value
        
        If default is None, it is taked from the endpoint's defaults
        (_defaultattrs).
        '''

        try:
            self.__getattribute__(attr)
        except AttributeError:
            logger.debug('Setting {} to default ({})'.format(
                attr, default))
            if default is None:
                try:
                    default = self._defaultattrs[attr]
                except KeyError:
                    pass
            setattr(self, attr, default)

    def setdefaultattrs(self, defaults=None):
        '''Sets the given default value for each attribute in defaults
        
        If defaults is None self._defaultattrs is used.
        '''

        if defaults is None:
            defaults = self._defaultattrs
        for attr, value in defaults.items():
            self.setdefaultattr(attr, value)

    def update(self, *args, **kwargs):
        '''Updates using items in the first argument, then keywords
        
        Special keywords (starting with $) are recognized as usual.
        '''

        super().update(*args, **kwargs)
        if not args or not isinstance(args[0], Endpoint):
            return

        # Was passed an Endpoint, update with its attributes
        for attr, value in args[0].getattrs().items():
            setattr(self, attr, value)

    def update_noclob(self, *args, **kwargs):
        '''Updates without overwriting existing keys or attributes
        
        Special keywords (starting with $) are recognized as usual. If
        the corresponding attribute has not been explicitly, it is
        overriden.
        '''

        def __setdefaultitem(key, value):
            if key[0] == '$':
                logger.debug(
                        'Updating without clobbering: attr {}={}'.format(
                            key[1:], value))
                self.setdefaultattr(key[1:], value)
            else:
                logger.debug(
                        'Updating without clobbering: key {}={}'.format(
                            key, value))
                self.setdefault(key, value)

        if args and isinstance(args[0], Endpoint):
            self._DictNoClobber__update(__setdefaultitem,
                    args[0].getattrs(as_keys=True))
        self._DictNoClobber__update(__setdefaultitem, *args, **kwargs)

    def clear(self):
        '''Clears child endpoints and all attributes'''

        super().clear()
        for attr in self.getattrs():
            self.__delattr__(attr)

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
        
        If path does resolve to an enpoint's path but the
        request is not allowed for some reason, raises an exception:
            MethodNotAllowedError
            MissingArgsError
            ExtraArgsError
        If path doesn't resolve to an enpoint's path raises an exception:
            NotAnEndpointError
        '''

        path = httpreq.raw_pathname
        if not path or path[0] != '/':
            raise ValueError('Path for endpoint parsing must begin with a /')

        # we don't yet know if the endpoint wants the arguments raw or
        # canonicalized. So we check each absolute segment; if it's an
        # endpoint remember it, check next
        logger.debug('Checking if endpoint takes raw arguments')
        ep = None
        handler = httpreq.do_default
        root = sub = args = ''
        for curr_path, curr_args in iter_abspath(path):
            logger.debug('Current abspath segment: {}'.format(curr_path))
            curr_ep, curr_handler, curr_root, curr_sub = \
                    self._select_handler(curr_path, httpreq)

            if curr_ep is None:
                logger.debug('No match on this level')
                continue

            ep = curr_ep
            handler = curr_handler
            root = curr_root
            sub = curr_sub
            args = curr_args
            logger.debug(
                    'Match on this level: root: {}, sub: {}, args: {}'.format(
                        root, sub, args))

            if ep.raw_args:
                logger.debug('{}({}) is "raw"; done'.format(root, sub))
                break # don't inspect rest of path

        if ep is None or ep.disabled:
            if ep is not None:
                logger.debug('{} is disabled'.format(root))
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

        logger.debug(
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
            raise MethodNotAllowedError(ep.allowed_methods)

        return ep

    def iter_path(self, path):
        '''Returns a generator for list(endpoints, curr_path) for each path segment
        
        path must be canonical (no double //, no ./ or ../).
        '''

        logger.debug('Getting endpoints from path {}'.format(path))
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
            logger.debug(
                    'Current list of subpoints: {}; trying {}'.format(
                        list(ep.keys()), p))
            try:
                ep = ep[p]
            except KeyError:
                return
            yield ep, pref + curr_path[1:] + suf

        logger.debug('Final: {}'.format(pref + curr_path[1:] + suf))

    def get_from_path(self, path, httpreq=None):
        '''Returns an endpoint with the given path or None
        
        path must be canonical (no double //, no ./ or ../).
        '''

        for ep, ep_path in self.iter_path(path):
            logger.debug('{} is an endpoint'.format(ep_path))
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
        logger.debug('Iterating over path {}'.format(path))
        for ep, ep_path in self.iter_path(path):
            logger.debug('{} is an endpoint'.format(ep_path))
            try:
                curr_handler = getattr(
                        httpreq, 'do' + ep_path.replace('/', '_'))
            except AttributeError:
                logger.debug('No handler for {}'.format(ep_path))
            else:
                logger.debug('Found handler for {}'.format(ep_path))
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
