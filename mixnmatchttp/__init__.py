from . import handlers
from . import servers

__all__ = [
        'handlers',
        'servers',
        ]

import logging
try:  # python2.7 and above
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())
