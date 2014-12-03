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

    mvm_template_default = os.path.normpath('gen_mvm_call_template.txt')
    parser.add_argument('--mvm_template', default=mvm_template_default,
                        help='mvm call template file'
                             'Default: {}'.format(mvm_template_default))

    mri_dir_default = None
    parser.add_argument('--mri_dir', default=mri_dir_default,
                        help='Directory containing stats files.\n'
                             'Default: {}'.format(mri_dir_default))

    outputDir_default = None
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

    within_vars_spec_file_default = None
    parser.add_argument('--within_vars_spec_file', default=within_vars_spec_file_default,
                        help='File specifying within subjects variable information for the study.\n'
                             'Default: {}'.format(within_vars_spec_file_default))

    between_vars_spec_file_default = None
    parser.add_argument('--between_vars_spec_file', default=between_vars_spec_file_default,
                        help='File specifying between subjects variable information for the study.\n'
                             'Default: {}'.format(between_vars_spec_file_default))

    num_jobs_default = '22'
    parser.add_argument('--num_jobs', default=num_jobs_default,
                        help='Number of jobs to run in parallel.\n'
                             'Default: {}'.format(num_jobs_default))

    mask_path_default = 'TT_MASK.nii.gz'
    parser.add_argument('--mask_path', default=mask_path_default,
                        help='Path to the mask to use in the MVM. This does not need to exist when this script is run, '
                             'but must be satisfied for the MVM to run; eg., if you leave this option as the default, '
                             '{d}, {d} must be a valid path (either relative from the location of your MVM call, or '
                             'absolute) when you run the MVM.\n'
                             'Default: {d}'.format(d=mask_path_default))

    body_entry_default = None
    parser.add_argument('--body_entry', default=body_entry_default,
                        help='Path to make to use in the MVM.\n'
                             'Default: {}'.format(body_entry_default))

    vox_covar_default = None
    parser.add_argument('--vox_covar', default=vox_covar_default,
                        help='Voxelwise covariate.\n'
                             'Default: {}'.format(vox_covar_default))

    vox_covar_pattern_default = None
    parser.add_argument('--vox_covar_pattern', default=vox_covar_pattern_default,
                        help='Pattern to match for file with the voxelwise covariate.\n'
                             'Default: {}'.format(vox_covar_pattern_default))

    proc_run_default = '.results'
    parser.add_argument('--proc_run', default=proc_run_default,
                        help='File containing condition information for the study.\n'
                             'Default: {}'.format(proc_run_default))

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
             '--outputDir /data1/bil/group_mvm_tables ' \
             '--mri_dir /data1/bil/mri_subjects ' \
             '--within_vars_spec_file /data1/bil/mvm_params/a187_within.txt ' \
             '--between_vars_spec_file /data1/bil/mvm_params/a187_between.txt ' \
             '--body_entry /data1/bil/mvm_params/a187_glts/test_glts.txt ' \
             '--output_table scaled_SFNR_vox_covar_table.txt ' \
             '--output_call scaled_SFNR_vox_covar_call.sh ' \
             '--proc_run .scale ' \
             '--vox_covar SFNR ' \
             '--vox_covar_pattern *SFNR*'


# todo: implement 3dinfo parsing instead of reading from the condition file
def _read_within_vars_spec_file(file_path):
    """
    Reads within subjects variable condition file
    """
    cft = file_utils.readTable2(fPath=file_path)
    var_perms = {tuple(entry[:-1]): entry[-1] for entry in cft[1:]}
    within_vars = {}
    for i, k in enumerate(cft[0][:-1]):
        within_vars[k] = set()
        for l in cft[1:]:
            within_vars[k].add(l[i])
    within_vars = {k: tuple(v) for k, v in within_vars.items()}

    return within_vars, var_perms


# todo
def _read_between_vars_spec_file(file_path):
    subj_map = {}
    between_vars = {}
    between_vars_table = file_utils.readTable2(fPath=file_path)
    header = between_vars_table[0]
    for var in header[1:]:
        between_vars[var] = set()
    data = between_vars_table[1:]
    for line in data:
        subj_map[line[0]] = {v: line[i] for i, v in enumerate(header[1:], start=1)}
        for i, entry in enumerate(header[1:], start=1):
            between_vars[entry].add(line[i])
    return subj_map, between_vars


def __main__():
    scriptName = os.path.splitext(os.path.basename(__file__))[0]
    parser = genArgParser()
    args = parser.parse_args()
    if len(sys.argv) == 1 or args.debug:
        _debug(*_debug_cmd.split(' '))
        args = parser.parse_args()
    args.mri_dir = os.path.normpath(args.mri_dir)
    args.outputDir = os.path.normpath(args.outputDir)
    args.within_vars_spec_file = os.path.normpath(args.within_vars_spec_file)
    output_table = os.path.join(args.outputDir, args.output_table)
    output_call = os.path.join(args.outputDir, args.output_call)

    within_vars, perm_map = _read_within_vars_spec_file(args.within_vars_spec_file)
    subj_map, between_vars = _read_between_vars_spec_file(args.between_vars_spec_file)

    scan_map = {}
    for s, v in subj_map:
        scan = mri_data.Scan(scan_id=s, data_dir=os.path.join(args.mri_dir, s))
        scan.add_proc_run(proc_tag=args.proc_run)
        scan_map[scan] = v

    bs_vars_entry = "-bsVars '{}'".format('*'.join(between_vars))
    ws_vars_entry = "-wsVars '{}'".format('*'.join(within_vars))

    # todo: read from file or args for AFNI implementation
    # for scan in scans:
    #     if scan.scan_id.startswith('hu'):
    #         scan_map[scan] = {'Site': 'HU'}
    #     elif scan.scan_id.startswith('ny'):
    #         scan_map[scan] = {'Site': 'NY'}

    mvmtable = mri_data.gen_mvm_table(scans_dict=scan_map, within=within_vars, between=between_vars,
                                      subbrick_mapping=perm_map, vox_covar=args.vox_covar,
                                      vox_covar_file_pattern=args.vox_covar_pattern, use_proc_run=args.proc_run)

    file_utils.writeTable(mvmtable, output_table, lineSep=' \\\n')

    with open(args.body_entry) as infile:
        body_entry = infile.read()
        num_glts = len(body_entry.split('-gltLabel')) - 1

    format_args = {'prefix': args.mvm_output_prefix,
                   'mvm_table': output_table,
                   'num_jobs': args.num_jobs,
                   'mask_path': args.mask_path,
                   'num_glts': num_glts,
                   'body_entry': body_entry,
                   'ws_vars_entry': ws_vars_entry,
                   'bs_vars_entry': bs_vars_entry}

    if args.vox_covar:
        format_args['vox_covar_entry'] = "-vVars '{}'".format(args.vox_covar)

    with open(args.mvm_template, 'r') as mvmcall:
        final_call = mvmcall.read().format(**format_args)
        with open(output_call, 'w') as mvmcall_out:
            mvmcall_out.write(final_call)


if __name__ == '__main__':
    __main__()