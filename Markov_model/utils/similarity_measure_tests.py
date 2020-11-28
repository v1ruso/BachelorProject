import unittest
import numpy as np
from similarity_measure import similarity_score
from similarity_measure import biggest_substring
from similarity_measure import biggest_submelody
from similarity_measure import count_substring_in_string
from similarity_measure import find_all_occurrences_and_indexes
from similarity_measure import first_order_markov_from_patterns
import pretty_midi
from midi_transform import parse_midi
class SimilarityMeasureTest(unittest.TestCase):
    """def test_similarity_score_works_for_same_length(self):
        seq_main = np.array([0,1,2,3,4,5])
        seq_compared = np.array([0,1,2,3,4,5])
        self.assertEqual(similarity_score(seq_main,seq_compared),1.0)
        seq_main = np.array([1,1,2])
        seq_compared = np.array([0,1,2])
        self.assertAlmostEqual(similarity_score(seq_main,seq_compared),0.86602540378)
    """
    def test_similarity_score_for_different_lengths(self):
        seq_main = np.array([1,1])
        seq_compared = np.array([1,1,0])
        self.assertEqual(similarity_score(seq_main,seq_compared),1.0)
        
        seq_main = np.array([1,1,0])
        seq_compared = np.array([1,1])
        self.assertEqual(similarity_score(seq_main,seq_compared),2.0/3)
        
        seq_main = np.array([0,1,2,3])
        seq_compared = np.array([2,1,2])
        self.assertEqual(similarity_score(seq_main,seq_compared),1.0/2)
        
        seq_main = np.array([0,1,2,3])
        seq_compared = np.array([1,2,3])
        self.assertEqual(similarity_score(seq_main,seq_compared),3.0/4)
    def test_biggest_subset(self):
        seq_main = np.array([1,1])
        seq_compared = np.array([1,1,0])
        for pair in zip(biggest_substring(seq_main,seq_compared), np.array([1,1])):
            self.assertEqual(pair[0], pair[1])
        
        seq_main = np.array([1,1,0])
        seq_compared = np.array([1,1])
        for pair in zip(biggest_substring(seq_main,seq_compared), np.array([1,1])):
            self.assertEqual(pair[0], pair[1])
        
        seq_main = np.array([0,1,2,3])
        seq_compared = np.array([2,1,2])
        for pair in zip(biggest_substring(seq_main,seq_compared), np.array([1,2])):
            self.assertEqual(pair[0], pair[1])
        
        seq_main = np.array([0,1,2,3])
        seq_compared = np.array([1,2,3])
        for pair in zip(biggest_substring(seq_main,seq_compared), np.array([1,2,3])):
            self.assertEqual(pair[0], pair[1])

    def test_biggest_submelody(self):
        input_data_1 = pretty_midi.PrettyMIDI("../MIDI_samples/yankee_doodle.mid")
        seq_main = input_data_1.instruments[0].notes
        input_data_2 = pretty_midi.PrettyMIDI("../MIDI_samples/yankee_doodle_slower.mid")
        seq_compared = input_data_2.instruments[0].notes
        #print(biggest_submelody(seq_main,seq_compared))
        result = pretty_midi.PrettyMIDI()
        result_program = pretty_midi.instrument_name_to_program("Acoustic Grand Piano")
        result_instrument = pretty_midi.Instrument(program=result_program)
        result_instrument.notes = biggest_submelody(seq_main,seq_compared)
        result.instruments.append(result_instrument)
        result.write("../MIDI_samples/test_biggest_submelody.mid")

    def test_count_substring_in_string(self):
        string = "01234012321244324102340123"
        substring = "0123" 
        self.assertEqual(count_substring_in_string(substring,string),3)
        self.assertEqual(count_substring_in_string(substring+str(4),string),1)
    """
    def test_find_biggest_recurring_pattern(self):
        seq = np.array([0,1,2,3,4,1,2,3,0,1,2,4,0,1,2,3,4])
        for pair in zip(find_biggest_recurring_pattern(seq),np.array([0,1,2,3,4])):
            self.assertEqual(pair[0],pair[1])
    """
    def test_find_all_recurring_pattern(self):
        print("\n")
        seq = "0123"
        print(seq)
        list_patterns,list_indexes = find_all_occurrences_and_indexes(seq)
        print("Patterns:")
        print(list_patterns)

        print("\nIndexes")
        print(list_indexes)

        print(first_order_markov_from_patterns(seq,list_patterns,list_indexes))

    """
    def test_find_recurring_pattern_in_midi(self):
        input_data = pretty_midi.PrettyMIDI("../MIDI_samples/midi_sample_c_major.mid")
        pitches, onsets, velocities, durations = parse_midi(input_data.instruments[0].notes)
        for pair in zip(find_biggest_recurring_pattern(pitches),np.array([67,69,67,65,64,60])):
            self.assertEqual(pair[0],pair[1])
    """
if __name__ == '__main__':
    unittest.main()