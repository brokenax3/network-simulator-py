import matplotlib.pyplot as plt
import numpy as np
from progress.bar import Bar
from network_simulator.components import simulator
from network_simulator.helpers import writeDataToFile 

def shareBudget(init_vars, aplist, usrlist):

    total_runs = np.arange(30)
    sharebudget = np.arange(0, 1.01, 0.01)

    """ No Transmission Policy (Energy Efficiency)
    """
    bar = Bar('Energy Share Budget (No Transmission Policy)(Energy Efficiency)', max=len(sharebudget))

    avg_serviced_sharebudget_no_trans_p = []

    # Cheapest Users
    init_vars["ENERGY_POLICY"] = 2
    # Efficiency
    init_vars["SHARE_ENERGY"] = 4
    init_vars["LOAD_BALANCE"] = 0
    init_vars["USR_LIMIT"] = 30

    for ratio in sharebudget:
        init_vars["ENERGY_BUDGET"] = ratio
        serviced_sharebudget_no_trans_p = []

        for run in total_runs:
            serviced_sharebudget_no_trans_p.append(simulator(init_vars, aplist, usrlist))

        avg_serviced_sharebudget_no_trans_p.append(sum(serviced_sharebudget_no_trans_p) / len(total_runs))
        bar.next()
    bar.finish()

    """ Cheapest Users (Energy Efficiency)

    """
    bar = Bar('Energy Share Budget (Cheapest Users)(Energy Efficiency)', max=len(sharebudget))

    avg_serviced_sharebudget_cheapest_users = []
    
    # Cheapest Users
    init_vars["ENERGY_POLICY"] = 2
    # Efficiency
    init_vars["SHARE_ENERGY"] = 4
    init_vars["LOAD_BALANCE"] = 0
    init_vars["USR_LIMIT"] = 30

    for ratio in sharebudget:
        init_vars["ENERGY_BUDGET"] = ratio
        serviced_sharebudget_cheapest_users = []

        for run in total_runs:
            serviced_sharebudget_cheapest_users.append(simulator(init_vars, aplist, usrlist))

        avg_serviced_sharebudget_cheapest_users.append(sum(serviced_sharebudget_cheapest_users) / len(total_runs))
        bar.next()
    bar.finish()

    print('Total Number of Serviced Users (Share Budget)(No Transmission Policy): {}'.format(avg_serviced_sharebudget_no_trans_p))
    # print('Total Number of Serviced Users (Share Budget)(Cheapest User): {}'.format(avg_serviced_sharebudget_cheapest_user))
    print('Total Number of Serviced Users (Share Budget)(Cheapest Users): {}'.format(avg_serviced_sharebudget_cheapest_users))

    plot = plt.figure(1)
    plt.plot(sharebudget, avg_serviced_sharebudget_no_trans_p, label='No Transmission Policy')
    # plt.plot(sharebudget, avg_serviced_sharebudget_cheapest_user, label='Cheapest User')
    plt.plot(sharebudget, avg_serviced_sharebudget_cheapest_users, label='Cheapest Users')

    plt.legend()
    plt.xlabel('Share Budget')
    plt.ylabel('Total Number of Serviced Users')
    plt.title('Total Number of Serviced Users against Share Budget')

    savedOutput = """
    range = {}
    avg_serviced_sharebudget_no_trans_p = {}
    avg_serviced_sharebudget_cheapest_users = {}
    """.format([sharebudget[0], sharebudget[-1]], avg_serviced_sharebudget_no_trans_p, avg_serviced_sharebudget_cheapest_users)

    writeDataToFile(savedOutput, 'saved-sharebudget.txt')
    
    return plt
