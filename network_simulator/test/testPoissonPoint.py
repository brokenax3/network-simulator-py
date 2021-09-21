import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
from network_simulator.poissonPointProcess import generateUsers, generateUsersPPP

def poissonPoint():
    x, y = generateUsersPPP(50, 0.2)
    x1, y1 = generateUsers(50, len(x))

    xy = np.vstack([x, y])
    z = scipy.stats.gaussian_kde(xy)(xy)

    xy1 = np.vstack([x1,y1])
    z1 = scipy.stats.gaussian_kde(xy1)(xy1)

    plt.figure(1)

    plt.subplot(121)
    plt.scatter(x, y, c=z)
    plt.title("Poisson Point Process")
    plt.xlabel("x")
    plt.ylabel("y")

    plt.subplot(122)
    plt.scatter(x1, y1, c=z1)
    plt.title("Python Uniform Random")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()

if __name__ == "__main__":
    poissonPoint()
