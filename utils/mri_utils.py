# -------------------------------------------------------------------------------
# Name:        mri_utils
# Purpose:      Classes and functions for handling MRI data
#
# Author:      Bryan Cort
#
# Created:     12/02/2014
# -------------------------------------------------------------------------------

import os
import subprocess
from subprocess import PIPE as PIPE
from utils import pathni, haskins_exceptions


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
    -g gzip list_attrs, filename.nii.gz [ignored if '-n n']: Y,N = Y
    -i ID  in filename [filename.dcm -> johndoe.nii]: Y,N = N
    -m manually prompt user to specify list_attrs format [NIfTI input only]: Y,N = Y
    -n list_attrs .nii file [if no, create .hdr/.img pair]: Y,N = Y
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
    subprocess.call(spc)


def get_subBrick_Map(niftiFilePath):
    """
    Parses 3dinfo for a number:name mapping for subbricks in a nifti file

    :param niftiFilePath: path to nifti file to get subbrick mapping for
    :returns subbrick number: subbrick name mapping for the given nifti file
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


#fixme: possibly buggy
def copy_mri_files(headfile, new_headfile):
    while 1:
        subprocess.call("3dcopy {} {}".format(headfile, new_headfile), shell=True)
        if os.path.exists(new_headfile) and os.path.exists(pathni.brik_from_head(new_headfile)):
            break
        if os.path.exists(pathni.brik_from_head(new_headfile)):
            os.remove(pathni.brik_from_head(new_headfile))
        if os.path.exists(new_headfile):
            os.remove(new_headfile)

def apply_mask(mask, dataset, prefix, out_id_string="Output dataset "):
    """
    Calls 3dcalc to mask dataset using mask, saving the output using prefix.

    :param mask: mask dset
    :param dataset: dset to mask, including subbrick selector if required, eg. path/to/dset'[some_subbrick]'
    :param prefix: prefix to give to 3dcalc for saving the output
    :returns output_dset: path to the output file
    """
    mask_call = "3dcalc -a {} -b {} -prefix {} -expr '1*step(a) * 1*b'".format(mask, dataset, prefix)
    print mask_call
    # todo: talk to afni devs about why 3dcalc sends its output to stderr?
    output = subprocess.Popen(mask_call, shell=True, stderr=PIPE).communicate()[1]
    output_dset = output.split(out_id_string, 1)[-1]
    output_dset = output_dset.split()[0]
    if output_dset[-5:] == ".BRIK":
        output_dset = pathni.head_from_brik(output_dset)
    return output_dset


#fixme: figure out how to use underlay/overlay not in the same directory
def gen_snapshots(underlay, overlay, out_prefix, mont_dims=(6, 5, 3), center_on="underlay"):
    if center_on == "overlay":
        center_on = overlay
    elif center_on == "underlay":
        center_on = underlay
    else:
        raise Exception("center_on argument to gen_snapshots() must be either 'overlay' or 'underlay'")
    work_dir = os.path.dirname(overlay)
    out_prefix = os.path.abspath(out_prefix)
    # underlay = os.path.abspath(underlay)
    # overlay = os.path.abspath(overlay)
    underlay = os.path.basename(underlay)
    overlay = os.path.basename(overlay)
    curr_dir = os.getcwd()
    # ulay_tempfile = "_" + str(time.time()) + pathni.get_tail(underlay)
    # olay_tempfile = "__" + str(time.time()) + pathni.get_tail(overlay)
    if work_dir:
        os.chdir(work_dir)
    try:
        # copy_mri_files(underlay, ulay_tempfile)
        # copy_mri_files(overlay, olay_tempfile)

        if not (os.path.exists(underlay) and os.path.exists(overlay)):
            raise Exception("Underlay and overlay must be in the same directory")

        center_cmd = "3dCM {}".format(center_on)
        center = subprocess.Popen(center_cmd, universal_newlines=True,
                                       stdout=PIPE, shell=True).communicate()[0]

        # fixme: -no_detach not working
        snapshot_cmd = '''/opt/X11/bin/Xvfb :1 -screen 0 1024x768x24 & afni -no_detach \
-com "OPEN_WINDOW A.axialimage mont={mont_x}x{mont_y}:{mont_spacing} geom=600x600+800+600" \
-com "CLOSE_WINDOW A.sagittalimage" \
-com "SWITCH_UNDERLAY {underlay}" \
-com "SWITCH_OVERLAY {overlay}" \
-com "SET_DICOM_XYZ A {center}" \
-com "SAVE_JPEG A.axialimage {out_prefix}" \
-com "QUIT"'''.format(mont_x=mont_dims[0], mont_y=mont_dims[1], mont_spacing=mont_dims[2],
                      underlay=underlay, overlay=overlay, center=center,
                      out_prefix=out_prefix)

        subprocess.call(snapshot_cmd, shell=True)
    except:
        raise
    finally:
        # if os.path.exists(underlay):
        #     pathni.remove_pair(underlay)
        # if os.path.exists(overlay):
        #     pathni.remove_pair(overlay)
        os.chdir(curr_dir)


# todo: this
def gen_snapshots2(underlay, overlay, out_prefix, mont_dims=(6, 5, 3), center_on="underlay"):
    pass


def tlrc_to_orig(some, placeholder, args, here):
    pass


def orig_to_tlrc(orig_dset, tlrc_template, prefix, vox_size=3, resample_mode="NN", first_time_warp=False,
                 dset_type="3D"):
    if first_time_warp:
        raise NotImplementedError("First time warping not yet implemented.")

    dset_type = str(dset_type).lower()
    if dset_type != "3d" and dset_type != "1d":
        raise haskins_exceptions.AfniError("dset_type must be 1D or 3D. {} not supported.".format(dset_type))

    if dset_type == "3d":
        warp_call = "adwarp -apar {tlrc_template} -dpar {orig_dset} -dxyz {vox_size} -prefix {prefix} " \
                    "-resam {resample_mode}".format(tlrc_template=tlrc_template, orig_dset=orig_dset,
                                                    vox_size=vox_size, prefix=prefix, resample_mode=resample_mode)
        subprocess.call(warp_call, shell=True, stdout=PIPE)
        expected_file = prefix + "+tlrc.HEAD"
        if os.path.exists(expected_file) and os.path.exists(pathni.brik_from_head(expected_file)):
            return expected_file
        return None

    if dset_type == "1d":
        warp_call = "Vecwarp -apar {tlrc_template} " \
                    "-input {orig_dset} -output {prefix}".format(tlrc_template=tlrc_template,
                                                                 orig_dset=orig_dset,
                                                                 prefix=prefix)
        out, err = subprocess.Popen(warp_call, shell=True, stdout=PIPE, stderr=PIPE).communicate()
        if "ERROR" in err:
            raise haskins_exceptions.AfniError("Vecwarp call {} failed:\n{}".format(warp_call, err))
        print out
        if os.path.exists(os.path.abspath(prefix)):
            return os.path.abspath(prefix)
        return None


def get_peak_voxel(dset, dec=None, out_path=None):
    # get the max value with 3dBrickStat
    brickstat_call = "3dBrickStat -max {}".format(dset)
    peak_activation_value = subprocess.Popen(brickstat_call, stdout=PIPE, shell=True).communicate()[0].strip()

    # get the coords of that value with 3dmaxima -coords_only
    all_coords = None
    adj_peak = peak_activation_value
    while True:
        maxima_call = "3dmaxima -input {} -coords_only -thresh {}".format(dset, adj_peak)
        all_coords = subprocess.Popen(maxima_call, stdout=PIPE, shell=True).communicate()[0].split()
        if all_coords:
            break
        adj_peak = adj_peak[:-1]
        if not adj_peak:
            raise haskins_exceptions.AfniError("3dmaxima could not locate the peak value '{}' reported by 3dBrickStat "
                                               "in {}. This could be due to incorrect header info; try '3drefit "
                                               "-redo_bstat dset' to correct.".format(peak_activation_value, dset))

    if len(all_coords)%3:
        raise haskins_exceptions.AfniError("3dmaxima returned coordinates list not divisible by 3.")

    all_coords = [float(n) for n in all_coords]

    coord_groups = [all_coords[0::3], all_coords[1::3], all_coords[2::3]]
    print "Taking the mean of {} voxels for best approximation of peak voxel location".format(len(coord_groups[0]))

    coords = [float(sum(group))/float(len(group)) for group in coord_groups]

    assert len(coords) == 3

    if adj_peak != peak_activation_value:
        print "Rounding error in 3dBrickStat; adjusted peak to {}".format(adj_peak)
    peak_x, peak_y, peak_z = coords[0], coords[1], coords[2]
    if dec:
        peak_x, peak_y, peak_z = round(peak_x, dec), round(peak_y, dec), round(peak_z, dec)
    if out_path:
        with open(out_path, "w") as outfile:
            outfile.write("{} {} {}".format(peak_x, peak_y, peak_z))
    return (peak_x, peak_y, peak_z), out_path