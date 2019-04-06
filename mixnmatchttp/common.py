#  from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import *
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

def iter_abspath_up_to_nth(path, n=1, join=False):
    '''Canonicalize the path up to the first n segments
    
    Leading slash is preserved if present, but is not required.
    Returns a generator for a list of canonicalized versions of path
    up to the first n segments, followed by the rest of the segments.
    For example /../foo/../bar/./baz/./ will result in
    [('/foo', '../bar/./baz/./'), ('/bar', './baz/./'), ('/bar', 'baz/./')]
    for n=1, and [('/bar/baz', './'), ('/bar/baz', '')] for n=2. If we
    never reach n segments, nothing is yielded.
    
    If join is True, the canonicalized part (with n segments) and the
    rest is joined. This will result in ['/bar/baz/./', '/bar/baz']
    for n=2.
    '''

    if not path:
        return

    if n <= 0:
        raise ValueError('Number of path segments must be positive')

    # temporarily add a trailing /
    pathlen = len(path)
    if path[-1] != '/':
        path += '/'

    curr_index = skip = path.find('/')
    root = path[: skip if skip != -1 else None]
    while skip != -1:
        curr_abs = abspath(path[:curr_index])
        curr_abs_parts = list(filter(None, curr_abs.split('/')))
        # filter because leading or trailing / will result in ''
        # items
        if len(curr_abs_parts) == n:
            if join:
                yield '/'.join(filter(None, [curr_abs,
                    path[curr_index+1:pathlen]]))
            else:
                yield curr_abs, path[curr_index+1:pathlen]
        skip = path[curr_index+1:].find('/')
        curr_index += skip + 1

def iter_abspath(path, start_n=1, join=False):
    '''Canonicalize the path segment by segment
    
    Returns a generator for a list of iter_abspath_up_to_nth results
    for all n's starting at start_n.
    '''

    while True:
        done = True
        for result in iter_abspath_up_to_nth(path, start_n):
            done = False
            yield result
        if done:
            return
        start_n += 1

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
