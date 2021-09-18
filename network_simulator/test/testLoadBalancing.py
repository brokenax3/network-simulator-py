from progress.bar import Bar
import matplotlib.pyplot as plt
from network_simulator.components import simulator

def loadBalancing(init_vars, aplist, usrlist):

    total_runs = range(10)
    usr_limit = range(10, 50, 5)

    bar = Bar('Load Balancing', max=len(usr_limit))

    avg_serviced_loadbalance = []

    init_vars["LOAD_BALANCE"] = 1
    for usrlimit in usr_limit:
        init_vars["USR_LIMIT"] = usrlimit
        serviced_loadbalance = []

        for run in total_runs:
            serviced_loadbalance.append(simulator(init_vars, aplist, usrlist))

        avg_serviced_loadbalance.append(sum(serviced_loadbalance) / len(total_runs))
        bar.next()
    bar.finish()

    print("Toal Number of Serviced Users (Load Balanced): {}".format(avg_serviced_loadbalance))

    plot = plt.figure(1)
    plt.plot(usr_limit, avg_serviced_loadbalance, label="Load Balanced")

    plt.legend()
    plt.xlabel('AP User Limit')
    plt.ylabel('Total Number of Serviced Users')
    plt.title('Total Number of Serviced Users against AP User Limit')


    return plt
