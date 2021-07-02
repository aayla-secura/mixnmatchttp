import logging
import importlib
from copy import copy, deepcopy
from wrapt import ObjectProxy
from wrapt.wrappers import _ObjectProxyMetaType

from .containers import DefaultAttrs, DefaultAttrDict
from .exc import ConfError, ConfRuntimeError, \
    ConfTypeError, ConfValueError
from ..utils import merge


logger = logging.getLogger(__name__)
__all__ = [
    'Conf',
    'ConfItem',
]


class _NotInitializedError(Exception):
    pass

class ConfItem(ObjectProxy):
    def __init__(self, value, /, **settings):
        '''Configuration item - a proxy for its value

        In almost all respects this behaves as the value itself, but
        the settings used determine if/how the value is transformed
        and what other checks are done to make sure it's valid.

        Accepted settings:
        - merge_value: whether the value is to be merged with its
          previous one during an update; default is False
        - merge_settings: whether the settings are to be merged with
          the previous ones during an update; default is True
        - allowed_values: a list of allowed values. Default is None,
          i.e. no restriction.
        - allowed_types: a tuple of allowed types for this item; if
          the item is not an instance of any of them, a conversion is
          attempted for each of the types in turn (by calling its
          constructor with the item), and the first successful
          conversion is used, otherwise an error is raised;
          default is (<value.__class__>,)
        - transformer: a callable that takes the value and returns
          a new value; this is done after conversion to allowed_types
        - requires: a callable which is passed the final value as
          a single argument and must return a list of modules which
          are required by this item; default is None
        '''

        # cannot set any attributes before calling parent __init__
        self_settings = DefaultAttrs(dict(
            # TODO option to merge just value, value and explicit
            # settings or value and all settings
            mergeable=False,
            allowed_values=None,
            allowed_types=(value.__class__,),
            transformer=None,
            requires=None), **settings)
        if isinstance(value, ConfItem):
            self_settings.__merge__(value._self_settings)
            value = value.__wrapped__
        self.__init(value, self_settings)

    def __copy__(self):
        # type(self) returns the real type, e.g. ConfItem, whereas
        # self.__class__ returns the class of the object to which we
        # proxy
        clone = type(self)(
            copy(self.__wrapped__),
            **self._self_settings.__explicit__)
        return clone

    def __deepcopy__(self, memo=None):
        settings = deepcopy(self._self_settings)
        clone = type(self)(
            deepcopy(self.__wrapped__),
            **settings)
        return clone

    def __getattr__(self, attr):
        # overriding ObjectProxy's __getattr__ which raises ValueError
        # if it hasn't been initialized
        # raise instead a custom exception here so we can rely on
        # catching this case
        if attr == '__wrapped__':
            raise _NotInitializedError(
                'wrapper has not been initialised')
        return super().__getattr__(attr)

    def __repr__(self):
        return str(self.__wrapped__)

    def __merge__(self, other):
        if isinstance(other, ConfItem):
            value = other.__wrapped__
            settings = other._self_settings
        else:
            value = other
            settings = self._self_settings.__class__()

        self.__init(value, settings)

    @property
    def __initialized(self):
        try:
            self.__wrapped__
        except _NotInitializedError:
            return False
        return True

    def __init(self, value, settings):

        def conv_type(value):
            if isinstance(value, settings.allowed_types):
                return value
            # try to convert
            for t in settings.allowed_types:
                try:
                    return t(value)
                except (TypeError, ValueError) as e:
                    pass
            raise ConfTypeError(
                'Cannot convert {type} to any of {allowed_types}'.format(
                    type=value.__class__.__name__,
                    allowed_types=settings.allowed_types))

        def check_modules(value):
            if settings.requires is None:
                return
            for m in settings.requires(value):
                if importlib.util.find_spec(m) is None:
                    raise ConfRuntimeError(
                        'module {module} is required'.format(module=m))

        def transform(value):
            try:
                return settings.transformer(value)
            # TODO any other exceptions to handle here?
            except (TypeError, ValueError) as e:
                raise ConfTypeError(e)

        def merge_with_current(value):
            from copy import copy
            try:
                return merge(self.__wrapped__, value)
            except (TypeError, ValueError) as e:
                raise ConfTypeError(e)

        ##########
        if self.__initialized:
            settings = self._self_settings + settings

        if settings.allowed_values is not None \
                and value not in settings.allowed_values:
            raise ConfValueError('{v} is an invalid value'.format(v=value))

        if settings.allowed_types:
            value = conv_type(value)

        if settings.transformer is not None:
            value = transform(value)

        check_modules(value)

        if settings.mergeable and self.__initialized:
            value = merge_with_current(value)

        super().__init__(value)
        self._self_settings = settings

class Conf(DefaultAttrDict):
    '''Holds ConfItems as attributes or keys

    Reassigning an item will merge it with the current one (the newly
    assigned item takes precedence):
        - any settings not explicitly given in the new item will
          inherit its parent
        - if the value can be merged with the parent, it will be

    Getting an item as an attribute will return the actual value,
    whereas getting an item as key will return the ConfItem proxy to
    the value.
    '''

    __item_type__ = ConfItem
    __attempt_merge__ = True

    def __getattr__(self, name):
        confitem = super().__getattr__(name)
        if isinstance(confitem, ConfItem):
            return confitem.__wrapped__
        return confitem
