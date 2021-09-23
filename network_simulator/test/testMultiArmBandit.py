from multiprocessing import Pool
import matplotlib.pyplot as plt
import numpy as np
from progress.bar import Bar
from network_simulator.components import simulator
from network_simulator.helpers import writeSimCache, readSimCache

def main():
    return simulator(g_init_vars, g_aplist, g_usrlist)

def mab(init_vars, aplist, usrlist):
    global g_init_vars, g_aplist, g_usrlist

    g_init_vars = init_vars
    g_aplist = aplist
    g_usrlist = usrlist
    
    plot_from_saved = 0
    total_runs = range(20)


    init_vars["SHARE_ENERGY"] = 6
    init_vars["SMART_PARAM"] = [0.5, 2]
    # ucbscale = np.arange(0.5, 3, 0.5)
    # epsilons = np.arange(0.01, 0.5, 0.01)
    # avg_serviced_user_mab = []

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
    # if plot_from_saved == 0:

    #     bar = Bar("UCB1", max=len(total_runs))
    #     # init_vars["SMART_PARAM"] = [0, 2]
    #     init_vars["ENERGY_BUDGET"] = 0.03

    #     _avg_serviced_users = []

    #     # serviced_user_mab = []
    #     for scale in ucbscale:
    #         init_vars["SMART_PARAM"] = [scale, 2]
    #         pool = Pool(10)
    #         _serviced_users = [pool.apply_async(main, ()) for run in total_runs]


    #         _avg_serviced_users.append(sum([result.get() for result in _serviced_users]) / len(total_runs))
    #         bar.next()
    #     bar.finish()

    #     # writeSimCache("UCB MAB - Scale(0.5,3,0.5)", _avg_serviced_users)
    # else:
    #     _avg_serviced_users = readSimCache("UCB MAB - Scale(0.5,3,0.5)")
    #     print(_avg_serviced_users)
    #     print(ucbscale)
    print(main())


    # plt.figure(1)
    # plt.plot(ucbscale, _avg_serviced_users)
    # plt.show()
    # print(simulator(init_vars, aplist, usrlist))

    return plt
