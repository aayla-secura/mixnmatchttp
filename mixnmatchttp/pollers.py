import logging
import threading
from uuid import uuid4 as uuid
from wrapt import decorator

from .utils import curr_datetime, to_http_date, http_date_to_datetime
from .containers import DefaultDict


logger = logging.getLogger(__name__)
__all__ = [
    'uses_poller',
    'Poller',
    'TimePoller',
    'PollerContainer',
]


def uses_poller(poller_name):

    @decorator
    def _decorator(wrapped, self, args, kwargs):
        poller = self.pollers[poller_name]
        if poller.type == 'time':
            headers = ('If-Modified-Since', 'If-Unmodified-Since')
        else:
            headers = ('If-None-Match', 'If-Match')
        value = self.headers.get(headers[0])
        accept_on_modified = True
        if value is None:
            value = self.headers.get(headers[1])
            accept_on_modified = False

        if value is not None:
            if self.command in ['GET', 'HEAD']:
                code = 304
            else:
                code = 412
            is_modified_since = poller.is_modified_since(value)
            if (is_modified_since and not accept_on_modified) or \
                    (not is_modified_since and accept_on_modified):
                self.send_response_empty(code)
                return

        return wrapped(*args, **kwargs)

    return _decorator


class PollerBase:
    type = None

    def __init__(self, name=None):
        self.__waiter__ = threading.Condition(threading.Lock())
        self.__closed__ = False
        self.name = name
        if self.type is None:
            raise NotImplementedError(
                '{} is a base class'.format(self.__class__.__name__))
        self.update()

    @property
    def closed(self):
        '''A boolean indicating if the poller has been closed'''

        return self.__closed__

    @property
    def latest(self):
        '''An UUID which is updated on change'''

        return self.__latest__

    @property
    def last_change(self):
        '''A datetime representing the last change time'''

        return self.__last_change__

    def wait(self, timeout=None):
        '''Wait for a change

        Returns the latest tag or None if the poller has been closed
        or a timeout has occurred
        '''

        if self.__closed__:
            return None
        with self.__waiter__:
            old = self.__latest__
            self.__waiter__.wait(timeout=timeout)
        if old == self.__latest__:
            # timed out or was closed
            return None
        return self.__latest__

    def close(self):
        '''Wake up all waiting threads

        From now on, wait will return None
        This method should be called at server shutdown
        '''

        self.__closed__ = True
        self.__notify__()

    def update(self):
        self.__latest__ = self.__new_tag__()
        self.__last_change__ = curr_datetime()
        self.__notify__()

    def is_modified_since(self, tag):
        raise NotImplementedError

    def __notify__(self):
        with self.__waiter__:
            self.__waiter__.notify_all()

    def __new_tag__(self):
        raise NotImplementedError

class Poller(PollerBase):
    '''A poller for ETags and waiters

    Can be used for client caching via If-None-Match or for event
    streaming with wake up notification via a threading.Condition
    - When the update method is called a new UUID is saved in latest
      and all threads waiting for waiter are notified
    '''

    type = 'uuid'

    def __new_tag__(self):
        return str(uuid())

    def is_modified_since(self, tag):
        return self.__latest__ != tag

class TimePoller:
    '''A poller for timestamps and waiters

    Can be used for client caching via If-Modified-Since or for event
    streaming with wake up notification via a threading.Condition
    - When the update method is called a new timestamp is saved in
      latest and all threads waiting for waiter are notified
    '''

    type = 'time'

    def __new_tag__(self):
        return to_http_date(curr_datetime())

    def is_modified_since(self, tag):
        return self.__last_change__ > http_date_to_datetime(tag)

class PollerContainer(DefaultDict):
    '''Transforms to Poller unless already a poller of some type'''

    def __transform__(self, value):
        if isinstance(value, PollerBase):
            return value
        return Poller(value)
