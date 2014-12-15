#!/usr/bin/python
# -------------------------------------------------------------------------------
# Name:        gen_roi.py
# Purpose:     Creates subject-specific ROIs from a search space and an activation map
#
# Author:      Bryan Cort
#
# Created:     12/15/2014
# -------------------------------------------------------------------------------
__author__ = 'cort'

import os
import argparse
from utils import base_utils, file_utils

def genArgParser():
    """
    Generate a command line argument parser for this script.
    """
    parser = argparse.ArgumentParser()

    debug_default = False
    parser.add_argument('--debug', action='store_true', default=debug_default,
                        help='Pass this flag to run in debug mode.'
                             'Default: {}'.format(debug_default))

    # todo: some output params will go here
    # mvm_output_prefix_default = 'output_mvm_{}.sh'.format(base_utils.getLocalTime())
    # parser.add_argument('--mvm_output_prefix', default=mvm_output_prefix_default,
    #                     help='mvm call template file'
    #                          'Default: {}'.format(mvm_output_prefix_default))
    #
    # outputDir_default = None
    # parser.add_argument('--outputDir', default=outputDir_default,
    #                     help='Output directory for MVM call and data table.\n'
    #                          'Default: {}'.format(outputDir_default))

    search_space_default = None
    parser.add_argument('--search_space', default=search_space_default,
                        help='Mask defining the search space.\n'
                             'Default: {}'.format(search_space_default))

    activation_map_default = None
    parser.add_argument('--activation_map', default=activation_map_default,
                        help='Activation map to define ROIs from.\n'
                             'Default: {}'.format(activation_map_default))

    roi_size_default = 500
    parser.add_argument('--roi_size', default=roi_size_default,
                        help='Number of voxels to include in the ROI.\n'
                             'Default: {}'.format(roi_size_default))

    # script action params
    report_default = False
    parser.add_argument('-r', '--report', action='store_true', default=report_default,
                        help='Pass this flag to generate a run report.'
                             'Default: {}'.format(report_default))
    return parser

def _gen_search_space_map():
    pass

def _get_hottest_vox():
    pass

def _cluster_from_vox():
    pass

def _roi_from_cluster():
    pass

