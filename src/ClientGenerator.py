from argparse import Namespace


class ClientGenerator:
    """Allow us to generate a client from an OpenAPI SDK.
    
    Attributes:
        _open_api_file_path: The path to the OpenAPI file that we are willing to use
        _dest_folder: The destination folder of the generated client
    """
    
    def __init__(self, arguments: Namespace):
        self._verify_args(arguments)
        self._open_api_file_path = arguments.file
        self._dest_folder = arguments.dest

    def _verify_args(self, arguments: Namespace):
        """Verify if the arguments are correct. Throws an Exception if they are
        not.
        
        Correct arguments currently means:
        - arguments.file exist
        - arguments.dest does not exist, or if it exists, it must be an empty folder

        :param arguments: The program arguments that we have to verify
        :type arguments: Namespace
        """

    def create_client(self):
        """Generate the python client from the arguments given
        """
        
