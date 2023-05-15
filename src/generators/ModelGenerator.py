from typing import Dict

from generators.generator_types import Schema


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
                "default": "The id of blockchain on which the exchange is taking place"
            },
            "exchange": {
                "title": "Exchange",
                "type": "string",
                "default": "The id of the exchange used for this trade"
            },
            "tokenIn": {
                "title": "Tokenin",
                "type": "string",
                "default": "The address of the token that you sell"
            },
            "tokenOut": {
                "title": "Tokenout",
                "type": "string",
                "default": "The address of the token that you buy"
            },
            "amountOut": {
                "title": "Amountout",
                "type": "integer",
                "default": "The amount of token1 that you wish to buy"
            },
            "amountIn": {
                "title": "Amountin",
                "type": "integer",
                "default": "The amount of token0 that you have to sell in order to get amountOut token1"
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
            """Creates an AmountIn model

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
        for schema_name in schemas:
            schema = schemas[schema_name]
            
