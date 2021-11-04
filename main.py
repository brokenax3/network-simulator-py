from random import randint, uniform
from copy import deepcopy
# import matplotlib.pyplot as plt
from bokeh.io import export_png, export_svg
from pathlib import Path
from os import remove
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
from network_simulator.test.testMultiArmBandit import mab
from network_simulator.test.testMultiProcessing import multiSimulation
from network_simulator.test.testSeriesRatioMP import seriesRatioMP
from network_simulator.test.testMultiArmBanditMP import mabMP
from network_simulator.test.testAlgorithmCompare import algorithmCompare
from network_simulator.test.testAPnumber import APNumberCompare
from network_simulator.test.testUserNumber import UserNumberCompare
from network_simulator.test.testPPPlambda import PPPlambdaCompare
from network_simulator.test.testStorageCapacity import energyStoreMaxCompare
from network_simulator.test.testUserMovement import userMovementDist
from network_simulator.test.testDataframeSize import dataframeSize
from network_simulator.test.testUCB1scale import mabUcbScale
from network_simulator.test.testPanelSize import panelSizeCompare
from network_simulator.helpers import genDescendUnitArray, writeGeneratedComponents, readGeneratedComponents, genUserMovementLoc


def initVariable():
    """ Initilise starting variables

    A dict is generated and modified as needed. This modified dict is passed into the simulator.
    Time unit 5 minutes.
    """

    # if Path("sim_cache/test/mabactionhistory.data").exists():
    #     remove("sim_cache/test/mabactionhistory.data")

    # if Path("sim_cache/test/mabscorehistory.data").exists():
    #     remove("sim_cache/test/mabscorehistory.data")

    init_vars = {
        "GRID_SIZE" : 50,
        "ENERGY_STORE_MAX" : 120000, # Joules
        "ENERGY_GEN_MAX" : 0.75, # Not used atm
        "PANEL_SIZE" : 8, # cm^2
        "ENERGY_USE_BASE" : 1950, # Joules every 5 minutes
        "AP_TOTAL" : 5,
        "USR_TOTAL" : 100,
        # "POWER_RECEIVED_DBM" : -70, 
        "TIME_MAX" : 8064,
        "DIST_MOVEUSER_MAX" : 5,
        "ENERGY_POLICY" : 0,
        "SHARE_ENERGY" : 0,
        "ENERGY_BUDGET" : 0.2,
        "LOAD_BALANCE" : 0,
        "USR_LIMIT" : 10,
        "SERIES_RATIO" : 0.2,
        "SMART_PARAM" : [0.01, 12]
    }

    # init_vars["POWER_RECEIVED_REQUIRED"] = 1 * pow(10, init_vars["POWER_RECEIVED_DBM"]/10) * 0.001

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
    init_vars["coord_start_x"] = usr_x 
    init_vars["coord_start_y"] = usr_y 
    # init_vars["usr_mov_loc_ppp"] = genUserMovementLoc(len(usr_x), init_vars["TIME_MAX"], init_vars["DIST_MOVEUSER_MAX"], init_vars["GRID_SIZE"], 1, [usr_x, usr_y]) 

    gen_usrlist_ppp = [User(i, Location(usr_x[i], usr_y[i])) for i in range(len(usr_x))]

    # Generating Users using Randint Placment
    usr_mov_loc = genUserMovementLoc(USR_TOTAL, init_vars["TIME_MAX"], init_vars["DIST_MOVEUSER_MAX"], init_vars["GRID_SIZE"], 0, [0, 0]) 
    gen_usrlist = [User(index, Location(usr_mov_loc[index][0][0], usr_mov_loc[index][0][1])) for index in range(USR_TOTAL)]

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

    # init_vars["ppp"] = 1
    # plt_apnum = APNumberCompare(deepcopy(init_vars), aplist, usrlist_ppp)
    # export_svg(plt_apnum, filename="figures/totalapnum.svg")

    # init_vars, aplist, usrlist, usrlist_ppp = readGeneratedComponents()
    # init_vars["ppp"] = 0
    # plt_usernum = UserNumberCompare(deepcopy(init_vars), aplist, usrlist_ppp)
    # export_svg(plt_usernum, filename="figures/totalusernum.svg")

    # init_vars, aplist, usrlist, usrlist_ppp = readGeneratedComponents()
    # init_vars["ppp"] = 1
    # plt_energystoremax = energyStoreMaxCompare(deepcopy(init_vars), aplist, usrlist_ppp)
    # export_svg(plt_energystoremax, filename="figures/energystoremax.svg")

    # init_vars, aplist, usrlist, usrlist_ppp = readGeneratedComponents()
    # init_vars["ppp"] = 1
    # plt_ppp = PPPlambdaCompare(deepcopy(init_vars), aplist, usrlist_ppp)
    # export_svg(plt_ppp, filename="figures/ppplambda.svg")

    # init_vars, aplist, usrlist, usrlist_ppp = readGeneratedComponents()
    # init_vars["ppp"] = 1
    # plt_loadbalance = loadBalancing(deepcopy(init_vars), aplist, usrlist_ppp)
    # export_svg(plt_loadbalance, filename="figures/loadbalance.svg")
    # export_png(plt_loadbalance, filename="figures/loadbalance.png", width=50, height=70)

    # init_vars, aplist, usrlist, usrlist_ppp = readGeneratedComponents()
    # init_vars["ppp"] = 1
    # plt_usermovement = userMovementDist(deepcopy(init_vars), aplist, usrlist_ppp)
    # export_svg(plt_usermovement, filename="figures/usermovement.svg")

    # init_vars, aplist, usrlist, usrlist_ppp = readGeneratedComponents()
    # init_vars["ppp"] = 1
    # plt_dataframe = dataframeSize(deepcopy(init_vars), aplist, usrlist_ppp)
    # export_svg(plt_dataframe, filename="figures/dataframesize.svg")

    # init_vars, aplist, usrlist, usrlist_ppp = readGeneratedComponents()
    # init_vars["ppp"] = 1
    # plt_seriesratio = seriesRatioMP(deepcopy(init_vars), aplist, usrlist_ppp)
    # export_svg(plt_seriesratio, filename="figures/seriesratio.svg")

    # init_vars, aplist, usrlist, usrlist_ppp = readGeneratedComponents()
    # init_vars["ppp"] = 1
    # plt_mab = mabMP(deepcopy(init_vars), aplist, usrlist_ppp)
    # export_svg(plt_mab, filename="figures/epsilongreedy.svg")

    # init_vars, aplist, usrlist, usrlist_ppp = readGeneratedComponents()
    # init_vars["ppp"] = 1
    # plt_ucbtest = mabUcbScale(deepcopy(init_vars), aplist, usrlist_ppp)
    # export_png(plt_ucbtest, filename="figures/ucbtest.png")

    # init_vars, aplist, usrlist, usrlist_ppp = readGeneratedComponents()
    # init_vars["ppp"] = 1
    # plt_panelsize = panelSizeCompare(deepcopy(init_vars), aplist, usrlist_ppp)
    # export_svg(plt_panelsize, filename="figures/panelsize.svg")

    init_vars, aplist, usrlist, usrlist_ppp = readGeneratedComponents()
    init_vars["ppp"] = 1
    plt_compare = algorithmCompare(deepcopy(init_vars), aplist, usrlist_ppp)
    export_svg(plt_compare, filename="figures/algorithmCompare.svg")

if __name__ == "__main__":
    main()
