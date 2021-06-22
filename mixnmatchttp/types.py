import logging
from copy import copy


logger = logging.getLogger(__name__)
__all__ = [
    'Settings',
]


class Settings:
    '''A dictionary with hidden defaults

    If <key> is not set on the instance, but is in the defaults then
    it can be accessed in the usual way, however <key> in <instance>
    would still return False.

    Defaults can be set using the setdefault or setdefaults methods.
    The setdefault method does not explicitly set the item as is the
    case for regular dictionaries.
    '''

    def __init__(self, **settings):
        self._defaults = {}
        self._data = {}
        for s in settings:
            setattr(self, s, settings[s])

    def setdefault(self, key, value):
        self._defaults[key] = value

    def setdefaults(self, **kargs):
        for k in kargs:
            self.setdefault(k, kargs[k])

    def update(self, other=None, /, **settings):
        explicit = {}
        defaults = {}
        if other is not None:
            if isinstance(other, Settings):
                explicit = other._data
                defaults = other._defaults
            else:
                explicit = other

        for k in explicit:
            self[k] = explicit[k]
        for k in settings:
            self[k] = settings[k]
        self.setdefaults(**defaults)

    def copy(self):
        data = self._data
        defaults = self._defaults
        try:
            self._data = {}
            self._defaults = {}
            clone = copy(self)
        finally:
            self._data = data
            self._defaults = defaults
        clone.update(self)
        return clone

    def __eq__(self, other):
        if not isinstance(other, Settings):
            return False
        return self._data == other._data and \
            self._defaults == other._defaults

    def __getattr__(self, key):
        if key.startswith('_'):
            return super().__getattr__(key)

        try:
            return self[key]
        except KeyError as e:
            raise AttributeError(e)

    def __getitem__(self, key):
        try:
            return self._data[key]
        except KeyError:
            return self._defaults[key]

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if not key.startswith('_'):
            self[key] = value

    def __setitem__(self, key, value):
        self._data[key] = value

    def __iter__(self):
        yield from self._data

    def __contains__(self, key):
        return key in self._data

    def __repr__(self):
        return repr(self._data)
