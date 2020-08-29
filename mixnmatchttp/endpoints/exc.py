class EndpointError(Exception):
    '''Base class for exceptions related creation of endpoints'''

    pass

class EndpointParseError(Exception):
    '''Base class for exceptions related parsing of endpoints'''

    pass

class NotAnEndpointError(EndpointParseError):
    '''Exception raised when the root path is unknown'''

    def __init__(self, root):
        super().__init__('{} is not special.'.format(root))

class MethodNotAllowedError(EndpointParseError):
    '''Exception raised when the request method is not allowed

    Will have an "allowed_methods" attribute containing a set of
    allowed HTTP methods for this endpoint.
    '''

    def __init__(self, allowed_methods):
        self.allowed_methods = allowed_methods
        super().__init__('Method not allowed.')

class MissingArgsError(EndpointParseError):
    '''Exception raised when a required argument is not given'''

    def __init__(self):
        super().__init__('Missing required argument.')

class ExtraArgsError(EndpointParseError):
    '''Exception raised when extra arguments are given'''

    def __init__(self, nargs):
        super().__init__('Extra arguments: {}.'.format(nargs))
