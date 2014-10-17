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


class AfniDataDir(object):
    def __init__(self, code_exec_dir):
        super(AfniDataDir, self).__init__()
        self.code_exec_dir = code_exec_dir

    def execute_cmd(self, cmd):
        curr_dir = os.getcwd()
        os.chdir(self.code_exec_dir)
        subprocess.call(cmd, shell=True)
        os.chdir(curr_dir)


class ProcRun(AfniDataDir):
    def __init__(self, scan, proc_tag):
        self.scan = scan
        self.proc_tag = proc_tag
        self._find_run_files(self.scan, self.proc_tag)
        super(ProcRun, self).__init__(code_exec_dir=self.run_dir)

    def _find_run_files(self, scan, proc_tag):
        self.run_dir = utils.file_utils.match_single_dir(scan.data_dir, proc_tag, True)
        leaf_name = os.path.split(self.run_dir)
        script_name = 'afni_{}.tcsh'.format(leaf_name).replace('.results', '')
        script_output_name = 'output.{}'.format(script_name)
        self.run_script = utils.file_utils.match_single_file(scan.data_dir, script_name)
        self.run_script_output = utils.file_utils.match_single_file(scan.data_dir, script_output_name)


class ScanData(AfniDataDir):
    def __init__(self, scan_id, data_dir):
        self.scan_id = scan_id
        self.data_dir = data_dir
        self.proc_runs = {}
        super(ScanData, self).__init__(code_exec_dir=self.data_dir)

    def add_proc_run(self, proc_tag, run_name=None):
        if not run_name:
            run_name = proc_tag
        self.proc_runs[run_name] = ProcRun(self.scan_id, proc_tag)


class Subject(object):
    def __init__(self, subj_id, project=None, **scans):
        super(Subject, self).__init__()
        self.subj_id = subj_id
        self.project = project
        if scans:
            self.scans = scans
        else:
            self.scans = {'main': None}


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

