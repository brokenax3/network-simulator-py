""" Energy Distributor

This module returns an amount of energy which satisfies a certain energy sharing policy.

energystats:

["ap.id", "ap.energystore", "ap.data_energyarrival", "ap.data_energyuse", "ap.servicedusers"]

energydistributed:

["id", "energyin"]
"""
from operator import itemgetter

def efficiencyDistribute(energystats):
    pass   

def energyUseDistribute(energystats, array):
    """ Distribute Energy depending on past energy usage

    """
    energyusestats = list()
    totalenergy = 0

    for item in energystats:
        totalenergy = totalenergy + item[1]
        energyusestats.append([item[0],  sum(item[3])])
    # print("USE STATS: {}".format(energyusestats))

    energyusestats.sort(key=itemgetter(1), reverse=True)

    if len(energyusestats) > 1:
        energy = list(map(lambda x: x * totalenergy, array))
        energydistributed = list(zip([item[0] for item in energyusestats], energy))
    else:
        print("Energy cannot be distributed with one member")
        energydistributed = [0, totalenergy]
    # print(energydistributed)

    return sorted(energydistributed, key=itemgetter(0))

def energyArrivalDistribute(energystats):
    pass   

def evenDistribute(energystats):
    """ Even Distribution of Energy
    
    Collects all the energy and distributing it evenly to all Access Points
    """

    totalenergy = 0
    energydistributed = []

    for apstat in energystats:
        totalenergy = totalenergy + apstat[1]


    each_energy = totalenergy / len(energystats)

    # print("The total energy of all Access Points is: {}".format(totalenergy))
    # print("This total is divided by {} and allocating {} to each Access Point".format(len(energystats), each_energy))

    for item in energystats:
        energydistributed.append([item[0], each_energy])

    return energydistributed

def genEnergyStats(aplist):
    
    energystats = []

    for ap in aplist:
        energystats.append([ap.id, ap.energy_store, ap.data_energyarrival, ap.data_energyuse, ap.service_counter])

    # print(energystats)

    return energystats

def energyDistributeSel(aplist, sel, descendunit_arr):

    # Generate energystats
    energystats = genEnergyStats(aplist)

    if sel == 1:
        energydistributed = evenDistribute(energystats)
    elif sel == 2:
        energydistributed = energyArrivalDistribute(energystats)
    elif sel == 3: 
        energydistributed = energyUseDistribute(energystats, descendunit_arr)
    elif sel == 4:
        energydistributed = efficiencyDistribute(energystats)
    else:
        energydistributed = [[0, 0]*len(aplist)]

    return energydistributed



