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
    _list_target_ap = []

    for _apid in history.keys():

        explore = np.random.binomial(1, epsilon)
        
        # Unpack values
        if explore == 1 or history[_apid]["action"].get("now") == None:
            length = len(history.keys())

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


def ucb1(history):

    _list_target_ap = []
    # print(history)

    for _apid in history.keys():
        _score = [[key, value] for key, value in history[_apid]["score"]["mean-ucb"].items()]

        best_score = sorted(_score, key=itemgetter(1), reverse=True)
        target_ap = best_score[0][0]

        # Save history and increment counter
        history[_apid]["action"]["now"] = target_ap
        _prev_count = history[_apid]["action"]["count"][target_ap]
        # print(_prev_count)
        history[_apid]["action"]["count"][target_ap] = _prev_count + 1 

        _list_target_ap.append([_apid, target_ap])

    sorted(_list_target_ap, key=itemgetter(0))

    return _list_target_ap, history


def updateHistory(history, time, aplist, dataframe, sel, param):
    # history = readSimCache(_mab_history)
    # history = _history

    # list of increase in serviced users
    inc_serviced_users = [ap.data_serviced_users[-dataframe:] for ap in aplist]

    if sel == 0 and time == 1:
        return history

    if sel == 1 and time == 1:
        for _apid in history.keys():
            for key in history[_apid]["action"]["count"].keys():
                history[_apid]["action"]["count"][key] += 1
                history[_apid]["score"]["list"][key].append(mean(inc_serviced_users[key]))
                history[_apid]["score"]["mean"][key] = mean(inc_serviced_users[key])
                history[_apid]["score"]["mean-ucb"][key] = mean(inc_serviced_users[key]) / 115

        return history

    # Keep the last 5 scores when the list is too long
    if len(history[0]["score"]["list"][1]) == 48:

        for _apid in history.keys():
            for key in history[_apid]["action"]["count"].keys():
                history[_apid]["score"]["list"][key] = history[_apid]["score"]["list"][key][-5:]

    for _apid in history.keys():

        _prev_target = history[_apid]["action"]["now"]
        _new_score = inc_serviced_users[_prev_target]
        history[_apid]["score"]["list"][_prev_target].append(mean(_new_score))

        _scores = history[_apid]["score"]["list"][_prev_target]
        # print(_scores)

        # Calculate new mean
        history[_apid]["score"]["mean"][_prev_target] = sum(_scores) / len(_scores)

        # Calculate UCB Mean
        if sel == 1:
            _ucb_scale = param["ucbscale"]

            for item in history[_apid]["score"]["mean-ucb"].keys():
                _my_count = history[_apid]["action"]["count"][item]

                history[_apid]["score"]["mean-ucb"][item] = (history[_apid]["score"]["mean"][item]) / 115 + np.sqrt(
                    ((_ucb_scale * np.log10(time)) / _my_count))

    return history


def generateHistory(length):
    _history = {}
    
    for _apid in range(length):
        _history[_apid] = { 
            "action" : { 
                "count" : {},
                "now" : None
            },
            "score" : { 
                "list" : {},
                "mean" : {},
                "mean-ucb" : {}
            }
        }

        # Create an array without the current apid
        _empty_history = list(range(length))
        _empty_history.remove(_apid)

        for target in _empty_history:

            _history[_apid]["action"]["count"][target] = 0
            _history[_apid]["score"]["list"][target] = []
            _history[_apid]["score"]["mean"][target] = 0
            _history[_apid]["score"]["mean-ucb"][target] = 0

    return _history


def multiArmBanditSel(sel, time, param, aplist, history):

    dataframe = param["dataframe"]

    _history = updateHistory(history, time, aplist, dataframe, sel, param)

    
    if sel == 0:
        epsilon = param["epsilon"]
        _list_target, _history = epsilonGreedy(_history, epsilon)
    elif sel == 1:
        _list_target, _history = ucb1(_history)
    else:
        # _new_history = _history
        _list_target = [[apid, 0] for apid in range(len(aplist))]

    # if time == 100:
    #     print(history)

    #     exit()
    return _list_target, _history

