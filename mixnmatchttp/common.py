#  from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import dict
from builtins import filter
from builtins import str
from future import standard_library
standard_library.install_aliases()
import os.path
import re
from collections import UserDict
import logging

_logger = logging.getLogger(__name__)

class DictNoClobber(UserDict, object):
    # python2's UserDict.update does not call __setitem__,
    # __getitem__, etc; so override it here to explicitly access the
    # keys using the [] operator (as python3's UserDict.update does)
    def update(*args, **kwargs):
        if not args:
            raise TypeError("descriptor 'update' of 'UserDict' object "
                            "needs an argument")
        self = args[0]
        args = args[1:]
        if len(args) > 1:
            raise TypeError('expected at most 1 arguments, got %d' % len(args))
        if args:
            other = args[0]
        elif 'dict' in kwargs:
            other = kwargs.pop('dict')
            import warnings
            warnings.warn("Passing 'dict' as keyword argument is deprecated",
                          PendingDeprecationWarning, stacklevel=2)
        else:
            other = None
        if other is None:
            other = kwargs
        for k, v in other.items():
            self[k] = v

    def update_noclob(self, *args, **kwargs):
        '''Updates without overwriting existing keys'''

        d = dict(*args, **kwargs)
        self.update({k:v for k,v in d.items() if k not in self.keys()})

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
    '''Returns a dictionary of keys/values from the string s
    
    itemsep: regex for separating items
    valsep: literal string for separating key/value
    '''

    if s is None:
        return {}

    params = dict()
    sepfunc = lambda x: x.split(valsep)
    if values_are_opt:
        sepfunc = lambda x: x.partition(valsep)[0::2]

    try:
        params = dict([sepfunc(v) for v in re.split(itemsep, s)])
    except ValueError:
        pass

    _logger.debug('Got params from {}: {}'.format(s, params))
    return params
