import logging


logger = logging.getLogger(__name__)
__all__ = [
    'DefaultAttrs',
    'DefaultKeys',
    'DefaultDict',
    'DefaultAttrKeys',
    'DefaultAttrDict',
]


class _DefaultsBase:
    '''A container for defaults

    If <name> is not set on the instance, but is in the defaults then
    it can be accessed in the usual way.

    Supported operations:
      in:  To check if an attribute is explicitly set, then use the in
           operator, like <name> in <instance>.
      +:   You can add object A to B and this would return a new
           object with all of A's attributes and defaults in addition
           to B's. B's attributes and defaults override those of A's
      iteration: You can iterate over the attributes; order not
           guaranteed
      len: you can query the number of items added

    Defaults can only be set at instantiation (or using the private
    method __update_single__ but this is subject to change). No public
    methods or attributes are provided by this class to ensure that
    they don't clash with attributes to be set.
    '''
    __data_type__ = dict

    def __init__(self, defaults={}, /, **explicit):
        self.__explicit__ = self.__data_type__()
        self.__default__ = self.__data_type__()
        self.__update__(defaults, **explicit)

    def __update__(self, defaults={}, /, **explicit):
        for e in explicit:
            self.__update_single__(e, explicit[e], True)
        for d in defaults:
            self.__update_single__(d, defaults[d], False)

    def __update_single__(self, name, value, is_explicit):
        '''This is the only method that should modify __explicit__ or
        __default__

        This allows child classes to easily hook into any changes
        to __explicit__ or __default__ and override that behaviour by
        overriding this method alone
        '''

        if is_explicit:
            self.__explicit__[name] = value
        else:
            self.__default__[name] = value

    def __eq__(self, other):
        if not isinstance(other, DefaultAttrs):
            return False
        return self.__explicit__ == other.__explicit__ and \
            self.__default__ == other.__default__

    def __iter__(self):
        yield from self.__explicit__

    def __contains__(self, key):
        return key in self.__explicit__

    def __add__(self, other):
        if self.__class__ is not other.__class__:
            return NotImplemented

        clone = self.__copy__()
        clone.__update__(other.__default__, **other.__explicit__)
        return clone

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        if self.__class__ is not other.__class__:
            return NotImplemented

        self.__update__(other.__default__, **other.__explicit__)
        return self

    def __repr__(self):
        return repr(self.__explicit__)

    def __len__(self):
        return len(self.__explicit__)

    def __copy__(self):
        clone = self.__class__()
        clone.__explicit__ = self.__explicit__.copy()
        clone.__default__ = self.__default__.copy()
        return clone

class DefaultAttrs(_DefaultsBase):
    '''An object with default attributes'''

    def __setattr__(self, name, value):
        if name.startswith('__'):
            super().__setattr__(name, value)
        else:
            self.__update_single__(name, value, True)

    def __getattr__(self, name):
        if name.startswith('__'):
            raise AttributeError(name)

        try:
            try:
                return self.__explicit__[name]
            except KeyError:
                return self.__default__[name]
        except KeyError as e:
            raise AttributeError(e)

class DefaultKeys(_DefaultsBase):
    '''A dictionary with hidden defaults'''

    def __setitem__(self, name, value):
        self.__update_single__(name, value, True)

    def __getitem__(self, name):
        try:
            return self.__explicit__[name]
        except KeyError:
            return self.__default__[name]

class DefaultDict(DefaultKeys):
    '''A dictionary with hidden defaults

    Like DefaultKeys except it provides the following public
    methods:
      setdefault
      setdefaults
      update
      copy
      keys
      values
      items
      defaultkeys
      defaultvalues
      defaultitems
    '''

    def setdefault(self, key, value):
        '''Does not set key explicitly unlike regular dict'''

        self.__default__[key] = value

    def setdefaults(self, **kargs):
        for k in kargs:
            self.setdefault(k, kargs[k])

    def update(self, arg=None, /, **kargs):
        '''Updates the explicitly set and default items

        arg can be a regular dictionary (in which case it updates
        explicitly the object) or another DefaultKeys (in which
        case defaults update defaults and explicitly set items update
        explicitly set items).
        '''

        if arg and kargs:
            raise ValueError(
                ('Keyword arguments cannot be used with a '
                 'positional argument'))
        if isinstance(arg, DefaultAttrs):
            explicit = arg.__explicit__
            defaults = arg.__default__
        else:
            other = arg or kargs
            explicit = self.__explicit__.__class__(other)
            defaults = self.__default__.__class__()

        self.__update__(defaults, **explicit)

    def copy(self):
        return self.__copy__()

    def keys(self):
        yield from self.__explicit__.keys()

    def values(self):
        yield from self.__explicit__.values()

    def items(self):
        yield from self.__explicit__.items()

    def defaultkeys(self):
        yield from self.__default__.keys()

    def defaultvalues(self):
        yield from self.__default__.values()

    def defaultitems(self):
        yield from self.__default__.items()

class DefaultAttrKeys(DefaultAttrs, DefaultKeys):
    pass

class DefaultAttrDict(DefaultAttrs, DefaultDict):
    pass
