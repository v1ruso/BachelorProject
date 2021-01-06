# Location to write output to
OUTPUT_FOLDER = 'PATH/TO/OUTPUT/FOLDER' # no "/" at the end. This is where the plots are generated. ### CHANGE THIS ###
# point the dataset path to the appropriate path on your file system
DATASET_PATH = "../Datasets/PPDD-Sep2018_sym_mono_small" ### CHANGE THIS ###

MODEL_DIRS = { ### NO NEED TO CHANGE THIS ###
    'Translation-based': DATASET_PATH + '/markov_with_non_exact_prediction_csv',
    'Baseline': DATASET_PATH + '/cont_foil_csv',
    'String-based': DATASET_PATH + '/markov_with_prediction_csv',
    'Simple': DATASET_PATH + '/markov_without_prediction_csv'
}
MODEL_KEYS = { ### NO NEED TO CHANGE THIS ###
    'Translation-based': ['onset', 'pitch', 'morph', 'dur', 'ch'],
    'Baseline': ['onset', 'pitch', 'morph', 'dur', 'ch'],
    'String-based': ['onset', 'pitch', 'morph', 'dur', 'ch'],
    'Simple': ['onset', 'pitch', 'morph', 'dur', 'ch']
}
DISCRIM_MONO_FILES = {
    'mdl1': 'path/to/mono1.csv',
    'mdl2': 'path/to/mono2.csv'
}
DISCRIM_POLY_FILES = {
    'mdl1': 'path/to/poly1.csv',
    'mdl2': 'path/to/poly2.csv'
}
### CHANGE THIS ###
FILENAME_FRAGMENT = "FILENAME"

