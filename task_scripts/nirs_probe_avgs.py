#!/usr/bin/python
# -------------------------------------------------------------------------------
# Name:        task_scripts.nirs_probe_avgs.py
# Purpose:      Creates in-brain portion of spherical masks for specified coords, averages within each mask
#               Copies the coordinate list file for each subjects and adds two new columns for the speech
#               average and the print average (in that order)
#
# Author:      Bryan Cort
#
# Created:     1/13/2015
# -------------------------------------------------------------------------------

import os
import sys
import subprocess
from subprocess import PIPE as PIPE


def _left_value_dict(fname, header=False):
    with open(fname, 'rU') as infile:
        rows = infile.read().split('\n')
        if header:
            rows = rows[1:]
        l_dict = {}
        for row in rows:
            v,k = row.split('\t')
            l_dict[k] = v
        return l_dict


def _get_stats_file_path(mri_scan):
    return os.path.normpath('{scan}/{scan}.fastloc/stats.{scan}_REML+tlrc.HEAD'.format(scan=mri_scan))


def _get_coords_file_path(nirs_scan):
    return os.path.normpath('../../nirs/ROI_LIST/{}_roi_list'.format(nirs_scan))


def __main__():
    os.chdir('/data3/a40p1/Wave_One')

    if len(sys.argv) == 1:
        subj_list_fname = 'HBMSubsList.txt'
    else:
        subj_list_fname = sys.argv[1]

    # print subj_list_fname

    nirs_to_tb = _left_value_dict(subj_list_fname, header=True)

    # this is unused?
    # TT_N27_mask_fpath = 'TT_N27_MASK.nii'

    # print nirs_to_tb

    for nirs_scan, mri_scan in nirs_to_tb.items():
        outfile_name = '{}_{}_means.txt'.format(mri_scan, nirs_scan)
        outfile_path = os.path.join('../../nirs/NIRS_corr_data', outfile_name)
        if not os.path.exists(outfile_path):
            mri_stats_file_path = _get_stats_file_path(mri_scan)
            coords_list_file_path = _get_coords_file_path(nirs_scan)

            # print mri_stats_file_path, os.path.exists(mri_stats_file_path)
            # print coords_list_file_path, os.path.exists(coords_list_file_path)

            # for each coord, create the masked dset
            all_coords = None
            with open(coords_list_file_path, 'rU') as coords_file:
                all_coords = coords_file.read().split('\n')
            for i, coord_row in enumerate(all_coords):
                coord = coord_row.split('\t')
                x_coord, y_coord, z_coord, coord_n = coord[0], coord[1], coord[2], coord[3]
                mask_dset = '{}_coord_{}_mask.nii'.format(mri_scan, coord_n)
                call_3dcalc = "3dcalc -a TT_N27_MASK.nii " \
                              "-expr 'a*step(900-(x+{x})*(x+{x})-(y+{y})*(y+{y})-(z+{z})*(z+{z}))'" \
                              "-LPI -prefix {out}".format(out=mask_dset, x=x_coord, y=y_coord, z=z_coord)
                subprocess.call(call_3dcalc, shell=True)

                #average the masked dset[speech] and masked dset[print] within the mask
                print_call_3dbrickstat = "3dBrickStat -mean -mask {mask} {stats}[13]".format(mask=mask_dset,
                                                                                             stats=mri_stats_file_path)
                print_avg = subprocess.Popen(print_call_3dbrickstat, shell=True, stdout=PIPE).communicate()[0]
                print_avg = print_avg.strip('\n')

                speech_call_3dbrickstat = "3dBrickStat -mean -mask {mask} {stats}[16]".format(mask=mask_dset,
                                                                                             stats=mri_stats_file_path)
                speech_avg = subprocess.Popen(speech_call_3dbrickstat, shell=True, stdout=PIPE).communicate()[0]
                speech_avg = speech_avg.strip('\n')

                #record the averages
                all_coords[i] += '\t'
                all_coords[i] += '\t'.join([print_avg, speech_avg])
                if os.path.exists(mask_dset):
                    os.remove(mask_dset)

            # write the new coord file for this subj
            with open(outfile_path, 'w') as outfile:
                outfile.write('\n'.join(all_coords))


if __name__ == '__main__':
    __main__()