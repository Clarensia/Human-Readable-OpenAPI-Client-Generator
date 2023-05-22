def convert_type(type: str) -> str:
    """Convert a type from OpenAPI to a python type.
    
    * "integer" -> "int"
    * "string" -> "str"

    :param type: The type in OpenAPI
    :type type: str
    :return: The type in python
    :rtype: str
    """
    match type:
        case "integer":
            return "int"
        case "string":
            return "str"
        case other:
            raise Exception(f"{other} is not a supported type")
