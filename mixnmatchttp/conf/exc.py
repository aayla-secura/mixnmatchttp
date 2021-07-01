class ConfError(Exception):
    pass

class ConfRuntimeError(ConfError, RuntimeError):
    pass

class ConfTypeError(ConfError, TypeError):
    pass

class ConfValueError(ConfError, ValueError):
    pass
