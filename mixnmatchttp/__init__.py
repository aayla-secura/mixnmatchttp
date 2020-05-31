from . import handlers
from . import servers
from .webapp import WebApp

import logging
try:  # python2.7 and above
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass


__all__ = [
    'handlers',
    'servers',
    'WebApp',
]

logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())
