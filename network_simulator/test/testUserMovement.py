from multiprocessing import Pool
from bokeh.plotting import figure, show, output_file
from bokeh.palettes import Category20 as palette
import itertools
import numpy as np
import tqdm
from network_simulator.components import simulator
from network_simulator.helpers import writeSimCache, readSimCache

def main():
    return simulator(g_init_vars, g_aplist, g_usrlist)


def userMovementDist(init_vars, aplist, usrlist):
    global g_init_vars, g_aplist, g_usrlist

    g_init_vars = init_vars
    g_aplist = aplist
    g_usrlist = usrlist

    plot_from_saved = 1
    movement_dist = np.arange(1, 16, 1)
    total_runs = range(20)
    _output = {}


    if plot_from_saved == 0:
        _sim_dict_axes = {
            "axes1" : {
                "param" : "No Policy - Epsilon Greedy",
                "ENERGY_POLICY" : 0,
                "SHARE_ENERGY" : 5,
                "SMART_PARAM" : [0.01, 12]
            },
            "axes2" : {
                "param" : "Cheapest Users - Epsilon Greedy",
                "ENERGY_POLICY" : 2,
                "SHARE_ENERGY" : 5,
                "SMART_PARAM" : [0.01, 12]
            },
            "axes3" : {
                "param" : "No Policy - UCB1",
                "ENERGY_POLICY" : 0,
                "SHARE_ENERGY" : 6,
                "SMART_PARAM" : [0.001, 12]
            },
            "axes4" : {
                "param" : "Cheapest Users - UCB1",
                "ENERGY_POLICY" : 2,
                "SHARE_ENERGY" : 6,
                "SMART_PARAM" : [0.001, 12]
            },
            "axes5" : {
                "param" : "No Transmission Policy - Shared Evenly",
                "ENERGY_POLICY" : 0,
                "SHARE_ENERGY" : 1,
            },
            "axes6" : {
                "param" : "Cheapest Users - Shared Evenly",
                "ENERGY_POLICY" : 2,
                "SHARE_ENERGY" : 1,
            },
            "axes7" : {
                "param" : "No Transmission Policy - AP Energy Arrival",
                "ENERGY_POLICY" : 0,
                "SHARE_ENERGY" : 2,
            },
            "axes8" : {
                "param" : "Cheapest Users - AP Energy Arrival",
                "ENERGY_POLICY" : 2,
                "SHARE_ENERGY" : 2,
            },
            "axes9" : {
                "param" : "No Transmission Policy - AP Energy Use",
                "ENERGY_POLICY" : 0,
                "SHARE_ENERGY" : 3,
            },
            "axes10" : {
                "param" : "Cheapest Users - AP Energy Use",
                "ENERGY_POLICY" : 2,
                "SHARE_ENERGY" : 3,
            },
            "axes11" : {
                "param" : "No Transmission Policy - AP Energy Efficiency",
                "ENERGY_POLICY" : 0,
                "SHARE_ENERGY" : 4,
            },
            "axes12" : {
                "param" : "Cheapest Users - AP Energy Efficiency",
                "ENERGY_POLICY" : 2,
                "SHARE_ENERGY" : 4,
            }
        }

        bar = tqdm.tqdm(desc="UserMovementDist", total=len(_sim_dict_axes.keys()) * len(movement_dist))

        for axes in _sim_dict_axes.values():
            
            for param in ["ENERGY_POLICY", "SHARE_ENERGY"]:
                init_vars[param] = axes[param]

            if init_vars["SHARE_ENERGY"] == 6 or init_vars["SHARE_ENERGY"] == 5:
                init_vars["SMART_PARAM"] == axes["SMART_PARAM"]

            _avg_serviced_users = []

            for dist in movement_dist:
                init_vars["DIST_MOVEUSER_MAX"] = dist

                pool = Pool(10)

                _serviced_users = [pool.apply_async(main, ()) for run in total_runs]

                _avg_serviced_users.append(sum([result.get() for result in _serviced_users]) / len(total_runs))
                bar.update(1)
                pool.close()
                pool.join()

            _output[axes["param"]] = { "result" : _avg_serviced_users }
        bar.close()

        writeSimCache("UserMovementDist", _output)
    else:
        _output = readSimCache("UserMovementDist")

    output_file("interactive/usermovement.html")

    TOOLTIPS = [
            ("(x, y)", "($x, $y)"),
            ("desc", "$name")
            ]
    
    # Plot colours
    colors = itertools.cycle(palette[20])

    p = figure(width=700, height=800, x_axis_label='Maximum User Movement Distance', y_axis_label='Total Number of Serviced Users', tooltips=TOOLTIPS)

    for key, value in _output.items():
        print(key + " : " + str(sum(value["result"])/len(value["result"])))
        p.line(movement_dist, value["result"], legend_label=key, name=key, color=next(colors), line_width=3)

    p.legend.location = (20, 100)

    show(p)
    p.toolbar.logo = None
    p.toolbar_location = None

    return p

