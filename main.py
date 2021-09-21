from random import randint, uniform
import matplotlib.pyplot as plt
from pathlib import Path
# from network_simulator.components import simulator
from network_simulator.components import Location
from network_simulator.components import AccessPoint
from network_simulator.components import User
from network_simulator.poissonPointProcess import generateUsersPPP
from network_simulator.discreteMarkov import energyArrivalStates
from network_simulator.test.testTransmissionPolicy import transmissionPolicyTest
from network_simulator.test.testLoadBalancing import loadBalancing
from network_simulator.test.testSeriesRatio import seriesRatio
from network_simulator.test.testShareBudget import shareBudget
from network_simulator.helpers import genDescendUnitArray, writeGeneratedComponents, readGeneratedComponents
# from progress.bar import Bar

def initVariable():
    """ Initilise starting variables

    A dict is generated and modified as needed. This modified dict is passed into the simulator.
    Time unit 5 minutes.
    """

    init_vars = {
        "GRID_SIZE" : 50,
        "ENERGY_STORE_MAX" : 120000, # Joules
        "ENERGY_GEN_MAX" : 0.75, # Not used atm
        "PANEL_SIZE" : 8, # cm^2
        "ENERGY_USE_BASE" : 1950, # Joules every 5 minutes
        "AP_TOTAL" : 5,
        "USR_TOTAL" : 100,
        "POWER_RECEIVED_DBM" : -70, 
        "TIME_MAX" : 8064,
        "DIST_MOVEUSER_MAX" : 5,
        "ENERGY_POLICY" : 0,
        "SHARE_ENERGY" : 0,
        "ENERGY_BUDGET" : 0.2,
        "LOAD_BALANCE" : 0,
        "USR_LIMIT" : 10,
        "SERIES_RATIO" : 0.2,
    }

    init_vars["POWER_RECEIVED_REQUIRED"] = 1 * pow(10, init_vars["POWER_RECEIVED_DBM"]/10) * 0.001

    GRID_SIZE = init_vars["GRID_SIZE"]
    ENERGY_STORE_MAX = init_vars["ENERGY_STORE_MAX"]
    AP_TOTAL = init_vars["AP_TOTAL"]
    USR_TOTAL = init_vars["USR_TOTAL"]
    init_vars["markov"] = energyArrivalStates(init_vars["TIME_MAX"])
    init_vars["descendunit_arr"] = genDescendUnitArray(init_vars["AP_TOTAL"], 1, init_vars["SERIES_RATIO"])

    # Generate fixed User and AP list
    gen_aplist = [AccessPoint(index, Location(uniform(0, GRID_SIZE), uniform(0, GRID_SIZE)), randint(ENERGY_STORE_MAX * 0.4, ENERGY_STORE_MAX)) for index in range(AP_TOTAL)]

    # Generating Users using Possion Point Process Placment
    usr_x, usr_y = generateUsersPPP(GRID_SIZE, USR_TOTAL / GRID_SIZE / GRID_SIZE)
    gen_usrlist_ppp = [User(i, Location(usr_x[i], usr_y[i])) for i in range(len(usr_x))]

    # Generating Users using Randint Placment
    gen_usrlist = [User(index, Location(uniform(0, GRID_SIZE), uniform(0, GRID_SIZE))) for index in range(USR_TOTAL)]

    return init_vars, gen_aplist, gen_usrlist, gen_usrlist_ppp

def main():

    # total_runs = range(5)
    """ Generate Simulation Components

    Set to 0 to use existing parameters.
    """
    gen_vars = 0
    save = 0

    file = Path('generated/init_vars.data')
    if file.exists() and gen_vars == 0:
        # Read Generated Components from File
        init_vars, aplist, usrlist, usrlist_ppp = readGeneratedComponents()
    elif gen_vars == 1:
        # Generate Components to File
        init_vars, aplist, usrlist, usrlist_ppp = initVariable()

        if save == 1:
            writeGeneratedComponents(init_vars, aplist, usrlist, usrlist_ppp)
    else:
        print("File does not exist and gen_vars = {}".format(gen_vars))
        exit()

    # plt_poltest = transmissionPolicyTest(init_vars, aplist, usrlist_ppp)
    # plt_poltest.savefig('figures/transmissionpolicy.png')

    # plt.figure(2, dpi=600, figsize=[10, 12])
    # plt_loadbalance = loadBalancing(init_vars, aplist, usrlist_ppp)
    # plt_loadbalance.savefig('figures/loadbalance.png')

    # plt_seriesratio = seriesRatio(init_vars, aplist, usrlist_ppp)
    # plt_seriesratio.savefig('figures/seriesratio.png')

    # plt_budgettest = shareBudget(init_vars, aplist, usrlist_ppp)
    # plt_budgettest.savefig('figures/sharebudget.png')

if __name__ == '__main__':
    main()
