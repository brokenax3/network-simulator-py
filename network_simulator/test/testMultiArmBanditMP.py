from multiprocessing import Pool
from bokeh.plotting import figure, show, output_file
from bokeh.palettes import Category10 as palette
import itertools
# from progress.bar import Bar
# import matplotlib.pyplot as plt
import numpy as np
# from progress.bar import Bar
import tqdm
from network_simulator.components import simulator
from network_simulator.helpers import writeSimCache, readSimCache

def main():
    return simulator(g_init_vars, g_aplist, g_usrlist)


def mabMP(init_vars, aplist, usrlist):
    global g_init_vars, g_aplist, g_usrlist

    g_init_vars = init_vars
    g_aplist = aplist
    g_usrlist = usrlist

    plot_from_saved = 1
    total_runs = range(20)
    epsilons = np.arange(0.01, 0.5, 0.2)
    _output = {}

    if plot_from_saved == 0:
        _sim_dict_axes = {
            "axes1" : {
                "param" : "Epsilon Greedy - Budget @ 0.01",
                "ENERGY_BUDGET" : 0.01,
                "ENERGY_POLICY" : 2,
            },
             "axes2" : {
                "param" : "Epsilon Greedy - Budget @ 0.1",
                "ENERGY_BUDGET" : 0.1,
                "ENERGY_POLICY" : 2,
            },
            "axes3" : {
                "param" : "Epsilon Greedy - Budget @ 0.3",
                "ENERGY_BUDGET" : 0.3,
                "ENERGY_POLICY" : 2,
            },
            "axes4" : {
                "param" : "Epsilon Greedy - Budget @ 0.6",
                "ENERGY_BUDGET" : 0.6,
                "ENERGY_POLICY" : 2,
            },
            "axes5" : {
                "param" : "Epsilon Greedy - Budget @ 0.9",
                "ENERGY_BUDGET" : 0.9,
                "ENERGY_POLICY" : 2,
            },
        }

        init_vars["SHARE_ENERGY"] = 5
        bar = tqdm.tqdm(total=len(_sim_dict_axes.keys()) * len(epsilons))

        # bar = Bar("MultiArmBandit Epsilon Greedy" , max=len(epsilons))
        for axes in _sim_dict_axes.values():
            
            for param in ["ENERGY_POLICY", "ENERGY_BUDGET"]:
                init_vars[param] = axes[param]

            _avg_serviced_users = []

            for epsilon in epsilons:
                init_vars["SMART_PARAM"] = [epsilon, 12]

                pool = Pool(10)

                _serviced_users = [pool.apply_async(main, ()) for run in total_runs]

                _avg_serviced_users.append(sum([result.get() for result in _serviced_users]) / len(total_runs))
                bar.update(1)
                pool.close()
                pool.join()

            _output[axes["param"]] = { "result" : _avg_serviced_users }
        bar.close()

        writeSimCache("epsilonGreedyMAB", _output)
    else:
        _output = readSimCache("epsilonGreedyMAB")

    output_file("interactive/epsilonCompare.html")

    TOOLTIPS = [
            ("(x, y)", "($x, $y)"),
            ("desc", "$name")
            ]
    
    # Plot colours
    colors = itertools.cycle(palette[8])

    p = figure(width=1200, height=800, x_axis_label='Epsilon', y_axis_label='Total Number of Serviced Users', tooltips=TOOLTIPS, output_backend='svg')

    for key, value in _output.items():
        print(key + " : " + str(sum(value["result"])/len(value["result"])))

        p.line(epsilons, value["result"], legend_label=key, name=key, color=next(colors), line_width=3)

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
