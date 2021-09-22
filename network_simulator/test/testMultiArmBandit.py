import matplotlib.pyplot as plt
import numpy as np
from progress.bar import Bar
from network_simulator.components import simulator
from network_simulator.helpers import writeSimCache, readSimCache

def mab(init_vars, aplist, usrlist):

    total_runs = range(10)
    init_vars["SHARE_ENERGY"] = 6
    # init_vars["SMART_PARAM"] = [0.05, 2]
    ucbscale = np.arange(0.5, 3, 0.5)
    # epsilons = np.arange(0.01, 0.5, 0.01)
    avg_serviced_user_mab = []

    # bar = Bar("MAB epsilon ", max=len(epsilons))
    # for epsilon in epsilons:
    #     init_vars["SMART_PARAM"] = [epsilon, 12]

    #     serviced_user_mab = []

    #     for run in total_runs:
    #         serviced_user_mab.append(simulator(init_vars, aplist, usrlist))

    #     avg_serviced_user_mab.append(sum(serviced_user_mab)/ len(total_runs))

    #     bar.next()
    # bar.finish()

    # plt.figure(1)
    # plt.plot(epsilons, avg_serviced_user_mab)
    # plt.show()

    bar = Bar("UCB1", max=len(total_runs))
    # init_vars["SMART_PARAM"] = [0, 2]
    init_vars["ENERGY_BUDGET"] = 0.03

    serviced_user_mab = []
    for scale in ucbscale:
        init_vars["SMART_PARAM"] = [scale, 2]

        for run in total_runs:
            serviced_user_mab.append(simulator(init_vars, aplist, usrlist))

        avg_serviced_user_mab.append(sum(serviced_user_mab)/ len(total_runs))
        bar.next()
    bar.finish()

    writeSimCache("UCB MAB", avg_serviced_user_mab)


    plt.figure(1)
    plt.plot(ucbscale, avg_serviced_user_mab)
    plt.show()
    # print(simulator(init_vars, aplist, usrlist))

    return plt
