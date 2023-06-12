import json
import os
from typing import Any, Dict, List, Tuple

from src.utils import add_indent, convert_type, extract_schema_name_from_ref, get_method_name, is_native_python_type
from src.generators.generator_types import FuncParam, Get, Info, OpenAPI, OpenAPIPath, Property, Schema


class MainClassGenerator:
    '''Generates the class that the users will instantiate to interact
    with the API.
    
    This class is generated from the infos inside of the API + the paths,
    as well as the configuration file.
    
    It will write the title and description of the info this way:
    Example:
    
    ```json
    {
        title: "High-frequency DEX API",
        description: "Very long descriptions with some \n\n(Multiple new lines)\n"
    }
    ```
    
    Will generate the following:
    
    ```python
    class TitleClass:
        """High-frequency DEX API
       
        Very long description with some 
       
        (Multiple new lines)
       
        """

        _api_key: str | None = None
        """Your API key.
    
        This SDK will work without an API key, but we advise you to provide one in order to
        unlock better performance.
        
        You can get your API key for free on this link: https://dashboard.blockchainapis.io
        """
        
        _session: ClientSession
        """The session that is used by async operation.
        
        This session must be closed at the end of your program or usage of the API.
        
        It can be closed with:
        await blockchain_apis_instance.close()
        
        (replace blockchain_apis_instance with your instance of BlockchainAPIs)
        """
        
        _headers: Dict[str, str]
        """The headers of the API.
        
        We pre-generate them and save it because it will be the same
        headers for all requests.
        
        By saving it, we prevent from creating multiple dict and having
        multiple dict assignments which improves performance and code
        readability.
        """
        
        def __init__(self, api_key: str | None = None):
            """Create a BlcokchainAPIs async instance that allow you do API calls.

            :param api_key: Your API key, defaults to None
            :type api_key: str | None, optional
            """
            self._api_key = api_key
            self._headers = {
                "accept": "application/json"
            }
            if self._api_key is not None:
                self._headers["api-key"] = self._api_key
            self._session = ClientSession("https://api.blockchainapis.io")

        async def close(self):
            """Close the async session object.
            
            You must call this method at the end of your program or when you have finished
            working with BlockchainAPIs.
            """
            await self._session.close()

        async def _do_request(self, path: str, params: Dict[str, Any] | None = None) -> Dict[str, None]:
            """Make raw API requests (that return the json result).
            
            This method additionaly adds the user API key to the request if it is present.

            :param path: The path to the request
            :type path: str
            :param params: The optional query parameters of the request, defaults to None
            :type params: Dict[str, Any] | None, optional
            :return: The json-formated result
            :rtype: Dict[str, None]
            """
            async with self._session.get(path, params=params, headers=self._headers) as response:
                return await response.json()

    ```
    
    The TitleClass will come from the config.yml file that will be parsed.
    As well as the api key settings.
    The url: "https://api.blockchainapis.io" is also set inside of config.yml
    Please note that on top of the file will be added all imports for all
    of the models that are required for the API to work.
    
    Once we have generated the base above, we will generate all of the methods
    from the "paths" key from open API.
    
    For example:
    ```json
    "/v0/exchanges/": {
        "get": {
            "tags": [
                "exchanges"
            ],
            "summary": "Get the list of supported exchanges by the API",
            "operationId": "exchanges_v0_exchanges__get",
            "parameters": [
                {
                    "description": "You can ignore this value for this version of the API.",
                    "required": false,
                    "schema": {
                        "title": "Page",
                        "type": "integer",
                        "description": "You can ignore this value for this version of the API.",
                        "default": 1
                    },
                    "name": "page",
                    "in": "query"
                },
                {
                    "description": "The blockchain from which you want to get the exchanges",
                    "required": false,
                    "schema": {
                        "title": "Blockchain",
                        "type": "string",
                        "description": "The blockchain from which you want to get the exchanges"
                    },
                    "name": "blockchain",
                    "in": "query"
                }
            ],
            "responses": {
                "200": {
                    "description": "The list of all supported exchange of the API.\n\nYou can use the exchange id responded from this for other API calls.\n",
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/Exchanges"
                            }
                        }
                    }
                },
                "422": {
                    "description": "Validation Error",
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/HTTPValidationError"
                            }
                        }
                    }
                }
            }
        }
    }
    ```
    Will generate the following method:
    ```python
    async def exchanges(self, page: int = 1, blockchain: str | None = None) -> Exchanges:
    """Get the list of supported exchanges by the API

    :param page: You can ignore this value for the current version of the API
    :type page: int, optional
    :param blockchain: The blockchain from which you want to get the exchanges
    :type blockchain: str | None, optional
    :return: The list of all supported exchanges of the API.
    
    You can use the exchange id responded from this for other API calls.
    
    Example response:
    ```json
    {
        "page": 1,
        "total_pages": 1,
        "data": [
            {
                "exchange": "lydia_finance_avalanche",
                "blockchain": "avalanche",
                "name": "Lydia Finance",
                "url": "https://exchange.lydia.finance/#/swap",
                "fee": 200
            },
            {
                "exchange": "oliveswap_avalanche",
                "blockchain": "avalanche",
                "name": "Oliveswap",
                "url": "https://avax.olive.cash/",
                "fee": 250
            }
        ]
    }
    ```
    :rtype: Exchanges
    """
    params = {
        "page": page
    }
    if blockchain is not None:
        params["blockchain"] = blockchain
    
    ret = await self._do_request("/v0/exchanges", params)
    print(ret)
    return Exchanges(
        page=ret["page"],
        total_pages=ret["total_pages"],
        data=[
            Exchange(
                d["exchange"],
                d["blockchain"],
                d["name"],
                d["url"],
                d["fee"]
            )
            for d in ret["data"]
        ]
    )
    ```
    We have to manually put each fields, this way, if the class returns additional fields
    we will not have an error
    '''

    def __init__(self, class_name: str, api_url: str, result_folder: str, is_async: bool):
        self._class_name = class_name
        self._api_url = api_url
        self._result_folder = result_folder
        self._is_async = is_async

    def _has_list(self, paths: Dict[str, OpenAPIPath]) -> bool:
        for path in paths:
            returned_schema = paths[path]["get"]["responses"]["200"]["content"]["application/json"]["schema"]
            if "type" in returned_schema and returned_schema["type"] == "array":
                return True
            
        return False

    def _get_depend_schemas(self, schema: str, all_schema: Dict[str, Schema]) -> List[str]:
        """When we import a schema, sometimes, the schema will have a list of another shema,
        so we need to import the other schema also.
        
        This method allow us to detect dependant schemas

        :param schema: The schema name
        :type schema: str
        :param all_schema: The dictionary containing as key the schema name and as value the given
                           schema
        :type all_schema: Dict[str, Schema]
        :return: The list of schema names
        :rtype: List[str]
        """
        curr_schema = all_schema[schema]
        ret = []
        for property_name in curr_schema["properties"]:
            _proterty = curr_schema["properties"][property_name]
            if _proterty["type"] != "string" and _proterty["type"] != "integer" and _proterty["type"] != "number":
                if _proterty["type"] == "array":
                    ret.append(extract_schema_name_from_ref(_proterty["items"]["$ref"]))
                else:
                    raise Exception(f"Not supported property type: {_proterty['type']}")
        return ret

    def _get_models_to_import(self, paths: Dict[str, OpenAPIPath], all_schema: Dict[str, Schema]) -> List[str]:
        ret = []
        for path in paths:
            returned_schema = paths[path]["get"]["responses"]["200"]["content"]["application/json"]["schema"]
            if "items" in returned_schema:
                schema_to_add = returned_schema["items"]["$ref"].split("/")[-1]
                if schema_to_add not in ret:
                    ret.append(schema_to_add)
                dependant_schemas = self._get_depend_schemas(schema_to_add, all_schema)
                for dependant_schema in dependant_schemas:
                    if dependant_schema not in ret:
                        ret.append(dependant_schema)
            elif "$ref" in returned_schema:
                schema_to_add = returned_schema["$ref"].split("/")[-1]
                if schema_to_add not in ret:
                    ret.append(schema_to_add)
                dependant_schemas = self._get_depend_schemas(schema_to_add, all_schema)
                for dependant_schema in dependant_schemas:
                    if dependant_schema not in ret:
                        ret.append(dependant_schema)
            elif "type" in returned_schema:
                # It can be a simple int, so nothing to import
                continue
            else:
                raise Exception(f"Not 'item' nor '$ref' in current returned schema: {returned_schema}")
        return ret                

    def _add_necessary_imports(self, paths: Dict[str, OpenAPIPath], all_schema: Dict[str, Schema], exceptions: List[str]) -> str:
        ret = ""
        if not self._is_async:
            ret += "import requests\n\n"
        if self._has_list(paths):
            ret += "from typing import Any, Dict, List\n"
        else:
            ret += "from typing import Any, Dict\n"
        if not self._is_async:
            ret += "from urllib.parse import urljoin\n"

        if self._is_async:
            ret += "\nfrom aiohttp import ClientSession\n\n"
        else:
            ret += "\n"

        models_to_import = self._get_models_to_import(paths, all_schema)
        for model in models_to_import:
            ret += f"from .models import {model}\n"

        ret += "\n"
        for exception in exceptions:
            ret += f"from .exceptions import {exception}\n"

        return ret

    def _match_error_type(self, exceptions: List[str], indent: int) -> str:
        indentation = ' ' * indent
        ret = f'{indentation}match error_type:\n'
        for exception in exceptions:
            ret += f'{indentation}    case "{exception}":\n'
            if not self._is_async:
                ret += f'{indentation}        raise {exception}(response.status_code, error_data["detail"]["detail"])\n'
            else:
                ret += f'{indentation}        raise {exception}(response.status, error_data["detail"]["detail"])\n'
        ret += f"{indentation}    case unknown:\n"
        ret += indentation + '        raise Exception(f"Unkwnown Exception type: {unknown}.\\nGot this exception while handling:\\n{error_data} with status code: {response.status}")\n'
        return ret

    def _add_do_request_method(self, exceptions: List[str]) -> str:
        ret = f'''
    async def _do_request(self, path: str, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """Make raw API request (that return the json result).
        
        This method additionaly adds the user API key to the request if it is present.

        :param path: The path to the request
        :type path: str
        :param params: The optional query parameters of the request, defaults to None
        :type params: Dict[str, Any] | None, optional
        :return: The json-formated result
        :rtype: Dict[str, None]
        """
        async with self._session.get(path, params=params, headers=self._headers) as response:
            if response.status != 200:
                error_data = await response.json()
                error_type = error_data["detail"]["error_type"]
'''
        ret += self._match_error_type(exceptions, 16)
        ret += "\n"
        ret += '            return await response.json()\n'
        return ret        

    def _add_do_request_method_sync(self, exceptions: List[str]) -> str:
        ret = f'''
    def _do_request(self, path: str, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """Make a raw API request (that return the json result).
        
        It makes the request in a synchronous way and you don't need to close the
        BlockchainAPIs instance.

        :param path: The path of the request
        :type path: str
        :param params: The optional query parameters of the request, defaults to None
        :type params: Dict[str, Any] | None, optional
        :return: The json-formated result
        :rtype: Dict[str, Any]
        """
        url = urljoin(self._base_url, path)
        response = requests.get(url, params=params, headers=self._headers)
        if response.status_code != 200:
            error_data = response.json()
            error_type = error_data["detail"]["error_type"]
'''
        ret += self._match_error_type(exceptions, 12)
        ret += "\n"
        ret += "        return response.json()\n"
        return ret

    def _add_class_begining(self, infos: Info, exceptions: List[str]) -> str:
        ret = f'''
class {self._class_name}:
    """{infos["title"]}

    {add_indent(infos["description"], 4)}
    """

    _session: ClientSession
    """The session that is used by async operation.
    
    This session must be closed at the end of your program or usage of the API.
    
    It can be closed with:
    await blockchain_apis_instance.close()
    
    (replace blockchain_apis_instance with your instance of BlockchainAPIs)
    """
    
    def __init__(self, api_key: str | None = None):
        """Creates a {self._class_name} async instance that allow you to make API calls.

        The client works without an API key, but for better performance, we advise you
        to get one at: https://dashboard.blockchainapis.io

        :param api_key: Your API key, defaults to None
        :type api_key: str | None, optional
        """
        self._api_key = api_key
        self._headers = {{
            "accept": "application/json"
        }}
        if api_key is not None:
            self._headers["api-key"] = api_key
        self._session = ClientSession("{self._api_url}")

    async def close(self):
        """Close the async session object.
        
        You must call this method at the end of your program or when you have finished
        working with BlockchainAPIs.
        """
        await self._session.close()

    async def __aenter__(self):
        """Called when you use `async with`.
        
        For example:
        async with {self._class_name}() as blockchain_apis:
            # do some stuff
            pass

        :return: self
        :rtype: self
        """
        return self

    async def __aexit__(self, *_):
        """Called at the end of the `async with` statement in order
        to free the resources used by the API instance.
        """
        await self.close()
'''
        ret += self._add_do_request_method(exceptions)
        return ret

    def _add_class_begining_sync(self, infos: Info, exceptions: List[str]) -> str:
        ret = f'''
class {self._class_name}Sync:
    """{infos["title"]}

    {add_indent(infos["description"], 4)}
    Please note that this class is not async which is less optimized. To run more otpimized
    requests, please use: {self._class_name}
    """
    
    def __init__(self, api_key: str | None = None):
        """Creates a {self._class_name}Sync sync instance that allow you to make API calls
        in a synchronous way.

        The client works without an API key, but for better performance, we advise you
        to get one at: https://dashboard.blockchainapis.io

        :param api_key: Your API key, defaults to None
        :type api_key: str | None, optional
        """
        self._headers = {{
            "accept": "application/json"
        }}
        if api_key is not None:
            self._headers["api-key"] = api_key
        self._base_url = "{self._api_url}"

'''
        ret += self._add_do_request_method_sync(exceptions)
        return ret

    def _get_func_param_with_default(self, param: FuncParam) -> str:
        """Get the function parameters with the default value
        
        The default value, depend of the schema. If the schema contains
        a default value, we will add " = {default_value}"
        
        If the schema does not contain any default value, we will add:
        " | None = None"
        The None is to make the value optional

        :param param: The parameter that we have to get the values
        :type param: FuncParam
        :return: The parameter with the default value set
        :rtype: str
        """
        func_schema = param['schema']
        ret = f", {param['name']}: {convert_type(func_schema['type'])}"
        if 'default' in func_schema:
            ret += f" = {func_schema['default']}"
        else:
            ret += " | None = None"
        return ret

    def _get_func_params(self, get: Get) -> str:
        ret = ""
        if "parameters" in get:
            for param in get["parameters"]:
                # We first write the required parameters
                if param["required"]:
                    ret += f", {param['name']}: {convert_type(param['schema']['type'])}"

            # We now put the rest
            for param in get["parameters"]:
                if not param["required"]:
                    ret += self._get_func_param_with_default(param)

        return ret

    def _get_func_param_desc(self, get: Get) -> str:
        ret = ""
        if "parameters" in get:
            for param in get["parameters"]:
                if param["required"]:
                    ret += f'        :param {param["name"]}: {param["description"]}\n'
                    ret += f'        :type {param["name"]}: {convert_type(param["schema"]["type"])}\n'
                    ret += f'        :example {param["name"]}: {param["example"]}\n'
            for param in get["parameters"]:
                if not param["required"]:
                    ret += f'        :param {param["name"]}: {param["description"]}, defaults to {"None" if "default" not in param["schema"] else param["schema"]["default"]}\n'
                    ret += f'        :type {param["name"]}: {convert_type(param["schema"]["type"])}, Optional\n'
                    ret += f'        :example {param["name"]}: '
                    if "example" in param:
                        ret += str(param["example"])
                    else:
                        ret += str(param["schema"]["default"])
                    ret += "\n"
        return ret

    def _get_schema_name(self, get: Get) -> Tuple[str, bool]:
        """Get the name of the schema.
        
        If the schema is a list, it also returns True in secondary, False otherwise

        :param get: The get object from the path
        :type get: Get
        :return: At first the name of the schema and as second if it is an array or not
        :rtype: Tuple[str, bool]
        """
        schema = get["responses"]["200"]["content"]["application/json"]["schema"]
        if "$ref" in schema:
            return extract_schema_name_from_ref(schema["$ref"]), False
        elif "items" not in schema:
            return convert_type(schema["type"]), False
        else:
            return extract_schema_name_from_ref(schema["items"]["$ref"]), True

    def _format_example(self, schema: Schema, indent: int) -> str:
        """Format the given schema example
        
        For example:
        ```json
        {
            "page": 1,
            "total_pages": 1,
            "data": [
                {
                    "exchange": "lydia_finance_avalanche",
                    "blockchain": "avalanche",
                    "name": "Lydia Finance",
                    "url": "https://exchange.lydia.finance/#/swap",
                    "fee": 200
                },
                {
                    "exchange": "oliveswap_avalanche",
                    "blockchain": "avalanche",
                    "name": "Oliveswap",
                    "url": "https://avax.olive.cash/",
                    "fee": 250
                }
            ]
        }
        ```

        :param schema: The schema that we have to get te the example
        :type schema: Schema
        :param indent: The amount of indentation that we should have at start
        :return: The Example formated
        :rtype: str
        """
        json_string = json.dumps(schema["example"], indent=4)
        # Add space_add spaces
        indentation = ' ' * indent
        # Add the 4 spaces at the beginning of each lines
        space_added = '\n'.join(indentation + line for line in json_string.splitlines())
        return f'{space_added}\n'

    def _get_func_example_response(self, get: Get, schema: Dict[str, Schema]) -> str:
        schema_name, is_array = self._get_schema_name(get)
        if is_array:
            return f'        ```json\n        [\n{self._format_example(schema[schema_name], 12)}\n        ]\n        ```'
        elif is_native_python_type(schema_name):
            return f'        ```json\n        16\n        ```'
        else:
            return f'        ```json\n{self._format_example(schema[schema_name], 8)}\n        ```'

    def _get_response_type(self, get: Get) -> str:
        schema_name, is_array = self._get_schema_name(get)
        if is_array:
            return f"List[{schema_name}]"
        else:
            return schema_name

    def _get_func_error_desc(self, get: Get, schema: Dict[str, Schema]) -> str:
        ret = ""
        for response_code in get["responses"]:
            if response_code != "200":
                application_json = get["responses"][response_code]["content"]["application/json"]
                if "schema" in application_json:
                    exception_thrown = extract_schema_name_from_ref(application_json["schema"]["$ref"])
                    ret += f'        :raises {exception_thrown}: {get["responses"][response_code]["description"]}\n'
                elif "oneOf" in application_json:
                    possible_exceptions = application_json["oneOf"]
                    for exception in possible_exceptions:
                        ret += f'        :raises {extract_schema_name_from_ref(exception["$ref"])}: {exception["description"]}\n'

        return ret

    def _get_function_description(self, get: Get, schema: Dict[str, Schema]) -> str:
        ret = ""
        ret += f'        """{get["summary"]}\n\n'
        ret += self._get_func_error_desc(get, schema)
        ret += "\n"
        ret += self._get_func_param_desc(get)
        ret += f'        :return: {add_indent(get["responses"]["200"]["description"], 8, True)}\n'
        ret += "\n        Example response:\n"
        ret += self._get_func_example_response(get, schema)
        ret += "\n"
        ret += f"        :rtype: {self._get_response_type(get)}\n"
        ret += '        """\n'
        return ret

    def _build_returned_value_recursive(self, all_schemas: Dict[str, Schema], schema_name: str, indent: int, ret_str: str, is_first: bool = False) -> str:
        if is_native_python_type(schema_name):
            if not is_first:
                indentation = ' ' * indent
                if schema_name == "int":
                    return f"{indentation}{schema_name}(ret)"
                else:
                    return f"{indentation}ret"
            else:
                if schema_name == "int":
                    return "int(ret)"
                else:
                    return "ret"
        schema = all_schemas[schema_name]
        indentation = ' ' * indent
        new_indentation = indentation
        if not is_first:
            ret = f"{indentation}{schema_name}(\n"
            new_indentation += "    "
        else:
            ret = schema_name + "(\n"
        property_count = 0
        for property_name in schema["properties"]:
            _property: Property = schema["properties"][property_name]
            if _property["type"] == "array":
                ret += f'{indentation}{property_name}=[\n'
                schema_name = extract_schema_name_from_ref(_property['items']["$ref"])
                ret += self._build_returned_value_recursive(all_schemas, schema_name, indent + 4, "d")
                array_indent = indentation + "    "
                ret += f'{array_indent}for d in {ret_str}["{property_name}"]\n'
                ret += f'{indentation}]\n'
            else:
                ret += f'{new_indentation}{property_name}={ret_str}["{property_name}"]'
                if property_count == len(schema["properties"]) - 1:
                    ret += "\n"
                else:
                    ret += ",\n"
            property_count += 1

        if is_first:
            return ret + f"        )\n"
        else:
            return ret + f"{indentation})\n"

    def _build_returned_value(self, get: Get, schema: Dict[str, Schema]) -> str:
        """Build the returned statement of the function.
        
        This return statement have to build entirely our models
        We need to build the model this way, for example:
        Example schema:
        ```json
        {
            "page": 1,
            "total_pages": 1,
            "data": [
                {
                    "exchange": "lydia_finance_avalanche",
                    "blockchain": "avalanche",
                    "name": "Lydia Finance",
                    "url": "https://exchange.lydia.finance/#/swap",
                    "fee": 200
                },
                {
                    "exchange": "oliveswap_avalanche",
                    "blockchain": "avalanche",
                    "name": "Oliveswap",
                    "url": "https://avax.olive.cash/",
                    "fee": 250
                }
            ]
        }
        ```

        Will have to be formated this way:
        ```python
        return Exchanges(
            ret["page"],
            ret["total_pages"],
            [
                Exchange(
                    d["exchange"],
                    d["blockchain"],
                    d["name"],
                    d["url"],
                    d["fee"]
                )
                for d in ret["data"]
            ]
        )
        ```

        :param get: The get parameters
        :type get: Get
        :param schema: The dictionary containing all of the schemas
        :type schema: Dict[str, Schema]
        :return: The code for formating the return value
        :rtype: str
        """
        ret_type, is_array = self._get_schema_name(get)
        if is_array:
            ret = "        return [\n"
            ret += self._build_returned_value_recursive(schema, ret_type, 12, "r")
            ret += "            for r in ret\n        ]\n"
        else:
            ret = f'        return {self._build_returned_value_recursive(schema, ret_type, 12, "ret", True)}'

        return ret + "\n"

    def _get_function_implementation(self, path: str, get: Get, schema: Dict[str, Schema]) -> str:
        ret = ""
        if "parameters" in get:
            ret += '        params = {}\n'
            for param in get["parameters"]:
                if not param["required"]:
                    if "default" in param["schema"]:
                        ret += f'        params["{param["name"]}"] = {param["name"]}\n'
                    else:
                        ret += f'        if {param["name"]} is not None:\n'
                        ret += f'            params["{param["name"]}"] = {param["name"]}\n'
                else:
                    ret += f'        params["{param["name"]}"] = {param["name"]}\n'
            if self._is_async:
                ret += f'        ret = await self._do_request("{path}", params)\n'
            else:
                ret += f'        ret = self._do_request("{path}", params)\n'
        else:
            if self._is_async:
                ret += f'        ret = await self._do_request("{path}")\n'
            else:
                ret += f'        ret = self._do_request("{path}")\n'
        ret += self._build_returned_value(get, schema)
        return ret

    def _add_method(self, path: str, path_object: OpenAPIPath, schema: Dict[str, Schema]) -> str:
        get = path_object["get"]
        method_name = get_method_name(path)
        ret = "    "
        if self._is_async:
            ret += "async "
        
        ret += f"def {method_name}(self{self._get_func_params(get)}) -> {self._get_response_type(get)}:\n"
        ret += self._get_function_description(get, schema)
        ret += self._get_function_implementation(path, get, schema)
        return ret

    def _write_main_class(self, to_write: str):
        if self._is_async:
            with open(os.path.join(self._result_folder, f"{self._class_name}.py"), "w+") as f:
                f.write(to_write)
        else:
            with open(os.path.join(self._result_folder, f"{self._class_name}Sync.py"), "w+") as f:
                f.write(to_write)

    def _get_list_of_exceptions(self, schemas: Dict[str, Schema]) -> List[str]:
        """Get the list of each exception that we can possibly throw

        :param schemas: The dictionary containing as key the schema name and as value its implementation
        :type schemas: Dict[str, Schema]
        :return: The list of the exception schema names
        :rtype: List[str]
        """
        return [schema_name for schema_name in schemas if "Exception" in schema_name]

    def _add_export_to_package(self):
        """Append to the __init__.py file in order to allow it to export the current module
        """
        with open(os.path.join(self._result_folder, "__init__.py"), "a") as f:
            if self._is_async:
                f.write(f'from .{self._class_name} import {self._class_name}\n')
            else:
                f.write(f'from .{self._class_name}Sync import {self._class_name}Sync\n')

    def generate_main_class(self, open_api_file: OpenAPI, package_folder: str):
        main_class_text = ""
        exception_names = self._get_list_of_exceptions(open_api_file["components"]["schemas"])
        main_class_text += self._add_necessary_imports(open_api_file["paths"], open_api_file["components"]["schemas"], exception_names)
        main_class_text += "\n"
        if self._is_async:
            main_class_text += self._add_class_begining(open_api_file["info"], exception_names)
        else:
            main_class_text += self._add_class_begining_sync(open_api_file["info"], exception_names)
        main_class_text += "\n"
        for path in open_api_file["paths"]:
            main_class_text += self._add_method(path, open_api_file["paths"][path], open_api_file["components"]["schemas"])

        self._write_main_class(main_class_text)
        self._add_export_to_package()
