import unittest
from approximate_patterns_discovery import hamming_distance
from approximate_patterns_discovery import edit_distance
from approximate_patterns_discovery import find_all_patterns
from approximate_patterns_discovery import collapse_pattern_to_indices
from approximate_patterns_discovery import transform_collapsed_and_indices
from approximate_patterns_discovery import transform_back_into_seq
from midi_transform import markov_model_first_order
class ApproximatePatternsTest(unittest.TestCase):
    def test_find_approximate_patterns(self):
        """list_notes = list()
        list_notes.append((67,0.0))
        list_notes.append((68,0.5))
        list_notes.append((69,1.0))
        list_notes.append((67,1.5))
        list_notes.append((69,2.0))
        list_notes.append((69,2.5))

        notes = list()
        notes.append((1,1)) # a
        notes.append((1,3)) # b
        notes.append((2,1)) # c
        notes.append((2,2)) # d
        notes.append((2,3)) # e
        notes.append((3,2)) # f
        result = find_approximate_patterns(notes)
        for v in result:
            print(str(v) + ": " + str(result[v]))
        """
        notes = list()
        notes.append((0.0,2))
        notes.append((0.5,0))
        notes.append((1.0,1))

        notes.append((1.5,3))
        notes.append((2.0,1))
        notes.append((2.5,2))

        notes.append((3.0,2))
        notes.append((3.5,1))
        notes.append((4.0,0))

        notes.append((4.5,2))
        notes.append((5.0,1))
        notes.append((5.5,0))
        notes.append((6.0,0))

        notes.append((6.5,0))
        list_patterns,pattern_to_indices,trans_vectors = find_all_patterns(notes)
        print(notes)
        print("Patterns:")
        print(list_patterns)
        print("Indices:")
        print(pattern_to_indices)
        print("Trans_vectors:")
        print(trans_vectors)
        collapsed = collapse_pattern_to_indices(trans_vectors)
        print("Collapsed:")
        print(collapsed)
        true_indices = transform_collapsed_and_indices(collapsed,pattern_to_indices)
        print("True indices")
        print(true_indices)

        print("Transformed back")
        seq = transform_back_into_seq(true_indices)
        print(seq)
    def test_hamming_distance(self):
        seq_1 = "01234"
        seq_2 = "01224"
        self.assertEqual(hamming_distance(seq_1,seq_2),1)

    def test_edit_distance(self):
        seq_1 = "01234"
        seq_2 = "0234"
        self.assertEqual(edit_distance(seq_1,seq_2),1)
    """def test_midi_markov(self):
        seq = "AABCDDB"
        print(markov_model_first_order(seq))
"""
if __name__ == '__main__':
    unittest.main()