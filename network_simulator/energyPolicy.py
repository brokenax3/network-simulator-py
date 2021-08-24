""" Transmission Policies
1. Picking the cheapest user and only transmitting once
2. Picking the cheapest users and transmitting until there is no more energy (Greedy)
3. Smart

returns energy consumption, energy shared and number of users serviced
"""
from . import envs
from .helpers import calcPowerTransmit

def noTransmitPolicy(userlist, energystore):
    """ No energy sharing
    """
    energyuselist = [calcPowerTransmit(user[1]) for user in userlist]
    energyuse = [envs.ENERGY_USE_BASE]

    for item in energyuselist:
        if energystore < sum(energyuse):
            break
        energyuse.append(item)

    serviced = len(energyuse) - 1

    return sum(energyuse), serviced

def pickCheapTransmitOnce(userlist, energystore):
    """ Picking the cheapest user and only transmitting once
    """
    energyuselist = [calcPowerTransmit(user[1]) for user in userlist]
    serviced = 0
    cheapest = [envs.ENERGY_USE_BASE]

    if energyuselist == []:
        return 0, 0

    if energystore > min(energyuselist):
        cheapest.append(min(energyuselist))
        serviced = 1

    return sum(cheapest), serviced

def pickCheapTransmitGreedy(userlist, energystore):
    """Picking the cheapest users and transmitting until there is no more energy (Greedy)
    """
    energyuselist = [calcPowerTransmit(user[1]) for user in userlist]
    energyuselist.sort()
    energyuse = [envs.ENERGY_USE_BASE]

    for item in energyuselist:
        if energystore < sum(energyuse):
            break
        energyuse.append(item)

    serviced = len(energyuse) - 1

    return sum(energyuse), serviced

def pickSmartTransmit():
    """ Smart energy usage
    """
    pass

def energyPolicy(sel, userlist, energystore):
    """ Calls the respective function for energy usage policy
    """
    if sel == 0:
        out = noTransmitPolicy(userlist, energystore)
    elif sel == 1:
        out = pickCheapTransmitOnce(userlist, energystore)
    elif sel == 2:
        out = pickCheapTransmitGreedy(userlist, energystore)
    else:
        out = [0, 0]
        print("Energy consumption policy not selected")

    return out
