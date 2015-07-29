#!/usr/bin/python
# -------------------------------------------------------------------------------
# Name:        task_scripts.calc_sfnr
# Purpose:      runs 3dtstat on specified subjects to generate sfnr measurements
#
# Author:      Bryan Cort
#
# Created:     10/20/2014
# -------------------------------------------------------------------------------

import argparse
import os
import sys
import traceback
from utils import base_utils, file_utils
from core import mri_data

def genArgParser():
    """
    Generate a command line argument parser for this script.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--debug', action='store_true', default=False,
                        help='Debug mode on. Default: off')

    parser.add_argument('--mri_dir', default='/data1/bil/mri_subjects',
                        help='Directory containing mri subjects.'
                             'Default: /data1/bil/mri_subjects')

    parser.add_argument('--proc_pats', nargs='*', default=['*.results'],
                        help='One or more substrings uniquely identifying proc runs. '
                             'NOT unix-style wildcard expressions.'
                             'Looks for unique subdir matching *TAG*. Default: results')

    parser.add_argument('--patterns', nargs='*', default='*',
                        help='One or more unix-style wildcard expressions to generate the list of subject '
                             'data directories to process. Default: *')

    return parser


def _debug(*cmd_args):
    sys.argv = [sys.argv[0]] + list(cmd_args)


_debug_cmd = '--mri_dir /data1/bil/mri_subjects --proc_pats *.results *.scale --patterns hu_* ny???'
# _debug_cmd = '--mri_dir /data1/bil/mri_subjects --proc_pats results scale --patterns hu_AG_228*'

def __main__():
    scriptName = os.path.splitext(os.path.basename(__file__))[0]
    parser = genArgParser()
    args = parser.parse_args()
    if len(sys.argv) == 1 or args.debug:
        _debug(*_debug_cmd.split(' '))
        args = parser.parse_args()

    dirs = file_utils.get_immediate_subdirectories(args.mri_dir)
    subj_dirs = base_utils.mfilter(dirs, *args.patterns)
    scans = []
    for d in subj_dirs:
        try:
            scans.append(mri_data.Scan2(os.path.split(d)[1], os.path.join(args.mri_dir, d)))
        except:
            print traceback.format_exc()
    for scan in scans:
        for pat in args.proc_pats:
            try:
                scan.add_proc_run(proc_pat=pat, run_name=pat)
                headfile = file_utils.match_single_file(path=scan.proc_runs[pat].root_dir, pattern='all_runs*.HEAD')
                scan.proc_runs[pat].execute_cmd('3dTstat -cvarinv -prefix {}_SFNR {}'.format(scan.scan_id, headfile))
            except:
                print traceback.format_exc()
if __name__ == '__main__':
    __main__()