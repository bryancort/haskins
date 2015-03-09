#!/usr/bin/python
# -------------------------------------------------------------------------------
# Name:        gen_roi.py
# Purpose:     Creates subject-specific ROIs from a search space and an activation map
#
# Author:      Bryan Cort
#
# Created:     12/15/2014
# -------------------------------------------------------------------------------


# If you use this program, please reference the introductory/description
# paper for the FATCAT toolbox:
#         Taylor PA, Saad ZS (2013).  FATCAT: (An Efficient) Functional
#         And Tractographic Connectivity Analysis Toolbox. Brain
#         Connectivity 3(5):523-535.

__author__ = 'cort'

import os
import sys
import argparse
import subprocess
from utils import base_utils, file_utils
from core import mri_data

# from pete:
# todo: if you wanted your life to be easier, you could run
# todo: @auto_tlrc -base TT_N27+tlrc -input anat_final.tb1234+orig.HEAD -init_xform CENTER - no_ss on each subject
# todo: and then you'd be guaranteed to have an anat_final*+tlrc


def gen_standard_anat(mri_subject, anat_tag='anat'):
    pass


def genArgParser():
    """
    Generate a command line argument parser for this script.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('patterns', nargs='+',
                        help='One or more unix-style wildcard expressions to generate the list of subject data '
                             'subdirectories.')

    mri_data_dir_default = None
    parser.add_argument('--mri_data_dir', default=mri_data_dir_default, required=True,
                        help='Directory containing scans. Default: {}'.format(mri_data_dir_default))

    search_space_default = None
    parser.add_argument('--search_space', default=search_space_default, required=True,
                        help='Mask defining the search space. Default: {}'.format(search_space_default))

    proc_run_default = "fastloc"
    parser.add_argument('--proc_run', default=proc_run_default, required=True,
                        help='Tag uniquely identifying the proc run to search for the activation map. '
                             'Default: {}'.format(proc_run_default))

    activation_map_pattern_default = None
    parser.add_argument('--activation_map_pattern', default=activation_map_pattern_default, required=True,
                        help='Pattern to match to find the activation map to define ROIs from for each subject. '
                             'Default: {}'.format(activation_map_pattern_default))

    #todo: merge this with warp_tag (keep this option, add help text from warp)
    anat_pattern_default = None
    parser.add_argument('--anat_pattern', default=anat_pattern_default, required=True,
                        help='Pattern to match to find the anat for each subject. '
                             'Default: {}'.format(anat_pattern_default))

    contrast_subbrick_default = 0
    parser.add_argument('--contrast_subbrick', default=contrast_subbrick_default,
                        help='Activation map subbrick to use. Should be the t-stat, NOT the coefficients.'
                             'Default: {}'.format(contrast_subbrick_default))

    warp_tag_default = None
    parser.add_argument('--warp_tag', default=warp_tag_default,
                        help="Argument to the -warp option of 3dfractionize. This "
                             ""
                             " From the AFNI 3dfractionize help:"
                             "If this option is used, 'wset' is a dataset that provides a transformation (warp) from "
                             "+orig coordinates to the coordinates of 'iset'.In this case, the output dataset will be "
                             "in +orig coordinates rather than the coordinatesof 'iset'.  With this option:** 'tset' "
                             "must be in +orig coordinates ** 'iset' must be in +acpc or +tlrc coordinates ** 'wset' "
                             "must be in the same coordinates as 'iset'"
                             'Default: {}'.format(warp_tag_default))

    output_dir_default = None
    parser.add_argument('--output_dir', default=output_dir_default,
                        help='Output directory (relative to the subject directory) for results. If none, output for '
                             'will be generated in the subject directory.'
                             'Default: {}'.format(output_dir_default))

    output_file_prefix_default = 'ROI_{}'.format(base_utils.getLocalTime())
    parser.add_argument('--output_file_prefix', default=output_file_prefix_default,
                        help='Output prefix for the final ROI. '
                             'Default: ROI_[DATE_TIME].nii.gz')

    roi_size_default = 500
    parser.add_argument('--roi_size', default=roi_size_default,
                        help='Number of voxels to include in the ROI. '
                             'Default: {}'.format(roi_size_default))

    clip_default = 0.2
    parser.add_argument('--clip', default=clip_default,
                        help='Clipping threshold for the mask. Passed directly to the -clip option of 3dfractionize.'
                             'Default: {}'.format(clip_default))

    cluster_thresh_default = -100000
    parser.add_argument('--thresh', default=cluster_thresh_default,
                        help="Default threshold for including voxels in the cluster. Don't change this unless you know "
                             "exactly what you're doing."
                             "Default: {} (an [roi_size] voxel cluster)".format(cluster_thresh_default))

    # todo: allow custom anat/func to be passed and override the ones in the proc_run?

    # fixme: revert to None when testing complete
    mask_output_prefix_default = 'int_mask_{}.nii.gz'.format(base_utils.getLocalTime())
    parser.add_argument('--mask_output_prefix', default=mask_output_prefix_default,
                        help="Name for the search space mask. If 'None', the intermediate mask will be discarded after "
                             "processing is complete. Default: {}".format(mask_output_prefix_default))

    # debugging and logging
    # report_default = False
    # parser.add_argument('-r', '--report', action='store_true', default=report_default,
    #                     help='Pass this flag to generate a run report.'
    #                          'Default: {}'.format(report_default))

    # debug_default = False
    # parser.add_argument('--debug', action='store_true', default=debug_default,
    #                     help='Pass this flag to run in debug mode.'
    #                          'Default: {}'.format(debug_default))
    return parser


def gen_subj_roi(search_space, activation_map_pattern, contrast_subbrick, warp_tag, mask_output_prefix):
    pass


def _debug(*cmd_args):
    sys.argv = [sys.argv[0]] + list(cmd_args)


# fixme
_debug_cmd = '--output_dir roi_output ' \
             '--search_space /data1/A182/mri_subjects/A182_ROI_Scripts/A182_BC_ROI_from_clust/vwfa+tlrc.HEAD ' \
             '--activation_map_pattern /data1/A182/mri_subjects/tb0027/tb0027.fastloc/stats.tb0027_REML+orig.HEAD ' \
             '--warp /data1/A182/mri_subjects/tb0027/tb0027.fastloc/Sag3DMPRAGEs002a1001_ns+tlrc.HEAD ' \
             '--contrast_subbrick 25'


def gen_roi(output_dir, *placeholder):

    # 3dFractionalize to warp (if needed) and downsample our mask to the subject
    # see example 2 in the 3dFractionalize help for details and explanation
    fract_call = "3dfractionize -template {subj_functional} -input {search_space_mask} -warp {subj_anat_tlrc} " \
    "-preserve -clip {clip_value} -prefix {temp_xformed_mask}".format(subj_functional=args.activation_map_tag,
                                                                      search_space_mask=args.search_space,
                                                                      subj_anat_tlrc=args.warp,
                                                                      clip_value=args.clip,
                                                                      temp_xformed_mask=mask_path)
    if not args.warp:
        fract_call = fract_call.replace('-warp ', '')

    out_file = os.path.join(args.output_dir, args.output_file_prefix)
    subprocess.call(fract_call, shell=True)

    # 3dROIMaker to generate our functionally defined ROI
    roimaker_call = "3dROIMaker -inset {subj_functional} -thresh {act_thresh} -prefix {outfile_name} " \
                    "-mask {temp_xformed_mask} -only_conn_top {roi_size}".format(subj_functional=act_map,
                                                                                 act_thresh=args.thresh,
                                                                                 outfile_name=out_file,
                                                                                 temp_xformed_mask=mask_path,
                                                                                 roi_size=args.roi_size)
    subprocess.call(roimaker_call, shell=True)

    if os.path.exists(os.path.join(args.output_dir, temp_mask_name)):
        os.remove(os.path.join(args.output_dir, temp_mask_name))


def __main__():
    scriptName = os.path.splitext(os.path.basename(__file__))[0]
    # if len(sys.argv) == 1 :
    #     _debug(*_debug_cmd.split(' '))
    parser = genArgParser()
    args = parser.parse_args()

    bad_paths = file_utils.check_paths(True, args.search_space, args.mri_data_dir)

    if bad_paths:
        print 'ERROR: The following paths do not exist'
        for p in bad_paths:
            print p
        return

    subj_dirs = file_utils.get_dirs_from_patterns(args.mri_data_dir, True, *args.patterns)
    for subj_dir in subj_dirs:
        subj_scan = mri_data.Scan(scan_id=os.path.split(subj_dir)[1], root_dir=subj_dir, proc_runs=(args.proc_run,))
        proc_run = subj_scan.proc_runs[args.proc_run]
        # check that we have the necessary files
        if not proc_run.active_stats_file and not proc_run.active_anat_file:
            print "{} is missing a required file; check the stats and anat in {}".format(subj_scan, proc_run)
            continue    # todo adjust this for when we override defaults

        # some filepath and data set specification
        temp_mask_name = 'mask_temp.nii.gz'
        mask_name = args.mask_output_prefix
        if not mask_name:
            mask_name = temp_mask_name

        act_map = proc_run.active_stats_file
        if args.activation_map_pattern:
            act_map = proc_run.set_active_stats_file(args.activation_map_pattern)
        act_map_volume = "{}'[{}]'".format(act_map, args.contrast_subbrick)
        anat = proc_run.active_anat_file
        if args.anat_pattern:
            anat = proc_run.set_active_anat_file(args.anat_pattern)

        #set the output dir
        subj_out_dir = subj_scan.root_dir
        if args.output_dir:
            subj_out_dir = os.path.join(subj_scan.root_dir, args.output_dir)
        if not os.path.exists(subj_out_dir):
            os.mkdir(subj_out_dir)

        mask_output_path = os.path.join(args.output_dir, mask_name)

        bad_paths = file_utils.check_paths(True, act_map, anat, subj_out_dir)

        if bad_paths:
            print 'ERROR: The following paths do not exist'
            for p in bad_paths:
                print p
            return

        gen_roi(subj_scan, proc_run, act_map_volume, anat, args.search_space, subj_out_dir, mask_output_path,
                args.roi_size, args.clip, args.cluster_thresh)





if __name__ == '__main__':
    __main__()


# Might not need these with the new 3dROIMaker feature
# def _gen_search_space_map():
#     pass
#
#
# def _get_hottest_vox():
#     pass
#
#
# def _cluster_from_vox():
#     pass
#
#
# def _roi_from_cluster():
#     pass
#
