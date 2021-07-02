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


class LogHandlerStorage:
    def __init__(self):
        self._store = {'.': {}}

    def add(self, handler, pkg, level, dest):
        store = self._get_store(pkg)
        store[(level, dest)] = handler

    def _get_store(self, pkg):
        store = self._store
        for p in pkg.split('.'):
            store.setdefault(p, {'.': {}})
            store = store[p]
        return store['.']

    def get(self, pkg, level, dest):
        curr_pkg = pkg
        while True:
            store = self._get_store(curr_pkg)
            try:
                return store[(level, dest)]
            except KeyError:
                curr_pkg = '.'.join(curr_pkg.split('.')[:-1])
                if not curr_pkg:
                    return None

    def __str__(self):
        return str(self._store)


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
    store = LogHandlerStorage()
    return partial(func, store)

@_get_handler_dec
def get_handler(store, pkg, level, logdir, filename):
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

    try:
        conf = targets[level]
    except KeyError:
        raise ValueError('{} is not a valid log level'.format(level))

    if logdir is None or filename is None:
        dest = None
    else:
        dest = '{}/{}'.format(logdir, filename)

    l_id = (pkg, level, dest)
    handler = store.get(*l_id)
    if handler is not None:
        # doesn't make sense to add duplicate loggers
        return None

    if dest is None:
        # logging to console
        handler = conf['stream_hn'](
            sys.stderr if level in [
                'ERROR', 'WARNING', 'CRITICAL'] else sys.stdout)

    else:
        handler = conf['file_hn'](dest)

    store.add(handler, *l_id)
    return handler
