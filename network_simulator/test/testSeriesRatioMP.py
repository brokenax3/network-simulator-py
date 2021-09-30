from multiprocessing import Pool
import matplotlib.pyplot as plt
import numpy as np
import tqdm
# from progress.bar import Bar
from network_simulator.components import simulator
from network_simulator.helpers import writeSimCache, readSimCache, genDescendUnitArray

def main():
    return simulator(g_init_vars, g_aplist, g_usrlist)


def seriesRatioMP(init_vars, aplist, usrlist):
    global g_init_vars, g_aplist, g_usrlist

    g_init_vars = init_vars
    g_aplist = aplist
    g_usrlist = usrlist

    plot_from_saved = 0
    geometric_ratio = np.arange(0.01, 0.99, 0.01)
    total_runs = range(20)
    _output = {}


    if plot_from_saved == 0:
        _sim_dict_axes = {
            "axes1" : {
                "param" : "No Transmission Policy - Share Evenly",
                "ENERGY_POLICY" : 0,
                "SHARE_ENERGY" : 1,
            },
            "axes2" : {
                "param" : "Cheapest Users - Share Evenly",
                "ENERGY_POLICY" : 2,
                "SHARE_ENERGY" : 1,
            },
            "axes3" : {
                "param" : "No Transmission Policy - AP Energy Arrival",
                "ENERGY_POLICY" : 0,
                "SHARE_ENERGY" : 2,
            },
            "axes4" : {
                "param" : "Cheapest Users - AP Energy Arrival",
                "ENERGY_POLICY" : 2,
                "SHARE_ENERGY" : 2,
            },
            "axes5" : {
                "param" : "No Transmission Policy - AP Energy Use",
                "ENERGY_POLICY" : 0,
                "SHARE_ENERGY" : 3,
            },
            "axes6" : {
                "param" : "Cheapest Users - AP Energy Use",
                "ENERGY_POLICY" : 2,
                "SHARE_ENERGY" : 3,
            },
            "axes7" : {
                "param" : "No Transmission Policy - AP Efficiency",
                "ENERGY_POLICY" : 0,
                "SHARE_ENERGY" : 4,
            },
            "axes8" : {
                "param" : "Cheapest Users - AP Efficiency",
                "ENERGY_POLICY" : 2,
                "SHARE_ENERGY" : 4,
            }
        }
        bar = tqdm.tqdm(total=len(_sim_dict_axes.keys()) * len(geometric_ratio))

        # bar = Bar("Geometric Ratio MP" , max=len(_sim_dict_axes.values()))
        for axes in _sim_dict_axes.values():
            
            for param in ["ENERGY_POLICY", "SHARE_ENERGY"]:
                init_vars[param] = axes[param]

            _avg_serviced_users = []

            for ratio in geometric_ratio:
                init_vars["SERIES_RATIO"] = ratio
                init_vars["descendunit_arr"] = genDescendUnitArray(init_vars["AP_TOTAL"], 1, init_vars["SERIES_RATIO"])

                pool = Pool(10)

                _serviced_users = [pool.apply_async(main, ()) for run in total_runs]

                _avg_serviced_users.append(sum([result.get() for result in _serviced_users]) / len(total_runs))
                bar.update(1)
                pool.close()
                pool.join()

            _output[axes["param"]] = { "result" : _avg_serviced_users }
        bar.close()

        writeSimCache("GeometricRatioMP", _output)
    else:
        _output = readSimCache("GeometricRatioMP")


    plt.figure(1, dpi=600, figsize=[10, 8])
    # print(_output.items())
    for key, value in _output.items():

        plt.plot(geometric_ratio, value["result"], label=key)

    ax = plt.subplot(111)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                     box.width, box.height * 0.9])

    plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=3, prop={"size": 9})
    plt.xlabel('Geometric Ratio')
    plt.ylabel('Total Number of Serviced Users')
    plt.title('Impact of Geometric Ratio of Energy Allocation on Total Number of Serviced Users')
    plt.grid()
    # plt.ylim(5000, 40000)

    # plt.show()

    return plt

