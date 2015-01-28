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

    search_space_default = None
    parser.add_argument('--search_space', default=search_space_default, required=True,
                        help='Mask defining the search space. '
                             'Default: {}'.format(search_space_default))

    activation_map_default = None
    parser.add_argument('--activation_map', default=activation_map_default, required=True,
                        help='Activation map to define ROIs from. '
                             'Default: {}'.format(activation_map_default))

    activation_map_subbrick_default = 0
    parser.add_argument('--activation_map_subbrick', default=activation_map_subbrick_default,
                        help='Activation map subbrick to use. '
                             'Default: {}'.format(activation_map_subbrick_default))

    warp_default = None
    parser.add_argument('--warp', default=warp_default,
                        help="Argument to the -warp option of 3dFractionalize. From the AFNI 3dFractionalize help:"
                             "If this option is used, 'wset' is a dataset that provides a transformation (warp) from "
                             "+orig coordinates to the coordinates of 'iset'.In this case, the output dataset will be "
                             "in +orig coordinates rather than the coordinatesof 'iset'.  With this option:** 'tset' "
                             "must be in +orig coordinates ** 'iset' must be in +acpc or +tlrc coordinates ** 'wset' "
                             "must be in the same coordinates as 'iset'"
                             'Default: {}'.format(warp_default))

    output_dir_default = '.'
    parser.add_argument('--output_dir', default=output_dir_default,
                        help='Output directory for results. '
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
                        help='Clipping threshold for the mask. '
                             'Default: {}'.format(clip_default))

    cluster_thresh_default = 0
    parser.add_argument('--thresh', default=cluster_thresh_default,
                        help='Default threshold for including voxels in the cluster. '
                             'Default: {} (this will always result in an '
                             'N-voxel cluster)'.format(cluster_thresh_default))

    mask_output_prefix_default = 'int_mask.nii.gz'  # fixme: revert to None when testing complete
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


def _debug(*cmd_args):
    sys.argv = [sys.argv[0]] + list(cmd_args)


# fixme
_debug_cmd = '--output_dir /data1/A182/mri_subjects/A182_ROI_Scripts/A182_BC_ROI_from_clust/output ' \
             '--search_space /data1/A182/mri_subjects/A182_ROI_Scripts/A182_BC_ROI_from_clust/vwfa+tlrc.HEAD ' \
             '--activation_map /data1/A182/mri_subjects/tb0027/tb0027.fastloc/stats.tb0027_REML+orig.HEAD ' \
             '--warp /data1/A182/mri_subjects/tb0027/tb0027.fastloc/Sag3DMPRAGEs002a1001_ns+tlrc.HEAD ' \
             '--activation_map_subbrick 25'


def __main__():
    scriptName = os.path.splitext(os.path.basename(__file__))[0]
    if len(sys.argv) == 1:
        _debug(*_debug_cmd.split(' '))
    parser = genArgParser()
    args = parser.parse_args()

    bad_paths = file_utils.check_paths(True, args.output_dir, args.activation_map, args.search_space)

    if bad_paths:
        print 'ERROR: The following paths do not exist'
        for p in bad_paths:
            print p
        return

    # some filepath and data set specification
    temp_mask_name = 'mask_temp.nii.gz'
    mask_path = args.mask_output_prefix
    if not mask_path:
        mask_path = temp_mask_name
    mask_path = os.path.join(args.output_dir, mask_path)

    act_map = "{}'[{}]'".format(args.activation_map, args.activation_map_subbrick)

    # if args.output_file_prefix == None:
    #     args.output_file_prefix = 'ROI_{}__{}_'.format(os.path.split(args.activation_map)[1],
    #                                                      os.path.split(args.search_space)[1])

    # 3dFractionalize to warp (if needed) and downsample our mask to the subject
    # see example 2 in the 3dFractionalize help for details and explanation
    fract_call = "3dfractionize -template {subj_functional} -input {search_space_mask} -warp {subj_anat_tlrc} " \
    "-preserve -clip {clip_value} -prefix {temp_xformed_mask}".format(subj_functional=args.activation_map,
                                                                      search_space_mask=args.search_space,
                                                                      subj_anat_tlrc=args.warp, clip_value=args.clip,
                                                                      temp_xformed_mask=mask_path)
    if not args.warp:
        fract_call = fract_call.replace('-warp ', '')
    out_file = os.path.join(args.output_dir, args.output_file_prefix)
    subprocess.call(fract_call, shell=True)  # 3dROIMaker to generate our functionally defined ROI
    roimaker_call = "3dROIMaker -inset {subj_functional} -thresh {act_thresh} -prefix {outfile_name} " \
                    "-mask {temp_xformed_mask} -only_conn_top {roi_size}".format(subj_functional=act_map,
                                                                                 act_thresh=args.thresh,
                                                                                 outfile_name=out_file,
                                                                                 temp_xformed_mask=mask_path,
                                                                                 roi_size=args.roi_size)
    subprocess.call(roimaker_call, shell=True)

    if os.path.exists(os.path.join(args.output_dir, temp_mask_name)):
        os.remove(os.path.join(args.output_dir, temp_mask_name))


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
