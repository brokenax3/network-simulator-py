from multiprocessing import Pool
from bokeh.io import export_png
from bokeh.plotting import figure, show, output_file
from bokeh.palettes import Category10 as palette
import itertools
# import matplotlib.pyplot as plt
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

    plot_from_saved = 1
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

    # output_file("interactive/geometricratio.html")

    TOOLTIPS = [
            ("(x, y)", "($x, $y)"),
            ("desc", "$name")
            ]
    
    # Plot colours
    colors = itertools.cycle(palette[8])

    p = figure(width=700, height=800, x_axis_label='Geometric Ratio', y_axis_label='Total Number of Serviced Users', tooltips=TOOLTIPS)

    for key, value in _output.items():
        print(key + " : " + str(sum(value["result"])/len(value["result"])))
        p.line(geometric_ratio, value["result"], legend_label=key, name=key, color=next(colors), line_width=3)

    p.legend.location = (20, 100)
    # export_png(p, filename="test.png")

    # show(p)
    p.toolbar.logo = None
    p.toolbar_location = None

    return p

