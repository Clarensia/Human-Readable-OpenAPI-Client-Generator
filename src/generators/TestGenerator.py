import json
import os

from typing import Dict

from src.utils import add_indent, get_method_name
from src.generators.generator_types import Get, OpenAPIPath


class TestGenerator:
    """Generate the test folder for the API client that we generate.
    
    This test folder is generated from the OpenAPI file in order to test
    some possible inputs.
    """

    _api_name: str
    """The name of the API"""

    _api_url: str
    """The url of the API"""

    _test_folder: str
    """The path to the folder containing the tests"""

    def __init__(self, api_name: str, api_url: str, test_folder: str):
        self._api_name = api_name
        self._api_url = api_url
        self._test_folder = test_folder

    def _write_test(self, test_file: str, text: str):
        with open(os.path.join(self._test_folder, test_file + ".py"), "w+") as f:
            f.write(text)

    def _generate_helper_file(self):
        helper_name = f"{self._api_name}Tester"
        to_write = f'''
from unittest import IsolatedAsyncioTestCase
from typing import Any

from aiohttp import ClientSession

from {self._api_name} import {self._api_name}
from secret_config import API_KEY

class {helper_name}(IsolatedAsyncioTestCase):
    """
    Helper class to write some test for {self._api_name}
    """
    
    _api_key: str
    """The key that we use to make API calls"""
    
    api: {self._api_name}
    """The API SDK that we have to test"""
    
    _session: ClientSession
    """The asyncio client session that we use to make manual API
    calls
    
    These API calls are made to compare the results
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._api_key = API_KEY
        self.api = None
        self._session = None
    
    async def asyncSetUp(self):
        """Setup the api instance.
        
        We create a new API instance and session instance for every run
        this way the tests are truly isolated.
        """
        self.api = {self._api_name}(api_key=self._api_key)
        self._session = ClientSession("{self._api_url}")
        
    async def asyncTearDown(self):
        """Free the resources created from asyncSetUp
        """
        await self.api.close()
        await self._session.close()
    
    async def do_request(self, url: str, params = {{}}) -> Any:
        """Make a request to the API and return the json
        result

        :param url: The url that we have to fetch (only url after {self._api_url})
        :type url: str
        :param params: The query parameters of the request, defaults to {{}}
        :type params: dict, optional
        :return: The result of the request from querying directly the API.
                 This result should be compared with the one returned by the SDK.
        :rtype: Any
        """
        async with self._session.get(url, params=params, headers={{"api-key": self._api_key}}) as response:
            return await response.json()

'''
        self._write_test(helper_name, to_write)


    def _generate_config_files(self):
        to_write = '''
# Fill this file with your config and rename it secret_config.yml

# Write your api key here.
# Don't forget to rename the file to secret_config.py before you
# do so, to prevent pushing the file by accident
API_KEY = "<Your api key here>"
'''
        self._write_test("config", to_write)
        self._write_test("secret_config", to_write)

    def _get_class_begining(self, method_name: str) -> str:
        helper_name = f"{self._api_name}Tester"
        return f'''
from dataclasses import asdict

from {helper_name} import {helper_name}

class Test{method_name[0].upper() + method_name[1:]}({helper_name}):
    """
    Test for the method {method_name} of {self._api_name}
    """
'''

    def _get_all_params_with_example(self, get: Get) -> Dict[str, Dict[str, str | int]]:
        """Allow us to get the query parameter with their example
        from the given get object.
        
        It will get all possible combination.
        
        Like when a value is optional, it will try to call it without.

        :param get: The get object
        :type get: Get
        :return: As key the name of the function and as value the parameters with their value
        :rtype: Dict[Dict[str, str | int]]
        """
        # TODO: Create multiple examples with default values and not
        if "parameters" not in get:
            return {}
        ret = {}
        for parameter in get["parameters"]:
            if "example" in parameter:
                ret[parameter["name"]] = parameter["example"]
            else:
                ret[parameter["name"]] = parameter["schema"]["default"]

        return ret

    def _format_example(self, example: str | int) -> str:
        if type(example) == int:
            return example
        else:
            return f'"{example}"'

    def _add_examples_to_method_call(self, examples: Dict[str, str | int]) -> str:
        ret = ""
        is_first = True
        for example_key in examples:
            if not is_first:
                ret += ", "
            else:
                is_first = False
            
            ret += f'{example_key}={self._format_example(examples[example_key])}'
 
        return ret

    def _format_params_api_call(self, examples: Dict[str, str | int]) -> str:
        ret = add_indent(json.dumps(examples, indent=4), 8, True)
        # remove latest line and replace it by a ')'
        parts = ret.rsplit('\n', 1)
        return ')'.join(parts)

    def _is_response_list(self, get: Get) -> bool:
        """Verify if the given response type is a List or a dataclass

        :param get: The get of the path object
        :type get: Get
        :return: `True` if the returned value is an array `False` otherwise
        :rtype: bool
        """
        ret_schema = get["responses"]["200"]["content"]["application/json"]["schema"]
        return "type" in ret_schema and ret_schema["type"] == "array"

    def _is_response_python_type(self, get: Get) -> bool:
        """Verify if the given response is a normal Python type

        :param get: The get from the route
        :type get: Get
        :return: `True` if the response is a normal Python type
        :rtype: bool
        """
        ret_schema = get["responses"]["200"]["content"]["application/json"]["schema"]
        return "type" in ret_schema and (ret_schema["type"] == "integer"\
            or ret_schema["type"] == "string")

    def _add_tests_for_route(self, route_path: str, get: Get):
        method_name = get_method_name(route_path)
        all_params = self._get_all_params_with_examples(get)
        params_examples = self._get_params_with_example(get)
        ret = self._get_class_begining(method_name, param_name)
        for param_name in all_params:
            params_examples = all_params[param_name]
            ret += "\n"
            ret += f'    async def test_{method_name}_{param_name}(self):'
            if params_examples == {}:
                ret += f'        api_result = await self.api.{method_name}()\n'
                ret += f'        api_call = await self.do_request("{route_path}")\n'
            else:
                ret += f'        api_result = await self.api.{method_name}({self._add_examples_to_method_call(params_examples)})\n'
                # We ommit the ')' here because it is added by _format_params_api_call
                ret += f'        api_call = await self.do_request("{route_path}", params={self._format_params_api_call(params_examples)}\n'
            if self._is_response_list(get):
                ret += '        self.assertListEqual([asdict(r) for r in api_result], api_call)\n'
            elif self._is_response_python_type(get):
                ret += '        self.assertEqual(api_result, api_call)\n'
            else:
                ret += '        self.assertDictEqual(asdict(api_result), api_call)\n'
        self._write_test(f"test_{method_name}", ret)

    def generate_tests(self, routes: Dict[str, OpenAPIPath]):
        """Generate all of the test files for the API

        :param routes: The routes of the API
        :type routes: Dict[str, OpenAPIPath]
        """
        self._generate_helper_file()
        self._generate_config_files()
        for route in routes:
            self._add_tests_for_route(route, routes[route]["get"])
