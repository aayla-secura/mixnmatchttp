import logging
from collections import MutableMapping, Mapping, OrderedDict


logger = logging.getLogger(__name__)
__all__ = [
    'CaseInsensitiveOrderedDict',
]


class CaseInsensitiveOrderedDict(MutableMapping):
    '''Case-insensitive dictionary

    Based on requests.structures.CaseInsensitiveDict (thanks!)

    The structure remembers the case of the last key to be set.
    The item as well as the key in its original case is returned
    by the getkey method.
    '''

    def __init__(self, data=None, /, **kwargs):
        self._store = OrderedDict()
        if data is None:
            data = {}
        self.update(data, **kwargs)

    def __setitem__(self, key, value):
        # Use the lowercased key for lookups, but store the actual
        # key alongside the value.
        self._store[key.lower()] = (key, value)

    def __getitem__(self, key):
        return self._store[key.lower()][1]

    def __delitem__(self, key):
        del self._store[key.lower()]

    def __iter__(self):
        return (casedkey for casedkey, mappedvalue in self._store.values())

    def __len__(self):
        return len(self._store)

    def __eq__(self, other):
        if isinstance(other, Mapping):
            other = self.__class__(other)
        else:
            return NotImplemented
        # Compare insensitively
        return dict(self.lower_items()) == dict(other.lower_items())

    def getkey(self, key):
        return self._store[key.lower()][0]

    def copy(self):
        return self.__class__(self._store.values())

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            self.__str__())

    def __str__(self):
        return str(dict(self.items()))