from math import sqrt
from random import uniform
import envs


def calcDistance(x1, y1, x2, y2):
    """ Calculate the distance between two points 
    """

    return sqrt(pow((x1 - x2),2) + pow((y1 - y2),2))

def calcPowerTransmit(distance):
    """ Calculate the transmit power required to satisfy POWER_RECEIVED_REQUIRED

    Pu = POWER_RECEIVED_REQUIRED * (pow(distance, alpha))
    Channel Gain is 1/(d^alpha)
    alpha is the path loss exponent between 2 and 4

    Returns transmit power in Watts
    """

    alpha = uniform(2,4)
    Pu = envs.POWER_RECEIVED_REQUIRED * (pow(distance, alpha))

    return Pu
