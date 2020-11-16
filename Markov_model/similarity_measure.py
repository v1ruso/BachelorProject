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


def similarity_score_with_translation(q, s):
    """
    Calculates the similarity score between two sets of notes.
    q,s: sets of MIDI notes.
    return: the similarity score [0,1], higher values mean higher similarity
    """
    cart_product = itertools.product(q, s)
    max_number_of_sim_notes = 0
    max_translation_pitch = 0
    max_translation_onset = 0
    for current_translation_vector in cart_product:
        current_number_of_sim_notes = 0
        diff_onsets = 0
        diff_pitches = 0
        for j in range(len(q)):
            diff_onsets = current_translation_vector[
                0].start - current_translation_vector[1].start
            diff_pitches = current_translation_vector[
                0].pitch - current_translation_vector[1].pitch
            new_note = pretty_midi.Note(velocity=q[j].velocity,
                                        pitch=q[j].pitch + diff_pitches,
                                        start=q[j].start + diff_onsets,
                                        end=q[j].end + diff_onsets)
            if is_note_in_seq(new_note, s):
                current_number_of_sim_notes += 1
        if current_number_of_sim_notes > max_number_of_sim_notes:
            max_number_of_sim_notes = current_number_of_sim_notes
            max_translation_onset = diff_onsets
            max_translation_pitch = diff_pitches
    return 1 - np.linalg.norm(
        np.array([max_translation_onset, max_translation_pitch])) / len(q)


def similarity_score(q, p):
    # computes how similar two sequences are
    # higher returned values mean higher similarities
    # returns values between 0 and 1
    if len(q) == 0 or len(p) == 0:
        return 1.0
    if len(q) == len(p):
        q_average = sum(q) / len(q)
        p_average = sum(p) / len(p)
        upper_sum = sum((q - q_average) * (p - p_average))
        lower_q_sum = sum((q - q_average)**2)
        lower_p_sum = sum((p - p_average)**2)
        return upper_sum / ((lower_q_sum**(1.0 / 2)) *
                            (lower_p_sum**(1.0 / 2)))
    else:
        A = np.zeros((len(p), len(q)))
        W_insert = -0.5
        W_delete = -0.5
        for i in range(1, len(p)):
            for j in range(1, len(q)):
                subs = 1 if p[i] == q[j] else -1
                A[i][j] = np.max([
                    A[i - 1][j - 1] + subs, A[i][j - 1] + W_insert,
                    A[i - 1][j] + W_delete, 0
                ])
        return np.max(A) / len(q)


def biggest_subset_similarity(q, p):
    """
    This function will use a sliding window for p, and calculate 
    the biggest similarity between q and a subset of p. Returns 
    the subset which has the highest similarity with q
    """
    max_subset = np.array([])
    max_similarity = 0
    for i in range(len(p)):
        for j in range(i + 1, len(p) + 1):
            current_subset = p[i:j]
            current_similarity_score = similarity_score(q, current_subset)
            if current_similarity_score > max_similarity:
                max_similarity = current_similarity_score
                max_subset = current_subset
    return max_subset
