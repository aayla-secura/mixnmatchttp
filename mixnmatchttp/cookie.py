import logging
import re
from datetime import datetime
from copy import copy

from .containers import CaseInsensitiveOrderedDict
from .conf import ConfItem
from .conf.exc import ConfError
from .containers import DefaultAttrs, DefaultAttrKeys
from .utils import datetime_from_timestamp, datetime_from_str, datetime_to_str


logger = logging.getLogger(__name__)
__all__ = [
    'Cookie',
]


class Expiry:
    def __init__(self, value):
        if isinstance(value, datetime):
            self.value = value
        elif isinstance(value, int):
            self.value = datetime_from_timestamp(value)
        else:
            self.value = datetime_from_str(value)

    def __str__(self):
        return datetime_to_str(
            self.value, datefmt='%a, %d %b %Y %H:%M:%S {{TZ}}')

    def __repr__(self):
        return '{cls}({val})'.format(
            cls=self.__class__.__name__,
            val=self.__str__())

class SameSite:
    def __init__(self, value):
        allowed = ['None', 'Lax', 'Strict']
        value = str(value).capitalize()
        if value not in allowed:
            raise ValueError(
                'SameSite flag must be one of {}'.format(allowed))
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return '{cls}({val})'.format(
            cls=self.__class__.__name__,
            val=self.__str__())

class CookieAttrs(DefaultAttrKeys):
    __container_type__ = CaseInsensitiveOrderedDict
    __item_type__ = ConfItem

    def __init__(self, **explicit):
        super().__init__(
            {
                'Expires': ConfItem(
                    0,
                    allowed_types=(Expiry,)),
                'Max-Age': 0,
                'Domain': '',
                'Path': '/',
                'Secure': False,
                'HttpOnly': False,
                'SameSite': ConfItem(
                    'Lax',
                    allowed_types=(SameSite,)),
            })
        self.__update__(**explicit)

    def __update_single__(self, name, value, is_explicit):
        if is_explicit:
            try:
                ci = self.__get_single__(name, False)[0]
            except KeyError:
                raise ValueError(
                    '{} is not a valid cookie flag'.format(name))
            name = self.__default__.getkey(name)

            if name == 'Expires':
                if value is None:
                    try:
                        self.__delete_single__(name, True)
                    except KeyError:
                        pass
                    return

            ci = copy(ci)
            try:
                ci.__merge__(value)
            except ConfError as e:
                raise ValueError('{} is not a valid {} value'.format(
                    value, name))

        else:
            # defaults should be set by us only, not checking
            ci = value

        super().__update_single__(name, ci, is_explicit)

    def __getitem__(self, name):
        '''Only explicit'''

        return self.__get_single__(name, True)[0]

    def __getattr__(self, name):
        '''Only explicit'''

        if name.startswith('__'):
            raise AttributeError(name)

        try:
            return self.__get_single__(name, True)[0]
        except KeyError as e:
            raise AttributeError(e)

    def __str__(self):
        result = '; '.join([
            '{key}={val}'.format(
                key=key,
                val=self.__get_single__(key, True)[0])
            for key in self.__explicit__
            if key not in ['Secure', 'HttpOnly']
        ])

        for k in ['Secure', 'HttpOnly']:
            try:
                if self[k]:
                    result += '; ' + k
            except KeyError:
                pass
        return result

class Cookie(DefaultAttrs):
    __container_type__ = CookieAttrs

    def __init__(self, name, value='', /, **kwargs):
        object.__setattr__(self, 'name', str(name))
        if not self.name:
            raise ValueError('Cookie name is required')
        object.__setattr__(self, 'value', str(value))
        super().__init__(**kwargs)

    @property
    def attributes(self):
        return self.__explicit__

    def __str__(self):
        return '{name}={value}{sep}{attrs}'.format(
            name=self.name,
            value=self.value,
            sep='; ' if self.attributes else '',
            attrs=self.attributes)

    def __repr__(self):
        return '{cls}({val})'.format(
            cls=self.__class__.__name__,
            val=self.__str__())

    @classmethod
    def parse(cls, value):
        def split(arg, default):
            try:
                k, v = arg.split('=', maxsplit=1)
            except ValueError:
                k = arg
                v = default
            return k, v

        keyval, *attrlst = re.split(' *; *', value)
        name, value = split(keyval, '')
        attrs = {}
        for a in attrlst:
            k, v = split(a, True)
            attrs[k] = v
        return cls(name, value, **attrs)
