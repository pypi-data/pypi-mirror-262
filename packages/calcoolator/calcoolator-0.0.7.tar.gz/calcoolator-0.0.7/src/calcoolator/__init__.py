"""
calcoolator package info:

In this package you'll find two main modules:
    > base_class
    > handler_class

And the submodule exceptions, containing the negative_root module, a custom
    exception class created to handle roots of negative numbers as this
    calculators are not so smart and aren't designed to handle complex numbers.

Below is a summary of the basic features:

    1) base_class contains Calculator: A simple, yet effective class to compute
        basic arithmetic operations, such as addition, subtraction,
        multiplication, division, nth roots, powers and some more.
    2) handler_class contains HandlerCalculator: A child to Calculator. Same
        functionality with the difference that catches errors and continues
        operations instead of stopping execution.

For easy use, please structure your imports as follow:

    from calcoolator.base_class import Calculator
    or
    from calcoolator.handler_class import HandlerCalculator

And just create the instances in your project:

    instance = Calculator()
    or
    instance = HandlerCalculator()

For full feature description please refer to the specific help() or __doc__
    of the class or method you are interested in.

Thank you for your download! :)
"""
