import pretty_midi
import numpy as np

NUMBER_OF_PITCHES = 128
PITCHES_PER_OCTAVE = 12

def similarity_score(q,p):
    # computes how similar two sequences are
    # higher returned values mean higher similarities
    # returns values between 0 and 1
    if len(q)==0 or len(p)==0:
        return 1.0
    if len(q) == len(p):
        q_average = sum(q)/len(q)
        p_average = sum(p)/len(p)
        upper_sum = sum((q-q_average)*(p-p_average))
        lower_q_sum = sum((q-q_average)**2)
        lower_p_sum = sum((p-p_average)**2)
        return upper_sum/((lower_q_sum**(1.0/2))*(lower_p_sum**(1.0/2)))
    else:
        A = np.zeros((len(p),len(q)))
        W_insert = -0.5
        W_delete = -0.5
        for i in range(1,len(p)):
            for j in range(1,len(q)):
                subs = 1 if p[i]==q[i] else -1
                A[i][j] = np.max([A[i-1][j-1]+subs,A[i][j-1]+W_insert,A[i-1][j]+W_delete,0])
        return np.max(A)/len(q)

def biggest_subset_similarity(q,p):
    """
    This function will use a sliding window for p, and calculate 
    the biggest similarity between q and a subset of p. Returns 
    the subset which has the highest similarity with q
    """