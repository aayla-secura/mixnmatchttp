import logging
import re

from datetime import datetime, tzinfo, timedelta
from datetime import timezone
from dateutil.parser import parse as parse_date


UTCTimeZone = timezone.utc
LocalTimeZone = datetime.now(tz=timezone.utc).astimezone().tzinfo
logger = logging.getLogger(__name__)
__all__ = [
    'is_timestamp_like',
    'curr_timestamp',
    'datetime_to_timestamp',
    'datetime_from_timestamp',
    'date_from_timestamp',
    'datetime_to_str',
    'datetime_from_str',
]


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
        datefmt = re.sub('{{TZ}} +| +{{TZ}}|{{TZ}}', '', datefmt)
    else:
        datefmt = datefmt.replace('{{TZ}}', tzname)
    return dtime.strftime(datefmt)

def datetime_from_str(dstr,
                      datefmt=None,  # '%d %b %Y %H:%M:%S',
                      #  to_utc=True,
                      from_utc=False):
    '''Returns a datetime object from the given string

    - datefmt is the input format used to parse the date; if None,
      then it is guessed
    - If from_utc is True it assumes the time is in UTC, instead of
      local timezone. If datefmt is None and the timezone is
      explicitly given in the string, then this argument is ignored
      and the timezone is guessed from the string
    '''

    if datefmt is None:
        dtime = parse_date(dstr)
    else:
        dtime = datetime.strptime(dstr, datefmt)

    if dtime.tzinfo is None:
        tz = UTCTimeZone if from_utc else LocalTimeZone
        dtime = dtime.replace(tzinfo=tz)
    #  if to_utc:
    #      pass  # XXX TODO
    return dtime
