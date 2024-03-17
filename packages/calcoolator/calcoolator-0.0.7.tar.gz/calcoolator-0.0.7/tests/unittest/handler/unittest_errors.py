import unittest
from calcoolator.handler_class import HandlerCalculator

# Default testing values
DEFAULT = 10
NEGATIVE = -2
STRING = "abc"
LIST = [1, 2, 3]
calc = HandlerCalculator()

class ExceptionsBypass(unittest.TestCase):
    """
    UnitTest to check that child class bypasses errors thrown by parent class
    """

    def test_instantiation(self):
        """
        Instantiation with wrong values defaults to 0
        """

        a = HandlerCalculator(STRING)
        b = HandlerCalculator(LIST)
        self.assertEqual(a.memory, 0)
        self.assertEqual(b.memory, 0)


    def test_add(self):
        """
        Bypass ValueError and TypeError in add() method
        and show it in STDOUT
        """
        
        calc.reset(DEFAULT)
        calc.add(3, 4)
        test = DEFAULT + 3 + 4
        self.assertEqual(calc.memory, test)

        calc.add(STRING)
        self.assertEqual(calc.memory, test)

        calc.add(LIST)
        self.assertEqual(calc.memory, test)
        
        calc.add(1, 2)
        test = test + 1 + 2
        self.assertEqual(calc.memory, test)


    def test_subtract(self):
        """
        Bypass ValueError and TypeError in subtract() method
        and show message in STDOUT
        """

        calc.reset(DEFAULT)
        calc.subtract(3, 4)
        test = DEFAULT - 3 - 4
        self.assertEqual(calc.memory, test)

        calc.subtract(STRING)
        self.assertEqual(calc.memory, test)

        calc.subtract(LIST)
        self.assertEqual(calc.memory, test)

        calc.subtract(1, 2)
        test = test - 1 - 2
        self.assertEqual(calc.memory, test)


    def test_multiply(self):
        """
        Bypass ValueError and TypeError in multiply() method
        and show message in STDOUT
        """

        calc.reset(DEFAULT)
        calc.multiply(10, -3)
        test = DEFAULT * 10 * (-3)
        self.assertEqual(calc.memory, test)

        calc.multiply(STRING)
        self.assertEqual(calc.memory, test)

        calc.multiply(LIST)
        self.assertEqual(calc.memory, test)

        calc.multiply(1, 2)
        test = test * 2
        self.assertEqual(calc.memory, test)


    def test_divide(self):
        """
        Bypass ValueError, TypeError and ZeroDivisionError in divide()
        and show message in STDOUT
        """

        calc.reset(DEFAULT)
        calc.divide(2, -1)
        test = DEFAULT / 2 / (-1)
        self.assertEqual(calc.memory, test)

        calc.divide(STRING)
        self.assertEqual(calc.memory, test)

        calc.divide(LIST)
        self.assertEqual(calc.memory, test)

        calc.divide(0)
        self.assertEqual(calc.memory, test)

        calc.divide(1, 2)
        test = test / 1 / 2
        self.assertEqual(calc.memory, test)

    def test_root(self):
        """
        Bypass all errors in nth_root() method
        and show message in STDOUT
        """

        calc.reset(DEFAULT)
        self.assertEqual(calc.memory, DEFAULT)

        calc.nth_root(STRING) # ValueError
        self.assertEqual(calc.memory, DEFAULT)

        calc.nth_root(LIST)   # TypeError
        self.assertEqual(calc.memory, DEFAULT)

        calc.nth_root(0)      # ZeroDivisionError
        self.assertEqual(calc.memory, DEFAULT)

        calc.reset(NEGATIVE)
        calc.nth_root(2)      # NegativeRootError
        self.assertEqual(calc.memory, NEGATIVE)

    def test_root(self):
        """
        Bypass all errors in power() method
        and show message in STDOUT
        """

        calc.reset(DEFAULT)
        self.assertEqual(calc.memory, DEFAULT)

        calc.power(STRING)
        self.assertEqual(calc.memory, DEFAULT)

        calc.power(LIST)
        self.assertEqual(calc.memory, DEFAULT)

        calc.reset(0)
        calc.power(NEGATIVE)
        self.assertEqual(calc.memory, 0)

    def test_reset(self):
        """
        Bypass TypeError in reset() method, set memory to 0
        and show message in STDOUT
        """

        calc.reset(DEFAULT)
        calc.reset(STRING)
        self.assertEqual(calc.memory, 0)

        calc.reset(DEFAULT)
        calc.reset(LIST)
        self.assertEqual(calc.memory, 0)

        print(calc.screen.__doc__)



if __name__ == '__main__':
    unittest.main()