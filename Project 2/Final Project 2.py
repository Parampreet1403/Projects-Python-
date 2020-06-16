"""
Created on Fri Mar 22 20:08:11 2019
@author: Parampreet Singh
Computational Physics - Project 2
"""
#Import packages

import numpy as np 
import matplotlib.pyplot as plt
from os import path

#Function Definitions

#Function to find displacement and velocity via exact solution
def exact_solution_method(gamma, frequency, time):
    displacement = -((1/frequency) * np.exp((gamma/-2) * time) * np.sin(frequency*time)) #-(1/w)*exp[-(gamma*t/2)]*sin(wt)
    velocity = (np.exp((gamma/-2) * time) ) * ((gamma / (2 * frequency)) * ( np.sin(frequency * time))) - (np.cos(frequency * time)) # exp[-(gamma*t/2)]*((gamma/2*w)*sin(wt) - cos(wt))
    
    return displacement, velocity
    
#Function to find displacement and velocity via Euler
def Euler_method(damping_constant, spring_constant, step_size, mass, steps, x_0, v_0):
    a_n = np.zeros(steps) #Acceleration
    x_n = np.zeros(steps) #Displacement
    v_n = np.zeros(steps) #Velocity
    #Setting Initial conditions
    x_n[0] = x_0
    v_n[0] = v_0
    for i in range (0, steps - 1): #Looping to find values at later steps
        a_n[i] = -damping_constant*v_n[i]/mass - spring_constant*x_n[i]/mass
        v_n[i+1] = v_n[i] + step_size * a_n[i]
        x_n[i+1] = x_n[i] + (step_size * v_n[i])
    
    return x_n, v_n
    
#Function to find displacement and velocity via Improved Euler    
def improved_euler_method(damping_constant, spring_constant, step_size, mass, steps, x_0, v_0):
    a_n = np.zeros(steps) #Acceleration
    x_n = np.zeros(steps) #Displacement
    v_n = np.zeros(steps) #Velocity
    #Setting Initial conditions
    x_n[0] = x_0
    v_n[0] = v_0
    for i in range (0, steps - 1): #Looping to find values at later steps
        a_n[i] = -damping_constant*v_n[i]/mass - spring_constant*x_n[i]/mass
        v_n[i+1] = v_n[i] + step_size * a_n[i]
        x_n[i+1] = x_n[i] + step_size*v_n[i] + 0.5 * step_size**2 * a_n[i]
    
    return x_n, v_n
       
#Function to find displacement and velocity via Verlet  
def Verlet_method(damping_constant, spring_constant, step_size, mass, steps, external_force, position, euler_displacement, x_0, v_0):
    x_n = np.zeros(steps) #Displacement
    v_n = np.zeros(steps) #Velocity
    F = np.zeros(steps) #Force
    #Setting constants 
    F[position:] = external_force #Placing force on chosen position in cycle #Continous Force 
    A = 2 - ((np.square(step_size)*spring_constant)/mass)
    B = (damping_constant*step_size)/(2*mass) - 1
    C = (np.square(step_size)*F) / mass #Extra term to include external force
    D = 1 + ((damping_constant*step_size)/(2*mass))
    #Setting Initial conditions
    x_n[0] = x_0
    x_n[1] = euler_displacement #Verlet is not self starting
    v_n[0] = v_0
    for i in range (1, steps - 1): #Looping to find values at later steps
        x_n[i+1] = (A*x_n[i] + B*x_n[i-1] + C[i]) / D
        v_n[i] = (x_n[i+1] - x_n[i-1]) / (2*step_size)
    
    return x_n, v_n  

#Function to find displacement and velocity via Euler-Cromer     
#Note no damping constant dependace    
def Euler_cromer_method(spring_constant, step_size, mass, steps, x_0, v_0):
    x_n = np.zeros(steps) #Displacement
    v_n = np.zeros(steps) #Velocity
    #Setting Initial conditions
    x_n[0] = x_0
    v_n[0] = v_0
    for i in range (0, steps - 1): #Looping to find values at later steps
        v_n[i+1] = v_n[i] - spring_constant * step_size*x_n[i]/mass
        x_n[i+1] = x_n[i] + step_size * v_n[i+1]
    
    return x_n, v_n
    
#Function to find Kinetic Energy
def Kineic_energy(mass, velocity):
    ke = 0.5*mass*np.square(velocity) #1/2 * mv^2
    
    return ke
    
#Function to find Elastic potential energy
def Elastic_energy(spring_constant, dispalcement):
    elastic_energy = 0.5*spring_constant*np.square(dispalcement) # 1/2 kx^2
    
    return elastic_energy
    
#Function to find total energy
def Total_energy(mass, spring_cpnstant, displacement, velocity):
    ke = Kineic_energy(mass, velocity) #Calls function to find kinetic energy
    elastic_energy = Elastic_energy(spring_constant, displacement) #Calls function to find elastic energy
    total_energy = ke + elastic_energy #Sums two type of energies to give total
    
    return total_energy

#Function to unpack data from file
def Unpack(Name, column):
    value = np.loadtxt(Name, delimiter = " ", usecols = (column), unpack=True) #Separates data with spaces 
    
    return value

#Global Variables

#Input values
spring_constant = float(input("What value would you like to assign to the spring constant?"))# 2.14 # k
mass = float(input("What value would you like to assign to the mass?")) #3.62 # m
damping_constant_critical = 2 * np.sqrt(spring_constant * mass) # b_cr
damping_constant_multiple = float(input("What multiple of the critical damping constant would you like to assign as the damping constant?"))
damping_constant = damping_constant_multiple*damping_constant_critical # b
total_time = 100 # T
step_size = 0.1 # h

#Inital conditions
x_0 = float(input("What value would you like to assign to the initial displacement?")) #Intitial Displacement
v_0 = float(input("What value would you like to assign to the initial velocity?")) #Initial Velocity

#Constants
gamma = damping_constant / mass
natural_frequency = np.sqrt(spring_constant / mass) # W_0
frequency = np.sqrt((spring_constant / mass) - (np.square(damping_constant) / (4 * np.square(mass)))) # W
steps = int(total_time / step_size) # n
time = np.array(np.linspace(0, total_time, steps + 1))
time = time[:-1] #Makes time the same size as displacement and velocity

#Creating different location to apply the force
total_position = steps 
position_1 = int(total_position / 4) #Quarter cycle
position_2 = position_1 * 2 #Half Cycle
position_3 = position_1 * 3 #Three quarter cycle

#Creating Sin Force
sin_frequency = 1
external_force = 1 
sin_force = external_force * np.sin(sin_frequency*time[position_1:]) # F(t) = F.*sin(wt)

#Frequency range with corresponding force above and below natural frequency
frequency_1 = natural_frequency/2 # 1/2 * W_0
frequency_2 = natural_frequency + frequency_1 # 3/2 * W_0
frequency_3 = natural_frequency/4 # 1/4 * W_0
frequency_4 = natural_frequency + frequency_3 # 3/4 * W_0
resonance_force_1 = external_force * np.sin(frequency_1*time) # F(w) = F.*sin(wt)
resonance_force_2 = external_force * np.sin(frequency_2*time)
resonance_force_3 = external_force * np.sin(frequency_3*time)
resonance_force_4 = external_force * np.sin(frequency_4*time)
Resonance_force = external_force * np.sin(natural_frequency*time) #Force at which Resonance should occur


#Main Body

#Finding dispalcement and velocity for diferent methods
exact_displacement, exact_velocity = exact_solution_method(gamma, frequency, time)
euler_displacement, euler_velocity = Euler_method(damping_constant, spring_constant, step_size, mass, steps, x_0, v_0)
improved_euler_displacement, improved_euler_velocity = improved_euler_method(damping_constant, spring_constant, step_size, mass, steps, x_0, v_0) 
verlet_displacement, verlet_velocity = Verlet_method(damping_constant, spring_constant, step_size, mass, steps, 0, 0, euler_displacement[1], x_0, v_0)
euler_cromer_displacement, euler_cromer_velocity = Euler_cromer_method(spring_constant, step_size, mass, steps, x_0, v_0)

#Finding the difference between the peaks of the exact solution compared to the four methods
euler_residule = exact_displacement - euler_displacement
improved_euler_residule = exact_displacement - improved_euler_displacement
verlet_residule = exact_displacement - verlet_displacement
euler_cromer_residule = exact_displacement - euler_cromer_displacement 

#Finding dispalcement and velocity for Euler method for different step sizes
euler_displacement_lower, euler_velocity_lower = Euler_method(damping_constant, spring_constant, step_size/2, mass, steps, x_0, v_0)
euler_displacement_higher, euler_velocity_higher = Euler_method(damping_constant, spring_constant, 3*step_size/4, mass, steps, x_0, v_0)

#Finding energy for Euler Method with different Time steps
euler_energy = Total_energy(mass, spring_constant, euler_displacement, euler_velocity)
euler_energy_higher = Total_energy(mass, spring_constant, euler_displacement_higher, euler_velocity_higher)
euler_energy_lower = Total_energy(mass, spring_constant, euler_displacement_lower, euler_velocity_lower)

#Fiding energy as a function of time for different methods 
exact_energy = Total_energy(mass, spring_constant, exact_displacement, exact_velocity)
improved_euler_energy = Total_energy(mass, spring_constant, improved_euler_displacement, improved_euler_velocity)
verlet_energy = Total_energy(mass, spring_constant, verlet_displacement, verlet_velocity)
euler_cromer_energy = Total_energy(mass, spring_constant, euler_cromer_displacement, euler_cromer_velocity)

#Finding Solutions for the "best method" with different damping terms
verlet_displacement_crit, verlet_velocity_crit = Verlet_method(damping_constant_critical, spring_constant, step_size, mass, steps, 0, 0, euler_displacement[1], x_0, v_0)
verlet_displacement_half, verlet_velocity_half = Verlet_method(0.5*damping_constant_critical, spring_constant, step_size, mass, steps, 0, 0, euler_displacement[1], x_0, v_0)
verlet_displacement_double, verlet_velocity_double = Verlet_method(2*damping_constant_critical, spring_constant, step_size, mass, steps, 0, 0, euler_displacement[1], x_0, v_0)

#Verlet Solution with an external force
verlet_push_1_displacement, verlet_push_1_velocity = Verlet_method(damping_constant, spring_constant, step_size, mass, steps, external_force, position_1, euler_displacement[1], x_0, v_0)
#multiplying force by -ve 1 to make force be in oppisite direction
verlet_negative_push_1_displacement, verlet_negative_push_1_velocity = Verlet_method(damping_constant, spring_constant, step_size, mass, steps, -1*external_force, position_1, euler_displacement[1], x_0, v_0)
verlet_push_2_displacement, verlet_push_2_velocity = Verlet_method(damping_constant, spring_constant, step_size, mass, steps, external_force, position_2, euler_displacement[1], x_0, v_0)
verlet_negative_push_2_displacement, verlet_negative_push_2_velocity = Verlet_method(damping_constant, spring_constant, step_size, mass, steps, -1*external_force, position_2, euler_displacement[1], x_0, v_0)
verlet_push_3_displacement, verlet_push_3_velocity = Verlet_method(damping_constant, spring_constant, step_size, mass, steps, external_force, position_3, euler_displacement[1], x_0, v_0)
verlet_negative_push_3_displacement, verlet_negative_push_3_velocity = Verlet_method(damping_constant, spring_constant, step_size, mass, steps, -1*external_force, position_3, euler_displacement[1], x_0, v_0)

#Verlet Solution with an sinusoidal external force
verlet_sin_displacement, verlet_sin_velocity = Verlet_method(damping_constant, spring_constant, step_size, mass, steps, sin_force, position_1, euler_displacement[1], x_0, v_0)

#Bonus
#Verlet solution for different frequencies 
verlet_resonance_1_displacement, verlet_resonance_1_velocity = Verlet_method(damping_constant, spring_constant, step_size, mass, steps, resonance_force_1, 0, euler_displacement[1], x_0, v_0)
verlet_resonance_2_displacement, verlet_resonance_2_velocity = Verlet_method(damping_constant, spring_constant, step_size, mass, steps, resonance_force_2, 0, euler_displacement[1], x_0, v_0)
verlet_resonance_3_displacement, verlet_resonance_3_velocity = Verlet_method(damping_constant, spring_constant, step_size, mass, steps, resonance_force_3, 0, euler_displacement[1], x_0, v_0)
verlet_resonance_4_displacement, verlet_resonance_4_velocity = Verlet_method(damping_constant, spring_constant, step_size, mass, steps, resonance_force_4, 0, euler_displacement[1], x_0, v_0)
verlet_Resonance_displacement, verlet_Resonance_velocity = Verlet_method(damping_constant, spring_constant, step_size, mass, steps, Resonance_force, 0, euler_displacement[1], x_0, v_0)

#File Writing

#File to store Time
time_filename = "time.txt" #Name of file
file_0 = open(time_filename, "w") #Writes to file
np.savetxt(time_filename, time) #Saves data to file
file_0.close() #CLoses file
print( str(time_filename) + " exists:" + str(path.exists(time_filename))) #Checks if file exists

#File to store all Displacements
displacement_output = np.column_stack((exact_displacement, euler_displacement, improved_euler_displacement, verlet_displacement, euler_cromer_displacement))
displacement_filename = "Displacements.txt"
file_1 = open(displacement_filename, "w")
np.savetxt(displacement_filename, displacement_output)
file_1.close()
print(str(displacement_filename) + " exists:" + str(path.exists(displacement_filename))) #Checks if file exists

#File to store all Velocities
velocity_output = np.column_stack((exact_velocity, euler_velocity, improved_euler_velocity, verlet_velocity, euler_cromer_velocity))
velocity_filename = "Velocities.txt"
file_2 = open(velocity_filename, "w")
np.savetxt(velocity_filename, velocity_output)
file_2.close()
print(str(velocity_filename) + " exists:" + str(path.exists(velocity_filename))) #Checks if file exists

#File to store all Energies
energy_output = np.column_stack((exact_energy, euler_energy, improved_euler_energy, verlet_energy, euler_cromer_energy))
energy_filename = "Energies.txt"
file_3 = open(energy_filename, "w")
np.savetxt(energy_filename, energy_output)
file_3.close()
print(str(energy_filename) + " exists:" + str(path.exists(energy_filename))) #Checks if file exists

#File to store all Residule displacements 
residule_output = np.column_stack((euler_residule, improved_euler_residule, verlet_residule, euler_cromer_residule))
residule_filename = "Residule.txt"
file_4 = open(residule_filename, "w")
np.savetxt(residule_filename, residule_output)
file_4.close()
print(str(residule_filename) + " exists:" + str(path.exists(residule_filename))) #Checks if file exists


#Graph Plotting and Comments

#Graph 1: Displacement against Time for all methods
plt.figure(1)
plt.grid()
plt.plot(Unpack(time_filename, 0), Unpack(displacement_filename, 1), label = "Euler")
plt.plot(Unpack(time_filename, 0), Unpack(displacement_filename, 2), label = "Improved Euler")
plt.plot(Unpack(time_filename, 0), Unpack(displacement_filename, 3), label = "Verlet")
plt.plot(Unpack(time_filename, 0), Unpack(displacement_filename, 4), label = "Cromer")
plt.plot(Unpack(time_filename, 0), Unpack(displacement_filename, 0), label = "Exact Solution")
plt.legend()
plt.title("Displacement against Time for different methods")
plt.ylabel("Displacment (m)")
plt.xlabel("Time (s)")

"""
From Graph 1 it can be seen that both Euler and Improved Euler have an increasing displacement as time increases, 
where Euler has a much more rapidly increasing displacement. 
Verlet and Euler Cromer can be seen overlapping the exact solution.
"""

#Graph 10: Residule Displacement agasint Time for all methods compared to exact solution 
plt.figure(10)
plt.grid()
plt.plot(Unpack(time_filename, 0), Unpack(residule_filename, 0), label = "Euler")
plt.plot(Unpack(time_filename, 0), Unpack(residule_filename, 1), label = "Improved Euler")
plt.plot(Unpack(time_filename, 0), Unpack(residule_filename, 2), label = "Verlet")
plt.plot(Unpack(time_filename, 0), Unpack(residule_filename, 3), label = "Cromer")
plt.legend()
plt.title("Residule displacement against Time for different methods compared to exact solution")
plt.ylabel("Displacment (m)")
plt.xlabel("Time (s)")

"""
From Graph 10, the differences in displacements for each method compared to the exact solution were found. 
It can be seen again that Euler and improved Euler start to blow up where as Verlet and Euler-Cromer are almost identical to the exact solution. 
Supporting that either Verlet or Euler Cromer is the better method.
"""

#Graph 2: Energy against time for Euler with different Time steps
plt.figure(2)
plt.grid()
plt.plot(Unpack(time_filename, 0), Unpack(energy_filename, 0), label = "Exact solution, time step = h")
plt.plot(Unpack(time_filename, 0), Unpack(energy_filename, 1), label = "Time step = h")
plt.plot(Unpack(time_filename, 0), euler_energy_higher, label = "Time step = (3/4)*h")
plt.plot(Unpack(time_filename, 0), euler_energy_lower, label = "Time step = h/2")
plt.legend()
plt.title("Energy against Time for Euler Method")
plt.ylabel("Energy")
plt.xlabel("Time (s)")

"""
From Graph 2, it can be seen that as the time step decreases so does the energy. 
Compared to the exact solution, it is seen that having a smaller time step increases the accuracy as the energy drops lower, 
coming closer to the exact solution value.
"""

#Graph 3: Energy as a function of time for different methods 
plt.figure(3)
plt.grid()
plt.plot(Unpack(time_filename, 0), Unpack(energy_filename, 0), label = "Exact Solution")
plt.plot(Unpack(time_filename, 0), Unpack(energy_filename, 1), label = "Euler")
plt.plot(Unpack(time_filename, 0), Unpack(energy_filename, 2), label = "Improved Euler")
plt.plot(Unpack(time_filename, 0), Unpack(energy_filename, 3), label = "Verlet")
plt.plot(Unpack(time_filename, 0), Unpack(energy_filename, 4), label = "Cromer")
plt.legend()
plt.title("Energy against Time for different methods")
plt.ylabel("Energy")
plt.xlabel("Time (s)")

"""
Again, it is seen that Verlet and Cromer solutions are more accurate than improved Euler and 
Euler solutions as energy is exponentially increasing for the Euler methods but staying steady for the others.
"""

#Graph 4: Phase sapce as a function of time for Euler and Improved Euler
plt.figure(4)
plt.grid()
plt.plot(Unpack(displacement_filename, 1), Unpack(velocity_filename, 1), label = "Euler")
plt.plot(Unpack(displacement_filename, 2), Unpack(velocity_filename, 2), label = "Improved Euler")
plt.plot(Unpack(displacement_filename, 0), Unpack(velocity_filename, 0), label = "Exact Solution")
plt.legend()
plt.title("Velocity against Displacement for different methods")
plt.ylabel("Velocity (m/s)")
plt.xlabel("Displacement (m)")

#Graph 9: Phase sapce as a function of time for Verlet and Cromer
plt.figure(9)
plt.grid()
plt.plot(Unpack(displacement_filename, 3), Unpack(velocity_filename, 3), label = "Verlet")
plt.plot(Unpack(displacement_filename, 4), Unpack(velocity_filename, 4), label = "Cromer")
plt.plot(Unpack(displacement_filename, 0), Unpack(velocity_filename, 0), label = "Exact Solution")
plt.legend()
plt.title("Velocity against Displacement for different methods")
plt.ylabel("Velocity (m/s)")
plt.xlabel("Displacement (m)")

"""
Two phase space graphs have been plotted, 
the first graph shows how much the two Euler methods spiral out compared to the exact solution. 
Looking at the second plot it can be seen that both Verlet and Euler Cromer are steady circles just like the exact solution. 
This is to be expected as with an increasing displacement and velocity the energy of the system should also increase which was seen in the previous graphs.

In conclusion, both Euler and improved Euler have an increasing displacement and velocity causing the energy of the system to exponentially increase. 
Leaving only Verlet and Euler-Cromer as accurate methods, however, 
Euler-Cromer does not include a damping term making it unrealistic; leaving only Verlet as the best method.
"""

#Best method = Verlet
#Graph 5: Dispalcement against Time for different damping constants
plt.figure(5)
plt.grid()
plt.plot(time, verlet_displacement_crit, label = "Critical")
plt.plot(time, verlet_displacement_half, label = "Half critical")
plt.plot(time, verlet_displacement_double, label = "Double critical")
plt.legend()
plt.title("Displacement against Time for Verlet with different damping constants")
plt.xlabel("Time (s)")
plt.ylabel("Displacement (m)")
plt.xlim(0,30)

"""
From Graph 5, the line which shows half the critical value of damping is to be expected as it approaches zero faster than in the case of critical damping, 
but oscillates about that zero. When the damping constant is at its critical value it reaches zero the quickest. 
When the system is overdamped it will approach zero but take the longest time, which can be seen for damping which is twice the critical. 
The damping coefficient is greater than the undamped resonant frequency.
"""


#Graph 6: Dispalcement against Time via Verlet for different locations and signs for force
plt.figure(6)
plt.grid()
plt.plot(time, verlet_negative_push_1_displacement, label = "Negative force position: " + str(position_1*step_size)+ "s")
plt.plot(time, verlet_negative_push_2_displacement, label = "Negative force position: " + str(position_2*step_size)+ "s")
#plt.plot(time, verlet_negative_push_3_displacement, label = "Negative force position: " + str(position_3*step_size)+ "s")
plt.plot(time, verlet_push_1_displacement, label = "Force position: " + str(position_1*step_size) + "s")
plt.plot(time, verlet_push_2_displacement, label = "Force position: " + str(position_2*step_size)+ "s")
#plt.plot(time, verlet_push_3_displacement, label = "Force position: " + str(position_3*step_size)+ "s")
plt.legend(loc=3)
plt.title("Displacement against Time for Verlet with different force positions")
plt.xlabel("Time (s)")
plt.ylabel("Displacement (m)")

"""
From Graph 6, it can be seen that all waves overlap until the force is introduced. A quarter through the cycle, 
a positive force causes the total displacement to increase and a negative force has the opposite effect. 
As the external force is constant and continuous it can be seen that the effect of the force is continuous when it is introduced.  
Introducing the same negative external force later in the cycle causes the total amplitude to decrease. 
Introducing the same positive external force later in the cycle causes the total amplitude to increase.
"""

#Graph 7: Dispalcement against Time via Verlet for sinusoidal external force applied a quarter into the cycle
plt.figure(7)
plt.grid()
plt.plot(time, verlet_sin_displacement, label = "Forced oscillation")
plt.plot(time, verlet_displacement, label = "Unforced oscillation")
plt.legend()
plt.title("Displacement against Time for Verlet with sinusoidal external force")
plt.xlabel("Time (s)")
plt.ylabel("Displacement (m)")

"""
From Graph 7, it can be seen that the forced oscillator has lower amplitude compared to the unforced oscillator. 
The frequency is greater than that of the natural frequency of the system. 
If a damping term is introduced the unforced oscillation will decay until it reach zero, 
whereas the forced oscillation amplitude would reduce but still carry on oscillating around zero
"""

#Bonus
#Graph 8: Amplitude as a function of frequency against Time via Verlet
plt.figure(8)
plt.grid()
plt.plot(time, verlet_resonance_3_displacement, label = "0.25W_0")
plt.plot(time, verlet_resonance_1_displacement, label = "0.5W_0")
plt.plot(time, verlet_resonance_4_displacement, label = "1.25W_0")
plt.plot(time, verlet_Resonance_displacement, label = "W_0")
plt.plot(time, verlet_resonance_2_displacement, label = "1.5W_0")
plt.legend()
plt.title("Displacement against Time for Verlet with different frequencies")
plt.xlabel("Time (s)")
plt.ylabel("Displacement (m)")
plt.xlim(0, 50)

"""
From Graph 8 it can be seen that as frequency approaches resonance, 
the amplitude increases and when frequency is equal to resonance the displacement increases drastically over time.
"""