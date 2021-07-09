import logging
import os
from awesomedict import AwesomeDict
import mimetypes
from string import Template as StringTemplate
from collections import Mapping

from .containers import DefaultDict
from .utils import ReprFromStr, curr_timestamp, \
    is_str, is_modified_since, read_file, is_map_like


logger = logging.getLogger(__name__)
__all__ = [
    'Template',
    'TemplateFile',
    'TemplateDirectory',
    'TemplateContainer',
]


class TemplateBase:
    __keys__ = None

    def __init__(self, **kwargs):
        self.__data__ = None
        self.mimetype = None

        if self.__keys__ is None:
            raise NotImplementedError('This is a base class')

        for key, required in self.__keys__.items():
            try:
                setattr(self, key, kwargs.pop(key))
            except KeyError as e:
                if required:
                    raise TypeError(
                        'Template needs the {} key'.format(e))

        if kwargs:
            raise TypeError('Unknown keyword arguments: {}'.format(
                ', '.join(kwargs.keys())))

    @property
    def data(self):
        return self.__data__

    @data.setter
    def data(self, value):
        self.__data__ = value

    def substitute_all(self, **fields):
        return self._substitute(False, fields)

    def substitute(self, **fields):
        return self._substitute(True, fields)

    def _substitute(self, keep_unused, fields):
        if not keep_unused:
            fields = AwesomeDict(fields).set_defaults({'.*': ''})
        new = self.__copy__()
        new.data = StringTemplate(new.data).safe_substitute(fields)
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
        attrs = {}
        for key, required in self.__keys__.items():
            try:
                attrs[key] = getattr(self, key)
            except AttributeError:
                pass
        return self.__class__(**attrs)

    def __repr__(self):
        return '{cls}({attrs})'.format(
            cls=self.__class__.__name__,
            attrs=', '.join(['{}={}'.format(k, getattr(self, k))
                             for k in self.__keys__]))

    def __str__(self):
        return self.data

class Template(TemplateBase):
    '''A template page of a specific mimetype

    obj: a dictionary with the following keys:
    - data: the literal content
    - mimetype: the Content-Type of the page
    '''

    __keys__ = {
        'data': True,
        'mimetype': True,
    }

class TemplateFile(TemplateBase):
    '''A template page backed by a file

    obj: a dictionary with the following keys:
    - file: the filename from which to read the content
    - mimetype: (optional) the Content-Type of the page; otherwise guessed
      from the filename

    The file is re-read only if modified since last time of reading
    '''

    __keys__ = {
        'file': True,
        'data': False,
        'mimetype': False,
    }

    def __init__(self, **kwargs):
        self.__last_accessed__ = None
        super().__init__(**kwargs)
        if self.mimetype is None:
            self.mimetype = mimetypes.guess_type(self.file)[0]
        if self.mimetype is None:
            self.mimetype = 'text/plain'

    @property
    def data(self):
        last_ts = self.__last_accessed__
        if last_ts is None or is_modified_since(self.file, last_ts):
            logger.debug('Re-reading template {}'.format(self.file))
            self.data = read_file(self.file)
        return self.__data__

    @data.setter
    def data(self, value):
        self.__last_accessed__ = curr_timestamp()
        self.__data__ = value

class TemplateDirectory(ReprFromStr, Mapping):
    '''A directory for template files'''

    def __init__(self, directory):
        if not isinstance(directory, str):
            raise ValueError('directory must be a string')
        self.root = directory
        self.__cache__ = {}  # cache

    def __getitem__(self, key):
        try:
            return self.__cache__[key]
        except KeyError:
            t = TemplateFile(file=os.path.join(self.root, key))
            self.__cache__[key] = t
            return t

    def __iter__(self):
        yield from self.__cache__

    def __len__(self):
        return len(self.__cache__)

    def __eq__(self, other):
        if isinstance(other, TemplateDirectory):
            return self.root == other.root
        elif isinstance(other, str):
            return self.root == other
        return NotImplemented

    def __str__(self):
        return self.root

class TemplateContainer(DefaultDict):
    def __transform__(self, value):
        if isinstance(value, (Template, TemplateFile, TemplateDirectory)):
            return value
        if is_map_like(value):
            return Template(**value)
        if isinstance(value, str):
            return TemplateDirectory(value)
        raise ValueError("Can't convert {} to a template".format(value))
