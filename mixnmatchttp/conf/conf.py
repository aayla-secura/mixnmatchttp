import logging
import importlib
from wrapt import ObjectProxy

from ..utils import merge
from ..types import Settings


logger = logging.getLogger(__name__)


class ConfError(Exception):
    pass

class ConfRuntimeError(ConfError, RuntimeError):
    pass

class ConfTypeError(ConfError, TypeError):
    pass

class Conf:
    '''Holds ConfItems

    Reassigning an item will merge it with the current one (the newly
    assigned item takes precedence):
        - any settings not explicitly given in the new item will
          inherit its parent
        - if the value can be merged with the parent, it will be
    '''

    def __init__(self, dic=None, /, **kwargs):
        init = dic or kwargs
        for k in init:
            setattr(self, k, init[k])

    def __setattr__(self, attr, val):
        curr = getattr(self, attr, None)
        try:
            new = ConfItem(val, inherit=curr)
        except ConfError as e:
            raise ConfError(
                'Error in config item {name}: {err!s}'.format(
                    name=attr, err=e))
        super().__setattr__(attr, new)

class ConfItem(ObjectProxy):
    def __init__(self, item, /, inherit=None, **settings):
        '''
        If item is an instance of <ConfItem>, then it is duplicated.
        Otherwise item is taken as a literal value and settings are
        inherited from inherit if given.
        Any explicitly given settings always take highest precedence.

        Accepted settings:
        - can_be_merged: whether to merge the new value with the value
          of inherit (if given); this is valid only for sequences and
          mappings, where concatenation/merging makes sense; default
          is False
        - allowed_types: a tuple of allowed types for this item;
          if the item is not an instance of any of them, a conversion
          is attempted for each of the types in turn (by calling its
          constructor with the item), and the first successful
          conversion is used, otherwise an error is raised;
          default is (<type(new value)>,)
        - required_modules: a list of modules which are required by
          this item; default is []

        | item is  | inherit  | result                           |
        | ConfItem | is given |                                  |
        ----------------------------------------------------------
        |     Y    |    Y     | merge inherit's value if         |
        |          |          | can_be_merged is used            |
        |          |          | inherit's settings are ignored   |
        |__________|__________|__________________________________|
        |     Y    |    N     | duplicate item                   |
        |__________|__________|__________________________________|
        |     N    |    Y     | use inherit's settings and       |
        |          |          | merge inherit's value if         |
        |          |          | can_be_merged is used            |
        |__________|__________|__________________________________|
        |     N    |    N     | use item as the new value        |
        '''

        self._self_settings = Settings()
        self._self_settings.setdefaults(
            can_be_merged=False,
            allowed_types=(),
            required_modules=[])
        if inherit is not None:
            if not isinstance(inherit, ConfItem):
                raise TypeError("'inherit' must be a <ConfItem>")
            self._self_settings.update(inherit._self_settings)
        if isinstance(item, ConfItem):
            self._self_settings.update(item._self_settings)
            value = item.__wrapped__
        else:
            value = item

        self._self_settings.update(settings)

        if 'allowed_types' not in self._self_settings:
            self._self_settings.setdefault(
                'allowed_types', (value.__class__,))

        self.__check_modules()

        value = self.__conv_type(value)
        if self._self_settings['can_be_merged'] \
                and inherit is not None:
            try:
                value = merge(inherit.__wrapped__, value)
            except TypeError as e:
                raise ConfTypeError(e)
        super().__init__(value)

    def __conv_type(self, value):
        if isinstance(value, self._self_settings['allowed_types']):
            return value
        # try to convert
        for t in self._self_settings['allowed_types']:
            try:
                return t(value)
            except (TypeError, ValueError) as e:
                pass
        raise ConfTypeError(
            'Cannot convert {type} to any of {allowed_types}'.format(
                type=value.__class__.__name__,
                allowed_types=self._self_settings['allowed_types']))

    def __check_modules(self):
        for m in self._self_settings['required_modules']:
            if importlib.util.find_spec(m) is None:
                raise ConfRuntimeError(
                    'module {module} is required'.format(module=m))
