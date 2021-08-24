""" Energy Distributor

This module returns an amount of energy which satisfies a certain energy sharing policy.

energystats:

["ap.id", "ap.energystore", "ap.data_energyarrival", "ap.data_energyuse", "ap.servicedusers"]

energydistributed:

["id", "energyin", "energyout"]
"""
def efficiencyDistribute(energystats):
    pass   

def energyUseDistribute(energystats):
    pass   

def energyArrivalDistribute(energystats):
    pass   

def evenDistribute(energystats):

    totalenergy = 0
    energydistributed = []

    for apstat in energystats:
        totalenergy = totalenergy + apstat[1]


    each_energy = totalenergy / len(energystats)

    # print("The total energy of all Access Points is: {}".format(totalenergy))
    # print("This total is divided by {} and allocating {} to each Access Point".format(len(energystats), each_energy))

    for item in energystats:
        energydistributed.append([item[0], each_energy, 0])

    return energydistributed

def genEnergyStats(aplist):
    
    energystats = []

    for ap in aplist:
        energystats.append([ap.id, ap.energy_store, ap.data_energyarrival, ap.data_energyuse, ap.service_counter])

    return energystats

def energyDistributeSel(aplist, sel):

    # Generate energystats
    energystats = genEnergyStats(aplist)

    if sel == 0:
        energydistributed = evenDistribute(energystats)
    elif sel == 1:
        energydistributed = energyArrivalDistribute(energystats)
    elif sel == 2:
        energydistributed = energyUseDistribute(energystats)
    elif sel == 3:
        energydistributed = efficiencyDistribute(energystats)
    else:
        energydistributed = [[0, 0]*len(aplist)]

    return energydistributed



