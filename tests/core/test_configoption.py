import unittest

from qudi.core.configoption import ConfigOption


class TestConfigOption(unittest.TestCase):
    def setUp(self):
        self.config_option = ConfigOption(
            name='some_config_option',
            default=[4, 5],
        )

    def tearDown(self):
        del self.config_option

    def test_set_name(self):
        class DummyModule:
            my_config_option = ConfigOption()
        dummy = DummyModule()
        self.assertEqual('my_config_option', dummy.my_config_option.name)

    def test_optional(self):
        config_option = ConfigOption(missing='nothing')
        self.assertTrue(config_option.optional)

    def test_copy(self):
        new = self.config_option.copy()
        self.assertEqual(self.config_option.name, new.name)
        self.assertEqual(self.config_option.default, new.default)
        self.assertEqual(self.config_option.missing, new.missing)
        self.assertEqual(self.config_option.constructor_function, new.constructor_function)
        self.assertEqual(self.config_option.converter, new.converter)

    def test_check_no_checker(self):
        self.assertTrue(self.config_option.check(0))

    def test_check(self):
        def check_positive(x):
            return x > 0
        config_option_with_checker = self.config_option.copy(checker=check_positive)
        self.assertTrue(config_option_with_checker.check(5))
        self.assertFalse(config_option_with_checker.check(-5))

    def test_convert_no_converter(self):
        self.assertEqual(self.config_option.convert(4), 4)

    def test_convert(self):
        def multiply_by_two(x):
            return 2 * x
        config_option_with_converter = self.config_option.copy(converter=multiply_by_two)
        self.assertEqual(config_option_with_converter.convert(4), multiply_by_two(4))

    def test_constructor(self):
        config_option = ConfigOption()

        @config_option.constructor
        def multiply_by_two(x):
            return 2 * x

        self.assertEqual(config_option.constructor_function(config_option, 2), 4)


if __name__ == '__main__':
    unittest.main()
