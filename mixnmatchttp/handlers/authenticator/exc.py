class AuthError(Exception):
    '''Base class for exceptions related to request body read'''

    pass

class UserAlreadyExistsError(AuthError):
    '''Exception raised when a duplicate user is created'''

    def __init__(self, username):
        super().__init__('User "{}" already exists'.format(username))

class NoSuchUserError(AuthError):
    '''Exception raised when a non-existend user is accessed'''

    def __init__(self, username):
        super().__init__('No such user "{}"'.format(username))

class InvalidUsernameError(AuthError):
    '''Exception raised when an invalid username is created'''

    def __init__(self, username):
        super().__init__('Invalid username "{}"'.format(username))

class BadPasswordError(AuthError):
    '''Exception raised when new password is invalid'''

    def __init__(self, username):
        super().__init__(
            'Choose a stronger password for user "{}"'.format(username))
