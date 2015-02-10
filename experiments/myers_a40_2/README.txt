TROUBLESHOOTING: Contact Bryan Cort (cort@haskins.yale.edu; 203-691-0075).

This is the current PsychoPy implementation of the Haskins Laboratories A40-2 experiment. To run the experiment, double click 
on the A40_2_EXP shortcut. This will launch the experiment and prompt for a subject ID; after entering the ID, you will see a 
menu prompting you to choose a run or exit. Choose the appropriate run and the experiment will enter a 'ready' state, where it 
will wait for the start signal from the MRI (this should happen automatically, but if you need to start the experiment manually, 
you can hit '5' to start). Once it receives the start signal, the experiment will wait 12s for the MRI to warm up, and then will 
begin presenting trials. The experimentor can press 'q' at any time during the run and the experiment will exit after the 
current trial completes. Once all trials in the run have been presented, the program will exit. To start the next run, again 
double click the A40_2_EXP shortcut and select the next run.

Behavioral data is stored in myers_a40_2/data. Data is saved written to a 'raw' file first, and then reformatted to a more 
readable structure after each run. Primary data (saved after the each run completes successfully) is saved in the top level 
myers_a40_2/data directory as SubjID_run#_DateTime.txt. Behavioral data is also saved after each trial to a backup file named 
backup_SubjID_run#_DateTime.txt. This means that there should be 2 full data files for each full run, and one partial data file 
(containing only the trials that were run before the experiment terminated) for partial runs. For any formatted file 
(SubjID_run#_DateTime.txt or backup_SubjID_run#_DateTime.txt) there should also be a copy of the raw, unformatted data in 
myers_a40_2/data/raw_backups. Naming should be identical except that each of the raw backup files will have 'raw_' prepended to 
the name, eg. raw_SubjID_run#_DateTime.txt or raw_backup_SubjID_run#_DateTime.txt
