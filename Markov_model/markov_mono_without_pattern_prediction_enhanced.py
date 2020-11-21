import random
import pretty_midi
import numpy as np
import glob
from utils.midi_transform import parse_midi
from utils.midi_transform import markov_model_first_order
NUMBER_OF_PITCHES = 128
DATASET_FILEPATH = '../Datasets/PPDD-Sep2018_sym_mono_small/'
NB_ITERATIONS = 100
ROUND_DURATIONS_DECIMALS = 8

for filename in glob.glob(DATASET_FILEPATH + "prime_midi/*.mid"):
    input_data = pretty_midi.PrettyMIDI(filename)
    result = pretty_midi.PrettyMIDI()
    result_program = pretty_midi.instrument_name_to_program("Acoustic Grand Piano")
    result_instrument = pretty_midi.Instrument(program=result_program)

    # Assume monophonic
    notes = input_data.instruments[0].notes
    if len(notes) > 0:
        # First write current notes
        for note in notes:
            result_instrument.notes.append(note)
        
        # Statistic model with first order markov model
        pitches,onsets,velocities,durations = parse_midi(notes,round_durations=ROUND_DURATIONS_DECIMALS)

        markov_pitches = markov_model_first_order(pitches)
        markov_velocities = markov_model_first_order(velocities)
        markov_durations = markov_model_first_order(durations)
        csv_output_file = ""
        for i in range(NB_ITERATIONS):
            last_note = result_instrument.notes[len(result_instrument.notes)-1]
            #duration
            rounded_duration = round(last_note.get_duration(),ROUND_DURATIONS_DECIMALS)
            new_note_duration = random.choices(list(markov_durations[rounded_duration].keys()),weights=markov_durations[rounded_duration].values())[0]
            # velocity
            new_note_velocity = int(random.choices(list(markov_velocities[
                last_note.velocity].keys()),weights=markov_velocities[last_note.velocity].values())[0])
            # pitch
            new_note_pitch = int(random.choices(list(markov_pitches[
                last_note.pitch].keys()),weights=markov_pitches[last_note.pitch].values())[0])
            # new_note
            new_note = pretty_midi.Note(velocity=new_note_velocity,pitch=new_note_pitch,start=last_note.end,end=last_note.end+new_note_duration)

            # write onto csv, each line like: start,pitch,morph_pitch,duration,channel\n
            # morph pitch == pitch here. It is unused
            csv_output_file += str(last_note.end) + "," + str(new_note_pitch) + "," + str(new_note_pitch) + "," + str(new_note_duration) + "," + str(4) + "\n"

            # append note to result
            result_instrument.notes.append(new_note)
        result.instruments.append(result_instrument)
        filename = filename.split("/")
        filename = filename[len(filename)-1]
        result.write(DATASET_FILEPATH + "out_midi/" + filename)
        file = open(DATASET_FILEPATH + "out_csv/" + filename[:len(filename)-3] + "csv", "w")
        file.write(csv_output_file)
        file.close()
