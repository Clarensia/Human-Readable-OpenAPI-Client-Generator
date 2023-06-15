from BlockchainAPIsTester import BlockchainAPIsTester

class TestUnsignedDecimal(BlockchainAPIsTester):
    async def test_decimal_then_unsigned(self):
        decimal_form = self.api.get_token_decimal_form(2500000000000000000, 18)
        self.assertEqual(2500000000000000000, self.api.get_token_unsigned_form(decimal_form, 18))

    async def test_unsigned_then_decimal(self):
        unsigned_form = self.api.get_token_unsigned_form("2.5", 18)
        self.assertEqual("2.5", self.api.get_token_decimal_form(unsigned_form, 18))

    async def test_decimal_then_unsigned_short(self):
        decimal_form = self.api.get_token_decimal_form(2504000000000000000, 18)
        self.assertEqual(2504000000000000000, self.api.get_token_unsigned_form(decimal_form, 18))

    async def test_unsigned_then_decimal_short(self):
        unsigned_form = self.api.get_token_unsigned_form("2.504", 18)
        self.assertEqual("2.504", self.api.get_token_decimal_form(unsigned_form, 18))

    async def test_decimal_then_unsigned_long(self):
        decimal_form = self.api.get_token_decimal_form(2500000000000000001, 18)
        self.assertEqual(2500000000000000001, self.api.get_token_unsigned_form(decimal_form, 18))

    async def test_unsigned_then_decimal_long(self):
        unsigned_form = self.api.get_token_unsigned_form("2.500000000000000001", 18)
        self.assertEqual("2.500000000000000001", self.api.get_token_decimal_form(unsigned_form, 18))

    async def test_decimal_then_unsigned_no_decimal(self):
        decimal_form = self.api.get_token_decimal_form(2000000000000000000, 18)
        self.assertEqual(2000000000000000000, self.api.get_token_unsigned_form(decimal_form, 18))
    
    async def test_unsigned_then_decimal_no_decimal(self):
        unsigned_form = self.api.get_token_unsigned_form("2", 18)
        self.assertEqual("2", self.api.get_token_decimal_form(unsigned_form, 18))

    async def test_decimal_then_unsigned_lots_of_decimals(self):
        decimal_form = self.api.get_token_decimal_form(200, 42)
        self.assertEqual(200, self.api.get_token_unsigned_form(decimal_form, 42))

    async def test_unsigned_then_decimal_lots_of_decimals(self):
        unsigned_form = self.api.get_token_unsigned_form("0.0000000000000000000000000000000000000002", 42)
        self.assertEqual("0.0000000000000000000000000000000000000002", self.api.get_token_decimal_form(unsigned_form, 42))

    async def test_decimal_then_unsigned_zero_decimals(self):
        decimal_form = self.api.get_token_decimal_form(42, 0)
        self.assertEqual(42, self.api.get_token_unsigned_form(decimal_form, 0))

    async def test_unsigned_then_decimal_zero_decimals(self):
        unsigned_form = self.api.get_token_unsigned_form("42", 0)
        self.assertEqual("42", self.api.get_token_decimal_form(unsigned_form, 0))

    async def test_decimal_then_unsigned_few_decimals(self):
        decimal_form = self.api.get_token_decimal_form(42, 1)
        self.assertEqual(42, self.api.get_token_unsigned_form(decimal_form, 1))

    async def test_unsigned_then_decimal_few_decimals(self):
        unsigned_form = self.api.get_token_unsigned_form("4.2", 1)
        self.assertEqual("4.2", self.api.get_token_decimal_form(unsigned_form, 1))
