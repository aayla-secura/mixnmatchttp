from .._py2 import *

class ServerError(Exception):
    '''Base class for exceptions raised when there is a server error'''

    pass

class InvalidRequestError(Exception):
    '''Base class for exceptions raised when request is invalid'''

    pass

class PageReadError(Exception):
    '''Base class for exceptions related to request body read'''
    pass

class UnsupportedOperationError(PageReadError):
    '''Exception raised when request body is read more than once'''

    def __init__(self):
        super().__init__(
            'Cannot read body data again, buffer not seekable')

class DecodingError(PageReadError):
    '''Exception raised when cannot decode sent data'''
    pass
