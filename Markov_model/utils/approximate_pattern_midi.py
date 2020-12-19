import numpy as np
import pretty_midi
def find_approximate_patterns(seq_notes):
    """
    seq_notes: a list a pretty_midi notes
    based on SIA(tec) algorithm
    """
    vector_matrix = np.empty((len(seq_notes),len(seq_notes)),dtype=object)
    for i in range(len(seq_notes)): # rows
        if seq_notes[i]==None:
            continue
        for j in range(len(seq_notes)): # columns
            if seq_notes[j]==None:
                continue
            if j<i:
                vector_matrix[i,j] = (seq_notes[i].start-seq_notes[j].start,seq_notes[i].pitch-seq_notes[j].pitch)
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
    return result

def is_note_in_seq(note,seq):
    for n in seq:
        if n.start == note.start and n.pitch == note.pitch:
            return True
    return False
def are_seqs_equal(seq_1,seq_2):
    if len(seq_1)!=len(seq_2):
        return False
    for i in range(len(seq_1)):
        if seq_1[i].start!=seq_2[i].start or seq_1[i].pitch!=seq_2[i].pitch:
            return False
    return True

def filter_patterns(patterns, notes):
    """
    patterns: dictionary, keys are translation vectors, values are notes which 
        can be transformed into other notes using the key
    """
    # first transform list of notes into dictionary
    new_patterns = {}
    for key in patterns:
        # transform list of notes from pattern into dictionary
        temp_notes = {}
        for n in patterns[key]:
            temp_notes[n.start] = n.pitch
        temp_pattern = list()
        # filter patterns so that a note isn't repeated twice within a pattern
        for n in patterns[key]:
            if (n.start + key[0]) not in temp_notes:
                temp_pattern.append(n)
        # now we need to check if all elements are contiguous within a pattern
        new_patterns[key] = list()
        for i in range(len(notes)):
            if notes[i]==None:
                continue
            if notes[i].start == temp_pattern[0].start and notes[i].pitch == temp_pattern[0].pitch:
                for j in range(0,min(len(notes),len(temp_pattern))):
                    if notes[j+i].start == temp_pattern[j].start and notes[j+i].pitch == temp_pattern[j].pitch:
                        new_patterns[key].append(temp_pattern[j])
                    else:
                        break
    # now remove whose size is not greater than 1
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
    return pattern,trans_vector
def find_all_trans_vector_with_pattern(dict, pattern):
    ret = list()
    for key in dict:
        if are_seqs_equal(pattern,dict[key]):
            ret.append(key)
    return ret
def find_pattern_with_indices(seq,list_patterns,pattern_to_indices,index_pattern):
    """
    seq: list of pretty midi notes
    pattern_to_indices: already existent patterns
    index_pattern: key where to add the new pattern, i.e. pattern_to_indices[index_pattern] = ...
    This method is supposed to find one pattern.
    """
    result = find_approximate_patterns(seq)
    result_filter = filter_patterns(result,seq)
    pattern,trans_vector = find_biggest_pattern_in_patterns(result_filter)
    if pattern!=None:
        all_trans_vectors = find_all_trans_vector_with_pattern(result_filter,pattern)
        all_trans_vectors.insert(0,(0,0))
        ret_trans_vectors = list()
        for trans in all_trans_vectors:
            first_trans_note = (pattern[0].start + trans[0],pattern[0].pitch + trans[1])
            length_pattern = len(pattern)
            i = 0
            current_pattern = list()
            while i<len(seq):
                current_note = seq[i]
                if current_note!=None and current_note.start == first_trans_note[0] and current_note.pitch == first_trans_note[1]:
                    pattern_to_indices[index_pattern] = i
                    for j in range(length_pattern):
                        trans_note = pretty_midi.Note(velocity = 100, start = pattern[j].start + trans[0],end=pattern[j].start + trans[0]+1, pitch = pattern[j].pitch + trans[1])
                        current_pattern.append(trans_note)
                        seq[i+j] = None
                    break
                else:
                    i+=1
            if len(current_pattern)!=0:
                index_pattern+=1
                ret_trans_vectors.append(trans)
                list_patterns.append(current_pattern)
        return pattern,index_pattern,None
def is_list_empty(seq):
    for n in seq:
        if n!=None:
            return False
    return True

def find_all_patterns(seq):
    list_patterns = list()
    pattern_to_indices = {}
    index_pattern = 0
    trans_vectors = list()
    while not is_list_empty(seq):
        pattern,index_pattern,all_trans_vectors = find_pattern_with_indices(seq,list_patterns,pattern_to_indices,index_pattern)
        if pattern==None: # case only one note patterns
            for i in range(len(seq)):
                if seq[i]!=None:
                    list_patterns.append([seq[i]])
                    pattern_to_indices[index_pattern] = i
                    index_pattern+=1
                    trans_vectors.append((0,0))
            break
        for i in range(len(all_trans_vectors)):
            trans_vectors.append(all_trans_vectors[i])
    return list_patterns,pattern_to_indices,trans_vectors

def collapse_pattern_to_indices(trans_vectors):
    trans_vectors.append((0,0))
    collapsed_indices_to_pattern = {}
    current_index = 0
    i = 0
    while i<len(trans_vectors)-1:
        trans_v = trans_vectors[i]
        if trans_v[0]==0 and trans_v[1]==0:
            temp_dict = {}
            temp_index = 0.0
            temp_dict[temp_index] = list()
            temp_dict[temp_index].append(i)
            for j in range(i+1,len(trans_vectors)):
                current_trans = trans_vectors[j]
                if current_trans[0]==0 and current_trans[1]==0:
                    for key in temp_dict:
                        collapsed_indices_to_pattern[current_index] = temp_dict
                        current_index+=1
                    break
                if current_trans[1] not in temp_dict:
                    temp_dict[current_trans[1]] = list()
                temp_dict[current_trans[1]].append(j)
            else:
                continue
        i+=1
    return collapsed_indices_to_pattern

def transform_collapsed_and_indices(collapsed,pattern_to_indices):
    true_indices = {}
    for key in collapsed:
        true_indices[key] = list()
        for val in collapsed[key]:
            true_indices[key].append(pattern_to_indices[val])
    return true_indices

def transform_back_into_seq(true_indices):
    reversed_indices = {}
    for key in true_indices:
        for val in true_indices[key]:
            reversed_indices[val] = key
    seq = list()
    keys = list(reversed_indices.keys())
    keys.sort()
    for val in keys:
        seq.append(reversed_indices[val])
    return seq