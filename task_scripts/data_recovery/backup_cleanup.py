# -------------------------------------------------------------------------------
# Name:        backup_cleanup
# Purpose:      remove the files from the backup that we plan to exclude
#
# Author:      Bryan Cort
#
# Created:     8/12/2014
# -------------------------------------------------------------------------------

import os
import shutil
import sys
scr_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.normpath(os.path.join(scr_dir, '../..')))
from utils import file_utils


def __main__():
    top_node = sys.argv[1]
    exclude_filepath  = sys.argv[2]

    with open(exclude_filepath, 'rU') as infile:
        exclude_patterns = [pat for pat in infile.read().split('\n') if pat]
        for curr_node, dirnames, filenames in os.walk(top_node):
            matching_dirs = file_utils.get_dirs_from_patterns(curr_node, True, *exclude_patterns)
            matching_files = file_utils.get_files_from_patterns(curr_node, True, *exclude_patterns)
            for d in matching_dirs:
                print d
                if os.path.islink(d):
                    os.unlink(d)
                else:
                    shutil.rmtree(d)
            for f in matching_files:
                print f
                os.remove(f)


if __name__ == '__main__':
    __main__()