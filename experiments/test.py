from myers_a40_2.a40_2 import _reformat_output
import os

data_file = os.path.normpath('myers_a40_2/data/0001_run1_2014_11_24_14h_51m.txt')
backup_dir = os.path.normpath('myers_a40_2/data/raw_backups')
_reformat_output(data_file, backup_dir)
