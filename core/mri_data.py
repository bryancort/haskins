# -------------------------------------------------------------------------------
# Name:        core.mri_data
# Purpose:      representation of haskins mri data
#
# Author:      Bryan Cort
#
# Created:     10/20/2014
# -------------------------------------------------------------------------------

import subprocess
import os
import utils.file_utils


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
    def __init__(self, scan, proc_tag, active_stats_file_tag='REML'):
        self.scan = scan
        self.proc_tag = proc_tag
        self.run_dir = None
        self.run_script = None
        self.run_script_output = None
        self.active_stats_files = None  # tuple of either (head,brik) or (nifti,)
        self._find_run_files(self.scan, self.proc_tag)
        self.set_active_stats_file(active_stats_file_tag)
        super(ProcRun, self).__init__(code_exec_dir=self.run_dir)

    def _find_run_files(self, scan, proc_tag):
        self.run_dir = utils.file_utils.match_single_dir(path=scan.data_dir, pattern='*{}*'.format(proc_tag),
                                                         except_on_fail=True)
        leaf_name = os.path.split(self.run_dir)[1]
        script_name = 'afni_{}.tcsh'.format(leaf_name).replace('.results', '')
        script_output_name = 'output.{}'.format(script_name)
        self.run_script = utils.file_utils.match_single_file(path=scan.data_dir, pattern=script_name)
        self.run_script_output = utils.file_utils.match_single_file(path=scan.data_dir, pattern=script_output_name)
        # todo: implement actual logging here
        if not self.run_script:
            print 'WARNING: could not find a unique run script for {} run of {}'.format(self.proc_tag, self.scan)
        if not self.run_script_output:
            print 'WARNING: could not find a unique run script output for {} run of {}'.format(self.proc_tag, self.scan)

    def set_active_stats_file(self, stats_file_tag):
        stats_head = utils.file_utils.match_single_file(self.run_dir, 'stats.*{}+*.HEAD'.format(stats_file_tag))
        stats_brik = utils.file_utils.match_single_file(self.run_dir, 'stats.*{}+*.BRIK'.format(stats_file_tag))
        stats_nii = utils.file_utils.match_single_file(self.run_dir, 'stats.*{}+*.nii'.format(stats_file_tag))
        if stats_head and stats_brik:
            self.active_stats_files = (stats_head, stats_brik)
        elif stats_nii:
            self.active_stats_files = (stats_nii, )
        else:
            raise utils.file_utils.FileError("Could not find unique head/brik pair or nii stats files for {} in {} "
                                             "with tag {}".format(self.scan, self.run_dir, stats_file_tag))

    def __str__(self):
        return 'Proc Run {} of {} located at {}'.format(self.proc_tag, self.scan, self.run_dir)

    def __repr__(self):  # fixme: need a real __repr__ here
        return 'Proc Run {} of {} located at {}'.format(self.proc_tag, self.scan, self.run_dir)


class Scan(AfniDataDir):
    def __init__(self, scan_id, data_dir):
        self.scan_id = scan_id
        self.data_dir = data_dir  # rightmost component should match scan_id
        self.proc_runs = {}
        super(Scan, self).__init__(code_exec_dir=self.data_dir)

    def add_proc_run(self, proc_tag, run_name=None):
        if not run_name:
            run_name = proc_tag
        self.proc_runs[run_name] = ProcRun(self, proc_tag)

    def __str__(self):
        return self.scan_id

    def __repr__(self):  # fixme: need a real __repr__ here
        return self.scan_id
