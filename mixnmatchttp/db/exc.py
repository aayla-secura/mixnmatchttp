from ..handlers.exc import ServerError, InvalidRequestError

class ObjectConversionError(InvalidRequestError, ValueError):
    pass

class ObjectNotFoundError(ObjectConversionError):
    pass

class ServerDBError(ServerError):
    pass

class MetadataMistmatchError(ServerDBError, RuntimeError):
    pass
