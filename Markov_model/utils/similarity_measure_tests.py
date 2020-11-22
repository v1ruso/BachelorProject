import unittest
import numpy as np
from similarity_measure import similarity_score
from similarity_measure import biggest_substring
from similarity_measure import biggest_submelody
from similarity_measure import count_substring_in_string
from similarity_measure import find_biggest_recurring_pattern
import pretty_midi
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
        input_data_2 = pretty_midi.PrettyMIDI("../MIDI_samples/midi_sample_a_minor.mid")
        seq_compared = input_data_2.instruments[0].notes
        biggest_submelody(seq_main,seq_compared)

    def test_count_substring_in_string(self):
        string = "01234012321244324102340123"
        substring = "0123" 
        self.assertEqual(count_substring_in_string(substring,string),3)
        self.assertEqual(count_substring_in_string(substring+str(4),string),1)

    def test_find_biggest_recurring_pattern(self):
        seq = np.array([0,1,2,3,4,1,2,3,0,1,2,4,0,1,2,3,4])
        print(find_biggest_recurring_pattern(seq))
if __name__ == '__main__':
    unittest.main()