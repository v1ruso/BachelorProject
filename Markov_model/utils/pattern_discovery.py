import numpy as np

def is_pitch_equal(this,that):
    return this.pitch == that.pitch

def find_biggest_recurring_pattern(seq):
    """
    seq: sequence of notes
    """
    A = np.zeros((len(seq)+1,len(seq)+1),dtype=int)
    res = list()
    res_length = 0
    index = 0
    for i in range(1,len(seq)+1):
        for j in range(i+1,len(seq)+1):
            if seq[i-1]!=None and seq[j-1]!=None and is_pitch_equal(seq[i-1],seq[j-1]) and (j-i) > A[i-1][j-1]:
                A[i][j] = A[i-1][j-1] + 1
                if A[i][j] > res_length:
                    res_length = A[i][j]
                    index = max(i,index)
            else:
                A[i][j] = 0
    if res_length > 0:
        for i in range(index-res_length + 1, index+1):
            res.append(seq[i-1])
    return res, index-res_length