import logging
import re
from wrapt import ObjectProxy

from ..utils import iter_abspath, DictNoClobber
from .exc import EndpointError, NotAnEndpointError, \
    MissingArgsError, ExtraArgsError, MethodNotAllowedError


ARGS_OPTIONAL = '?'  # 0 or 1
ARGS_ANY = '*'       # any number
ARGS_REQUIRED = '+'  # 1 or more


logger = logging.getLogger(__name__)


class Endpoint(DictNoClobber):
    '''Special endpoints

    The Endpoint constructor has the same signature as for
    a dictionary. For example you can define the endpoints like so:
        endpoints = endpoints.Endpoints(
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
        endpoints = endpoint.Endpoints({
            'some_sub': { ... },
            '$disabled': False,
            })
    or like so:
        endpoints = endpoint.Endpoints({
            '$disabled': False,
            },
            some_sub={ ... }
            )

    Endpoint names shouldn't have underscores, we don't handle them
    well, so expect unexpected behaviour. TODO maybe?
    Note also that endpoints are treated as case-insensitive, and the
    handler should assume the path is all lowercase, i.e. /FoO/BAR
    should be handled by do_{METHOD}_foo_bar

    An endpoint's name can be a '*', in which case it is treated as
    a variable. It will match anything and the actual match will be
    available in a dictionary passed to the endpoint handler, see
    documentation on Endpoint.parse. The dictionary key defaults to
    the parent's name, but can be overridden with the '$varname'
    attribute (useful for consecutive variable endpoints). For
    example:
        endpoints = endpoints.Endpoints(
                person={
                    '$allowed_methods': {'GET', 'POST'},
                    '*': {
                        '$varname': 'username',
                        }
                    },
                )
    will look for a method do_{METHOD}_person or do_person (a variable
    path component is discarded when selecting a handler name).
    The endpoint passed to the handler will have params['username']
    set to the match path component.

    Recognized attributes:
        disabled: <bool>, defaults to True for the root, False
                  otherwise
        allowed_methods: <set>, defaults to {'GET'}
        nargs: <number>|ARGS_*, defaults to 0
        raw_args: <bool>, defaults to False
        varname: <string>, only for wildcards, defaults to parent's
                 name
    Attempting to set another attribute (a key beginning with $) will
    result in AttributeError. If you want to add additional
    attributes, add them as keys to the instance's _defaultattrs
    dictionary (along with their default value).
    '''

    def __init__(self, *args, **kwargs):
        self._defaultattrs = {
            'name': None,  # for internal user
            'parent': None,  # for internal user
            'disabled': True,  # True for root only
            'allowed_methods': {'GET', 'HEAD'},
            'nargs': 0,
            'raw_args': False,
            'varname': '',
        }

        # Set the name of the endpoint before initializing, so that
        # its children have access to it
        setattr(self, 'name', kwargs.pop('$name', None))
        super().__init__(*args, **kwargs)
        logger.debug(
            'list of subpoints: {}'.format(list(self.keys())))

        if self.raw_args and \
                self.nargs not in [ARGS_ANY, ARGS_REQUIRED]:
            logger.warning(('Endpoint requires raw '
                            'arguments, but is sensitive to the '
                            'number of arguments; not reliable!'))
        if self.raw_args and self.keys():
            raise EndpointError('Endpoints expecting raw arguments '
                                'cannot have subpoints.')

    def __eq__(self, other):
        '''Compares endpoint to other taking into account attributes

        Attributes which have not been explicitly set are also
        compared.
        '''

        if not isinstance(other, Endpoint):
            return NotImplemented
        return (dict(self.items()) == dict(other.items()) and
                self.getattrs(with_defaults=True).items()
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
            logger.debug(('Endpoint special key {}, '
                          'setting as attribute').format(key))
            # raise an exception if attribute is unknown
            getattr(self, key[1:])
            setattr(self, key[1:], item)
        else:
            logger.debug('Creating endpoint {}'.format(key))
            if isinstance(item, Endpoint):
                super().__setitem__(key, item.copy())
            else:
                super().__setitem__(key, Endpoint(
                    item, **{'$name': key}))

            # Enable the endpoint, unless disabled is explicitly set
            self[key]._defaultattrs['disabled'] = False
            # Save the parent
            #  self[key]._defaultattrs['parent'] = self
            setattr(self[key], 'parent', self)
            # For variable endpoints, set the default varname to the
            # parent's name
            if key == '*':
                self[key]._defaultattrs['varname'] = \
                    self.getattr('name')  # will be None for root
                logger.debug('Endpoint {} is variable ({})'.format(
                    key, self.getattr('name')))
            logger.debug('Endpoint {} done'.format(key))

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
        '''Sets the given attribute if not already set

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
            self._DictNoClobber__update(
                __setdefaultitem, args[0].getattrs(as_keys=True))
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
            handler: the selected httpreq's method;
                the most specific handler for the endpoint's path and
                request method is used, or do_default if none found.
                E.g. for a GET to an endpoint /foo/bar/baz, first
                do_GET_foo_bar_baz is looked for, then do_foo_bar_baz,
                then do_GET_foo_bar, then do_foo_bar, then do_GET_foo,
                then do_foo, finally do_default
            root: longest path of the endpoint corresponding to
                a defined handler
            sub: rest of the path of the endpoint
            args: everything following the endpoint's path
                (/root/sub/)
            argslen: actual number of arguments it was called with
            params: a dictionary of all parameters for the full path;
                each key defaults to the parent's name
        For example if an endpoint /cache/new/static accepts
        arguments, and httpreq has a method do_cache, but not
        do_cache_new_static, and not do_cache_new, a request for
        /cache/new/static/page will set ep.root to 'cache', ep.sub to
        'new/static', ep.handler to httpreq.do_cache, ep.args to
        'page', and ep.argslen to 1.
        Or if /employee/*/dept/*/location is an endpoint and httpreq
        has a method do_employee_dept_location, then a request for
        /employee/jsmith/dept/it/location will set ep.root to
        /employee/dept/location, ep.sub to '', ep.args to
        '', ep.argslen to 0, ep.params['employee'] to 'jsmith', and
        ep.params['dept'] to 'it'

        If path does resolve to an enpoint's path but the
        request is not allowed for some reason, raises an exception:
            MethodNotAllowedError
            MissingArgsError
            ExtraArgsError
        If path doesn't resolve to an enpoint's path raises an
        exception:
            NotAnEndpointError
        '''

        path = httpreq.raw_pathname
        if not path or path[0] != '/':
            raise ValueError(
                'Path for endpoint parsing must begin with a /')
        if not path.startswith(httpreq.conf.endpoint_prefix):
            raise NotAnEndpointError(path)
        path = path[len(httpreq.conf.endpoint_prefix):]

        # we don't yet know if the endpoint wants the arguments raw or
        # canonicalized. So we check each absolute segment; if it's an
        # endpoint remember it, check next
        logger.debug('Checking if endpoint takes raw arguments')
        ep = None
        handler = httpreq.do_default
        root = sub = args = ''
        params = {}
        for curr_path, curr_args in iter_abspath(path):
            logger.debug(
                'Current abspath segment: {}'.format(curr_path))
            curr_ep, curr_handler, curr_root, \
                curr_sub, curr_params = \
                self._select_handler(curr_path, httpreq)

            if curr_ep is None:
                logger.debug('No match on this level')
                continue

            ep = curr_ep
            handler = curr_handler
            root = curr_root
            sub = curr_sub
            args = curr_args
            params = curr_params
            logger.debug(
                ('Match on this level: root: {}, sub: {}, '
                 'args: {}, params: {}').format(
                     root, sub, args, params))

            if ep.raw_args:
                logger.debug(
                    '{}({}) is "raw"; done'.format(root, sub))
                break  # don't inspect rest of path

        if ep is None or ep.disabled:
            if ep is not None:
                logger.debug('{} is disabled'.format(root))
            raise NotAnEndpointError(path)

        # either entire canonical path resolved to an endpoint, or
        # part of it resolved to an endpoint expecting raw arguments;
        # either way, we're done
        args_arr = list(filter(None, args.split('/')))

        ep = ParsedEndpoint(ep, httpreq, handler, root,
                            sub, args, len(args_arr), params)

        logger.debug(('API call: {}, root: {}, sub: {}, '
                      '{} args: {}, params: {}').format(
                          ep, ep.root, ep.sub,
                          ep.argslen, ep.args, ep.params))

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
        '''Generator for list(endpoints, curr_path) for each segment

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
                ep = ep[p.lower()]
            except KeyError:
                try:
                    ep = ep['*']
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

    def to_path(self):
        def _append_handler_name(ep, so_far=''):
            try:
                ep.parent
            except AttributeError:
                return so_far
            if ep.name == '*':
                this_name = ''
            else:
                this_name = '/' + ep.name
            return _append_handler_name(
                ep.parent, '{}{}'.format(this_name, so_far))

        return _append_handler_name(self)

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
                path matching the given path and method, e.g. if
                there's a handler do_a_b but not do_a_b_*, do_a_b will
                be selected for all endpoints starting with /a/b; if
                no matching handler is defined, do_default is returned
            root: the beginning of the path which matched a handler,
                e.g. /a/b if do_a_b is defined, or '' if no matching
                handler
            sub: the rest of the path after root/ (leading / is
                stripped)
            params: a dictionary of all parameters for the full path;
                each key defaults to the parent's name
        '''

        ep = handler = None
        ep_path = root = sub = ''
        params = {}
        logger.debug('Iterating over path {}'.format(path))
        for ep, ep_path in self.iter_path(path):
            logger.debug('{} is an endpoint'.format(ep_path))
            if ep.name == '*':
                params[ep.varname] = ep_path.split('/')[-1]
            try_path = ep.to_path().replace('/', '_')
            try:
                curr_handler = getattr(
                    httpreq, 'do_{}{}'.format(httpreq.command,
                                              try_path))
            except AttributeError:
                logger.debug(
                    'No {} handler for {}'.format(httpreq.command,
                                                  ep_path))
                try:
                    curr_handler = getattr(
                        httpreq, 'do{}'.format(try_path))
                except AttributeError:
                    logger.debug('No handler for {}'.format(ep_path))
                else:
                    logger.debug(
                        'Found handler for {}'.format(ep_path))
                    root = ep.to_path()
                    handler = curr_handler
            else:
                logger.debug('Found {} handler for {}'.format(
                    httpreq.command, ep_path))
                root = ep.to_path()
                handler = curr_handler

        # skip leading slash of sub
        if ep is not None:
            sub = ep.to_path()[len(root) + 1:]

        if ep_path and ep_path != path and not ep.raw_args:
            # there was an endpoint corresponding to part, but not
            # the entire path, and it does not accept raw arguments
            return None, None, '', '', {}

        if handler is None:
            handler = httpreq.do_default
        return ep, handler, root, sub, params

class ParsedEndpoint(ObjectProxy):
    '''An instance of an Endpoint which has been parsed

    The following additional attributes are defined as given to the
    constructor:
        httpreq: the instance of BaseHTTPRequestHandler which it was
            parsed from
        handler: the httpreq's method called 'do_{root}' or
            'do_default'
        root: longest path of the endpoint corresponding to a defined
            handler
        sub: rest of the path of the endpoint
        args: everything following the endpoint's path (/root/sub/)
        argslen: number of path components in args
        params: a dictionary of all parameters for the full path
    '''

    def __init__(self, endpoint, httpreq, handler, root, sub,
                 args, argslen, params):
        if not isinstance(endpoint, Endpoint):
            raise TypeError(
                'ParsedEndpoint must be initialized from an Endpoint')

        super(ParsedEndpoint, self).__init__(endpoint.copy())
        self.httpreq = httpreq
        self.handler = handler
        self.root = root
        self.sub = sub
        self.args = args
        self.argslen = argslen
        self.params = params

    def __repr__(self):
        # ObjectProxy's repr doesn't call wrapped's __repr__
        return self.__wrapped__.__repr__()
