import unittest
import numpy as np
from similarity_measure import similarity_score
from similarity_measure import biggest_substring
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


if __name__ == '__main__':
    unittest.main()