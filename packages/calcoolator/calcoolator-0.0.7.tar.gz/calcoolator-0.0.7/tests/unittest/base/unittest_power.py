import unittest
from calcoolator.base_class import Calculator

# Setting default test values
DEFAULT = 10
POSITIVE = 2
NEGATIVE = -3
calc = Calculator()

class TestPower(unittest.TestCase):
    """
    Tests for the Calculator.power() method
    """
    
    def test_empty(self):
        """
        Test for a positive integer value
        """

        calc.reset(DEFAULT)
        calc.power()
        self.assertEqual(calc.memory, DEFAULT)
    
    def test_parsing(self):
        """
        Test for checking parsing to int
        """

        calc.reset(DEFAULT)
        calc.power(5.43)
        test = DEFAULT ** 5
        self.assertEqual(calc.memory, test)

    def test_positive_power(self):
        """
        Test for a positive integer value
        """

        calc.reset(DEFAULT)
        calc.power(POSITIVE)
        test = DEFAULT ** POSITIVE
        self.assertEqual(calc.memory, test)

    def test_negative_power(self):
        """
        Test for a positive integer value
        """

        calc.reset(DEFAULT)
        calc.power(NEGATIVE)
        test = DEFAULT ** NEGATIVE
        self.assertEqual(calc.memory, test)

    def test_override(self):
        """
        Test for override of current memory
        """

        calc.reset(DEFAULT)
        calc.power(5, 8)
        test = 8 ** 5
        self.assertEqual(calc.memory, test)

    def test_zero(self):
        """
        Test for rising 0 to a positive number
        """

        calc.reset(0)
        calc.power(POSITIVE)
        test = 0 ** POSITIVE
        self.assertEqual(calc.memory, test)

    def test_zero_negative(self):
        """
        Test for rising 0 to a negative number
        """

        calc.reset(0)
        with self.assertRaises(ZeroDivisionError):
            calc.power(NEGATIVE)
        self.assertEqual(calc.memory, 0)

    def test_zero_zero(self):
        """
        Test for raising 0 to 0
        """

        calc.reset(0)
        calc.power(0)
        self.assertTrue(0 ** 0, calc.memory)
        self.assertTrue(0 ** 0, 1)
        self.assertEqual(calc.memory, 1)

    def test_exceptions(self):
        """
        Test for checking exceptions raised
        """

        calc.reset(DEFAULT)
        with self.assertRaises(ValueError):
            calc.power("hello")
        with self.assertRaises(TypeError):
            calc.power([1, 2, 3])
        self.assertEqual(calc.memory, DEFAULT)



if __name__ == '__main__':
    unittest.main()