import unittest
from approximate_patterns_discovery import hamming_distance
from approximate_patterns_discovery import edit_distance
from approximate_patterns_discovery import find_approximate_patterns
from approximate_patterns_discovery import filter_patterns
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
        notes.append((0.0,0))
        notes.append((0.5,1))
        notes.append((1.0,2))

        notes.append((1.5,0))
        notes.append((2.0,1))
        notes.append((2.5,2))

        notes.append((3.0,2))
        notes.append((3.5,3))
        notes.append((4.0,4))

        result= find_approximate_patterns(notes)
        for v in result:
            print(str(v) + ": " + str(result[v]))
        print("Result filtered:")
        result_filter = filter_patterns(result,notes)
        for v in result_filter:
            print(str(v) + ": " + str(result_filter[v]))


    def test_hamming_distance(self):
        seq_1 = "01234"
        seq_2 = "01224"
        self.assertEqual(hamming_distance(seq_1,seq_2),1)

    def test_edit_distance(self):
        seq_1 = "01234"
        seq_2 = "0234"
        self.assertEqual(edit_distance(seq_1,seq_2),1)
if __name__ == '__main__':
    unittest.main()