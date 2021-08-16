""" Transmission Policies
1. Picking the cheapest user and only transmitting once
2. Picking the cheapest users and transmitting until there is no more energy (Greedy)
3. Smart

returns energy consumption, energy shared and number of users serviced
"""
import envs
from helpers import calcPowerTransmit

def noEnergyShare(userlist, energystore):
    """ No energy sharing
    """
    energyuselist = [calcPowerTransmit(user[1]) for user in userlist]
    energyuse = [envs.ENERGY_USE_BASE]

    for item in energyuselist:
        if energystore < sum(energyuse):
            break
        energyuse.append(item)

    serviced = len(energyuse) - 1

    return sum(energyuse), 0, serviced

def pickCheapTransmitOnce():
    """ Picking the cheapest user and only transmitting once
    """
    pass

def pickCheapTransmitGreedy():
    """Picking the cheapest users and transmitting until there is no more energy (Greedy)
    """
    pass

def pickSmartTransmit():
    """ Smart energy usage
    """
    pass

def energyPolicy(sel):
    """ Calls the respective function for energy usage policy
    """
