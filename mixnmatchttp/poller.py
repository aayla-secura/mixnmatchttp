import logging
import threading

from .utils import datetime_from_timestamp
from uuid import uuid4 as uuid


logger = logging.getLogger(__name__)
__all__ = [
    'Poller',
]


class Poller:
    '''A container for ETags and waiters

    Can be used for client caching via If-None-Match or for event
    streaming with wake up notification via a threading.Condition
    - When the update method is called a new ETag is saved in latest
      and all threads waiting for waiter are notified
    '''

    def __init__(self):
        self.__waiter = threading.Condition(threading.Lock())
        self.__closed = False
        self.update()

    @property
    def closed(self):
        '''A boolean indicating if the poller has been closed'''

        return self.__closed

    @property
    def latest(self):
        '''An ETag string (UUID) which is updated on change'''

        return self.__latest

    @property
    def last_change(self):
        '''A datetime representing the last change time'''

        return self.__last_change

    def wait(self, timeout=None):
        '''Wait for a change

        Returns the latest tag or None if the poller has been closed
        or a timeout has occurred
        '''

        if self.__closed:
            return None
        with self.__waiter:
            old = self.__latest
            self.__waiter.wait(timeout=timeout)
        if old == self.__latest:
            # timed out or was closed
            return None
        return self.__latest

    def close(self):
        '''Wake up all waiting threads

        From now on, wait will return None
        This method should be called at server shutdown
        '''

        self.__closed = True
        with self.__waiter:
            self.__waiter.notify_all()

    def update(self):
        self.__last_change = datetime_from_timestamp(
            0, to_utc=False, relative=True)
        self.__latest = str(uuid())
        with self.__waiter:
            self.__waiter.notify_all()

    def is_match(self, tag):
        return self.__latest == tag
