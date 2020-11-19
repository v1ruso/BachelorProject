import pretty_midi
import numpy as np
import itertools
NUMBER_OF_PITCHES = 128
PITCHES_PER_OCTAVE = 12


def is_note_in_seq(note, seq):
    for n in seq:
        if note.pitch == n.pitch and note.start == n.start:
            return True
    return False


def similarity_score_with_translation(seq_main,seq_compared):
    """
    Calculates the similarity score between two sets of notes.
    seq_main,seq_compared: sets of pretty_midi notes.
    return: the similarity score [0,1], higher values mean higher similarity
    """
    all_pairs = itertools.product(seq_main, seq_compared)
    max_number_of_sim_notes = 0
    for current_translation_vector in all_pairs:
        current_number_of_sim_notes = 0
        diff_onsets = current_translation_vector[0].start - current_translation_vector[1].start
        diff_pitches = current_translation_vector[0].pitch - current_translation_vector[1].pitch
        for j in range(len(seq_main)):
            new_note = pretty_midi.Note(velocity=seq_main[j].velocity,
                                        pitch=seq_main[j].pitch - diff_pitches,
                                        start=seq_main[j].start - diff_onsets,
                                        end=seq_main[j].end - diff_onsets)
            if is_note_in_seq(new_note, seq_compared):
                current_number_of_sim_notes += 1
        if current_number_of_sim_notes > max_number_of_sim_notes:
            max_number_of_sim_notes = current_number_of_sim_notes
    return max_number_of_sim_notes / len(seq_main)

def similarity_score(seq_main, seq_compared):
    # computes how similar two sequences are
    # higher returned values mean higher similarities
    # returns values between 0 and 1
    if len(seq_main) == 0 or len(seq_compared) == 0:
        return 1.0
    else:
        A = np.zeros((len(seq_compared)+1, len(seq_main)+1))
        W_insert = -0.5
        W_delete = -0.5
        for i in range(1, len(seq_compared)+1):
            for j in range(1, len(seq_main)+1):
                subs = 1 if seq_compared[i-1] == seq_main[j-1] else -1
                A[i][j] = np.max([
                    A[i - 1][j - 1] + subs, A[i][j - 1] + W_insert,
                    A[i - 1][j] + W_delete, 0
                ])
        return np.max(A) / len(seq_main)

def biggest_substring(seq_main, seq_compared):
    if len(seq_main) == 0 or len(seq_compared) == 0:
        return np.array([])
    else:
        A = np.zeros((len(seq_main), len(seq_compared)),dtype=int)
        ret = np.array([])
        z = 0
        for i in range(len(seq_main)):
            for j in range(len(seq_compared)):
                if seq_compared[j]==seq_main[i]:
                    if i==0 or j==0:
                        A[i][j]=1
                    else: 
                        A[i][j]=A[i-1][j-1]+1
                    if A[i][j] > z:
                        z = A[i][j]
                        ret = seq_main[i-z + 1:i+1]
                    elif A[i][j] == z:
                        np.append(ret,seq_main[i-z+1:i+1])
                else:
                    A[i][j] = 0
        return ret

def biggest_submelody(seq_main, seq_compared):
    """
    Compares all possible substring of seq_compared to seq_main.
    Returns the pattern which has the biggest similarity with seq_main.
    In other words, it returns the biggest pattern that appears in both melodies.
    seq_main: pretty_MIDI sequence of notes (monophonic)
    seq_compared: pretty_MIDI sequence of notes (monophonic)
    """
    max_subset = np.array([])
    max_similarity = 0
    for i in range(len(seq_compared)):
        for j in range(i + 1, len(seq_compared) + 1):
            current_subset = seq_compared[i:j]
            current_similarity_score = similarity_score_with_translation(seq_main, current_subset)
            print(str(i)+","+str(j)+":"+str(current_similarity_score))
            if current_similarity_score > max_similarity:
                max_similarity = current_similarity_score
                max_subset = current_subset
    print("Max similarity is: "+ str(max_similarity))
    return max_subset