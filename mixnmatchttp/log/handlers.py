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
