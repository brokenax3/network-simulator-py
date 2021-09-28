import numpy as np
import matplotlib.pyplot as plt
from network_simulator.simulator import simulate

def algorithmCompare(init_vars, aplist, usrlist):

    # Dict to store simulation parameters
    _sim_mode = {
        "mode" : "AlgorithmCompare",
        "x-axis" : "Share Budget",
        "title" : "Impact of Energy Sharing Budget on Total Number of Serviced Users",
        "range" : np.arange(0, 1.01, 0.1),
        "total_runs" : 20,
        "change" : "ENERGY_BUDGET",
        "sim_vars" : init_vars,
    }

    _sim_axes = {
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

    # Store axes
    _sim_mode["axes"] = _sim_axes

    simulate(init_vars, aplist, usrlist, _sim_mode)


    return plt



