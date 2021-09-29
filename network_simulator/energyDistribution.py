""" Energy Distributor

This module returns an amount of energy which satisfies a certain energy sharing policy.

energystats:

["ap.id", "ap.energystore", "ap.data_energyarrival", "ap.data_energyuse", "ap.servicedusers"]

energydistributed:

["id", "energyin"]
"""
from operator import itemgetter
from network_simulator.multiArmBandit import multiArmBanditSel

def efficiencyDistribute(energystats, array):
    """ Distribute Energy based on efficiency of AP
    """

    totalenergy = 0
    energydistributed = []
    distribution = []
    efficiency = []
    energy = []

    for item in energystats:
        totalenergy = totalenergy + item[1]
        efficiency_i = (sum(item[3]) / item[4]) if item[4] != 0 else 0
        efficiency.append([item[0], efficiency_i])

    efficiency.sort(key=itemgetter(1), reverse=True)

    if len(efficiency) > 1:
        energy = [arr_item * totalenergy for arr_item in array]
        energydistributed = [[efficiency[i][0], energy_item] for i, energy_item in enumerate(energy)]

    else:
        print("Energy cannot be distributed with one member")
        energydistributed = [[0, totalenergy]*len(array)]

    distribution = sorted(energydistributed, key=itemgetter(0))

    return distribution


def energyUseDistribute(energystats, array):
    """ Distribute Energy depending on past energy usage

    """
    totalenergy = 0
    energydistributed = []
    energyusestats = []

    for item in energystats:
        totalenergy = totalenergy + item[1]

        # Use average of last ten energy use history
        if len(item[3]) > 12:
            _data_energyuse = sum(item[3][-12:]) 
        else:
            _data_energyuse = sum(item[3])

        energyusestats.append([item[0], _data_energyuse])
    # print("USE STATS: {}".format(energyusestats))

    energyusestats.sort(key=itemgetter(1), reverse=True)

    if len(energyusestats) > 1:
        energy = [arr_item * totalenergy for arr_item in array]
        energydistributed = [[energyusestats[i][0], energy_item] for i, energy_item in enumerate(energy)]
    else:
        print("Energy cannot be distributed with one member")
        energydistributed = [[0, totalenergy]*len(array)]
    # print(energydistributed)

    distribution = sorted(energydistributed, key=itemgetter(0))

    return distribution


def energyArrivalDistribute(energystats, array):
    """ Distribute Energy Depending on Past Energy Arrival

    """
    totalenergy = 0
    energydistributed = []
    energyarrival = []

    for item in energystats:
        totalenergy = totalenergy + item[1]

        if len(item[2]) > 12:
            _data_energyarrival = sum(item[2][-12:])
        else:
            _data_energyarrival = sum(item[2])

        energyarrival.append([item[0], _data_energyarrival])

    energyarrival.sort(key=itemgetter(1))

    if len(energyarrival) > 1:
        energy = [arr_item * totalenergy for arr_item in array]
        energydistributed = [[energyarrival[i][0], energy_item] for i, energy_item in enumerate(energy)]
    else:
        print("Energy cannot be distributed with one member")
        energydistributed = [[0, totalenergy]*len(array)]

    distribution = sorted(energydistributed, key=itemgetter(0))

    return distribution


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


def smartDistribute(energystats, aplist, sel, param, time, history):

    # energydistributed = []
    distribution = [[ap.id, 0] for ap in aplist]

    actions, _history = multiArmBanditSel(sel, time, param, aplist, history)
    # for action in actions:
    #     energydistributed.append([action[1], energystats[action[0]][1]]) 
    energydistributed = [[action[1], energystats[action[0]][1]] for action in actions]

    sorted(energydistributed, key=itemgetter(0))


    for distribute in energydistributed:
        distribution[distribute[0]][1] += distribute[1] 
        
    return distribution, _history


def genEnergyStats(aplist, energybudget):
    
    # energystats = []

    energystats = [[ap.id, energybudget[ap.id], ap.data_energyarrival, ap.data_energyuse, ap.service_counter] for ap in aplist]

    # for ap in aplist:
    #     energystats.append([ap.id, energybudget[ap.id], ap.data_energyarrival, ap.data_energyuse, ap.service_counter])

    # print(energystats)

    return energystats


def energyDistributeSel(aplist, sel, descendunit_arr, energybudget, smart_param, time, history):

    # Generate energystats
    energystats = genEnergyStats(aplist, energybudget)

    if sel == 1:
        energydistributed = evenDistribute(energystats)
    elif sel == 2:
        energydistributed = energyArrivalDistribute(energystats, descendunit_arr)
    elif sel == 3: 
        energydistributed = energyUseDistribute(energystats, descendunit_arr)
    elif sel == 4:
        energydistributed = efficiencyDistribute(energystats, descendunit_arr)
    elif sel == 5:
        param = { "epsilon" : smart_param[0],
                "dataframe": smart_param[1]
                }

        energydistributed, history = smartDistribute(energystats, aplist, 0, param, time, history)
    elif sel == 6:
        param = {
                "ucbscale" : smart_param[0],
                "dataframe": smart_param[1]
                }

        energydistributed, history = smartDistribute(energystats, aplist, 1, param, time, history)
    else:
        energydistributed = [[0, 0]*len(aplist)]

    return energydistributed, history



