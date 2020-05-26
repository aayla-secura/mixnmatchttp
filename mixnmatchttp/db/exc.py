from ..handlers.base import ServerError, InvalidRequestError

class ObjectConversionError(InvalidRequestError, ValueError):
    pass

class ServerDBError(ServerError):
    pass

class MetadataMistmatchError(ServerDBError, RuntimeError):
    pass
