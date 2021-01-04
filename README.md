# BachelorProject

Here's how to run the continuation programs.

- Clone this repository.
- Download and install <a href="https://abjad.github.io/">abjad</a>, <a href="http://lilypond.org">LilyPond</a> (needed by abjad) and <a href="https://github.com/craffel/pretty-midi">pretty_midi</a>, as well as the standard python librairies, such as numpy.
- Download any of the monophonic  <a href="https://www.music-ir.org/mirex/wiki/2019:Patterns_for_Prediction#Data">MIREX 2019: Patterns for Prediction</a> datasets.
- In the newly downloaded folders, at the same level as the "prime_csv" folder, add 6 folders: "markov_without_prediction_midi", "markov_without_prediction_csv". "markov_with_prediction_midi", "markov_with_prediction_csv", "markov_with_non_exact_prediction_midi" and "markov_with_non_exact_prediction_csv". These folders are needed for the evaluation code.
- Run the notebook Generation/Generation.ipynb, and follow the instructions to run the evaluation code.

All the code necessary to find patterns and produce the continuation is available in the .py file in Generation.
