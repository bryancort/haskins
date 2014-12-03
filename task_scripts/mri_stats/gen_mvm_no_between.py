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
    # todo: Fix defaults, add support for stats file tag input (currently defaults to REML)
    parser = argparse.ArgumentParser()

    debug_default = False
    parser.add_argument('--debug', action='store_true', default=debug_default,
                        help='Pass this flag to run in debug mode.'
                             'Default: {}'.format(debug_default))

    mvm_output_prefix_default = 'output_mvm_{}.sh'.format(base_utils.getLocalTime())
    parser.add_argument('--mvm_output_prefix', default=mvm_output_prefix_default,
                        help='mvm output log filename. '
                             'Default: {}'.format(mvm_output_prefix_default))

    mvm_template_default = os.path.normpath('mvm_call_template_no_between.txt')
    parser.add_argument('--mvm_template', default=mvm_template_default,
                        help='mvm call template file. '
                             'Default: {}'.format(mvm_template_default))

    mri_dir_default = None # os.path.normpath('/data1/bil/mri_subjects')
    parser.add_argument('--mri_dir', default=mri_dir_default,
                        help='Directory containing scans. '
                             'Default: {}'.format(mri_dir_default))

    output_dir_default = None # os.path.normpath('/data1/bil/group_mvm_tables')
    parser.add_argument('--output_dir', default='/data1/bil/group_mvm_tables',
                        help='Output directory for MVM call and data table. '
                             'Default: {}'.format(output_dir_default))

    output_table_name_default = 'mvm_table_{}.txt'.format(base_utils.getLocalTime(hr_min=False))
    parser.add_argument('--output_table_name', default=output_table_name_default,
                        help='Name (without preceding path) of the table output file. '
                             'Default: {}'.format(output_table_name_default))

    output_call_name_default = 'mvm_call_{}.sh'.format(base_utils.getLocalTime(hr_min=False))
    parser.add_argument('--output_call_name', default=output_call_name_default,
                        help='Name (without preceding path) of the call output file. '
                             'Default: {}'.format(output_call_name_default))

    condition_file_default = None # os.path.normpath('/data1/bil/mri_subjects/a187_within.txt')
    parser.add_argument('--condition_file', default=condition_file_default,
                        help='File containing condition information for the study. '
                             'Default: {}'.format(condition_file_default))

    num_jobs_default = 22
    parser.add_argument('--num_jobs', default=num_jobs_default,
                        help='Number of jobs to run in parallel. '
                             'Default: {}'.format(num_jobs_default))

    mask_path_default = 'TT_MASK.nii.gz'
    parser.add_argument('--mask_path', default=mask_path_default,
                        help='Path to make to use in the MVM. '
                             'Default: {}'.format(mask_path_default))

    glt_specs_default = 'test_glts.txt'
    parser.add_argument('--glt_specs', default=glt_specs_default,
                        help='Path to the file containing the glms. Formatting is the same as normal MVM, including any '
                             'backslash line continuations. '
                             'Default: {}'.format(glt_specs_default))

    vox_covar_default = None
    parser.add_argument('--vox_covar', default=vox_covar_default,
                        help='Voxelwise covariate name. '
                             'Default: {}'.format(vox_covar_default))

    vox_covar_pattern_default = None
    parser.add_argument('--vox_covar_pattern', default=vox_covar_pattern_default,
                        help='Pattern to match for file with the voxelwise covariate.'
                             'NB: this needs to match a SINGLE file; if you have a .HEAD/.BRIK pair, '
                             'specify [PATTERN].HEAD, eg. *SFNRN*.HEAD'
                             'Default: {}'.format(vox_covar_pattern_default))

    proc_run_default = 'results'
    parser.add_argument('--proc_run', default=proc_run_default,
                        help='Pattern uniquely identifying the proc run directory within each subject directory.'
                             'Example: *.srtt*'
                             'Default: {}'.format(proc_run_default))

    parser.add_argument('--subjects', nargs='+',
                        help='List of subjects to include in the mvm. '
                             'Required argument.')

    # script action params
    report_default = False
    parser.add_argument('-r', '--report', action='store_true', default=report_default,
                        help='Pass this flag to generate a run report.'
                             'Default: {}'.format(report_default))
    return parser


def _debug(*cmd_args):
    sys.argv = [sys.argv[0]] + list(cmd_args)

_debug_cmd = '--subjects tb5688 tb5689 ' \
             '--mri_dir /data1/A182/mri_subjects ' \
             '--condition_file /data1/scripts_refactor/haskins/task_scripts/mri_stats/temp_test/a182_test.txt ' \
             '--mvm_output_prefix test_new_mvm_gen ' \
             '--mvm_template /data1/scripts_refactor/haskins/task_scripts/mri_stats/mvm_call_template_no_between.txt ' \
             '--output_dir /data1/scripts_refactor/haskins/task_scripts/mri_stats/temp_test ' \
             '--output_table test_new_mvm_gen_table5.txt ' \
             '--output_call test_new_mvm_gen_scr5.sh ' \
             '--proc_run .srtt' #\
             #'--vox_covar SFNR ' \
             #'--vox_covar_pattern *SFNR*.HEAD'


# todo: implement 3dinfo parsing instead of reading from the condition file
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
    args.output_dir = os.path.normpath(args.output_dir)
    args.condition_file = os.path.normpath(args.condition_file)
    output_table = os.path.join(args.output_dir, args.output_table_name)
    output_call = os.path.join(args.output_dir, args.output_call_name)

    scans = []
    for s in args.subjects:
        scan = mri_data.Scan(scan_id=s, data_dir=os.path.join(args.mri_dir, s))
        scan.add_proc_run(proc_tag=args.proc_run)
        scans.append(scan)

    within_vars, perm_map = read_condition_file(args.condition_file)
    between_vars = {'Site': ('HU', 'NY')}
    # todo: read from file or args for AFNI implementation
    scan_map = {}
    # todo: some between subjs variable magic here
    for scan in scans:
        scan_map[scan] = {}     # ugly placeholder

    mvmtable = mri_data.gen_mvm_table(scans_dict=scan_map, within=within_vars, between=None,
                                      subbrick_mapping=perm_map, vox_covar=args.vox_covar,
                                      vox_covar_file_pattern=args.vox_covar_pattern, use_proc_run=args.proc_run)

    num_glts = 0
    with open(args.glt_specs) as infile:
        glt_entry = infile.read()
        num_glts = len(glt_entry.split('\n'))

    format_args = {'prefix': args.mvm_output_prefix,
                   'mvm_table': output_table,
                   'num_jobs': args.num_jobs,
                   'mask_path': args.mask_path,
                   'num_glts': num_glts,
                   'glt_entry': glt_entry,
                   'ws_vars_entry': "-wsVars '{}'".format('*'.join(within_vars))}

    if args.vox_covar:
        format_args['vox_covar_entry'] = "-vVars '{}'".format(args.vox_covar)
    else:
        format_args['vox_covar_entry'] = ""

    # if args.vox_covar:
    with open(args.mvm_template, 'r') as mvmcall:
        final_call = mvmcall.read().format(**format_args)
        final_call = final_call.replace('\n \\\n', '\n')
        with open(output_call, 'w') as mvmcall_out:
            mvmcall_out.write(final_call)
    file_utils.writeTable(mvmtable, output_table, lineSep=' \\\n')
            # else:
            # with open(args.mvm_template, 'r') as mvmcall:
            # mvmcall.format(dmy_date=base_utils.getLocalTime(hr_min=False), vox_covar=args.vox_covar,
            #                    mvm_table=outputFile)


if __name__ == '__main__':
    __main__()