import logging
import os


logger = logging.getLogger(__name__)
__all__ = [
    'abspath',
    'iter_abspath_up_to_nth',
    'iter_abspath',
]


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
        '//', '/')[len(prefix):]

def iter_abspath_up_to_nth(path, n=1, join=False):
    '''Canonicalize the path up to the first n segments

    Leading slash is preserved if present, but is not required.
    Returns a generator for a list of canonicalized versions of path
    up to the first n segments, followed by the rest of the segments.
    For example /../foo/../bar/./baz/./ will result in
    [('/foo', '../bar/./baz/./'), ('/bar', './baz/./'),
     ('/bar', 'baz/./')]
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
                yield '/'.join(filter(
                    None, [curr_abs, path[curr_index + 1:pathlen]]))
            else:
                yield curr_abs, path[curr_index + 1:pathlen]
        skip = path[curr_index + 1:].find('/')
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
