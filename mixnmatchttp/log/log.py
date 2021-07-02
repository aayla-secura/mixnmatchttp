import sys
import logging

from .utils import get_handler, get_formatter


__all__ = [
    'get_loggers'
]


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
            if not dest:
                dest = ['']
            pkg, *files = dest
            if not files:
                files = ['{}.log'.format(pkg if pkg else 'all')]

            for filename in files:
                logger = logging.getLogger(pkg)
                logger.setLevel(logging.TRACE)  # the handler filters
                loggers[pkg] = logger

                handler = get_handler(pkg, level, logdir, filename)
                if handler is not None:
                    lf = get_formatter(
                        level, fmt if level != 'DEBUG' else dbgfmt,
                        datefmt, color)
                    if lf is not None:
                        handler.setFormatter(lf)
                    logger.addHandler(handler)

    return loggers
