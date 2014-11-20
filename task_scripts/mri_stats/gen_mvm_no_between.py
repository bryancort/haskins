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

    debug_default = False
    parser.add_argument('--debug', action='store_true', default=debug_default,
                        help='Pass this flag to run in debug mode.'
                             'Default: {}'.format(debug_default))

    mvm_output_prefix_default = 'output_mvm_{}.sh'.format(base_utils.getLocalTime())
    parser.add_argument('--mvm_output_prefix', default=mvm_output_prefix_default,
                        help='mvm call template file'
                             'Default: {}'.format(mvm_output_prefix_default))

    mvm_template_default = os.path.normpath('mvm_call_template.txt')
    parser.add_argument('--mvm_template', default=mvm_template_default,  # todo: improve
                        help='mvm call template file'
                             'Default: {}'.format(mvm_template_default))

    mri_dir_default = os.path.normpath('/data1/bil/mri_subjects')
    parser.add_argument('--mri_dir', default=mri_dir_default,
                        help='Directory containing stats files.\n'
                             'Default: {}'.format(mri_dir_default))

    outputDir_default = os.path.normpath('/data1/bil/group_mvm_tables')
    parser.add_argument('--outputDir', default='/data1/bil/group_mvm_tables',
                        help='Output directory for MVM call and data table.\n'
                             'Default: {}'.format(outputDir_default))

    output_table_name_default = 'mvm_table_{}.txt'.format(base_utils.getLocalTime(hr_min=False))
    parser.add_argument('--output_table_name', default=output_table_name_default,
                        help='Name (without preceding path) of the table list_attrs file.\n'
                             'Default: {}'.format(output_table_name_default))

    output_call_name_default = 'mvm_call_{}.sh'.format(base_utils.getLocalTime(hr_min=False))
    parser.add_argument('--output_call_name', default=output_call_name_default,
                        help='Name (without preceding path) of the call list_attrs file.\n'
                             'Default: {}'.format(output_call_name_default))

    condition_file_default = os.path.normpath('/data1/bil/mri_subjects/a187_within.txt')
    parser.add_argument('--condition_file', default=condition_file_default,
                        help='File containing condition information for the study.\n'
                             'Default: {}'.format(condition_file_default))

    num_jobs_default = 22
    parser.add_argument('--num_jobs', default=num_jobs_default,
                        help='Number of jobs to run in parallel.\n'
                             'Default: {}'.format(num_jobs_default))

    mask_path_default = 'TT_MASK.nii.gz'
    parser.add_argument('--mask_path', default=mask_path_default,
                        help='Path to make to use in the MVM.\n'
                             'Default: {}'.format(mask_path_default))

    glt_specs_default = 'test_glts.txt'
    parser.add_argument('--glt_specs', default=glt_specs_default,
                        help='Path to make to use in the MVM.\n'
                             'Default: {}'.format(glt_specs_default))

    vox_covar_default = None
    parser.add_argument('--vox_covar', default=vox_covar_default,
                        help='Voxelwise covariate.\n'
                             'Default: {}'.format(vox_covar_default))

    vox_covar_pattern_default = None
    parser.add_argument('--vox_covar_pattern', default=vox_covar_pattern_default,
                        help='Pattern to match for file with the voxelwise covariate.\n'
                             'Default: {}'.format(vox_covar_pattern_default))

    proc_run_default = 'results'
    parser.add_argument('--proc_run', default=proc_run_default,
                        help='File containing condition information for the study.\n'
                             'Default: {}'.format(proc_run_default))

    parser.add_argument('--subjects', nargs='+',
                        help='List of subjects to include in the mvm.\n'
                             'Required argument.')

    # script action params
    report_default = False
    parser.add_argument('-r', '--report', action='store_true', default=report_default,
                        help='Pass this flag to generate a run report.'
                             'Default: {}'.format(report_default))
    return parser


def _debug(*cmd_args):
    sys.argv = [sys.argv[0]] + list(cmd_args)


_debug_cmd = '--subjects hu_AA380_16_3_13 hu_AC513_25_4_12 hu_AE239 ny039 ny060 ny032 ' \
             '--mvm_output_prefix scaled_SFNR_vox_covar ' \
             '--mvm_template /data1/scripts_refactor/haskins/task_scripts/mri_stats/mvm_call_template_vox_covar.txt ' \
             '--outputDir /data1/bil/group_mvms_10_29_14 ' \
             '--output_table scaled_SFNR_vox_covar_table.txt ' \
             '--output_call scaled_SFNR_vox_covar_call.sh ' \
             '--proc_run scale ' \
             '--vox_covar SFNR ' \
             '--vox_covar_pattern *SFNR*'


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
    args.outputDir = os.path.normpath(args.outputDir)
    args.condition_file = os.path.normpath(args.condition_file)
    output_table = os.path.join(args.outputDir, args.output_table)
    output_call = os.path.join(args.outputDir, args.output_call)

    scans = []
    for s in args.subjects:
        scan = mri_data.Scan(scan_id=s, data_dir=os.path.join(args.mri_dir, s))
        scan.add_proc_run(proc_tag=args.proc_run)
        scans.append(scan)

    within_vars, perm_map = read_condition_file(args.condition_file)
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

    with open(args.glt_specs) as infile:
        glt_entry = infile.read()
        num_glts = sum(1 for line in infile)

    format_args = {'prefix': args.mvm_output_prefix,
                   'mvm_table': output_table,
                   'num_jobs': args.num_jobs,
                   'mask_path': args.mask_path,
                   'num_glts': num_glts,
                   'glt_entry': glt_entry}

    if args.vox_covar:
        format_args['vox_covar_entry'] = "-vVars '{}'".format(args.vox_covar)

    # if args.vox_covar:
    with open(args.mvm_template, 'r') as mvmcall:
        final_call = mvmcall.read().format(**format_args)
        with open(output_call, 'w') as mvmcall_out:
            mvmcall_out.write(final_call)
            # else:
            # with open(args.mvm_template, 'r') as mvmcall:
            # mvmcall.format(dmy_date=base_utils.getLocalTime(hr_min=False), vox_covar=args.vox_covar,
            #                    mvm_table=outputFile)


if __name__ == '__main__':
    __main__()