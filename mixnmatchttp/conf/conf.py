import logging
from copy import copy
import importlib

from ..types import DictRepr
from ..utils import merge


logger = logging.getLogger(__name__)


class Conf(DictRepr):
    def __setattr__(self, attr, val):
        try:
            curr = getattr(self, attr)
        except AttributeError:
            curr = None

        setting = val
        if not isinstance(setting, ConfItem):
            if curr is None:
                setting = ConfItem(val)
            else:
                setting = copy(curr)
                setting.value = val

        if not setting.name:
            setting.name = attr
        setting.validate()
        if setting.merge and curr is not None:
            setting = merge(curr, setting)
        super().__setattr__(attr, setting)

class ConfItem:
    def __init__(self, value, copy_from=None, **kargs):
        '''
        If copy_from is given, all settings (other keyword arguments)
        are taken from it. Any explicitly given arguments override the
        setting.

        Accepted keyword arguments:
        - merge: whether to merge the given value with the value of
          copy_from (if given); this is used only for sequences and
          mappings, where concatenation/merging makes sense; default
          is False
        - name: used for logging messages only; default is ''
        - allowed_types: a list of allowed types for this item;
          default is [<type(value)>]
        - transformer: a callable which take a single argument, the
          value, and returns a new value to be used; default is None
        - required_modules: a list of modules which are required by
          this item; default is []
        '''

        def __init__(merge=False,
                     name='',
                     allowed_types=[value.__class__],
                     transformer=None,
                     required_modules=[]):
            return locals()

        self.value = value

        # easy way to check for unexpected kargs and raise the
        # expected exception
        settings = __init__(**kargs)
        if copy_from is not None:
            if not isinstance(copy_from, ConfItem):
                raise TypeError('copy_from must be a <ConfItem>')
            for key in settings:
                if key not in kargs:
                    settings[key] = getattr(copy_from, key)
            if settings['merge']:
                pass
                # TODO

        for k, v in settings.items():
            setattr(self, k, v)

    def validate(self):
        self._transform_type()
        self._transform_value()
        self._check_modules()

    def _transform_type(self):
        if isinstance(self.value, self.allowed_types):
            return
        # try to convert
        for t in self.allowed_types:
            try:
                self.value = t(self.value)
            except (TypeError, ValueError) as e:
                pass
            else:
                return
        raise TypeError(
            ('Error in config item {name}: '
             'Cannot convert {type} to any of {allowed_types}').format(
                 name=self.name,
                 type=self.value.__class__.__name__,
                 allowed_types=self.allowed_types))

    def _transform_value(self):
        if self.transformer is None:
            return
        self.value = self.transformer(self.value)

    def _check_modules(self):
        for m in self.required_modules:
            if importlib.util.find_spec(m) is None:
                raise RuntimeError(
                    ('Config item {name} reqiures '
                     'module {module}').format(
                         name=self.name, module=m))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.value)
