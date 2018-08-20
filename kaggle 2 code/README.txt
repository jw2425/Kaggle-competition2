To generate the label submission run submission_generator.py 
with Label.csv and Observations.csv in the same directory.

Required dependencies: pandas, numpy, csv
Code written and tested on Python 2.7

NOTE: this algorithm takes several hours to finish, so the code has printouts to stdout for progress updates.
To reduce the time it takes to run, you can reduce the initial_tolerance and iteration_tolerance constants at
the top of the file to around 0.001 and 0.02 respectively (see comments in the code for more info).
Note that if you make this alteration, then the predictions are slightly worse than our top score on kaggle
and the algorithm will still take a few hours to run.

A submission.csv file is generated at the end of the run with the labels that can be submitted to kaggle.