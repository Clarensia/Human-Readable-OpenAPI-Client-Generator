import json
import os
import sys

from argparse import Namespace
from typing import Dict

from src.generator_types import Schema


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
        """Verify if the arguments are correct. It prints an error if the arguments
        are wrong and exit the program with error code.
        
        Here are the error code used:
        https://stackoverflow.com/questions/1101957/are-there-any-standard-exit-status-codes-in-linux
        
        Correct arguments currently means:
        - arguments.file exist
        - arguments.dest does not exist, or if it exists, it must be an empty folder

        exit the program with 66 (cannot open) if arguments.file does not exist
        exit the program with 73 (can't create user output file) if arguments.dest is a non-empty folder or a file

        :param arguments: The program arguments that we have to verify
        :type arguments: Namespace
        """
        if not os.path.isfile(arguments.file):
            print(f"The file at path: {arguments.file} does not exist, please provide a valid input file")
            sys.exit(66)
        if os.path.isdir(arguments.dest) and len(os.listdir(arguments.dest)) > 0:
            print(f"The destination folder: {arguments.dest} exist and is not empty. You must call the program with a valid folder.")
            sys.exit(73)

    def _build_schemas(self, schemas: Dict[str, Schema]):
        pass

    def create_client(self):
        """Generate the python client from the arguments given
        """
        with open(self._open_api_file_path, "r") as f:
            open_api_file = json.load(f)
        schemas: Dict[str, Schema] = open_api_file["components"]["schemas"]
        
