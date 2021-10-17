from network_simulator.helpers import readSimCache, writeSimCache

_output = readSimCache("epsilonGreedyMAB")

_newdict = {}

for key, value in _output.items():

    # temp_key = key.replace("AP Efficiency", "AP Energy Efficiency").replace("Share Evenly", "Shared Evenly")
    temp_key = key.replace("0.01", "1%").replace("0.1", "10%").replace("0.3", "30%").replace("0.6", "60%").replace("0.9", "90%")

    _newdict[temp_key] = value

writeSimCache("epsilonGreedyMAB", _newdict)
