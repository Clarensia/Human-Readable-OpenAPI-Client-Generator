import json
import os

from typing import Any, Dict, List

from src.generators.generator_types import Property, Schema


class ModelGenerator:
    '''Create a model from the given shemas from OpenAPI.
    
    We call this model, because they are more high level data structure
    than schemas.
    
    If the schema contains "Error" in his name, we write the
    model inside of "Exceptions" instead.
    
    Here is an example of input and ouput for a schema:
    Input schema:
    "AmountIn": {
        "title": "AmountIn",
        "type": "object",
        "properties": {
            "blockchain": {
                "title": "Blockchain",
                "type": "string",
                "description": "The id of blockchain on which the exchange is taking place"
            },
            "exchange": {
                "title": "Exchange",
                "type": "string",
                "description": "The id of the exchange used for this trade"
            },
            "tokenIn": {
                "title": "Tokenin",
                "type": "string",
                "description": "The address of the token that you sell"
            },
            "tokenOut": {
                "title": "Tokenout",
                "type": "string",
                "description": "The address of the token that you buy"
            },
            "amountOut": {
                "title": "Amountout",
                "type": "integer",
                "description": "The amount of token1 that you wish to buy"
            },
            "amountIn": {
                "title": "Amountin",
                "type": "integer",
                "description": "The amount of token0 that you have to sell in order to get amountOut token1"
            }
        },
        "example": {
            "blockchain": "avalanche",
            "exchange": "lydia_finance_avalanche",
            "tokenIn": "0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7",
            "tokenOut": "0xde3A24028580884448a5397872046a019649b084",
            "amountIn": 843047442340946,
            "amountOut": 10000
        }
    }
    
    Here is the resulting file:
    ```python
    from dataclasses import dataclass


    @dataclass(slots=True, frozen=True)
    class AmountIn:
        """The AmountIn model"""

        blockchain: str
        """The id of blockchain on which the exchange is taking place
        
        example: "avalanche"
        """
        exchange: str
        """The id of the exchange used for this trade
        
        example: "lydia_finance_avalanche"
        """
        tokenIn: str
        """The address of the token that you sell
        
        example: "0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7"
        """
        tokenOut: str
        """The address of the token that you buy
        
        example: "0xde3A24028580884448a5397872046a019649b084"
        """
        amountIn: str
        """The amount of tokenIn that you have to sell in order to get amountOut tokenOut
        
        example: 843047442340946
        """
        amountOut: str
        """The amount of tokenOut that you wish to buy
        
        example: 10000
        """

        def __init__(self, blockchain: str, exchange: str, tokenIn: str, tokenOut: str, amountIn: str, amountOut: str, **_):
            """Instantiate an AmountIn model

            :param blockchain: The id of blockchain on which the exchange is taking place
            :type blockchain: str
            :param exchange: The id of the exchange used for this trade
            :type exchange: str
            :param tokenIn: The address of the token that you sell
            :type tokenIn: str
            :param tokenOut: The address of the token that you buy
            :type tokenOut: str
            :param amountIn: The amount of tokenIn that you have to sell in order to get amountOut tokenOut
            :type amountIn: str
            :param amountOut: The amount of tokenOut that you wish to buy
            :type amountOut: str
            """
            self.blockchain = blockchain
            self.exchange = exchange
            self.tokenIn = tokenIn
            self.tokenOut = tokenOut
            self.amountIn = amountIn
            self.amountOut = amountOut
    ```
    
    We create a custom constructor, because the API might be updated and return more fields. If the API got an update
    and return more fields, we want the user client to still work. So we generate a custom constructor in order to
    ignore additional fields.
    
    Additionaly, the dataclass generated is using slots=True, slots allow a faster access to the data for the user.
    We also use froze=True inside of the dataclasse because it is a returned value from the API, modifying any field
    from the returned value is a misstake.
    '''
    
    _models_path: str
    """The path to the model folder"""
    _exceptions_path: str
    """The path to the exception folder"""
    
    def __init__(self, models_path: str, exceptions_path: str):
        self._models_path = models_path
        self._exceptions_path = exceptions_path

    def _has_array(self, properties: Dict[str, Property]) -> bool:
        for property_name in properties:
            if properties[property_name]["type"] == "array":
                return True

        return False

    def _has_decimals(self, properties: Dict[str, Property]) -> str:
        for property_name in properties:
            if properties[property_name]["type"] == "number":
                return True

        return False

    def _get_array_type(self, _property: Property) -> str:
        """For a given property of type "array", it will give the type of the array.
        
        A property of type "array" will usually look like this:
        {
            title: "Data",
            type: "array",
            items: {
                "$ref": "#/components/schemas/Exchange"
            },
            description: "The list of exchanges"
        }
        
        To get the type of the array, we go to _property["items"]["$ref"] and take
        the word after the last "/", here, it will be "Exchange"

        :param _property: The property that has the array type. (We must _property because
                          property is a reserved keyword in Python)
        :type _property: Property
        :return: The name of the type of the array
        :rtype: str
        """
        if _property["type"] != "array":
            raise Exception("ModelGenerator: _get_array_type: Called _get_array_type with a type that is not \"array\":", _property["type"])
        ref = _property["items"]["$ref"]
        return ref.split("/")[-1]

    def _get_array_types(self, properties: Dict[str, Property]) -> List[str]:
        """For a dictionary of properties, it will get all the types of the arrays.
        
        This is required for the dataclass, because if a dataclass has a list, we must import
        the type of the list

        :param properties: The dictionary containing as key the name of the property and as
                           value the Property object.
        :type properties: Dict[str, Property]
        """
        ret = []
        for property_name in properties:
            _property = properties[property_name]
            if _property["type"] == "array":
                ret.append(self._get_array_type(_property))
        return ret

    def _add_special_imports(self, properties: Dict[str, Property]) -> str:
        """Some fields require some special imports:
        List
        Decimals
        Other models
        
        This method allow us to detect which imports are required and add
        them.
        
        For example, if we detect a "number" type in one of the properties fields,
        we add: from decimal import Decimal
        
        We use "Decimal" for the number type because it is more precise.

        :param properties: The properties that we have for the program
        :type properties: Dict[str, Property]
        :return: Some added imports when necessary
        :rtype: str
        """
        ret = ""
        if self._has_decimals(properties):
            ret += "from decimal import Decimal\n"
        if self._has_array(properties):
            array_types = self._get_array_types(properties)
            ret += "from typing import List\n"
            for array_type in array_types:
                ret += f"from models.{array_type} import {array_type}\n"
        return ret

    def _add_first_lines(self, model_name: str, properties: Dict[str, Property]) -> str:
        ret = "from dataclasses import dataclass\n"
        ret += self._add_special_imports(properties)
        ret += f'''

@dataclass(slots=True, frozen=True)
class {model_name}:
    """The {model_name} model"""

'''
        return ret
        

    def _add_property(self, property_name: str, _property: Property, example: Any) -> str:
        ret = ""
        match _property["type"]:
            case "string":
               ret += f"    {property_name}: str\n"
               ret += '    """' + _property["description"] + "\n"
               ret += f'\n    Example: "{example}"\n'
               ret += '    """\n\n'
            case "integer":
                ret += f"    {property_name}: int\n"
                ret += '    """' + _property["description"] + "\n"
                ret += f'\n    Example: {example}\n'
                ret += '    """\n\n'
            case "array":
                array_type = self._get_array_type(_property)
                ret += f"    {property_name}: List[" + array_type + "]\n"
                ret += '    """' + _property["description"] + "\n"
                ret += "\n    Example:\n"
                ret += json.dumps(example, indent=4)
                ret += '    """\n\n'
            case "number":
                ret += f"    {property_name}: Decimal\n"
                ret += '    """' + _property["description"] + "\n"
                ret += f'\n    Example: Decimal({example})\n'
                ret += '    """\n\n'
            case _:
                raise Exception(f'The generator does not support the type {_property["type"]} please open an issue on: https://github.com/Clarensia/Human-Readable-OpenAPI-Client-Generator/issues')
        return ret

    def _create_constructor_doc_field(self, property_name: str, _property: Property):
        ret = f'        :param {property_name}: {_property["description"]}\n'
        match _property["type"]:
            case "string":
                ret += f'        :type {property_name}: str\n'
            case "integer":
                ret += f'        :type {property_name}: int\n'
            case "array":
                array_type = self._get_array_type(_property)
                ret += f'        :type {property_name}: List[{array_type}]\n'
            case "number":
                ret += f'        :type {property_name}: Decimal\n'
            case _:
                raise Exception(f'The generator does not support the type {_property["type"]} please open an issue on: https://github.com/Clarensia/Human-Readable-OpenAPI-Client-Generator/issues')
        return ret

    def _add_constructor(self, schema_name: str, schema: Schema) -> str:
        ret = ""
        ret += "    def __init__(self"
        for property_name in schema["properties"]:
            ret += ", "
            ret += property_name
            match schema["properties"][property_name]["type"]:
                case "string":
                    ret += ": str"
                case "integer":
                    ret += ": int"
                case "array":
                    array_type = self._get_array_type(schema["properties"][property_name])
                    ret += f": List[{array_type}]"
                case "number":
                    ret += f': Decimal'
                case _:
                    raise Exception(f'The generator does not support the type {schema["properties"][property_name]["type"]} please open an issue on: https://github.com/Clarensia/Human-Readable-OpenAPI-Client-Generator/issues')
        ret += "**_):\n"
        ret += f'        """Instantiate an {schema_name} model\n\n'
        for property_name in schema["properties"]:
            ret += self._create_constructor_doc_field(property_name, schema["properties"][property_name])
        ret += '        """\n'
        for property_name in schema["properties"]:
            ret += f'        self.{property_name} = {property_name}\n'
        return ret

    def _write_model(self, model_name: str, model_text: str):
        with open(os.path.join(self._models_path, model_name + ".py"), "w+") as f:
            f.write(model_text)

    def build_models(self, schemas: Dict[str, Schema]):
        """Build the schemas and write them inside of the model folder.
        
        If the given shema is an exception, it writes it inside of "exceptions"

        :param schemas: The dictionary containing as key the schema id and as value the
                        schema object that we have to create
        :type schemas: Dict[str, Schema]
        """
        for schema_name in schemas:
            # We will handle errors later
            if "Error" in schema_name:
                continue
            schema = schemas[schema_name]
            to_write = ""
            to_write += self._add_first_lines(schema_name, schema["properties"])
            for property_name in schema["properties"]:
                _property = schema["properties"][property_name]
                to_write += self._add_property(property_name, _property, schema["example"][property_name])
            to_write += self._add_constructor(schema_name, schema)
            self._write_model(schema_name, to_write)
