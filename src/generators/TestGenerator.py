class TestGenerator:
    """Generate the test folder for the API client that we generate.
    
    This test folder is generated from the OpenAPI file in order to test
    some possible inputs.
    """

    _test_folder: str
    """The path to the folder containing the tests"""

    def __init__(self, test_folder: str):
        self._test_folder = test_folder

    #def generate_tests(self, )
