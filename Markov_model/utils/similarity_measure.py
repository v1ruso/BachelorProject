import pretty_midi
import numpy as np
import itertools
from midi_transform import markov_model_first_order
NUMBER_OF_PITCHES = 128
PITCHES_PER_OCTAVE = 12


def is_note_in_seq(note, seq):
    for n in seq:
        if note.pitch == n.pitch and note.start == n.start:
            return True
    return False


def similarity_score_with_translation(seq_main,seq_compared):
    """
    Calculates the similarity score between two sets of notes.
    seq_main,seq_compared: sets of pretty_midi notes.
    return: the similarity score [0,1], higher values mean higher similarity
    This method doesn't work with time dilation.
    """
    all_pairs = itertools.product(seq_compared, seq_main)
    max_number_of_sim_notes = 0
    for current_translation_vector in all_pairs:
        current_number_of_sim_notes = 0
        diff_onsets = current_translation_vector[0].start - current_translation_vector[1].start
        diff_pitches = current_translation_vector[0].pitch - current_translation_vector[1].pitch
        for j in range(len(seq_compared)):
            new_note = pretty_midi.Note(velocity=seq_compared[j].velocity,
                                        pitch=seq_compared[j].pitch - diff_pitches,
                                        start=seq_compared[j].start - diff_onsets,
                                        end=seq_compared[j].end - diff_onsets)
            if is_note_in_seq(new_note, seq_main):
                current_number_of_sim_notes += 1
        if current_number_of_sim_notes > max_number_of_sim_notes:
            max_number_of_sim_notes = current_number_of_sim_notes
    return max_number_of_sim_notes / len(seq_main)

def similarity_score(seq_main, seq_compared):
    # computes how similar two sequences are
    # higher returned values mean higher similarities
    # returns values between 0 and 1
    if len(seq_main) == 0 or len(seq_compared) == 0:
        return 0.0
    else:
        A = np.zeros((len(seq_compared)+1, len(seq_main)+1))
        W_insert = -0.5
        W_delete = -0.5
        for i in range(1, len(seq_compared)+1):
            for j in range(1, len(seq_main)+1):
                subs = 1 if seq_compared[i-1] == seq_main[j-1] else -1
                A[i][j] = np.max([
                    A[i - 1][j - 1] + subs, A[i][j - 1] + W_insert,
                    A[i - 1][j] + W_delete, 0
                ])
        return np.max(A) / len(seq_main)

def biggest_substring(seq_main, seq_compared):
    if len(seq_main) == 0 or len(seq_compared) == 0:
        return np.array([])
    else:
        A = np.zeros((len(seq_main), len(seq_compared)),dtype=int)
        ret = np.array([])
        z = 0
        for i in range(len(seq_main)):
            for j in range(len(seq_compared)):
                if seq_compared[j]==seq_main[i]:
                    if i==0 or j==0:
                        A[i][j]=1
                    else: 
                        A[i][j]=A[i-1][j-1]+1
                    if A[i][j] > z:
                        z = A[i][j]
                        ret = seq_main[i-z + 1:i+1]
                    elif A[i][j] == z:
                        np.append(ret,seq_main[i-z+1:i+1])
                else:
                    A[i][j] = 0
        return ret

def biggest_submelody(seq_main, seq_compared):
    """
    Compares all possible substring of seq_compared to seq_main.
    Returns the pattern which has the biggest similarity with seq_main.
    In other words, it returns the biggest pattern that appears in both melodies.
    seq_main: pretty_MIDI sequence of notes (monophonic)
    seq_compared: pretty_MIDI sequence of notes (monophonic)
    """
    max_subset = np.array([])
    max_similarity = 0
    for i in range(len(seq_compared)):
        for j in range(i + 1, len(seq_compared) + 1):
            current_subset = seq_compared[i:j]
            current_similarity_score = similarity_score_with_translation(seq_main, current_subset)
            if current_similarity_score > max_similarity:
                max_similarity = current_similarity_score
                max_subset = current_subset
    return max_subset

def count_substring_in_string(substring,string):
    return string.count(substring)

def find_biggest_recurring_pattern(seq,special_char = ' '):
    """
    Find the biggest recurring pattern in the array of pitches
    Dynamic programming: longest repeating and non-overlapping substring
    Finds result in O(n^2)
    Code inspired by https://www.geeksforgeeks.org/longest-repeating-and-non-overlapping-substring/
    Returns the biggest sequence and the index of the first time it appears
    """
    A = np.zeros((len(seq)+1,len(seq)+1),dtype=int)
    res = ""
    res_length = 0
    index = 0
    for i in range(1,len(seq)+1):
        for j in range(i+1,len(seq)+1):
            if seq[i-1]==seq[j-1] and (j-i) > A[i-1][j-1] and seq[i-1]!=special_char:
                A[i][j] = A[i-1][j-1] + 1
                if A[i][j] > res_length:
                    res_length = A[i][j]
                    index = max(i,index)
            else:
                A[i][j] = 0
    if (res_length > 0): 
        for i in range(index - res_length + 1, index + 1): 
            res = res + seq[i-1]#np.append(res,seq[i - 1]) 
  
    return res, index-res_length

def find_occurrences_and_indexes(seq):
    """
    Given a sequence, finds the biggest recurring pattern in it, and replaces
    it with " " (space character). Also returns the indexes where it occurs.
    Ex: seq=01201, then the biggest recurring pattern is "01", the indexes would
    be 0 and 3, and the resulting string is "  2  "
    """
    res, index_first_occurrence = find_biggest_recurring_pattern(seq)
    if res=="":
        return seq, None, list()
    temp_seq = seq[0:index_first_occurrence]
    i = index_first_occurrence
    index_occurrences = list()
    while i < len(seq):
        is_start = False
        if seq[i]==res[0]:
            is_start = True
            for j in range(len(res)):
                if i+j >= len(seq) or seq[i+j]!=res[j]:
                    is_start = False
                    break
        if not is_start:
            temp_seq += seq[i]
            i+=1
        else:
            index_occurrences.append(i)
            for j in range(len(res)):
                temp_seq+=" "
            i += len(res)
    return temp_seq, res, index_occurrences

def find_all_occurrences_and_indexes(seq):
    """
    Given a string, find all patterns in it and their start indices
    Ex: seq = 01201. list_patterns = ["01","2"], list_indexes = [[0,3],[2]]
    """
    list_patterns = list()
    list_indexes = list()
    res = ""
    seq_x = seq
    while res!=None:
        seq_x, res, indexes = find_occurrences_and_indexes(seq_x)
        if res!=None:
            list_patterns.append(res)
            list_indexes.append(indexes)
    for i in range(len(seq_x)):
        if seq_x[i]!=' ':
            list_patterns.append(seq_x[i])
            list_indexes.append([i])
    return list_patterns, list_indexes

def first_order_markov_from_patterns(seq,list_pattern,list_indexes):
    """
    Given a string, a list of patterns and its indexes, find the first order markov model
    of the patterns.
    Ex: seq = "01201", list_patterns = ["01","2"] and list_indexes = [[0,3],[2]]
    The result would be {0:{1:1.0},1:{0:1.0}}.

    In other words, the first pattern "01" (index 0) is followed by the second pattern "2" (index 1)
    with probability 1. Same goes the other way around.
    """
    index_to_pattern_index = {}
    for i in range(len(list_indexes)):
        for j in range(len(list_indexes[i])):
            index_to_pattern_index[list_indexes[i][j]] = i
    pattern_indexes_seq = ""
    if len(index_to_pattern_index.keys())>0:
        head = 0
        while head<len(seq):
            pattern_indexes_seq += str(index_to_pattern_index[head])
            head += len(list_pattern[index_to_pattern_index[head]])
    return markov_model_first_order(pattern_indexes_seq)

