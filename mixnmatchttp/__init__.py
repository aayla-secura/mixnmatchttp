import logging as _logging
from logging import NullHandler as _NullHandler

_logging.TRACE = 1
class _TraceLogger(_logging.Logger):
    def trace(self, *args, **kargs):
        return super(_TraceLogger, self).log(
            _logging.TRACE, *args, **kargs)


_logging.setLoggerClass(_TraceLogger)
_logger = _logging.getLogger(__name__)
_logger.addHandler(_NullHandler())


# XXX  from . import handlers
#  from . import servers
#  from .app import App


__all__ = [
    'handlers',
    'servers',
    'App',
]
