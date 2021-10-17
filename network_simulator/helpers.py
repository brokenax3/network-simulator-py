from math import sqrt
import numpy as np
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
    # print('\033[1;31mRunning Simulation with these parameters:\033[0;0m')
    # for key, value in _init_vars.items():
    #     if key != "markov":
    #         print('    \033[1;32m {}\033[0;0m : {}'.format(key, value))

    # print('Read Generated Components from Binary File.')

    return _init_vars, _aplist, _usrlist, _usrlist_ppp

def writeSimCache(filename, data):
    with open('sim_cache/' + filename + '.data', 'wb') as file:
        pickle.dump(data, file)

def readSimCache(filename):
    with open('sim_cache/' + filename + '.data', 'rb') as file:
        data = pickle.load(file)
    return data

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


def movementGiveCoord(movement, coordinate, GRID_SIZE):
    n1 = movement[0]
    n2 = movement[1]

    new_coordinate = [0, 0]

    if(coordinate[0] + n1 > GRID_SIZE):
        new_coordinate[0] = GRID_SIZE + (GRID_SIZE - (coordinate[0] + n1))
    elif(coordinate[0] + n1 < 0):
        new_coordinate[0] = -(coordinate[0] + n1)
    else:
        new_coordinate[0] = coordinate[0] + n1
    # For y coordinate
    if(coordinate[1] + n2 > GRID_SIZE):
        new_coordinate[1] = GRID_SIZE + (GRID_SIZE - (coordinate[1] + n2))
    elif(coordinate[1] + n2 < 0):
        new_coordinate[1] = -(coordinate[1] + n2)
    else:
        new_coordinate[1] = coordinate[1] + n2
    
    return new_coordinate


def genUserMovementLoc(length, time, limit, GRID_SIZE, ppp, pppcoord):
    _loc = []
    time = time + 1

    if ppp == 0:
        # Starting Coordinates for Users
        _x_start = np.random.uniform(0, GRID_SIZE, size=length)
        _y_start = np.random.uniform(0, GRID_SIZE, size=length)
    else: 
        _x_start = pppcoord[0]
        _y_start = pppcoord[1]

    _coord_start = list(zip(_x_start, _y_start))
    # print(_coord_start)
    
    _loc = [list(zip(np.random.uniform(-limit, limit, size=time), np.random.uniform(-limit, limit, size=time))) for item in range(length)] 

    _new_coord_u = {}
    for item in range(length):
        _new_coord_u[item] = []

    for i, _coord in enumerate(_coord_start):
        _new_coord = [[_coord[0], _coord[1]]]
        for t in range(time):
            _new_coord.append(movementGiveCoord(_loc[i][t], _new_coord[-1:][0], GRID_SIZE))
        _new_coord_u[i] = _new_coord

    # for item in _new_coord_u:
    #     print(item[0])

    return _new_coord_u

# if __name__ == "__main__":
#     print(genDescendUnitArray(40, 1, 0.2))
#     print(genDescendUnitArray(5, 1, 0.2))

#     print(genDescendUnitArray(40, 1, 0.6))
#     print(genDescendUnitArray(5, 1, 0.6))

#     print(genDescendUnitArray(40, 0, 0.6))
#     print(genDescendUnitArray(5, 0, 0.6))
