import unittest
from calcoolator.base_class import Calculator

# Setting default test values
DEFAULT = 10
calc = Calculator()

class TestAdd(unittest.TestCase):
    """
    Tests for the Calculator.add() method
    """
    
    def test_single_positive(self):
        """
        Test for a single positive integer value
        """

        calc.reset(DEFAULT)
        calc.add(5)
        test = DEFAULT + 5
        self.assertEqual(calc.memory, test)

    def test_single_negative(self):
        """
        Test for a single negative integer value
        """

        calc.reset(DEFAULT)
        calc.add(-78)
        test = DEFAULT + (-78)
        self.assertEqual(calc.memory, test)

    def test_positives(self):
        """
        Test for multiple positive float values
        """

        calc.reset(DEFAULT)
        calc.add(9.5)
        calc.add(6.2)
        test = DEFAULT + 9.5 + 6.2
        self.assertEqual(calc.memory, test)

    def test_negatives(self):
        """
        Test for multiple negative float values
        """

        calc.reset(DEFAULT)
        calc.add(-10.2)
        calc.add(-4)
        test = DEFAULT + (-10.2) + (-4)
        self.assertEqual(calc.memory, test)

    def test_strings(self):
        """
        Test for checking parsing of strings
        """

        calc.reset(DEFAULT)
        calc.add(" 11  ")        # This value should be fine
        calc.add("-10")
        with self.assertRaises(ValueError):
            calc.add("   1  z")  # This value should raise ValueError
        calc.add("22")
        with self.assertRaises(ValueError):
            calc.add(" 50  x")   # Also this one
        calc.add("-.5")
        test1 = DEFAULT + 11 + (-10) + 22 + (-.5)
        test2 = DEFAULT + 11 + (-10) + 1 + 22 + 50 + (-.5)
        self.assertEqual(calc.memory, test1)      # 11-10+22-0.5 = 22.5
        self.assertNotEqual(calc.memory, test2)

    def test_big(self):
        """
        Test for checking large numbers
        """
        calc.reset(DEFAULT)
        calc.add(7908)
        calc.add(42687)
        test = DEFAULT + 7908 + 42687
        self.assertEqual(calc.memory, test)

    def test_exceptions(self):
        """
        Test for checking exceptions handling
        """

        calc.reset(DEFAULT)
        calc.add(1, 2, 3)
        with self.assertRaises(ValueError):
            calc.add("g")
        with self.assertRaises(NameError):   # Cannot be handled inside class
            calc.add(x)
        with self.assertRaises(TypeError):   # Cannot be handled inside class
            calc.add([1, 2, 3])
        test = DEFAULT + 1 + 2 + 3
        self.assertEqual(calc.memory, test)   # Memory hasn't changed



if __name__ == '__main__':
    unittest.main()