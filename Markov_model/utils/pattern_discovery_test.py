import unittest
import numpy as np
import random
import pretty_midi
from midi_transform import parse_midi
from pattern_discovery import find_biggest_recurring_pattern
from pattern_discovery import find_occurrences_and_indexes
from pattern_discovery import find_all_occurrences_and_indexes
from pattern_discovery import first_order_markov_with_patterns
class PatternDiscoveryTest(unittest.TestCase):
    def test_find_biggest_recurring_pattern(self):
        input = pretty_midi.PrettyMIDI("../MIDI_samples/midi_sample_c_major.mid")
        seq = input.instruments[0].notes
        result = pretty_midi.PrettyMIDI()
        result_program = pretty_midi.instrument_name_to_program("Acoustic Grand Piano")
        result_instrument = pretty_midi.Instrument(program=result_program)
        result_instrument.notes,index = find_biggest_recurring_pattern(seq)
        result.instruments.append(result_instrument)
        result.write("../MIDI_samples/test_biggest_recurring_pattern.mid")

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
    """
    def test_find_all_recurring_pattern(self):
        input = pretty_midi.PrettyMIDI("../MIDI_samples/midi_sample_c_major.mid")
        seq = input.instruments[0].notes
        patterns,indexes = find_all_occurrences_and_indexes(seq)
        print("\nPatterns:")
        print(patterns)
        print("Indexes:")
        print(indexes)
    """
    """def test_first_order_markov_model(self):
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
        print(transformed_seq)"""

    def test_generate_continuation_with_patterns(self):
        input = pretty_midi.PrettyMIDI("../MIDI_samples/midi_sample_c_major.mid")
        seq = input.instruments[0].notes
        # 1) Transform sequence of notes into sequence of patterns
        markov,patterns,indexes,transformed_seq = first_order_markov_with_patterns(seq)
        
        # 2) Generate next patterns
        nb_iterations = 4
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

if __name__ == '__main__':
    unittest.main()