import logging
from copy import copy
import importlib

from ..types import DictRepr
from ..utils import merge


logger = logging.getLogger(__name__)


class Conf(DictRepr):
    '''Holds ConfItems

    Item names that start with _ are ignored, i.e. saved as they are
    without transformation or validation.
    '''

    def __setattr__(self, attr, val):
        if not attr.startswith('_'):
            curr = getattr(self, attr, None)
            new = ConfItem(val, copy_from=curr)
            new.validate(attr)
        else:
            new = val
        super().__setattr__(attr, new)

class ConfItem(DictRepr):
    def __init__(self, item, /, copy_from=None, **settings):
        '''
        If item is an instance of <ConfItem>, then it is basically
        duplicated. Otherwise, if copy_from is given, all settings
        are taken from it. copy_from must be an instance of
        <ConfItem>.

        | item is  | copy_from| result                           |
        | ConfItem | is given |                                  |
        ----------------------------------------------------------
        |     Y    |    Y     | merge copy_from's value if       |
        |          |          | merge_value is used              |
        |          |          | copy_from's settings are ignored |
        |__________|__________|__________________________________|
        |     Y    |    N     | duplicate item                   |
        |__________|__________|__________________________________|
        |     N    |    Y     | use copy_from's settings and     |
        |          |          | merge copy_from's value if       |
        |          |          | merge_value is used              |
        |__________|__________|__________________________________|
        |     N    |    N     | use item as the new value        |

        In any case, any explicitly given settings always take
        precedence.

        Accepted settings:
        - merge_value: whether to merge the new value with the value
          of copy_from (if given); this is valid only for sequences and
          mappings, where concatenation/merging makes sense; default
          is False
        - allowed_types: a list of allowed types for this item;
          default is [<type(new value)>]
        - transformer: a callable which take a single argument, the
          value, and returns a new value to be used; default is None
        - required_modules: a list of modules which are required by
          this item; default is []
        '''

        def __init__(merge_value=False,
                     allowed_types=(),
                     transformer=None,
                     required_modules=[]):
            #  if not allowed_types:
            #      allowed_types = (value.__class__,)
            return locals()

        this_settings = {}
        if copy_from is not None:
            if not isinstance(copy_from, ConfItem):
                raise TypeError('copy_from must be a <ConfItem>')
            this_settings.update(copy_from)

        if isinstance(item, ConfItem):
            this_settings.update(item)
            value = item.value
        else:
            value = item
        this_settings.pop('value', None)

        # easy way to check for unexpected settings and raise the
        # usual exception
        this_settings.update(__init__(**settings))
        super().__init__(this_settings)

        if not self.allowed_types:
            self.allowed_types = (value.__class__,)
        if self.transformer is not None:
            value = self.transformer(value)

        if copy_from is not None:
            if not isinstance(copy_from, ConfItem):
                raise TypeError('copy_from must be a <ConfItem>')
            if self.merge_value:
                value = merge(copy_from.value, value)

        self.value = value

    def validate(self, name=''):
        self._transform_type(name)
        #  self._transform_value(name)
        self._check_modules(name)

    def _transform_type(self, name):
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
                 name=name,
                 type=self.value.__class__.__name__,
                 allowed_types=self.allowed_types))

    #  def _transform_value(self, name):
    #      if self.transformer is None:
    #          return
    #      self.value = self.transformer(self.value)

    def _check_modules(self, name):
        for m in self.required_modules:
            if importlib.util.find_spec(m) is None:
                raise RuntimeError(
                    ('Config item {name} reqiures '
                     'module {module}').format(
                         name=name, module=m))

    def __getattr__(self, attr):
        return getattr(self.value, attr)
