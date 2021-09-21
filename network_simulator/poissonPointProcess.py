from random import uniform
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt

def generateUsersPPP(areasize, lambda0):

    #Simulation window parameters
    xMin=0;xMax=areasize;
    yMin=0;yMax=areasize;
    xDelta=xMax-xMin;yDelta=yMax-yMin; #rectangle dimensions
    areaTotal=xDelta*yDelta;
     
    #Point process parameters
    # lambda0=0.04; #intensity (ie mean density) of the Poisson process
     
    #Simulate Poisson point process
    numbPoints = scipy.stats.poisson(lambda0*areaTotal).rvs()#Poisson number of points
    xx = xDelta*scipy.stats.uniform.rvs(0,1,((numbPoints,1)))+xMin#x coordinates of Poisson points
    yy = yDelta*scipy.stats.uniform.rvs(0,1,((numbPoints,1)))+yMin#y coordinates of Poisson points

    x = [itemx.tolist()[0] for itemx in xx]
    y = [itemy.tolist()[0] for itemy in yy]

    return x, y

def generateUsers(areasize, number):
    x = []
    y = []

    for user in range(number):
        x.append(uniform(0, areasize))
        y.append(uniform(0, areasize))

    return x, y

# if __name__ == '__main__':

#     x, y = generateUsersPPP(50, 0.2)
#     x1, y1 = generateUsers(50, len(x))

#     xy = np.vstack([x, y])
#     z = scipy.stats.gaussian_kde(xy)(xy)

#     xy1 = np.vstack([x1,y1])
#     z1 = scipy.stats.gaussian_kde(xy1)(xy1)

#     fig = plt.figure(1)

#     plt.subplot(121)
#     plt.scatter(x, y, c=z)
#     plt.title("Poisson Point Process")
#     plt.xlabel("x")
#     plt.ylabel("y")

#     plt.subplot(122)
#     plt.scatter(x1, y1, c=z1)
#     plt.title("Python Uniform Random")
#     plt.xlabel("x")
#     plt.ylabel("y")
#     plt.show()
