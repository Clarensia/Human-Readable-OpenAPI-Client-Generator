from src.generators.generator_types import Schema


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

def extract_schema_name_from_ref(ref: str) -> str:
    """Extract the schema name from a certain $ref value
    
    For example:
    "#/components/schemas/Exchanges" -> "Exchange"

    :param ref: The $ref value of the schema
    :type ref: str
    :return: The name extracted
    :rtype: str
    """
    return ref.split("/")[-1]
