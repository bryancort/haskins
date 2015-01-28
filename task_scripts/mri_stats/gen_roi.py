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
#   paper for the FATCAT toolbox:
#         Taylor PA, Saad ZS (2013).  FATCAT: (An Efficient) Functional
#         And Tractographic Connectivity Analysis Toolbox. Brain
#         Connectivity 3(5):523-535.

__author__ = 'cort'

import os
import argparse
import subprocess
from utils import base_utils, file_utils

# from pete:
# todo: if you wanted your life to be easier, you could run
# todo: @auto_tlrc -base TT_N27+tlrc -input anat_final.tb1234+orig.HEAD -init_xform CENTER - no_ss on each subject
# todo: and then you'd be guaranteed to have an anat_final*+tlrc

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
    parser.add_argument('--outputDir', default=output_dir_default,
                        help='Output directory for results. '
                             'Default: {}'.format(output_dir_default))

    output_file_prefix_default = 'ROI_[FUNCTIONAL_FILE]_[SEARCH_SPACE_MASK]'
    parser.add_argument('--output_file_prefix', default=output_dir_default,
                        help='Output prefix for the final ROI. '
                             'Default: {}'.format(output_file_prefix_default))

    roi_size_default = 500
    parser.add_argument('--roi_size', default=roi_size_default,
                        help='Number of voxels to include in the ROI. '
                             'Default: {}'.format(roi_size_default))

    clip_default = 0.2
    parser.add_argument('--clip', default=clip_default,
                        help='Clipping threshold for the mask. '
                             'Default: {}'.format(clip_default))

    cluster_thresh_default = 0
    parser.add_argument('--cluster_thresh', default=cluster_thresh_default,
                        help='Default threshold for including voxels in the cluster. '
                             'Default: {} (this will always result in an '
                             'N-voxel cluster)'.format(cluster_thresh_default))

    mask_output_name_default = None
    parser.add_argument('--mask_output_name', default=mask_output_name_default,
                        help='Name for the search space mask. '
                             'Default: {} (search space mask will be deleted '
                             'during cleanup)'.format(mask_output_name_default))

    # debugging and logging
    report_default = False
    parser.add_argument('-r', '--report', action='store_true', default=report_default,
                        help='Pass this flag to generate a run report.'
                             'Default: {}'.format(report_default))

    debug_default = False
    parser.add_argument('--debug', action='store_true', default=debug_default,
                        help='Pass this flag to run in debug mode.'
                             'Default: {}'.format(debug_default))
    return parser


def __main__():
    scriptName = os.path.splitext(os.path.basename(__file__))[0]
    parser = genArgParser()
    temp_mask_name = 'mask_temp.nii.gz'
    args = parser.parse_args()
    mask_path = args.mask_output_name
    if not mask_path:
        mask_path = temp_mask_name
    mask_path = os.path.join(args.output_dir, mask_path)
    # 3dFractionalize to warp (if needed) and downsample our mask to the subject
    # see example 2 in the 3dFractionalize help for details and explanation
    fract_call = "3dfractionize -template {subj_functional} -input {search_space_mask} -warp {subj_anat_tlrc} "
    "-preserve -clip {clip_value} -prefix {temp_xformed_mask}".format(subj_functional=args.activation_map,
                                                                      search_space_mask=args.search_space,
                                                                      subj_anat_tlrc=args.warp, clip_value=args.clip)
    if not args.warp:
        fract_call = fract_call.replace('-warp ', '')
    subprocess.call(fract_call, shell = True)  # 3dROIMaker to generate our functionally defined ROI
    # todo: add arg for, outfile_name
    # todo: test -mask, -thresh options
    subprocess.call("3dROIMaker -inset {subj_functional} -thresh {act_thresh} -prefix {outfile_name} "
                    "-mask {temp_xformed_mask}".format(), shell=True)

    if os.path.exists(os.path.join(args.output_dir, temp_mask_name)):
        os.remove(os.path.join(args.output_dir, temp_mask_name))


if __name__ == '__main__':
    __main__()


def gen_standard_anat(mri_subject, anat_tag='anat'):
    pass


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
