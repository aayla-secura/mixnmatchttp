import logging
import re
from copy import copy
from collections.abc import Iterable, Mapping, \
    MutableMapping, MutableSet, MutableSequence


logger = logging.getLogger(__name__)
__all__ = [
    'is_mutable',
    'is_bool_like',
    'is_str',
    'is_str_like',
    'is_seq_like',
    'is_iterable',
    'is_map_like',
    'is_mergeable',
    'to_bool',
    'to_natint',
    'to_posint',
    'str_remove_chars',
    'str_trunc',
    'str_to_hex',
    'hex_to_bytes',
    'int_to_hex',
    'int_to_bytes',
    'param_dict',
    'merge',
]


def is_mutable(val):
    return isinstance(val, (
        MutableMapping, MutableSet, MutableSequence))

def is_bool_like(val):
    if is_str(val):
        return val.lower() in [
            '1', 'yes', 'true', '', '0', 'no', 'false']
    return val in [None, 0, 1]

def is_str(val):
    '''True if val is a string (including unicode or bytes)'''

    return isinstance(val, (str, bytes))

def is_str_like(val):
    '''True if val can be converted to string straightforwardly

    i.e. if it's a string, boolean or int
    '''

    return is_str(val) or isinstance(val, (int, float, bool))

def is_seq_like(val):
    '''True if val is an iterable (but not a string, or dict)

    i.e. if it's a list, set, tuple, or some mutable sequence
    '''

    return isinstance(val, Iterable) \
        and not is_str_like(val) \
        and not is_map_like(val)

def is_iterable(val):
    '''True if val is any iterable'''

    return isinstance(val, Iterable)

def is_map_like(val):
    '''True if val is like a dict (mapping)'''

    return isinstance(val, Mapping)

def is_mergeable(val, inplace=True):
    '''True if value can be merged with another of its type'''

    # __merge__ are custom used by us
    return hasattr(val, '__merge__') \
        or hasattr(val, 'update') \
        or hasattr(val, 'extend') \
        or hasattr(val, 'add') \
        or hasattr(val, '__iadd__') \
        or hasattr(val, '__ior__') \
        or hasattr(val, '__setitem__') \
        or not inplace and (
            hasattr(val, '__add__')
            or hasattr(val, '__or__'))

def to_bool(val):
    '''Converts val to a boolean. val can be numeric or a string

    If None it is False.
    If numeric, 0 is False, 1 is True and otherwise ValueError is
    raised.
    If a string, "1", "yes" or "true" is True; "", "0", "no" or
    "false" is False and otherwise ValueError is raised. Comparison is
    case-insensitive.
    '''

    if not is_bool_like(val):
        raise ValueError('{} is not a boolean'.format(val))
    if (is_str(val) and val.lower() in ['1', 'yes', 'true']) \
            or val == 1:
        return True
    return False

def to_natint(val, base=0):
    '''Convert val to an integer and requires it to be >=0'''

    if is_str(val):
        new = int(val, base=base)
    else:
        new = int(val)
    if new < 0:
        raise ValueError('{} is negative'.format(val))
    return new

def to_posint(val, base=0):
    '''Convert val to an integer and requires it to be >0'''

    if is_str(val):
        new = int(val, base=base)
    else:
        new = int(val)
    if new <= 0:
        raise ValueError('{} is not positive'.format(val))
    return new

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
