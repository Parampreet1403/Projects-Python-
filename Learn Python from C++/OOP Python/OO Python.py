# Parampreet Singh - 20/06/20
# Object Oriented Programming in Python

import math


class Asteroid(object):  # Declare class as object

    def __init__(self, x, y):  # Constructor
        self.x = x  # Self is bassically "this->"
        self.y = y
        """ Whats going on
        Self is bassically "this->"
        But because to create a class in Python we need to make a class in C
        to call type class. 
        We are essentially making a class inside a class (CLASSception ;) )
        SO self needs to be passed as an argument to be read by the function
        but doesn't need ot be passed when calling the function
        as its kinda of "in built" into python

        *Note this is how I think it works not how it acctually does
        """

    def getX(self):  # Accessing private variables
        return self.x  # But in this case everything is public
        # So just varibles declared in constructor

    def getY(self):
        return self.y

    def computeDistance(self, otherA):  # Member Function
        # Note we do not need to declare type asteroid in arguments
        # d**2 = x**2 + y**2
        distX = self.x - otherA.getX()
        distY = self.y - otherA.getY()
        return math.sqrt((distX**2) + (distY**2))


a1 = Asteroid(0, 0)
a2 = Asteroid(3, 4)
print(a1.computeDistance(a2))


class Dog:

    def __init__(self, name, age):
        self._name = name  # Underscore represents private variable
        self._age = age

    def get_age(self):
        return self._age

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def set_age(self, age):
        self.age = age

    def __str__(self):  # When we try to print the class (Overloading std::cout)
        return "Dog:\nName: " + self._name + "\nAge: " + str(self._age)

    def random():  # No link to instance
        return 7


dog1 = Dog("Scruffy", 5)
print(dog1)
print(dog1.get_age())

print(Dog.random())  # Can use class to access functions
