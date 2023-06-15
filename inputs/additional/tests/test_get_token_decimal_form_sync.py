from BlockchainAPIsSyncTester import BlockchainAPIsSyncTester

class TestTokenDecimalFormSync(BlockchainAPIsSyncTester):
    def test_to_decimal(self):
        decimal_form = self.api.get_token_decimal_form(2500000000000000000, 18)
        self.assertEqual(decimal_form, "2.5")

    def test_to_decimal_short(self):
        decimal_form = self.api.get_token_decimal_form(2504000000000000000, 18)
        self.assertEqual(decimal_form, "2.504")

    def test_to_decimal_long(self):
        decimal_form = self.api.get_token_decimal_form(2500000000000000001, 18)
        self.assertEqual(decimal_form, "2.500000000000000001")

    def test_to_decimal_no_decimal(self):
        decimal_form = self.api.get_token_decimal_form(2000000000000000000, 18)
        self.assertEqual(decimal_form, "2")

    def test_to_decimal_lots_of_decimals(self):
        decimal_form = self.api.get_token_decimal_form(200, 42)
        self.assertEqual("0.0000000000000000000000000000000000000002", decimal_form)

    def test_to_decimal_zero_decimals(self):
        decimal_form = self.api.get_token_decimal_form(42, 0)
        self.assertEqual("42", decimal_form)

    def test_to_unsigned_few_decimals(self):
        decimal_form = self.api.get_token_decimal_form(42, 1)
        self.assertEqual("4.2", decimal_form)
