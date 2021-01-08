import random
import pretty_midi
import numpy as np
import glob
from utility import *

def find_approximate_patterns(seq_notes):
    """
    Based on SIA(TEC) algorithm
    seq_notes: list of (onset,pitch) elements
    
    Returns a dictionary of translation vectors: (onset,pitch).
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
    return result

def is_note_in_seq(note,seq):
    """
    note: (onset,pitch) tuple
    seq: list of (onset,pitch) tuples
    
    Returns True if note is in seq.
    """
    for n in seq:
        if n[0] == note[0] and n[1]==note[1]:
            return True
    return False

def are_seqs_equal(seq_1,seq_2):
    """
    seq_1: list of (onset,pitch) tuples
    seq_2: list of (onset,pitch) tuples
    
    Returns True if the two lists are equal.
    """
    if len(seq_1)!=len(seq_2):
        return False
    for i in range(len(seq_1)):
        if seq_1[i][0]!=seq_2[i][0] or seq_1[i][1]!=seq_2[i][1]:
            return False
    return True

def filter_patterns(patterns, notes):
    """
    patterns: dictionary, keys are translation vectors, values are (onset,pitch) tuples
        which can be transformed into other tuples using the key
        
    Returns a filtered version of the patterns found. Keeps only the values which don't overlap:
    ex: pattern = [(0,1),(1,2)], translation vector =(1,1), the first note can be turned into a 
    note within the same pattern, so we remove that entry.
    
    And values whose notes are not continuous, let's say we have four notes:
    [(0,0),(1,1),(2,0),(3,1)], a pattern would be [(0,0),(2,0)] and its corresponding translection vector is
    (1,1). However, the notes in the patterns are not continuous, so we remove that entry.
    
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
        new_patterns[key] = list()
        for i in range(len(notes)):
            if notes[i]==None:
                continue
            if notes[i][0] == temp_pattern[0][0] and notes[i][1] == temp_pattern[0][1]:
                for j in range(0,min(len(notes),len(temp_pattern))):
                    if notes[j+i]==None:
                        continue
                    if notes[j+i][0] == temp_pattern[j][0] and notes[j+i][1] == temp_pattern[j][1]:
                        new_patterns[key].append(temp_pattern[j])
                    else:
                        break
    # now remove entries containing 0 or 1 note
    result = {}
    for key in new_patterns:
        if len(new_patterns[key])>1:
            result[key] = new_patterns[key]
    return result

def find_biggest_pattern_in_patterns(dict):
    """
    dict: dictionary of translation vector->pattern
    
    Returns the biggest pattern and its corresponding translation vector.
    """
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
    """
    dict: dictionary of translation vector->pattern
    pattern: list of (onset,pitch)
    
    Returns all translation vectors which have the same pattern as key
    """
    ret = list()
    for key in dict:
        if are_seqs_equal(pattern,dict[key]):
            ret.append(key)
    return ret

def find_pattern_with_indices(seq,list_patterns,pattern_to_indices,index_pattern):
    """
    seq: list of (onset,pitch) elements
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
        index_before = index_pattern
        ret_trans_vectors = list()
        for trans in all_trans_vectors:

            first_trans_note = (pattern[0][0]+trans[0],pattern[0][1]+trans[1])
            length_pattern = len(pattern)
            i = 0
            current_pattern = list()
            while i < len(seq):
                current_note = seq[i]
                if current_note!=None and current_note[0]==first_trans_note[0] and current_note[1] == first_trans_note[1]:
                    pattern_to_indices[index_pattern] = i
                    for j in range(length_pattern):
                        trans_note = (pattern[j][0]+trans[0],pattern[j][1]+trans[1])
                        current_pattern.append(trans_note)
                        seq[i+j] = None
                    break
                else:
                    i+=1
            if len(current_pattern)!=0:
                index_pattern+=1
                ret_trans_vectors.append(trans)
                list_patterns.append(current_pattern)
        return pattern,index_pattern,ret_trans_vectors
    return pattern,index_pattern,None

def is_list_empty(seq):
    """
    Checks whether "seq" containes only None values
    """
    for n in seq:
        if n!=None:
            return False
    return True

def find_all_patterns(seq):
    """
    finds all patterns in a list of (onset,pitch) tuples.
    Ex: let a certain sequence be 0,1,2,0,1,2,2,3,4,1,3,1,3
    Then a first pattern would be [0,1,2], appearing three times, 
    the third time being shifted up by 2 ([2,3,4]).
    A second pattern would be [1,3], appearing twice.
    In this case, the function should return:
    list_patterns = [[0,1,2],[0,1,2],[2,3,4],[1,3],[1,3]]
    patterns_to_indices = {
        0: 0,
        1: 3,
        2: 6,
        3: 9,
        4: 11
    }
    """
    list_patterns = list()
    pattern_to_indices = {}
    index_pattern = 0
    trans_vectors = list()
    while not is_list_empty(seq):
        pattern,index_pattern,all_trans_vectors = find_pattern_with_indices(seq,list_patterns,pattern_to_indices,index_pattern)
        if pattern==None: # case only one note at the end
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
    """
    trans_vectors: list of translation vectors
    
    Let's say we have the following translation vectors:
    [(0,0),(1,0),(0,0),(2,1),(0,0)], then for the generation process, we'll
    need to have different patterns if the translation vectors are different in their second value.
    So technically, (0,0) and (1,0) are the same patterns, only time-shifted. However,
    (0,0) and (2,1) are different, as they are vertically shifted.
    """
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
                        collapsed_indices_to_pattern[current_index] = temp_dict[key]
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
    """
    Takes results from collapse_pattern_to_indices and patterns to indices and 
    returns the indices of each pattern within the sequence of notes
    """
    true_indices = {}
    for key in collapsed:
        true_indices[key] = list()
        for val in collapsed[key]:
            true_indices[key].append(pattern_to_indices[val])
    return true_indices

def transform_back_into_seq(true_indices):
    """
    Given the indices of the prime, returns a sequence of patterns.
    """
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

def midi_notes_to_tuples(notes):
    """
    converts a sequence of pretty_midi notes into a list of (onset,pitch) elements
    """
    seq = list()
    for n in notes:
        seq.append((n.start,n.pitch))
    return seq



def generate_prediction_with_translation_based(filename, patterns_to_generate = 4,with_smoothing=False,probability_known_patterns=0.9):
    """
    filename: string of the filename to read, has to be a midi (.mid) file.
    patterns_to_generate: the number of patterns to generate in the continuation
    with_smoothing: default False. Whether the continuation should have additive smoothing or not.
    probability_known_patterns: only useful when with_smoothing is set to True. It is the probability assigned to known patterns,
    1 - probability_known_patterns will be the probilities assigned to unknown patterns. Needs to be between 0 and 1.
    """
    NB_ITERATIONS = patterns_to_generate
    seq_temp = pretty_midi.PrettyMIDI(filename).instruments[0].notes
    
    # 0) Transform seq_temp so it has correct durations
    _,onsets,_,_ = parse_midi(seq_temp)
    diff_onsets = onsets[1:] - onsets[:len(onsets)-1]
    notes = list()
    # write current notes, each note ends when the next note starts
    for i in range(len(seq_temp)-1):
        note = seq_temp[i]
        notes.append(pretty_midi.Note(velocity=note.velocity,pitch=note.pitch,start=note.start,end=seq_temp[i+1].start))
    # special case for last note, as there isn't a next note
    last_note = seq_temp[len(seq_temp)-1]
    notes.append(pretty_midi.Note(velocity=last_note.velocity,pitch=last_note.pitch,start=last_note.start,end=last_note.start + find_closest(diff_onsets,last_note.get_duration())))

    tuples = midi_notes_to_tuples(seq_temp)

    # 1) Transform sequence of notes into sequence of patterns 
    list_patterns,pattern_to_indices,trans_vectors = find_all_patterns(tuples)
    collapsed = collapse_pattern_to_indices(trans_vectors)
    true_indices = transform_collapsed_and_indices(collapsed,pattern_to_indices)
    seq = transform_back_into_seq(true_indices)
    mm1 = markov_model_first_order(seq,with_smoothing,probability_known_patterns)
    # 2) Generate next patterns
    for i in range(NB_ITERATIONS):
        last_pattern = seq[len(seq)-1]
        next_pattern = random.choices(list(mm1[last_pattern].keys()),weights=mm1[last_pattern].values())[0]
        seq.append(next_pattern)
    # 3) Transform back into notes
    # need to use collapsed, and list of patterns and seq
    notes_to_write = list()
    # need index first pattern and length of pattern
    first_pattern = notes[true_indices[seq[0]][0]:true_indices[seq[0]][0]+len(list_patterns[collapsed[seq[0]][0]])]
    # special case for the first pattern, as there is no previous note to base the duration on.
    first_note = first_pattern[0]
    notes_to_write.append(first_note)
    for i in range(1,len(first_pattern)):
        current_note = first_pattern[i]
        previous_note = notes_to_write[len(notes_to_write)-1]
        new_note = pretty_midi.Note(velocity=current_note.velocity,pitch=current_note.pitch,start=previous_note.end,end=previous_note.end+current_note.get_duration())
        notes_to_write.append(new_note)
    # for the other patterns
    for i in range(1,len(seq)):
        current_pattern = notes[true_indices[seq[i]][0]:true_indices[seq[i]][0]+len(list_patterns[collapsed[seq[i]][0]])]
        for j in range(len(current_pattern)):
            current_note = current_pattern[j]
            previous_note = notes_to_write[len(notes_to_write)-1]
            new_note = pretty_midi.Note(velocity=current_note.velocity,pitch=current_note.pitch, start = previous_note.end,end=previous_note.end + current_note.get_duration())
            notes_to_write.append(new_note)
    # 4) Write results
    result = pretty_midi.PrettyMIDI()
    result_program = pretty_midi.instrument_name_to_program("Acoustic Grand Piano")
    result_instrument = pretty_midi.Instrument(program=result_program)
    result_instrument.notes = notes_to_write#[len(seq_temp):]
    result.instruments.append(result_instrument)
    filename = filename.split("/")
    filename = filename[len(filename)-1]
    result.write(filename[:len(filename)-4] + "_result.mid")
    # 5) Show results using abjad
    show_notes(result_instrument.notes)

def generate_prediction_with_translation_based_for_dataset(dataset_filepath, patterns_to_generate = 20,with_smoothing=True,probability_known_states=0.9):
    """
    dataset_filepath: string of the dataset path to read from.
    patterns_to_generate: the number of patterns to generate in the continuation
    with_smoothing: default True. Whether the continuation should have additive smoothing or not.
    probability_known_patterns: only useful when with_smoothing is set to True. It is the probability assigned to known patterns,
    1 - probability_known_patterns will be the probilities assigned to unknown patterns. Needs to be between 0 and 1.
    """
    DATASET_FILEPATH = dataset_filepath
    NB_ITERATIONS = patterns_to_generate
    NB_FILES = len(glob.glob(DATASET_FILEPATH + "prime_csv/*.csv"))
    counter = 0
    steps = int(NB_FILES*0.01)
    for filename in glob.glob(DATASET_FILEPATH+"prime_csv/*.csv"):
        seq_temp = csv_to_notes(filename)
        # 0) Transform seq_temp so it has correct durations
        _,onsets,_,_ = parse_midi(seq_temp)
        diff_onsets = onsets[1:] - onsets[:len(onsets)-1]
        notes = list()
        # write current notes, each note ends when the next note starts
        for i in range(len(seq_temp)-1):
            note = seq_temp[i]
            notes.append(pretty_midi.Note(velocity=note.velocity,pitch=note.pitch,start=note.start,end=seq_temp[i+1].start))
        # special case for last note, as there isn't a next note
        last_note = seq_temp[len(seq_temp)-1]
        notes.append(pretty_midi.Note(velocity=last_note.velocity,pitch=last_note.pitch,start=last_note.start,end=last_note.start + find_closest(diff_onsets,last_note.get_duration())))

        tuples = midi_notes_to_tuples(seq_temp)

        # 1) Transform sequence of notes into sequence of patterns 
        list_patterns,pattern_to_indices,trans_vectors = find_all_patterns(tuples)
        collapsed = collapse_pattern_to_indices(trans_vectors)
        true_indices = transform_collapsed_and_indices(collapsed,pattern_to_indices)
        seq = transform_back_into_seq(true_indices)
        mm1 = markov_model_first_order(seq,with_smoothing,probability_known_states)
        # 2) Generate next patterns
        for i in range(NB_ITERATIONS):
            last_pattern = seq[len(seq)-1]
            next_pattern = random.choices(list(mm1[last_pattern].keys()),weights=mm1[last_pattern].values())[0]
            seq.append(next_pattern)
        # 3) Transform back into notes
        # need to use collapsed, and list of patterns and seq
        notes_to_write = list()
        # need index first pattern and length of pattern
        # special case for the first pattern
        first_pattern = notes[true_indices[seq[0]][0]:true_indices[seq[0]][0]+len(list_patterns[collapsed[seq[0]][0]])]
        first_note = first_pattern[0]
        notes_to_write.append(first_note)
        for i in range(1,len(first_pattern)):
            current_note = first_pattern[i]
            previous_note = notes_to_write[len(notes_to_write)-1]
            new_note = pretty_midi.Note(velocity=current_note.velocity,pitch=current_note.pitch,start=previous_note.end,end=previous_note.end+current_note.get_duration())
            notes_to_write.append(new_note)
        for i in range(1,len(seq)):
            current_pattern = notes[true_indices[seq[i]][0]:true_indices[seq[i]][0]+len(list_patterns[collapsed[seq[i]][0]])]
            for j in range(len(current_pattern)):
                current_note = current_pattern[j]
                previous_note = notes_to_write[len(notes_to_write)-1]
                new_note = pretty_midi.Note(velocity=current_note.velocity,pitch=current_note.pitch, start = previous_note.end,end=previous_note.end + current_note.get_duration())
                notes_to_write.append(new_note)
        # 4) Write results
        result = pretty_midi.PrettyMIDI()
        result_program = pretty_midi.instrument_name_to_program("Acoustic Grand Piano")
        result_instrument = pretty_midi.Instrument(program=result_program)
        result_instrument.notes = notes_to_write#[len(seq_temp):]
        result.instruments.append(result_instrument)
        filename = filename.split("/")
        filename = filename[len(filename)-1]
        result.write(DATASET_FILEPATH + "markov_with_non_exact_prediction_midi/" + filename[:len(filename)-3] + "mid")
        # 5) write result into csv file
        midi_to_csv(notes_to_write[len(seq_temp):],DATASET_FILEPATH + "markov_with_non_exact_prediction_csv/" + filename)
        counter+=1
        if steps!=0 and counter%steps==0:
            print("\rProgress: " + str(counter/steps) + "%",end='')
#generate_prediction_with_translation_based_for_dataset('../Datasets/PPDD-Sep2018_sym_mono_small/')
