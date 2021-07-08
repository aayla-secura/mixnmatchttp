import logging
import os
import sys
import re
from functools import partial
from copy import copy

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
        #  print(f'XXX adding handler {handler.name}')

    def rm(self, pkg, level, dest):
        store = self._get_store(pkg)
        #  handler = store[(level, dest)]  # XXX
        #  print(f'XXX removing handler {handler.name}')
        del store[(level, dest)]

    def get(self, pkg, level, dest):
        curr_pkg = pkg
        at_root = False
        while True:
            store = self._get_store(curr_pkg)
            try:
                return store[(level, dest)]
            except KeyError:
                curr_pkg = '.'.join(curr_pkg.split('.')[:-1])
                if not curr_pkg:
                    if at_root:
                        return None
                    # one last time for the root logger ''
                    at_root = True

    def _get_store(self, pkg):
        store = self._store
        for p in pkg.split('.'):
            store.setdefault(p, {'.': {}})
            store = store[p]
        return store['.']

    def __str__(self):
        return str(self._store)


def get_destinations(destinations_map, complete=True):
    _destinations_map = destinations_map.copy()
    if complete:
        _highest_dest = None
        for _lvl in [
                'TRACE', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            try:
                _highest_dest = _destinations_map[_lvl]
            except KeyError:
                if _highest_dest is None:
                    continue
                _destinations_map[_lvl] = copy(_highest_dest)

    for level, destinations in _destinations_map.items():
        for i, dest in enumerate(destinations):
            if not dest:
                dest = ['']
            pkg, *files = dest
            if not files:
                files = ['{}.log'.format(pkg if pkg else 'all')]
            destinations[i] = (pkg, files)
    return _destinations_map

def get_formatter(level,
                  fmt=None,
                  datefmt=None,
                  log_colors={},
                  secondary_log_colors={}):
    if log_colors or secondary_log_colors:
        try:
            ColoredFormatter
        except NameError:
            raise ModuleNotFoundError(
                'colorlog is required if using colors')

        # prepend the color unless the format explicitly uses it
        if re.search('%\(([^)]+_)?log_color\)s', fmt):
            lcs = ''
        else:
            lcs = '%(log_color)s'
        fmt = lcs + fmt

        return ColoredFormatter(
            fmt=fmt,
            datefmt=datefmt,
            reset=True,
            log_colors=log_colors,
            secondary_log_colors=secondary_log_colors)
    else:
        return logging.Formatter(fmt=fmt, datefmt=datefmt)

def log_id(*args, **kwargs):
    if len(args) == 1:
        return _log_id_from_name(args[0].name)
    return _log_id_from_multi(*args, **kwargs)

def _log_id_from_name(name):
    pkg, level, dest = name.split('@', maxsplit=2)
    if not dest:
        dest = None
    return (pkg, level, dest), dest

def _log_id_from_multi(pkg, level, logdir, filename):
    if logdir is None or filename is None:
        dest = None
    else:
        dest = os.path.join(logdir, filename)

    return (pkg, level, dest), dest

def log_name(pkg, level, logdir, filename):
    dest = _log_id_from_multi(pkg, level, logdir, filename)[1]
    if dest is None:
        dest = ''
    return '@'.join((pkg, level, dest))

def get_handler(pkg, level, logdir=None, filename=None, existing=False):
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

    l_id, dest = log_id(pkg, level, logdir, filename)
    handler = log_store.get(*l_id)
    if handler is not None:
        if existing:
            return handler
        # doesn't make sense to add duplicate loggers
        return None

    if existing:
        # no such handler and not creating a new one
        return None

    if dest is None:
        # logging to console
        handler = conf['stream_hn'](
            sys.stderr if level in [
                'ERROR', 'WARNING', 'CRITICAL'] else sys.stdout)

    else:
        handler = conf['file_hn'](dest)

    handler.set_name(log_name(pkg, level, logdir, filename))
    log_store.add(handler, *l_id)
    return handler

def rm_handler(*args, **kwargs):
    l_id = log_id(*args, **kwargs)[0]
    log_store.rm(*l_id)


log_store = LogHandlerStorage()
