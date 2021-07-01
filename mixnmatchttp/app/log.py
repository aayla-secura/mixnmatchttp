import sys
import logging
from functools import partial


class LogHandler:
    def emit(self, record):
        if record.levelno < self._min_level \
                or record.levelno > self._max_level:
            return
        super().emit(record)

class FileHandler(LogHandler, logging.FileHandler):
    pass

class StreamHandler(LogHandler, logging.StreamHandler):
    pass

class ErrorFileHandler(FileHandler):
    _min_level = logging.WARNING
    _max_level = logging.ERROR

class ErrorStreamHandler(StreamHandler):
    _min_level = logging.WARNING
    _max_level = logging.ERROR

class InfoFileHandler(FileHandler):
    _min_level = logging.INFO
    _max_level = logging.INFO

class InfoStreamHandler(StreamHandler):
    _min_level = logging.INFO
    _max_level = logging.INFO

class DebugFileHandler(FileHandler):
    _min_level = logging.DEBUG
    _max_level = logging.DEBUG

class DebugStreamHandler(StreamHandler):
    _min_level = logging.DEBUG
    _max_level = logging.DEBUG

class RequestDebugFileHandler(FileHandler):
    _min_level = logging.TRACE
    _max_level = logging.TRACE

class RequestDebugStreamHandler(StreamHandler):
    _min_level = logging.TRACE
    _max_level = logging.TRACE


def _get_formatter(level, fmt, datefmt):
    if fmt is None:
        return None
    if level == 'DEBUG':
        fmt = '[%(filename)s, %(lineno)d] {}'.format(fmt)
    return logging.Formatter(fmt=fmt, datefmt=datefmt)

def _get_handler_dec(func):
    seen = set()
    return partial(func, seen)

@_get_handler_dec
def _get_handler(seen, pkg, level, logdir, filename):
    targets = dict(
        REQUEST=dict(
            stream_hn=RequestDebugStreamHandler,
            file_hn=RequestDebugFileHandler,
            default_fname='request.log'),
        DEBUG=dict(
            stream_hn=DebugStreamHandler,
            file_hn=DebugFileHandler,
            default_fname='debug.log'),
        INFO=dict(
            stream_hn=InfoStreamHandler,
            file_hn=InfoFileHandler,
            default_fname='info.log'),
        ERROR=dict(
            stream_hn=ErrorStreamHandler,
            file_hn=ErrorFileHandler,
            default_fname='error.log'))

    handler = None
    if logdir is None:
        # logging to console
        if '{}.{}'.format(pkg, level) not in seen:
            # doesn't make sense to add duplicate loggers
            # when not writing to files
            handler = targets[level]['stream_hn'](
                sys.stderr if level == 'ERROR' else sys.stdout)

    else:
        if filename is None:
            filename = targets[level]['default_fname']
        handler = targets[level]['file_hn'](
            '{}/{}'.format(logdir, filename))

    seen.add('{}.{}'.format(pkg, level))
    return handler

def get_loggers(
        destinations_map,
        logdir=None,
        fmt=None,
        datefmt='%d/%b/%Y %H:%M:%S'):

    loggers = {}

    for level, destinations in destinations_map.items():
        for dest in destinations:
            pkg, *files = dest
            if not files:
                files = [None]

            for filename in files:
                handler = _get_handler(pkg, level, logdir, filename)
                if handler is None:
                    continue

                lf = _get_formatter(level, fmt, datefmt)
                if lf is not None:
                    handler.setFormatter(lf)

                logger = logging.getLogger(pkg)
                logger.addHandler(handler)
                logger.setLevel(logging.TRACE)  # the handler filters
                loggers[pkg] = logger

    return loggers
