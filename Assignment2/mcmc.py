'''Iacopo Poli, 2015 - Numerical Methods II, held by G. Bussi at SISSA, Trieste

This script samples the configurations of a particle subject to an harmonic potential of stiffness k=1,
at temperature kBT=1, in 1D'''

#import libraries
import numpy as np
import random as rnd
import sys

#potential energy for 1D harmonic oscillator: U = (q^2)/2  
def pot_energy1D(pos):
    return np.power(pos, 2)/2.0

def batch_mean_and_variance(list, blocksize):
    
    totalsize = len(list)
    mean_of_blocks = []
    variance_of_blocks = []
    blocks = np.split(np.asarray(list), blocksize)
    
    for chunk in blocks:
        mean_of_blocks.append(np.mean(chunk))
        variance_of_blocks.append(np.var(chunk))  
        
    mean = np.mean(mean_of_blocks)
    variance = np.sum(variance_of_blocks)*(blocksize/totalsize)**2
    
    return mean, variance   

#initialization
q = []

#read parameters from input file - reason: automate with bash script
in_file = open(sys.argv[1], "r")
data = in_file.readlines()

first_line = data[0].split()
delta = float(first_line[1])

second_line = data[1].split()
nstep = int(second_line[1]) #int(round(int(second_line[1])/delta))

third_line = data[2].split()
q.append(float(third_line[1]))

fourth_line = data[3].split()
nblock = int(fourth_line[1])

#compute potential energy of starting point
U = [pot_energy1D(q[0])]

#sums initialization
accepted = 0
sum_alpha = 0
sum_squared = 0
average_q_squared = [np.power(float(q[0]), 2)]

rnd.seed(134567)

#opens file to write data
out_file = open(sys.argv[2],"w")
for i in xrange(0, nstep-1):
    out_file.write(str(i*delta) + " " + str(q[i]) + " " + str(average_q_squared[i]) + "\n")
    
    q_new = q[i] + rnd.uniform(-delta, delta)
    U_new = pot_energy1D(q_new)
    
    alpha = np.exp(U[i] - U_new) #beta = 1
    
    #Metropolis algorithm
    if(alpha > 1):
        alpha = 1
    
    if(alpha > rnd.random()):
        q.append(q_new)
        U.append(U_new)
        accepted += 1
    else:
        q.append(q[i])
        U.append(U[i])
    
    sum_squared+=np.power(q[i], 2)
    average_q_squared.append(sum_squared/(i+1))   
    sum_alpha+=alpha
out_file.close()

mean, variance = batch_mean_and_variance(average_q_squared, nstep/10)
std = np.sqrt(variance)


out_file = open("variance-delta.txt", "a+")
out_file.write(str(delta) + " " + str(std) + "\n")
out_file.close()


#Compute average alpha in function of delta and alpha*delta in function of delta
###average alpha and acceptance rate should converge to the same number if the simulation is long enough
average_alpha = sum_alpha/nstep
alphadelta = accepted*delta/nstep

print "<alpha>, alpha*delta", average_alpha, alphadelta