# -------------------------------------------------------------------------------
# Name:        mri_automation
# Purpose:      Module for automated large scale processing mri data
#
# Author:      Bryan Cort
#
# Created:     08/10/2014
# -------------------------------------------------------------------------------


niftiDirName = 'nifti'

a187_ny_pairs = {'func': ('*language*',),  # todo: bring these filestructures back in line with A182
                 'DTI': ('*dti*',),
                 'anat': ('Hi*',)}

a187_hu_pairs = {'func': ('TR2*', '*Haskins132TRs*'),
                 'DTI': ('ep2ddiffMDD*', '*hadassahDTIs*'),
                 'anat': ('t1mprage*',),
                 'anat/extra': ('local*', 't1fl*', 'ep2dTR3A*')}

a40_pid_pairs = {'func': ('*bold*',),
                 'anat': ('*Sag*', '*SAG*', '*AXIAL*', '*MPRAGE*')}