import random
import pretty_midi
import numpy as np
import glob
PITCHES_PER_OCTAVE = 12

# create database
pitch_array = np.zeros((12, 13), dtype=float)
for filename in glob.glob('PPDD-Sep2018_sym_mono_small/prime_midi/*.mid'):
    midi_data = pretty_midi.PrettyMIDI(filename)
    for instrument in midi_data.instruments:
        if not instrument.is_drum:
            last_note_pitch = instrument.notes[len(instrument.notes)-1].pitch%PITCHES_PER_OCTAVE
            for i in range(len(instrument.notes)-1):
                pitch_array[instrument.notes[i].pitch %
                            PITCHES_PER_OCTAVE][(instrument.notes[i+1].pitch-last_note_pitch) % PITCHES_PER_OCTAVE] += 1
                pitch_array[(instrument.notes[i].pitch-last_note_pitch) %
                            PITCHES_PER_OCTAVE][PITCHES_PER_OCTAVE] += 1
for i in range(PITCHES_PER_OCTAVE):
    if(pitch_array[i][PITCHES_PER_OCTAVE] != 0):
        for j in range(PITCHES_PER_OCTAVE):
            pitch_array[i][j] /= pitch_array[i][PITCHES_PER_OCTAVE]
# generate continuation from file
"""
filename = "frerejacques.mid"
input_data = pretty_midi.PrettyMIDI(filename)
result = pretty_midi.PrettyMIDI()
result_program = pretty_midi.instrument_name_to_program("Acoustic Grand Piano")
result_instrument = pretty_midi.Instrument(program=result_program)
for instrument in input_data.instruments:
    if not instrument.is_drum:
        for note in instrument.notes:
            result_instrument.notes.append(note)


nb_iterations = 100
for i in range(nb_iterations):
    last_note = result_instrument.notes[len(result_instrument.notes)-1]
    octave_last_note = 5*(PITCHES_PER_OCTAVE)
    duration = last_note.end-last_note.start
    new_note_pitch = random.choices(range(PITCHES_PER_OCTAVE),weights=pitch_array[last_note.pitch%PITCHES_PER_OCTAVE][0:PITCHES_PER_OCTAVE])[0]
    new_note = pretty_midi.Note(velocity=last_note.velocity,pitch=new_note_pitch+octave_last_note,start=last_note.start+0.5,end=last_note.end+0.5)
    result_instrument.notes.append(new_note)
print("Prediction calculated")
result.instruments.append(result_instrument)
result.write("generated_" + filename)
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
