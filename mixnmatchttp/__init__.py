import logging as _logging
from logging import NullHandler as _NullHandler

_logging.TRACE = 1
class _TraceLogger(_logging.Logger):
    def trace(self, *args, **kwargs):
        return super(_TraceLogger, self).log(
            _logging.TRACE, *args, **kwargs)


_logging.setLoggerClass(_TraceLogger)
_logger = _logging.getLogger(__name__)
_logger.addHandler(_NullHandler())
