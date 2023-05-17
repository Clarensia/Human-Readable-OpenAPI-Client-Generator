import json
import os
import sys

from argparse import Namespace
from typing import Dict
from src.generators.MainClassGenerator import MainClassGenerator
from src.generators.ModelGenerator import ModelGenerator

from src.generators.generator_types import Schema


class ClientGenerator:
    """Allow us to generate a client from an OpenAPI SDK.
    
    Attributes:
        _open_api_file_path: The path to the OpenAPI file that we are willing to use
        _dest_folder: The destination folder of the generated client
    """
    
    _open_api_file_path: str
    """The path to the targeted open API file. This file has to be valid, otherwise,
    the program will print an error
    """
    
    _dest_folder: str
    """The path to the destination folder"""
    
    _models_folder: str
    """The path to the folder that will contain the resulting models"""
    
    _exceptions_folder: str
    """The path to the folder that will contain the exceptions"""
    
    _main_class_generator: MainClassGenerator
    """The class that allow us to generate the main class"""
    
    _model_generator: ModelGenerator
    """The class that allow us to generate the models"""
    
    def __init__(self, arguments: Namespace):
        self._verify_args(arguments)
        self._open_api_file_path = arguments.file
        self._dest_folder = arguments.dest
        self._models_folder = os.path.join(self._dest_folder, "models")
        self._exceptions_folder = os.path.join(self._dest_folder, "exceptions")
        self._main_class_generator = MainClassGenerator()
        self._model_generator = ModelGenerator(self._models_folder, self._exceptions_folder)

    def _verify_args(self, arguments: Namespace):
        """Verify if the arguments are correct. It prints an error if the arguments
        are wrong and exit the program with error code.
        
        Here are the error code used:
        https://stackoverflow.com/questions/1101957/are-there-any-standard-exit-status-codes-in-linux
        
        Correct arguments currently means:
        - arguments.file exist
        - arguments.dest does not exist, or if it exists, it must be an empty folder
        - argument.dest is a file

        :param arguments: The program arguments that we have to verify
        :type arguments: Namespace
        """
        if not os.path.isfile(arguments.file):
            print(f"The file at path: {arguments.file} does not exist, please provide a valid input file")
            sys.exit(1)
        if os.path.isdir(arguments.dest) and len(os.listdir(arguments.dest)) > 0:
            print(f"The destination folder: {arguments.dest} exist and is not empty. You must call the program with an empty or non-existant folder.")
            sys.exit(1)
        if os.path.isfile(arguments.dest):
            print(f"The destination folder: {arguments.dest} is a file, it should be either an empty folder or not exist.")
            sys.exit(1)

    def _init_dest_folder(self):
        """Create the destination folder if not exist as well as the
        child folders:
        - models
        - exceptions
        """
        if not os.path.exists(self._dest_folder):
            parent = os.path.dirname(self._dest_folder)
            if parent and not os.path.exists(parent):
                print(f"Error: parent directory of the specified destination: {parent} does not exist. Can't create output file")
                sys.exit(1)
            os.mkdir(self._dest_folder)

        os.mkdir(self._models_folder)
        os.mkdir(self._exceptions_folder)

    def create_client(self):
        """Generate the python client from the arguments given
        """
        with open(self._open_api_file_path, "r") as f:
            open_api_file = json.load(f)
        self._init_dest_folder()
        self._main_class_generator.generate_main_class()
        schemas: Dict[str, Schema] = open_api_file["components"]["schemas"]
        self._model_generator.build_models(schemas)
