

DEFAULT = 5
calc = Calculator(DEFAULT)


# ========== subtract() ==========

# Regular
calc.reset(DEFAULT)
calc.subtract()
assert(calc.memory == DEFAULT)

# Regular
calc.reset(DEFAULT)
calc.subtract(1, 2, 3)
test = DEFAULT - 1 - 2 - 3
assert(calc.memory == test)

# Parse
calc.reset(DEFAULT)
calc.subtract(1, "-2", 3)
test = DEFAULT - 1 - (-2) - 3
assert(calc.memory == test)

# Only
calc.reset(DEFAULT)
calc.subtract(1, 2, 3, only=True)
test = 1 - 2 - 3
assert(calc.memory == test)

# Reverse
calc.reset(DEFAULT)
calc.subtract(1, 2, 3, reverse=True)
test = 3 - 2 - 1 - DEFAULT
assert(calc.memory == test)

# Only & reverse
calc.reset(DEFAULT)
calc.subtract(1, 2, 3, reverse=True, only=True)
test = 3 - 2 - 1
assert(calc.memory == test)

# Error
calc.reset(DEFAULT)
calc.subtract(1, "2x", 3, reverse=True)
test = 3 - 2 - 1 - DEFAULT
assert(calc.memory != test)
assert(calc.memory == DEFAULT)

# Error
calc.reset(DEFAULT)
calc.subtract(1, 2, 3, ())
assert(calc.memory != test)
assert(calc.memory == DEFAULT)