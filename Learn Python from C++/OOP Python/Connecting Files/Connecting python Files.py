# Parampreet Singh - 22/06/20
# Connecting Files

import myFunc as f  # Import .py file name
import sys  # import sys package to locate directory

# Import file directory
sys.path.append(
    "C:/Users/param/Desktop/Programming/Projects Python/Re-Learning Python")


f.fizz_buzz(15)  # Functions are derivative of name

# Note: .py names must have underscore for space, space causes an error
# e.g. my file name (WRONG)
#      my_file_name (RIGHT)

# This is a way you can import objects
