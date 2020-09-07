import logging
from collections import UserDict


logger = logging.getLogger(__name__)
__all__ = [
    'Settings',
]

class Settings(UserDict):
    '''A dictionary with hidden defaults

    XXX todo parent support

    If <key> is not set on the instance, but is in the defaults then
    it can be accessed in the usual way, however <key> in <instance>
    would still return False.

    Defaults can be set using the setdefault or setdefaults methods.
    The setdefault method does not explicitly set the item as is the
    case for regular dictionaries.
    '''

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self._defaults = {}

    def setdefault(self, key, value):
        self._defaults[key] = value

    def setdefaults(self, **kargs):
        for k, v in kargs.items():
            self.setdefault(k, v)

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            return self._defaults[key]
