# -------------------------------------------------------------------------------
# Name:        mri_automation.processing
# Purpose:      mri data processing tasks (file unpacking, organization, preprocessing
#
# Author:      Bryan Cort
#
# Created:     08/10/2014
# -------------------------------------------------------------------------------

import os
import shutil
import subprocess
from subprocess import PIPE as PIPE
import tarfile
import traceback
from utils import mri_utils, file_utils, base_utils


def get_overwrite_paths(scan_dir, script_call):     #todo: test
    """
    Gets the file/directory paths to remove or archive for any run with --overwrite or --archive options.
    Works with Haskins naming/scripting conventions, untested on other combinations of options and defaults.

    :param scan_dir: subject ID
    :param script_call: final afni_proc.py script to check conflicting paths for
    :return: (directory, script, script output) tuple of paths
    """
    opts = script_call.split(' ')
    if '-out_dir' in opts:
        overwrite_dir = opts[opts.index('-out_dir') + 1]
    else:
        overwrite_dir = os.path.basename(scan_dir) + '.results'
    if '-script' in opts:
        overwrite_script = opts[opts.index('-script') + 1]
    else:
        overwrite_script = 'proc_subj.tcsh'
    overwrite_script_output = 'output.' + overwrite_script
    return map(os.path.join, ((scan_dir, overwrite_dir), (scan_dir, overwrite_script),
                              (scan_dir, overwrite_script_output)))


def org_scan_files(source, dest, are_dcms=True, cleanup=None, stim_times=None, **dir_structure): # todo: test
    """
    Organizes mri scan files from one directory into (optionally) another based on the dir_structure specified

    :param source: source directory with files to organize
    :param dest: destination directory to organize into
    :param are_dcms: if true, will dcm2nii the source directory and output to dest
    :param cleanup: optional cleanup dir name for files that do not match any pattern in dir_structures. Will be created
        in dest
    :param stim_times: optional stim times directory to copy into dest
    :param dir_structure: dict of {subdir: (filename patterns,)} pairs; for every key subdir, and subdirectory is
        created in dest and all files matching any pattern in filename patterns are moved into that subdirectory
    """
    if are_dcms:
        mri_utils.dcm2nii_all(source=source, o=dest, d='n')
    else:
        file_utils.copy_files(source, dest, '*')
    for sdir, patterns in dir_structure.iteritems():
            file_utils.move_files(dest, os.path.join(dest, sdir), *patterns)
    if cleanup:
        cleanup_path = os.path.join(dest, cleanup)
        if not os.path.exists(cleanup_path):
            os.makedirs(cleanup_path)
        for f in file_utils.get_immediate_files(dest):
            shutil.move(f, cleanup_path)
    if os.path.exists(stim_times):
        shutil.copytree(stim_times, os.path.join(dest, os.path.basename(stim_times.rstrip(os.path.sep))))


def preprocess_scan(scan_dir, afni_proc_call, archive=False, overwrite=False):  #todo: test
    """
    :param scan_dir: Full path to directory containing subject data.
    :param archive: Archives any previous processing (tar.gz format) if this evaluates to True.
    :param overwrite: Overwrites any previous processing (tar.gz format) if this evaluates to True. This is implied in
    archive=True.
    :return: Message string. Message is our best guess at what happened during processing.
    """
    subjID = os.path.basename(scan_dir)
    try:
        if not file_utils.match_single_file(os.path.join(scan_dir, 'anat'), '*.nii*'):
            return '{}: Multiple anat files in {}.'.format(subjID, os.path.join(scan_dir, 'anat'))
        with open(afni_proc_call) as scriptFile:
            afniCall = scriptFile.read()
        afniCall = afniCall.format(subjID)

        overwrite_leafs = get_overwrite_paths(subjID, afniCall)
        overwrite_paths = [os.path.join(scan_dir, leaf) for leaf in overwrite_leafs]
        overwrite_paths = filter(os.path.exists, overwrite_paths)

        if archive and overwrite_paths:  # tar.gz the previous results and afni scripts so we can replace with new ones
            with tarfile.open(os.path.join(scan_dir, '{}_{}.tar.gz'.format(subjID, base_utils.getLocalTime())),
                              'w:gz') as tar:
                for p in overwrite_paths:
                    tar.add(p, arcname=p.rsplit(os.path.sep, 1)[-1])
        if archive or overwrite:  # remove the results of our previous analysis
            for p in overwrite_paths:
                if os.path.isdir(p):
                    shutil.rmtree(p)
                else:
                    os.remove(p)

        basedir = os.path.abspath('.')
        os.chdir(scan_dir)
        out, err = subprocess.Popen(afniCall, stdout=None, stderr=PIPE, shell=True).communicate()
        os.chdir(basedir)
        if err:  # fixme: afni_proc.py doesn't write to stderr, all output goes to stdout
            return '{}: process_subject() generated the following error:\n{}'.format(subjID, err)
        return '{}: process_subject() ran successfully.'.format(subjID)
    except:
        return '{}: process_subject failed with stack trace\n{}'.format(subjID, traceback.format_exc())