import pretty_midi
import numpy as np

def find_closest(values,val):
    """
    Finds the closest value in the list.
    values: array-like of possible values
    val: value to compare with all the values in the list.
    """
    closest = values[0]
    distance = float("inf")
    for d in values:
        new_dist = abs(d-val)
        if new_dist < distance:
            distance = new_dist
            closest = d
    return closest

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
    nb_dict = {}
    for i in range(length-1):
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

    # special case for the last element
    # need to "fallback" -> go back to a known state
    probability_known_patterns = 0.9
    probability_unknown_patterns = 1-probability_known_patterns
    last_item = table[length-1]
    if last_item not in ret:
        ret[last_item] = {}
        for i in range(length):
            next_item = table[i]
            if next_item in ret[last_item]:
                ret[last_item][next_item] += 1
            else:
                ret[last_item][next_item] = 1
        for key in ret[last_item].keys():
            ret[last_item][key] /= length
    
    probability_keys = {}
    for item in table:
        if item in probability_keys:
            probability_keys[item]+=1
        else:
            probability_keys[item]=1
    for key in probability_keys:
        probability_keys[key]/=length
    # alpha smoothing for all states
    for item in ret:
        keys_ret = list(ret.keys())
        for key in ret[item]:
            ret[item][key]*=probability_known_patterns
            ret[item][key] += probability_keys[key]*probability_unknown_patterns
            keys_ret.remove(key)
        for key in keys_ret:
            ret[item][key] = probability_keys[key]*probability_unknown_patterns
    return ret

def midi_to_csv(notes,filename):
    csv = ""
    for i in range(len(notes)):
        note = notes[i]
        # write onto csv, each line like: start,pitch,morph_pitch,duration,channel\n
        # morph pitch == pitch here. It is unused, as well as the channel
        csv += str(note.start) + "," + str(note.pitch) + "," + str(note.pitch) + "," + str(note.get_duration()) + "," + str(4) + "\n"
    file = open(filename, "w")
    file.write(csv)
    file.close()

def csv_to_notes(filename):
    import csv
    notes = list()
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            notes.append(pretty_midi.Note(velocity=80,start=float(row[0]),pitch=int(row[1]),end=float(row[0])+float(row[3])))
    return notes
