import pretty_midi
import numpy as np

def parse_midi(notes,round_durations=4):
    """
    Parse midi notes into four lists: pitches, onsets, velocities and durations
    
    Input: array-like of pretty_midi notes
    Output: four np.array in this order: pitches, onsets, velocities and durations
    """
    length = len(notes)
    pitches = np.zeros(length)
    onsets = np.zeros(length)
    velocities = np.zeros(length)
    durations = np.zeros(length)
    for i in range(length):
        pitches[i] = notes[i].pitch
        onsets[i] = notes[i].start
        velocities[i] = notes[i].velocity
        durations[i] = round(notes[i].get_duration(),round_durations)

    return pitches, onsets, velocities, durations

def markov_model_first_order(table):
    """
    Returns a 1-order markov model.
    Inputs:
        table: array_like of items to calculate a 1-order markov model from
    Output:
        ret: a dictionary of event:key:probability of that event happening.
    """
    ret = {}
    length = len(table)
    assert length > 0
    # TODO I fixed the problem of unknown pitches reusing the first note as 
    # if it was the last, resulting in basically a cyclic array
    table = np.append(table,table[0])
    nb_dict = {}
    for i in range(length):
        item = table[i]
        next_item = table[i+1]
        if item in ret:
            nb_dict[item] += 1
            if next_item in ret[item]:
                ret[item][next_item] += 1
            else:
                ret[item][next_item] = 1            
        else:
            nb_dict[item] = 1
            ret[item] = {}
            ret[item][next_item] = 1
    for key_1 in ret.keys():
        for key_2 in ret[key_1].keys():
            ret[key_1][key_2] /= nb_dict[key_1]
    return ret

