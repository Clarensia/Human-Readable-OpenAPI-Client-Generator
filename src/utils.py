from src.generators.generator_types import Schema


def convert_type(give_type: str) -> str:
    """Convert a type from OpenAPI to a python type.
    
    * "integer" -> "int"
    * "string" -> "str"

    :param give_type: The type in OpenAPI
    :type give_type: str
    :return: The type in python
    :rtype: str
    """
    match give_type:
        case "integer":
            return "int"
        case "string":
            return "str"
        case other:
            raise Exception(f"{other} is not a supported type")

def is_native_python_type(schema_name: str) -> bool:
    """Verify if the given schema name is a native python type.
    
    A native python type is "int", or "str"

    :param schema_name: The name of the schema
    :type schema_name: str
    :return: `True` if the given type name is a Python native type, `False` otherwise
    :rtype: bool
    """
    return schema_name == "int" or schema_name == "str"

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

def add_indent(text: str, indent: int, except_first_line: bool = False) -> str:
    """Add indent spaces after each new lines of text

    :param text: The text that we have to write with multiple lines
    :type text: str
    :param indent: The amount of indentation that we should have
    :type indent: int
    :param except_first_line: If we should not add indent for the first line, default False
    :type except_first_line: bool
    :return: The text with spaces added
    :rtype: str
    """
    indentation = " " * indent
    split_line = text.splitlines()
    if len(split_line) == 0:
        return text
    ret = f"{indentation}{split_line[0]}" if not except_first_line else split_line[0]
    ret += "\n"
    for i in range(1, len(split_line)):
        ret += f"{indentation}{split_line[i]}\n"
    return ret
