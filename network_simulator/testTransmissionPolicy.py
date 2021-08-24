""" Transmission Policy Tests

"""
import matplotlib.pyplot as plt
from network_simulator.components import simulator
from progress.bar import Bar
from network_simulator.helpers import writeDataToFile 

def transmissionPolicyTest(init_vars, aplist, usrlist):
    # Initilise environment variables
    total_runs = range(5)

    """ Test Policy 1:
            - No Transmission Policy
            - No Energy Sharing
    """
    bar = Bar('Running simulation (Energy Policy: No Transmission Policy)', max=len(total_runs))
    serviced_nopolicy = []

    init_vars["ENERGY_POLICY"] = 0
    for run in total_runs:
        serviced_nopolicy.append(simulator(init_vars, aplist, usrlist))
        bar.next()
    bar.finish()
    avg_serviced_nopolicy = sum(serviced_nopolicy) / len(total_runs)



    """ Test Policy 2:
            - Only servicing the cheapest user
            - No Energy Sharing
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
            - No Energy Sharing
    """
    bar = Bar('Running simulation (Energy Policy: Cheapest Users)', max=len(total_runs))
    serviced_cheapestusers = []

    init_vars["ENERGY_POLICY"] = 2
    for run in total_runs:
        serviced_cheapestusers.append(simulator(init_vars, aplist, usrlist))
        bar.next()
    bar.finish()
    avg_serviced_cheapestusers = sum(serviced_cheapestusers) / len(total_runs)


    """ Test Policy 1 and Energy Sharing:
            - No Transmission Policy
            - Energy Sharing
    """
    bar = Bar('Running simulation (Energy Policy: No Transmission Policy and Energy Share Even)', max=len(total_runs))
    serviced_nopolicy_shareeven = []

    init_vars["ENERGY_POLICY"] = 0
    init_vars["SHARE_ENERGY"] = 1
    for run in total_runs:
        serviced_nopolicy_shareeven.append(simulator(init_vars, aplist, usrlist))
        bar.next()
    bar.finish()
    avg_serviced_nopolicy_shareeven = sum(serviced_nopolicy_shareeven) / len(total_runs)



    """ Test Policy 2 and Energy Sharing:
            - Only servicing the cheapest user
            - Energy Sharing
    """
    bar = Bar('Running simulation (Energy Policy: Cheapest User and Energy Share Even)', max=len(total_runs))
    serviced_cheapest_shareeven = []

    init_vars["ENERGY_POLICY"] = 1
    init_vars["SHARE_ENERGY"] = 1
    for run in total_runs:
        serviced_cheapest_shareeven.append(simulator(init_vars, aplist, usrlist))
        bar.next()
    bar.finish()
    avg_serviced_cheapest_shareeven = sum(serviced_cheapest_shareeven) / len(total_runs)



    """ Test Policy 3 and Energy Sharing:
            - Only servicing the cheapest users (More than one)
            - Energy Sharing
    """
    bar = Bar('Running simulation (Energy Policy: Cheapest Users and Energy Share Even)', max=len(total_runs))
    serviced_cheapestusers_shareeven = []

    init_vars["ENERGY_POLICY"] = 2
    init_vars["SHARE_ENERGY"] = 1
    for run in total_runs:
        serviced_cheapestusers_shareeven.append(simulator(init_vars, aplist, usrlist))
        bar.next()
    bar.finish()
    avg_serviced_cheapestusers_shareeven = sum(serviced_cheapestusers_shareeven) / len(total_runs)

    print("Total Serviced Users (No Transmission Policy): {}".format(avg_serviced_nopolicy))
    print("Total Serviced Users (Cheapest): {}".format(avg_serviced_cheapest))
    print("Total Serviced Users (Cheapest Users): {}".format(avg_serviced_cheapestusers))

    print("Total Serviced Users (No Transmission Policy) (Share Even): {}".format(avg_serviced_nopolicy_shareeven))
    print("Total Serviced Users (Cheapest) (Share Even): {}".format(avg_serviced_cheapest_shareeven))
    print("Total Serviced Users (Cheapest Users) (Share Even): {}".format(avg_serviced_cheapestusers_shareeven))

    plot = plt.figure(1)
    plt.plot(range(len(serviced_nopolicy)), serviced_nopolicy, label="No Transmission Policy")
    plt.plot(range(len(serviced_cheapest)), serviced_cheapest, label="Cheapest User")
    plt.plot(range(len(serviced_cheapestusers)), serviced_cheapestusers, label="Cheapest Users")

    plt.plot(range(len(serviced_nopolicy_shareeven)), serviced_nopolicy_shareeven, label="No Transmission Policy (Share Even)", alpha=0.8)
    plt.plot(range(len(serviced_cheapest_shareeven)), serviced_cheapest_shareeven, label="Cheapest User (Share Even)", alpha=0.8)
    plt.plot(range(len(serviced_cheapestusers_shareeven)), serviced_cheapestusers_shareeven, label="Cheapest Users (Share Even)", alpha=0.8)

    plt.legend()
    plt.xlabel('Index of Simulation')
    plt.ylabel('Total Number of Serviced Users')
    plt.title('Total Number of Serviced users on Transmission Policies')

    savedOutput = """
    serviced_nopolicy = {}
    serviced_cheapest = {}
    serviced_cheapestusers = {}

    serviced_nopolicy_shareeven = {}
    serviced_cheapest_shareeven = {}
    serviced_cheapestusers_shareeven = {}
    """.format(serviced_nopolicy, serviced_cheapest, serviced_cheapestusers, serviced_nopolicy_shareeven, serviced_cheapest_shareeven, serviced_cheapestusers_shareeven)

    writeDataToFile(savedOutput)
    
    return plt
