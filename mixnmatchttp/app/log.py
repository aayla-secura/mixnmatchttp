import sys
import logging


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


def get_loggers(destinations_map, logdir=None, fmt=None):
    def unpack_dest(pkg, *files):
        return pkg, files

    log_formatter = None
    if fmt is not None:
        log_formatter = logging.Formatter(
            fmt=fmt, datefmt='%d/%b/%Y %H:%M:%S')
    loggers = {}
    seen = []
    logger_classes = {
        'REQUEST': (RequestDebugStreamHandler,
                    RequestDebugFileHandler, 'request.log'),
        'DEBUG': (DebugStreamHandler, DebugFileHandler, 'debug.log'),
        'INFO': (InfoStreamHandler, InfoFileHandler, None),
        'ERROR': (ErrorStreamHandler, ErrorFileHandler, 'error.log')}

    for level, destinations in destinations_map.items():
        for dest in destinations:
            pkg, files = unpack_dest(*dest)
            if not files:
                files = [None]
            for filename in files:
                streamHandler, fileHandler, def_filename = \
                    logger_classes[level]
                if logdir is None:
                    if '{}.{}'.format(pkg, level) in seen:
                        # doesn't make sense to add duplicate loggers
                        # when not writing to files
                        continue
                    handler = streamHandler(
                        sys.stderr
                        if level == 'ERROR' else sys.stdout)
                else:
                    if filename is None:
                        filename = def_filename
                    if filename is None:
                        if '/' in pkg:
                            raise ValueError(
                                ('{} cannot be used as a '
                                 'filename').format(pkg))
                        filename = '{}.log'.format(pkg)
                    handler = fileHandler('{}/{}'.format(
                        logdir, filename))
                if log_formatter is not None:
                    handler.setFormatter(log_formatter)
                logger = logging.getLogger(pkg)
                logger.addHandler(handler)
                logger.setLevel(logging.TRACE)  # the handler filters
                loggers[pkg] = logger
                seen.append('{}.{}'.format(pkg, level))
    return loggers
