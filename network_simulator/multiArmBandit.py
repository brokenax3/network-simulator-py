import numpy as np
from operator import itemgetter
from statistics import mean
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
def epsilonGreedy(history, epsilon):
    length = len(history.keys())
    _list_target_ap = []
    # print("running ep greedy")
    # print(history)

    for _apid in history.keys():

        explore = np.random.binomial(1, epsilon)
        
        # Unpack values

        if explore == 1 or history[_apid]["action"].get("now") == None:

            # Create a list of potential candidates (Cannot be itself)
            _choices = list(range(length))
            _choices.remove(_apid)

            # Pick a candidate among the list
            target_ap = np.random.choice(_choices, 1)
            target_ap = target_ap[0]
        else:

            # Unpack mean of scores
            _score = [[key, value] for key, value in history[_apid]["score"]["mean"].items()]
            # Point to the best scoring Access Point
            best_score = sorted(_score, key=itemgetter(1), reverse=True)
            target_ap = best_score[0][0]

        # Save history and increment counter
        history[_apid]["action"]["now"] = target_ap
        _prev_count = history[_apid]["action"]["count"][target_ap]
        history[_apid]["action"]["count"][target_ap] = _prev_count + 1 

        _list_target_ap.append([_apid, target_ap])

    sorted(_list_target_ap, key=itemgetter(0))

    return _list_target_ap, history


# def ucb1(score_ap):

# def multiArmBandit(aplist, epsilon, dataframe):

#     _mab_score_cache = "test/mabscorehistory"
#     _mab_action_cache = "test/mabactionhistory"

#     _list_target_ap = []

#     if Path("sim_cache/test/mabscorehistory.data").exists() and Path("sim_cache/test/mabactionhistory.data").exists():
#         score_history = readSimCache(_mab_score_cache)
#         action_history = readSimCache(_mab_action_cache)

#         inc_serviced_users = [ap.data_serviced_users[-dataframe:] for ap in aplist]
#         # print(inc_serviced_users)
#         # print(score_history)

#         for history in action_history:

#             # Get score from increase of serviced users due to my choice
#             _my_score = inc_serviced_users[history[1]]
#             # print(history)
#             # print(_my_score)

#             # Update score history with new data
#             score_history[history[0]][1][history[1]] += sum(_my_score)
#             _my_score_history = score_history[history[0]]

#             _list_target_ap.append([history[0], epsilonGreedy(_my_score_history, epsilon, len(aplist))])
#     else:
#         # Create empty score history
#         score_history = []

#         for ap in aplist:
#             # Generate an list of apids without the current one
#             _empty_scores = list(range(len(aplist)))
#             _empty_scores.remove(ap.id)

#             _list_empty_scores = {}
#             for _empty_score in _empty_scores:
#                 _list_empty_scores[_empty_score] = 0

#             score_history.append([ap.id, _list_empty_scores])

#             _list_target_ap.append([ap.id, epsilonGreedy([ap.id, {}], epsilon, len(aplist))])

#     # Cache Scores and Action
#     writeSimCache(_mab_score_cache, score_history)
#     writeSimCache(_mab_action_cache, _list_target_ap)

#     return _list_target_ap

def updateHistory(time, aplist, dataframe):
    _mab_history = "test/_mab_history"
    # Create empty history dict when time == 1
    if time == 1:
        history = {}
        num_ap = len(aplist)
        
        for _apid in range(num_ap):
            history[_apid] = {"action" : {},
                    "score" : {}
                    }

            # Create an array without the current apid
            _empty_history = list(range(num_ap))
            _empty_history.remove(_apid)

            history[_apid]["action"]["count"] = {}
            history[_apid]["score"]["list"] = {}
            history[_apid]["score"]["mean"] = {}

            for target in _empty_history:

                history[_apid]["action"]["count"][target] = 0
                history[_apid]["score"]["list"][target] = []
                history[_apid]["score"]["mean"][target] = 0

    else:
        history = readSimCache(_mab_history)

        # list of increase in serviced users
        inc_serviced_users = [ap.data_serviced_users[-dataframe:] for ap in aplist]

        _prev_actionlist = [[key, history[key]["action"]["now"]] for key in history.keys()]

        for _action in _prev_actionlist:

            # Find the effect of my decision
            _my_score = inc_serviced_users[_action[1]]
            # print()
            # print(_action)
            _prev_scores = history[_action[0]]["score"]["list"][_action[1]]

            history[_action[0]]["score"]["list"][_action[1]].append(sum(_my_score))
            history[_action[0]]["score"]["mean"][_action[1]] = mean(_prev_scores)

    return history


def multiArmBanditSel(sel, time, param, aplist):
    _mab_history = "test/_mab_history"

    dataframe = param["dataframe"]

    _history = updateHistory(time, aplist, dataframe)
    
    if sel == 0:
        epsilon = param["epsilon"]
        _list_target, _new_history = epsilonGreedy(_history, epsilon)
    else:
        _new_history = _history
        _list_target = [[apid, 0] for apid in range(len(aplist))]
    # print(_new_history)

    writeSimCache(_mab_history, _new_history)

    return _list_target


# if __name__ == "__main__":

#     print("Multiarm Bandit")

#     for run in range(100):
#         target = epsilonGreedy(0, [0, 1, 2, 3], 0.15)
#         print(target)
