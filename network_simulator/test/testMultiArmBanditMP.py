from multiprocessing import Pool
import matplotlib.pyplot as plt
import numpy as np
from progress.bar import Bar
from network_simulator.components import simulator
from network_simulator.helpers import writeSimCache, readSimCache

def main():
    return simulator(g_init_vars, g_aplist, g_usrlist)


def mabMP(init_vars, aplist, usrlist):
    global g_init_vars, g_aplist, g_usrlist

    g_init_vars = init_vars
    g_aplist = aplist
    g_usrlist = usrlist

    plot_from_saved = 0
    total_runs = range(20)
    epsilons = np.arange(0.01, 0.5, 0.01)
    _output = {}

    if plot_from_saved == 0:
        _sim_dict_axes = {
            "axes1" : {
                "param" : "Epsilon Greedy - Budget @ 0.03",
                "ENERGY_BUDGET" : 0.03,
                "ENERGY_POLICY" : 2,
            },
            "axes2" : {
                "param" : "Epsilon Greedy - Budget @ 0.2",
                "ENERGY_BUDGET" : 0.2,
                "ENERGY_POLICY" : 2,
            },
            "axes3" : {
                "param" : "Epsilon Greedy - Budget @ 0.6",
                "ENERGY_BUDGET" : 0.6,
                "ENERGY_POLICY" : 2,
            },
        }

        init_vars["SHARE_ENERGY"] = 5

        bar = Bar("MultiArmBandit Epsilon Greedy" , max=len(epsilons))
        for axes in _sim_dict_axes.values():
            
            for param in ["ENERGY_POLICY", "ENERGY_BUDGET"]:
                init_vars[param] = axes[param]

            _avg_serviced_users = []

            for epsilon in epsilons:
                init_vars["SMART_PARAM"] = [epsilon, 12]

                pool = Pool(10)

                _serviced_users = [pool.apply_async(main, ()) for run in total_runs]

                _avg_serviced_users.append(sum([result.get() for result in _serviced_users]) / len(total_runs))
            bar.next()

            _output[axes["param"]] = { "result" : _avg_serviced_users }
        bar.finish()

        writeSimCache("epsilonGreedyMAB", _output)
    else:
        _output = readSimCache("epsilonGreedyMAB")

    plt.figure(1, dpi=600, figsize=[10, 8])
    # print(_output.items())
    for key, value in _output.items():

        plt.plot(epsilons, value["result"], label=key)

    ax = plt.subplot(111)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                     box.width, box.height * 0.9])

    plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=3, prop={"size": 9})
    plt.xlabel('Epsilon')
    plt.ylabel('Total Number of Serviced Users')
    plt.title('Impact of Epsilon for Epsilon Greedy Multi Arm Bandit on Total Number of Serviced Users')
    plt.grid()
    plt.ylim(5000, 40000)

    return plt
