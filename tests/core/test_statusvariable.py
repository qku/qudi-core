import unittest

from qudi.core.statusvariable import StatusVar


class TestConfigOption(unittest.TestCase):
    def setUp(self):
        self.status_var = StatusVar(
            name='some_status_var',
            default=[4, 5],
        )

    def tearDown(self):
        del self.status_var

    def test_set_name(self):
        class DummyModule:
            my_status_var = StatusVar()
        dummy = DummyModule()
        self.assertEqual('my_status_var', dummy.my_status_var.name)

    def test_copy(self):
        new = self.status_var.copy()
        self.assertEqual(self.status_var.name, new.name)
        self.assertEqual(self.status_var.default, new.default)
        self.assertEqual(self.status_var.constructor_function, new.constructor_function)
        self.assertEqual(self.status_var.representer_function, new.representer_function)

    def test_constructor(self):
        status_var = StatusVar()

        @status_var.constructor
        def multiply_by_two(x):
            return 2 * x

        self.assertEqual(status_var.constructor_function(status_var, 2), 4)

    def test_representer(self):
        status_var = StatusVar()

        @status_var.representer
        def multiply_by_two(x):
            return 2 * x

        self.assertEqual(status_var.representer_function(status_var, 2), 4)


if __name__ == '__main__':
    unittest.main()
