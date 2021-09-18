from math import sqrt
import datetime
import pickle
from . import envs

def calcDistance(x1, y1, x2, y2):
    """ Calculate the distance between two points 
    """

    return sqrt((x1 - x2)*(x1 - x2) + (y1 - y2)*(y1 - y2))

def calcPowerTransmit(distance):
    """ Calculate the transmit power required to satisfy POWER_RECEIVED_REQUIRED

    Pu = POWER_RECEIVED_REQUIRED * (pow(distance, alpha))
    Channel Gain is 1/(d^alpha)
    alpha is the path loss exponent between 2 and 4

    Returns transmit power in Watts
    """

    alpha = 2
    # Pu = envs.POWER_RECEIVED_REQUIRED * (pow(distance, alpha))
    Pu = envs.POWER_RECEIVED_REQUIRED * (distance ** alpha)

    return Pu * 60 * 5

def writeDataToFile(input, filename):
    f = open(filename, "a")

    input = str(datetime.datetime.now()) + "\n" + input

    f.write(input)
    f.close()

def writeGeneratedComponents(init_vars, aplist, usrlist, usrlist_ppp):

    with open('generated/init_vars.data', 'wb') as file:
        pickle.dump(init_vars, file)

    with open('generated/aplist.data', 'wb') as file:
        pickle.dump(aplist, file)

    with open('generated/usrlist.data', 'wb') as file:
        pickle.dump(usrlist, file)

    with open('generated/usrlist_ppp.data', 'wb') as file:
        pickle.dump(usrlist_ppp, file)

    print('Wrote Generated Components to Binary File.')

def readGeneratedComponents():

    with open('generated/init_vars.data', 'rb') as file:
        _init_vars = pickle.load(file)

    with open('generated/aplist.data', 'rb') as file:
        _aplist = pickle.load(file)

    with open('generated/usrlist.data', 'rb') as file:
        _usrlist = pickle.load(file)

    with open('generated/usrlist_ppp.data', 'rb') as file:
        _usrlist_ppp = pickle.load(file)

    # Unpack some vars to show simulation parameters
    print('\033[1;31mRunning Simulation with these parameters:\033[0;0m')
    for key, value in _init_vars.items():
        if key != "markov":
            print('    \033[1;32m {}\033[0;0m : {}'.format(key, value))

    print('Read Generated Components from Binary File.')

    return _init_vars, _aplist, _usrlist, _usrlist_ppp

def genDescendUnitArray(llength, sel, ratio):

    if sel == 0:
        for length in range(1, llength + 1):
            array = [2*x/(length * (length + 1)) for x in range(length,0,-1)]
    elif sel == 1:
        
        """ Allocation based on Geometric Series
        """
        r = ratio

        tmp_array = [r ** length for length in range(llength)]
        sum_tmp_array = sum(tmp_array)
        array = [item / sum_tmp_array for item in tmp_array]

        return array
