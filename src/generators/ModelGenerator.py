from typing import Dict

from generators.generator_types import Schema


class ModelGenerator:
    def __init__(self, models_path: str, exceptions_path: str):
        self._models_path = models_path
        self._exceptions_path = exceptions_path

    def build_models(self, schemas: Dict[str, Schema]):
        """Build the schemas and write them inside of the model folder.
        
        If the given shema is an exception, it writes it inside of "exceptions"

        :param schemas: The dictionary containing as key the schema id and as value the
                        schema object that we have to create
        :type schemas: Dict[str, Schema]
        """
        pass
