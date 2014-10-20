# -------------------------------------------------------------------------------
# Name:        task_scripts.calc_sfnr
# Purpose:      runs 3dtstat on specified subjects to generate sfnr measurements
#
# Author:      Bryan Cort
#
# Created:     10/20/2014
# -------------------------------------------------------------------------------

import argparse

def genArgParser():
    """
    Generate a command line argument parser for this script.
    """
    parser = argparse.ArgumentParser()

    # path and study info params
    parser.add_argument('--statsDir', default='/data1/bil/group_8_27_14',
                        help='Directory containing stats files.\n'
                             'Default: /data1/bil/group_8_27_14')

    parser.add_argument('include', nargs='+',
                        help='Only data with classifications (in the a187_config.txt file) specified here will be '
                             'included in the MVM table. Data matching all arguments for this option will '
                             'be included.\n')

    parser.add_argument('patterns', nargs='+',
                        help='One or more unix-style wildcard expressions to generate the list of subject '
                             'data directories to process.')
    return parser
