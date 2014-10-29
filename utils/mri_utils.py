# -------------------------------------------------------------------------------
# Name:        mri_utils
# Purpose:      Classes and functions for handling MRI data
#
# Author:      Bryan Cort
#
# Created:     12/02/2014
# -------------------------------------------------------------------------------

import subprocess
from subprocess import PIPE as PIPE

import utils.base_utils


class BetweenVarMismatchError(Exception):
    pass

def dcm2nii_all(source, **kwargs):
    """
    Python wrapper for dcm2nii
    Runs dcm2nii on source, outputing nii files to dest (if specified)
    :param source:  Source directory to run dcm2nii on
    :param kwargs:  Option=Value pairs to pass to dcm2nii

    Partial documentation reproduced below from Chris Rorden's dcm2nii :: 12 12 2012
    See http://www.mccauslandcenter.sc.edu/mricro/mricron/dcm2nii.html

    -4 Create 4D volumes, else DTI/fMRI saved as many 3D volumes: Y,N = Y
    -a Anonymize [remove identifying information]: Y,N = Y
    -b load settings from specified inifile, e.g. '-b C:\set\t1.ini'
    -c Collapse input folders: Y,N = Y
    -d Date in filename [filename.dcm -> 20061230122032.nii]: Y,N = Y
    -e events (series/acq) in filename [filename.dcm -> s002a003.nii]: Y,N = Y
    -f Source filename [e.g. filename.par -> filename.nii]: Y,N = N
    -g gzip output, filename.nii.gz [ignored if '-n n']: Y,N = Y
    -i ID  in filename [filename.dcm -> johndoe.nii]: Y,N = N
    -m manually prompt user to specify output format [NIfTI input only]: Y,N = Y
    -n output .nii file [if no, create .hdr/.img pair]: Y,N = Y
    -o Output Directory, e.g. 'C:\TEMP' (if unspecified, source directory is used)
    -p Protocol in filename [filename.dcm -> TFE_T1.nii]: Y,N = Y
    -r Reorient image to nearest orthogonal: Y,N
    -s SPM2/Analyze not SPM5/NIfTI [ignored if '-n y']: Y,N = N
    -v Convert every image in the directory: Y,N = Y
    -x Reorient and crop 3D NIfTI images: Y,N = N
    """
    spc = ['dcm2nii']
    for kw, arg in kwargs.iteritems():
        spc.append('-{}'.format(kw))
        spc.append(arg)
    spc.append(source)
    # print spc
    # return
    subprocess.call(spc)


def get_subBrick_Map(niftiFilePath):
    """
    Parses 3dinfo for a number:name mapping for subbricks in a nifti file

    :param niftiFilePath: path to nifti file to get subbrick mapping for
    :return: subbrick number: subbrick name mapping for the given nifti file
    """
    labels = subprocess.Popen(['3dinfo', '-label', niftiFilePath],
                              universal_newlines=True, stdout=PIPE).communicate()[0].strip('\n').split('|')
    subBricks = {str(n): lab for (n, lab) in enumerate(labels)}
    return subBricks


def rename_subbrick(filepath, old_sb_num, new_label):
    """
    Renames filepath[old_sb_num] to filepath[new_label]

    :param filepath: path to afni file (nifti or .HEAD
    :param old_sb_num: subbrick number to relabel
    :param new_label: new subbrick label
    """
    old_sb_num = str(old_sb_num)
    old_label = subprocess.Popen('3dinfo -label "{}[{}]"'.format(filepath, old_sb_num),
                              stdout=PIPE, shell=True).communicate()[0]
    if new_label != old_label:
        subprocess.call('3drefit -sublabel {} {} {}'.format(old_sb_num, new_label, filepath),
                              stdout=PIPE, shell=True)