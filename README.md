# BachelorProject

Here's how to run the continuation programs.

- Clone this repository.
- Download and install <a href="https://abjad.github.io/">abjad</a>, <a href="http://lilypond.org">LilyPond</a> (needed by abjad) and <a href="https://github.com/craffel/pretty-midi">pretty_midi</a>, as well as the standard python librairies, such as numpy.
- Download any of the monophonic datasets from <a href="https://www.music-ir.org/mirex/wiki/2019:Patterns_for_Prediction#Data">MIREX 2019: Patterns for Prediction</a>: <a href="http://tomcollinsresearch.net/research/data/mirex/ppdd/ppdd-sep2018/PPDD-Sep2018_sym_mono_small.zip">small</a>, <a href="http://tomcollinsresearch.net/research/data/mirex/ppdd/ppdd-sep2018/PPDD-Sep2018_sym_mono_medium.zip">medium</a> or <a href="http://tomcollinsresearch.net/research/data/mirex/ppdd/ppdd-sep2018/PPDD-Sep2018_sym_mono_large.zip">large</a>.
- In the newly downloaded folders, at the same level as the "prime_csv" folder, add 6 folders: "markov_without_prediction_midi", "markov_without_prediction_csv". "markov_with_prediction_midi", "markov_with_prediction_csv", "markov_with_non_exact_prediction_midi" and "markov_with_non_exact_prediction_csv". These folders are needed for the evaluation code.
- Download the <a href="https://github.com/BeritJanssen/PatternsForPrediction/tree/mirex2019">evaluation code</a>, and follow the instructions. 
- Copy and paste the content of [config_corrected.py](Generation/config_corrected.py) into config.py (in the newly downloaded evaluation folder), and modify "OUTPUT_FOLDER", "DATASET_PATH" and "FILENAME_FRAGMENT".
- Edit cs.py (in the evaluation code) to [cs_corrected.py](Generation/cs_corrected.py) (copy and paste the code).
- Run the jupyter notebook [Generation/Generation.ipynb](Generation/Generation.ipynb).

All the code necessary to find patterns and produce the continuations is available in [Generation/utility.py](Generation/utility.py), [Generation/simple_first_order_mm.py](Generation/simple_first_order_mm.py), [Generation/string_based.py](Generation/string_based.py) and [Generation/translation_based.py](Generation/translation_based.py).
