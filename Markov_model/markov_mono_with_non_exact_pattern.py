import random
import pretty_midi
import glob
from utils.midi_transform import parse_midi
from utils.midi_transform import find_closest
from utils.midi_transform import midi_to_csv
from utils.midi_transform import csv_to_notes
from utils.midi_transform import markov_model_first_order
from utils.approximate_patterns_discovery import find_all_patterns
from utils.approximate_patterns_discovery import collapse_pattern_to_indices
from utils.approximate_patterns_discovery import transform_collapsed_and_indices
from utils.approximate_patterns_discovery import transform_back_into_seq
from utils.approximate_patterns_discovery import midi_notes_to_tuples

DATASET_FILEPATH = '../Datasets/PPDD-Sep2018_sym_mono_large/'
NB_ITERATIONS = 20
NB_FILES = len(glob.glob(DATASET_FILEPATH + "prime_csv/*.csv"))
counter = 0
steps = int(NB_FILES*0.01)
print()
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
    mm1 = markov_model_first_order(seq)
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
    result_instrument.notes = notes_to_write[len(seq_temp):]
    result.instruments.append(result_instrument)
    filename = filename.split("/")
    filename = filename[len(filename)-1]
    result.write(DATASET_FILEPATH + "markov_with_non_exact_prediction_midi/" + filename[:len(filename)-3] + "mid")
    # 5) write result into csv file
    midi_to_csv(notes_to_write[len(seq_temp):],DATASET_FILEPATH + "markov_with_non_exact_prediction_csv/" + filename)
    counter+=1
    if counter%steps==0:
        print("\033[A\033[A")
        print("Progress: " + str(counter/steps) + "%")