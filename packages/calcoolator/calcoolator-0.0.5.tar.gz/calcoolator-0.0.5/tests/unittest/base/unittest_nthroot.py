import unittest
from calcoolator.base_class import Calculator
from calcoolator.exceptions import NegativeRootError

# Setting default test values
DEFAULT = 10
NEGATIVE = -3
calc = Calculator()

class TestRoot(unittest.TestCase):
    """
    Tests for the Calculator.nth_root() method
    """
    
    def test_positive(self):
        """
        Test for a positive integer value
        """

        calc.reset(DEFAULT)
        calc.nth_root(2)
        test = DEFAULT ** (1/2)
        self.assertEqual(calc.memory, test)

    def test_float(self):
        """
        Test for a positive float value
        """

        calc.reset(DEFAULT)
        calc.nth_root(2.4987)
        test = DEFAULT ** (1/2)
        self.assertEqual(calc.memory, test)

    def test_negative_root(self):
        """
        Test for a negative root value
        """

        calc.reset(DEFAULT)
        calc.nth_root(NEGATIVE)
        test = DEFAULT ** (1/NEGATIVE)
        self.assertEqual(calc.memory, test)

    def test_negative_radicand(self):
        """
        Test for a negative radicand value
        """

        calc.reset(NEGATIVE)
        with self.assertRaises(NegativeRootError):
            calc.nth_root(2)
        self.assertEqual(calc.memory, NEGATIVE)

    def test_empty_positive(self):
        """
        Test for empty arguments on positive memory
        """

        calc.reset(DEFAULT)
        calc.nth_root()
        self.assertEqual(calc.memory, DEFAULT)

    def test_empty_negative(self):
        """
        Test for empty arguments on negative memory
        """

        calc.reset(NEGATIVE)
        with self.assertRaises(NegativeRootError):
            calc.nth_root()
        self.assertEqual(calc.memory, NEGATIVE)

    def test_0th_root(self):
        """
        Test for 0th root
        """

        calc.reset(DEFAULT)
        with self.assertRaises(ZeroDivisionError):
            calc.nth_root(0)
        self.assertEqual(calc.memory, DEFAULT)

    def test_exceptions(self):
        """
        Test for TypeError and ValueError
        """

        calc.reset(DEFAULT)
        with self.assertRaises(ValueError):
            calc.nth_root("a")
        with self.assertRaises(TypeError):
            calc.nth_root([1, 2, 3])
        self.assertEqual(calc.memory, DEFAULT)


if __name__ == '__main__':
    unittest.main()