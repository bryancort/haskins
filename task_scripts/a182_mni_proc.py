
import os
import sys
import glob
import fnmatch
import argparse
import subprocess
import shutil
from subprocess import PIPE as PIPE
import traceback
from utils import base_utils, file_utils, mri_utils, pathni
from core import mri_data
from utils.haskins_exceptions import *


def genArgParser():
    """
    Generate a command line argument parser for this script.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('patterns', nargs='+',
                        help='One or more unix-style wildcard expressions to generate the list of subject data '
                             'subdirectories.')

    mri_data_dir_default = "/data1/A182/mri_subjects"
    parser.add_argument('--mri_data_dir', default=mri_data_dir_default, required=True,
                        help='Directory containing scans. Default: {}'.format(mri_data_dir_default))

    symlink_data_dir_default = "/data1/A182"
    parser.add_argument('--symlink_data_dir', default=symlink_data_dir_default, required=True,
                        help='Directory containing scans. Default: {}'.format(symlink_data_dir_default))

    suma_dir_default = "/data1/A182"
    parser.add_argument('--suma_dir', default=suma_dir_default, required=True,
                        help='Directory containing scans. Default: {}'.format(suma_dir_default))

    id_table_default = "/data1/A182/A182BehavioralData/idTable.txt"
    parser.add_argument('--id_table', default=id_table_default, required=True,
                        help='Directory containing scans. Default: {}'.format(id_table_default))

    return parser


def map_ids(ftable):
    """
    Looks up MRI IDs and maps them to subject IDs. All ids are stored as strings.
    :param ftable: table of haskins id, [mri ids].
    :return: dictionary of {all ids: haskins id}. haskins ids are mapped to themselves.
    """
    table = file_utils.readTable2(ftable)
    assert ftable
    idMap = {}
    for row in table:
        for entry in row:
            if entry in idMap.keys():
                print "Entry {} appears multiple times in idtable".format(entry)
                continue
            # This maps subjIDs to themselves; this is important for renaming functions to work on both MRI IDs and subject IDs
            idMap[str(entry)] = str(row[0])
    return idMap

def get_anat_dir(scan_dir, except_on_fail=True):
    anat_dir = os.path.join(scan_dir, "anat")
    if os.path.exists(anat_dir):
        return anat_dir
    if except_on_fail:
        raise FileError("No anat dir in {}".format(scan_dir))
    return None

def get_suma_brain(freesurfer_dir, haskins_id, except_on_fail=True):
    brain_path = os.path.join(freesurfer_dir, haskins_id, "SUMA", "brain.nii")
    if os.path.exists(brain_path):
        return brain_path
    brain_path += ".gz"
    if os.path.exists(brain_path):
        return brain_path
    if except_on_fail:
        raise FileError("No SUMA brain.nii or brain.nii.gz file")
    return None


def _debug(*cmd_args):
    sys.argv = [sys.argv[0]] + list(cmd_args)

_debug_cmd = None


def __main__():
    scriptName = os.path.splitext(os.path.basename(__file__))[0]
    if len(sys.argv) == 1:
        _debug(*_debug_cmd.split(' '))
    parser = genArgParser()
    args = parser.parse_args()

    # todo: read the idtable
    id_map = map_ids(args.id_table)

    # todo: copy brain.nii's that don't exist
    for scan_id in id_map:
        h_id = "h" + id_map[scan_id]
        scan_dir = os.path.join(args.mri_data_dir, scan_id)     # todo: make sure notes don't break this
        brain_nii_path = get_suma_brain(args.suma_dir, h_id)    # todo: or this
        anat_dir = get_anat_dir(scan_dir)

        #todo: CHANGE BELOW CODE, ANAT DIR AND BRAIN PATH WILL NOW RAISE ERRORS IF NOT THERE

        new_brain_nii_path = os.path.join(scan_dir, )
        # todo: could simplify this and just let the copy raise an error
        if os.path.exists(scan_dir) and os.path.exists(brain_nii_path) and anat_dir \
                and not os.path.exists(new_brain_nii_path):
            pass

    # todo: run afni_proc.py for all the scans with a +tlrc anat

    # todo: logging



if __name__ == '__main__':
    __main__()

