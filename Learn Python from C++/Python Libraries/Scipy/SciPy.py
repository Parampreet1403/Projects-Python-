# Parampreet Singh - 22/06/20
# brief exploration SciPy package

import matplotlib.pyplot as plt
from scipy import interpolate as intpol
from scipy import linalg
from scipy.fftpack import fft, ifft
from scipy import integrate
from scipy import special
import numpy as np

a = special.exp10(3)  # 10 ** 3
print(a)

a = special.sindg(90)  # sin value in degress
print(a)

# integration
# integrate.quad(expression, lower limit, upper limit)
a = integrate.quad(lambda x: x**2, 0, 1)
# quad is a single varibale
# dblquad is two variables
print(a)

# integrate.quad(expression, lower limit, upper limit, lower(2nd), upper(2nd))
a = integrate.dblquad(lambda x, y: x**2 + y**2, 0, 1, 0, 1)
print(a)


# Fourier transformation
x = np.array([1, 2, 3, 4])
y = ifft(x)  # inverse
print(y)

# Linear Algebra
a = np.array([[1, 2], [3, 4]])
b = linalg.inv(a)  # Inverse of matrix
print(b)

# Interpolation Function
x = np.arange(5, 20)
y = np.exp(x/3.0)
f = intpol.interp1d(x, y)
x1 = np.arange(6, 12)
y1 = f(x1)  # use interpolation function returned by interp1d
plt.plot(x, y, "o", x1, y1, "--")
plt.show()
