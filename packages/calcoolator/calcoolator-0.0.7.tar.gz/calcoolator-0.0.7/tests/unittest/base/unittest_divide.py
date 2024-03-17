import unittest
from calcoolator.base_class import Calculator


DEFAULT = 10
calc = Calculator()

class TestDivide(unittest.TestCase):
    """
    Tests for the Calculator.divide() method
    """

    def test_empty(self):
        """
        Test for checking empty arguments
        """

        calc.reset(DEFAULT)
        calc.divide()
        self.assertEqual(calc.memory, DEFAULT)


    def test_single_positive(self):
        """
        Test for checking a single value
        """

        calc.reset(DEFAULT)
        calc.divide(5)
        test1 = DEFAULT / 5
        self.assertEqual(calc.memory, test1)
        calc.divide(3, reverse=True)
        test2 = 3 / test1
        self.assertEqual(calc.memory, test2)


    def test_single_negative(self):
        """
        Test for checking chained operations
        """
        
        calc.reset(DEFAULT)
        calc.divide(-5)
        test = DEFAULT / (-5)
        self.assertEqual(calc.memory, test)


    def test_multiple(self):
        """
        Test for checking chained operations
        """

        calc.reset(DEFAULT)
        calc.divide(7, 4, 8)
        calc.divide(2, 5)
        calc.divide(10, reverse=True)
        test1 = DEFAULT / 7 / 4 / 8
        test2 = test1 / 2 / 5
        test3 = 10 / test2
        self.assertEqual(calc.memory, test3)


    def test_only(self):
        """
        Test for checking "only"
        """

        calc.reset(DEFAULT)
        calc.divide(7, 4, 8, only=True)
        test1 = DEFAULT / 7 / 4 / 8
        test2 = 7 / 4 / 8
        self.assertNotEqual(calc.memory, test1)
        self.assertEqual(calc.memory, test2)


    def test_reverse(self):
        """
        Test for checking "reverse"
        """

        calc.reset(DEFAULT)
        calc.divide(7, 4, 8, reverse=True)
        test = 8 / 4 / 7 / DEFAULT
        self.assertEqual(calc.memory, test)


    def test_only_reverse(self):
        """
        Test for checking "reverse" and "only"
        """
                
        calc.reset(DEFAULT)
        calc.divide("3", -2, 5, only=True, reverse=True)
        test1 = DEFAULT / 3 / (-2) / 5              # Regular 
        test2 = 5 / (-2) / 3 / DEFAULT              # Reverse
        test3 = 3 / (-2) / 5                        # Only 
        test4 = 5 / (-2) / 3                        # Reverse & only
        self.assertNotEqual(calc.memory, test1)
        self.assertNotEqual(calc.memory, test2)
        self.assertNotEqual(calc.memory, test3)
        self.assertEqual(calc.memory, test4)


    def test_exceptions(self):
        """
        Test for checking exceptions
        """

        calc.reset(DEFAULT)
        calc.divide(1, 2, 3)
        with self.assertRaises(ValueError):
            calc.divide("meow")
        with self.assertRaises(TypeError):
            calc.divide([1, 2, 3])
        with self.assertRaises(ZeroDivisionError):
            calc.divide(6, 14, "0")
        test = DEFAULT / 1 / 2 / 3
        self.assertEqual(calc.memory, test)   # Memory hasn't changed


if __name__ == '__main__':
    unittest.main()