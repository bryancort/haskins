#!/usr/bin/python
# -------------------------------------------------------------------------------
# Name:        relabel_subbricks
# Purpose:      batch relabels subbricks for subjects with 3drefit
#
# Author:      Bryan Cort
#
# Created:     10/21/2014
# -------------------------------------------------------------------------------
__author__ = 'cort'

import argparse
import os
import sys
from utils import mri_utils, file_utils
from core import mri_data

from utils.haskins_exceptions import *


def genArgParser():
    """
    Generate a command line argument parser for this script.
    """
    parser = argparse.ArgumentParser()

    debug_default = False
    parser.add_argument('--debug', action='store_true', default=debug_default,
                        help='Debug mode on. Default: {}'.format(debug_default))

    mri_dir_default = '/data3/a202/group_analysis/W1_all_subjects_fastloc'
    parser.add_argument('--mri_dir', default=mri_dir_default,
                        help='Directory containing mri data directories.\n'
                             'Default: {}'.format(mri_dir_default))

    rename_table_file_default = None
    parser.add_argument('--rename_table_file', default=rename_table_file_default,
                        help='Filepath to table with subbrick number, new subbrick name columns.\n'
                             'Default: {}'.format(rename_table_file_default))

    proc_runs_default = ['*.fastloc']
    parser.add_argument('--proc_runs', default=proc_runs_default, nargs='*',
                        help='Processing runs to change subbrick names for.\n'
                             'Default: {}'.format(proc_runs_default))

    subjects_patterns_default = ['ny*']
    parser.add_argument('--subjects_patterns', nargs='*', default=subjects_patterns_default,
                        help='Subject name patterns to change subbrick names for.\n'
                             'Default: {}'.format(subjects_patterns_default))

    filename_patterns_default = ['*stats*REML+*.HEAD']
    parser.add_argument('--filename_patterns', nargs='*', default=filename_patterns_default,
                        help='Filename patterns to change subbrick names in.\n'
                             'Default: {}'.format(filename_patterns_default))

    #script action params
    report_default = False
    parser.add_argument('-r', '--report', action='store_true', default=report_default,
                        help='Pass this flag to generate a run report. Default: {}'.format(report_default))
    return parser


def _debug(*cmd_args):
    sys.argv = [sys.argv[0]] + list(cmd_args)

_debug_cmd = '--rename_table_file /data3/a202/group_analysis/subbrick_corrections_BC.txt ' \
             '--subjects_patterns 1???_t?'


def __main__():
    scriptName = os.path.splitext(os.path.basename(__file__))[0]
    parser = genArgParser()
    args = parser.parse_args()
    if len(sys.argv) == 1 or args.debug:
        _debug(*_debug_cmd.split(' '))
        args = parser.parse_args()
    args.mri_dir = os.path.normpath(args.mri_dir)
    args.rename_table_file = os.path.normpath(args.rename_table_file)

    # args.proc_runs = args.proc_runs.split(',')
    # args.subjects_patterns = args.subjects_patterns.split(',')
    # args.filename_patterns = args.filename_patterns.split(',')

    new_sb_names = file_utils.readTable2(args.rename_table_file, delim=' ')
    pairs = new_sb_names[1:]

    scan_dir_names = file_utils.get_dirs_from_patterns(args.mri_dir, False, *args.subjects_patterns)
    scans = []
    for d in scan_dir_names:
        scan = mri_data.Scan2(scan_id=d, root_dir=os.path.join(args.mri_dir, d))
        for run in args.proc_runs:
            try:
                scan.add_proc_run(run)
            except FileError:
                print 'Could not create run {} for {}'.format(run, scan)
        scans.append(scan)

    for scan in scans:
        for pr in scan.proc_runs.values():
            files = file_utils.get_files_from_patterns(pr.root_dir, True, *args.filename_patterns)
            for f in files:
                for p in pairs:
                    mri_utils.rename_subbrick(f, p[0], p[1])  # todo: test this

if __name__ == '__main__':
    __main__()