class DBError(Exception):
    pass

class ObjectConversionError(DBError, ValueError):
    pass

class MetadataMistmatchError(DBError, RuntimeError):
    pass
