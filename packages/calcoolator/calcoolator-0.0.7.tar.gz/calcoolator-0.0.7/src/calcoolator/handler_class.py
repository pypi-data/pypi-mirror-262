from typing import Union
from .base_class import Calculator
from .exceptions.negative_root import NegativeRootError

# Definition of custom type for clearer type hinting
Number = Union[int, float]

class HandlerCalculator(Calculator):
    """
    Simple calculator which perfoms various mathematical operations.

    The main difference with it's parent -Calculator- class is that instead of
        stopping execution when an exception is raised, the memory value is not
        changed and continues operation. Otherwise, it works exactly the same.
    
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
            elevates the current memory to the power of p

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
        HandlerCalculator instance constructor (inherited from Calculator)

        Parameters
        ----------
            memory : Number, optional
                Initializing value for the memory of the calculator

        Returns
        -------
            None

        Notes
        -----
            If an invalid type is passed, HandlerCalculator is initialized with
                memory = 0
        """

        try:
            super().__init__(memory)
        except TypeError as te:
            print(f"add() failed with TypeError:\
                \nmessage: {str(te)}\
                \ninitialized with memory = 0\n")
            self.memory = 0


    def add(self, *args: Number, only: bool=False) -> float:
        """
        Parses and adds the values of args to calculator.memory by default

        Parameters
        ----------
            args : Number
                The values to add
            only : bool, optional
                If True, add() performs 'only' the addition of the args

        Returns
        -------
            float
                The result of the operation if all can be completed, else, the
                initial memory state

        Notes
        -----
            If no argument is passed, no changes in memory occur
            If the full operation is not completed successfully (i.e. one or
                some of the arguments is not valid) no changes in memory occur

        Examples
        --------
            (all starting with instance.memory = 10)

            >>> instance.add(1, 2, 3) == 10+1+2+3
            13.0
            >>> instance.add(1, 2, 3, only=True) == 1+2+3
            6.0
            >>> instance.add(1, 2, "x") <- Catches ValueError and resets
            10.0
        """

        try:
            super().add(*args, only=only)
        except ValueError as ve:
            print(f"add() failed with ValueError:\
                \nmessage: {str(ve)}\
                \nno operations were performed, memory is {self.memory}\n")
        except TypeError as te:
            print(f"add() failed with TypeError:\
                \nmessage: {str(te)}\
                \nno operations were performed, memory is {self.memory}\n")
        
        return self.memory
    
    
    def subtract(self, *args: Number,
                 only: bool=False, reverse: bool=False) -> float:
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

        Returns
        -------
            float
                The result of the operation or the previous memory state if the
                operation fails to complete

        Notes
        -----
            If no argument is passed, no changes in memory occur
            If the full operation is not completed successfully (i.e. one or
                some of the arguments is not valid) no changes in memory occur

        Examples
        --------
            (All starting with instance.memory = 5)

            >>> instance.subtract(1, 2, 3) == 5-3-2-1
            -1.0
            >>> instance.subtract(1, 2, 3, only=True) ==  1-2-3
            -4.0
            >>> instance.subtract(1, 2, 3, reverse=True) == 3-2-1-5
            -5.0
            >>> instance.subtract(1, 2, 3, reverse=True, only=True) == 3-2-1
            0.0
            >>> instance.subtract(1, 2, "should be ValueError")
            5.0
        """

        try:
            super().subtract(*args, only=only, reverse=reverse)
        except ValueError as ve:
            print(f"subtract() failed with ValueError:\
                  \nmessage: {str(ve)}\
                  \nno operations were performed, memory is {self.memory}\n")
        except TypeError as te:
            print(f"subtract() failed with TypeError:\
                  \nmessage: {str(te)}\
                  \nno operations were performed, memory is {self.memory}\n")
            
        return self.memory
    
    
    def multiply(self, *args: Number, 
                 only=False, factor=False) -> float:
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

        Returns
        -------
            float
                The product of the given numbers or the previous memory value
                if the operation fails to complete
        
        Notes
        -----
            'factor' will override 'only'
            If no arguments are passed, no change in memory occur
            If the full operation is not completed successfully (i.e. one or
                some of the arguments is not valid) no changes in memory occur

        Examples
        --------
            All assuming instance.memory = 5

            >>> instance.multiply(1, 2, 3) == 5*3*2*1
            30.0
            >>> instance.multiply(1, 2, 3, only=True) == 1*2*3
            6.0
            >>> instance.multiply(1, 2, 3, factor=True) == (5*1)*(5*2)*(5*3)
            750.0
            >>> instance.multiply(1, 2, [10, 20, 30])
            5.0
        """

        try:
            super().multiply(*args, only=only, factor=factor)
        except ValueError as ve:
            print(f"multiply() failed with ValueError:\
                  \nmessage: {str(ve)}\
                  \nno operations were performed, memory is {self.memory}\n")
        except TypeError as te:
            print(f"multiply() failed with TypeError:\
                  \nmessage: {str(te)}\
                  \nno operations were performed, memory is {self.memory}\n")
            
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

        Returns
        ------
            float
                the result of the operation or the previous memory state if the
                operation fails to complete in full
                
        Notes
        -----
            If no argument is passed, no changes in memory occur
            If the full operation is not completed successfully (i.e. one or
                some of the arguments is not valid) no changes in memory occur

        Examples
        --------
            (All starting with instance.memory = 5)

            >>> instance.divide()
            5
            >>> instance.divide(10)
            0.5
            >>> instance.divide(10, reverse=True)
            2.0
            >>> instance.divide(10, 2, only=True)
            5.0
            >>> instance.divide(10, 2, only=True, reverse=True)
            0.2
            >>> instance.divide(9, 0, [])
            5

        """
        try:
            super().divide(*args, only=only, reverse=reverse)
        except ValueError as ve:
            print(f"divide() failed with ValueError:\
                  \nmessage: {str(ve)}\
                  \nno operations were performed, memory is {self.memory}\n")
        except TypeError as te:
            print(f"divide() failed with TypeError:\
                  \nmessage: {str(te)}\
                  \nno operations were performed, memory is {self.memory}\n")
        except ZeroDivisionError as zde:
            print(f"divide() failed with ZeroDivisionError:\
                  \nmessage: {str(zde)}\
                  \nno operations were performed, memory is {self.memory}\n")
            
        return self.memory
    
    
    def nth_root(self, n: int=1, value: Number= 0) -> float:
        """
        Parses n to int and calculates the n-th root of the value in memory
            if no other parameter is specified

        Parameters
        ----------
            n : int
                The degree of the root
            value : Number, optional
                The radicant of the root; instance.memory by default

        Returns
        ------
            float
                the result of the operation or the previous memory if an error
                    occured
                
        Notes
        -----
            If no arguments are passed, no changes in memory occur

        Examples
        --------
            (All starting with instance.memory = 5)

            >>> instance.nth_root()
            5.0
            >>> instance.nth_root(2)
            2.23606797749979
            >>> calculator.nth_root(2, 16)
            4.0

            >>> instance.reset(-3)
            >>> instance.nth_root(2)
            5.0
        """

        try:
            super().nth_root(n, value)
        except ValueError as ve:
            print(f"nth_root() failed with ValueError:\
                  \nmessage: {str(ve)}\
                  \nno operations were performed, memory is {self.memory}\n")
        except TypeError as te:
            print(f"nth_root() failed with TypeError:\
                  \nmessage: {str(te)}\
                  \nno operations were performed, memory is {self.memory}\n")
        except ZeroDivisionError as zde:
            print(f"nth_root() failed with ZeroDivisionError:\
                  \nmessage: {str(zde)}\
                  \nno operations were performed, memory is {self.memory}\n")
        except NegativeRootError as nnr:
            print(f"nth_root() failed with NegativeRootError:\
                  \nmessage: {str(nnr)}\
                  \nno operations were performed, memory is {self.memory}\n")
            
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
                The base of the power; instance.memory by default

        Raises
        ------
            ValueError
                If the argument is non-valid (e.g. "spam")
            TypeError
                If the argument is a non-supported type (e.g. list or tuple)

        Returns
        ------
            float
                The result of the operation or 1 if 0⁰
                If an exception is caught, the original memory value is returned
                
        Notes
        -----
            If no arguments are passed, no changes in memory occur

        Examples
        --------
            (All starting with instance.memory = 5)

            >>> instance.power(2)
            25
            >>> instance.power(2, 10)
            100
            >>> instance.power("a")
            5

            >>> instance.reset(-5)
            >>> instance.power(3)
            -125
        """

        try:
            super().power(p, value)
        except ValueError as ve:
            print(f"power() failed with ValueError:\
                  \nmessage: {str(ve)}\
                  \nno operations were performed, memory is {self.memory}\n")
        except TypeError as te:
            print(f"power() failed with TypeError:\
                  \nmessage: {str(te)}\
                  \nno operations were performed, memory is {self.memory}\n")
        except ZeroDivisionError as zde:
            print(f"power() failed with ZeroDivisionError:\
                  \nmessage: {str(zde)}\
                  \nno operations were performed, memory is {self.memory}\n")
            
        return self.memory
    
    
    def reset(self, value: Number= 0) -> None:
        """
        Resets the calculator memory to 0 or the specified value

        Parameters
        ----------
            value : Number, optional
                The value to set the memory to. Default is 0

        Notes
        -----
            If the argument passed is not valid, memory is set to 0

        Returns
        ------
            None
        """

        try:
            super().reset(value)
        except TypeError as te:
            self.memory = 0
            print(f"reset() failed with TypeError:\
                  \nmessage: {str(te)}\
                  \nmemory was set to 0\n")
        