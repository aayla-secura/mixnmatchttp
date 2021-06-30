import logging
import os
import string
import random
from wrapt import ObjectProxy

from .types import str_to_hex, str_remove_chars


logger = logging.getLogger(__name__)
__all__ = [
    'randhex',
    'randstr',
    'startswith',
]


def randhex(size):
    '''Returns a random hex string of length size

    The number of random bytes will be int(size / 2).
    Read from urandom.
    '''

    return str_to_hex(os.urandom(int(size / 2)))

def randstr(size,
            use_lower=True,
            use_upper=True,
            use_digit=True,
            use_punct=True,
            skip=''):
    '''Returns a random string of length size

    The string consists of letters, digits and punctuation excluding
    any characters given in skip.
    '''

    alphabet = ''
    if use_lower:
        alphabet += string.ascii_lowercase
    if use_upper:
        alphabet += string.ascii_uppercase
    if use_digit:
        alphabet += string.digits
    if use_punct:
        alphabet += string.punctuation
    if skip:
        alphabet = str_remove_chars(alphabet, skip)
    return ''.join([random.choice(alphabet) for i in range(size)])

def startswith(instr, pref):
    '''Like str.startswith but it correctly handles ObjectProxy's'''

    if isinstance(pref, ObjectProxy):
        return instr.startswith(pref.__wrapped__)
    return instr.startswith(pref)
