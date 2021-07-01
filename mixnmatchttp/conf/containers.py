import logging
from copy import copy, deepcopy

from ..utils import merge, is_mergeable


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

    Items are stored in an object of type given by the class attribute
    __container_type__ (default dict).

    If the class attribute __item_type__ is not None, then items are
    converted to __item_type__.

    If the class attribute __attempt_merge__ is True, then setting
    a new value for an existing item attempts to merge them (if
    applicable).
    '''
    __container_type__ = dict
    __item_type__ = None
    __attempt_merge__ = False

    def __init__(self, defaults={}, /, **explicit):
        self.__explicit__ = self.__container_type__()
        self.__default__ = self.__container_type__()
        self.__update__(defaults, **explicit)

    def __merge__(self, other):
        if isinstance(other, _DefaultsBase):
            self.__update__(other.__default__, **other.__explicit__)
        else:
            self.__update__(**other)

    def __update__(self, defaults={}, /, **explicit):
        for d in defaults:
            self.__update_single__(d, defaults[d], False)
        for e in explicit:
            self.__update_single__(e, explicit[e], True)

    def __get_single__(self, name, is_explicit):
        '''This is the only method that should retrieve items

        If is_explicit is None: searches in both explicit and
        default; otherwise in one or the other

        Returns a tuple of (the found item, was_it_explicit) or raises
        KeyError.
        '''

        if is_explicit is None:
            try:
                return self.__explicit__[name], True
            except KeyError:
                return self.__default__[name], False
        elif is_explicit:
            return self.__explicit__[name], True
        else:
            return self.__default__[name], False

    def __update_single__(self, name, value, is_explicit):
        '''This is the only method that should add/change items

        If is_explicit is None name is required to be present, i.e.
        update the entry (default or explicit); otherwise update or
        set the corresponding explicit or default entry
        '''

        def attempt_merge(curr):
            if not is_mergeable(curr):
                return False
            merge(curr, value, inplace=True)
            return True

        ##########
        if self.__item_type__ and \
                not isinstance(value, self.__item_type__):
            value = self.__item_type__(value)

        curr = None
        try:
            # set is_explicit to True/False if it was None
            curr, is_explicit = \
                self.__get_single__(name, is_explicit)
        except KeyError:
            if is_explicit is None:
                raise

        # merge?
        if curr is not None and self.__attempt_merge__:
            if attempt_merge(curr):
                return  # done

        # set a new one
        assert is_explicit is not None
        if is_explicit:
            self.__explicit__[name] = value
        else:
            self.__default__[name] = value

    def __delete_single__(self, name, is_explicit):
        '''This is the only method that should remove items

        If is_explicit is None it removes it from both explicit and
        default; otherwise from one or the other
        '''

        def _del(d, required):
            try:
                del d[name]
            except KeyError:
                if required:
                    raise

        def _delexp(required):
            _del(self.__explicit__, required)

        def _deldef(required):
            _del(self.__default__, required)

        ##########
        if is_explicit is None:
            try:
                _delexp(True)
            except KeyError:
                # if it wasn't in explicit it must be in default or
                # KeyError
                _deldef(True)
            else:
                # if it was in explicit it can also be in default
                # but don't raise a KeyError
                _deldef(False)
        elif is_explicit:
            _delexp(True)
        else:
            _deldef(True)

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
        clone.__merge__(other)
        return clone

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        if self.__class__ is not other.__class__:
            return NotImplemented

        self.__merge__(other)
        return self

    def __repr__(self):
        return repr(self.__explicit__)

    def __len__(self):
        return len(self.__explicit__)

    def __copy__(self):
        clone = self.__class__()
        clone.__explicit__ = copy(self.__explicit__)
        clone.__default__ = copy(self.__default__)
        return clone

    def __deepcopy__(self, memo=None):
        clone = self.__class__()
        clone.__explicit__ = deepcopy(self.__explicit__)
        clone.__default__ = deepcopy(self.__default__)
        return clone

class DefaultAttrs(_DefaultsBase):
    '''An object with default attributes'''

    def __setattr__(self, name, value):
        if name.startswith('__'):
            super().__setattr__(name, value)
        else:
            self.__update_single__(name, value, True)

    def __delattr__(self, name):
        self.__delete_single__(name, None)

    def __getattr__(self, name):
        if name.startswith('__'):
            raise AttributeError(name)

        try:
            return self.__get_single__(name, None)[0]
        except KeyError as e:
            raise AttributeError(e)

class DefaultKeys(_DefaultsBase):
    '''A dictionary with hidden defaults'''

    def __setitem__(self, name, value):
        self.__update_single__(name, value, True)

    def __delitem__(self, name):
        self.__delete_single__(name, None)

    def __getitem__(self, name):
        return self.__get_single__(name, None)[0]

class DefaultDict(DefaultKeys):
    '''A dictionary with hidden defaults

    Like DefaultKeys except it provides the following public
    methods:
      setdefault
      setdefaults
      update
      get
      pop
      popitem
      clear
      cleardefaults
      clearall
      fromkeys
      copy
      keys
      values
      items
      defaultkeys
      defaultvalues
      defaultitems
      allkeys
      allvalues
      allitems
    '''

    def setdefault(self, key, value):
        '''Does not set key explicitly unlike regular dict'''

        self.__update_single__(key, value, False)

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

    def get(self, *args, **kargs):
        pass  # TODO

    def pop(self, *args, **kargs):
        pass  # TODO

    def popitem(self, *args, **kargs):
        pass  # TODO

    def clear(self):
        pass  # TODO

    def cleardefaults(self):
        pass  # TODO

    def clearall(self):
        pass  # TODO

    def fromkeys(self):
        pass  # TODO

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

    def allkeys(self):
        yield from self.__explicit__.keys()
        yield from self.__default__.keys()

    def allvalues(self):
        yield from self.__explicit__.values()
        yield from self.__default__.values()

    def allitems(self):
        yield from self.__explicit__.items()
        yield from self.__default__.items()

class DefaultAttrKeys(DefaultAttrs, DefaultKeys):
    pass

class DefaultAttrDict(DefaultAttrs, DefaultDict):
    pass
