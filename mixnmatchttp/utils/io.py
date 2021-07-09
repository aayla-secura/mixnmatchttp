import logging
import os
from contextlib import contextmanager

from .time import to_timestamp


logger = logging.getLogger(__name__)
__all__ = [
    'open_path',
    'read_file',
    'is_modified_since',
]


@contextmanager
def open_path(path, mode='r'):
    if hasattr(path, 'read'):
        filename = getattr(path, 'name', None)
        fd = path
        needs_closing = False
        logger.debug('Using open file {}'.format(filename))
    else:
        filename = path
        fd = open(path, mode)
        needs_closing = True
        logger.debug('Opened file {}'.format(filename))
    try:
        yield fd, filename
    finally:
        if needs_closing:
            fd.close()
            logger.debug('Closed file {}'.format(filename))

def read_file(path, mode='r'):
    with open_path(path, mode=mode) as (fd, filename):
        logger.debug('Reading file {}'.format(filename))
        return fd.read()

def is_modified_since(path, last_time):
    '''True if path's been modified since last_time

    last_time can be a string, integer, float or datetime; see
    to_datetime
    '''

    if hasattr(path, 'read'):
        fs = os.fstat(path)
    else:
        fs = os.stat(path)

    return int(fs.st_mtime) > int(to_timestamp(last_time))
