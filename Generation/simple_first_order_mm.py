import random
import pretty_midi
import numpy as np
import glob
from utility import *

def generate_prediction_with_simple_markov(filename, notes_to_generate = 4,with_smoothing=False,probability_known_states=0.9):
    """
    filename: string of the filename to read, has to be a midi (.mid) file.
    notes_to_generate: the number of notes to generate in the continuation
    with_smoothing: default False. Whether the continuation should have additive smoothing or not.
    probability_known_patterns: only useful when with_smoothing is set to True. It is the probability assigned to known patterns,
    1 - probability_known_patterns will be the probilities assigned to unknown patterns. Needs to be between 0 and 1.
    """
    NB_ITERATIONS = notes_to_generate
    notes = pretty_midi.PrettyMIDI(filename).instruments[0].notes
    
    
    result = pretty_midi.PrettyMIDI()
    result_program = pretty_midi.instrument_name_to_program("Acoustic Grand Piano")
    result_instrument = pretty_midi.Instrument(program=result_program)

    # Statistic model with first order markov model
    pitches,onsets,velocities,durations = parse_midi(notes)

    # difference of onsets, will be used as durations
    diff_onsets = onsets[1:] - onsets[:len(onsets)-1]

    markov_pitches = markov_model_first_order(pitches,with_smoothing,probability_known_states)
    markov_velocities = markov_model_first_order(velocities,with_smoothing,probability_known_states)
    markov_diff_onsets = markov_model_first_order(diff_onsets,with_smoothing,probability_known_states)

    # write current notes, each note ends when the next note starts
    for i in range(len(notes)-1):
        note = notes[i]
        result_instrument.notes.append(pretty_midi.Note(velocity=note.velocity,pitch=note.pitch,start=note.start,end=notes[i+1].start))
    # special case for last note, as there isn't a next note
    last_note = notes[len(notes)-1]
    result_instrument.notes.append(pretty_midi.Note(velocity=last_note.velocity,pitch=last_note.pitch,start=last_note.start,end=last_note.start + find_closest(list(markov_diff_onsets.keys()),last_note.get_duration())))

    for i in range(NB_ITERATIONS):
        last_note = result_instrument.notes[len(result_instrument.notes)-1]
        #duration using difference of onsets
        diff_start = find_closest(list(markov_diff_onsets.keys()),last_note.get_duration())
        new_note_duration = random.choices(list(markov_diff_onsets[diff_start].keys()),weights=markov_diff_onsets[diff_start].values())[0]
        # velocity
        new_note_velocity = int(random.choices(list(markov_velocities[
            last_note.velocity].keys()),weights=markov_velocities[last_note.velocity].values())[0])
        # pitch
        new_note_pitch = int(random.choices(list(markov_pitches[
            last_note.pitch].keys()),weights=markov_pitches[last_note.pitch].values())[0])
        # new_note
        new_note = pretty_midi.Note(velocity=new_note_velocity,pitch=new_note_pitch,start=last_note.end,end=last_note.end+new_note_duration)

        # append note to result
        result_instrument.notes.append(new_note)
    result.instruments.append(result_instrument)
    # 4) Write results
    result.write(filename[:len(filename)-4] + "_result.mid")
    # 5) Show results using abjad
    show_notes(result_instrument.notes)


def generate_prediction_with_simple_markov_for_dataset(dataset_filepath, notes_to_generate = 30,with_smoothing=True,probability_known_states=0.9):
    """
    dataset_filepath: string of the dataset path to read from.
    notes_to_generate: the number of notes to generate in the continuation
    with_smoothing: default True. Whether the continuation should have additive smoothing or not.
    probability_known_patterns: only useful when with_smoothing is set to True. It is the probability assigned to known patterns,
    1 - probability_known_patterns will be the probilities assigned to unknown patterns. Needs to be between 0 and 1.
    """
    nb_iterations = notes_to_generate
    counter = 0
    nb_files = len(glob.glob(dataset_filepath + "prime_csv/*.csv"))
    steps = int(nb_files*0.01)
    print()
    for filename in glob.glob(dataset_filepath + "prime_csv/*.csv"):
        notes = csv_to_notes(filename)
    
        if len(notes) > 0:
            result = pretty_midi.PrettyMIDI()
            result_program = pretty_midi.instrument_name_to_program("Acoustic Grand Piano")
            result_instrument = pretty_midi.Instrument(program=result_program)

            # Statistic model with first order markov model
            pitches,onsets,velocities,_ = parse_midi(notes)

            # difference of onsets, will be used as durations
            diff_onsets = onsets[1:] - onsets[:len(onsets)-1]

            markov_pitches = markov_model_first_order(pitches,with_smoothing,probability_known_states)
            markov_velocities = markov_model_first_order(velocities,with_smoothing,probability_known_states)
            markov_diff_onsets = markov_model_first_order(diff_onsets,with_smoothing,probability_known_states)

            # write current notes, each note ends when the next note starts
            for i in range(len(notes)-1):
                note = notes[i]
                result_instrument.notes.append(pretty_midi.Note(velocity=note.velocity,pitch=note.pitch,start=note.start,end=notes[i+1].start))
            # special case for last note, as there isn't a next note
            last_note = notes[len(notes)-1]
            result_instrument.notes.append(pretty_midi.Note(velocity=last_note.velocity,pitch=last_note.pitch,start=last_note.start,end=last_note.start + find_closest(list(markov_diff_onsets.keys()),last_note.get_duration())))

            csv_output_file = ""
            for i in range(nb_iterations):
                last_note = result_instrument.notes[len(result_instrument.notes)-1]
                #duration using difference of onsets
                diff_start = find_closest(list(markov_diff_onsets.keys()),last_note.get_duration())
                new_note_duration = random.choices(list(markov_diff_onsets[diff_start].keys()),weights=markov_diff_onsets[diff_start].values())[0]
                # velocity
                new_note_velocity = int(random.choices(list(markov_velocities[
                    last_note.velocity].keys()),weights=markov_velocities[last_note.velocity].values())[0])
                # pitch
                new_note_pitch = int(random.choices(list(markov_pitches[
                    last_note.pitch].keys()),weights=markov_pitches[last_note.pitch].values())[0])
                # new_note
                new_note = pretty_midi.Note(velocity=new_note_velocity,pitch=new_note_pitch,start=last_note.end,end=last_note.end+new_note_duration)

                # write onto csv, each line like: start,pitch,morph_pitch,duration,channel\n
                # morph pitch == pitch here. It is unused, as well as the channel
                csv_output_file += str(last_note.end) + "," + str(new_note_pitch) + "," + str(new_note_pitch) + "," + str(new_note_duration) + "," + str(4) + "\n"

                # append note to result
                result_instrument.notes.append(new_note)
            result.instruments.append(result_instrument)
            filename = filename.split("/")
            filename = filename[len(filename)-1]
            result.write(dataset_filepath + "markov_without_prediction_midi/" + filename[:len(filename)-3] + "mid")
            file = open(dataset_filepath + "markov_without_prediction_csv/" + filename, "w")
            file.write(csv_output_file)
            file.close()
        counter+=1
        if counter%steps==0:
            print("\033[A\033[A")
            print("\rProgress: " + str(counter/steps) + "%")
#generate_prediction_with_simple_markov_for_dataset('../Datasets/PPDD-Sep2018_sym_mono_small/')
