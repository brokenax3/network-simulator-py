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


def dataframeSize(init_vars, aplist, usrlist):
    global g_init_vars, g_aplist, g_usrlist

    g_init_vars = init_vars
    g_aplist = aplist
    g_usrlist = usrlist

    plot_from_saved = 0
    dataframe_size = np.arange(1, 40, 5)
    total_runs = range(20)
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
            "SMART_PARAM" : [0.01, 12]
        },
        "axes4" : {
            "param" : "Cheapest Users - UCB1",
            "ENERGY_POLICY" : 2,
            "SHARE_ENERGY" : 6,
            "SMART_PARAM" : [0.01, 12]
        }
    }

    if plot_from_saved == 0:

        bar = tqdm.tqdm(desc="Dataframe Size", total=len(_sim_dict_axes.keys()) * len(dataframe_size))

        for axes in _sim_dict_axes.values():
            
            for param in ["ENERGY_POLICY", "SHARE_ENERGY"]:
                init_vars[param] = axes[param]

            _avg_serviced_users = []

            for size in dataframe_size:
                if axes["SHARE_ENERGY"] == 5:
                    init_vars["SMART_PARAM"] = [0.01, size]
                else:
                    init_vars["SMART_PARAM"] = [0.01, size]

                pool = Pool(10)

                _serviced_users = [pool.apply_async(main, ()) for run in total_runs]

                _avg_serviced_users.append(sum([result.get() for result in _serviced_users]) / len(total_runs))
                bar.update(1)
                pool.close()
                pool.join()

            _output[axes["param"]] = { "result" : _avg_serviced_users }
        bar.close()

        writeSimCache("DataframeSize", _output)
    else:
        _output = readSimCache("DataframeSize")

    output_file("interactive/dataframesize.html")

    TOOLTIPS = [
            ("(x, y)", "($x, $y)"),
            ("desc", "$name")
            ]
    
    # Plot colours
    colors = itertools.cycle(palette[20])

    p = figure(width=700, height=800, x_axis_label='Dataframe Size', y_axis_label='Total Number of Serviced Users', tooltips=TOOLTIPS)

    for key, value in _output.items():
        print(key + " : " + str(sum(value["result"])/len(value["result"])))
        p.line(dataframe_size, value["result"], legend_label=key, name=key, color=next(colors), line_width=3)

    p.legend.location = (20, 100)

    show(p)
    p.toolbar.logo = None
    p.toolbar_location = None

    return p

