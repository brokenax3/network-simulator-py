import numpy as np
import scipy.stats
import matplotlib.pyplot as plt

def generateUsersPPP(areasize, lambda0):
    #Simulation window parameters
    areaTotal = areasize * areasize
    
    #Point process parameters
    # lambda0=0.04; #intensity (ie mean density) of the Poisson process
     
    #Simulate Poisson point process
    numbPoints = scipy.stats.poisson( lambda0*areaTotal ).rvs()#
    x = scipy.stats.uniform.rvs(0, areasize,((numbPoints,1)))
    y = scipy.stats.uniform.rvs(0, areasize, ((numbPoints,1)))
    P = np.hstack((x,y))

    return P.T[0], P.T[1]
    # P = np.hstack((x,y))
    #Plotting
    # fig = plt.figure(1)
    # plt.scatter(P.T[0], P.T[1], edgecolor='b', facecolor='none', alpha=0.5 )
    # plt.xlabel("x")
    # plt.ylabel("y")
    # plt.savefig('ppp.png')

# if __name__ == '__main__':
#      print(generateUsersPPP(50, 0.04))

