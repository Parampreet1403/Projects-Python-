"""
Parampreet Singh - (01/03/19)
Computational Physics - Project 1
"""

#Import Packages 
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.interpolate import interp1d

#Functoins

#Finds the mean of 2 values
def mean(x, y):
    z = []
    for i in range (0, len(x)):
        temp1 = (x[i] + y[i]) / 2
        z.append(temp1)
    return(z);

#Finds the mean of 3 values
def mean_3(x, y, q):
    z = []
    for i in range (0, len(x)):
        temp1 = (x[i] + y[i] + q[i]) / 3
        z.append(temp1)
    return(z);

#Finds Standard deviation of two given lists 
def standard_deviation_2values(x, y):
    temp1 = []
    for i in range (0, len(x)):
        temp2 = (x[i], y[i])
        temp1.append(np.std(temp2))
    return(temp1);
    
#Finds Standard deviation of 3 given lists 
def standard_deviation_3values(x, y, z):
    temp1 = []
    for i in range (0, len(x)):
        temp2 = (x[i], y[i], z[i])
        temp1.append(np.std(temp2))
    return(temp1);    
    
#Finding maximum droplet height
def maximum_droplet_height(x):
    V = 7600 #Volume of droplet in micro m^3 (7.6pL)
    max_drop_height = []
    for i in range (0, len(x)):
        #Puts coeficients of max droplet height in order of decreasing power 
        temp1 = np.array([1, 0, 3*np.square(x[i]), -6*V/math.pi])
        temp2 = np.roots(temp1) #Finds roots for max drop height
        max_drop_height.append(temp2[2].real) #Only appends real part of the real root 
    return(max_drop_height);
    
#Finding theta
def theta(x, h):
    theta = []
    for i in range (0, len(x)):
        temp1 = math.atan((np.square(x[i]) - np.square(h[i])) / (2*x[i]*h[i])) #Intermediate calculation
        temp2 = (math.pi/2) - temp1
        theta.append(temp2)
    return(theta);

#Finding velocity
def velocity(x, t):
    velocity = []
    for i in range(0, len(x) - 1):
        temp1 = (x[i+1]-x[i])/(t[i+1]-t[i])
        velocity.append(temp1)
    return(velocity);

#Error propagation of 1 value:
def error_propagation_1value(x):
    sigma = []
    for i in range (0, len(x) -1):
        sigma.append(np.sqrt(np.square(x[i+1]) + np.square(x[i])))
    return(sigma);
    
#Squares given value
def square(x):
    y = np.square(x)
    return(y);
    
#Cubes given value
def cube(x):
    z = np.array(x)
    y = np.power(z, 3)
    return(y);    
    
#Graph plotting
def plot(number, x, y, y_error, title, xlab, ylab):
    plt.figure(number)
    plt.grid()
    plt.ylabel(ylab)
    plt.xlabel(xlab)
    plt.title(title)
    plt.errorbar(x, y, yerr = y_error, ecolor = "r")
    return;
#Finding the error on max droplet height, h
def sigma_height(x, y, z):
    x_2 = np.square(x)
    y_2 = np.square(y)
    sigma_h = z * ((x_2 + y_2) / (2*np.array(x)*np.array(y)))
    return(sigma_h);

#Finding error on contact angle, theta
def sigma_theta(x, sigma_x, y, sigma_y, z):
    error_x = sigma_x/np.array(x) 
    error_y = sigma_y/np.array(y) 
    sigma_z = z* np.sqrt(np.square(2*error_x + 2*error_y) + np.square(error_x) + np.square(error_y)) # error on contact angle
    return(sigma_z);

#Function to find chi squared   
def chi_squared(y, y_fit, y_err):
    temp1 = np.square( (np.array(y) - np.array(y_fit) ) / np.array(y_err)) 
    temp2 = np.sum(temp1)
    return(temp2);
    
#Function to find reduced chi squared   
def reduced_chi_squared(y, chi, parameters, type_):
    temp1 = (chi) / ( len(y) - parameters)
    print("\n" + str(type_) + " Reduced Chi-Square of: %f6.2" %(temp1))
    return(temp1);
    
#Function to interpolate velocity to a range of theta values
def interpolate_velocity(theta, velocity):
    temp1 = np.linspace(theta[0], theta[-1], len(velocity)) # Equally spaced x values in the range of theta
    temp2 = interp1d(theta[:-1], velocity, kind = "linear", fill_value = "extrapolate") #Function for the linear graph of (x, y)
    temp3 = temp2(temp1) # Y-values associated with the function f for the values of (x) # y = f(x)
    #y = f(x)
    return(temp3);
    
#Finding the fitting coefficients    
def coefficient(x, y, n, type_): #y = mx + c (U = U_0*theta^n - U_0*theta_0^n)
                                 #y = U, m = U_0,
    x_n = np.power( np.array(x), n)
    gradient = (y[1] - y[0]) - (x[1] - x[0])
    velocity_nort = gradient
    y_intercept = y[0] - (gradient * x_n[0]) # -U. * (theta.)^n
    theta_nort = y_intercept/(-1*gradient)
    print("\n" +  str(type_) + " Fitting coefficients for \n Velocity: %f6.2 and Theta^" %(velocity_nort)+ str(n) 
                                                    + ": %6.2f" %(theta_nort))
    return(velocity_nort, theta_nort);

print("\n                                               ***RESULTS***    ")

#Read in data
drop2_time = np.loadtxt('Drop_2_data_run1.txt', dtype=float, usecols=(0)) #Units = seconds
drop2_radius_run1 = np.loadtxt('Drop_2_data_run1.txt', dtype=float, usecols=(1)) #Units = micro meter
drop2_radius_run2 = np.loadtxt('Drop_2_data_run2.txt', dtype=float, usecols=(1)) #Units = micro meter

drop1_time = np.loadtxt('Drop_1_data_run1.txt', dtype=float, usecols=(0)) #Units = seconds
drop1_radius_run1 = np.loadtxt('Drop_1_data_run1.txt', dtype=float, usecols=(1)) #Units = micro meter
drop1_radius_run2 = np.loadtxt('Drop_1_data_run2.txt', dtype=float, usecols=(1)) #Units = micro meter
drop1_radius_run3 = np.loadtxt('Drop_1_data_run3.txt', dtype=float, usecols=(1)) #Units = micro meter

#Finding mean radius
drop2_radius_mean = mean(drop2_radius_run1, drop2_radius_run2) #Units = micro meter

drop1_radius_mean = mean_3(drop1_radius_run1, drop1_radius_run2, drop1_radius_run3 ) #Units = micro meter

#Finding error on mean radius
drop2_sigma_radius_mean = standard_deviation_2values(drop2_radius_run1, drop2_radius_run2)

drop1_sigma_radius_mean = standard_deviation_3values(drop1_radius_run1, drop1_radius_run2, drop1_radius_run3)

#Method 1 (Propagation) 
#Relating radius, R, to conact angle, Theta, via finding max drop height, h.
drop2_mean_radius_height = maximum_droplet_height(drop2_radius_mean) #Units = micro meter
drop2_mean_radius_theta = theta(drop2_radius_mean, drop2_mean_radius_height) #Units = radians

drop1_mean_radius_height = maximum_droplet_height(drop1_radius_mean) #Units = micro meter
drop1_mean_radius_theta = theta(drop1_radius_mean, drop1_mean_radius_height) #Units = radians

#Finding velocity and error
#drop2_mean_radius_34theta = drop2_mean_radius_theta[:-1] #Contact angle with 34 points
drop2_mean_radius_velocity = velocity(drop2_radius_mean, drop2_time) #Units = micro meter / seconds
drop2_sigma_propagation_velocity = error_propagation_1value(drop2_sigma_radius_mean) #Units = micro meter / seconds
drop2_sigma_propagation_height = sigma_height(drop2_radius_mean, drop2_mean_radius_height, drop2_sigma_radius_mean) #Units = micro meter
drop2_sigma_propagation_theta = sigma_theta(drop2_radius_mean, drop2_sigma_radius_mean, drop2_mean_radius_height, 
                                            drop2_sigma_propagation_height, drop2_mean_radius_theta) #Units = radians

drop1_mean_radius_velocity = velocity(drop1_radius_mean, drop1_time) #Units = micro meter / seconds
drop1_sigma_propagation_velocity = error_propagation_1value(drop1_sigma_radius_mean) #Units = micro meter / seconds
drop1_sigma_propagation_height = sigma_height(drop1_radius_mean, drop1_mean_radius_height, drop1_sigma_radius_mean) #Units = micro meter
drop1_sigma_propagation_theta = sigma_theta(drop1_radius_mean, drop1_sigma_radius_mean, drop1_mean_radius_height, 
                                            drop1_sigma_propagation_height, drop1_mean_radius_theta) #Units = radians

#Method 2 (Data spread)
#Finding velocity and error
drop2_velocity_run1 = velocity(drop2_radius_run1, drop2_time)
drop2_velocity_run2 = velocity(drop2_radius_run2, drop2_time)
drop2_velocity_mean = mean(drop2_velocity_run1, drop2_velocity_run2)
drop2_sigma_spread_velocity = standard_deviation_2values(drop2_velocity_run1, drop2_velocity_run2)

drop1_velocity_run1 = velocity(drop1_radius_run1, drop1_time)
drop1_velocity_run2 = velocity(drop1_radius_run2, drop1_time)
drop1_velocity_run3 = velocity(drop1_radius_run3, drop1_time)
drop1_velocity_mean = mean_3(drop1_velocity_run1, drop1_velocity_run2, drop1_velocity_run3)
drop1_sigma_spread_velocity = standard_deviation_3values(drop1_velocity_run1, drop1_velocity_run2, drop1_velocity_run3)

#Finding maximum droplet height
drop2_height_run1 = maximum_droplet_height(drop2_radius_run1)
drop2_height_run2 = maximum_droplet_height(drop2_radius_run2)

drop1_height_run1 = maximum_droplet_height(drop1_radius_run1)
drop1_height_run2 = maximum_droplet_height(drop1_radius_run2)
drop1_height_run3 = maximum_droplet_height(drop1_radius_run3)

#Finding contact angle and error
drop2_theta_run1 = theta(drop2_radius_run1, drop2_height_run1)
drop2_theta_run2 = theta(drop2_radius_run2, drop2_height_run2)
drop2_theta_mean = mean(drop2_theta_run1, drop2_theta_run2)
drop2_sigma_spread_theta = standard_deviation_2values(drop2_theta_run1, drop2_theta_run2)

drop1_theta_run1 = theta(drop1_radius_run1, drop1_height_run1)
drop1_theta_run2 = theta(drop1_radius_run2, drop1_height_run2)
drop1_theta_run3 = theta(drop1_radius_run3, drop1_height_run3)
drop1_theta_mean = mean_3(drop1_theta_run1, drop1_theta_run2, drop1_theta_run3)
drop1_sigma_spread_theta = standard_deviation_3values(drop1_theta_run1, drop1_theta_run2, drop1_theta_run3)

#Plotting Time against Mean Radius for Drop 2
plot(1, drop2_time, drop2_radius_mean, drop2_sigma_radius_mean, "Drop 2: Mean Radius against Time", "Time (s)", 
     "Mean Radius ($\mu$m)")

#Plotting Contact Angle against Time - Propagation
plot(3, drop2_time, drop2_mean_radius_theta, drop2_sigma_propagation_theta, "Drop 2: Contact Angle against Time (Propagation)", "Time (s)",
     "Contact Angle (radians)")

#Plotting Time against Contact Angle - Data spread
plot(4, drop2_time, drop2_theta_mean, drop2_sigma_spread_theta, "Drop 2: Contact Angle against Time (Data Spread)", "Time (s)",
     "Contact Angle (radians)")

#Plotting Contact Angle against Contact Line Velocity - Propagation
plot(7, drop2_mean_radius_theta[:-1], drop2_mean_radius_velocity, drop2_sigma_propagation_velocity, "Drop 2: Contact Angle against Velocity (Propagation)",
     "Contact Angle (radians)", "Velocity ($\mu$m/s)")

#Plotting Contact Angle against Contact Line Velocity - Data spread
plot(8, drop2_theta_mean[:-1], drop2_velocity_mean, drop2_sigma_spread_velocity, "Drop 2: Contact Angle against Velocity (Data Spread)",
     "Contact Angle (radians)", "Velocity ($\mu$m/s)")

#From the graphs it can be seen that the lowest errror is achieved from using data spread (Method 2) 
#for finding the error on contact angle and propagation for velocity (Method 1)  
#however the error for velocity seems to be too small for propagtion so from this point onward I will be using data spread (Method 2)
#drop2_theta_mean +/- drop2_sigma_spread_theta (Method 2)
#drop2_velocity_mean +/- drop2_sigma_spread_velocity (Method 2)

#Plotting Time against Mean Radius for Drop 1
plot(2, drop1_time, drop1_radius_mean, drop1_sigma_radius_mean, "Drop 1: Mean Radius against Time", "Time (s)", 
     "Mean Radius ($\mu$m)")

#Plotting Contact Angle against Time - Propagation
plot(5, drop1_time, drop1_mean_radius_theta, drop1_sigma_propagation_theta, "Drop 1: Contact Angle against Time (Propagation)", "Time (s)",
     "Contact Angle (radians)")

#Plotting Time against Contact Angle - Data spread
plot(6, drop1_time, drop1_theta_mean, drop1_sigma_spread_theta, "Drop 1: Contact Angle against Time (Data Spread)", "Time (s)",
     "Contact Angle (radians)")

#Plotting Contact Angle against Contact Line Velocity - Propagation
plot(9, drop1_mean_radius_theta[:-1], drop1_mean_radius_velocity, drop1_sigma_propagation_velocity, "Drop 1: Contact Angle against Velocity (Propagation)",
     "Contact Angle (radians)", "Velocity ($\mu$m/s)")

#Plotting Contact Angle against Contact Line Velocity - Data spread
plot(10, drop1_theta_mean[:-1], drop1_velocity_mean, drop1_sigma_spread_velocity, "Drop 1: Contact Angle against Velocity (Data Spread)",
     "Contact Angle (radians)", "Velocity ($\mu$m/s)")

#Similarly it is clear that data spread is the best method to use as the errors are best i.e. smallest
#drop1_theta_mean +/- drop1_sigma_spread_theta (Method 2)
#drop1_velocity_mean +/- drop1_sigma_spread_velocity (Method 2)

#Graph Fitting

#I am also assuming that there is no error on theta linear as this is essentially my 'time'

#Using mean theta and velocity (Method 1)
drop2_theta_linear = np.linspace(drop2_theta_mean[0], drop2_theta_mean[-1], len(drop2_theta_mean[:-1])) # Equally spaced x values in the range of theta
drop2_f_velocity_mean = interp1d(drop2_theta_mean[:-1], drop2_velocity_mean, kind = "linear", fill_value = "extrapolate") #Function for the linear graph of (x, y)
drop2_interpolated_velocity = drop2_f_velocity_mean(drop2_theta_linear) # Y-values associated with the function f for the values of (x) # y = f(x)

drop1_theta_linear = np.linspace(drop1_theta_mean[0], drop1_theta_mean[-1], len(drop1_theta_mean[:-1])) # Equally spaced x values in the range of theta
drop1_f_velocity_mean = interp1d(drop1_theta_mean[:-1], drop1_velocity_mean, kind = "linear", fill_value = "extrapolate") #Function for the linear graph of (x, y)
drop1_interpolated_velocity = drop1_f_velocity_mean(drop1_theta_linear) # Y-values associated with the function f for the values of (x) # y = f(x)

#Finding the mean interpolated velocity and error via data spread (Method 2)
drop2_interpolated_velocity_run1 = interpolate_velocity(drop2_theta_run1, drop2_velocity_run1)
drop2_interpolated_velocity_run2 = interpolate_velocity(drop2_theta_run2, drop2_velocity_run2)
drop2_interpolated_velocity_mean = mean(drop2_interpolated_velocity_run1, drop2_interpolated_velocity_run2 )

drop1_interpolated_velocity_run1 = interpolate_velocity(drop1_theta_run1, drop1_velocity_run1)
drop1_interpolated_velocity_run2 = interpolate_velocity(drop1_theta_run2, drop1_velocity_run2)
drop1_interpolated_velocity_run3 = interpolate_velocity(drop1_theta_run3, drop1_velocity_run3)
drop1_interpolated_velocity_mean = mean_3(drop1_interpolated_velocity_run1, drop1_interpolated_velocity_run2,drop1_interpolated_velocity_run3 )


#Error on inerpolated velocity via data spread
drop2_sigma_interpolated_velocity_mean = standard_deviation_2values(drop2_interpolated_velocity_run1, drop2_interpolated_velocity_run2)

drop1_sigma_interpolated_velocity_mean = standard_deviation_3values(drop1_interpolated_velocity_run1, drop1_interpolated_velocity_run2, drop1_interpolated_velocity_run3)

#drop2_interpolated_velocity_mean and drop2_interpolated_velocity are similar values leading me to believe that Meythod is okay to use
#Same for drop 1

#De-Gennes Law
(drop2_coefficient_gennes, drop2_covariance_gennes) = np.polyfit(square(drop2_theta_linear), drop2_interpolated_velocity_mean, 1, cov = True)
parameter_gennes = 2
drop2_fitted_velocity_gennes = np.polyval(drop2_coefficient_gennes, square(drop2_theta_linear)) #Evaluate coeff at the discrete points of theta^n (coeff is of all the curve)

#Calculating Chi squared and Reduced Chi squared
drop2_chi_squared_gennes = chi_squared(drop2_interpolated_velocity_mean, drop2_fitted_velocity_gennes, drop2_sigma_interpolated_velocity_mean)
drop2_chi_squared_reduced_gennes = reduced_chi_squared(drop2_interpolated_velocity_mean, drop2_chi_squared_gennes, parameter_gennes, "Drop 2: De-Gennes Law")

#Graph 11 Plotting De-Gennes Law Fit
plt.figure(11)
plt.errorbar(drop2_theta_linear, drop2_interpolated_velocity_mean, yerr = drop2_sigma_interpolated_velocity_mean, ecolor = "r" )
plt.plot(drop2_theta_linear, drop2_interpolated_velocity_mean)
plt.plot(drop2_theta_linear, drop2_fitted_velocity_gennes, color = "y")
plt.xlabel("Linear Contact angle (radians)")
plt.ylabel("Velocity ($\mu$m/s) ")
plt.title("Drop2 : De-Gennes Law fitted onto linear contact angle against linear interpolated velocity")
plt.grid()

(drop1_coefficient_gennes, drop1_covariance_gennes) = np.polyfit(square(drop1_theta_linear), drop1_interpolated_velocity_mean, 1, cov = True)
drop1_fitted_velocity_gennes = np.polyval(drop1_coefficient_gennes, square(drop1_theta_linear)) #Evaluate coeff at the discrete points of theta^n (coeff is of all the curve)

#Calculating Chi squared and Reduced Chi squared
drop1_chi_squared_gennes = chi_squared(drop1_interpolated_velocity_mean, drop1_fitted_velocity_gennes, drop1_sigma_interpolated_velocity_mean)
drop1_chi_squared_reduced_gennes = reduced_chi_squared(drop1_interpolated_velocity_mean, drop1_chi_squared_gennes, parameter_gennes, "Drop 1: De-Gennes Law")

#Graph 12 Plotting De-Gennes Law Fit
plt.figure(12)
plt.errorbar(drop1_theta_linear, drop1_interpolated_velocity_mean, yerr = drop1_sigma_interpolated_velocity_mean, ecolor = "r" )
plt.plot(drop1_theta_linear, drop1_interpolated_velocity_mean)
plt.plot(drop1_theta_linear, drop1_fitted_velocity_gennes, color = "y")
plt.xlabel("Linear Contact angle (radians)")
plt.ylabel("Velocity ($\mu$m/s) ")
plt.title("Drop1 : De-Gennes Law fitted onto linear contact angle against linear interpolated velocity")
plt.grid()

#Cox-Voinov Law
(drop2_coefficient_cox, drop2_covariance_cox) = np.polyfit(cube(drop2_theta_linear), drop2_interpolated_velocity_mean, 1, cov = True)
parameter_cox = 3
drop2_fitted_velocity_cox = np.polyval(drop2_coefficient_cox, cube(drop2_theta_linear)) #Evaluate coeff at the discrete points of theta^n (coeff is of all the curve)

#Calculating Chi squared and Reduced Chi squared
drop2_chi_squared_cox = chi_squared(drop2_interpolated_velocity_mean, drop2_fitted_velocity_cox, drop2_sigma_interpolated_velocity_mean)
drop2_chi_squared_reduced_cox = reduced_chi_squared(drop2_interpolated_velocity_mean, drop2_chi_squared_cox, parameter_cox, "Drop 2: Cox-Voinov Law")

#Graph 13 Plotting Cox-Voinov Law Fit
plt.figure(13)
plt.errorbar(drop2_theta_linear, drop2_interpolated_velocity_mean, yerr = drop2_sigma_interpolated_velocity_mean, ecolor = "r" )
plt.plot(drop2_theta_linear, drop2_interpolated_velocity_mean)
plt.plot(drop2_theta_linear, drop2_fitted_velocity_cox, color = "y")
plt.xlabel("Linear Contact angle (radians)")
plt.ylabel("Velocity ($\mu$m/s) ")
plt.title("Drop2 : Cox-Voinov Law fitted onto linear Contact Angle against linear Interpolated Velocity")
plt.grid()

(drop1_coefficient_cox, drop1_covariance_cox) = np.polyfit(cube(drop1_theta_linear), drop1_interpolated_velocity_mean, 1, cov = True)
drop1_fitted_velocity_cox = np.polyval(drop1_coefficient_cox, cube(drop1_theta_linear)) #Evaluate coeff at the discrete points of theta^n (coeff is of all the curve)

#Calculating Chi squared and Reduced Chi squared
drop1_chi_squared_cox = chi_squared(drop1_interpolated_velocity_mean, drop1_fitted_velocity_cox, drop1_sigma_interpolated_velocity_mean)
drop1_chi_squared_reduced_cox = reduced_chi_squared(drop1_interpolated_velocity_mean, drop1_chi_squared_cox, parameter_cox, "Drop 1: Cox-Voinov Law")

#Graph 14 Plotting Cox-Voinov Law Fit
plt.figure(14)
plt.errorbar(drop1_theta_linear, drop1_interpolated_velocity_mean, yerr = drop1_sigma_interpolated_velocity_mean, ecolor = "r" )
plt.plot(drop1_theta_linear, drop1_interpolated_velocity_mean)
plt.plot(drop1_theta_linear, drop1_fitted_velocity_cox, color = "y")
plt.xlabel("Linear Contact angle (radians)")
plt.ylabel("Velocity ($\mu$m/s) ")
plt.title("Drop1 : Cox-Voinov Law fitted onto linear Contact Angle against linear Interpolated Velocity")
plt.grid()

#Cubic Fit
(drop2_coefficient_cubic, drop2_covariance_cubic) = np.polyfit(drop2_theta_linear, drop2_interpolated_velocity_mean, 3, cov = True)
parameter_cubic = 3
drop2_fitted_velocity_cubic = np.polyval(drop2_coefficient_cubic, drop2_theta_linear) #Evaluate coeff at the discrete points of theta^n (coeff is of all the curve)

#Calculating Chi squared and Reduced Chi squared
drop2_chi_squared_cubic = chi_squared(drop2_interpolated_velocity_mean, drop2_fitted_velocity_cubic, drop2_sigma_interpolated_velocity_mean)
drop2_chi_squared_reduced_cubic = reduced_chi_squared(drop2_interpolated_velocity_mean, drop2_chi_squared_cubic, parameter_cubic, "Drop 2: Cubic Fit")

#Graph 15 Plotting Cubic Fit
plt.figure(15)
plt.errorbar(drop2_theta_linear, drop2_interpolated_velocity_mean, yerr = drop2_sigma_interpolated_velocity_mean, ecolor = "r" )
plt.plot(drop2_theta_linear, drop2_interpolated_velocity_mean)
plt.plot(drop2_theta_linear, drop2_fitted_velocity_cubic, color = "y")
plt.xlabel("Linear Contact angle (radians)")
plt.ylabel("Velocity ($\mu$m/s) ")
plt.title("Drop2 : Cubic fit fitted onto linear Contact Angle against linear Interpolated Velocity")
plt.grid()

(drop1_coefficient_cubic, drop1_covariance_cubic) = np.polyfit(drop1_theta_linear, drop1_interpolated_velocity_mean, 3, cov = True)
drop1_fitted_velocity_cubic = np.polyval(drop1_coefficient_cubic, drop1_theta_linear) #Evaluate coeff at the discrete points of theta^n (coeff is of all the curve)

#Calculating Chi squared and Reduced Chi squared
drop1_chi_squared_cubic = chi_squared(drop1_interpolated_velocity_mean, drop1_fitted_velocity_cubic, drop1_sigma_interpolated_velocity_mean)
drop1_chi_squared_reduced_cubic = reduced_chi_squared(drop1_interpolated_velocity_mean, drop1_chi_squared_cubic, parameter_cubic, "Drop 1: Cubic Fit")

#Graph 16 Plotting Cubic Fit
plt.figure(16)
plt.errorbar(drop1_theta_linear, drop1_interpolated_velocity_mean, yerr = drop1_sigma_interpolated_velocity_mean, ecolor = "r" )
plt.plot(drop1_theta_linear, drop1_interpolated_velocity_mean)
plt.plot(drop1_theta_linear, drop1_fitted_velocity_cubic, color = "y")
plt.xlabel("Linear Contact angle (radians)")
plt.ylabel("Velocity ($\mu$m/s) ")
plt.title("Drop1 : Cubic fit fitted onto linear Contact Angle against linear Interpolated Velocity")
plt.grid()

#Quadratic Fit
(drop2_coefficient_square, drop2_covariance_square) = np.polyfit(drop2_theta_linear, drop2_interpolated_velocity_mean, 2, cov = True)
parameter_square = 2
drop2_fitted_velocity_square = np.polyval(drop2_coefficient_square, drop2_theta_linear) #Evaluate coeff at the discrete points of theta^n (coeff is of all the curve)

#Calculating Chi squared and Reduced Chi squared
drop2_chi_squared_square = chi_squared(drop2_interpolated_velocity_mean, drop2_fitted_velocity_square, drop2_sigma_interpolated_velocity_mean)
drop2_chi_squared_reduced_square = reduced_chi_squared(drop2_interpolated_velocity_mean, drop2_chi_squared_square, parameter_square, "Drop 2: Quadratic Fit")

#Graph 17 Plotting Quadratic Fit
plt.figure(17)
plt.errorbar(drop2_theta_linear, drop2_interpolated_velocity_mean, yerr = drop2_sigma_interpolated_velocity_mean, ecolor = "r" )
plt.plot(drop2_theta_linear, drop2_interpolated_velocity_mean)
plt.plot(drop2_theta_linear, drop2_fitted_velocity_square, color = "y")
plt.xlabel("Linear Contact angle (radians)")
plt.ylabel("Velocity ($\mu$m/s) ")
plt.title("Drop2 : Quadratic fit fitted onto linear Contact Angle against linear Interpolated Velocity")
plt.grid()

(drop1_coefficient_square, drop1_covariance_square) = np.polyfit(drop1_theta_linear, drop1_interpolated_velocity_mean, 2, cov = True)
drop1_fitted_velocity_square = np.polyval(drop1_coefficient_square, drop1_theta_linear) #Evaluate coeff at the discrete points of theta^n (coeff is of all the curve)

#Calculating Chi squared and Reduced Chi squared
drop1_chi_squared_square = chi_squared(drop1_interpolated_velocity_mean, drop1_fitted_velocity_square, drop1_sigma_interpolated_velocity_mean)
drop1_chi_squared_reduced_square = reduced_chi_squared(drop1_interpolated_velocity_mean, drop1_chi_squared_square, parameter_square, "Drop 1: Quadratic Fit")

#Graph 18 Plotting Quadratic Fit
plt.figure(18)
plt.errorbar(drop1_theta_linear, drop1_interpolated_velocity_mean, yerr = drop1_sigma_interpolated_velocity_mean, ecolor = "r" )
plt.plot(drop1_theta_linear, drop1_interpolated_velocity_mean)
plt.plot(drop1_theta_linear, drop1_fitted_velocity_square, color = "y")
plt.xlabel("Linear Contact angle (radians)")
plt.ylabel("Velocity ($\mu$m/s) ")
plt.title("Drop1 : Quadratic fit fitted onto linear Contact Angle against linear Interpolated Velocity")
plt.grid()


#Finding fitting coeffcients
(drop2_fitting_coefficient_velocity_gennes, drop2_fitting_coefficient_theta_gennes) = coefficient(drop2_theta_linear, drop2_fitted_velocity_gennes, 2, "Drop 2: De-Gennes" ) 
(drop2_fitting_coefficient_velocity_cox, drop2_fitting_coefficient_theta_cox) = coefficient(drop2_theta_linear, drop2_fitted_velocity_cox, 3, "Drop 2: Cox-Voinov" ) 

(drop1_fitting_coefficient_velocity_gennes, drop1_fitting_coefficient_theta_gennes) = coefficient(drop1_theta_linear, drop1_fitted_velocity_gennes, 2, "Drop 1: De-Gennes" ) 
(drop1_fitting_coefficient_velocity_cox, drop1_fitting_coefficient_theta_cox) = coefficient(drop1_theta_linear, drop1_fitted_velocity_cox, 3, "Drop 1: Cox-Voinov" ) 

#Results
print("\n                                               ***CONCLUSION***    ")
print("\n For drop 1 it can be seen that the cubic fit gives the reduced chi-square value closest to 1 (%f6.2)" %(drop1_chi_squared_reduced_cubic))
print("\n For drop 1 it can be seen that out of De-Gennes Law and Cox, Gennes gives the reduced chi-square value closest to 1 (%f6.2)" %(drop1_chi_squared_reduced_gennes))
print("\n For drop 2 it can be seen that the cubic fit gives the reduced chi-square value closest to 1 (%f6.2)" %(drop2_chi_squared_reduced_cubic))
print("\n For drop 2 it can be seen that out of De-Gennes Law and Cox, Cox gives the reduced chi-square value closest to 1 (%f6.2)" %(drop2_chi_squared_reduced_cox))
print("\n                                               ***GRAPHS***    ")    

    







