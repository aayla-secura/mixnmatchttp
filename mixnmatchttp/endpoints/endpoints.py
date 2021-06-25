import logging
import re
from copy import copy
from wrapt import ObjectProxy
from bidict import bidict

from ..utils import iter_abspath, to_natint
from ..conf.containers import DefaultDict, DefaultAttrs, DefaultAttrDict
from .exc import EndpointError, NotAnEndpointError, \
    MissingArgsError, ExtraArgsError, MethodNotAllowedError


logger = logging.getLogger(__name__)
__all__ = [
    'ARGS_OPTIONAL',
    'ARGS_ANY',
    'ARGS_REQUIRED',
    'Endpoint',
    'ParsedEndpoint',
]


class EndpointArgs:
    _special = bidict(
        optional='?',  # 0 or 1
        any='*',       # any number
        required='+'  # 1 or more
    )

    def __init__(self, num):
        try:
            self.value = to_natint(num)
        except ValueError:
            if num in self._special:
                self.value = num
            elif num in self._special.inverse:
                self.value = self._special.inverse[num]
            else:
                raise ValueError(
                    ('{} is not a valid self.valueber of '
                     'endpoint numuments').format(num))

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.value)

    def __str__(self):
        return str(self.value)

    def parse(self, num):
        pass  # TODO

class EndpointSettings(DefaultAttrs):
    def __init__(self):
        super().__init__(dict(
            name='',
            disabled=True,  # False for children
            nargs=0,        # ARGS_ANY if raw_args is True
            allowed_methods={'GET', 'HEAD'},
            raw_args=False,
            varname='',
        ))

    def __update_single__(self, name, value, is_explicit):
        if name == 'allowed_methods' and 'GET' in value:
            # it doesn't make sense to allow GET but not HEAD
            value |= {'HEAD'}
        if name == 'raw_args' and value is True:
            # update default nargs
            self.__update_single__('nargs', ARGS_ANY, False)
        if name == 'name':
            # it must be a child, update default disabled
            self.__update_single__('disabled', False, False)

        super().__update_single__(name, value, is_explicit)


class Endpoint(DefaultDict):
    '''API endpoints

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
    Any dictionary keys starting with $ correspond to an attribute
    (without the $). All other keys become subpoints of the parent;
    their value should be either another Endpoint (in which case it is
    copied), or a plain dictionary to be converted to an Endpoint.

    Recognized attributes for endpoints (keys starting with $):
        disabled:        <bool>; whether the endpoint can be called;
                         defaults to True for the root, False
                         otherwise
        allowed_methods: <set>; which HTTP methods are allowed;
                         defaults to {'GET'}
        nargs:           <number>|ARGS_*; how many arguments are
                         accepted after the full enpoint path;
                         defaults to 0 if raw_args is False, otherwise
                         to ARGS_ANY;
                         special non-numerical values:
                           ARGS_OPTIONAL is 0 or 1
                           ARGS_ANY      is any number
                           ARGS_REQUIRED is 1 or more
        raw_args:        <bool>; whether to skip canonicalizing the
                           arguments; defaults to False, e.g.
                           foo/../bar -> bar
        varname:         <string>; the name the variable component
                         is to be saved as; only for wildcards;
                         defaults to parent's name

    All child endpoints are enabled by default. The root endpoint is
    disabled by default; if you want it enabled, either manually
    change the 'disabled' attribute, or construct it like so:
        endpoints = endpoint.Endpoints({
            'some_sub': { ... },
            '$disabled': False,
            })
    or like so:
        endpoints = endpoint.Endpoints(
            some_sub={ ... },
            **{'$disabled': False}
            )

    When an endpoint is parsed for a given request, the child endpoint
    (or the root itself) with the most specific match is selected and
    a request handler (a method of a BaseHTTPRequestHandler instance)
    is selected based on the selected endpoint's path. See
    documentation on Endpoint.parse. Because / are replaced by _ when
    looking for a handler, Endpoint names shouldn't have underscores.
    TODO fix.

    An endpoint's name can be a '*', in which case it is treated as
    variable. It will match anything and the actual match will be
    available in a dictionary attribute of the parsed endpoint (which
    is passed to the endpoint handler); see the documentation on
    Endpoint.parse. The dictionary key defaults to the parent's name,
    but can be overridden with the '$varname' attribute (useful for
    consecutive variable endpoints). For example:
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
    The endpoint passed to the handler will have
    <endpoint>.params['username'] set to the matched path component,
    e.g. john if /person/john has been requested.

    The Endpoint class attribite, case_sensitive, dictates whether
    path and handler name matching is case-sensitive. Note that
    variable components are still saved as given, i.e. a request to
    /user/John for a variable endpoint /user/* would still get "John"
    and not "john" in its parameters regardless if it's case-sensitive
    or not; default is the corresponding class attribute (False for
    Endpoint)
    '''

    case_sensitive = False

    def __init__(self, arg=None, /, **kargs):
        '''Keyword arguments take precedence'''

        if arg and kargs:
            init = arg.copy()
            init.update(kargs)
        else:
            init = arg or kargs

        self._id = '{:x}'.format(id(self))
        self._settings = EndpointSettings()

        super().__init__()

        if '$name' in init:
            # Set the name of the endpoint before initializing, so
            # that its children have access to it
            #  self.__update_single__('$name', init.pop('$name'), True)
            self._settings.name = init.pop('$name')

        self.parent = None
        super().__update__(**init)

        logger.debug(
            'Endpoint {id} ({name}): list of subpoints {sub}'.format(
                id=self._id,
                name=self.name,
                sub=self.children))

        if self.raw_args and \
                self.nargs not in [ARGS_ANY, ARGS_REQUIRED]:
            logger.warning(('Endpoint {} requires raw '
                            'arguments, but is sensitive to the '
                            'number of arguments; not '
                            'reliable!').format(self.name))
        if self.raw_args and self.children:
            raise EndpointError('Endpoints expecting raw arguments '
                                'cannot have subpoints.')

    @property
    def children(self):
        return list(self.keys())

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
            args: array of everything following the endpoint's path
                (/root/sub/) split on /
            params: a dictionary of all parameters for the full path;
                each key defaults to the parent's name

        For example if an endpoint /cache/new/static accepts
        arguments, and httpreq has a method do_cache, but not
        do_cache_new_static, and not do_cache_new, a request for
        /cache/new/static/page will result in a ParsedEndpoint ep with
        ep.root set to 'cache', ep.sub to 'new/static', ep.handler
        to httpreq.do_cache, ep.args to ['page'].
        Or if /employee/*/dept/*/location is an endpoint and httpreq
        has a method do_employee_dept_location, then a request for
        /employee/jsmith/dept/it/location will set ep.root to
        /employee/dept/location, ep.sub to '', ep.args to
        [], ep.params['employee'] to 'jsmith', and
        ep.params['dept'] to 'it'

        If path does resolve to an enpoint's path but the
        request is not allowed for some reason, raises an exception:
            MethodNotAllowedError: HTTP method not allowed
            MissingArgsError:      < the minimum # of arguments given
            ExtraArgsError:        > the maximum # of arguments given
        If path doesn't resolve to an enpoint's path raises an
        exception:
            NotAnEndpointError
        '''

        path = httpreq.raw_pathname
        if not path or path[0] != '/':
            raise ValueError(
                'Path for endpoint parsing must begin with a /')
        if httpreq.conf.api_prefix and \
                not path.startswith(httpreq.conf.api_prefix):
            raise NotAnEndpointError(path)
        path = path[len(httpreq.conf.api_prefix):]

        # we don't yet know if the endpoint wants the arguments raw or
        # canonicalized. So we check each absolute segment; if it's an
        # endpoint remember it, check next
        logger.debug('Checking if endpoint takes raw arguments')

        # defaults
        ep = self  # if path is / the for loop won't run
        handler = httpreq.do_default
        sub = args = ''
        root = '/'
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
                    ("root = {}, sub = {} takes raw arguments; "
                     "we're done").format(
                         root, sub))
                break  # don't inspect rest of path

        if ep is None or ep.disabled:
            if ep is not None:
                logger.debug('{} is disabled'.format(root))
            raise NotAnEndpointError(path)

        # at this point either entire canonical path resolved to an
        # endpoint, or part of it resolved to an endpoint expecting
        # raw arguments; either way, we have a match

        if ep.raw_args:
            # keep double slashes
            args_arr = args.split('/')
        else:
            # ignore double slashes
            args_arr = list(filter(None, args.split('/')))

        nargs = len(args_arr)
        if ep.nargs == ARGS_ANY:
            pass
        elif ep.nargs == ARGS_REQUIRED:
            if not args_arr:
                raise MissingArgsError
        elif ep.nargs == ARGS_OPTIONAL:
            if nargs > 1:
                raise ExtraArgsError(nargs - 1, args)
        elif nargs > ep.nargs:
            raise ExtraArgsError(nargs - ep.nargs, args)
        elif nargs < ep.nargs:
            raise MissingArgsError(ep.nargs - nargs)

        if httpreq.command not in ep.allowed_methods:
            raise MethodNotAllowedError(ep.allowed_methods)

        logger.debug(('API call: "{}", root: {}, sub: {}, '
                      '{} args: {}, params: {}').format(
                          ep.name, root, sub,
                          len(args_arr), args, params))
        return ParsedEndpoint(ep,
                              httpreq=httpreq,
                              handler=handler,
                              root=root,
                              sub=sub,
                              args=args_arr,
                              params=params)

    def iter_path(self, path):
        '''Generator for list(endpoints, curr_path) for each segment

        path must be canonical (no double //, no ./ or ../).
        '''

        logger.debug('Getting endpoints from path {}'.format(path))
        ep = self
        curr_path = ''
        pref = ''
        suf = ''

        if path[0] == '/':
            pref = '/'
            path = path[1:]
        if path[-1] == '/':
            suf = '/'
            path = path[:-1]

        for p in path.split('/'):
            curr_path += '/' + p
            logger.debug(
                'Current list of subpoints: {}; trying {}'.format(
                    ep.children, p))
            try:
                ep = ep[p]
            except KeyError:
                try:
                    ep = ep['*']
                except KeyError:
                    return
            yield ep, pref + curr_path[1:] + suf

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
            if ep.parent is None:
                # reached the top
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
                e.g. /a/b if do_a_b is defined, or / if no matching
                handler
            sub: the rest of the path after root/ (leading / is
                stripped)
            params: a dictionary of all parameters for the full path;
                each key defaults to the parent's name
        '''

        ep = handler = ep_path = None
        root = '/'
        sub = ''
        params = {}
        logger.debug('Iterating over path {}'.format(path))
        for ep, ep_path in self.iter_path(path):
            logger.debug('{} is an endpoint'.format(ep_path))
            if ep.name == '*':
                params[ep.varname] = ep_path.split('/')[-1]

            # ep_path contains parameters for variable name ep's
            # ep.to_path() doesn't
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
                    logger.debug('No handler do{} for {}'.format(
                        try_path, ep_path))
                else:
                    logger.debug(
                        'Found generic handler do{} for {}'.format(
                            try_path, ep_path))
                    root = ep.to_path()
                    handler = curr_handler
            else:
                logger.debug('Found {} handler do{} for {}'.format(
                    httpreq.command, try_path, ep_path))
                root = ep.to_path()
                handler = curr_handler

        if ep is not None:
            sub = ep.to_path()[len(root):]
            assert root == '/' or sub == '' or sub[0] == '/'
            if sub[:1] == '/':
                # skip leading slash of sub
                sub = sub[1:]

        if ep_path and ep_path != path and not ep.raw_args:
            # there was an endpoint corresponding to part, but not
            # the entire path, and it does not accept raw arguments
            return None, None, '', '', {}

        if handler is None:
            handler = httpreq.do_default
        return ep, handler, root, sub, params

    def __getattr__(self, name):
        return getattr(self._settings, name)

    def __getitem__(self, name):
        if not self.case_sensitive:
            name = name.lower()
        return super().__getitem__(name)

    def __contains__(self, name):
        if not self.case_sensitive:
            name = name.lower()
        return super().__contains__(name)

    def __update_single__(self, key, item, is_explicit):
        if not key:
            raise ValueError('Endpoint name must be non-empty')

        if key[0] == '$':
            logger.debug(
                'Endpoint {id} ({name}): {key} = {val}{comment}'.format(
                    id=self._id,
                    name=self.name,
                    key=key[1:],
                    val=item,
                    comment="" if is_explicit else " (default)"))
            self._settings.__update_single__(
                key[1:], item, is_explicit)
            return

        logger.debug(
            'Endpoint {id} ({name}): creating child "{child}"'.format(
                id=self._id,
                name=self.name,
                child=key))
        if isinstance(item, Endpoint):
            item = copy(item)
            item._settings.name = key
        else:
            item = self.__class__(item, **{'$name': key})

        item.parent = self
        # For variable endpoints, set the default varname to the
        # parent's name
        if key == '*':
            item.__update_single__('$varname', self.name, False)
        logger.debug('Endpoint {id} ({name}) done'.format(
            id=item._id, name=key))

        if not item.case_sensitive:
            key = key.lower()
        super().__update_single__(key, item, is_explicit)

    def __copy__(self):
        clone = super().__copy__()
        clone._id = '{:x}'.format(id(clone))
        clone._settings = self._settings.__copy__()
        clone.parent = self.parent
        return clone

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
        args: array of everything following the endpoint's path
            (/root/sub/) split on /
        params: a dictionary of all parameters for the full path
    '''

    def __init__(self, endpoint, httpreq, handler, root, sub,
                 args, params):
        if not isinstance(endpoint, Endpoint):
            raise TypeError(
                'ParsedEndpoint must be initialized from an Endpoint')

        super().__init__(endpoint.copy())
        self.httpreq = httpreq
        self.handler = handler
        self.root = root
        self.sub = sub
        self.args = args
        self.params = params

    def __repr__(self):
        return self.__wrapped__.__repr__()


ARGS_OPTIONAL = '?'
ARGS_ANY = '*'
ARGS_REQUIRED = '+'
# TODO
#  ARGS_OPTIONAL = EndpointArgs('?')
#  ARGS_ANY = EndpointArgs('*')
#  ARGS_REQUIRED = EndpointArgs('+')
