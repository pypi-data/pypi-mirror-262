import unittest
from calcoolator.base_class import Calculator


# Default testing values
DEFAULT = 10
NEGATIVE = -3
calc = Calculator()

class TestPower(unittest.TestCase):
    """
    Tests for the Calculator.reset() method
    """

    def test_empty(self):
        """
        Test for resetting to 0
        """

        calc.reset()
        self.assertEqual(calc.memory, 0)

    def test_errors(self):
        """
        Test for resetting to 0
        """

        calc.reset(DEFAULT)
        with self.assertRaises(TypeError):
            calc.reset("hello")
        with self.assertRaises(TypeError):
            calc.reset("34")
        with self.assertRaises(TypeError):
            calc.reset([])
        calc.reset(NEGATIVE)
        self.assertEqual(calc.memory, NEGATIVE)


if __name__ == '__main__':
    unittest.main()