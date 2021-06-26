import logging
import importlib
from copy import copy, deepcopy
from wrapt import ObjectProxy
from wrapt.wrappers import _ObjectProxyMetaType

from .containers import DefaultAttrs, DefaultAttrDict
from .exc import ConfError, ConfRuntimeError, ConfTypeError


logger = logging.getLogger(__name__)
__all__ = [
    'Conf',
    'ConfItem',
]


class _NotInitializedError(Exception):
    pass

class _ConfItemMeta(_ObjectProxyMetaType):
    def __new__(cls, name, bases, attrs):
        new = super().__new__(cls, name, bases, attrs)
        # save the class of the proxyobject for later, since __class__
        # is overriden by a property in ObjectProxy
        new.__proxyclass__ = new
        return new

class ConfItem(ObjectProxy, metaclass=_ConfItemMeta):
    def __init__(self, value, /, **settings):
        '''Configuration item - a proxy for its value

        In almost all respects this behaves as the value itself, but
        the settings used determine if/how the value is transformed
        and what other checks are done to make sure it's valid.

        Accepted settings:
        - mergeable: whether the value is to be merged with its
          previous one during an update (see __merge__ method);
          this is valid only for sequences and mappings,
          where concatenation/merging makes sense; default is False
        - allowed_types: a tuple of allowed types for this item; if
          the item is not an instance of any of them, a conversion is
          attempted for each of the types in turn (by calling its
          constructor with the item), and the first successful
          conversion is used, otherwise an error is raised;
          default is (<type(value)>,)
        - transformer: a callable that takes the value and returns
          a new value; this is done after conversion to allowed_types
        - requires: a list of modules which are required by
          this item; default is ()
        '''

        # cannot set any attributes before calling parent __init__
        self_settings = DefaultAttrs(dict(
            mergeable=False,
            allowed_types=(value.__class__,),
            transformer=None,
            requires=()), **settings)
        if isinstance(value, ConfItem):
            self_settings.__merge__(value._self_settings)
            value = value.__wrapped__
        self.__init(value, self_settings)

    @property
    def __mergeable__(self):
        return self._self_settings.mergeable

    def __copy__(self):
        clone = self.__proxyclass__(
            copy(self.__wrapped__),
            **self._self_settings.__explicit__)
        return clone

    def __deepcopy__(self, memo=None):
        settings = deepcopy(self._self_settings)
        clone = self.__proxyclass__(
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
        self_settings = self._self_settings

        if isinstance(other, ConfItem):
            value = other.__wrapped__
            #  other_settings = other._self_settings
            other_settings = self._self_settings.__class__(
                **other._self_settings.__explicit__)
        else:
            value = other
            other_settings = self._self_settings.__class__()

        self.__init(value, self_settings + other_settings)

    @property
    def __initialized(self):
        try:
            self.__wrapped__
        except _NotInitializedError:
            return False
        return True

    def __init(self, value, settings):
        from ..utils import merge as _merge

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

        def check_modules():
            for m in settings.requires:
                if importlib.util.find_spec(m) is None:
                    raise ConfRuntimeError(
                        'module {module} is required'.format(module=m))

        def transform(value):
            try:
                return settings.transformer(value)
            # TODO any other exceptions to handle here?
            except (TypeError, ValueError) as e:
                raise ConfTypeError(e)

        def merge(value):
            from copy import copy
            try:
                return _merge(self.__wrapped__, value)
            except (TypeError, ValueError) as e:
                raise ConfTypeError(e)

        ##########
        if settings.allowed_types:
            value = conv_type(value)

        if settings.transformer is not None:
            value = transform(value)

        check_modules()

        if settings.mergeable and self.__initialized:
            value = merge(value)

        super().__init__(value)
        self._self_settings = settings


class Conf(DefaultAttrDict):
    '''Holds ConfItems as attributes

    Reassigning an item will merge it with the current one (the newly
    assigned item takes precedence):
        - any settings not explicitly given in the new item will
          inherit its parent
        - if the value can be merged with the parent, it will be
    '''

    __item_type__ = ConfItem  # dictates whether it is mergeable
    __attempt_merge__ = True
