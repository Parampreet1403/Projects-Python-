"""
Parampreet Singh - 25/04/19
Computational Physics: Project 3
"""

#Import packages 
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math

#Functions

#Draga Function for generating random numbers
def randssp(p,q):
    
    #global m, a, c, x
        
    try: x
    except NameError:
        m = pow(2, 31)
        a = pow(2, 16) + 3
        c = 0
        x = 123456789
    
    try: p
    except NameError:
        p = 1
    try: q
    except NameError:
        q = p
    
    r = np.zeros([p,q])

    for l in range (0, q):
        for k in range (0, p):
            x = np.mod(a*x + c, m)
            r[k, l] = x/m
            
    return r

#Function to create random uniform numbers in a matrix of (x, y ,z)
def random_uniform_matrix(n):
    value = np.random.uniform(0, 1, n*3) #Random uniform numbers
    value_2 = np.reshape(value, (3, n)) #Turns array into matrix with 3 rows
    x = value_2[0, :] #Takes first row from matrix (x)
    y = value_2[1, :]
    z = value_2[2, :]
    
    return x, y, z

#Function to create random uniform numbers between 0 and 1
def random_uniform(n):
    value = np.random.uniform(0, 1, n) #Random uniform numbers

    return value

#Function to create random uniform numbers distributed according to exp(-x/lambda) #Step length
def random_exp(n, lambda_): #number of itterations, mean free path
    k_i = np.array(random_uniform(n)) # U(0, 1)
    x_i = -lambda_*np.log(k_i) #Inverse CDF
    #s_i = -lambda_*np.log(x_1)
    
    return x_i

#Function to find the number of absorbing molecules 
def absorbing_molecules(density, molar_mass):
    n = ((density*avogadro_constant)/molar_mass) #Units cm^-3
    
    return n

#Function to find mean free path
def mean_free_path(absorbing_molecules, absorption_cross_section, scattering_cross_section):
    lambda_ = 1/((absorbing_molecules*absorption_cross_section) + (absorbing_molecules*scattering_cross_section))*10**24 #Units cm
    lambda_
    return lambda_

#Function to create random uniform numbers between any range
def random_uniform_any(min_, max_, n):
    value = np.random.uniform(min_, max_, n) #Random uniform numbers

    return value

#Function to find absorbing limit
def absorbing_limit(absorption_cross_section, scattering_cross_section):
    u = absorption_cross_section / (absorption_cross_section + scattering_cross_section)
    
    return u
    
#Function to generate isotropic unit vectors
def uniform_sphere(n):
    u = random_uniform(n)
    theta = random_uniform_any(-np.pi, np.pi, n) #Randomly distributed numbers between -pi and pi
    phi = np.arccos(1 - 2*u) # F−1(u)=arccos(1−2u) #inverse CDF
    x = np.sin(phi) * np.cos(theta) # r = 1 # cartesian to spherical coordinates
    y = np.sin(phi) * np.sin(theta)
    z = np.cos(phi)
    return x, y, z

#Generating isotropic steps with lengths distributed as exp(-x/lambda)
def isotropic_steps(N, lambda_):
    A = random_exp(N, lambda_)
    n = uniform_sphere(N)
    value = A*n
    x = value[0, :] #Takes first row from matrix (x)
    y = value[1, :]
    z = value[2, :]
    return x, y, z

#Function to find number of neutrons absorbed, transmitted and reflected in slab                
def neutron_path(n, thickness, mean_free_path, absorbing_limit):
    is_absorbed, is_transmitted, is_reflected= 0, 0, 0 #Tally
    for i in range(0, n):
        first_step = random_exp(1, mean_free_path) #To allow guranteed penetration
        step_counter = 1 #count steps
        absorption = 0
        position_x, position_y, position_z = 0, 0, first_step #Initial position
        particle_history_x, particle_history_y, particle_history_z = [0, 0], [0, 0], [0, position_z] #History of particle
        while position_z > 0 and position_z < thickness and absorption == 0: #While in slab
            absorption_probability = random_uniform(1) #Find number from U(0, 1) #Is particle absorbed?
            if absorption_probability < absorbing_limit:
                is_absorbed += 1
                absorption = 1 #Particle is absorbed
            else:
                step_x, step_y, step_z = isotropic_steps(1, mean_free_path)
                position_x = position_x + step_x
                position_y = position_y + step_y
                position_z = position_z + step_z
                step_counter += 1
                particle_history_x.append(position_x)
                particle_history_y.append(position_y)
                particle_history_z.append(position_z)
                #particle_z.append(position_z)
        if position_z < 0:
            is_reflected += 1 #Particle reflected
        elif position_z > thickness:
            is_transmitted += 1 #Particle transmitted
    return is_absorbed, is_transmitted, is_reflected   

def attentuation_length(n, bin_number, x_points):
    plt.figure(n)
    bin_frequency, bin_edges, bin_temp = plt.hist(x_points, bin_number) #BinFreq = y
    bin_x = []
    for i in range(0, bin_number):
        bin_x.append((bin_edges[i] + bin_edges[i+1])/2) #Finding mid point of bins
    coeff, covarience = np.polyfit(bin_x, np.log(bin_frequency), 1, cov = True)    
    coeff_m = coeff[0] # gradient
    lambda_ = (-1/coeff_m)
    coeff_c = coeff[1] # y intercept
    x = np.array(np.linspace(0, bin_x[bin_number-1], bin_number)) # x values
    y = coeff_m*x + coeff_c #ln(y) = x * -1/lambda # coresponding y values
    y = np.exp(y)
    plt.plot(x, y)
    plt.xlabel("x-axis")
    plt.ylabel("y-axis")
    return lambda_
    

#Main Body
    
#Constants
absorption_cross_section_water = 0.6652 #Units = barn
absorption_cross_section_lead = 0.158 #Units = barn
absorption_cross_section_graphite = 0.0045 #Units = barn

scattering_cross_section_water = 103.0 #Units = barn
scattering_cross_section_lead = 11.221 #Units = barn
scattering_cross_section_graphite = 4.74 #Units = barn

density_water = 1.00 #Units g/cm^-3
density_lead = 11.35 #Units g/cm^-3
density_graphite = 1.67 #Units g/cm^-3


molar_mass_water = 18.015 #Units g/mol
molar_mass_lead = 207.2 #Units g/mol
molar_mass_graphite = 12.0107 #Units g/mol

barn = 10**(-24) #cm^2
avogadro_constant = 6.022*10**23 #Units mol^-1

#Finding absorbing molecules #Units 1/cm^-3
absorbing_molecules_water = absorbing_molecules(density_water, molar_mass_water)
absorbing_molecules_lead = absorbing_molecules(density_lead, molar_mass_lead)
absorbing_molecules_graphite = absorbing_molecules(density_graphite, molar_mass_graphite)

#Finding mean free path #Units cm
mean_free_path_water = mean_free_path(absorbing_molecules_water, absorption_cross_section_water, scattering_cross_section_water)
mean_free_path_lead = mean_free_path(absorbing_molecules_lead, absorption_cross_section_lead, scattering_cross_section_lead)
mean_free_path_graphite = mean_free_path(absorbing_molecules_graphite, absorption_cross_section_graphite, scattering_cross_section_graphite)
mean_free_path_water_45 = 45 #cm

#Finding absorbing limit # if u < limit ; then molecule is absorbed 
absorbing_limit_water = absorbing_limit(absorption_cross_section_water, scattering_cross_section_water)
absorbing_limit_lead = absorbing_limit(absorption_cross_section_lead, scattering_cross_section_lead)
absorbing_limit_graphite = absorbing_limit(absorption_cross_section_graphite, scattering_cross_section_graphite)

"""
#Plotting using Draga random number generator to see if spectral problem present (it should be)
draga_value = randssp(3, 5000) #points in 3 dimensions (x,y,z)
x1 = draga_value[0, :] #Takes first column from matrix (x)
y1 = draga_value[1, :]
z1 = draga_value[2, :]
fig_1 = plt.figure(1)
ax = fig_1.add_subplot(111, projection = "3d")
ax.scatter(x1, y1, z1, c="r", marker="o")
plt.title("Spectral problem on Draga code")

#Plotting using built in random number generator to see if spectral problem present (it shouldn't be)
x2, y2, z2 = random_uniform_matrix(5000)
fig_2 = plt.figure(2)
ax_2 = fig_2.add_subplot(111, projection = "3d")
ax_2.scatter(x2, y2, z2, c="b", marker="o")
plt.title("Uniform points with no spectral problem")
"""
"""
#Samples distributed according to exp(-x/lambda)
x3 =random_exp(1000, mean_free_path_water_45)
plt.figure(3)
bins = 10 #Number of bins
bin_frequency, bin_edges, bin_temp = plt.hist(x3, bins)  #BinFreq = y
bin_x = []
for i in range(0, bins):
    bin_x.append((bin_edges[i] + bin_edges[i+1])/2) #Finding mid point of bins
coeff, covarience = np.polyfit(bin_x, np.log(bin_frequency), 1, cov = True)    
coeff_m = coeff[0] # gradient
aL = (-1/coeff_m) #attentuation length
coeff_c = coeff[1] # y intercept
x4 = np.array(np.linspace(0,bin_x[bins-1], bins)) # x values
y4 = coeff_m*x4 + coeff_c #ln(y) = x * -1/lambda # coresponding y values 
plt.plot(x4, np.exp(y4))
plt.title("Exponentialy distributed samples")
plt.xlabel("x-axis")
plt.ylabel("y-axis")
plt.savefig("Exponentialy distributed samples")
"""
"""
#Generating isotropic unit vectors
x6, y6, z6 = uniform_sphere(1000)
fig_4 = plt.figure(4)
ax_4 = fig_4.add_subplot(111, projection = "3d")
ax_4.scatter(x6, y6, z6, c="r", marker="o")
plt.title("Uniform points over a sphere")

#Generating isotropic steps with lengths distributed as exp(-x/lambda)
x7, y7, z7 = isotropic_steps(10, mean_free_path_water)
fig_5 = plt.figure(5)
ax_5 = fig_5.add_subplot(111, projection = "3d")
ax_5.plot(x7, y7, z7, c="b", marker="o")
plt.title("Isotropic steps with lengths distributed as exp(-x/lambda)")
ax_5.set_xlabel('X Label')
ax_5.set_ylabel('Y Label')
ax_5.set_zlabel('Z Label')
plt.savefig("Isotropic steps with lengths distributed as exp(-x/lambda)")
"""
#Finding neutron history for different materials
print("\nWelcome to Neutron testing chamber, you are able to select three different neutron numbers for testing and three different thicknesses")
print("\nThe first neutron number you pick wil be kept constant as thickness varies and vice versa")
print("\nThe materials being tested are Water, Lead and Graphite")
thickness1 = 10 #float(input("You have three different thicknesses to test, what would you like to be your first thickness (cm)?")) #Units cm
thickness2 = 5 #float(input("You have three different thicknesses to test, what would you like to be your second thickness (cm)?")) #Units cm
thickness3 = 15 #float(input("You have three different thicknesses to test, what would you like to be your third thickness (cm)?")) #Units cm
neutron_number4 = 1000 #int(input("How many neutrons would you like to test first?")) #1000
neutron_number5 = 500 #int(input("How many neutrons would you like to test second?")) #1000
neutron_number6 = 1500 #int(input("How many neutrons would you like to test third?")) #1000
"""
#Calculating number of neutrons absorbed, transmitted and reflected at constant neutron number
water_absorbed1, water_transmitted1, water_reflected1 = neutron_path(neutron_number4, thickness1, mean_free_path_water, absorbing_limit_water)
lead_absorbed1, lead_transmitted1, lead_reflected1 = neutron_path(neutron_number4, thickness1, mean_free_path_lead, absorbing_limit_lead)
graphite_absorbed1, graphite_transmitted1, graphite_reflected1 = neutron_path(neutron_number4, thickness1, mean_free_path_graphite, absorbing_limit_graphite)    

water_absorbed2, water_transmitted2, water_reflected2 = neutron_path(neutron_number4, thickness2, mean_free_path_water, absorbing_limit_water)
lead_absorbed2, lead_transmitted2, lead_reflected2 = neutron_path(neutron_number4, thickness2, mean_free_path_lead, absorbing_limit_lead)
graphite_absorbed2, graphite_transmitted2, graphite_reflected2 = neutron_path(neutron_number4, thickness2, mean_free_path_graphite, absorbing_limit_graphite)    

water_absorbed3, water_transmitted3, water_reflected3 = neutron_path(neutron_number4, thickness3, mean_free_path_water, absorbing_limit_water)
lead_absorbed3, lead_transmitted3, lead_reflected3 = neutron_path(neutron_number4, thickness3, mean_free_path_lead, absorbing_limit_lead)
graphite_absorbed3, graphite_transmitted3, graphite_reflected3 = neutron_path(neutron_number4, thickness3, mean_free_path_graphite, absorbing_limit_graphite)    

#Calculating number of neutrons absorbed, transmitted and reflected at constant thickness
water_absorbed4, water_transmitted4, water_reflected4 = neutron_path(neutron_number4, thickness1, mean_free_path_water, absorbing_limit_water)
lead_absorbed4, lead_transmitted4, lead_reflected4 = neutron_path(neutron_number5, thickness1, mean_free_path_lead, absorbing_limit_lead)
graphite_absorbed4, graphite_transmitted4, graphite_reflected4 = neutron_path(neutron_number6, thickness1, mean_free_path_graphite, absorbing_limit_graphite)    

water_absorbed5, water_transmitted5, water_reflected5 = neutron_path(neutron_number4, thickness1, mean_free_path_water, absorbing_limit_water)
lead_absorbed5, lead_transmitted5, lead_reflected5 = neutron_path(neutron_number5, thickness1, mean_free_path_lead, absorbing_limit_lead)
graphite_absorbed5, graphite_transmitted5, graphite_reflected5 = neutron_path(neutron_number6, thickness1, mean_free_path_graphite, absorbing_limit_graphite)    

water_absorbed6, water_transmitted6, water_reflected6 = neutron_path(neutron_number4, thickness1, mean_free_path_water, absorbing_limit_water)
lead_absorbed6, lead_transmitted6, lead_reflected6 = neutron_path(neutron_number5, thickness1, mean_free_path_lead, absorbing_limit_lead)
graphite_absorbed6, graphite_transmitted6, graphite_reflected6 = neutron_path(neutron_number6, thickness1, mean_free_path_graphite, absorbing_limit_graphite)    

#Calculating percentage transmitted for constant neutron number
water_percentage_transmitted1 = round((water_transmitted1/neutron_number4)*100, 3)
water_percentage_transmitted2 = round((water_transmitted2/neutron_number4)*100, 3)
water_percentage_transmitted3 = round((water_transmitted3/neutron_number4)*100, 3)
lead_percentage_transmitted1 = round((lead_transmitted1/neutron_number4)*100, 3)
lead_percentage_transmitted2 = round((lead_transmitted2/neutron_number4)*100, 3)
lead_percentage_transmitted3 = round((lead_transmitted3/neutron_number4)*100, 3)
graphite_percentage_transmitted1 = round((graphite_transmitted1/neutron_number4)*100, 3)
graphite_percentage_transmitted2 = round((graphite_transmitted2/neutron_number4)*100, 3)
graphite_percentage_transmitted3 = round((graphite_transmitted3/neutron_number4)*100, 3)

#Calculating percentage transmitted for constant thickness
water_percentage_transmitted4 = round((water_transmitted4/neutron_number4)*100, 3)
water_percentage_transmitted5 = round((water_transmitted5/neutron_number4)*100, 3)
water_percentage_transmitted6 = round((water_transmitted6/neutron_number4)*100, 3)
lead_percentage_transmitted4 = round((lead_transmitted4/neutron_number4)*100, 3)
lead_percentage_transmitted5 = round((lead_transmitted5/neutron_number4)*100, 3)
lead_percentage_transmitted6 = round((lead_transmitted6/neutron_number4)*100, 3)
graphite_percentage_transmitted4 = round((graphite_transmitted4/neutron_number4)*100, 3)
graphite_percentage_transmitted5 = round((graphite_transmitted5/neutron_number4)*100, 3)
graphite_percentage_transmitted6 = round((graphite_transmitted6/neutron_number4)*100, 3)
"""
"""
fig_6 = plt.figure(6)
ax_6 = fig_6.add_subplot(111, projection = "3d")
ax_6.plot(particle_history_x, particle_history_y, particle_history_z, c="b", marker="o")
plt.title("Simulated random walks")
ax_6.set_xlabel('X Label')
ax_6.set_ylabel('Y Label')
ax_6.set_zlabel('Z Label')
plt.savefig("Simulated random walks")
"""
"""
#Printing Results
print ("\n------------------------------------------------------------\n")   
print("Transmission for fixed Neutron Number:\n")
print ("------------------------------------------------------------\n") 
  
print("Material - Water (fixed Neutron Number)")
print ("------------------------------------------------------------")   
print("|Thickness (cm)             |"+str(thickness1)+" "*(10-(len(str(thickness1))))+"|"+str(thickness2)+" "*(10-(len(str(thickness2))))+"|"+str(thickness3)) 
print("|Total Neutrons             |"+str(neutron_number4)+" "*(10-(len(str(neutron_number4))))+"|"+str(neutron_number4)+" "*(10-(len(str(neutron_number4))))+"|"+str(neutron_number4))
print("|Neutrons Reflected         |"+str(water_reflected1)+" "*(10-(len(str(water_reflected1))))+"|"+str(water_reflected2)+" "*(10-(len(str(water_reflected2))))+"|"+str(water_reflected3))
print("|Neutrons Absorbed          |"+str(water_absorbed1)+" "*(10-(len(str(water_absorbed1))))+"|"+str(water_absorbed2)+" "*(10-(len(str(water_absorbed2))))+"|"+str(water_absorbed3))
print("|Neutrons Transmitted       |"+str(water_transmitted1)+" "*(10-(len(str(water_transmitted1))))+"|"+str(water_transmitted2)+" "*(10-(len(str(water_transmitted2))))+"|"+str(water_transmitted3))
print("|Percentage Transmitted (%) |"+str(water_percentage_transmitted1)+" "*(10-(len(str(water_percentage_transmitted1))))+"|"+str(water_percentage_transmitted2)+" "*(10-(len(str(water_percentage_transmitted2))))+"|"+str(water_percentage_transmitted3)+"\n\n")

  
print("Material - Lead (fixed Neutron Number)")
print ("------------------------------------------------------------")   
print("|Thickness (cm)             |"+str(thickness1)+" "*(10-(len(str(thickness1))))+"|"+str(thickness2)+" "*(10-(len(str(thickness2))))+"|"+str(thickness3)) 
print("|Total Neutrons             |"+str(neutron_number4)+" "*(10-(len(str(neutron_number4))))+"|"+str(neutron_number4)+" "*(10-(len(str(neutron_number4))))+"|"+str(neutron_number4))
print("|Neutrons Reflected         |"+str(lead_reflected1)+" "*(10-(len(str(lead_reflected1))))+"|"+str(lead_reflected2)+" "*(10-(len(str(lead_reflected2))))+"|"+str(lead_reflected3))
print("|Neutrons Absorbed          |"+str(lead_absorbed1)+" "*(10-(len(str(lead_absorbed1))))+"|"+str(lead_absorbed2)+" "*(10-(len(str(lead_absorbed2))))+"|"+str(lead_absorbed3))
print("|Neutrons Transmitted       |"+str(lead_transmitted1)+" "*(10-(len(str(lead_transmitted1))))+"|"+str(lead_transmitted2)+" "*(10-(len(str(lead_transmitted2))))+"|"+str(lead_transmitted3))
print("|Percentage Transmitted (%) |"+str(lead_percentage_transmitted1)+" "*(10-(len(str(lead_percentage_transmitted1))))+"|"+str(lead_percentage_transmitted2)+" "*(10-(len(str(lead_percentage_transmitted2))))+"|"+str(lead_percentage_transmitted3)+"\n\n")

  
print("Material - Graphite (fixed Neutron Number)")
print ("------------------------------------------------------------")   
print("|Thickness (cm)             |"+str(thickness1)+" "*(10-(len(str(thickness1))))+"|"+str(thickness2)+" "*(10-(len(str(thickness2))))+"|"+str(thickness3)) 
print("|Total Neutrons             |"+str(neutron_number4)+" "*(10-(len(str(neutron_number4))))+"|"+str(neutron_number4)+" "*(10-(len(str(neutron_number4))))+"|"+str(neutron_number4))
print("|Neutrons Reflected         |"+str(graphite_reflected1)+" "*(10-(len(str(graphite_reflected1))))+"|"+str(graphite_reflected2)+" "*(10-(len(str(graphite_reflected2))))+"|"+str(graphite_reflected3))
print("|Neutrons Absorbed          |"+str(graphite_absorbed1)+" "*(10-(len(str(graphite_absorbed1))))+"|"+str(graphite_absorbed2)+" "*(10-(len(str(graphite_absorbed2))))+"|"+str(graphite_absorbed3))
print("|Neutrons Transmitted       |"+str(graphite_transmitted1)+" "*(10-(len(str(graphite_transmitted1))))+"|"+str(graphite_transmitted2)+" "*(10-(len(str(graphite_transmitted2))))+"|"+str(graphite_transmitted3))
print("|Percentage Transmitted (%) |"+str(graphite_percentage_transmitted1)+" "*(10-(len(str(graphite_percentage_transmitted1))))+"|"+str(graphite_percentage_transmitted2)+" "*(10-(len(str(graphite_percentage_transmitted2))))+"|"+str(graphite_percentage_transmitted3)+"\n\n")

print ("\n------------------------------------------------------------\n")   
print("Transmission for fixed Thickness:\n")
print ("------------------------------------------------------------\n") 
  
print("Material - Water (fixed Thickness)")
print ("------------------------------------------------------------")   
print("|Thickness (cm)             |"+str(thickness1)+" "*(10-(len(str(thickness1))))+"|"+str(thickness1)+" "*(10-(len(str(thickness1))))+"|"+str(thickness1)) 
print("|Total Neutrons             |"+str(neutron_number4)+" "*(10-(len(str(neutron_number4))))+"|"+str(neutron_number5)+" "*(10-(len(str(neutron_number5))))+"|"+str(neutron_number6))
print("|Neutrons Reflected         |"+str(water_reflected4)+" "*(10-(len(str(water_reflected4))))+"|"+str(water_reflected5)+" "*(10-(len(str(water_reflected5))))+"|"+str(water_reflected6))
print("|Neutrons Absorbed          |"+str(water_absorbed4)+" "*(10-(len(str(water_absorbed4))))+"|"+str(water_absorbed5)+" "*(10-(len(str(water_absorbed5))))+"|"+str(water_absorbed6))
print("|Neutrons Transmitted       |"+str(water_transmitted4)+" "*(10-(len(str(water_transmitted4))))+"|"+str(water_transmitted5)+" "*(10-(len(str(water_transmitted5))))+"|"+str(water_transmitted6))
print("|Percentage Transmitted (%) |"+str(water_percentage_transmitted4)+" "*(10-(len(str(water_percentage_transmitted4))))+"|"+str(water_percentage_transmitted5)+" "*(10-(len(str(water_percentage_transmitted5))))+"|"+str(water_percentage_transmitted6)+"\n\n")

print("Material - Lead (fixed Thickness)")
print ("------------------------------------------------------------")   
print("|Thickness (cm)             |"+str(thickness1)+" "*(10-(len(str(thickness1))))+"|"+str(thickness1)+" "*(10-(len(str(thickness1))))+"|"+str(thickness1)) 
print("|Total Neutrons             |"+str(neutron_number4)+" "*(10-(len(str(neutron_number4))))+"|"+str(neutron_number5)+" "*(10-(len(str(neutron_number5))))+"|"+str(neutron_number6))
print("|Neutrons Reflected         |"+str(lead_reflected4)+" "*(10-(len(str(lead_reflected4))))+"|"+str(lead_reflected5)+" "*(10-(len(str(lead_reflected5))))+"|"+str(lead_reflected6))
print("|Neutrons Absorbed          |"+str(lead_absorbed4)+" "*(10-(len(str(lead_absorbed4))))+"|"+str(lead_absorbed5)+" "*(10-(len(str(lead_absorbed5))))+"|"+str(lead_absorbed6))
print("|Neutrons Transmitted       |"+str(lead_transmitted4)+" "*(10-(len(str(lead_transmitted4))))+"|"+str(lead_transmitted5)+" "*(10-(len(str(lead_transmitted5))))+"|"+str(lead_transmitted6))
print("|Percentage Transmitted (%) |"+str(lead_percentage_transmitted4)+" "*(10-(len(str(lead_percentage_transmitted4))))+"|"+str(lead_percentage_transmitted5)+" "*(10-(len(str(lead_percentage_transmitted5))))+"|"+str(lead_percentage_transmitted6)+"\n\n")

print("Material - Graphite (fixed Thickness)")
print ("------------------------------------------------------------")   
print("|Thickness (cm)             |"+str(thickness1)+" "*(10-(len(str(thickness1))))+"|"+str(thickness1)+" "*(10-(len(str(thickness1))))+"|"+str(thickness1)) 
print("|Total Neutrons             |"+str(neutron_number4)+" "*(10-(len(str(neutron_number4))))+"|"+str(neutron_number5)+" "*(10-(len(str(neutron_number5))))+"|"+str(neutron_number6))
print("|Neutrons Reflected         |"+str(graphite_reflected4)+" "*(10-(len(str(graphite_reflected4))))+"|"+str(graphite_reflected5)+" "*(10-(len(str(graphite_reflected5))))+"|"+str(graphite_reflected6))
print("|Neutrons Absorbed          |"+str(graphite_absorbed4)+" "*(10-(len(str(graphite_absorbed4))))+"|"+str(graphite_absorbed5)+" "*(10-(len(str(graphite_absorbed5))))+"|"+str(graphite_absorbed6))
print("|Neutrons Transmitted       |"+str(graphite_transmitted4)+" "*(10-(len(str(graphite_transmitted4))))+"|"+str(graphite_transmitted5)+" "*(10-(len(str(graphite_transmitted5))))+"|"+str(graphite_transmitted6))
print("|Percentage Transmitted (%) |"+str(graphite_percentage_transmitted4)+" "*(10-(len(str(graphite_percentage_transmitted4))))+"|"+str(graphite_percentage_transmitted5)+" "*(10-(len(str(graphite_percentage_transmitted5))))+"|"+str(graphite_percentage_transmitted6)+"\n\n")
"""
