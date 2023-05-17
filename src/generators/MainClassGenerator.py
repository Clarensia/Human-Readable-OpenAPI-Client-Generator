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
    Exchanges(
        page=1,
        total_pages=1,
        data=[
            Exchange(
                exchange="lydia_finance_avalanche",
                blockchain="avalanche",
                name="Lydia Finance",
                url="https://exchange.lydia.finance/#/swap",
                fee=200
            ),
            Exchange(
                exchange="oliveswap_avalanche",
                blockchain="avalanche",
                name="Oliveswap",
                url="https://avax.olive.cash/",
                fee=250
            )
        ]
    )
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

    def __init__(self):
        pass
    
    def generate_main_class(self):
        pass
