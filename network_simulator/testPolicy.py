""" Energy Policy Tests

"""
import matplotlib.pyplot as plt
from network_simulator.components import simulator
from progress.bar import Bar

def energyPolicyTest(init_vars, aplist, usrlist):
    # Initilise environment variables
    total_runs = range(20)
    
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

    return plt
