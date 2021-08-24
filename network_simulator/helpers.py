from math import sqrt
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

    f.write(input)
    f.close()

    
