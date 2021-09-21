import matplotlib.pyplot as plt
import numpy as np
from progress.bar import Bar
from network_simulator.components import simulator
from network_simulator.helpers import writeSimCache, readSimCache

def mab(init_vars, aplist, usrlist):

    total_runs = range(20)
    init_vars["SHARE_ENERGY"] = 5
    init_vars["SMART_PARAM"] = [0.05, 2]
    epsilons = np.arange(0.01, 0.5, 0.01)
    avg_serviced_user_mab = []

    bar = Bar("MAB epsilon ", max=len(epsilons))
    for epsilon in epsilons:
        init_vars["SMART_PARAM"] = [epsilon, 12]

        serviced_user_mab = []

        for run in total_runs:
            serviced_user_mab.append(simulator(init_vars, aplist, usrlist))

        avg_serviced_user_mab.append(sum(serviced_user_mab)/ len(total_runs))

        bar.next()
    bar.finish()

    plt.figure(1)
    plt.plot(epsilons, avg_serviced_user_mab)
    plt.show()
    # simulator(init_vars, aplist, usrlist)

    return plt
