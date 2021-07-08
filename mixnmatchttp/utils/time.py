import logging
import re

from datetime import datetime, tzinfo, timedelta
import pytz
from dateutil.parser import parse as parse_date, \
    ParserError as DateParserError


UTCTimeZone = pytz.utc
LocalTimeZone = datetime.now().astimezone().tzinfo
logger = logging.getLogger(__name__)
__all__ = [
    'is_time_like',
    'is_timestamp_like',
    'curr_timestamp',
    'curr_datetime',
    'curr_date',
    'datetime_to_timestamp',
    'datetime_from_timestamp',
    'datetime_to_str',
    'datetime_from_str',
    'datetime_to_tz',
    'date_to_timestamp',
    'date_from_timestamp',
    'to_datetime',
    'to_timestamp',
    'http_datetime',
    'http_date',
]


def tz(timezone):
    '''Converts timezone to a datetime.tzinfo object

    timezone can be a string or None in which case local timzone is
    returned.
    '''

    if timezone is None:
        return LocalTimeZone
    if isinstance(timezone, tzinfo):
        return timezone
    if isinstance(timezone, str):
        return pytz.timezone(timezone)
    raise ValueError('Cannot convert {} to a timezone')

def is_time_like(val, datefmt=None):
    '''True if string is a date'''

    try:
        datetime_from_str(val, datefmt=datefmt)
    except (TypeError, ValueError):
        return False
    return True

def is_timestamp_like(val,
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
    The timestamp is assumed to be in seconds and in local timezone.
    '''

    try:
        ts = int(float(val))
    except (TypeError, ValueError):
        return False

    if ts < 0:
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
    return ts < datetime_to_timestamp(dmax)

def curr_timestamp(timezone=None):
    '''Returns the current timestamp (in seconds since epoch)

    - If timezone is given it returns a timestamp in that timezone
      (otherwise in the local timezone)
    '''

    return datetime_to_timestamp(curr_datetime(timezone=timezone))

def curr_datetime(timezone=None):
    '''Current datetime in the given timezone (or local if None)'''

    return datetime.now(tz=tz(timezone))

def curr_date(timezone=None, **kwargs):
    '''Current datetime in the given timezone (or local if None)

    Keyword arguments are those of datetime_to_str
    '''

    return datetime_to_str(curr_datetime(timezone=timezone), **kwargs)

def datetime_to_timestamp(dtime):
    '''Returns the timestamp (in seconds since epoch)'''

    return float(dtime.strftime('%s')) + dtime.microsecond / 1000000

def datetime_from_timestamp(ts,
                            timezone=None,
                            relative=False):
    '''Returns the datetime from a timestamp

    - timezone determines the timzone of the timestamp (if None,
      it is assumed in local timezone).
    - If relative is True, the timestamp is taken to be relative to
      the current timestamp
    '''

    ts = float(ts)  # support strings
    if relative:
        ts += curr_timestamp()
    return datetime.fromtimestamp(ts, tz=tz(timezone))

def datetime_to_str(dtime, datefmt='%a, %d %b %Y %H:%M:%S %Z'):
    '''Returns the formatted datetime

    - datefmt is the format. The default one corresponds to the HTTP
      date specification (as long as the timezone is GMT)
    '''

    return dtime.strftime(datefmt)

def datetime_from_str(dstr, datefmt=None, timezone=None):
    '''Returns a datetime object from the given string

    - datefmt is the input format used to parse the date; if None,
      then it is guessed
    - If timezone is given, then it assumes the time is in that zone
      and the datetime object will have that timezone set. If timezone
      is None, it assumes local timezone. If datefmt is None and the
      timezone is explicitly given in the string, then this argument
      is ignored and the timezone is guessed from the string

    Raises ValueError if dstr cannot be parsed.
    '''

    if datefmt is None:
        try:
            dtime = parse_date(dstr)
        except DateParserError as e:
            raise ValueError(e)
    else:
        dtime = datetime.strptime(dstr, datefmt)

    if dtime.tzinfo is None:
        dtime = dtime.replace(tzinfo=tz(timezone))
    return dtime

def datetime_to_tz(dtime, timezone):
    '''Converts the datetime to the given timezone

    If timezone is None, then a datetime in local timezone is
    returned.
    '''

    return dtime.astimezone(tz=tz(timezone))

def date_to_timestamp(dstr, datefmt=None, timezone=None):
    '''Converts the given date to a timestamp

    - See datetime_from_str for the meaning of datefmt and timezone
    '''

    return datetime_to_timestamp(
        datetime_from_str(dstr, datefmt=datefmt, timezone=timezone))

def date_from_timestamp(ts, **kwargs):
    '''Returns the date from a timestamp

    All keyword arguments of datetime_from_timestamp and
    datetime_to_str are supported.
    '''

    to_str_kwargs = {}
    try:
        to_str_kwargs['datefmt'] = kwargs.pop('datefmt')
    except KeyError:
        pass

    dtime = datetime_from_timestamp(ts, **kwargs)
    return datetime_to_str(dtime, **to_str_kwargs)

def to_datetime(value):
    '''Converts the given value to a datetime

    - If value is an integer or float, it is assumed to be a timestamp
      in the local timezone
    - Otherwise, if it is a datetime, then it is converted to a string
      as per datetime_to_str
    - Otherwise, if it is a string, it is parsed into a datetime and
      its format is guessed
    '''

    if is_timestamp_like(value):
        return datetime_from_timestamp(value)
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return datetime_from_str(value)

def to_timestamp(value):
    '''Converts the given value to a timestamp in local timezone

    value can be a string, integer, float or datetime; see to_datetime
    '''

    return datetime_to_timestamp(
        datetime_to_tz(to_datetime(value), None))

def http_datetime(value):
    '''Converts the given value to an HTTP datetime

    value can be a string, integer, float or datetime; see to_datetime
    '''

    return datetime_to_tz(to_datetime(value), 'GMT')

def http_date(value):
    '''Converts the given value to an HTTP date'''

    return datetime_to_str(
        http_datetime(value),
        datefmt='%a, %d %b %Y %H:%M:%S %Z')
