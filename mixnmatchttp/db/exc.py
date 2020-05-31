from ..handlers.exc import ServerError as _ServerError, \
    InvalidRequestError as _InvalidRequestError

class ObjectConversionError(_InvalidRequestError, ValueError):
    pass

class ObjectExistsError(ObjectConversionError):
    pass

class ObjectNotFoundError(ObjectConversionError):
    pass

class ServerDBError(_ServerError):
    pass

class MetadataMistmatchError(ServerDBError, RuntimeError):
    pass
