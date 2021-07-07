import logging
from time import time
from awesomedict import AwesomeDict
import mimetypes
from string import Template as StringTemplate
from collections import Mapping

from ..containers import DefaultDict
from ..utils import ReprFromStr, \
    is_str, is_modified_since, read_file, is_map_like
from .exc import TemplateError


logger = logging.getLogger(__name__)
__all__ = [
    'TemplateContainer',
    'Template',
    'TemplateFile',
    'TemplateDirectory',
]


def to_template_or_dir(val):
    if isinstance(val, (Template, TemplateFile, TemplateDirectory)):
        return val
    if is_map_like(val):
        return Template(val)
    return TemplateDirectory(val)


class TemplateBase:
    __init_keys__ = None

    def __init__(self, obj):
        self.__data__ = None
        self.__type__ = None

        if self.__init_keys__ is None:
            raise NotImplementedError('This is a base class')

        for k in self.__init_keys__:
            try:
                setattr(self, k, obj[k])
            except TypeError:
                raise TemplateError(
                    'Template should be instantiated from a dictionary')
            except KeyError as e:
                raise TemplateError(
                    'Template needs the {} key'.format(e))

    @property
    def data(self):
        return self.__data__

    @data.setter
    def data(self, value):
        self.__data__ = value

    @property
    def type(self):
        return self.__type__

    @type.setter
    def type(self, value):
        self.__type__ = value

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
        return self.__class__(
            {k: getattr(self, k) for k in self.__init_keys__})

    def __repr__(self):
        return '{cls}({attrs})'.format(
            cls=self.__class__.__name__,
            attrs=', '.join(['{}={}'.format(k, getattr(self, k))
                             for k in self.__init_keys__]))

    def __str__(self):
        return self.data

class Template(TemplateBase):
    '''A template page of a specific type

    obj: a dictionary with the following keys:
    - data: the literal content
    - type: the Content-Type of the page
    '''

    __init_keys__ = ['data', 'type']

class TemplateFile(TemplateBase):
    '''A template page backed by a file

    obj: a dictionary with the following keys:
    - file: the filename from which to read the content
    - type: (optional) the Content-Type of the page; otherwise guessed
      from the filename

    The file is re-read only if modified since last time of reading
    '''

    __init_keys__ = ['file']

    def __init__(self, obj):
        self.__last_accessed__ = None
        super().__init__(obj)
        if self.type is None:
            self.type = mimetypes.guess_type(self.file)[0]
        if self.type is None:
            raise TemplateError(
                'Cannot guess Content-Type of {}'.format(self.file))

    @property
    def data(self):
        last_ts = self.__last_accessed__
        self.__last_accessed__ = time()
        if last_ts is None or is_modified_since(self.file, last_ts):
            logger.debug('Re-reading template {}'.format(self.file))
            self.data = read_file(self.file)
        return self.__data__

class TemplateDirectory(ReprFromStr, Mapping):
    '''A directory for template files'''

    def __init__(self, directory):
        if not isinstance(directory, str):
            raise ValueError('directory must be a string')
        self.root = directory
        self.__cache__ = {}  # cache

    def __getitem__(self, key):
        return self.__cache__[key]

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
    __transformer__ = to_template_or_dir
