import numpy as np
from .midi_transform import markov_model_first_order

def is_pitch_equal(this,that):
    if this==None or that==None:
        return False
    return this.pitch == that.pitch and this.get_duration() == that.get_duration()

def find_biggest_recurring_pattern(seq):
    """
    seq: sequence of notes
    """
    A = np.zeros((len(seq)+1,len(seq)+1),dtype=int)
    res = list()
    res_length = 0
    index = 0
    for i in range(1,len(seq)+1):
        for j in range(i+1,len(seq)+1):
            if seq[i-1]!=None and seq[j-1]!=None and is_pitch_equal(seq[i-1],seq[j-1]) and (j-i) > A[i-1][j-1]:
                A[i][j] = A[i-1][j-1] + 1
                if A[i][j] > res_length:
                    res_length = A[i][j]
                    index = max(i,index)
            else:
                A[i][j] = 0
    if res_length > 0:
        for i in range(index-res_length + 1, index+1):
            res.append(seq[i-1])
    return res, index-res_length

def find_occurrences_and_indexes(seq):
    """
    seq: sequence of notes
    """
    res, index_first_occurrence = find_biggest_recurring_pattern(seq)
    if len(res)==0:
        return seq, None, list()
    temp_seq = seq[0:index_first_occurrence]
    i = index_first_occurrence
    index_occurrences = list()
    while i < len(seq):
        is_start = False
        if is_pitch_equal(seq[i],res[0]):
            is_start = True
            for j in range(len(res)):
                if i + j >= len(seq) or not is_pitch_equal(seq[i+j],res[j]):
                    is_start = False
                    break
        if not is_start:
            temp_seq.append(seq[i])
            i+=1
        else:
            index_occurrences.append(i)
            for j in range(len(res)):
                temp_seq.append(None)
            i+=len(res)
    return temp_seq, res, index_occurrences

def find_all_occurrences_and_indexes(seq):
    """
    seq: sequence of notes
    """
    list_patterns = list()
    list_indexes = list()
    res = list()
    seq_x = seq
    while res!=None:
        seq_x, res, indexes = find_occurrences_and_indexes(seq_x)
        if res!=None:
            list_patterns.append(res)
            list_indexes.append(indexes)
    for i in range(len(seq_x)):
        # special case for non recurring patterns: notes that appear only once
        if seq_x[i]!=None:
            list_patterns.append([seq_x[i]])
            list_indexes.append([i])
    return list_patterns,list_indexes

def first_order_markov_with_patterns(seq):
    """
    seq: sequence of notes
    """
    list_patterns, list_indexes = find_all_occurrences_and_indexes(seq)
    index_to_pattern_index = {}
    for i in range(len(list_indexes)):
        for j in range(len(list_indexes[i])):
            index_to_pattern_index[list_indexes[i][j]] = i
    pattern_indexes_seq = list()
    if len(index_to_pattern_index.keys())>0:
        head = 0
        while head < len(seq):
            pattern_indexes_seq.append(index_to_pattern_index[head])
            head += len(list_patterns[index_to_pattern_index[head]])
    return markov_model_first_order(pattern_indexes_seq),list_patterns,list_indexes,pattern_indexes_seq
