import logging
from collections import MutableMapping, OrderedDict

from ..utils import ReprFromStr, is_map_like


logger = logging.getLogger(__name__)
__all__ = [
    'CaseInsensitiveOrderedDict',
]


class CaseInsensitiveOrderedDict(ReprFromStr, MutableMapping):
    '''Case-insensitive dictionary

    Based on requests.structures.CaseInsensitiveDict (thanks!)

    The structure remembers the case of the last key to be set.
    The item as well as the key in its original case is returned
    by the getkey method.
    '''

    def __init__(self, data=None, /, **kwargs):
        self.__data__ = OrderedDict()
        if data is None:
            data = {}
        self.update(data, **kwargs)

    def __setitem__(self, key, value):
        # Use the lowercased key for lookups, but store the actual
        # key alongside the value.
        self.__data__[key.lower()] = (key, value)

    def __getitem__(self, key):
        return self.__data__[key.lower()][1]

    def __delitem__(self, key):
        del self.__data__[key.lower()]

    def __iter__(self):
        return (casedkey for casedkey, mappedvalue in self.__data__.values())

    def __len__(self):
        return len(self.__data__)

    def __eq__(self, other):
        if is_map_like(other):
            other = self.__class__(other)
        else:
            return NotImplemented
        # Compare insensitively
        return dict(self.lower_items()) == dict(other.lower_items())

    def getkey(self, key):
        return self.__data__[key.lower()][0]

    def copy(self):
        return self.__class__(self.__data__.values())

    def __str__(self):
        return str(dict(self.items()))
