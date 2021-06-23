import logging


logger = logging.getLogger(__name__)
__all__ = [
    'ObjectWithDefaults',
    'ObjectDictWithDefaults',
]


class ObjectWithDefaults:
    '''An object with default attributes

    If <attr> is not set on the instance, but is in the defaults then
    it can be accessed in the usual way.

    Attributes can also be accessed as keys

    Supported operations:
      in:  To check if an attribute is explicitly set, then use the in
           operator, like <attr> in <instance>.
      +:   You can add object A to B and this would return a new
           object with all of A's attributes and defaults in addition
           to B's. B's attributes and defaults override those of A's
      iteration: You can iterate over the attributes; order not
           guaranteed
      indexing: you can set and get attributes as you do dictionary
           keys
      len: you can query the number of items added

    Defaults can only be set at instantiation (or using the private
    attribute __defaults__ but this is subject to change). No public
    methods or attributes are provided by this class to ensure that
    they don't clash with attributes to be set.
    '''

    __data_type__ = dict

    def __init__(self, defaults={}, /, **explicit):
        self.__explicit__ = self.__data_type__()
        self.__defaults__ = self.__data_type__()
        self.__additems__(defaults, **explicit)

    def __additems__(self, defaults={}, /, **explicit):
        for e in explicit:
            self.__setitem__(e, explicit[e])
        for d in defaults:
            self.__setdefaultitem__(d, defaults[d])

    def __setitem__(self, attr, value):
        '''This is the only method that should modify __explicit__

        This allows child classes to easily hook into any changes
        to __explicit__ and override that behaviour by overriding this
        method alone
        '''

        self.__explicit__[attr] = value

    def __setdefaultitem__(self, attr, value):
        '''This is the only method that should modify __defaults__

        This allows child classes to easily hook into any changes
        to __defaults__ and override that behaviour by overriding this
        method alone
        '''

        self.__defaults__[attr] = value

    def __getitem__(self, attr):
        try:
            return self.__explicit__[attr]
        except KeyError:
            return self.__defaults__[attr]

    def __setattr__(self, attr, value):
        if attr.startswith('__'):
            super().__setattr__(attr, value)
        else:
            self.__setitem__(attr, value)

    def __getattr__(self, attr):
        if attr.startswith('__'):
            raise AttributeError(attr)

        try:
            return self.__getitem__(attr)
        except KeyError as e:
            raise AttributeError(e)

    def __eq__(self, other):
        if not isinstance(other, ObjectWithDefaults):
            return False
        return self.__explicit__ == other.__explicit__ and \
            self.__defaults__ == other.__defaults__

    def __iter__(self):
        yield from self.__explicit__

    def __contains__(self, key):
        return key in self.__explicit__

    def __add__(self, other):
        if self.__class__ is not other.__class__:
            return NotImplemented

        clone = self.__copy__()
        clone.__additems__(other.__defaults__, **other.__explicit__)
        return clone

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        if self.__class__ is not other.__class__:
            return NotImplemented

        self.__additems__(other.__defaults__, **other.__explicit__)
        return self

    def __repr__(self):
        return repr(self.__explicit__)

    def __len__(self):
        return len(self.__explicit__)

    def __copy__(self):
        clone = self.__class__()
        clone.__explicit__ = self.__explicit__.copy()
        clone.__defaults__ = self.__defaults__.copy()
        return clone

class ObjectDictWithDefaults(ObjectWithDefaults):
    '''A dictionary with hidden defaults

    Like ObjectWithDefaults except it provides the following public
    methods:
      setdefault
      setdefaults
      update

    Same key--attribute correspondence as ObjectWithDefaults, however,
    set keys can only be accessed as attributes if they are not the
    same as any of the available methods.

    Defaults can be set during instantiation (the only positional
    argument) or using the setdefault or setdefaults methods.
    The setdefault method does not explicitly set the item as is the
    case for regular dictionaries.
    '''

    def setdefault(self, key, value):
        self.__defaults__[key] = value

    def setdefaults(self, **kargs):
        for k in kargs:
            self.setdefault(k, kargs[k])

    def update(self, arg=None, /, **kargs):
        '''Updates the explicitly set and default items'''

        if arg and kargs:
            raise ValueError(
                ('Keyword arguments cannot be used with a '
                 'positional argument'))
        other = arg or kargs
        if isinstance(other, ObjectWithDefaults):
            explicit = other.__explicit__
            defaults = other.__defaults__
        else:
            explicit = self.__explicit__.__class__(other)
            defaults = self.__defaults__.__class__()

        self.__additems__(defaults, **explicit)
