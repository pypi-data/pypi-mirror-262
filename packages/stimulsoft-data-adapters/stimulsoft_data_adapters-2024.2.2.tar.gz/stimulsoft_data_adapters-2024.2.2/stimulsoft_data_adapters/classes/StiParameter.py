class StiParameter:
    
    name: str = None
    """The name of the parameter."""

    typeCode: int = None
    """The type code of the parameter."""

    typeName: str = None
    """The type name of the parameter."""

    typeGroup: str = None
    """The type group of the parameter."""

    size: int = None
    """The size of the parameter."""

    value: object = None
    """The value of the parameter. The type of object depends on the type of parameter."""

    def __init__(self, name: str, typeCode: int, typeName: str, typeGroup: str, size: int, value: object):
        self.name = name
        self.typeCode = typeCode
        self.typeName = typeName
        self.typeGroup = typeGroup
        self.size = size
        self.value = value
        