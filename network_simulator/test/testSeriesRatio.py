import matplotlib.pyplot as plt
import numpy as np
from progress.bar import Bar
from network_simulator.components import simulator
from network_simulator.helpers import writeSimCache, readSimCache, genDescendUnitArray

def seriesRatio(init_vars, aplist, usrlist):

    plot_from_saved = 1
    _sim_dict_axes = {
        "axes1" : {
            "param" : "No Transmission Policy - Shared Evenly",
            "ENERGY_POLICY" : 0,
            "SHARE_ENERGY" : 1,
        },
        "axes2" : {
            "param" : "Cheapest Users - Shared Evenly",
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
            "param" : "No Transmission Policy - AP Energy Efficiency",
            "ENERGY_POLICY" : 0,
            "SHARE_ENERGY" : 4,
        },
        "axes8" : {
            "param" : "Cheapest Users - AP Energy Efficiency",
            "ENERGY_POLICY" : 2,
            "SHARE_ENERGY" : 4,
        }
    }
    total_runs = np.arange(20)
    geometric_ratio = np.arange(0.01, 0.99, 0.01)
    init_vars["ENERGY_BUDGET"] = 0.03

    if plot_from_saved == 0:
        for axes in _sim_dict_axes.values():
            
            desc = "Energy Share Geometric Series Ratio " + axes["param"]

            bar = Bar(desc, max=len(geometric_ratio))

            avg_serviced = []

            for param in ["ENERGY_POLICY", "SHARE_ENERGY"]:
                init_vars[param] = axes[param]

            for ratio in geometric_ratio:
                init_vars["SERIES_RATIO"] = ratio
                init_vars["descendunit_arr"] = genDescendUnitArray(init_vars["AP_TOTAL"], 1, init_vars["SERIES_RATIO"])
            
                serviced_users = []

                for run in total_runs:
                    serviced_users.append(simulator(init_vars, aplist, usrlist))

                avg_serviced.append(sum(serviced_users) / len(total_runs))

                bar.next()

            bar.finish()
            print("\nTotal Serviced Users " + axes["param"] + "{}".format(avg_serviced))
            writeSimCache("GeometricRatio" + axes["param"].replace(" ",""), avg_serviced)

    plt.figure(1, dpi=600, figsize=[10, 8])
    for axes in _sim_dict_axes.values():
        avg_serviced = readSimCache("GeometricRatio" + axes["param"].replace(" ",""))
        plt.plot(geometric_ratio, avg_serviced, label=axes["param"])

    ax = plt.subplot(111)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                     box.width, box.height * 0.9])

    plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=3, prop={"size": 9})
    plt.xlabel('Geometric Ratio')
    plt.ylabel('Total Number of Serviced Users')
    plt.title('Impact of Geometric Ratio for Energy Sharing on Total Number of Serviced Users')
    plt.grid()

    return plt
