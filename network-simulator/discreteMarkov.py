from pydtmc import MarkovChain
import numpy as np
from math import sqrt

def energyArrivalStates(TIMEMAX):
    """ Returns an array of states for energy arrival

    The states for energy arrival is an output from the discrete Markov Chain as demonstrated in https://arxiv.org/pdf/1405.7254.pdf.

    Outputs the whole Markov Chain in a list.
    """

    probability_5min = [[0.979, 0.015, 0.006, 0], [0.005, 0.988, 0.007, 0], [0.006, 0.009, 0.975, 0.010], [0, 0, 0.007, 0.993]]

    mc = MarkovChain(probability_5min, ['Poor', 'Fair', 'Good', 'Excellent'])
    
    states = mc.walk(TIMEMAX, seed = 42)

    return states

def energyArrivalOutput(state):
    """ Returns the energy arrival by sampling a normal distribution

    The dict states provides the mean and the variance of the normal distribution of each state of the markov chain.

    The function picks a sample from the normal distribution in the unit of 0.1 W/cm^2.

    """
    states = {
        'Poor' : [1.75, 0.65],
        'Fair' : [4.21, 1.04],
        'Good' : [7.02, 2.34],
        'Excellent' : [9.38, 0.54]
    }
    
    vars = states[state]
    normaldist = np.random.normal(vars[0], sqrt(vars[1]), 1)

    return normaldist


if __name__ == '__main__':

    for state in energyArrivalStates(10):
        print(state)
        print(energyArrivalOutput(state))
