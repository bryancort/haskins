# -------------------------------------------------------------------------------
# Name:        core.subject
# Purpose:      representation of generalized or project-specific subjects
#
# Author:      Bryan Cort
#
# Created:     10/17/2014
# -------------------------------------------------------------------------------

import utils.file_utils
import os
import subprocess
import glob
import fnmatch


class Subject(object):
    def __init__(self, subj_id, project=None, **scans):
        super(Subject, self).__init__()
        self.subj_id = subj_id
        self.project = project
        self.scans = {}
        for scan_name, scan in scans:
            self.add_scan(scan_name=scan_name, scan=scan)

    def add_scan(self, scan_name, scan):
        self.scans[scan_name] = scan


class A187Subject(Subject):
    def __init__(self, subj_id, site, lang_type, **scans):
        if not scans:
            scans = {'time1': None, 'time3': None}
        super(A187Subject, self).__init__(subj_id, project='A187', scans=scans)
        self.site = site
        self.lang_type = lang_type


class A182Subject(Subject):
    def __init__(self, subj_id, **scans):
        if not scans:
            scans = {'SRTT': None, 'SAL_VAL': None}
        super(A182Subject, self).__init__(subj_id, project='A182', scans=scans)
        raise NotImplementedError('A182Subject not implemented. Refactor in progress.')
