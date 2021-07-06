import sys
import logging

from .utils import get_handler, get_formatter, rm_handler, \
    get_destinations


__all__ = [
    'get_loggers',
    'clear_loggers',
]


def get_loggers(
        destinations_map,
        logdir=None,
        fmt='%(message)s',
        dbgfmt=None,
        datefmt=None,
        log_colors={},
        secondary_log_colors={}):
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

    If log_colors or secondary_log_colors are given, then log is
    colorful. See doc on colorlog for their format.
    '''

    loggers = {}
    if dbgfmt is None:
        dbgfmt = fmt
    _destinations_map = get_destinations(
        destinations_map, complete=True)

    for level, destinations in _destinations_map.items():
        for pkg, files in destinations:
            for filename in files:
                logger = logging.getLogger(pkg)
                logger.setLevel(logging.TRACE)  # the handler filters
                loggers[pkg] = logger

                handler = get_handler(
                    pkg, level, logdir=logdir, filename=filename)
                if handler is None:
                    continue

                lf = get_formatter(
                    level,
                    fmt=fmt if level != 'DEBUG' else dbgfmt,
                    datefmt=datefmt,
                    log_colors=log_colors,
                    secondary_log_colors=secondary_log_colors)
                if lf is not None:
                    handler.setFormatter(lf)
                logger.addHandler(handler)

    return loggers

def clear_loggers(loggers, destinations_map=None, logdir=None):
    '''Remove specified handlers from loggers

    If destinations_map is None, then all handlers are removed.
    Otherwise only those handlers in destinations_map are removed.
    Loggers are never removed, but they may not have any handlers
    after this call.
    '''

    def _clear_all_loggers():
        for logger in loggers.values():
            for handler in logger.handlers.copy():
                if handler.name is None:
                    # not set by us
                    continue
                logger.removeHandler(handler)
                rm_handler(handler)

    if destinations_map is None:
        _clear_all_loggers()
        return

    _destinations_map = get_destinations(
        destinations_map, complete=False)
    for level, destinations in _destinations_map.items():
        for pkg, files in destinations:
            for filename in files:
                try:
                    logger = loggers[pkg]
                except KeyError:
                    continue

                handler = get_handler(
                    pkg,
                    level,
                    logdir=logdir,
                    filename=filename,
                    existing=True)
                if handler is None:
                    continue

                rm_handler(
                    pkg, level, logdir=logdir, filename=filename)
                logger.removeHandler(handler)
