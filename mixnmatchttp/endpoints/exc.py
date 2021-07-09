class EndpointError(Exception):
    '''Base class for exceptions related creation of endpoints'''

    pass

class EndpointParseError(Exception):
    '''Base class for exceptions related parsing of endpoints'''

    pass

class NotAnEndpointError(EndpointParseError):
    '''Exception raised when the root path is unknown'''

    def __init__(self, root):
        super().__init__('{} is not special'.format(root))

class MethodNotAllowedError(EndpointParseError):
    '''Exception raised when the request method is not allowed

    Will have an "allow" attribute containing a set of
    allowed HTTP methods for this endpoint.
    '''

    def __init__(self, allow):
        self.allow = allow
        super().__init__('Method not allowed')

class MissingArgsError(EndpointParseError):
    '''Exception raised when a required argument is not given'''

    def __init__(self, nargs=None):
        super().__init__(
            '{n} missing required argument{suffix}'.format(
                n=nargs if nargs else 'At least one',
                suffix='' if nargs is not None and nargs == 1 else 's'))

class ExtraArgsError(EndpointParseError):
    '''Exception raised when extra arguments are given'''

    def __init__(self, extra_args):
        nargs = len(extra_args)
        super().__init__(
            '{n} extra argument{suffix}: {extra}'.format(
                n=nargs,
                suffix='' if nargs == 1 else 's',
                extra='/'.join(extra_args)))
