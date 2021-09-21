import numpy as np
from operator import itemgetter
from pathlib import Path
from network_simulator.helpers import writeSimCache, readSimCache

""" Epsilon Greedy Algorithm

score = [[apid, total_serviced_users] ... ] 
score_history = [[apid, { targeted_apid1 : score_ap1, 
                        targeted_apid2 : score_ap2
                            } ] ...]]
action_history = [[apid, targeted_ap] ... ]

returns a list of actions
"""
def epsilonGreedy(score_ap, epsilon, length):

    explore = np.random.binomial(1, epsilon)
    
    # Unpack values
    _apid = score_ap[0]
    _score = [[key, value] for key, value in score_ap[1].items()]

    if explore == 1 or _score == []:

        # Create a list of potential candidates (Cannot be itself)
        _choices = list(range(length))
        _choices.remove(_apid)

        # Pick a candidate among the list
        target_ap = np.random.choice(_choices, 1)
    else:
        # Point to the best scoring Access Point
        best_score = sorted(_score, key=itemgetter(1), reverse=True)
        target_ap = best_score[0]

    return target_ap[0]


# def ucb1(score_ap):
#     o

def multiArmBandit(aplist, epsilon, dataframe):

    _mab_score_cache = "test/mabscorehistory"
    _mab_action_cache = "test/mabactionhistory"

    _list_target_ap = []

    if Path("sim_cache/test/mabscorehistory.data").exists() and Path("sim_cache/test/mabactionhistory.data").exists():
        score_history = readSimCache(_mab_score_cache)
        action_history = readSimCache(_mab_action_cache)

        inc_serviced_users = [ap.data_serviced_users[-dataframe:] for ap in aplist]
        # print(inc_serviced_users)
        # print(score_history)

        for history in action_history:

            # Get score from increase of serviced users due to my choice
            _my_score = inc_serviced_users[history[1]]
            # print(history)
            # print(_my_score)

            # Update score history with new data
            score_history[history[0]][1][history[1]] += sum(_my_score)
            _my_score_history = score_history[history[0]]

            _list_target_ap.append([history[0], epsilonGreedy(_my_score_history, epsilon, len(aplist))])
    else:
        # Create empty score history
        score_history = []

        for ap in aplist:
            # Generate an list of apids without the current one
            _empty_scores = list(range(len(aplist)))
            _empty_scores.remove(ap.id)

            _list_empty_scores = {}
            for _empty_score in _empty_scores:
                _list_empty_scores[_empty_score] = 0

            score_history.append([ap.id, _list_empty_scores])

            _list_target_ap.append([ap.id, epsilonGreedy([ap.id, {}], epsilon, len(aplist))])

    # Cache Scores and Action
    writeSimCache(_mab_score_cache, score_history)
    writeSimCache(_mab_action_cache, _list_target_ap)

    return _list_target_ap


# if __name__ == "__main__":

#     print("Multiarm Bandit")

#     for run in range(100):
#         target = epsilonGreedy(0, [0, 1, 2, 3], 0.15)
#         print(target)
