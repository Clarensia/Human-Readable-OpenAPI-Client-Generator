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

    ```
    
    The TitleClass will come from the config.yml file that will be parsed.
    As well as the api key settings.
    Please note that on top of the file will be added all imports for all
    of the models that are required for the API to work.
    
    Once we have generated the base above, we will generate all of the methods
    from 
    '''
