from colorlog.escape_codes import \
    esc as _esc, escape_codes as _esc_codes
_esc_codes['inverse'] = _esc('03')
from .log import *
