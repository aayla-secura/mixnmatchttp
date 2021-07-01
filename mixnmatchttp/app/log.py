import sys
import logging
from functools import partial
try:
    from colorlog import ColoredFormatter
except ImportError:
    pass


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

class CritFileHandler(FileHandler):
    _min_level = logging.CRITICAL
    _max_level = logging.CRITICAL

class CritStreamHandler(StreamHandler):
    _min_level = logging.CRITICAL
    _max_level = logging.CRITICAL

class ErrorFileHandler(FileHandler):
    _min_level = logging.ERROR
    _max_level = logging.ERROR

class ErrorStreamHandler(StreamHandler):
    _min_level = logging.ERROR
    _max_level = logging.ERROR

class WarnFileHandler(FileHandler):
    _min_level = logging.WARNING
    _max_level = logging.WARNING

class WarnStreamHandler(StreamHandler):
    _min_level = logging.WARNING
    _max_level = logging.WARNING

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


def _get_formatter(level, fmt, datefmt, color):
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
    seen = set()
    return partial(func, seen)

@_get_handler_dec
def _get_handler(seen, pkg, level, logdir, filename):
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
    if l_id in seen:
        # doesn't make sense to add duplicate loggers
        return
    seen.add(l_id)

    if dest is None:
        # logging to console
        return conf['stream_hn'](
            sys.stderr if level in [
                'ERROR', 'WARNING', 'CRITICAL'] else sys.stdout)

    else:
        return conf['file_hn'](dest)

def get_loggers(
        destinations_map,
        color=True,
        logdir=None,
        fmt='%(levelname)-8s [%(asctime)s] %(name)s: %(message)s',
        dbgfmt=('%(levelname)-8s [%(asctime)s] %(name)s:'
                '%(funcName)s@%(lineno)d : %(message)s'),
        datefmt='%d/%b/%Y %H:%M:%S'):
    '''Sets up loggers for given packages and levels.

    destinations_map is a dictionary where the keys are one of the
    supported log levels: CRITICAL, ERROR, WARNING, INFO, DEBUG,
    TRACE, and where the values is a list of iterables of one or
    more values. The first value is the logger name (should match
    a package or module), and the remaining are destinations for
    logging, which should be filenames or None for console log. If no
    filenames are given, then <pkg>.log is used (if pkg is '', i.e.
    root logger, then default file is all.log).

    When logging to console, WARNING and above is sent to stderr, and
    other console output to stdout.

    If logdir is None, all output is to console.

    If any of the levels is missing from the map it is added to the
    destinations of the highest given level. For example:
        {
            'WARNING': [('mixnmatchttp', None, 'error.log')],
            'INFO': [('mixnmatchttp', 'info.log')],
            'DEBUG': [('mixnmatchttp', None)],
            'TRACE': [('mixnmatchttp',)],
        }
    will log WARNING, ERROR and CRITICAL to stderr and to error.log,
    INFO will go to info.log and DEBUG to stdout and TRACE to
    mixnmatchttp.log.

    If color is True, then log is colorful.
    '''

    loggers = {}

    destinations_map = destinations_map.copy()
    _highest_dest = None
    for _lvl in [
            'TRACE', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        try:
            _highest_dest = destinations_map[_lvl]
        except KeyError:
            if _highest_dest is None:
                continue
            destinations_map[_lvl] = _highest_dest

    for level, destinations in destinations_map.items():
        for dest in destinations:
            pkg, *files = dest
            if not files:
                files = ['{}.log'.format(pkg if pkg else 'all')]

            for filename in files:
                handler = _get_handler(pkg, level, logdir, filename)
                if handler is None:
                    # has already been added
                    continue

                lf = _get_formatter(
                    level, fmt if level != 'DEBUG' else dbgfmt,
                    datefmt, color)
                if lf is not None:
                    handler.setFormatter(lf)

                logger = logging.getLogger(pkg)
                logger.addHandler(handler)
                logger.setLevel(logging.TRACE)  # the handler filters
                loggers[pkg] = logger

    return loggers
