from multiprocessing import Pool
# from progress.bar import Bar
import tqdm
import numpy as np
import matplotlib.pyplot as plt
from network_simulator.components import simulator
from network_simulator.helpers import writeSimCache, readSimCache

def main():
    return simulator(g_init_vars, g_aplist, g_usrlist)

def algorithmCompare(init_vars, aplist, usrlist):
    global g_init_vars, g_aplist, g_usrlist

    g_init_vars = init_vars
    g_aplist = aplist
    g_usrlist = usrlist


    plot_from_saved = 1
    total_runs = range(20)
    sharebudget = np.arange(0, 1.01, 0.01)
    _output = {}

    _sim_dict_axes = {
        "axes1" : {
            "param" : "Epsilon Greedy",
            "ENERGY_POLICY" : 2,
            "SHARE_ENERGY" : 5,
            "SMART_PARAM" : [0.01, 12]
        },
        "axes2" : {
            "param" : "UCB1",
            "ENERGY_POLICY" : 2,
            "SHARE_ENERGY" : 6,
            "SMART_PARAM" : [2, 12]
        },
        "axes3" : {
            "param" : "Share Evenly",
            "ENERGY_POLICY" : 2,
            "SHARE_ENERGY" : 1,
        },
        "axes4" : {
            "param" : "AP Energy Arrival",
            "ENERGY_POLICY" : 2,
            "SHARE_ENERGY" : 2,
        },
        "axes5" : {
            "param" : "AP Energy Use",
            "ENERGY_POLICY" : 2,
            "SHARE_ENERGY" : 3,
        },
        "axes6" : {
            "param" : "AP Efficiency",
            "ENERGY_POLICY" : 2,
            "SHARE_ENERGY" : 4,
        },
    }

    if plot_from_saved == 0:
        
        # bar = Bar("Algorithms" , max=len(_sim_dict_axes.keys()))
        bar = tqdm.tqdm(total=len(_sim_dict_axes.keys()))

        for axes in _sim_dict_axes.values():
            print("Algorithms " + axes["param"])

            for key in ["ENERGY_POLICY", "SHARE_ENERGY"]:
                init_vars[key] = axes[key]

                if axes.get("SMART_PARAM") != None:
                    init_vars["SMART_PARAM"] = axes.get("SMART_PARAM")

            _avg_serviced_users = []

            for ratio in sharebudget:
                init_vars["ENERGY_BUDGET"] = ratio

                pool = Pool()
                _serviced_users = [pool.apply_async(main, ()) for run in total_runs]

                _avg_serviced_users.append(sum([result.get() for result in _serviced_users]) / len(total_runs))

            _output[axes["param"]] = { "result" : _avg_serviced_users }
            bar.update(1)
            pool.close()
            pool.join()
        bar.close()

        _output["x-axis"] = { 
            "label" : "Share Budget",
            "values" : sharebudget,
        }

        writeSimCache("algorithmCompareShareBudget", _output)
    else:
        _output = readSimCache("algorithmCompareShareBudget")

    plt.figure(1, dpi=600, figsize=[10, 8])

    for key, value in _output.items():
        if value.get("result") != None:
            plt.plot(_output["x-axis"]["values"], value["result"], label=key)

    ax = plt.subplot(111)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                     box.width, box.height * 0.9])

    plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=3, prop={"size": 9})
    plt.xlabel(_output["x-axis"]["label"])
    plt.ylabel("Total Number of Serviced Users")
    plt.title("Impact of Energy Sharing Budget on Total Number of Serviced Users")
    plt.grid()
    plt.ylim(5000, 40000)

    return plt



