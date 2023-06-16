
    def get_token_decimal_form(self, amount: int, decimals: int) -> str:
        """Convert a token from his unsigned integer form to his decimal form.
        
        This method should be used when you want to display a token to a user.
        
        For highest precision, the implementation is made using only str.

        :param amount: The integer amount that you want to convert
        :type amount: int
        :example amount: 2500000000000000000
        :param decimals: The amount of decimals that the token you are trying to convert
                         has. You can use the [decimals](/docs/python-sdk/blockchain-apis/decimals)
                         method in order to get the amount of decimals.
        :type decimals: int
        :example decimals: 18
        :return: The given amount in a decimal form.
        
        Example response:
        ```json
        2.5
        ```
        :rtype: str
        """
        str_amount = str(amount)

        # special case when decimals is 0
        if decimals == 0:
            return str_amount

        # Check if the string length is less than the decimals
        if len(str_amount) <= decimals:
            # Add leading zeros to the string
            str_amount = '0' * (decimals - len(str_amount) + 1) + str_amount
            
        # Insert the decimal point at the correct position
        str_amount = str_amount[:-decimals] + "." + str_amount[-decimals:]
        
        str_amount = str_amount.rstrip('0').rstrip('.') if '.' in str_amount else str_amount
        return str_amount

    def get_token_unsigned_form(self, amount: str, decimals: int) -> int:
        """Convert a token from his decimal form back to his unsigned integer form (this
        method does the reverse of get_token_decimal_form)
        
        This method should be used when you receive an amount from a user, in order to convert his
        input.

        For the highest precision, the implementation only uses str

        :param amount: The amount in str format that you want to convert
        :type amount: str
        :example amount: 2.5
        :param decimals: The amount of decimals that the token has. You can use the [decimals](/docs/python-sdk/blockchain-apis/decimals)
                         method in order to get the amount of decimals.
        :type decimals: int
        :example decimals: 18
        :return: The amount converted to unsigned integer
        
        Example response:
        ```json
        2500000000000000000
        ```
        :rtype: int
        """
        split = amount.split('.')
        if len(split) >= 2:
            integer_part, fractional_part = split
        else:
            integer_part, fractional_part = split[0], ""

        # Check if the fractional part has less digits than the decimal places
        if len(fractional_part) < decimals:
            # Append zeros to the end of the fractional part
            fractional_part += '0' * (decimals - len(fractional_part))
        else:
            # Trim the fractional part to the number of decimal places
            fractional_part = fractional_part[:decimals]

        # Combine the integer and fractional parts and convert to an integer
        integer_token_amount = int(integer_part + fractional_part)

        return integer_token_amount
