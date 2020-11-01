import pretty_midi
import numpy as np

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

# Load MIDI file into PrettyMIDI object
midi_data = pretty_midi.PrettyMIDI('mz_331_3.mid')
# Print an empirical estimate of its global tempo
# print(midi_data.estimate_tempo())
# Compute the relative amount of each semitone across the entire song, a proxy for key
total_velocity = sum(sum(midi_data.get_chroma()))
# print([sum(semitone)/total_velocity for semitone in midi_data.get_chroma()])
# Shift all notes up by 5 semitones
# Create result with only on beat notes
result_chord = pretty_midi.PrettyMIDI()
result_program = pretty_midi.instrument_name_to_program("Acoustic Grand Piano")
result = pretty_midi.Instrument(program=result_program)
count = 0
beats = midi_data.get_beats()
for instrument in midi_data.instruments:
    # Don't want to shift drum notes
    if not instrument.is_drum:
        for note in instrument.notes:
            temp_note = pretty_midi.Note(velocity=note.velocity,pitch=note.pitch,start=note.start,end=note.end)
            closest_start = find_nearest(beats,temp_note.start)
            if abs(temp_note.start-closest_start)<0.001:
                result.notes.append(temp_note)
            count+=1
            note.pitch -= 5

# Synthesize the resulting MIDI data using sine waves
#audio_data = midi_data.synthesize()
print("There are "+ str(count) + " notes")
midi_data.write("result.mid")
result_chord.instruments.append(result)
result_chord.write("on_beats.mid")
"""
import pretty_midi
# Create a PrettyMIDI object
cello_c_chord = pretty_midi.PrettyMIDI()
# Create an Instrument instance for a cello instrument
cello_program = pretty_midi.instrument_name_to_program('Cello')
cello = pretty_midi.Instrument(program=cello_program)
# Iterate over note names, which will be converted to note number later
for note_name in ['C5', 'E5', 'G5']:
    # Retrieve the MIDI note number for this note name
    note_number = pretty_midi.note_name_to_number(note_name)
    # Create a Note instance for this note, starting at 0s and ending at .5s
    note = pretty_midi.Note(velocity=100, pitch=note_number, start=0, end=.5)
    # Add it to our cello instrument
    cello.notes.append(note)
# Add the cello instrument to the PrettyMIDI object
cello_c_chord.instruments.append(cello)
# Write out the MIDI data
cello_c_chord.write('cello-C-chord.mid')"""