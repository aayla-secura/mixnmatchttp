import logging

from .exc import CacheMemoryError, CacheOverwriteError, \
    PageNotCachedError, PageClearedError


logger = logging.getLogger(__name__)


class Cache:
    __max_size = 2 * 1024 * 1024

    def __init__(self, max_size=None):
        if max_size is not None:
            self.__max_size = max_size
        self.__size = 0
        self.__pages = {}

    def save(self, name, page):
        '''Saves the page to the cache

        name is the alphanumeric identifier
        page is a Template
        '''

        if self.size + len(page.data) > self.max_size:
            raise CacheMemoryError
        try:
            self.__pages[name]
        except KeyError:
            logger.debug('Caching page "{}"'.format(name))
            self.__pages[name] = page
            self.__size += len(page.data)
            logger.debug('Cache size is: {}'.format(self.size))
        else:
            raise CacheOverwriteError

    def get(self, name):
        logger.debug('Trying to get page "{}"'.format(name))
        try:
            page = self.__pages[name]
        except KeyError:
            raise PageNotCachedError
        if page is None:
            raise PageClearedError
        return page

    def clear(self, name=None):
        '''Marks all pages as purged, but remembers page names'''

        try:
            self.__pages[name]
        except KeyError:
            if name is None:
                to_clear = [k for k, v in self.__pages.items()
                            if v is not None]
            else:
                return  # no such cached page
        else:
            to_clear = [name]

        logger.debug('Clearing from cache: {}'.format(
            ', '.join(to_clear)))

        for key in to_clear:
            if self.__pages[key] is not None:
                self.__size -= len(self.__pages[key].data)
            self.__pages[key] = None

        logger.debug('Cache size is: {}'.format(self.size))
        assert self.__size >= 0

    @property
    def max_size(self):
        return self.__max_size

    @property
    def size(self):
        return self.__size
