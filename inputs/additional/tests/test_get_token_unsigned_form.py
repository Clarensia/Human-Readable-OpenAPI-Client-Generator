from BlockchainAPIsTester import BlockchainAPIsTester

class TestTokenUnsignedForm(BlockchainAPIsTester):
    async def test_to_unsigned(self):
        unsigned_form = self.api.get_token_unsigned_form("2.5", 18)
        self.assertEqual(unsigned_form, 2500000000000000000)

    async def test_to_unsigned_short(self):
        unsigned_form = self.api.get_token_unsigned_form("2.504", 18)
        self.assertEqual(unsigned_form, 2504000000000000000)

    async def test_to_unsigned_long(self):
        unsigned_form = self.api.get_token_unsigned_form("2.500000000000000001", 18)
        self.assertEqual(unsigned_form, 2500000000000000001)

    async def test_to_unsigned_no_decimal(self):
        unsigned_form = self.api.get_token_unsigned_form("2", 18)
        self.assertEqual(unsigned_form, 2000000000000000000)

    async def test_to_unsigned_no_decimal_but_trailing_zeros(self):
        unsigned_form = self.api.get_token_unsigned_form("2.00000000000000", 18)
        self.assertEqual(unsigned_form, 2000000000000000000)

    async def test_to_unsigned_lots_of_decimals(self):
        unsigned_form = self.api.get_token_unsigned_form("0.0000000000000000000000000000000000000002", 42)
        self.assertEqual(200, unsigned_form)

    async def test_to_unsigned_zero_decimals(self):
        unsigned_form = self.api.get_token_unsigned_form("42", 0)
        self.assertEqual(42, unsigned_form)

    async def test_to_unsigned_few_decimals(self):
        unsigned_form = self.api.get_token_unsigned_form("4.2", 1)
        self.assertEqual(42, unsigned_form)
