#!/usr/bin/python
# -------------------------------------------------------------------------------
# Name:        task_scripts.gen_mvm_table_txt
# Purpose:      generates a data table and shell call for use with 3dMVM
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
                        help='Prefix for the output log generated by 3dMVM.'
                             'Default: {}'.format(mvm_output_prefix_default))

    mvm_template_default = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'gen_mvm_call_template.txt')
    parser.add_argument('--mvm_template', default=mvm_template_default,
                        help="mvm call template file. Do not change this unless you know what you're doing."
                             "Default: {}".format(mvm_template_default))

    mri_dir_default = None
    parser.add_argument('--mri_dir', default=mri_dir_default,
                        help='Directory containing mri scan data. '
                             'Default: {}'.format(mri_dir_default))

    proc_run_default = '.results'
    parser.add_argument('--proc_run', default=proc_run_default,
                        help='Unique substring identifying the directory with processed data to use for each scan. NOT '
                             'a wildcard expression. '
                             'Default: {}'.format(proc_run_default))

    output_dir_default = None
    parser.add_argument('--output_dir', default=output_dir_default,
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

    within_vars_spec_file_default = None
    parser.add_argument('--within_vars_spec_file', default=within_vars_spec_file_default,
                        help='File specifying within subjects variable information for the study. See README.md for '
                             'more details and examples. '
                             'Default: {}'.format(within_vars_spec_file_default))

    between_vars_spec_file_default = None
    parser.add_argument('--between_vars_spec_file', default=between_vars_spec_file_default,
                        help='File specifying between subjects variable information for the study. See README.md for '
                             'more details and examples. '
                             'Default: {}'.format(between_vars_spec_file_default))

    body_entry_default = None
    parser.add_argument('--body_entry', default=body_entry_default,
                        help='Body of the MVM call. Should include (at least) GLT numbers and specifications. '
                             'See README.md for more details and examples. '
                             'Default: {}'.format(body_entry_default))

    num_jobs_default = '22'
    parser.add_argument('--num_jobs', default=num_jobs_default,
                        help='Number of jobs to run in parallel. '
                             'Default: {}'.format(num_jobs_default))

    mask_path_default = 'TT_MASK.nii.gz'
    parser.add_argument('--mask_path', default=mask_path_default,
                        help='Path to the mask to use in the MVM. This does not need to exist when this script is run, '
                             'but must be satisfied for the MVM to run; eg., if you leave this option as the default, '
                             '{d}, {d} must be a valid path (either relative from the location of your MVM call, or '
                             'absolute) when you run the MVM. '
                             'Default: {d}'.format(d=mask_path_default))

    quant_covars_default = None
    parser.add_argument('--quant_covars', default=quant_covars_default,
                        help='Quantitative covariates in the format: qcv1,qcv2,...,qcvn '
                             'Default: {}'.format(quant_covars_default))

    quant_covars_centers_default = None
    parser.add_argument('--quant_covars_centers', default=quant_covars_centers_default,
                        help='Quantitative covariate centers in the format: qcv1_center,qcv2_center,...,qcvn_center '
                             'Default: {}'.format(quant_covars_centers_default))

    vox_covar_default = None
    parser.add_argument('--vox_covar', default=vox_covar_default,
                        help='Voxelwise covariate name. '
                             'Default: {}'.format(vox_covar_default))

    vox_covar_pattern_default = None
    parser.add_argument('--vox_covar_pattern', default=vox_covar_pattern_default,
                        help='Pattern to match for file with the voxelwise covariate. This must match a single file in '
                             'the selected proc_run directory of each scan; this means that if you specify a pattern '
                             'that matches .HEAD/.BRIK files, be sure to add .HEAD. ie., instead of '
                             '*my_covariate_file*, use *my_covariate_file*.HEAD for this option.'
                             'Default: {}'.format(vox_covar_pattern_default))

    # script action params
    report_default = False
    parser.add_argument('-r', '--report', action='store_true', default=report_default,
                        help='Pass this flag to generate a run report.'
                             'Default: {}'.format(report_default))
    return parser


def _debug(*cmd_args):
    sys.argv = [sys.argv[0]] + list(cmd_args)


_debug_cmd = '--mvm_output_prefix scaled_SFNR_vox_covar ' \
             '--output_dir /data1/bil/group_mvm_tables_test ' \
             '--mri_dir /data1/bil/mri_subjects ' \
             '--within_vars_spec_file /data1/bil/mvm_params_test/a187_within.txt ' \
             '--between_vars_spec_file /data1/bil/mvm_params_test/a187_between.txt ' \
             '--body_entry /data1/bil/mvm_params_test/a187_glts.txt ' \
             '--output_table scaled_SFNR_vox_covar_table.txt ' \
             '--output_call scaled_SFNR_vox_covar_call.sh ' \
             '--proc_run .scale ' \
             '--quant_covars dummy_covar1,dummy_covar2 ' \
             '--vox_covar SFNR ' \
             '--vox_covar_pattern *SFNR*.HEAD'


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


def _read_between_vars_spec_file(file_path, qvars):
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
    for qvar in qvars:
        del between_vars[qvar]
    return subj_map, between_vars


def __main__():
    scriptName = os.path.splitext(os.path.basename(__file__))[0]
    parser = genArgParser()
    args = parser.parse_args()
    # if len(sys.argv) == 1 or args.debug:
    if args.debug:
        _debug(*_debug_cmd.split(' '))
        args = parser.parse_args()
    args.mri_dir = os.path.normpath(args.mri_dir)
    args.output_dir = os.path.normpath(args.output_dir)
    args.within_vars_spec_file = os.path.normpath(args.within_vars_spec_file)
    args.between_vars_spec_file = os.path.normpath(args.between_vars_spec_file)
    output_table = os.path.join(args.output_dir, args.output_table_name)
    output_call = os.path.join(args.output_dir, args.output_call_name)

    quant_covars_entry = ''
    quant_covars_list = []
    quant_covars_centers_entry = ''
    if args.quant_covars:
        quant_covars_entry = "-qVars '{}'".format(args.quant_covars)
        quant_covars_list.extend(args.quant_covars.split(','))
        if args.quant_covars_centers:
            quant_covars_centers_entry = "-qVarCenters '{}'".format(args.quant_covars_centers)

    within_vars, perm_map = _read_within_vars_spec_file(args.within_vars_spec_file)
    subj_map, between_vars = _read_between_vars_spec_file(args.between_vars_spec_file, quant_covars_list)

    scan_map = {}
    for s, v in subj_map.iteritems():
        scan = mri_data.Scan(scan_id=s, data_dir=os.path.join(args.mri_dir, s))
        scan.add_proc_run(proc_tag=args.proc_run)
        scan_map[scan] = v

    if args.vox_covar is None:
        args.vox_covar = ""

    vox_covar_entry = ""
    bs_vars_entry = ""

    bs_vars_expr = '*'.join(between_vars)
    for qvar in quant_covars_list:
        bs_vars_expr += '+{}'.format(qvar)
    bs_vars_expr += '+{}'.format(args.vox_covar)
    bs_vars_expr = bs_vars_expr.strip('+')
    if args.vox_covar:
        vox_covar_entry = "-vVars '{}'".format(args.vox_covar)

    if bs_vars_expr:
        bs_vars_entry = "-bsVars '{}'".format(bs_vars_expr)

    ws_vars_entry = "-wsVars '{}'".format('*'.join(within_vars))

    mvmtable = mri_data.gen_mvm_table(scans_dict=scan_map, within=within_vars, between=between_vars,
                                      subbrick_mapping=perm_map, vox_covar=args.vox_covar, covars=quant_covars_list,
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
                   'bs_vars_entry': bs_vars_entry,
                   'quant_covars_entry': quant_covars_entry,
                   'quant_covars_centers_entry': quant_covars_centers_entry,    # todo: test
                   'vox_covar_entry': vox_covar_entry}

    with open(args.mvm_template, 'r') as mvmcall:
        final_call = mvmcall.read().format(**format_args)
        final_call = final_call.replace('\n \\\n', '\n')
        with open(output_call, 'w') as mvmcall_out:
            mvmcall_out.write(final_call)
    file_utils.writeTable(mvmtable, output_table, lineSep=' \\\n')


if __name__ == '__main__':
    __main__()