from math import sqrt
import datetime
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

def writeDataToFile(input):
    f = open("collected_data.txt", "a")

    input = str(datetime.datetime.now()) + "\n" + input

    f.write(input)
    f.close()

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
