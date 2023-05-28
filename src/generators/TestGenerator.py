import os

from typing import Dict

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
        with open(os.path.join(self._test_folder, test_file), "w+") as f:
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
        self._session = none
    
    async def asyncSetUp(self):
        """Setup the api instance.
        
        We create a new API instance and session instance for every run
        this way the tests are truly isolated.
        """
        self.api = {self._api_name}(api_key=self._api_key)
        self._session = ClientSession({self._api_url})
        
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
        async with self.session.get(url, params=params, headers={{"api-key": self._api_key}}) as response:
            return await response.json()

'''
        self._write_test(helper_name, to_write)

    def _add_test_for_route(self, route_path: str, get: Get):
        pass

    def _generate_config_files(self, )

    def generate_tests(self, routes: Dict[str, OpenAPIPath]):
        """Generate all of the test files for the API

        :param routes: The routes of the API
        :type routes: Dict[str, OpenAPIPath]
        """
        self._generate_helper_file()
        self._generate_config_files()
        for route in routes:
            self._add_test_for_route(route, routes[route]["get"])

