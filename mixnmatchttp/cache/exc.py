from .._py2 import *

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
