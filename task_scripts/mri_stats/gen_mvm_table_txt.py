#!/usr/bin/python
# -------------------------------------------------------------------------------
# Name:        task_scripts.gen_mvm_table_txt
# Purpose:      generates a data table for use with 3dMVM
#
# Author:      Bryan Cort
#
# Created:     10/21/2014
# -------------------------------------------------------------------------------
__author__ = 'cort'

import argparse
import os
import sys
from utils import base_utils, file_utils
from core import mri_data

def genArgParser():
    """
    Generate a command line argument parser for this script.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--debug', action='store_true', default=False,
                        help='Debug mode on. Default: off')

    parser.add_argument('--mvm_output_prefix', default='output_{}.sh'.format(base_utils.getLocalTime()),
                        help='mvm call template file'
                             'Default: /data1/scripts_refactor/haskins/task_scripts/mri_stats/mvm_call_template.txt')


    parser.add_argument('--mvm_template', default=os.path.normpath('./mvm_call_template.txt'), # todo: improve
                        help='mvm call template file'
                             'Default: /data1/scripts_refactor/haskins/task_scripts/mri_stats/mvm_call_template.txt')

    parser.add_argument('--mri_dir', default='/data1/bil/mri_subjects',
                        help='Directory containing stats files.\n'
                             'Default: /data1/bil/mri_subjects')

    parser.add_argument('--outputDir', default='/data1/bil/group_mvm_tables',
                        help='Output directory for MVM table.\n'
                             'Default: /data1/bil/group_mvm_tables')

    parser.add_argument('--outputFile', default='mvm_call_{}.sh'.format(base_utils.getLocalTime(hr_min=False)),
                        help='Name (without preceding path) of the output file.\n'
                             'Default: mvm_call_{date}.sh')

    parser.add_argument('--conditionFile', default='/data1/bil/mri_subjects/a187_within.txt',
                        help='File containing condition information for the study.\n'
                             'Default: /data1/bil/mri_subjects/a187_within.txt')

    parser.add_argument('--vox_covar', default=None,
                        help='Voxelwise covariate.\n'
                             'Default: None')

    parser.add_argument('--vox_covar_pattern', default=None,
                        help='Pattern to match for file with the voxelwise covariate.\n'
                             'Default: None')

    parser.add_argument('--proc_run', default='results',
                        help='File containing condition information for the study.\n'
                             'Default: /data1/bil/mri_subjects/a187_conditions.txt')

    parser.add_argument('--subjects', nargs='*', default='all',
                        help='List of subjects to include in the mvm.\n'
                             'Default: all')

    #script action params
    parser.add_argument('-r', '--report', action='store_true', default=False,
                        help='Pass this flag to generate a run report.')
    return parser


def _debug(*cmd_args):
    sys.argv = [sys.argv[0]] + list(cmd_args)


_debug_cmd = '--mri_dir Y:\\mri_subjects --outputDir Y:\\group_mvm_tables'+\
' --conditionFile Y:\\mri_subjects\\a187_within.txt --proc_run results --subjects hu_AA380_16_3_13 hu_AC513_25_4_12'+\
' hu_AE239 hu_AG228_21_1_14 ny051 ny057 ny058 ny059 --vox_covar sfnr --vox_covar_pattern *SFNR*.HEAD'


#todo: implement 3dinfo parsing instead of reading from the condition file
def read_condition_file(cond_file_path):
    """
    Reads within subjects variable condition file
    """
    cft = file_utils.readTable2(fPath=cond_file_path)
    # var_names = cft[0][:-1]
    var_perms = {tuple(entry[:-1]): entry[-1] for entry in cft[1:]}
    within_vars = {}
    for i, k in enumerate(cft[0][:-1]):
        within_vars[k] = set()
        for l in cft[1:]:
            within_vars[k].add(l[i])
    within_vars = {k: tuple(v) for k, v in within_vars.items()}

    return within_vars, var_perms


def __main__():
    scriptName = os.path.splitext(os.path.basename(__file__))[0]
    parser = genArgParser()
    args = parser.parse_args()
    if len(sys.argv) == 1 or args.debug:
        _debug(*_debug_cmd.split(' '))
        args = parser.parse_args()
    args.mri_dir = os.path.normpath(args.mri_dir)
    args.outputDir = os.path.normpath(args.outputDir)
    args.conditionFile = os.path.normpath(args.conditionFile)
    outputFile = os.path.join(args.outputDir, args.outputFile)

    scans = []
    for s in args.subjects:
        scan = mri_data.Scan(scan_id=s, data_dir=os.path.join(args.mri_dir, s))
        scan.add_proc_run(proc_tag=args.proc_run)
        scans.append(scan)

    within_vars, perm_map = read_condition_file(args.conditionFile)
    between_vars = {'Site': ('hu', 'ny')}
    # todo: read from file or args for AFNI implementation
    scan_map = {}
    for scan in scans:
        if scan.scan_id.startswith('hu'):
            scan_map[scan] = {'Site': 'hu'}
        elif scan.scan_id.startswith('ny'):
            scan_map[scan] = {'Site': 'ny'}

    mvmtable = mri_data.gen_mvm_table(scans_dict=scan_map, within=within_vars, between=between_vars,
                                      subbrick_mapping=perm_map, vox_covar=args.vox_covar,
                                      vox_covar_file_pattern=args.vox_covar_pattern, use_proc_run=args.proc_run)
    mvmtable = ' \\\n'.join(mvmtable)

    with open(outputFile, 'w') as outfile:
        outfile.write(mvmtable)

    format_args = {'prefix':args.mvm_output_prefix,
                    'mvm_table':outputFile}
    if args.vox_covar:
        format_args['vox_covar'] = args.vox_covar

    # if args.vox_covar:
    with open(args.mvm_template, 'r') as mvmcall:
        mvmcall.format(**format_args)
    # else:
        # with open(args.mvm_template, 'r') as mvmcall:
        #     mvmcall.format(dmy_date=base_utils.getLocalTime(hr_min=False), vox_covar=args.vox_covar,
        #                    mvm_table=outputFile)

if __name__ == '__main__':
    __main__()