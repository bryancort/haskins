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

    parser.add_argument('--output_table', default='mvm_table_{}.txt'.format(base_utils.getLocalTime(hr_min=False)),
                        help='Name (without preceding path) of the table list_attrs file.\n'
                             'Default: mvm_table_{date}.txt')

    parser.add_argument('--output_call', default='mvm_call_{}.sh'.format(base_utils.getLocalTime(hr_min=False)),
                        help='Name (without preceding path) of the call list_attrs file.\n'
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


_debug_cmd = '--subjects hu_AA380_16_3_13 hu_AC513_25_4_12 hu_AE239 hu_AG228_21_1_14 hu_AS780 hu_BK842_4_1_13 hu_BW331_9_5_14 hu_CL702 hu_DB391_30_11_13 hu_DF592_21_6_13_1509 hu_EA749_20140625 hu_GW218_3_8_12 hu_HF446_23_2_13 hu_HP010_4_2_14 hu_JR587_29_3_14 hu_JV009_15_2_13 hu_JW894_21_1_12 hu_KG310 hu_LA943_8_12_12 hu_LG712_17_06_14 hu_LK799 hu_MA306_8_3_13 hu_MK041_15_11_13_1100 hu_MN626 hu_MS135_5_2_14 hu_NA651_11_1_14 hu_NB712_15_11_13 hu_RE911_30_11_13 hu_RF998_18_1_14 hu_RG357_17_6_14 hu_RG905_7_12_13 hu_RL112 hu_SD031_20140625 hu_SN083 hu_SS322 hu_ST010_3_2_12 hu_TK132_23_3_12 hu_YD874_12_4_13_1236 hu_YG403_28_6_12_1059 hu_YG498_25_4_12 ny001 ny002 ny004 ny005 ny006 ny007 ny008 ny009 ny010 ny011 ny012 ny020 ny021b ny022 ny029 ny033 ny034 ny036 ny040 ny045 ny048 ny051 ny057 ny058 ny059 ny019 ny052 ny054 ny050 ny039 ny060 ny032 ny031 hu_MH148 hu_NI319 --mvm_output_prefix scaled_SFNR_vox_covar --mvm_template /data1/scripts_refactor/haskins/task_scripts/mri_stats/mvm_call_template_vox_covar.txt --outputDir /data1/bil/group_mvms_10_29_14 --output_table scaled_SFNR_vox_covar_table.txt --output_call scaled_SFNR_vox_covar_call.sh --proc_run scale --vox_covar SFNR --vox_covar_pattern *SFNR*'


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
    output_table = os.path.join(args.outputDir, args.output_table)
    output_call = os.path.join(args.outputDir, args.output_call)

    scans = []
    for s in args.subjects:
        scan = mri_data.Scan(scan_id=s, data_dir=os.path.join(args.mri_dir, s))
        scan.add_proc_run(proc_tag=args.proc_run)
        scans.append(scan)

    within_vars, perm_map = read_condition_file(args.conditionFile)
    between_vars = {'Site': ('HU', 'NY')}
    # todo: read from file or args for AFNI implementation
    scan_map = {}
    for scan in scans:
        if scan.scan_id.startswith('hu'):
            scan_map[scan] = {'Site': 'HU'}
        elif scan.scan_id.startswith('ny'):
            scan_map[scan] = {'Site': 'NY'}

    mvmtable = mri_data.gen_mvm_table(scans_dict=scan_map, within=within_vars, between=between_vars,
                                      subbrick_mapping=perm_map, vox_covar=args.vox_covar,
                                      vox_covar_file_pattern=args.vox_covar_pattern, use_proc_run=args.proc_run)

    file_utils.writeTable(mvmtable, output_table, lineSep=' \\\n')

    format_args = {'prefix':args.mvm_output_prefix,
                    'mvm_table':output_table}
    if args.vox_covar:
        format_args['vox_covar'] = args.vox_covar

    # if args.vox_covar:
    with open(args.mvm_template, 'r') as mvmcall:
        final_call = mvmcall.read().format(**format_args)
        with open(output_call, 'w') as mvmcall_out:
            mvmcall_out.write(final_call)
    # else:
        # with open(args.mvm_template, 'r') as mvmcall:
        #     mvmcall.format(dmy_date=base_utils.getLocalTime(hr_min=False), vox_covar=args.vox_covar,
        #                    mvm_table=outputFile)

if __name__ == '__main__':
    __main__()