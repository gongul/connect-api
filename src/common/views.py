import enum


class ActionEnum(enum.Enum):
    PARTIAL_UPDATE = 'partial_update'
    UPDATE = 'update'
    LIST = 'list'
    CREATE = 'create'
    RETRIEVE = 'retrieve'
    METADATA = 'metadata'
