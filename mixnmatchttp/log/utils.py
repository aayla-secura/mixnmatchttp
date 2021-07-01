import logging
import sys
from functools import partial

try:
    from colorlog import ColoredFormatter
except ImportError:
    pass

from .handlers import CritFileHandler, CritStreamHandler, \
    ErrorFileHandler, ErrorStreamHandler, WarnFileHandler, \
    WarnStreamHandler, InfoFileHandler, InfoStreamHandler, \
    DebugFileHandler, DebugStreamHandler, RequestDebugFileHandler, \
    RequestDebugStreamHandler


class LogDestStorage:
    def __init__(self):
        self._seen = {None: set()}

    def add(self, pkg, level, dest):
        seen = self._get_seen(pkg)
        seen.add((level, dest))

    def _get_seen(self, pkg):
        seen = self._seen
        for p in pkg.split('.'):
            seen.setdefault(p, {None: set()})
            seen = seen[p]
        return seen[None]

    def contains(self, pkg, level, dest):
        curr_pkg = pkg
        while True:
            seen = self._get_seen(curr_pkg)
            if (level, dest) in seen:
                return True
            curr_pkg = '.'.join(curr_pkg.split('.')[:-1])
            if not curr_pkg:
                return False


def get_formatter(level, fmt, datefmt, color):
    if color:
        try:
            ColoredFormatter
        except NameError:
            raise ModuleNotFoundError(
                'colorlog is required if using colors')

        return ColoredFormatter(
            fmt='%(log_color)s' + fmt,
            datefmt=datefmt,
            reset=True,
            log_colors={
                'DEBUG': 'blue',
                'INFO': 'bold',
                'WARNING': 'purple',
                'ERROR': 'bold,red',
                'CRITICAL': 'bold,fg_white,bg_red',
            }
        )
    else:
        return logging.Formatter(fmt=fmt, datefmt=datefmt)

def _get_handler_dec(func):
    seen = LogDestStorage()
    return partial(func, seen)

@_get_handler_dec
def get_handler(seen, pkg, level, logdir, filename):
    targets = dict(
        TRACE=dict(
            stream_hn=RequestDebugStreamHandler,
            file_hn=RequestDebugFileHandler),
        DEBUG=dict(
            stream_hn=DebugStreamHandler,
            file_hn=DebugFileHandler),
        INFO=dict(
            stream_hn=InfoStreamHandler,
            file_hn=InfoFileHandler),
        WARNING=dict(
            stream_hn=WarnStreamHandler,
            file_hn=WarnFileHandler),
        ERROR=dict(
            stream_hn=ErrorStreamHandler,
            file_hn=ErrorFileHandler),
        CRITICAL=dict(
            stream_hn=CritStreamHandler,
            file_hn=CritFileHandler))

    handler = None
    try:
        conf = targets[level]
    except KeyError:
        raise ValueError('{} is not a valid log level'.format(level))

    if logdir is None or filename is None:
        dest = None
    else:
        dest = '{}/{}'.format(logdir, filename)

    l_id = (pkg, level, dest)
    if seen.contains(*l_id):
        # doesn't make sense to add duplicate loggers
        return
    seen.add(*l_id)

    if dest is None:
        # logging to console
        return conf['stream_hn'](
            sys.stderr if level in [
                'ERROR', 'WARNING', 'CRITICAL'] else sys.stdout)

    else:
        return conf['file_hn'](dest)
