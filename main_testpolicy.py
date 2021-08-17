""" Energy Policy Tests

"""
from random import randint
import matplotlib.pyplot as plt
from network_simulator.components import simulator
from network_simulator.components import Location
from network_simulator.components import AccessPoint
from network_simulator.components import User
from network_simulator.poissonPointProcess import generateUsersPPP
from network_simulator.discreteMarkov import energyArrivalStates
from progress.bar import Bar

def initVariable(ppp):
    """ Initilise starting variables

    A dict is generated and modified as needed. This modified dict is passed into the simulator.
    Time unit 5 minutes.
    """

    init_vars = {
        "GRID_SIZE" : 50,
        "ENERGY_STORE_MAX" : 576, # Watt 5 minutes
        "ENERGY_GEN_MAX" : 0.75, # Watt  
        "PANEL_SIZE" : 5, # cm^2
        "ENERGY_USE_BASE" : 0.4417, # Watt per 5 minutes 5.3/60*5
        "AP_TOTAL" : 5,
        "USR_TOTAL" : 100,
        "POWER_RECEIVED_DBM" : -60, 
        "TIME_MAX" : 10000,
        "DIST_MOVEUSER_MAX" : 5,
        "ENERGY_POLICY" : 0,
        "SHARE_ENERGY" : 0,
    }
    init_vars["POWER_RECEIVED_REQUIRED"] = 1 * pow(10, init_vars["POWER_RECEIVED_DBM"]/10) * 60 * 5 * 0.001 # Watts per 5 minutes

    GRID_SIZE = init_vars["GRID_SIZE"]
    ENERGY_STORE_MAX = init_vars["ENERGY_STORE_MAX"]
    AP_TOTAL = init_vars["AP_TOTAL"]
    USR_TOTAL = init_vars["USR_TOTAL"]

    # Generate fixed User and AP list
    aplist = [AccessPoint(index, Location(randint(0, GRID_SIZE), randint(0, GRID_SIZE)), randint(0, ENERGY_STORE_MAX)) for index in range(AP_TOTAL)]

    if ppp == 1:
        usr_x, usr_y = generateUsersPPP(GRID_SIZE, USR_TOTAL / GRID_SIZE / GRID_SIZE)

        usrlist = [User(i, Location(usr_x[i], usr_y[i])) for i in range(len(usr_x))]
    else:
        usrlist = [User(index, Location(randint(0, GRID_SIZE), randint(0, GRID_SIZE))) for index in range(USR_TOTAL)]
    return init_vars, aplist, usrlist

if __name__ == "__main__":

    # Initilise environment variables
    total_runs = range(5)
    init_vars, aplist, usrlist = initVariable(1)
    markovstates = energyArrivalStates(init_vars["TIME_MAX"])
    init_vars["markov"] = markovstates



    """ Test Policy 1:
            - No Energy Share
            - No PPP
    """
    bar = Bar('Running simulation (Energy Policy: No Energy Sharing)', max=len(total_runs))
    serviced_noshare = []

    init_vars["ENERGY_POLICY"] = 0
    for run in total_runs:
        serviced_noshare.append(simulator(init_vars, aplist, usrlist))
        bar.next()
    bar.finish()
    avg_serviced_noshare = sum(serviced_noshare) / len(total_runs)



    """ Test Policy 2:
            - Only servicing the cheapest user
            - No PPP
    """
    bar = Bar('Running simulation (Energy Policy: Cheapest User)', max=len(total_runs))
    serviced_cheapest = []

    init_vars["ENERGY_POLICY"] = 1
    for run in total_runs:
        serviced_cheapest.append(simulator(init_vars, aplist, usrlist))
        bar.next()
    bar.finish()
    avg_serviced_cheapest = sum(serviced_cheapest) / len(total_runs)



    """ Test Policy 3:
            - Only servicing the cheapest users (More than one)
            - No PPP
    """
    bar = Bar('Running simulation (Energy Policy: Cheapest Users)', max=len(total_runs))
    serviced_cheapestusers = []

    init_vars["ENERGY_POLICY"] = 2
    for run in total_runs:
        serviced_cheapestusers.append(simulator(init_vars, aplist, usrlist))
        bar.next()
    bar.finish()
    avg_serviced_cheapestusers = sum(serviced_cheapestusers) / len(total_runs)



    print("Total Serviced Users (No Energy Sharing): {}".format(serviced_noshare))
    print("Total Serviced Users (Cheapest): {}".format(serviced_cheapest))
    print("Total Serviced Users (Cheapest Users): {}".format(serviced_cheapestusers))

    plot = plt.figure(1)
    plt.plot(range(len(serviced_noshare)), serviced_noshare, label="No Share")
    plt.plot(range(len(serviced_cheapest)), serviced_cheapest, label="Cheapest User")
    plt.plot(range(len(serviced_cheapestusers)), serviced_cheapestusers, label="Cheapest Users")
    plt.legend()
    plt.xlabel('Index of Simulation')
    plt.ylabel('Total Number of Serviced Users')
    plt.title('Total Number of Serviced users on Energy Policies')
    plt.savefig('energypolicyppp.png')


    
