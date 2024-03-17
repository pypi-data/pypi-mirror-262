from calcoolator.base_class import Calculator

DEFAULT = 5
calc = Calculator(DEFAULT)


# ========== multiply() ==========

# Regular
calc.reset(DEFAULT)
calc.multiply()
test = DEFAULT * 10 * 20 * 30
assert(calc.memory == DEFAULT)
print("Test empty args passed")

# Regular
calc.reset(DEFAULT)
calc.multiply(10, 20, 30)
test = DEFAULT * 10 * 20 * 30
assert(calc.memory == test)
print("Test regular passed")

# Parse
calc.reset(DEFAULT)
calc.multiply(10, "20", 30)
test = DEFAULT * 10 * 20 * 30
assert(calc.memory == test)
print("Test parsing positive passed")

# Parse
calc.reset(DEFAULT)
calc.multiply(10, "20", '-30')
test = DEFAULT * 10 * 20 * -30
assert(calc.memory == test)
print("Test parsing negative passed")

# Only
calc.reset(DEFAULT)
calc.multiply(10, 20, 30, only=True)
test = 10 * 20 * 30
assert(calc.memory == test)
print("Test only passed")

# Factor
calc.reset(DEFAULT)
calc.multiply(10, 20, 30, factor=True)
test = (DEFAULT*10) * (DEFAULT*20) * (DEFAULT*30)
assert(calc.memory == test)
print("Test factor passed")

# Factor
calc.reset(DEFAULT)
calc.multiply(-10, 20, 30, factor=True)
test = (DEFAULT*-10) * (DEFAULT*20) * (DEFAULT*30)
assert(calc.memory == test)
print("Test factor negative passed")

# Factor + only
calc.reset(DEFAULT)
calc.multiply(10, 20, 30, only=True, factor=True)
test = (DEFAULT*10) * (DEFAULT*20) * (DEFAULT*30)
assert(calc.memory == test)
print("Test override passed")

# Error
calc.reset(DEFAULT)
try:
    calc.multiply(10, "x", 20, 30, only=True)
except ValueError:
    print("ValueError was raised")
assert(calc.memory == DEFAULT)
assert(calc.memory != 10*20*30)
print("Test ValueError passed")

# Error
calc.reset(DEFAULT)
try:
    calc.multiply(["$", 5], "20", 30)
except TypeError:
    print("TypeError was raised")
assert(calc.memory == DEFAULT)
print("Test TypeError passed")