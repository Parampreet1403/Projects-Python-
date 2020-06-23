# Parampreet Singh - 19/06/20
# Exploring Python standard Libary
# Learn Python from a C++ perspective
# PEP 8 programming style

import math


print("Hello World :)")  # Dynamic Language


# Type declaration
students_count = 1000  # integer
student_count: int = 1000  # Type def
rating = 4.99  # float
is_published = False  # boolean, first letter uppercase
course_name = "Python"  # string
multi_line_declaration = """Multi
Line declaration"""


# Variable declaration
x, y = 1, 2  # Multi-variable declaration
x = y = 1  # Multi-variable initalisation


# Type indentifying
print("\nType Identifying\n")
print(type(multi_line_declaration))  # Type

age = 20
age = "Python insane"
print(age)  # This is crazy talk but valid

age: int = 20
age: str = "Python sane"  # String is str, alternative (>select mypy)
print(age)


# ==============================================================================

# Memory allocation
print("\nMemory allocation\n")
id(x)  # Memory location (&)
print(id(x))
x += 1  # x is allocated to new memory address -> immutable
print(id(x))

myList = [1, 2, 3]  # Same memory address upon alteration -> mutable
print(id(myList))
myList.append(4)
print(id(myList))

""" Whats going on behind closed doors?
As variables no longer need their type specified, I think the compiler assigns
each variable to a class. The class is determined on the rvalue of the variable,
whether that be int, float, str or bool. No void :(.
So when x is changed it is now an new instance of the class int and hence points to
a new memory location. However, lists are just modifying the same instance
of the class list and so you can change the variable without affecting its memory location.

*Note: This is my intuitive thought not a real answer
"""
# To edit memory location of a variable
# OR variable within a function
# Use the KeyWord global
message = "a"


def greet():
    global message
    message = "b"


greet()
print(message)


# ==============================================================================


# Strings
print("\nString Manipulation\n")
myStr = "Python Programming"
print(len(myStr))  # Length of string
print(myStr[0])
print(myStr[-1])  # No longer random memory location loops back in the string
print(myStr[0:6])  # This is called String Slicing
print(myStr[7:])  # Print part of string up untill... (This case end)

course = "   Python Programming   "
print(course.upper())
print(course.lower())
print(course.strip())  # Remove whitespace
print(course.lstrip())  # Remove left whitespace#

print(course.find("pro"))  # Boolean
print(course.replace("P", "-"))
print("Programming" in course)  # Boolean (built in "in" keyword, so elagant)
print("Programming" not in course)

# New Tool: Formatted String (SO POWERFUL, the ultimate variable conttructor)
first = "Param"
last = "Singh"
full = f"{first}\n{last} 2+2 "  # formatted string (THIS IS CRAZY!!!)
print(full)
""" formated string: non constant value, expression determined at run-time
variables in quotation evaluated at run time.
That means you can put a tab, new line and even space between variables and
they will be read alongside normal characters
"""

# Alternative
x = 5
print("x = ", x, sep="   ")  # Sep declares what will separate them
# default space is single whitespace

myString = "Hello I am a String which is a class not really a string"
print(myString.replace(" ", "-"))

myList = myString.split(" ")
print(myList)

print(myString[::-1])  # Reverses String


# ==============================================================================


# Lists
print("\nList\n")
myList = [1, 2, 3, 4]
print(myList[1])
myList.insert(1, 1.5)  # Like vectors
print(myList)
del(myList[:2])  # Super Powerful
print(myList)
myList.append(5)
print(myList)

list1 = [1, 2, 3]
list2 = [4, 5, 6]
list3 = list1 + list2
print(list3)
list4 = []
list4.append(list1)
list4.append(list2)  # List of lists
print(list4)  # Access a list in a list
print(list4[1][2])  # Access an element in a list in a list


# ==============================================================================


# Numbers
print("\nNumbers\n")

x = 10
x = 0b10  # Adds binary (rvalue) to integer (lvalue)
print(x)
x = 10
print(bin(x))  # Print binary

x = 0x12c  # Hex
print(x)
x = 10
print(hex(10))

# Complex numbers 1 + 2i
x = 1 + 2j  # Constructs a complex number class (This is insane)
print(x)


# Arithmatic
x = 10 + 3
x = 10 - 3
x = 10 * 3
x = 10 % 3
x = 10 / 3  # division (float)
x = 10 // 3  # int division
x = 10 ** 3  # pow(value, exponent)

# Augmented assignment operator:
# x = *operator= 5

# No increment or decrement ++ or -- :(

PI = 3.14  # Variables uppercase are seen as constant
round(PI)
abs(PI)
# Look up Built in Functions in Python

# Math package (math)
x = 1
math.acos(x)


# ==============================================================================


# Type conversion
print("\nType conversion\n")
# x = input("x: ") INPUT
y = int(x) + 1
print(y)
"""Whats going on?
The compliler is confused, the varible x is read in as string however is used in the
next line as an integer. The compiler is unsure as to if y should be a string or an int
so type specification is now required to run code.
"""
int()
float()
bool()  # 0/NULL = False, non-zero = True
str()

x = 3.5
print(int(x))


# Conditional statements
print("\nConditional Statements\n")
# ==
# !=
# >=
# <=
age = 22
# If : No braces, but require colon
if age >= 18:
    print("Adult")
elif age >= 13:
    print("Teenager")
else:
    print("Child")

# Use pass for empty block
if age == 20:
    pass
else:
    pass


# ==============================================================================


# Logical Operators
print("\nLogical Operators\n")
# and
# or
# not
# in
# is

x = "5"
y = 5
print(x is y)  # Checks for same type and value

name = ""
if not name:  # Check for empty String
    print("String empty")
""" Whats going on?
In C++ we would simply do varibale.empty() and this would return true if it was empty,
here in python the if statement needs a value of 1/true to run the indented lines.
By writing name we are passing the value of name and this will only be 0 if it is empty,
so to invert the 0 we place the not operator to invert an empty string to return 1
instead of 0.
Simply put:
name will return 0 if it is empty
not will invert 0 to 1
if will only run if (not name) is true/1
"""

if age >= 18 and age < 65:
    print("Eligible")
if age >= age < 65:  # Chain operators
    print("Eligible")

# Python Terniary Operator
age = 22
# operation ? true : false
# C++: message = age >= 18 ? "Eligible": "Not eligible"

# (true expression) if (operation) else (false expression)
message = "Eligible" if age >= 18 else "Not eligible"
print(message)


# ==============================================================================


# For loops
print("\nfor Loops\n")
for x in "Python":  # Iterates over string
    print(x, end="")

for x in ['a', 'b', 'c']:  # Iterates over list
    print(x, end=" ")

for x in range(2, 5):
    print(x, end=" ")

for x in range(0, 10, 2):  # (begin, end, step)
    print(x, end=" ")

# New type: 'range'
x = range(5000)
print(type(x))
# Creates an object with a range of 5000 and not 5000 objets
# more efficient


# New: for else loops
print("\nfor else Loop\n")
names = ["John", "Mary"]
for name in names:
    if name.startswith("j"):
        print("Found")
        break
else:  # else statement only executed if for loop breaks naturally
    print("Not found")


# while loop
print("\nWhile Loop\n")
guess = 5  # INPUT
answer = 5

while answer != guess:
    guess = int(input("Guess: "))
else:  # If while completes without break will move to else
    pass


# ==============================================================================


# Functions
print("\nFunctions\n")


def increment(number, factor):  # Function without a specifier will return null
    return number + factor


print(increment(10, 5))
print(increment(number=10, factor=3))  # Keyword Argument

# New Type: Tuple (Unmodifible List)
myTuple = ("String", 5)
print(myTuple)


def twoTypeReturn(type1, type2):  # multiple return types
    return type1, type2


x = twoTypeReturn("Str", 5)
print(x)

# Sane way of functions


def saneFunction(number: int, factor: int) -> int:  # Return type
    pass


# Assign function to variable
mystery = increment
print(mystery(10, 2))

# Default parameter


def sum(a, b, c=10):
    return a + b + c


print(sum(3, 4))


# ==============================================================================


# Pointers?
print("\nPointers\n")


def multiply(*list, myInt):  # pointer before parameter reads as tuple
    # Pass in an arbitary amount of arguments
    print(f"{list} {myInt}")


# Arg specification required otherwise will be packed as tuple
multiply(1, 2, 3, 4, myInt=5)


def save_user(**user):  # Double pointer (Kind of like passing in an object)
    print(user)
    print(user["id"])
    print(user["name"])  # Only print key values


save_user(id=1, name="admin")
""" Whats going on?
passing in key and value, this is essentially a C++ map.
Or in python terms a dictionary
"""

# The backslash (\escapeCharacter)
message = "Python \"Programming"
# \" Display the next character
# \' ^
# \\ ^^
# \n New line
