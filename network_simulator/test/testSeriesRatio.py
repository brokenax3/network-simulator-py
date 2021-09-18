import matplotlib.pyplot as plt
import numpy as np
from progress.bar import Bar
from network_simulator.components import simulator


def seriesRatio(init_vars, aplist, usrlist):

    total_runs = np.arange(20)
    seriesratio = np.arange(0.1, 0.9, 0.1)

    bar = Bar('Geometry Series Ratio', max=len(seriesratio))

    avg_serviced_seriesratio = []

    init_vars["ENERGY_POLICY"] = 2
    init_vars["SHARE_ENERGY"] = 4
    init_vars["LOAD_BALANCE"] = 1
    init_vars["USR_LIMIT"] = 50

    for ratio in seriesratio:
        init_vars["SERIES_RATIO"] = ratio
        serviced_seriesratio = []

        for run in total_runs:
            serviced_seriesratio.append(simulator(init_vars, aplist, usrlist))

        avg_serviced_seriesratio.append(sum(serviced_seriesratio) / len(total_runs))
        bar.next()
    bar.finish()

    print('Total Number of Serviced Users (Series Ratio): {}'.format(avg_serviced_seriesratio))

    plot = plt.figure(1)
    plt.plot(seriesratio, avg_serviced_seriesratio, label='Series Ratio')

    plt.legend()
    plt.xlabel('Geometry Series Ratio')
    plt.ylabel('Total Number of Serviced Users')
    plt.title('Total Number of Serviced Users against Series Ratio')

    return plt
