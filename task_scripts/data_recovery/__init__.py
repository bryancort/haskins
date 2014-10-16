# -------------------------------------------------------------------------------
# Name:        data_recovery
# Purpose:      code for .../dicoms/incoming recovery and verification
#
# Author:      Bryan Cort
#
# Created:     16/10/2014
# -------------------------------------------------------------------------------

import os

_dicoms_dir_path = os.path.normpath('U:\dicom\incoming')     # os.path.normpath('/zappa/dicom/incoming')
_dicoms_BU_dir_path = os.path.normpath('U:\dicom\incoming_BU')
_scans_list_filepath = os.path.normpath('./lost_scans.txt')