import logging
import re


logger = logging.getLogger(__name__)
__all__ = [
    'DictRepr',
    'DictReprExtended',
]


class DictRepr:
    '''A dictionary interface for the object's attributes

    It provides item access and assignment as well as iteration in the
    usual dictionary way. Assigning items and setting attributes is
    equivalent.

    Setting an item is the same as setting an attribute.
    I.e. o.x = 1 and o['x'] = 1 will both result in an attribute as
    well as an item 'x'. The only difference between setting an
    attribute and setting an item occurs if the key/attribute matches
    the regex in the 'skip' class attribute (default is /^_/).

    XXX

    If the dict_prop class attribute is set, then a dictionary by that
    name is instantiated for every instance, and every time an
    attribute or item is set on the instance, its value is saved in
    the dictionary, unless it matched the 'skip' regex.
    I.e. if the class's dict_prop is 'data', then
      o.x = 1
      o.y = 2
    will result in o.data being a static dictionary {'x': 1, 'y': 2}.
    All dict-related methods will operate on that dictionary.

    XXX One can assign items to this dictionary directly, if one does not
    wish to set the corresponding attribute.

    If dict_prop is not set (None) on the class, then every time any
    of the dict-related methods is accessed a new dictionary is
    constructed from the current values of the previously set
    attributes. This is the default.

    This class does not provide any methods meant to be called
    directly except keys (which is required for this class to be
    treated as a mapping). This is useful if you intend to assign
    items by the same name as those methods. If you want said methods,
    use DictReprExtended and take care not to set items with the same
    name as those methods.
    '''

    dict_prop = None
    skip = '^_'

    def keys(self):
        return self.__dict_data.keys()

    @property
    def __dict_data(self):
        if self.__class__.dict_prop is not None:
            return getattr(self, self.__class__.dict_prop)

        # get the current values of save attributes
        return {attr: getattr(self, attr) for attr in self.__attrs}

    @__dict_data.setter
    def __dict_data(self, value):
        if self.__class__.dict_prop is None:
            return
        setattr(self, self.__class__.dict_prop, value)

    def __init__(self, dic=None, /, **kwargs):
        self.__attrs = set()
        self.__dict_data = {}
        init = dic or kwargs
        for k in init:
            setattr(self, k, init[k])

    def __setattr__(self, attr, value):
        super().__setattr__(attr, value)
        if attr == self.__class__.dict_prop or \
                re.match('_DictRepr__', attr):
            return

        if self.__class__.skip is not None and \
                re.search(self.__class__.skip, attr):
            return

        self.__attrs.add(attr)
        if self.__class__.dict_prop is not None:
            self.__dict_data[attr] = value

    def __delattr__(self, attr):
        super().__delattr__(attr)
        self.__attrs.remove(attr)
        if self.__class__.dict_prop is not None:
            del self.__dict_data[attr]

    # XXX
    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __getitem__(self, key):
        return self.__dict_data.__getitem__(key)

    def __delitem__(self, key):
        self.__delattr__(key)

    def __copy__(self):
        return self.__dict_data.copy()

    def __contains__(self, key):
        return self.__dict_data.__contains__(key)

    def __iter__(self):
        return self.__dict_data.__iter__()

    def __len__(self):
        return self.__dict_data.__len__()

    def __le__(self, other):
        return self.__dict_data.__le__(other)

    def __lt__(self, other):
        return self.__dict_data.__lt__(other)

    def __ge__(self, other):
        return self.__dict_data.__ge__(other)

    def __gt__(self, other):
        return self.__dict_data.__gt__(other)

    def __eq__(self, other):
        return self.__dict_data.__eq__(other)

    def __ne__(self, other):
        return self.__dict_data.__ne__(other)

    def __reversed__(self):
        return self.__dict_data.__reversed__()

    def __str__(self):
        return self.__dict_data.__str__()

    def __repr__(self):
        return self.__dict_data.__repr__()

class DictReprExtended(DictRepr):
    '''Adds the standard dictionary methods'''

    def clear(self):
        keys = self.items()
        for k in keys:
            delattr(self, k)

    def copy(self):
        return self._DictRepr__dict_data.copy()

    @classmethod
    def fromkeys(cls, iterable, *args):
        return cls(dict.fromkeys(iterable, *args))

    def get(self, key, default=None, /):
        return self._DictRepr__dict_data.get(key, default)

    def items(self):
        return self._DictRepr__dict_data.items()

    def pop(self, key, *args):
        v = self._DictRepr__dict_data.pop(key, *args)
        try:
            delattr(self, key)
        except (AttributeError, KeyError):
            pass
        return v

    def popitem(self):
        k, v = self._DictRepr__dict_data.popitem()
        try:
            delattr(self, k)
        except (AttributeError, KeyError):
            pass
        return (k, v)

    def setdefault(self, key, default=None, /):
        try:
            curr = self[key]
        except KeyError:
            self[key] = default
            return default
        return curr

    def update(self, dic=None, /, **kwargs):
        new = dic or kwargs
        for k in new:
            setattr(self, k, new[k])

    def values(self):
        return self._DictRepr__dict_data.values()
