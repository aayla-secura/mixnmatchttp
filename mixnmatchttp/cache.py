#TODO
#  - Multi-thread safety!
#  from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import *
from future import standard_library
standard_library.install_aliases()
import logging

__all__ = [
        'CacheError',
        'PageNotCachedError',
        'PageClearedError',
        'CacheMemoryError',
        'CacheOverwriteError',
        'Cache',
        ]

logger = logging.getLogger(__name__)

######################### EXCEPTIONS ########################

class CacheError(Exception):
    '''Base class for exceptions related to the cache'''
    pass

class PageNotCachedError(CacheError):
    '''Exception raised when a non-existent page is requested'''

    def __init__(self):
        super().__init__('This page has not been cached yet.')

class PageClearedError(CacheError):
    '''Exception raised when a deleted page is requested'''

    def __init__(self):
        super().__init__('This page has been cleared.')

class CacheMemoryError(CacheError):
    '''Exception raised when max data already stored in cache'''

    def __init__(self):
        super().__init__(
            'Cannot save any more pages, call /cache/clear or' +
            '/cache/clear/{page_name}')

class CacheOverwriteError(CacheError):
    '''Exception raised when attempted overwriting of page'''

    def __init__(self):
        super().__init__(
            'Cannot overwrite page, choose a different name')

############################################################

class Cache(object):
    __max_size = 2*1024*1024

    def __init__(self, max_size=None):
        if max_size is not None:
            self.__max_size = max_size
        self.__size = 0
        self.__pages = {}

    def save(self, name, page):
        '''Saves the page to the cache
        
        name is the alphanumeric identifier
        page is a dictionary with the following items:
            - data: the content of the page
            - type: the content type
        '''

        if self.size + len(page['data']) > self.max_size:
            raise CacheMemoryError
        try:
            self.__pages[name]
        except KeyError:
            logger.debug('Caching page "{}"'.format(name))
            self.__pages[name] = page
            self.__size += len(page['data'])
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
                to_clear = [k for k,v in self.__pages.items() \
                        if v is not None]
            else:
                return # no such cached page
        else:
            to_clear = [name]

        logger.debug('Clearing from cache: {}'.format(
            ', '.join(to_clear)))

        for key in to_clear:
            if self.__pages[key] is not None:
                self.__size -= len(self.__pages[key]['data'])
            self.__pages[key] = None

        logger.debug('Cache size is: {}'.format(self.size))
        assert self.__size >= 0

    @property
    def max_size(self):
        return self.__max_size

    @property
    def size(self):
        return self.__size
