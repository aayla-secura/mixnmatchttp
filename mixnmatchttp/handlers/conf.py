import logging
import importlib
from wrapt import ObjectProxy

from ..types import DictWithDefaults


logger = logging.getLogger(__name__)


class ConfError(Exception):
    pass

class ConfRuntimeError(ConfError, RuntimeError):
    pass

class ConfTypeError(ConfError, TypeError):
    pass

class _NotInitializedError(Exception):
    pass

class Conf:
    '''Holds ConfItems as attributes

    Reassigning an item will merge it with the current one (the newly
    assigned item takes precedence):
        - any settings not explicitly given in the new item will
          inherit its parent
        - if the value can be merged with the parent, it will be
    '''

    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    def update(self, dic=None, /, **kwargs):
        if dic and kwargs:
            raise ValueError(
                ('Keyword arguments cannot be used with a '
                 'positional argument'))
        init = dic or kwargs
        for k in init:
            setattr(self, k, init[k])

    def __iter__(self):
        yield from []

    def __setattr__(self, attr, value):
        try:
            curr = getattr(self, attr)
        except AttributeError:
            pass
        else:
            return curr._ConfItem__update(value)

        if not isinstance(value, ConfItem):
            try:
                value = ConfItem(value)
            except ConfError as e:
                raise ConfError(
                    'Error in config item {name}: {err!s}'.format(
                        name=attr, err=e))

        super().__setattr__(attr, value)

class ConfItem(ObjectProxy):
    def __init__(self, value, /, **settings):
        '''Configuration item - a proxy for its value

        In almost all respects this behaves as the value itself, but
        the settings used determine if/how the value is transformed
        and what other checks are done to make sure it's valid.

        Accepted settings:
        - mergeable: whether the value is to be merged with its
          previous one during an update (see _ConfItem__update method);
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
        self_settings = DictWithDefaults()
        self_settings.setdefaults(
            mergeable=False,
            allowed_types=(),
            transformer=None,
            requires=())
        self_settings.update(settings)
        self.__init(value, self_settings)

    def __getattr__(self, attr):
        # overriding ObjectProxy's __getattr__ which raises ValueError
        # if it hasn't been initialized
        # raise instead a custom exception here so we can rely on
        # catching this case
        if attr == '__wrapped__':
            raise _NotInitializedError(
                'wrapper has not been initialised')
        return getattr(self.__wrapped__, attr)

    def __repr__(self):
        return str(self.__wrapped__)

    @property
    def __initialized(self):
        try:
            self.__wrapped__
        except _NotInitializedError:
            return False
        return True

    def __update(self, other):
        settings = self._self_settings.copy()

        if isinstance(other, ConfItem):
            value = other.__wrapped__
            settings.update(other._self_settings)
        else:
            value = other

        # this must be done after updating the settings
        self.__init(value, settings)

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
            try:
                return _merge(self.__wrapped__, value)
            except (TypeError, ValueError) as e:
                raise ConfTypeError(e)

        ##########
        if settings.allowed_types:
            value = conv_type(value)
        else:
            # default allowed_types is the type of the given value
            settings.setdefaults(
                allowed_types=(value.__class__,))

        if settings.transformer is not None:
            value = transform(value)

        check_modules()

        if settings.mergeable and self.__initialized:
            value = merge(value)

        super().__init__(value)
        self._self_settings = settings