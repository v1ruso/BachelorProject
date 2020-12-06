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
    """
    vector_matrix = np.empty((len(seq_notes),len(seq_notes)),dtype=object)
    for i in range(len(seq_notes)): # rows
        for j in range(len(seq_notes)): # columns
            if j<i:
                vector_matrix[i,j] = (seq_notes[i][0]-seq_notes[j][0],seq_notes[i][1]-seq_notes[j][1])
            else:
                vector_matrix[i,j] = (0,0)
    result = {}
    for i in range(len(seq_notes)):
        for j in range(len(seq_notes)):
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
def sort_patterns_by_length(patterns):
    """
    """
    return 0
def transform_pattern_sequence(patterns):

    return 0

def is_note_in_seq(note,seq):
    for n in seq:
        if n[0] == note[0] and n[1]==note[1]:
            return True
    return False
def score_per_translation_vector(patterns, notes):
    """
    patterns: dictionary, keys are translation vectors, values are notes
        which can be transformed into other notes using the key
    """
    scores = np.zeros(len(patterns.keys()))
    for i, translation_vector in enumerate(patterns):
        first_note_time = patterns[translation_vector][0][0]
        last_note_time = patterns[translation_vector][len(patterns[translation_vector])-1][0]+translation_vector[0]
        nb_notes_spanned_by_pattern = 0
        nb_notes_in_pattern = len(patterns[translation_vector])
        for n in notes:
            if n[0]>= first_note_time and n[0]<=last_note_time:
                current_note = (n[0]+translation_vector[0],n[1]+translation_vector[1])        
    return scores