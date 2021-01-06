from collections import Counter
import re
import os.path as op

import pandas as pd
from tqdm import tqdm
import seaborn as sns
import matplotlib.pyplot as plt

import config

def evaluate_cs(original, generated):
    '''Given a original and generated events, calculate precision, recall, and
    F1 of the cardinality score. It is expected that `original` and `generated`
    are pandas dataframes containing columns 'onset' and 'pitch' and that they
    have been deduplicated.

    Parameters
    ----------
    original : pd.DataFrame
        A dataframe containing columns 'onset' and 'pitch' representing the
        true continuation
    generated : pd.DataFrame
        A dataframe containing columns 'onset' and 'pitch' representing the
        generated continuation to be evaluated

    Returns
    -------
    output : dict[float]
        A dictionary containing three keys: 'rec', 'prec' and 'F1', the recall
        precision and the F1 of the cardinality score.
    '''
    translation_vectors = []
    generated_vec = generated[['onset', 'pitch']].values
    original_list = original[['onset', 'pitch']].values.tolist()
    for point in original_list:
        vectors = generated_vec - point
        translation_vectors.extend([tuple(v) for v in vectors])
    vector_counts = Counter(translation_vectors)
    most_common_vector, count = vector_counts.most_common(1)[0]
    recall = (count - 1) / float(len(original) - 1)
    precision = (count - 1) / float(len(generated) - 1)
    if precision + recall == 0:
        f1 = 0.0
    else:
        f1 = (2 * recall * precision) / (
            recall + precision
        )
    output = {'rec': recall, 'prec': precision, 'F1': f1}
    return output


def evaluate_continuation(original, generated, last_onset_prime,
                          onset_increment, evaluate_from_onset,
                          evaluate_until_onset):
    """Given the original and the generated continuations, get the cardinality
    score at different increments through time.

    arameters
    ----------
    original : pd.DataFrame
        A dataframe containing columns 'onset' and 'pitch' representing the
        true continuation
    generated : pd.DataFrame
        A dataframe containing columns 'onset' and 'pitch' representing the
        generated continuation to be evaluated
    last_onset_prime : int
        The onset time of the last onset of the prime
    onset_increment : float
        The increment to increase onset steps by for evaluation
    evaluate_from_onset : float
        The minimum number of onsets after `last_onset_prime` to evaluate the
        continuation from
    evaluate_until_onset : float
        The maximum number of onsets after `last_onset_prime` to evaluate the
        continuation to

    Returns
    -------
    output : pd.DataFrame
        A dataframe containing three columns:
        - 'onset' (evaluation is up to this onset)
        - 'measure' (prec / rec / F1)
        - 'value' for the onset / measure pair
    """
    scores = {'Onset': [], 'Precision': [], 'Recall': [], 'F1': []}
    nr_steps = int((evaluate_until_onset - evaluate_from_onset)
                   / onset_increment)
    max_onset = evaluate_until_onset + last_onset_prime
    for step in range(nr_steps + 1):
        onset = step * onset_increment + evaluate_from_onset
        cutoff = last_onset_prime + onset
        if cutoff <= max_onset:
            scores['Onset'].append(onset)
            # Select all rows with onset times less than or equal to cutoff
            original_events = original[original['onset'] <= cutoff]
            generated_events = generated[generated['onset'] <= cutoff]
            if (len(original_events) <= 1 or len(generated_events) <= 1):
                scores['Precision'].append(None)
                scores['Recall'].append(None)
                scores['F1'].append(None)
                continue
            else:
                output = evaluate_cs(original_events, generated_events)
                scores['Precision'].append(output['prec'])
                scores['Recall'].append(output['rec'])
                scores['F1'].append(output['F1'])
    return pd.DataFrame(scores)


def score_cs(fn_list, alg_names, files_dict, cont_true, prime):
    card_scores = []
    for alg in alg_names:
        print(f'Scoring {alg} with cardinality score')
        for fn in tqdm(fn_list):
            # the generated file name may have additions to original file name
            generated_fn = next(
                (alg_fn for alg_fn in files_dict[alg].keys()
                 if re.search(fn, alg_fn)),
                None
            )
            true_df = cont_true[fn]
            gen_df = files_dict[alg][generated_fn]
            prime_final_onset = prime[fn].iloc[-1]['onset']
            cs_score = evaluate_continuation(
                true_df,
                gen_df,
                prime_final_onset,
                0.5, 2.0, 10.0
            )
            cs_score['fn'] = fn
            cs_score['Model'] = alg
            card_scores.append(cs_score)
    card_df = pd.concat(card_scores, axis=0)
    data = card_df.melt(
        id_vars=['fn', 'Onset', 'Model'],
        value_vars=['Precision', 'Recall', 'F1'],
        var_name="measure",
        value_name="Score"
    )

    ### START MODIFICATION
    data['Onset'] = data['Onset'].astype(float)
    data['Score'] = data['Score'].astype(float)
    ### END MODIFICATION

    plt.figure()
    sns.set_style("whitegrid")
    g = sns.FacetGrid(
        data,
        col='measure',
        hue='Model',
        hue_order=config.MODEL_DIRS.keys(),
        hue_kws={
            'marker': ['o', 'v', 's', 'D'],
            'linestyle' : [":","--","-", "-."]
        }
        )
    g = g.map(
        sns.lineplot,
        'Onset',
        'Score',
        # style='Model',
        # style_order=config.MODEL_DIRS.keys(),
        # markers=['o', 'v', 's']
    ).add_legend()
    filename = op.join(config.OUTPUT_FOLDER, '{}_cs_scores.png'.format(config.FILENAME_FRAGMENT))
    plt.savefig(filename, dpi=300)

