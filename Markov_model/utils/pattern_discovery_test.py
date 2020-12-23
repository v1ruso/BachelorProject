import unittest
import numpy as np
import random
import pretty_midi
from midi_transform import markov_model_first_order
class PatternDiscoveryTest(unittest.TestCase):
    def test_find_biggest_recurring_pattern(self):
        input = pretty_midi.PrettyMIDI("midi_sample_c_major_cropped.mid")
        seq = input.instruments[0].notes
        result = pretty_midi.PrettyMIDI()
        notes = list()
        for n in seq:
            notes.append(n.pitch)
        print("MARKOV")
        mm1 = markov_model_first_order(notes)
        for n in mm1:
            print(str(n) + ": " + str(mm1[n]))
    """
    def test_find_occurrences_and_indexes(self):
        input = pretty_midi.PrettyMIDI("../MIDI_samples/midi_sample_c_major.mid")
        seq = input.instruments[0].notes
        # First pattern
        result = pretty_midi.PrettyMIDI()
        result_program = pretty_midi.instrument_name_to_program("Acoustic Grand Piano")
        result_instrument = pretty_midi.Instrument(program=result_program)
        notes,temp,indexes=find_occurrences_and_indexes(seq)
        for i in range(len(notes)):
            if notes[i]!=None:
                result_instrument.notes.append(notes[i])
        result.instruments.append(result_instrument)
        result.write("../MIDI_samples/test_occurrences_1.mid")

        # Second pattern
        result = pretty_midi.PrettyMIDI()
        result_program = pretty_midi.instrument_name_to_program("Acoustic Grand Piano")
        result_instrument = pretty_midi.Instrument(program=result_program)
        notes,temp,indexes = find_occurrences_and_indexes(notes)
        for i in range(len(notes)):
            if notes[i]!=None:
                result_instrument.notes.append(notes[i])
        result.instruments.append(result_instrument)
        result.write("../MIDI_samples/test_occurrences_2.mid")
    def test_find_all_recurring_pattern(self):
        input = pretty_midi.PrettyMIDI("../MIDI_samples/midi_sample_c_major.mid")
        seq = input.instruments[0].notes
        patterns,indexes = find_all_occurrences_and_indexes(seq)
        print("\nPatterns:")
        print(patterns)
        print("Indexes:")
        print(indexes)
    def test_first_order_markov_model(self):
        input = pretty_midi.PrettyMIDI("../MIDI_samples/midi_sample_c_major.mid")
        seq = input.instruments[0].notes
        markov,patterns,indexes,transformed_seq = first_order_markov_with_patterns(seq)
        print("\nPatterns:")
        print(patterns)
        print("\nIndexes:")
        print(indexes)
        print("\nMarkov:")
        print(markov)
        print("\nTransformed sequence")
        print(transformed_seq)

    def test_generate_continuation_with_patterns(self):
        input = pretty_midi.PrettyMIDI("../MIDI_samples/midi_sample_a_minor.mid")
        seq_temp = input.instruments[0].notes
        # 0) Transform seq_notes so it has correct durations
        # Statistic model with first order markov model
        pitches,onsets,velocities,durations = parse_midi(seq_temp)
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
        markov,patterns,indexes,transformed_seq = first_order_markov_with_patterns(seq)
        # 2) Generate next patterns
        nb_iterations = 7
        for i in range(nb_iterations):
            last_pattern = transformed_seq[len(transformed_seq)-1]
            next_pattern = random.choices(list(markov[last_pattern].keys()),weights=markov[last_pattern].values())[0]
            transformed_seq.append(next_pattern)

        print("\nGeneration:")
        print(transformed_seq)

        # 3) Generate back into notes
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

        # 4) write result
        result = pretty_midi.PrettyMIDI()
        result_program = pretty_midi.instrument_name_to_program("Acoustic Grand Piano")
        result_instrument = pretty_midi.Instrument(program=result_program)
        result_instrument.notes = notes
        result.instruments.append(result_instrument)
        result.write("../MIDI_samples/test_generation_with_pattern.mid")
        # 5) write result into csv file
        midi_to_csv(notes[len(seq_temp):],"../MIDI_samples/test_generation_with_pattern.csv")
"""
if __name__ == '__main__':
    unittest.main()