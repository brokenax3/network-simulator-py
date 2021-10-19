from multiprocessing import Pool
from bokeh.plotting import figure, show, output_file
from bokeh.palettes import Category20 as palette
import itertools
# from progress.bar import Bar
import tqdm
import numpy as np
import matplotlib.pyplot as plt
from network_simulator.components import simulator
from network_simulator.helpers import writeSimCache, readSimCache

def main():
    return simulator(g_init_vars, g_aplist, g_usrlist)

def panelSizeCompare(init_vars, aplist, usrlist):
    global g_init_vars, g_aplist, g_usrlist

    g_init_vars = init_vars
    g_aplist = aplist
    g_usrlist = usrlist


    plot_from_saved = 1
    total_runs = range(20)
    panelsize = np.arange(5, 20, 1)
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
        
        bar = tqdm.tqdm(desc="Panel Size", total=len(_sim_dict_axes.keys()) * len(panelsize))

        for axes in _sim_dict_axes.values():
            print("Algorithms " + axes["param"])

            for key in ["ENERGY_POLICY", "SHARE_ENERGY"]:
                init_vars[key] = axes[key]

            _avg_serviced_users = []

            for size in panelsize:
                init_vars["PANEL_SIZE"] = size

                pool = Pool(10)
                _serviced_users = [pool.apply_async(main, ()) for run in total_runs]

                _avg_serviced_users.append(sum([result.get() for result in _serviced_users]) / len(total_runs))
                bar.update(1)
                pool.close()
                pool.join()

            _output[axes["param"]] = { "result" : _avg_serviced_users }

        bar.close()

        writeSimCache("panelSize", _output)
    else:
        _output = readSimCache("panelSize")

    output_file("interactive/panelSize.html")

    TOOLTIPS = [
            ("(x, y)", "($x, $y)"),
            ("desc", "$name")
            ]
    
    # Plot colours
    colors = itertools.cycle(palette[20])

    p = figure(width=1200, height=800, x_axis_label='Solar Panel Size', y_axis_label='Total Number of Serviced Users', tooltips=TOOLTIPS, output_backend='svg')

    for key, value in _output.items():

        print(key + " : " + str(sum(value["result"])/len(value["result"])))
        p.line(panelsize, value["result"], legend_label=key, name=key, color=next(colors), line_width=3)

    p.xaxis.axis_label_text_font_size='20px'
    p.xaxis.major_label_text_font_size='20px'
    p.yaxis.axis_label_text_font_size='20px'
    p.yaxis.major_label_text_font_size='20px'
    p.legend.label_text_font_size='18px' 
    p.legend[0].orientation = "vertical"
    legend_ref = p.legend[0] 
    p.add_layout(legend_ref, "right")

    show(p)
    p.toolbar.logo = None
    p.toolbar_location = None

    return p

