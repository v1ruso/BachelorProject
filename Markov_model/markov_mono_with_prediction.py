import random
import pretty_midi
import numpy as np
import glob
from utils.midi_transform import parse_midi
from utils.midi_transform import markov_model_first_order
from utils.midi_transform import find_closest
from utils.midi_transform import midi_to_csv
from utils.pattern_discovery import first_order_markov_with_patterns
DATASET_FILEPATH = '../Datasets/PPDD-Sep2018_sym_mono_small/'
NB_ITERATIONS = 40

for filename in glob.glob(DATASET_FILEPATH + "prime_midi/*.mid"):
    input_data = pretty_midi.PrettyMIDI(filename)
    seq_temp = input_data.instruments[0].notes

    # 0) Transform seq_notes so it has correct durations
    # Statistic model with first order markov model
    _,onsets,_,_ = parse_midi(seq_temp)
    diff_onsets = onsets[1:] - onsets[:len(onsets)-1]
    markov_diff_onsets = markov_model_first_order(diff_onsets)
    seq = list()
    # write current notes, each note ends when the next note starts
    for i in range(len(seq_temp)-1):
        note = seq_temp[i]
        seq.append(pretty_midi.Note(velocity=note.velocity,pitch=note.pitch,start=note.start,end=seq_temp[i+1].start))
    # special case for last note, as there isn't a next note
    last_note = seq_temp[len(seq_temp)-1]
    seq.append(pretty_midi.Note(velocity=last_note.velocity,pitch=last_note.pitch,start=last_note.start,end=last_note.start + find_closest(list(markov_diff_onsets.keys()),last_note.get_duration())))
  
    # 1) Transform sequence of notes into sequence of patterns
    markov,patterns,_,transformed_seq = first_order_markov_with_patterns(seq)
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
    result_instrument.notes = notes
    result.instruments.append(result_instrument)
    filename = filename.split("/")
    filename = filename[len(filename)-1]
    result.write(DATASET_FILEPATH + "markov_with_prediction_midi/" + filename)
    # 5) write result into csv file
    midi_to_csv(notes[len(seq_temp):],DATASET_FILEPATH + "markov_with_prediction_csv/" + filename[:len(filename)-3] + "csv")