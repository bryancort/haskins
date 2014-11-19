from myers_a40_2.a40_2 import reformat_output
import os

data_file = os.path.normpath('data/0000_run2_2014_11_18_15h_33m.txt')
backup_dir = os.path.normpath('data/raw_backups')
reformat_output(data_file, backup_dir)
