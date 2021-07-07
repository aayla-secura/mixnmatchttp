import logging
from awesomedict import AwesomeDict
from string import Template as StringTemplate

from ..containers import DefaultDict
from ..utils import is_str
from .exc import TemplateError


logger = logging.getLogger(__name__)
__all__ = [
    'Templates',
    'TemplatePage',
]


class TemplatePage:
    def __init__(self, obj):
        try:
            self.data = obj['data']
            self.type = obj['type']
        except TypeError:
            raise TemplateError(
                'Template should be instantiated from a dictionary')
        except KeyError as e:
            raise TemplateError(
                'Template needs the {} key'.format(e))

        for i in ['data', 'type']:
            if not is_str(obj[i]):
                raise TemplateError('"{}" should be a string'.format(i))

    def substitute(self, **fields):
        fields = AwesomeDict(fields).set_defaults({'.*': ''})
        new = self.__copy__()
        new.data = StringTemplate(new.data).substitute(fields)
        return new

    def encode(self):
        new = self.__copy__()
        try:
            new.data = new.data.encode('utf-8')
        except UnicodeEncodeError:
            new.data = new.data.encode(
                'utf-8', errors='backslashreplace')
        return new

    def __copy__(self):
        return self.__class__(dict(data=self.data, type=self.type))

    def __repr__(self):
        return '{cls}(data={data}, type={type})'.format(
            cls=self.__class__.__name__,
            data=self.data,
            type=self.type)

    def __str__(self):
        return self.data

class Templates(DefaultDict):
    __item_type__ = TemplatePage
