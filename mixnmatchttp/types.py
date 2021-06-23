import logging
from copy import copy, deepcopy


logger = logging.getLogger(__name__)
__all__ = [
    'ObjectWithDefaults',
    'DictWithDefaults',
]


class ObjectWithDefaults:
    '''An object with default attributes

    If <attr> is not set on the instance, but is in the defaults then
    it can be accessed in the usual way.

    Attributes can also be accessed as keys

    Supported operations:
      in: To check if an attribute is explicitly set, then use the in
          operator, like <attr> in <instance>.
      +:  You can add object A to B and this would return a new
          object with all of A's attributes and defaults in addition
          to B's. B's attributes and defaults override those of A's
      iteration: You can iterate over the attributes; order not
          guaranteed
      indexing: you can set and get attributes as you do dictionary
          keys

    Defaults can only be set at instantiation. No public methods are
    provided by this class to ensure that they don't clash with
    attributes to be set.
    '''

    def __init__(self, defaults={}, /, **kargs):
        self.__data = kargs.copy()
        self.__defaults = defaults.copy()

    def __setitem__(self, attr, value):
        self.__data[attr] = value

    def __getitem__(self, attr):
        try:
            return self.__data[attr]
        except KeyError:
            return self.__defaults[attr]

    def __setattr__(self, attr, value):
        if attr.startswith('_ObjectWithDefaults__'):
            super().__setattr__(attr, value)
        else:
            self.__data[attr] = value

    def __getattr__(self, attr):
        if attr.startswith('_ObjectWithDefaults__'):
            raise AttributeError(attr)

        try:
            return self.__getitem__(attr)
        except KeyError as e:
            raise AttributeError(e)

    def __eq__(self, other):
        if not isinstance(other, ObjectWithDefaults):
            return False
        return self.__data == other.__data and \
            self.__defaults == other.__defaults

    def __iter__(self):
        yield from self.__data

    def __contains__(self, key):
        return key in self.__data

    def __add__(self, other):
        if not isinstance(other, ObjectWithDefaults):
            return NotImplemented

        data = self.__data
        defaults = self.__defaults
        try:
            self.__data = {}
            self.__defaults = {}
            clone = copy(self)
        finally:
            self.__data = data
            self.__defaults = defaults
        clone.__data = copy(data)
        clone.__defaults = copy(defaults)
        clone.__data.update(other.__data)
        clone.__defaults.update(other.__defaults)
        return clone

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        if not isinstance(other, ObjectWithDefaults):
            return NotImplemented
        self.__data.update(other.__data)
        self.__defaults.update(other.__defaults)
        return self

    def __repr__(self):
        return repr(self.__data)

class DictWithDefaults:
    '''A dictionary with hidden defaults

    If <key> is not set on the instance, but is in the defaults then
    it can be accessed in the usual way, however <key> in <instance>
    would still return False.

    Defaults can be set using the setdefault or setdefaults methods.
    The setdefault method does not explicitly set the item as is the
    case for regular dictionaries.
    '''

    def __init__(self, **kargs):
        self._defaults = {}
        self._data = {}
        self.update(kargs)

    def setdefault(self, key, value):
        self._defaults[key] = value

    def setdefaults(self, **kargs):
        for k in kargs:
            self.setdefault(k, kargs[k])

    def update(self, other=None, /, **kargs):
        '''TODO'''

        explicit = {}
        defaults = {}
        if other is not None:
            if isinstance(other, DictWithDefaults):
                explicit = other._data
                defaults = other._defaults
            else:
                explicit = other

        self._data.update(explicit)
        self._defaults.update(defaults)

    def copy(self, deep=False):
        if deep:
            _copy = deepcopy
        else:
            _copy = copy
        data = self._data
        defaults = self._defaults
        try:
            self._data = {}
            self._defaults = {}
            clone = _copy(self)
        finally:
            self._data = data
            self._defaults = defaults
        clone._data = _copy(data)
        clone._defaults = _copy(defaults)
        return clone

    def __eq__(self, other):
        if not isinstance(other, DictWithDefaults):
            return False
        return self._data == other._data and \
            self._defaults == other._defaults

    def __getitem__(self, key):
        try:
            return self._data[key]
        except KeyError:
            return self._defaults[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __iter__(self):
        yield from self._data

    def __contains__(self, key):
        return key in self._data

    def __repr__(self):
        return repr(self._data)
