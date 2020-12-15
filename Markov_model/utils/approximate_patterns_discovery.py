import numpy as np

def hamming_distance(seq_1,seq_2):
    return sum(c1 != c2 for c1, c2 in zip(seq_1, seq_2))

def edit_distance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

def find_approximate_patterns(seq_notes):
    """
    based on SIA(TEC) algorithm
    seq_notes: list of (onset,pitch) elements
    """
    vector_matrix = np.empty((len(seq_notes),len(seq_notes)),dtype=object)
    for i in range(len(seq_notes)): # rows
        if seq_notes[i]==None:
            continue
        for j in range(len(seq_notes)): # columns
            if seq_notes[j]==None:
                continue
            if j<i:
                vector_matrix[i,j] = (seq_notes[i][0]-seq_notes[j][0],seq_notes[i][1]-seq_notes[j][1])
            else:
                vector_matrix[i,j] = (0,0)
    result = {}
    for i in range(len(seq_notes)):
        if seq_notes[i]==None:
            continue
        for j in range(len(seq_notes)):
            if seq_notes[j]==None:
                continue
            if vector_matrix[i,j][0]==0 and vector_matrix[i,j][1]==0:
                continue
            else:
                if vector_matrix[i,j] in result:
                    result[vector_matrix[i,j]].append(seq_notes[j])
                else:
                    result[vector_matrix[i,j]] = list()
                    result[vector_matrix[i,j]].append(seq_notes[j])
    """mtp_head = (0,0)
    mtp_datapoints = list()
    max_length = 0
    for vector in result:
        if len(result[vector])>max_length:
            max_length=len(result[vector])
            mtp_datapoints = result[vector]
            mtp_head = vector"""
    return result

def is_note_in_seq(note,seq):
    for n in seq:
        if n[0] == note[0] and n[1]==note[1]:
            return True
    return False

def are_seqs_equal(seq_1,seq_2):
    if len(seq_1)!=len(seq_2):
        return False
    for i in range(len(seq_1)):
        if seq_1[i][0]!=seq_2[i][0] or seq_1[i][1]!=seq_2[i][1]:
            return False
    return True
def filter_patterns(patterns, notes):
    """
    patterns: dictionary, keys are translation vectors, values are notes
        which can be transformed into other notes using the key
    """
    # first transform list of notes into dictionary
    new_patterns = {}
    for key in patterns:
        # transform list of notes from pattern into dictionary
        temp_notes = {}
        for n in patterns[key]:
            temp_notes[n[0]]=n[1]
        temp_pattern = list()
        # filter patterns so that a note isn't repeated twice within a pattern
        for n in patterns[key]:
            new_note = (n[0]+key[0],n[1]+key[1])
            if new_note[0] not in temp_notes:
                temp_pattern.append(n)
        # now we need to check if all elements are contiguous within a pattern
        # TODO correct this
        new_patterns[key] = list()
        for i in range(len(notes)):
            if notes[i]==None:
                continue
            if notes[i][0] == temp_pattern[0][0] and notes[i][1] == temp_pattern[0][1]:
                for j in range(i,min(len(notes),len(temp_pattern))):
                    if notes[j][0] == temp_pattern[j][0] and notes[j][1] == temp_pattern[j][1]:
                        new_patterns[key].append(temp_pattern[j])
                    else:
                        break
    # now remove empty entries
    result = {}
    for key in new_patterns:
        if len(new_patterns[key])>1:
            result[key] = new_patterns[key]
    return result
def find_biggest_pattern_in_patterns(dict):
    max_length = -1
    pattern = None
    trans_vector = None
    for key in dict:
        if len(dict[key])>max_length:
            max_length=len(dict[key])
            trans_vector = key
            pattern = dict[key]
    return pattern, trans_vector
def find_all_trans_vector_with_pattern(dict,pattern):
    ret = list()
    for key in dict:
        if are_seqs_equal(pattern,dict[key]):
            ret.append(key)
    return ret
def find_patterns_in_notes(patterns,notes):
    pass
