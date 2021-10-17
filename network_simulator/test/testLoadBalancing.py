from multiprocessing import Pool
from bokeh.plotting import figure, show, output_file
from bokeh.palettes import Category20 as palette
import itertools
import tqdm
import numpy as np
from network_simulator.components import simulator
from network_simulator.helpers import writeSimCache, readSimCache

def main():
    return simulator(g_init_vars, g_aplist, g_usrlist)

def loadBalancing(init_vars, aplist, usrlist):
    global g_init_vars, g_aplist, g_usrlist

    g_init_vars = init_vars
    g_aplist = aplist
    g_usrlist = usrlist
    
    plot_from_saved = 1
    total_runs = range(20)
    usr_limit = np.arange(30, 120, 5)
    _output = {}

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

    if plot_from_saved == 0:

        bar = tqdm.tqdm(desc="Load Balancing", total=len(_sim_dict_axes.keys()) * len(usr_limit))

        init_vars["LOAD_BALANCE"] = 0

        # Run once for no Load Balancing
        for axes in _sim_dict_axes.values():

            for param in ["ENERGY_POLICY", "SHARE_ENERGY"]:
                init_vars[param] = axes[param]

            if init_vars["SHARE_ENERGY"] == 6 or init_vars["SHARE_ENERGY"] == 5:
                init_vars["SMART_PARAM"] == axes["SMART_PARAM"]

            _avg_serviced_users = []

            pool = Pool(10)

            _serviced_users = [pool.apply_async(main, ()) for run in total_runs]

            _avg_serviced_users = sum([result.get() for result in _serviced_users]) / len(total_runs)
            _output[axes["param"] + " No Balancing"] = { "result" : [_avg_serviced_users]*len(usr_limit) }
        bar.update(1)
        init_vars["LOAD_BALANCE"] = 1

        for axes in _sim_dict_axes.values():
            
            for param in ["ENERGY_POLICY", "SHARE_ENERGY"]:
                init_vars[param] = axes[param]

            _avg_serviced_users = []

            for num in usr_limit:
                init_vars["USR_LIMIT"] = num

                pool = Pool(10)

                _serviced_users = [pool.apply_async(main, ()) for run in total_runs]

                _avg_serviced_users.append(sum([result.get() for result in _serviced_users]) / len(total_runs))

            _output[axes["param"]] = { "result" : _avg_serviced_users }
            bar.update(1)
        bar.close()
        writeSimCache("LoadBalanceM", _output)
    else:
        _output = readSimCache("LoadBalanceM")

    output_file("interactive/loadbalancing.html")

    TOOLTIPS = [
            ("(x, y)", "($x, $y)"),
            ("desc", "$name")
            ]
    
    # Plot colours
    colors = itertools.cycle(palette[12])

    p = figure(width=1200, height=800, x_axis_label='Total Number of Users', y_axis_label='Total Number of Serviced Users', tooltips=TOOLTIPS)
    count = 0

    for key, value in _output.items():

        count += 1

        print(key + " : " + str(sum(value["result"])/len(value["result"])))
        if count >= 13:
            p.line(usr_limit, value["result"], legend_label=key, name=key, color=next(colors), line_width=3, line_dash="dashed")
        else:
            p.line(usr_limit, value["result"], legend_label=key, name=key, color=next(colors), line_width=3)

    p.legend[0].orientation = "vertical"
    legend_ref = p.legend[0] 
    # p.legend[0] = None

    p.add_layout(legend_ref, "right")

    show(p)
    p.toolbar.logo = None
    p.toolbar_location = None

    return p
