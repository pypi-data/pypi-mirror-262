from typing import Union
from .exceptions.negative_root import NegativeRootError

# Definition of custom type for clearer type hinting
Number = Union[int, float]

class Calculator:
    """
    Simple calculator which perfoms various mathematical operations.

    For more in-depth explanation, refer to help() or .__doc__ for the
        specific method. Only the default behaviour is described here.
    
        
    Attributes
    ----------
        memory : Number
            the current memory state of the calculator instance (default 0)

    Methods
    -------
        add(*args, only=False)
            adds the arguments to the current memory value

        subtract(*args, only=False, reverse=False)
            substracts the arguments from the current memory value

        multiply(*args, only=False, factor=False)
            multiplies the values passed and the current memory

        divide(*args, only=False, reverse=False)
            divides the current memory by the values passed as arguments

        nth_root(n=1, value=0)
            calculates the (n)th root of the current memory

        power(p=1, value=0)
            elevates the current memory to the p power

        reset(value=0)
            resets the calculator memory to 0

        get_memory()
            returns the current value in memory

        screen(message='')
            prints on stdout a pretty version of the calculator's memory

    Notes
    -----
        'Number' is an alias for Union[int, float]
        All methods parse the arguments to float type and work in sequential
            order, starting with the current memory value by default.
    """

    def __init__(self, memory: Number=0) -> None:
        """
        Calculator instance constructor

        Parameters
        ----------
            memory : Number, optional
                Initializing value for the memory of the calculator

        Raises
        ------
            TypeError
                If the memory is set to other than int or float types

        Returns
        -------
            None

        """

        if not isinstance(memory, (int, float)):
            raise TypeError("memory must be set to a number")
        self.memory = memory


    def add(self, *args: Number, only: bool=False) -> float:
        """
        Parses and adds the values of args to calculator.memory by default

        Parameters
        ----------
            args : Number
                The values to add
            only : bool, optional
                If True, add() performs 'only' the addition of the args

        Raises
        ------
            ValueError
                If the argument is non-valid (e.g. "hello")
            TypeError
                If the argument is a non-supported type (e.g. list or tuple)

        Returns
        -------
            float
                The result of the operation

        Notes
        -----
            If no argument is passed, no changes in memory occur

        Examples
        --------
            (all starting with calculator.memory = 10)

            >>> calculator.add(1, 2, 3) == 10+1+2+3
            13.0
            >>> calculator.add(1, 2, 3, only=True) == 1+2+3
            6.0
            >>> calculator.add(1, 2, "x")
            ValueError
        """

        if only:
            initial: float = 0
        else:
            initial = self.memory

        for value in args:
            initial += float(value)

        self.memory = initial
        return self.memory
    
    
    def subtract(self, *args, only: bool=False, reverse: bool=False) -> float:
        """
        Parses and subtracts the values of args from calculator.memory from
            left to right starting by the memory value by default

        Parameters
        ----------
            args : Number
                The values to subtract
            only : bool, optional
                If True, it performs 'only' the subtraction of args
            reverse : bool, optional
                If True, subtracts the values from right to left

        Raises
        ------
            ValueError
                If the argument is a non-valid string (e.g. "hello")
            TypeError
                If the argument is a non-supported type (e.g. list or tuple)

        Returns
        -------
            float
                The result of the operation

        Notes
        -----
            If no argument is passed, no changes in memory occur

        Examples
        --------
            (All starting with calculator.memory = 5)

            >>> calculator.subtract(1, 2, 3) == 5-3-2-1
            -1.0
            >>> calculator.subtract(1, 2, 3, only=True) ==  1-2-3
            -4.0
            >>> calculator.subtract(1, 2, 3, reverse=True) == 3-2-1-5
            -5.0
            >>> calculator.subtract(1, 2, 3, reverse=True, only=True) == 3-2-1
            0.0
            >>> calculator.subtract(1, 2, [3, 4, 5])
            TypeError
        """

        arg_list = list(args)
        # Setting up the initial value
        if reverse:
            arg_list.reverse()      # Reversing the list
            
        if reverse or only:
            initial = arg_list[0]   # Using the first element as initial
            arg_list.pop(0)         # Removing it from the list
        else:
            initial = self.memory   # Else, first element is the memory

        if reverse:
            for value in arg_list:
                initial -= float(value)
            if not only:
                initial -= self.memory
        else:
            for value in arg_list:
                initial -= float(value)

        self.memory = initial
        return self.memory
    
    
    def multiply(self, *args: Number, only=False, factor=False) -> float:
        """
        Parses and multiplies the values of args in sequential order, starting
            by the current memory by default

        Parameters
        ----------
            args : Number
                The values to multiply
            only : bool, optional
                If True, returns the product of all numbers without considering
                    the value stored in memory. Multiplies 'only' the arguments
            factor : bool, optional
                If set to True, multiplies each args value by the memory and
                    then multiplies the results together

        Raises
        ------
            ValueError
                If the argument is a non-valid string (e.g. "R2D2")
            TypeError
                If the argument is a non-supported type (e.g. list or tuple)

        Returns
        -------
            float
                The product of the given numbers 
        
        Notes
        -----
            'factor' will override 'only'
            If no arguments are passed, no change in memory occur

        Examples
        --------
            All assuming calculator.memory = 5

            >>> calculator.multiply(1, 2, 3) == 5*3*2*1
            30.0
            >>> calculator.multiply(1, 2, 3, only=True) == 1*2*3
            6.0
            >>> calculator.multiply(1, 2, 3, factor=True) == (5*1)*(5*2)*(5*3)
            750.0
            >>> calculator.multiply(1, 2, [10, 20, 30])
            TypeError
        """

        arg_list = list(args)
        if factor:
            arg_list = [self.memory * float(value) for value in arg_list]
        if only or factor:
            initial = arg_list[0]
            arg_list.pop(0)
        else:
            initial = self.memory

        for value in arg_list:
            initial *= float(value)
        
        self.memory = initial
        return self.memory
    
    
    def divide(self, *args: Number,
               only: bool=False, reverse: bool=False) -> float:
        """
        Divides the values in sequential order, memory value taken as first
            dividend
        
        Parameters
        ----------
            args : Number
                The values to use as divisors
            only : bool, optional
                If True, divides the values in args only: args[0] is first
                    dividend, args[1] is first divisor
            reverse : bool, optional
                If True, divides the values from right to left

        Raises
        ------
            ValueError
                If the argument is non-valid (e.g. "spam")
            TypeError
                If the argument is a non-supported type (e.g. list or tuple)
            ZeroDivisionError
                Pretty self explanatory, isn't it? 😅

        Returns
        ------
            float
                the result of the operation
                
        Notes
        -----
            If no argument is passed, no changes in memory occur

        Examples
        --------
            (All starting with calculator.memory = 5)

            >>> calculator.divide()
            5
            >>> calculator.divide(10)
            0.5
            >>> calculator.divide(10, reverse=True)
            2.0
            >>> calculator.divide(10, 2, only=True)
            5.0
            >>> calculator.divide(10, 2, only=True, reverse=True)
            0.2
            >>> calculator.divide(10, 2, [])
            TypeError
        """

        arg_list = list(args)
        if reverse:
            arg_list.reverse()
            
        if reverse or only:
            initial = float(arg_list[0])
            arg_list.pop(0)
        else:
            initial = float(self.memory)

        if reverse:
            for value in arg_list:
                initial /= float(value)
            if not only:
                initial /= self.memory
        else:
            for value in arg_list:
                initial /= float(value)

        self.memory = initial
        return self.memory
    

    def nth_root(self, n: int=1, value: Number=0) -> float:
        """
        Parses n to int and calculates the n-th root of the value in memory
            if no other parameter is specified

        Parameters
        ----------
            n : int
                The degree of the root
            value : Number, optional
                The radicant of the root; calculator.memory by default

        Raises
        ------
            ValueError
                If the argument is non-valid (e.g. "spam")
            TypeError
                If the argument is a non-supported type (e.g. list or tuple)
            ZeroDivisionError
                If trying to find the 0th root
            NegativeRootError
                If trying to calculate the root of a negative number. This
                    calculator hasn't been designed to handle complex numbers

        Returns
        ------
            float
                the result of the operation
                
        Notes
        -----
            If no arguments are passed, no changes in memory occur
            If memory is a negative number and no arguments ar passed, it will
                throw a NegativeRootException

        Examples
        --------
            (All starting with calculator.memory = 5)

            >>> calculator.nth_root()
            5.0
            >>> calculator.nth_root(2)
            2.23606797749979
            >>> calculator.nth_root(2, 16)
            4.0

            >>> calculator.reset(-3)
            >>> calculator.nth_root(2)
            NegativeRootError
        """

        value = float(value) or self.memory
        n = int(n)
        if value < 0:
            raise NegativeRootError(n, value)
        
        self.memory = value ** (1/n)
        return self.memory
    

    def power(self, p: int=1, value: Number=0) -> float:
        """
        Removes decimal part from p and elevates the value in memory to the
            power of p

        Parameters
        ----------
            p : int
                The exponent of the power
            value : Number, optional
                The base of the power. calculator.memory by default

        Raises
        ------
            ValueError
                If the argument is non-valid (e.g. "spam")
            TypeError
                If the argument is a non-supported type (e.g. list or tuple)
            ZeroDivisionError
                If trying to raise 0 to a negative value

        Returns
        ------
            float
                the result of the operation or 1 if 0⁰
                
        Notes
        -----
            If no arguments are passed, no changes in memory occur

        Examples
        --------
            (All starting with calculator.memory = 5)

            >>> calculator.power(2)
            25
            >>> calculator.power(2, 10)
            100
            >>> calculator.power("a")
            ValueError

            >>> calculator.reset(-5)
            >>> calculator.power(3)
            -125
        """

        power: float = 1
        base: float = value or self.memory
        p = int(p)

        if p == 0 and base == 0:
            self.memory = 1
            return self.memory
        elif p > 0:
            for _ in range(p):
                power *= base
        else:
            p = p * (-1)
            for _ in range(p):
                power *= base
            power = 1 / power

        self.memory = power
        return self.memory
    

    def reset(self, value: Number=0) -> None:
        """
        Resets the calculator memory to 0 or the specified value

        Parameters
        ----------
            value : Number, optional
                The value to set the memory to. Default is 0

        Raises
        ------
            TypeError
                If the argument is a non-supported type (e.g. string or list)

        Returns
        ------
            None
        """

        if not isinstance(value, (int, float)):
            raise TypeError("memory must be reset to a number")
        else:
            self.memory = value

    def get_memory(self) -> float:
        """
        Method to save the current memory value as a variable

        Parameters
        ----------
            None

        Returns
        ------
            calculator.memory : float
        """

        return self.memory
    

    def screen(self, message: str='') -> None:
        """
        Prints a prettified version of the memory value or a message of your
            liking in a screen-like format taking 32 characters wide by 3 lines

        Parameters
        ----------
            message : str, optional
                The message to display (truncated to 28 characters)

        Returns
        ------
            None

        Example
        -------
            Suposing calculator.memory = 10

            >>> calculator.screen()
            *------------------------------*
            |                         10.0 |
            *------------------------------*
            >>> calculator.screen("meow")
            *------------------------------*
            |             meow             |
            *------------------------------*
        """

        message = str(message).strip()
        if message:
            print(f'*{"-" * 30}*\n| {message:^28.28} |\n*{"-" * 30}*')
        else:
            print(f'*{"-" * 30}*\n| {float(self.memory):> 28} |\n*{"-" * 30}*')
