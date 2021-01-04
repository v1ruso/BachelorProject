import random
import pretty_midi
import numpy as np
import glob
from utility import *

def is_note_equal(this,that):
    """
    this: pretty_midi Note
    that: pretty_midi Note
    """
    if this==None or that==None:
        return False
    return this.pitch == that.pitch and this.get_duration() == that.get_duration()

def find_biggest_recurring_pattern(seq):
    """
    seq: array-like of pretty_midi Note.
    
    Returns the biggest pattern (sublist of notes) that appears at least twice, as well as the index of its first appearance in "seq".
    """
    A = np.zeros((len(seq)+1,len(seq)+1),dtype=int)
    res = list()
    res_length = 0
    index = 0
    for i in range(1,len(seq)+1):
        for j in range(i+1,len(seq)+1):
            if seq[i-1]!=None and seq[j-1]!=None and is_note_equal(seq[i-1],seq[j-1]) and (j-i) > A[i-1][j-1]:
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
    seq: array-like of pretty_midi Note
    
    Returns the sequence of notes with the biggest pattern removed, the biggest recurring pattern, and the indexes of each occurrence of that pattern.
    """
    res, index_first_occurrence = find_biggest_recurring_pattern(seq)
    if len(res)==0:
        return seq, None, list()
    temp_seq = seq[0:index_first_occurrence]
    i = index_first_occurrence
    index_occurrences = list()
    while i < len(seq):
        is_start = False
        if is_note_equal(seq[i],res[0]):
            is_start = True
            for j in range(len(res)):
                if i + j >= len(seq) or not is_note_equal(seq[i+j],res[j]):
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
    seq: array-like of pretty_midi Note
    
    Finds all patterns and indexes of those patterns.
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

def first_order_markov_with_patterns(seq,with_smoothing=False,probability_known_patterns=0.9):
    """
    seq: array-like of pretty_midi Note.
    
    Returns a first-order Markov model of the patterns found in the sequence of note,
        the list of patterns, the list of indexes, and a transformation of notes->patterns.
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
    return markov_model_first_order(pattern_indexes_seq,with_smoothing,probability_known_patterns),list_patterns,list_indexes,pattern_indexes_seq

def generate_prediction_with_string_based(filename, patterns_to_generate = 4,with_smoothing=False,probability_known_patterns=0.9):
    """
    filename: string of the filename to read, has to be a midi (.mid) file.

    """
    NB_ITERATIONS = patterns_to_generate
    seq_temp = pretty_midi.PrettyMIDI(filename).instruments[0].notes
    
    # 0) Transform seq_notes so it has correct durations
    # Statistic model with first order markov model
    _,onsets,_,_ = parse_midi(seq_temp)
    diff_onsets = onsets[1:] - onsets[:len(onsets)-1]
    seq = list()
    # write current notes, each note ends when the next note starts
    for i in range(len(seq_temp)-1):
        note = seq_temp[i]
        seq.append(pretty_midi.Note(velocity=note.velocity,pitch=note.pitch,start=note.start,end=seq_temp[i+1].start))
    # special case for last note, as there isn't a next note
    last_note = seq_temp[len(seq_temp)-1]
    seq.append(pretty_midi.Note(velocity=last_note.velocity,pitch=last_note.pitch,start=last_note.start,end=last_note.start + find_closest(diff_onsets,last_note.get_duration())))
  
    # 1) Transform sequence of notes into sequence of patterns
    markov,patterns,_,transformed_seq = first_order_markov_with_patterns(seq,with_smoothing,probability_known_patterns)
    # 2) Generate next patterns
    for i in range(NB_ITERATIONS):
        last_pattern = transformed_seq[len(transformed_seq)-1]
        next_pattern = random.choices(list(markov[last_pattern].keys()),weights=markov[last_pattern].values())[0]
        transformed_seq.append(next_pattern)
    
    # 3) Transform back into notes
    notes = list()
    # special case for first pattern
    first_pattern = patterns[transformed_seq[0]]
    first_note = first_pattern[0]
    notes.append(first_note)
    for i in range(1,len(first_pattern)):
        current_note = first_pattern[i]
        previous_note = notes[len(notes)-1]
        new_note = pretty_midi.Note(velocity=current_note.velocity,pitch=current_note.pitch,start=previous_note.end,end=previous_note.end+current_note.get_duration())
        notes.append(new_note)
    for i in range(1,len(transformed_seq)):
        current_pattern = patterns[transformed_seq[i]]
        for j in range(len(current_pattern)):
            current_note = current_pattern[j]
            previous_note = notes[len(notes)-1]
            new_note = pretty_midi.Note(velocity=current_note.velocity,pitch=current_note.pitch, start = previous_note.end,end=previous_note.end + current_note.get_duration())
            notes.append(new_note)
    # 4) Write results
    result = pretty_midi.PrettyMIDI()
    result_program = pretty_midi.instrument_name_to_program("Acoustic Grand Piano")
    result_instrument = pretty_midi.Instrument(program=result_program)
    result_instrument.notes = notes#[len(seq_temp):]
    result.instruments.append(result_instrument)
    result.write(filename[:len(filename)-4] + "_result.mid")
    # 5) Show results using abjad
    show_notes(result_instrument.notes)

def generate_prediction_with_string_based_for_dataset(dataset_filepath, patterns_to_generate = 20,with_smoothing=True,probability_known_states=0.9):
    DATASET_FILEPATH = dataset_filepath
    NB_ITERATIONS = patterns_to_generate
    NB_FILES = len(glob.glob(DATASET_FILEPATH + "prime_csv/*.csv"))
    counter = 0
    steps = int(NB_FILES*0.01)
    print()
    for filename in glob.glob(DATASET_FILEPATH + "prime_csv/*.csv"):
        seq_temp = csv_to_notes(filename)
        
        # 0) Transform seq_notes so it has correct durations
        # Statistic model with first order markov model
        _,onsets,_,_ = parse_midi(seq_temp)
        diff_onsets = onsets[1:] - onsets[:len(onsets)-1]
        seq = list()
        # write current notes, each note ends when the next note starts
        for i in range(len(seq_temp)-1):
            note = seq_temp[i]
            seq.append(pretty_midi.Note(velocity=note.velocity,pitch=note.pitch,start=note.start,end=seq_temp[i+1].start))
        # special case for last note, as there isn't a next note
        last_note = seq_temp[len(seq_temp)-1]
        seq.append(pretty_midi.Note(velocity=last_note.velocity,pitch=last_note.pitch,start=last_note.start,end=last_note.start + find_closest(diff_onsets,last_note.get_duration())))
    
        # 1) Transform sequence of notes into sequence of patterns
        markov,patterns,_,transformed_seq = first_order_markov_with_patterns(seq,with_smoothing,probability_known_states)
        # 2) Generate next patterns
        for i in range(NB_ITERATIONS):
            last_pattern = transformed_seq[len(transformed_seq)-1]
            next_pattern = random.choices(list(markov[last_pattern].keys()),weights=markov[last_pattern].values())[0]
            transformed_seq.append(next_pattern)
        
        # 3) Transform back into notes
        notes = list()
        # special case for first pattern
        first_pattern = patterns[transformed_seq[0]]
        first_note = first_pattern[0]
        notes.append(first_note)
        for i in range(1,len(first_pattern)):
            current_note = first_pattern[i]
            previous_note = notes[len(notes)-1]
            new_note = pretty_midi.Note(velocity=current_note.velocity,pitch=current_note.pitch,start=previous_note.end,end=previous_note.end+current_note.get_duration())
            notes.append(new_note)
        for i in range(1,len(transformed_seq)):
            current_pattern = patterns[transformed_seq[i]]
            for j in range(len(current_pattern)):
                current_note = current_pattern[j]
                previous_note = notes[len(notes)-1]
                new_note = pretty_midi.Note(velocity=current_note.velocity,pitch=current_note.pitch, start = previous_note.end,end=previous_note.end + current_note.get_duration())
                notes.append(new_note)
        # 4) Write results
        result = pretty_midi.PrettyMIDI()
        result_program = pretty_midi.instrument_name_to_program("Acoustic Grand Piano")
        result_instrument = pretty_midi.Instrument(program=result_program)
        result_instrument.notes = notes#[len(seq_temp):]
        result.instruments.append(result_instrument)
        filename = filename.split("/")
        filename = filename[len(filename)-1]
        result.write(DATASET_FILEPATH + "markov_with_prediction_midi/" + filename[:len(filename)-3] + "mid")
        # 5) write result into csv file
        midi_to_csv(notes[len(seq_temp):],DATASET_FILEPATH + "markov_with_prediction_csv/" + filename)
        counter+=1
        if counter%steps==0:
            print("\033[A\033[A")
            print("Progress: " + str(counter/steps) + "%")
#generate_prediction_with_string_based_for_dataset('../Datasets/PPDD-Sep2018_sym_mono_small/')