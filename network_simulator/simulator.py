from multiprocessing import Pool
import os

from network_simulator.components import simulator
from network_simulator.helpers import writeSimCache, readSimCache

def sim_exist(filename):
    """ Check if simulation with the same parameters have been ran before.

    """

    if os.path.exists(filename):
        run_again = input("Remove previous data and start again? (y/n)")

        if run_again.lower() == "y":
            return 0
        else:
            return 1
    else:
        return 0

""" Cache File Format
"axes1" : {
    "param" : "Epsilon Greedy",
    "result" : data,
    "last_var" : run_param,
}
"""
def readPartCache(filename, mode):
    """ Read Cache from previous simulation(s) that was ran partially.

    """

    partrun = readSimCache(filename + "-part")

    # Find the last saved simulation run
    lastkey = list(partrun.keys())[-1:]
    last_var = partrun[lastkey]["last_var"]
    last_param = partrun[lastkey]["param"]


    return last_param, last_var, partrun

def multirun():
    return simulator(g_init_vars, g_aplist, g_usrlist)


def simulate(init_vars, aplist, usrlist, mode):
    global g_init_vars, g_aplist, g_usrlist

    g_init_vars = init_vars
    g_aplist = aplist
    g_usrlist = usrlist

    fpath = mode["mode"]
    # if sim_exist(fpath):
    #     readPartCache(fpath)
    testcache = {
        "axes1" : {
            "param" : "Epsilon Greedy",
            "result" : [0, 1, 2, 3],
            "last_var" : 0.05,
        },
        "axes2" : {
            "param" : "UCB",
            "result" : [0, 1, 2, 3],
            "last_var" : 0.05,
        },
        "axes3" : {
            "param" : "Share Evenly",
            "result" : [0, 1, 2, 3],
            "last_var" : 0.05,
        }
    }
    writeSimCache(fpath + "-part", testcache)
    last_param, last_var, partrun = readPartCache(fpath, mode)

    variables = mode["range"]
    total_runs = range(mode["total_runs"])
    counter = 1
    simcache = {}

    try:
        for axes in mode["axes"].values():
            if axes["param"] == last_param:
                cont = 1

            if cont == 1:
                for key in ["ENERGY_POLICY", "SHARE_ENERGY"]:
                    init_vars[key] = axes[key]
                    if axes.get("SMART_PARAM") != None:
                        init_vars["SMART_PARAM"] = axes.get("SMART_PARAM")

                _avg_serviced_users = []

                for value in variables:
                    init_vars[mode["change"]] = value

                    pool = Pool(10)

                    _serviced_users = [pool.apply_async(multirun, ()) for run in total_runs]
                    _avg_serviced_users.append(sum([result.get() for result in _serviced_users]) / len(total_runs))

                dictstr = "axes" + str(counter)

                simcache[dictstr]["param"] = axes["param"]  
                simcache[dictstr]["result"] = _avg_serviced_users

    except KeyboardInterrupt:
        # Save cache and exit
        dictstr = "axes" + str(counter)

        simcache[dictstr]["param"] = axes["param"]  
        simcache[dictstr]["result"] = _avg_serviced_users



        exit()


