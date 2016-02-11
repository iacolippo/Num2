#remember: = when dealing with list points to the location of list in memory

#import libraries
import numpy as np
import random as rnd

def batch_mean_and_variance(list, blocksize):
    
    totalsize = len(list)
    mean_of_blocks = []
    variance_of_blocks = []
    blocks = np.split(np.asarray(list), blocksize)
    
    for chunk in blocks:
        mean_of_blocks.append(np.mean(chunk))
        variance_of_blocks.append(np.var(chunk))  
        
    mean = np.mean(mean_of_blocks)
    variance = np.sum(variance_of_blocks)*((blocksize*1.0/totalsize)**2)
    
    return mean, variance

def difference(pos1, pos2):
    return np.asarray(pos1) - np.asarray(pos2)

def norm(vector):
    norm = 0
    for n in xrange(0, len(vector)):
        norm+=vector[n]**2
    return np.sqrt(norm)

def pot_energy(pos1, pos2):
    L = 4
    return np.power(norm(difference(pos1, pos2)) - L, 2)/2.0

q1 = np.array([0.0, -2.0, 0.0])
q2 = np.array([0.0, 2.0, 0.0])

delta = 0.1
nsteps = 1000000
alpha = 0
U0 = pot_energy(q1, q2)

data = [norm(difference(q1, q2))]

rnd.seed(1234)

out_file = open("average_distance.txt", "w")
for i in xrange(0, nsteps-1):
    distance = norm(difference(q1, q2))
    out_file.write(str(i) + " " + str(norm(q1)) + " " + str(norm(q2)) + " " + str(distance) + " " + str(alpha) + "\n")
    
    particle_id = rnd.randint(1, 2)
    coordinate_id = rnd.randint(0, 2)

    q1_new = np.array(q1)
    q2_new = np.array(q2)
    
    if particle_id == 1:
        q0 = float(q1[coordinate_id])
        q1_new[coordinate_id] = q0 + rnd.uniform(-delta, delta)
        U_new = pot_energy(q1_new, q2)
    elif particle_id == 2:
        q0 = float(q2[coordinate_id])
        q2_new[coordinate_id] = q2[coordinate_id] + rnd.uniform(-delta, delta)
        U_new = pot_energy(q1, q2_new)

    #Metropolis
    alpha = np.exp(U0 - U_new)
    if alpha > 1:
        alpha = 1
    if alpha > rnd.random():
        q1 = q1_new
        q2 = q2_new
        U0 = U_new
    
    data.append(norm(difference(q1, q2)))
    
out_file.close()

mean, var = batch_mean_and_variance(data, nsteps/10)

print "average length:", mean, "+/-", var
    