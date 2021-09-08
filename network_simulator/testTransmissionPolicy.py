""" Transmission Policy Tests

"""
import matplotlib.pyplot as plt
from network_simulator.components import simulator
from progress.bar import Bar
from network_simulator.helpers import writeDataToFile 

def transmissionPolicyTest(init_vars, aplist, usrlist):
    # Initilise environment variables
    total_runs = range(100)

    """ Test Policy 1:
            - No Transmission Policy
            - No Energy Sharing
    """
    bar = Bar('Energy Policy: No Transmission Policy', max=len(total_runs))
    serviced_nopolicy = []

    init_vars["ENERGY_POLICY"] = 0
    init_vars["SHARE_ENERGY"] = 0
    for run in total_runs:
        serviced_nopolicy.append(simulator(init_vars, aplist, usrlist))
        bar.next()
    bar.finish()
    avg_serviced_nopolicy = sum(serviced_nopolicy) / len(total_runs)

    """ Test Policy 2:
            - Only servicing the cheapest user
            - No Energy Sharing
    """
    bar = Bar('Energy Policy: Cheapest User', max=len(total_runs))
    serviced_cheapest = []

    init_vars["ENERGY_POLICY"] = 1
    init_vars["SHARE_ENERGY"] = 0
    for run in total_runs:
        serviced_cheapest.append(simulator(init_vars, aplist, usrlist))
        bar.next()
    bar.finish()
    avg_serviced_cheapest = sum(serviced_cheapest) / len(total_runs)

    """ Test Policy 3:
            - Only servicing the cheapest users (More than one)
            - No Energy Sharing
    """
    bar = Bar('Energy Policy: Cheapest Users', max=len(total_runs))
    serviced_cheapestusers = []

    init_vars["ENERGY_POLICY"] = 2
    init_vars["SHARE_ENERGY"] = 0
    for run in total_runs:
        serviced_cheapestusers.append(simulator(init_vars, aplist, usrlist))
        bar.next()
    bar.finish()
    avg_serviced_cheapestusers = sum(serviced_cheapestusers) / len(total_runs)



    """ Energy Shared Evenly Across APs
    """

    """ Test Policy 1 and Energy Sharing:
            - No Transmission Policy
            - Energy Sharing
    """
    bar = Bar('Energy Policy: No Transmission Policy and Energy Share Even', max=len(total_runs))
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
    bar = Bar('Energy Policy: Cheapest User and Energy Share Even', max=len(total_runs))
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
    bar = Bar('Energy Policy: Cheapest Users and Energy Share Even', max=len(total_runs))
    serviced_cheapestusers_shareeven = []

    init_vars["ENERGY_POLICY"] = 2
    init_vars["SHARE_ENERGY"] = 1
    for run in total_runs:
        serviced_cheapestusers_shareeven.append(simulator(init_vars, aplist, usrlist))
        bar.next()
    bar.finish()
    avg_serviced_cheapestusers_shareeven = sum(serviced_cheapestusers_shareeven) / len(total_runs)


    """ Energy Shared based on AP Energy Use
    """

    """ Test Policy 1 and Energy Sharing:
            - No Transmission Policy
            - Energy Sharing (Distributed based on cumulative energy use)
    """
    bar = Bar('Energy Policy: No Transmission Policy and Energy Share Use', max=len(total_runs))
    serviced_nopolicy_shareuse = []

    init_vars["ENERGY_POLICY"] = 0
    init_vars["SHARE_ENERGY"] = 3
    for run in total_runs:
        serviced_nopolicy_shareuse.append(simulator(init_vars, aplist, usrlist))
        bar.next()
    bar.finish()
    avg_serviced_nopolicy_shareuse = sum(serviced_nopolicy_shareuse) / len(total_runs)

    """ Test Policy 2 and Energy Sharing:
            - Only servicing the cheapest user
            - Energy Sharing (Distributed based on cumulative energy use)
    """
    bar = Bar('Energy Policy: Cheapest User and Energy Share Use', max=len(total_runs))
    serviced_cheapest_shareuse = []

    init_vars["ENERGY_POLICY"] = 1
    init_vars["SHARE_ENERGY"] = 3
    for run in total_runs:
        serviced_cheapest_shareuse.append(simulator(init_vars, aplist, usrlist))
        bar.next()
    bar.finish()
    avg_serviced_cheapest_shareuse = sum(serviced_cheapest_shareuse) / len(total_runs)

    """ Test Policy 3 and Energy Sharing:
            - Only servicing the cheapest users (More than one)
            - Energy Sharing (Distributed based on cumulative energy use)
    """
    bar = Bar('Energy Policy: Cheapest Users and Energy Share Use', max=len(total_runs))
    serviced_cheapestusers_shareuse = []

    init_vars["ENERGY_POLICY"] = 2
    init_vars["SHARE_ENERGY"] = 3
    for run in total_runs:
        serviced_cheapestusers_shareuse.append(simulator(init_vars, aplist, usrlist))
        bar.next()
    bar.finish()
    avg_serviced_cheapestusers_shareuse = sum(serviced_cheapestusers_shareuse) / len(total_runs)


    """ Energy Shared based on AP Energy Efficiency
    """

    """ Test Policy 1 and Energy Sharing:
            - No Transmission Policy
            - Energy Sharing (Distributed based on AP efficiency)
    """
    bar = Bar('Energy Policy: No Transmission Policy and Energy Efficiency', max=len(total_runs))
    serviced_nopolicy_efficiency = []

    init_vars["ENERGY_POLICY"] = 0
    init_vars["SHARE_ENERGY"] = 4
    for run in total_runs:
        serviced_nopolicy_efficiency.append(simulator(init_vars, aplist, usrlist))
        bar.next()
    bar.finish()
    avg_serviced_nopolicy_efficiency = sum(serviced_nopolicy_efficiency) / len(total_runs)

    """ Test Policy 2 and Energy Sharing:
            - Only servicing the cheapest user
            - Energy Sharing (Distributed based on AP efficiency)
    """
    bar = Bar('Energy Policy: Cheapest User and Energy Efficiency', max=len(total_runs))
    serviced_cheapest_efficiency = []

    init_vars["ENERGY_POLICY"] = 1
    init_vars["SHARE_ENERGY"] = 4
    for run in total_runs:
        serviced_cheapest_efficiency.append(simulator(init_vars, aplist, usrlist))
        bar.next()
    bar.finish()
    avg_serviced_cheapest_efficiency = sum(serviced_cheapest_efficiency) / len(total_runs)

    """ Test Policy 3 and Energy Sharing:
            - Only servicing the cheapest users (More than one)
            - Energy Sharing (Distributed based on AP efficiency)
    """
    bar = Bar('Energy Policy: Cheapest Users and Energy Efficiency', max=len(total_runs))
    serviced_cheapestusers_efficiency = []

    init_vars["ENERGY_POLICY"] = 2
    init_vars["SHARE_ENERGY"] = 4
    for run in total_runs:
        serviced_cheapestusers_efficiency.append(simulator(init_vars, aplist, usrlist))
        bar.next()
    bar.finish()
    avg_serviced_cheapestusers_efficiency = sum(serviced_cheapestusers_efficiency) / len(total_runs)


    """ Energy Shared based on AP Energy Arrival Rate
    """

    """ Test Policy 1 and Energy Sharing:
            - No Transmission Policy
            - Energy Sharing (Distributed based on AP Energy Arrival)
    """
    bar = Bar('Energy Policy: No Transmission Policy and Energy Arrival', max=len(total_runs))
    serviced_nopolicy_arrival = []

    init_vars["ENERGY_POLICY"] = 0
    init_vars["SHARE_ENERGY"] = 4
    for run in total_runs:
        serviced_nopolicy_arrival.append(simulator(init_vars, aplist, usrlist))
        bar.next()
    bar.finish()
    avg_serviced_nopolicy_arrival = sum(serviced_nopolicy_arrival) / len(total_runs)

    """ Test Policy 2 and Energy Sharing:
            - Only servicing the cheapest user
            - Energy Sharing (Distributed based on AP Energy Arrival)
    """
    bar = Bar('Energy Policy: Cheapest User and Energy Arrival', max=len(total_runs))
    serviced_cheapest_arrival = []

    init_vars["ENERGY_POLICY"] = 1
    init_vars["SHARE_ENERGY"] = 4
    for run in total_runs:
        serviced_cheapest_arrival.append(simulator(init_vars, aplist, usrlist))
        bar.next()
    bar.finish()
    avg_serviced_cheapest_arrival = sum(serviced_cheapest_arrival) / len(total_runs)

    """ Test Policy 3 and Energy Sharing:
            - Only servicing the cheapest users (More than one)
            - Energy Sharing (Distributed based on AP Energy Arrival)
    """
    bar = Bar('Energy Policy: Cheapest Users and Energy Arrival', max=len(total_runs))
    serviced_cheapestusers_arrival = []

    init_vars["ENERGY_POLICY"] = 2
    init_vars["SHARE_ENERGY"] = 4
    for run in total_runs:
        serviced_cheapestusers_arrival.append(simulator(init_vars, aplist, usrlist))
        bar.next()
    bar.finish()
    avg_serviced_cheapestusers_arrival = sum(serviced_cheapestusers_arrival) / len(total_runs)


    print("Total Serviced Users (No Transmission Policy): {}".format(avg_serviced_nopolicy))
    print("Total Serviced Users (Cheapest): {}".format(avg_serviced_cheapest))
    print("Total Serviced Users (Cheapest Users): {}".format(avg_serviced_cheapestusers))

    print("Total Serviced Users (No Transmission Policy) (Share Even): {}".format(avg_serviced_nopolicy_shareeven))
    print("Total Serviced Users (Cheapest) (Share Even): {}".format(avg_serviced_cheapest_shareeven))
    print("Total Serviced Users (Cheapest Users) (Share Even): {}".format(avg_serviced_cheapestusers_shareeven))

    print("Total Serviced Users (No Transmission Policy) (Share Use): {}".format(avg_serviced_nopolicy_shareuse))
    print("Total Serviced Users (Cheapest) (Share Use): {}".format(avg_serviced_cheapest_shareuse))
    print("Total Serviced Users (Cheapest Users) (Share Use): {}".format(avg_serviced_cheapestusers_shareuse))

    print("Total Serviced Users (No Transmission Policy) (AP Efficiency): {}".format(avg_serviced_nopolicy_efficiency))
    print("Total Serviced Users (Cheapest) (AP Efficiency): {}".format(avg_serviced_cheapest_efficiency))
    print("Total Serviced Users (Cheapest Users) (AP Efficiency): {}".format(avg_serviced_cheapestusers_efficiency))

    print("Total Serviced Users (No Transmission Policy) (AP Energy Arrival): {}".format(avg_serviced_nopolicy_arrival))
    print("Total Serviced Users (Cheapest) (AP Energy Arrival): {}".format(avg_serviced_cheapest_arrival))
    print("Total Serviced Users (Cheapest Users) (AP Energy Arrival): {}".format(avg_serviced_cheapestusers_arrival))


    plot = plt.figure(1)
    plt.plot(range(len(serviced_nopolicy)), serviced_nopolicy, label="No Transmission Policy")
    plt.plot(range(len(serviced_cheapest)), serviced_cheapest, label="Cheapest User")
    plt.plot(range(len(serviced_cheapestusers)), serviced_cheapestusers, label="Cheapest Users")

    plt.plot(range(len(serviced_nopolicy_shareeven)), serviced_nopolicy_shareeven, label="No Transmission Policy (Share Even)", marker='o', linestyle='dashed')
    plt.plot(range(len(serviced_cheapest_shareeven)), serviced_cheapest_shareeven, label="Cheapest User (Share Even)", marker='o', linestyle='dashed')
    plt.plot(range(len(serviced_cheapestusers_shareeven)), serviced_cheapestusers_shareeven, label="Cheapest Users (Share Even)", marker='o', linestyle='dashed')

    plt.plot(range(len(serviced_nopolicy_shareuse)), serviced_nopolicy_shareuse, label="No Transmission Policy (Share Use)", marker='*', linestyle='dashdot', linewidth=1.5)
    plt.plot(range(len(serviced_cheapest_shareuse)), serviced_cheapest_shareuse, label="Cheapest User (Share Use)", marker='*', linestyle='dashdot', linewidth=1.5)
    plt.plot(range(len(serviced_cheapestusers_shareuse)), serviced_cheapestusers_shareuse, label="Cheapest Users (Share Use)", marker='*', linestyle='dashdot', linewidth=1.5)

    plt.plot(range(len(serviced_nopolicy_efficiency)), serviced_nopolicy_efficiency, label="No Transmission Policy (AP Efficiency)", marker='x', linestyle='dashdot', linewidth=2)
    plt.plot(range(len(serviced_cheapest_efficiency)), serviced_cheapest_efficiency, label="Cheapest User (AP Efficiency)", marker='x', linestyle='dashdot', linewidth=2)
    plt.plot(range(len(serviced_cheapestusers_efficiency)), serviced_cheapestusers_efficiency, label="Cheapest Users (AP Efficiency)", marker='x', linestyle='dashdot', linewidth=2)

    plt.plot(range(len(serviced_nopolicy_arrival)), serviced_nopolicy_arrival, label="No Transmission Policy (AP Energy Arrival)", marker='s', linestyle='dashdot', linewidth=2)
    plt.plot(range(len(serviced_cheapest_arrival)), serviced_cheapest_arrival, label="Cheapest User (AP Energy Arrival)", marker='s', linestyle='dashdot', linewidth=2)
    plt.plot(range(len(serviced_cheapestusers_arrival)), serviced_cheapestusers_arrival, label="Cheapest Users (AP Energy Arrival)", marker='s', linestyle='dashdot', linewidth=2)


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

    serviced_nopolicy_shareuse = {}
    serviced_cheapest_shareuse = {}
    serviced_cheapestusers_shareuse = {}

    serviced_nopolicy_efficiency = {}
    serviced_cheapest_efficiency = {}
    serviced_cheapestusers_efficiency = {}

    serviced_nopolicy_efficiency = {}
    serviced_cheapest_efficiency = {}
    serviced_cheapestusers_efficiency = {}
    """.format(serviced_nopolicy, serviced_cheapest, serviced_cheapestusers, serviced_nopolicy_shareuse, serviced_cheapest_shareuse, serviced_cheapestusers_shareuse, serviced_nopolicy_shareuse, serviced_cheapest_shareuse, serviced_cheapestusers_shareuse, serviced_nopolicy_efficiency, serviced_cheapest_efficiency, serviced_cheapestusers_efficiency, serviced_nopolicy_arrival, serviced_cheapest_arrival, serviced_cheapestusers_arrival)

    writeDataToFile(savedOutput)
    
    return plt
