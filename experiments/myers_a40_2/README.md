TROUBLESHOOTING: Contact Bryan Cort (cort@haskins.yale.edu; 203-691-0075).

This is the current PsychoPy implementation of the Haskins Laboratories A40-2 experiment. To run the experiment, double click 
on the A40_2_EXP shortcut. This will launch the experiment and prompt for a subject ID; after entering the ID, you will see a 
menu prompting you to choose a run or exit. Choose the appropriate run and the experiment will enter a 'ready' state, where it 
will wait for the start signal from the MRI (this should happen automatically, but if you need to start the experiment manually, 
you can hit '5' to start). Once it receives the start signal, the experiment will wait 12s for the MRI to warm up, and then will 
begin presenting trials. The experimentor can press 'q' at any time during the run and the experiment will exit after the 
current trial completes. Once all trials in the run have been presented, the program will exit. To start the next run, again 
double click the A40_2_EXP shortcut and select the next run.

Behavioral data is stored in myers_a40_2/data as [FNAME PATTERN HERE]. The data is saved in a 'running' save file after each 
trial, and data for the whole run is saved after that run successfully completes. This means that there should be 2 full data
files for each full run, and one partial data file (containing only the trials that were run before the experiment terminated) 
for partial runs.
