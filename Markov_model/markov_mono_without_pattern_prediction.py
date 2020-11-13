import random

from numpy.core.fromnumeric import reshape
import pretty_midi
import numpy as np
import glob
NUMBER_OF_PITCHES = 128
DATASET_FILEPATH = '../Datasets/PPDD-Sep2018_sym_mono_large/'
"""
# create database
pitch_array = np.zeros((NUMBER_OF_PITCHES, NUMBER_OF_PITCHES+1), dtype=float)
for filename in glob.glob('PPDD-Sep2018_sym_mono_large/cont_true_midi/*.mid'):
    midi_data = pretty_midi.PrettyMIDI(filename)
    for instrument in midi_data.instruments:
        if not instrument.is_drum:
            for i in range(len(instrument.notes)-1):
                #pitches
                pitch_array[instrument.notes[i].pitch][instrument.notes[i+1].pitch] += 1
                pitch_array[instrument.notes[i].pitch][NUMBER_OF_PITCHES] += 1
#normalize
for i in range(NUMBER_OF_PITCHES):
    if pitch_array[i][NUMBER_OF_PITCHES] != 0:
        for j in range(NUMBER_OF_PITCHES):
            pitch_array[i][j] /= pitch_array[i][NUMBER_OF_PITCHES]
# save database into file
pitch_database = open("pitch_array.txt","w")
for e in pitch_array:
    np.savetxt(pitch_database,e)
pitch_database.close()
"""
# if database already generated
pitch_array = np.loadtxt("pitch_mono_without_prediction.txt").reshape((NUMBER_OF_PITCHES,NUMBER_OF_PITCHES+1))

for filename in glob.glob(DATASET_FILEPATH + 'prime_midi/*.mid'):
    # generate continuation from file
    input_data = pretty_midi.PrettyMIDI(filename)
    result = pretty_midi.PrettyMIDI()
    result_program = pretty_midi.instrument_name_to_program("Acoustic Grand Piano")
    result_instrument = pretty_midi.Instrument(program=result_program)
    duration_dict = {}
    velocity_dict = {}
    time_between_notes = {}
    # set up prime notes
    number_of_notes = 0
    for instrument in input_data.instruments:
        if not instrument.is_drum:
            number_of_notes+=len(instrument.notes)
            for note in instrument.notes:
                result_instrument.notes.append(note)
                # duration
                if note.get_duration() in duration_dict:
                    duration_dict[note.get_duration()] += 1
                else:
                    duration_dict[note.get_duration()] = 1
                # velocity
                if note.velocity in velocity_dict:
                    velocity_dict[note.velocity] += 1
                else:
                    velocity_dict[note.velocity] = 1
            for i in range(len(instrument.notes)-1):
                diff_between_starts = instrument.notes[i+1].start - instrument.notes[i].start
                if diff_between_starts in time_between_notes:
                    time_between_notes[diff_between_starts] += 1
                else:
                    time_between_notes[diff_between_starts] = 1

    csv_output_file = ""
    if number_of_notes > 1:    
        for d in duration_dict.keys():
            duration_dict[d] /= number_of_notes
        for v in velocity_dict.keys():
            velocity_dict[v] /= number_of_notes
        for t in time_between_notes.keys():
            time_between_notes[t] /= (number_of_notes-1)
        nb_iterations = 100
        for i in range(nb_iterations):
            last_note = result_instrument.notes[len(result_instrument.notes)-1]
            new_note_duration = random.choices(list(duration_dict.keys()),weights=duration_dict.values())[0]
            new_note_velocity = int(random.choices(list(velocity_dict.keys()),weights=velocity_dict.values())[0])
            new_note_pitch = random.choices(range(NUMBER_OF_PITCHES),weights=pitch_array[last_note.pitch][0:NUMBER_OF_PITCHES])[0]
            new_note_start = last_note.start + random.choices(list(time_between_notes.keys()),weights=time_between_notes.values())[0]
            new_note = pretty_midi.Note(velocity=new_note_velocity,pitch=new_note_pitch,start=new_note_start, end=new_note_start+new_note_duration)
            csv_output_file+=str(new_note_start) + "," + str(new_note_pitch) + "," + str(new_note_pitch-6) + "," + str(new_note_duration) + "," +  str(4) + "\n"
            result_instrument.notes.append(new_note)
    result.instruments.append(result_instrument)
    filename = filename.split("/")
    filename = filename[len(filename)-1]
    result.write(DATASET_FILEPATH + "out/" + filename)
    file = open(DATASET_FILEPATH + "out_csv/" + filename[:len(filename)-3] + "csv", "w")
    file.write(csv_output_file)
    file.close()
"""
# generate from empty file
result = pretty_midi.PrettyMIDI()
result_program = pretty_midi.instrument_name_to_program("Acoustic Grand Piano")
result_instrument = pretty_midi.Instrument(program=result_program)
first_note_pitch = pretty_midi.note_name_to_number('C4')
first_note = pretty_midi.Note(
    velocity=100, pitch=first_note_pitch, start=0, end=0.5)
result_instrument.notes.append(first_note)
nb_iterations = 100
for i in range(nb_iterations):
    last_note = result_instrument.notes[len(result_instrument.notes)-1]
    octave_last_note = 5*(PITCHES_PER_OCTAVE)
    duration = last_note.end-last_note.start
    new_note_pitch = random.choices(range(
        PITCHES_PER_OCTAVE), weights=pitch_array[last_note.pitch % PITCHES_PER_OCTAVE][0:PITCHES_PER_OCTAVE])[0]
    new_note = pretty_midi.Note(velocity=last_note.velocity, pitch=new_note_pitch +
                                octave_last_note, start=last_note.start+0.5, end=last_note.end+0.5)
    result_instrument.notes.append(new_note)
print("Generation calculated")
result.instruments.append(result_instrument)
result.write("generated_sample.mid")
"""