from ._py2 import *

import os
from contextlib import contextmanager
import re
import string
import random
from collections import UserDict
from ._py2 import _abcoll
import logging
from datetime import datetime, tzinfo, timedelta
try:  # python3
    from datetime import timezone
except ImportError:  # python2
    # taken from
    # https://docs.python.org/2/library/datetime.html#datetime.tzinfo
    import time

    def _get_timezones():
        ZEROTD = timedelta(0)
        STDOFFSET = timedelta(seconds=-time.timezone)
        if time.daylight:
            DSTOFFSET = timedelta(seconds=-time.altzone)
        else:
            DSTOFFSET = STDOFFSET
        DSTDIFF = DSTOFFSET - STDOFFSET

        class UTCTimeZone(tzinfo):
            def utcoffset(self, dt):
                return ZEROTD

            def tzname(self, dt):
                return 'UTC'

            def dst(self, dt):
                return ZEROTD

        class LocalTimeZone(tzinfo):
            def utcoffset(self, dt):
                if self._isdst(dt):
                    return DSTOFFSET
                else:
                    return STDOFFSET

            def dst(self, dt):
                if self._isdst(dt):
                    return DSTDIFF
                else:
                    return ZEROTD

            def tzname(self, dt):
                return time.tzname[self._isdst(dt)]

            def _isdst(self, dt):
                tt = (dt.year, dt.month, dt.day,
                      dt.hour, dt.minute, dt.second,
                      dt.weekday(), 0, 0)
                stamp = time.mktime(tt)
                tt = time.localtime(stamp)
                return tt.tm_isdst > 0

        return UTCTimeZone(), LocalTimeZone()

    UTCTimeZone, LocalTimeZone = _get_timezones()

else:
    UTCTimeZone = timezone.utc
    LocalTimeZone = datetime.now(tz=timezone.utc).astimezone().tzinfo


############################################################
logger = logging.getLogger(__name__)


class DictNoClobber(UserDict, object):
    @staticmethod
    def __update(callback, *args, **kwargs):
        '''Iterates over items in the first argument, then keywords

        Calls callback with two arguments: key, value.'''

        if len(args) > 1:
            raise TypeError(
                'expected at most 1 arguments, got %d' % len(args))
        if args:
            other = args[0]
            if isinstance(other, _abcoll.Mapping):
                for key in other:
                    callback(key, other[key])
            elif hasattr(other, 'keys'):
                for key in other.keys():
                    callback(key, other[key])
            else:
                for key, value in other:
                    callback(key, value)
        for key, value in kwargs.items():
            callback(key, value)

    # python2's UserDict.update does not call __setitem__,
    # __getitem__, etc; so override it here to explicitly access the
    # keys using the [] operator (as python3's UserDict.update does).
    # Also python2's UserDict.update accepts the deprecated dict
    # argument; remove it--this update behaves like python3's
    # UserDict.update
    def update(*args, **kwargs):
        '''Updates using items in the first argument, then keywords'''

        if not args:
            raise TypeError("descriptor 'update' of 'UserDict' "
                            "object needs an argument")
        self = args[0]
        args = args[1:]
        self.__update(self.__setitem__, *args, **kwargs)

    def update_noclob(*args, **kwargs):
        '''Updates without overwriting existing keys'''

        if not args:
            raise TypeError("descriptor 'update' of 'UserDict' "
                            "object needs an argument")
        self = args[0]
        args = args[1:]
        self.__update(self.setdefault, *args, **kwargs)

    def keys(self):
        '''Returns a set-like object providing a view on the keys'''

        try:
            # python2
            return self.data.viewkeys()
        except AttributeError:
            # python3
            return super().keys()

    def values(self):
        '''Returns a set-like object providing a view on the values'''

        try:
            # python2
            return self.data.viewvalues()
        except AttributeError:
            # python3
            return super().values()

    def items(self):
        '''Returns a set-like object providing a view on the items'''

        try:
            # python2
            return self.data.viewitems()
        except AttributeError:
            # python3
            return super().items()


def to_bool(val):
    '''Converts val to a boolean. val can be numeric or a string

    If None it is False.
    If numeric, 0 is False, 1 is True and otherwise ValueError is
    raised.
    If a string, "1", "yes" or "true" is True; "", "0", "no" or
    "false" is False and otherwise ValueError is raised. Comparison is
    case-insensitive.
    '''

    if not is_bool_like(val):
        raise ValueError('{} is not a boolean'.format(val))
    if (is_str(val) and val.lower() in ['1', 'yes', 'true']) \
            or val == 1:
        return True
    return False

def is_bool_like(val):
    if is_str(val):
        return val.lower() in [
            '1', 'yes', 'true', '', '0', 'no', 'false']
    return val in [None, 0, 1]

def is_str(val):
    '''True if val is a string (including unicode or bytes)'''

    try:  # python2
        str_types = (basestring,)
    except NameError:  # python3
        str_types = (str, bytes)
    return isinstance(val, str_types)

def is_str_like(val):
    '''True if val can be converted to string straightforwardly

    i.e. if it's a string, boolean or int
    '''

    return is_str(val) or isinstance(val, (int, float, bool))

def is_seq_like(val):
    '''True if val is an iterable (but not a string, or dict)

    i.e. if it's a list, set, tuple, or some mutable sequence
    '''

    return isinstance(val, _abcoll.Iterable) \
        and not is_str_like(val) \
        and not is_map_like(val)

def is_map_like(val):
    '''True if val is like a dict (mapping)'''

    # in python2 UserDict is not a child of Mapping
    return isinstance(val, (_abcoll.Mapping, UserDict))

def is_time_like(val,
                 years_ahead=10,
                 months_ahead=0,
                 days_ahead=0,
                 hours_ahead=0,
                 minutes_ahead=0,
                 seconds_ahead=0,
                 microseconds_ahead=0):
    '''True if val is like a timestamp

    I.e. if non-negative number up to the current timestamp + the
    future time given by the *_ahead arguments.
    The timestamp is assumed to be in local timezone.
    '''

    try:
        ts = int(float(val))
    except (TypeError, ValueError):
        return False
    now = datetime_from_timestamp(0, relative=True)
    dmax = datetime(
        year=now.year + years_ahead,
        month=now.month + months_ahead,
        day=now.day + days_ahead,
        hour=now.hour + hours_ahead,
        minute=now.minute + minutes_ahead,
        second=now.second + seconds_ahead,
        microsecond=now.microsecond + microseconds_ahead,
        tzinfo=now.tzinfo)
    return (ts >= 0 and (
        ts < datetime_to_timestamp(dmax, to_utc=False)
        or ts < datetime_to_timestamp(
            dmax, to_utc=False, to_ms=True)))

def str_remove_chars(s, skip):
    try:  # python2
        return s.translate(None, skip)
    except TypeError:  # python3
        return s.translate(str.maketrans(dict.fromkeys(skip)))

def str_trunc(s, size):
    if len(s) <= size:
        return s
    if isinstance(s, bytes):
        suff = b'...'
    else:
        suff = '...'
    return s[:size - 3] + suff

def str_to_hex(s):
    try:  # python3
        return s.hex()
    except AttributeError:  # python2
        return s.encode('hex')

def hex_to_bytes(s):
    try:  # python3
        return bytes.fromhex(s)
    except AttributeError:  # python2
        return s.decode('hex')

def int_to_hex(i):
    h = '{:x}'.format(i)
    if len(h) % 2 != 0:
        h = '0' + h
    return h

def int_to_bytes(i):
    return hex_to_bytes(int_to_hex(i))

def randhex(size):
    '''Returns a random hex string of length size

    The number of random bytes will be int(size / 2).
    Read from urandom.
    '''

    return str_to_hex(os.urandom(int(size / 2)))

def randstr(size,
            use_lower=True,
            use_upper=True,
            use_digit=True,
            use_punct=True,
            skip=''):
    '''Returns a random string of length size

    The string consists of letters, digits and punctuation excluding
    any characters given in skip.
    '''

    alphabet = ''
    if use_lower:
        alphabet += string.ascii_lowercase
    if use_upper:
        alphabet += string.ascii_uppercase
    if use_digit:
        alphabet += string.digits
    if use_punct:
        alphabet += string.punctuation
    if skip:
        alphabet = str_remove_chars(alphabet, skip)
    return ''.join([random.choice(alphabet) for i in range(size)])

def abspath(path):
    '''Canonicalize the path segment by segment

    Leading slash is preserved if present, but is not required.
    '''

    if not path:
        return ''

    # if path doesn't start with /, temporarily add it so that
    prefix = ''
    if path[0] != '/':
        prefix = '/'
    # os.path.abspath doesn't prepend cwd
    # os.path.abspath preserves two consecutive slashes at the
    # beginning, since they may indicate a URI with a default
    # protocol; we explicitly remove them here
    return os.path.abspath(prefix + path).replace(
        '//', '/')[len(prefix):]

def iter_abspath_up_to_nth(path, n=1, join=False):
    '''Canonicalize the path up to the first n segments

    Leading slash is preserved if present, but is not required.
    Returns a generator for a list of canonicalized versions of path
    up to the first n segments, followed by the rest of the segments.
    For example /../foo/../bar/./baz/./ will result in
    [('/foo', '../bar/./baz/./'), ('/bar', './baz/./'),
     ('/bar', 'baz/./')]
    for n=1, and [('/bar/baz', './'), ('/bar/baz', '')] for n=2. If we
    never reach n segments, nothing is yielded.

    If join is True, the canonicalized part (with n segments) and the
    rest is joined. This will result in ['/bar/baz/./', '/bar/baz']
    for n=2.
    '''

    if not path:
        return

    if n <= 0:
        raise ValueError('Number of path segments must be positive')

    # temporarily add a trailing /
    pathlen = len(path)
    if path[-1] != '/':
        path += '/'

    curr_index = skip = path.find('/')
    root = path[: skip if skip != -1 else None]
    while skip != -1:
        curr_abs = abspath(path[:curr_index])
        curr_abs_parts = list(filter(None, curr_abs.split('/')))
        # filter because leading or trailing / will result in ''
        # items
        if len(curr_abs_parts) == n:
            if join:
                yield '/'.join(filter(
                    None, [curr_abs, path[curr_index + 1:pathlen]]))
            else:
                yield curr_abs, path[curr_index + 1:pathlen]
        skip = path[curr_index + 1:].find('/')
        curr_index += skip + 1

def iter_abspath(path, start_n=1, join=False):
    '''Canonicalize the path segment by segment

    Returns a generator for a list of iter_abspath_up_to_nth results
    for all n's starting at start_n.
    '''

    while True:
        done = True
        for result in iter_abspath_up_to_nth(path, start_n):
            done = False
            yield result
        if done:
            return
        start_n += 1

def param_dict(s,
               itemsep=' *; *',
               valsep='=',
               values_are_opt=False,
               decoder=None):
    '''Returns a dictionary of keys/values from the string s

    itemsep: regex for separating items
    valsep: literal string for separating key/value
    decoder: a callable to decode keys and values
    '''

    def _id(o):
        return o

    if s is None:
        return {}

    if decoder is None:
        decoder = _id
    params = dict()
    sepfunc = lambda x: x.split(valsep)
    if values_are_opt:
        sepfunc = lambda x: x.partition(valsep)[0::2]

    try:
        params = {decoder(k): decoder(v) for k, v in [
            sepfunc(v) for v in re.split(itemsep, s)]}
    except ValueError:
        pass

    logger.debug('Got params from {}: {}'.format(s, params))
    return params

def curr_timestamp(to_utc=True, to_ms=False):
    '''Returns the current timestamp (in seconds since epoch)

    - If to_utc is True it returns a timestamp in UTC timezone
      (otherwise in the local timezone)
    - If to_ms is True, then the timestamp is returned in milliseconds
    '''

    tz = UTCTimeZone if to_utc else LocalTimeZone
    return datetime_to_timestamp(
        datetime.now(tz=tz), to_utc=to_utc, to_ms=to_ms)

def datetime_to_timestamp(dtime, to_utc=True, to_ms=False):
    '''Returns the timestamp (in seconds since epoch)

    - If to_utc is True it returns the timestamp in UTC time,
      otherwise in local time (if dtime is not timezone aware, we
      assume it's in the local timezone)
    - If to_ms is True, then the timestamp is returned in milliseconds
    '''

    local_offset = datetime.now(tz=LocalTimeZone).utcoffset()
    dtime_offset = dtime.utcoffset()
    if dtime_offset is None:
        dtime_offset = local_offset
    if to_utc:
        offset = -dtime_offset
    else:
        offset = -dtime_offset + local_offset
    ts = float(dtime.strftime('%s')) + offset.total_seconds()
    if to_ms:
        ts = ts * 1000 + dtime.microsecond / 1000
    return ts

def datetime_from_timestamp(ts,
                            from_ms=False,
                            to_utc=True,
                            from_utc=False,
                            relative=False):
    '''Returns the datetime from a timestamp

    - If relative is True, the current timestamp is added
    - from_utc determines if the timestamp is in UTC time; it's
      ignored if relative is True.
    - If to_utc is True it returns a datetime in UTC timezone
      (otherwise in the local timezone)
    - If from_ms is True, then the timestamp should be in milliseconds
    '''

    ts = float(ts)  # support strings
    if from_ms:
        ts /= 1000
    if relative:
        ts += curr_timestamp(to_utc=False)
    # XXX don't ignore from_utc if relative is True
    elif from_utc:
        ts += datetime.now(
            tz=LocalTimeZone).utcoffset().total_seconds()
    tz = UTCTimeZone if to_utc else LocalTimeZone
    return datetime.fromtimestamp(ts, tz=tz)

def date_from_timestamp(ts,
                        from_ms=False,
                        to_utc=True,
                        from_utc=False,
                        datefmt='%a, %d %b %Y %H:%M:%S {{TZ}}',
                        relative=False):
    '''Returns the date from a timestamp

    - If relative is True, the current timestamp is added
    - from_utc determines if the timestamp is in UTC time; it's
      ignored if relative is True.
    - If to_utc is True it returns a date in UTC timezone
      (otherwise in the local timezone)
    - datefmt is the format; {{TZ}} is replaced by the timzone's name
    - If from_ms is True, then the timestamp should be in milliseconds
    '''

    dtime = datetime_from_timestamp(
        ts,
        from_ms=from_ms,
        to_utc=to_utc,
        from_utc=from_utc,
        relative=relative)
    datefmt = datefmt.replace('{{TZ}}', dtime.tzname())
    return dtime.strftime(datefmt)

def datetime_to_str(dtime, datefmt='%a, %d %b %Y %H:%M:%S {{TZ}}'):
    '''Returns the formatted datetime'''

    tzname = dtime.tzname()
    if tzname is None:
        datefmt = datefmt.replace(' {{TZ}}', '').replace('{{TZ}}', '')
    else:
        datefmt = datefmt.replace('{{TZ}}', tzname)
    return dtime.strftime(datefmt)

def datetime_from_str(dstr,
                      datefmt='%d %b %Y %H:%M:%S',
                      #  to_utc=True,
                      from_utc=False):
    '''Returns a datetime object from the given string

    - If from_utc is True it assumes the time is in UTC
      (otherwise in the local timezone)
    '''

    tz = UTCTimeZone if from_utc else LocalTimeZone
    dtime = datetime.strptime(dstr, datefmt).replace(tzinfo=tz)
    #  if to_utc:
    #      pass  # XXX TODO
    return dtime


@contextmanager
def open_path(path, mode='r'):
    if hasattr(path, 'read'):
        filename = getattr(path, 'name', None)
        fd = path
        needs_closing = False
        logger.debug('Using open file {}'.format(filename))
    else:
        filename = path
        fd = open(path, mode)
        needs_closing = True
        logger.debug('Opened file {}'.format(filename))
    try:
        yield fd, filename
    finally:
        if needs_closing:
            fd.close()
            logger.debug('Closed file {}'.format(filename))

def read_file(path, mode='r'):
    with open_path(path, mode=mode) as (fd, filename):
        logger.debug('Reading file {}'.format(filename))
        return fd.read()
