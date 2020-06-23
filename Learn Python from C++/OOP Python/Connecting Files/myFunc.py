# Parampreet Singh - 20/06/20
# Python algorithm

""" If input divisible by 3 it will return fizz
if divisible by 5 return buzz
if divisible by 3 and 5 return fizz buzz
else return same input

"""


def fizz_buzz(input):
    if (input % 3 == 0) and (input % 5 == 0):
        print("Fizz Buzz")
    elif ((input % 5) == 0):
        print("Buzz")
    elif ((input % 3) == 0):
        print("Fizz")
    else:
        print(input)


fizz_buzz(17)
