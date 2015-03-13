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
# Taylor PA, Saad ZS (2013).  FATCAT: (An Efficient) Functional
#         And Tractographic Connectivity Analysis Toolbox. Brain
#         Connectivity 3(5):523-535.

__author__ = 'cort'

import os
import sys
import glob
import fnmatch
import argparse
import subprocess
import traceback
from utils import base_utils, file_utils
from core import mri_data
from utils.haskins_exceptions import AfniError, FileError

# from pete:
# todo: if you wanted your life to be easier, you could run
# todo: @auto_tlrc -base TT_N27+tlrc -input anat_final.tb1234+orig.HEAD -init_xform CENTER - no_ss on each subject
# todo: and then you'd be guaranteed to have an anat_final*+tlrc


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
    parser.add_argument('--search_space', default=search_space_default,
                        help='Mask defining the search space. Default: {}'.format(search_space_default))

    proc_run_default = ".fastloc"
    parser.add_argument('--proc_run', default=proc_run_default,
                        help='Tag uniquely identifying the proc run to search for the activation map. '
                             'Default: {}'.format(proc_run_default))

    func_pattern_default = None
    parser.add_argument('--func_pattern', default=func_pattern_default, required=True,
                        help='Pattern to match to find the functional activation map to define ROIs from for each '
                             'subject. Commonly stats.*REML+*.HEAD* or stats.??????+*.HEAD*'
                             'Default: {}'.format(func_pattern_default))

    anat_tlrc_pattern_default = None
    parser.add_argument('--anat_tlrc_pattern', default=anat_tlrc_pattern_default,
                        help='Pattern to match to find the anat for each subject. This anat file will be passed to the '
                             '-warp option of 3dfractionize. This should be in standard space; it is used for the '
                             'transformation from standard space back to subject space. For more details, see: '
                             'http://afni.nimh.nih.gov/pub/dist/doc/program_help/3dfractionize.html '
                             'Default: {}'.format(anat_tlrc_pattern_default))

    contrast_subbrick_default = 26  # 26 is the A182 print - falsefont tstat
    parser.add_argument('--contrast_subbrick', default=contrast_subbrick_default,
                        help='Activation map subbrick to use. Should be the t-stat, NOT the coefficients.'
                             'Default: {}'.format(contrast_subbrick_default))

    output_dir_default = None
    parser.add_argument('--output_dir', default=output_dir_default,
                        help='Output directory (relative to the subject directory) for results. If none, output for '
                             'will be generated in the subject directory.'
                             'Default: {}'.format(output_dir_default))

    output_roi_prefix_default = 'ROI_{}'.format(base_utils.getLocalTime())
    parser.add_argument('--output_roi_prefix', default=output_roi_prefix_default,
                        help='Output prefix for the final ROI. '
                             'Default: ROI_[DATE_TIME].nii.gz')

    roi_size_default = 200
    parser.add_argument('--roi_size', default=roi_size_default,
                        help='Number of voxels to include in the ROI. '
                             'Default: {}'.format(roi_size_default))

    clip_default = 0.2
    parser.add_argument('--clip', default=clip_default,
                        help='Clipping threshold for the mask. Passed directly to the -clip option of 3dfractionize.'
                             'Default: {}'.format(clip_default))

    threshold_default = -100000
    parser.add_argument('--threshold', default=threshold_default,
                        help="Default threshold for including voxels in the cluster. Don't change this unless you know "
                             "exactly what you're doing."
                             "Default: {} (an [roi_size] voxel cluster)".format(threshold_default))

    warped_ss_prefix_default = None
    parser.add_argument('--warped_ss_prefix', default=warped_ss_prefix_default,
                        help="Name to save the subject space (+orig) search space mask. If 'None', the "
                             "intermediate mask will be discarded after processing is complete. "
                             "Default: {}".format(warped_ss_prefix_default))

    copy_anat_pattern_default = None
    parser.add_argument('--copy_anat_pattern', default=copy_anat_pattern_default,
                        help="Copy anat file(s) matching this pattern to the output_dir (probably for checking your "
                             "results using afni). Default: {}".format(copy_anat_pattern_default))

    warped_ss_exists_default = False
    parser.add_argument('--warped_ss_exists', action="store_true", default=warped_ss_exists_default,
                        help="Pass this flag to use an existing warped search space (with prefix specified from "
                             "--warped_ss_prefix) in output_dir. Default: {}".format(warped_ss_exists_default))

    make_snapshots_default = None
    parser.add_argument('--make_snapshots_default', default=make_snapshots_default,
                        help="Placeholder snapshots option. Default: {}".format(make_snapshots_default))

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


_debug_cmd = '--mri_data_dir /data1/A182/mri_subjects ' \
             '--search_space /data1/A182/mri_subjects/A182_ROI_Scripts/A182_BC_ROI_from_clust/vwfa+tlrc.HEAD ' \
             '--func_pattern stats.*REML+*.HEAD* ' \
             '--anat_tlrc *ns+tlrc.HEAD ' \
             '--contrast_subbrick 25 ' \
             '--warped_ss_prefix vwfa_ss+orig ' \
             '--copy_anat_pattern *ns+orig* ' \
             '--output_dir rois/func_roi_vwfa ' \
             '--roi_size 100 ' \
             '--output_roi_prefix vwfa_100 ' \
             '--warped_ss_exists ' \
             'tb5688 tb5689 tb5722'

# _debug_cmd = '--mri_data_dir /data1/A182/mri_subjects ' \
#              '--func_pattern stats.*REML+*.HEAD* ' \
#              '--contrast_subbrick 25 ' \
#              '--warped_ss_prefix vwfa_ss+orig ' \
#              '--copy_anat_pattern *ns+orig* ' \
#              '--output_dir rois/func_roi_vwfa_500 ' \
#              '--roi_size 500 ' \
#              '--output_roi_prefix vwfa_550 ' \
#              '--warped_ss_exists ' \
#              'tb5688 tb5689'

def gen_snapshots():
    pass


def _get_warped_mask(dir, prefix):
    return file_utils.match_single_file(dir, "{}*".format(prefix), except_on_fail=True, select_headfile=True)


def warp_search_space(func, search_space, clip, mask_out, anat_tlrc=None):
    """
    Downsamples search_space to the resolution of func and (if anat_tlrc is provided) warps search_space from +tlrc to
    +orig.

    :param func: functional volume with sub-brick specification, eg., subj_func.HEAD[1] or subj_func.HEAD[print]
    :param search_space: search space to define the ROI within; should be a one-subbrick volume containing a mask
    :param anat_tlrc: The +tlrc skull stripped anatomical for the subject in func. This will be passed directly
        to the -warp option of 3dfractionize and used to warp search_space from +tlrc to +orig. This parameter should
        only be filled if search_space is +tlrc and func is +orig.
    :param clip: clipping value to pass directly to the -clip argument of 3dfractionize
    :param mask_out: output path for the mask
    """
    if not anat_tlrc:
        anat_tlrc = ''
    # 3dFractionalize to warp (if needed) and downsample our search space to the subject
    # see example 2 in the 3dFractionalize help for details and explanation
    # Might need to cd into output_path[0] and use output_path[1] as the arg (after splitting output_path)
    fract_call = "3dfractionize -template {func} -input {search_space} -warp {anat_tlrc} " \
                 "-preserve -clip {clip} -prefix {mask_out}".format(func=func, search_space=search_space,
                                                                    anat_tlrc=anat_tlrc,
                                                                    clip=clip, mask_out=mask_out)
    if not anat_tlrc:
        fract_call = fract_call.replace('-warp ', '')

    # todo: more intelligent matching for prefixes
    ss_warp_files = glob.glob("{}*".format(mask_out))
    if ss_warp_files:
        raise AfniError("Files with prefix {} already exist; Aborted 3dfractionize call.".format(mask_out))

    subprocess.call(fract_call, shell=True)

    # todo: more intelligent matching for prefixes
    ss_warp_files = glob.glob("{}*".format(mask_out))
    if ss_warp_files:
        return ss_warp_files
    else:
        raise AfniError("3dfractionize did not successfully generate the file {}".format(mask_out))


def gen_func_roi(func, search_space, threshold, roi_size, output_path, remove_search_space=False):
    # 3dROIMaker to generate our functionally defined ROI
    # Might need to cd into output_path[0] and use output_path[1] as the arg (after splitting output_path)
    roimaker_call = "3dROIMaker -inset {func} -thresh {threshold} -prefix {output_path} " \
                    "-mask {search_space} -only_conn_top {roi_size}".format(func=func, threshold=threshold,
                                                                            output_path=output_path,
                                                                            search_space=search_space,
                                                                            roi_size=roi_size)
    # todo: more intelligent matching for prefixes
    roi_files = glob.glob("{}*".format(output_path))
    if roi_files:
        raise AfniError("Files with prefix {} already exist; Aborted 3droimaker call. ")

    subprocess.call(roimaker_call, shell=True)
    if remove_search_space:
        if os.path.exists(search_space):
            os.remove(search_space)

    # todo: more intelligent matching for prefixes
    roi_files = glob.glob("{}*".format(output_path))
    if roi_files:
        return roi_files
    else:
        raise AfniError("3droimaker did not successfully generate files with prefix {}".format(output_path))


def __main__():
    scriptName = os.path.splitext(os.path.basename(__file__))[0]
    if len(sys.argv) == 1:
        _debug(*_debug_cmd.split(' '))
    parser = genArgParser()
    args = parser.parse_args()

    check_paths = [args.mri_data_dir]
    if args.search_space:
        check_paths.append(args.search_space)

    bad_paths = file_utils.check_paths(True, *check_paths)

    if bad_paths:
        print 'ERROR: The following paths do not exist'
        for p in bad_paths:
            print p
        return

    subj_dirs = file_utils.get_dirs_from_patterns(args.mri_data_dir, True, *args.patterns)
    for subj_dir in sorted(subj_dirs):
        try:
            subj_scan = mri_data.Scan(scan_id=os.path.split(subj_dir)[1], root_dir=subj_dir, proc_runs=(args.proc_run,))
        except:
            print "Failed to instantiate a scan object for {}; skipping {}".format(subj_dir, subj_dir)
            continue

        proc_run = subj_scan.proc_runs[args.proc_run]

        # some filepath and data set specification
        temp_mask_name = 'int_mask.nii.gz'
        mask_name = args.warped_ss_prefix
        discard_mask = False
        if not mask_name:
            mask_name = temp_mask_name
            discard_mask = True

        # set the correct functional and anat
        if args.func_pattern:
            proc_run.set_active_stats_file(args.func_pattern)
        act_map = "{}'[{}]'".format(proc_run.active_stats_file, args.contrast_subbrick)
        anat = ''
        if args.anat_tlrc_pattern:
            proc_run.set_active_anat_file(args.anat_tlrc_pattern)
            anat = proc_run.active_anat_file

        # check that we have the necessary files
        if not proc_run.active_stats_file or (not proc_run.active_anat_file and args.anat_tlrc_pattern):
            print "{} is missing a required file; check the stats and anat in {}".format(subj_scan, proc_run)
            continue

        # set the output dir
        subj_out_dir = subj_scan.root_dir
        if args.output_dir:
            subj_out_dir = os.path.join(subj_scan.root_dir, args.output_dir)
        if not os.path.exists(subj_out_dir):
            os.makedirs(subj_out_dir)

        warped_ss_prefix = os.path.join(subj_out_dir, mask_name)

        bad_paths = file_utils.check_paths(True, proc_run.active_stats_file, subj_out_dir)

        if bad_paths:
            print 'ERROR: The following paths do not exist'
            for p in bad_paths:
                print p
            return

        ss_warp = None
        try:
            if args.warped_ss_exists:
                ss_warp = _get_warped_mask(subj_out_dir, mask_name)
            else:
                ss_warp_files = warp_search_space(func=proc_run.active_stats_file, search_space=args.search_space,
                                                  anat_tlrc=anat, clip=args.clip, mask_out=warped_ss_prefix)

                # todo: pathni module with this functionality
                ss_warp = fnmatch.filter(ss_warp_files, "*.HEAD")[0]
        except:
            print "Warp/downsample failed for {}".format(subj_scan)
            print "This could be due to a warped/downsampled mask already existing at the specified output path. " \
                  "Specify a new path or use the --warped_ss_exists option to use the existing mask.\nError Message:"
            print traceback.format_exc()
            continue
        try:
            output_path = os.path.join(subj_out_dir, args.output_roi_prefix)

            func_roi_files = gen_func_roi(func=act_map, search_space=ss_warp, threshold=args.threshold,
                                          roi_size=args.roi_size, output_path=output_path,
                                          remove_search_space=discard_mask)
            print "Generated functional ROI files for {}:\n{}\n".format(subj_scan, "\n".join(func_roi_files))

            if args.copy_anat_pattern:
                try:
                    file_utils.copy_files2(proc_run.root_dir, subj_out_dir, False, args.copy_anat_pattern)

                except:
                    print "Error copying anat files matching pattern {}:".format(args.copy_anat_pattern)
                    print traceback.format_exc()
        except:
            print "ROI generation failed for {}".format(subj_scan)
            print traceback.format_exc()


if __name__ == '__main__':
    __main__()