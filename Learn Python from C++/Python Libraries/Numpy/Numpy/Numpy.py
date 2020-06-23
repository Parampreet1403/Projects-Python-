# Parampreet Singh - 22/06/20
# Learn Numpy Package
# Multi dimensional array library

import numpy as np

# Basics
print("\nBasics\n")
a = np.array([1, 2, 3])
print(a)

b = np.array([[1, 2, 3], [4, 5, 6]], dtype="int8")
print(b)
print(b.ndim)
print(b.shape)  # 2 rows and 3 columns
print(b.dtype)  # data type


# Accessing
print("\nAccessing\n")
a = np.array([[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]])
print(a)

# Get an element [row, column]
print(a[1, 2])  # 9

# Get a row
print(a[0, :])

# Get a column
print(a[:, 2])  # 3, 9

# [start index : end index : stepsize]
print(a[0, 1:5:])


# initilising different types of arrays
print("\n Matrix\n")
a = np.zeros(5)  # FIll with 0
print(a)
a = np.zeros((2, 3))
print(a)
a = np.ones((4, 4))  # Fill with 1
print(a)
a = np.full((5, 5), 25)  # filled matrix
print(a)

# full_like(numpy array, number)
b = np.full_like(a, 7)  # Absorbs shape
print(b)

# Random decimal numbers
a = np.random.rand(4, 2)  # creates shape
print(a)
b = np.random.random_sample(a.shape)  # Passes shape
print(b)

a = np.random.randint(1, 7, size=(3, 3))  # Random numbers from beg to end
print(a)

a = np.identity(5)  # creates identity matrix
print(a)

a = np.array([1, 2, 3, 4, 5])
b = np.repeat(a, 3)  # Repeats element in argument x times
print(b)

a = np.array([[1, 2, 3, 4, 5]])  # 2D array
b = np.repeat(a, 3, axis=0)  # Repeats element in argument x times
print(b)

# Problem 1: Create this Matrix
"""
1 1 1 1 1
1 0 0 0 1
1 0 9 0 1
1 0 0 0 1
1 1 1 1 1
"""
output = np.ones((5, 5))
print(output)
inner_square = np.zeros((3, 3))
inner_square[1, 1] = 9
print(inner_square)
output[1:4, 1:4] = inner_square
print(output)


# Maths
print("\nMaths\n")
a = np.array([1, 2, 3, 4])
print(a)
a += 2  # Affects all elements in array
print(a)
a -= 2
print(a)
a *= 2
print(a)
a //= 2
print(a)

b = np.array([0, 1, 0, 1])
print(a+b)

print(np.sin(a))


# Linear Algebra
print("\n Linear Algebra\n")
a = np.ones((2, 3))
print(a)
b = np.full((3, 2), 2)
print(b)
# (Columns == Rows)
c = np.matmul(a, b)  # Multipies matrix
print(c)

# Find the determinant
a = np.identity(3)
b = np.linalg.det(a)
print(b)


# Statistics
print("\nStatistics\n")
a = np.array([[1, 2, 3], [4, 5, 6]])
print(a)
print(np.min(a))  # Find Min
print(np.max(a))  # Find Max
print(np.min(a, axis=1))

print(np.sum(a))  # Sum


# Reorganising arrays
print("\nReorganising Arrays\n")
a = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
print(a)

b = a.reshape((4, 2))
print(b)

# Vertical Stacks
a = np.array([1, 2, 3, 4])
b = np.array([5, 6, 7, 8])
c = np.vstack([a, b, a, a])
print(c)

# Horizontal Stacks
c = np.hstack([a, b, a, a])
print(c)


# Miscellaneous
print("\nMiscellaneous\n")
data = np.genfromtxt("Np_file.txt", delimiter=",")  # Read data from file
print(data)
print(data.astype("int32"))  # Specify data type

# Boolean masking and Advanced Indexing
print(data > 5)  # Comparison of data
print(data[data > 5])  # find values which satisfy operation

# Index in numpy array
a = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
print(a[[0, 1, -1]])  # Acessing element in array

# which columns satisfy operation on specified axis
print(np.any(data > 5, axis=0))

# which columns have all elements satisfying operation on specified axis
print(np.all(data > 5, axis=0))

print(np.all(data > 5, axis=1))  # Rows

print((data > 3) & (data < 5))
print(~((data > 3) & (data < 5)))  # ~ equivalent of not
