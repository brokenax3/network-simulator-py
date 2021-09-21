import matplotlib.pyplot as plt
import numpy as np
from progress.bar import Bar
from network_simulator.components import simulator
from network_simulator.helpers import writeSimCache, readSimCache

def mab(init_vars, aplist, usrlist):
    
    init_vars["SMART_PARAM"] = [0.05, 10]
