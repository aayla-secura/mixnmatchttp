#  from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import *
from future import standard_library
standard_library.install_aliases()

import re
from datetime import datetime

from ...utils import datetime_to_timestamp, date_from_timestamp

def num_charsets(arg):
    '''Returns the number of character sets in arg'''

    charsets = ['a-z', 'A-Z', '0-9']
    charsets += ['^{}'.format(''.join(charsets))]
    num = 0
    for c in charsets:
        if re.search('[{}]'.format(c), arg):
            num += 1
    return num

def cookie_expflag(expiry):
    '''Returns an "Expires={date} GMT" flag for cookies

    - expiry should be one of:
    1) an int or float as UTC seconds since Unix epoch
    2) datetime object
    '''

    if expiry is None:
        return ''
    fmt = '%a, %d %b %Y %H:%M:%S GMT'
    ts = expiry
    if isinstance(ts, datetime):
        ts = datetime_to_timestamp(ts, to_utc=True)
    return 'Expires={}; '.format(date_from_timestamp(
        ts, relative=False, from_utc=True, to_utc=True,
        datefmt=fmt))
