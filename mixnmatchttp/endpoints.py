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

from .common import abspath, abspath_up_to_nth, DictNoClobber

ARGS_OPTIONAL = '?' # 0 or 1
ARGS_ANY = '*'      # any number
ARGS_REQUIRED = '+' # 1 or more

_logger = logging.getLogger(__name__)

######################### EXCEPTIONS ########################

class EndpointError(Exception):
    '''Base class for exceptions related to the special endpoints'''
    pass

class NotAnEndpointError(EndpointError):
    '''Exception raised when the root path is unknown'''

    def __init__(self, root):
        super(NotAnEndpointError, self).__init__('{} is not special.'.format(root))

class MethodNotAllowedError(EndpointError):
    '''Exception raised when the request method is not allowed'''

    def __init__(self):
        super(MethodNotAllowedError, self).__init__('Method not allowed.')

class MissingArgsError(EndpointError):
    '''Exception raised when a required argument is not given'''

    def __init__(self):
        super(MissingArgsError, self).__init__('Missing required argument.')

class ExtraArgsError(EndpointError):
    '''Exception raised when extra arguments are given'''

    def __init__(self, args):
        super(ExtraArgsError, self).__init__('Extra arguments: {}.'.format(args))

############################################################

class Subpoint(DictNoClobber):
    _default = {
            'allowed_methods': {'GET'},
            'args': 0,
            'raw_args': False,
            }

    def __init__(self, *args, **kwargs):
        super(Subpoint, self).__init__(self._default)
        _logger.debug('Setting defaults for subpoint, then {}, {}'.format(args, kwargs))
        self.update(*args, **kwargs)

    def __setitem__(self, key, item):
        if key == 'allowed_methods':
            item |= {'HEAD', 'OPTIONS'}
        super(Subpoint, self).__setitem__(key, item)

class Endpoint(DictNoClobber):
    def __init__(self, *args, **kwargs):
        super(Endpoint, self).__init__(*args, **kwargs)
        _logger.debug('Setting default subpoint')
        self.setdefault('', Subpoint())
        _logger.debug('List of subpoints: {}'.format(list(self.keys())))

    def __setitem__(self, key, item):
        super(Endpoint, self).__setitem__(key, Subpoint(item))

    def has(self, sub=''):
        try:
            self[sub]
        except KeyError:
            return False

        return True

class Endpoints(DictNoClobber):
    '''Special endpoints
    
    Format for endpoints:
    '<root>': {
            '<subpoint>': {
                'allowed_methods': {'<method1>', ...}, # GET, POST, etc
                'args': <number>|ARGS_*, # how many args,
                                         # only reliable if
                                         # raw_args is False
                'raw_args': True|False,  # should we avoid
                                         # canonicalizing args
                }
            }
    
    'allowed_methods: <set>, defaults to {'GET'}
    'args': <number>|ARGS_*, defaults to 0
    'raw_args': <bool>, defaults to False
    '''

    def __setitem__(self, key, item):
        _logger.debug('Creating endpoint {}'.format(key))
        super(Endpoints, self).__setitem__(key, Endpoint(item))

    def has(self, root, sub=''):
        _logger.debug('Checking if {}[{}] exists'.format(root, sub))
        _logger.debug('List of roots: {}'.format(list(self.keys())))
        try:
            _logger.debug('List of {} keys: {}'.format(root, list(self[root].keys())))
        except KeyError:
            pass
        try:
            self[root][sub]
        except KeyError:
            return False

        return True

    def parse(self, path, command):
        '''Selects an endpoint for the path
        
        Returns (root, sub, args) if an endpoint, or raises an
        exception:
            NotAnEndpointError
            MethodNotAllowedError
            MissingArgsError
            ExtraArgsError
        '''

        if not path or path[0] != '/':
            raise ValueError('Path for endpoint parsing must begin with a /')

        # we don't yet know if the endpoints or subpoint wants the
        # arguments raw or canonicalized. So we check the first
        # absolute segment
        # if it's an endpoint which expects raw arguments, we're done
        root, sub, args = self._parse_raw(abspath_up_to_nth(path, 1))
        if not root:
            # otherwise check for the second abs segment
            _logger.debug('Checking if subpoint takes raw args')
            root, sub, args = self._parse_raw(abspath_up_to_nth(path, 2))

        if root:
            _logger.debug(('Parsed endpoint with raw args: root: {}, ' +
                'sub: {}, args: {}').format(root, sub, args))
            if self[root][sub]['args'] not in \
                [ARGS_ANY, ARGS_REQUIRED]:
                _logger.warning(('Endpoint {} requires non-canonical ' +
                    'arguments, but is sensitive to the number ' +
                    'of arguments; not reliable!').format(root))
        else:
            # finally canonicalize the whole path and take the root
            # endpoint and subpoint from there
            root, sub, args = _unpacker(
                    *abspath(path).lstrip('/').split('/', 2))
            _logger.debug(('Parsed endpoint: root: {}, sub: {}, args: {}'
                ).format(root, sub, args))

        if not self.has(root, sub):
            args = '/'.join(filter(None, [sub, args])) # consume the sub into args
            sub = ''

        if not self.has(root):
            raise NotAnEndpointError(root)

        _logger.debug(
                'API call: root: {}, sub: {}, args: {}'.format(
                    root, sub, args))

        args_arr = list(filter(None, args.split('/')))
        endpoint = self[root]
        if endpoint[sub]['args'] == ARGS_ANY:
            pass
        elif endpoint[sub]['args'] == ARGS_REQUIRED:
            if not args:
                raise MissingArgsError
        elif endpoint[sub]['args'] == ARGS_OPTIONAL:
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
        root, sub, args = _unpacker(*path.lstrip('/').split('/', 2))
        if self.has(root, sub) and \
                self[root][sub]['raw_args']:
            return root, sub, args

        return '', '', ''

def _unpacker(root, sub='',args=''):
    # handle case of not enough / in path during splitting
    return root, sub, args
