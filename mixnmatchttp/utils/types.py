import logging
import re
from collections.abc import Iterable, Mapping, \
    MutableMapping, MutableSet, MutableSequence


logger = logging.getLogger(__name__)
__all__ = [
    'ReprFromStr',
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
]


class ReprFromStr:
    def __repr__(self):
        return '{cls}({val})'.format(
            cls=self.__class__.__name__,
            val=self.__str__())

    def __str__(self):
        '''This should be overridden in children'''

        raise NotImplementedError


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
