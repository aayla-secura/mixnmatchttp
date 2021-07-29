import logging
import re
import os
import string
import random
from copy import copy
from wrapt import ObjectProxy


logger = logging.getLogger(__name__)
__all__ = [
    'randhex',
    'randstr',
    'startswith',
    'num_charsets',
    'str_remove_chars',
    'str_trunc',
    'str_to_hex',
    'hex_to_bytes',
    'int_to_hex',
    'int_to_bytes',
    'param_dict',
    'merge',
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

def num_charsets(arg):
    '''Returns the number of character sets in arg'''

    charsets = ['a-z', 'A-Z', '0-9']
    charsets += ['^{}'.format(''.join(charsets))]
    num = 0
    for c in charsets:
        if re.search('[{}]'.format(c), arg):
            num += 1
    return num

def str_remove_chars(s, skip):
    return s.translate(str.maketrans(dict.fromkeys(skip)))

def str_trunc(s, size):
    if len(s) <= size:
        return s
    if isinstance(s, bytes):
        suff = b'...'
    else:
        suff = '...'
    return s[:size - 3] + suff

def str_to_hex(s):
    if not isinstance(s, bytes):
        s = s.encode("utf-8")
    return s.hex()

def hex_to_bytes(s):
    return bytes.fromhex(s)

def int_to_hex(i):
    h = '{:x}'.format(i)
    if len(h) % 2 != 0:
        h = '0' + h
    return h

def int_to_bytes(i):
    return hex_to_bytes(int_to_hex(i))

def param_dict(s,
               itemsep=' *; *',
               valsep='=',
               values_are_opt=False,
               decoder=None):
    '''Returns a dictionary of keys/values from the string s

    itemsep: regex for separating items
    valsep: literal string for separating key/value
    decoder: a callable to decode keys and values
    '''

    if s is None:
        return {}

    if decoder is None:
        decoder = lambda o: o
    params = dict()
    sepfunc = lambda x: x.split(valsep)
    if values_are_opt:
        sepfunc = lambda x: x.partition(valsep)[0::2]

    try:
        params = {decoder(k): decoder(v) for k, v in [
            sepfunc(v) for v in re.split(itemsep, s)]}
    except ValueError:
        pass

    logger.debug('Got params from {}: {}'.format(s, params))
    return params

def merge(valA, valB, inplace=False):
    '''Attempt to merge valA and valB, valB takes precedence

    Works for sequences and mappings.
    If inplace is True, then it updates valA which must be mutable. If
    valA is not mutable raises TypeError. If inplace is False
    (default), it does not change the values, but returns a new one.
    '''

    if inplace:
        new = valA
    else:
        new = copy(valA)

    if hasattr(new, '__merge__'):
        new.__merge__(valB)
    elif hasattr(new, 'update'):
        new.update(valB)
    elif hasattr(new, 'extend'):
        new.extend(valB)
    elif hasattr(new, 'add'):
        for k in valB:
            new.add(k)
    elif hasattr(new, '__iadd__'):
        new += valB
    elif hasattr(new, '__ior__'):
        new |= valB
    elif hasattr(new, '__setitem__'):
        for k in valB:
            new[k] = valB[k]
    elif not inplace:
        # only applicable if making a copy
        if hasattr(new, '__add__'):
            new = new + valB
        elif hasattr(new, '__or__'):
            new = new | valB
    else:
        raise TypeError('Cannot merge {} and {}'.format(
            valA.__class__.__name__, valB.__class__.__name__))
    return new
