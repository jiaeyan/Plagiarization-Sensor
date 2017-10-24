# Plagiarization_Sensor
A detector to find all longest repeated language segments among large volumes of texts, multiprocessing is applied.
The fianl result is sotred in a CSV file.

■ PlagiarizationSensor.py: the main class to utilize multiprocessing and calls on other classes.

■ Counter.py: its count() function is mapped by multiprocessing to collect N-grams faster, and then aggregate the results.

■ Incrementor.py: grow the base-lengh N-grams from Counter.py to user defined length, with condition where all have >1 filehits. Eliminate the duplications in the meantime due to the sliding window of N-gram Model.
