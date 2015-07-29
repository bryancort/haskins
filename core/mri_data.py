# -------------------------------------------------------------------------------
# Name:        core.mri_data
# Purpose:      representation of haskins mri data
#
# Author:      Bryan Cort
#
# Created:     10/20/2014
# -------------------------------------------------------------------------------
from collections import OrderedDict
import itertools
import traceback
import subprocess
import os
import glob
from mixins import ComparableMixin, KeyedMixin
from utils.mri_utils import BetweenVarMismatchError
from utils import mri_utils, file_utils, pathni, haskins_exceptions


#todo
class AfniData(object):
    def __init__(self, fpath):
        self.ftype = pathni.get_type(fpath)
        if not self.ftype:
            raise haskins_exceptions.FileError("{} is not a recognized afni file.".format(fpath))
        if self.ftype == ".BRIK":
            fpath = pathni.head_from_brik(fpath)
            self.ftype = ".HEAD"
        self.fpath = os.path.abspath(fpath)
        self.space = pathni.get_space(self.fpath)

    # fixme: unfinished
    def copy(self, dest_path):
        copy_call = "3dcopy {} {}".format()

    def move(self):
        move_call = ""

    def rename(self):
        rename_call = ""

    def delete(self):
        delete_call = ""


class AfniDataDir(object):
    def __init__(self, root_dir):
        super(AfniDataDir, self).__init__()
        self.root_dir = root_dir

    def execute_cmd(self, cmd):
        curr_dir = os.getcwd()
        os.chdir(self.root_dir)
        subprocess.call(cmd, shell=True)
        os.chdir(curr_dir)

    # todo: better behavior for this than silently defaulting to None on a failed match_single_file()
    def get_files(self, pattern, require_singlet=False):
        if require_singlet:
            return file_utils.match_single_file(path=self.root_dir, pattern=pattern)
        else:
            return glob.glob(os.path.join(self.root_dir, pattern))


class ProcRun(AfniDataDir):
    def __init__(self, scan, proc_tag, active_stats_file_pattern='stats.*REML+*.HEAD*',
                 active_anat_pattern="*ns+tlrc.HEAD"):
        """
        :param scan: scan name.
        :param proc_tag: substring uniquely identifying the proc run directory.
        :param active_stats_file_tag: substring uniquely identifying the stats file (.nii) or files (.HEAD/.BRIK pair).
            defaults to the REML stats file.
        :param active_anat_pattern: pattern to match to a single anat file. defaults to the skull stripped standard
            space anat.
        """
        self.scan = scan
        self.proc_tag = proc_tag
        self.root_dir = None
        self.run_script = None
        self.run_script_output = None
        self.active_stats_file = None  # .HEAD or .nii file
        self.active_anat_file = None
        self._find_run_files(self.scan, self.proc_tag)      # fixme: self.root_dir is set here, so:
        self.set_active_anat_file(active_anat_pattern)
        self.set_active_stats_file(active_stats_file_pattern)
        super(ProcRun, self).__init__(root_dir=self.root_dir)   # fixme: don't need the super init here?

    def _find_run_files(self, scan, proc_tag):
        self.root_dir = file_utils.match_single_dir(path=scan.root_dir, pattern='*{}*'.format(proc_tag),
                                                    except_on_fail=True)
        leaf_name = os.path.split(self.root_dir)[1]
        script_name = 'afni_{}.tcsh'.format(leaf_name).replace('.results', '')
        script_output_name = 'output.{}'.format(script_name)
        self.run_script = file_utils.match_single_file(path=scan.root_dir, pattern=script_name)
        self.run_script_output = file_utils.match_single_file(path=scan.root_dir, pattern=script_output_name)
        # todo: implement actual logging here
        if not self.run_script:
            print 'WARNING: could not find a unique run script for {} run of {}'.format(self.proc_tag, self.scan)
        if not self.run_script_output:
            print 'WARNING: could not find a unique run script output for {} run of {}'.format(self.proc_tag, self.scan)

    def set_active_stats_file(self, stats_file_pattern):
        try:
            self.active_stats_file = file_utils.match_single_file(path=self.root_dir, pattern=stats_file_pattern,
                                                      except_on_fail=True)
        except:
            print "Could not set stats file for {} using pattern {}:".format(self, stats_file_pattern)
            print traceback.format_exc()
            print "Active stats file reverted to {}".format(self.active_stats_file)

    def set_active_anat_file(self, anat_pattern):
        try:
            self.active_anat_file = file_utils.match_single_file(self.root_dir, anat_pattern, except_on_fail=True)
        except:
            print "Could not set anat file for {} using pattern {}:".format(self, anat_pattern)
            print traceback.format_exc()
            print "Active anat file reverted to {}".format(self.active_anat_file)

    def __str__(self):
        return 'Proc Run {} of {} located at {}'.format(self.proc_tag, self.scan, self.root_dir)

    def __repr__(self):  # fixme: need a real __repr__ here
        return 'Proc Run {} of {} located at {}'.format(self.proc_tag, self.scan, self.root_dir)


class Scan(KeyedMixin, ComparableMixin, AfniDataDir):
    def __init__(self, scan_id, root_dir, proc_runs=()):
        AfniDataDir.__init__(self, root_dir=os.path.normpath(root_dir))
        self.scan_id = scan_id
        # self.root_dir = os.path.normpath(root_dir)
        self.proc_runs = {}
        for run in proc_runs:
            if run:
                self.add_proc_run(run)

    def add_proc_run(self, proc_tag, run_name=None):
        if not run_name:
            run_name = proc_tag
        self.proc_runs[run_name] = ProcRun(self, proc_tag)

    def __key__(self):
        return self.scan_id


class ProcRun2(AfniDataDir):
    def __init__(self, scan, proc_pat, active_stats_file_pattern='stats.*REML+*.HEAD*',
                 active_anat_pattern="*ns+tlrc.HEAD"):
        """
        :param scan: scan name.
        :param proc_pat: pattern uniquely identifying the proc run directory.
        :param active_stats_file_tag: substring uniquely identifying the stats file (.nii) or files (.HEAD/.BRIK pair).
            defaults to the REML stats file.
        :param active_anat_pattern: pattern to match to a single anat file. defaults to the skull stripped standard
            space anat.
        """
        self.scan = scan
        self.proc_pat = proc_pat
        self.root_dir = None
        self.run_script = None
        self.run_script_output = None
        self.active_stats_file = None  # .HEAD or .nii file
        self.active_anat_file = None
        self._find_run_files(self.scan, self.proc_pat)      # fixme: self.root_dir is set here, so:
        self.set_active_anat_file(active_anat_pattern)
        self.set_active_stats_file(active_stats_file_pattern)
        super(ProcRun2, self).__init__(root_dir=self.root_dir)   # fixme: don't need the super init here?

    def _find_run_files(self, scan, proc_pat):
        self.root_dir = file_utils.match_single_dir(path=scan.root_dir, pattern=proc_pat, except_on_fail=True)
        leaf_name = os.path.split(self.root_dir)[1]
        script_name = 'afni_{}.tcsh'.format(leaf_name).replace('.results', '')
        script_output_name = 'output.{}'.format(script_name)
        self.run_script = file_utils.match_single_file(path=scan.root_dir, pattern=script_name)
        self.run_script_output = file_utils.match_single_file(path=scan.root_dir, pattern=script_output_name)
        # todo: implement actual logging here
        if not self.run_script:
            print 'WARNING: could not find a unique run script for {} run of {}'.format(self.proc_pat, self.scan)
        if not self.run_script_output:
            print 'WARNING: could not find a unique run script output for {} run of {}'.format(self.proc_pat, self.scan)

    def set_active_stats_file(self, stats_file_pattern):
        try:
            self.active_stats_file = file_utils.match_single_file(path=self.root_dir, pattern=stats_file_pattern,
                                                      except_on_fail=True)
        except:
            print "Could not set stats file for {} using pattern {}:".format(self, stats_file_pattern)
            print traceback.format_exc()
            print "Active stats file reverted to {}".format(self.active_stats_file)

    def set_active_anat_file(self, anat_pattern):
        try:
            self.active_anat_file = file_utils.match_single_file(self.root_dir, anat_pattern, except_on_fail=True)
        except:
            print "Could not set anat file for {} using pattern {}:".format(self, anat_pattern)
            print traceback.format_exc()
            print "Active anat file reverted to {}".format(self.active_anat_file)

    def __str__(self):
        return 'Proc Run {} of {} located at {}'.format(self.proc_pat, self.scan, self.root_dir)

    def __repr__(self):  # fixme: need a real __repr__ here
        return 'Proc Run {} of {} located at {}'.format(self.proc_pat, self.scan, self.root_dir)

# todo: in progress
class Scan2(KeyedMixin, ComparableMixin, AfniDataDir):
    def __init__(self, scan_id, root_dir, proc_run_patterns=()):
        AfniDataDir.__init__(self, root_dir=os.path.normpath(root_dir))
        self.scan_id = scan_id
        # self.root_dir = os.path.normpath(root_dir)
        self.proc_runs = {}
        for run in proc_run_patterns:
            if run:
                self.add_proc_run(run)

    def add_proc_run(self, proc_pat, run_name=None):
        if not run_name:
            run_name = proc_pat
        self.proc_runs[run_name] = ProcRun2(self, proc_pat)

    def __key__(self):
        return self.scan_id


def gen_mvm_table(scans_dict, within, between, subbrick_mapping, covars=None, vox_covar=None,
                  vox_covar_file_pattern=None, use_proc_run='results'):
    """
    Generates table to pass to the -dataTable option of 3dMVM

    :param scans_dict: dict of {scan: ({between_var_level: between_var_value}} (dict of dicts)
    :param within: dict of {var_name:(var_levels,)} for within subject vars
    :param between: dict of {var_name:(var_levels,)} for between subject vars
    :param subbrick_mapping: dict of witin_var_combination:subbrick_name} for each combo of within subj vars
    :param covars: covariates to include in the MVM. NOT IMPLEMENTED
    :param vox_covar: voxel-wise covariate, corresponds to -vVars opt in 3dMVM.
        Mirrors the current 3dMVM implementation of allowing only one voxelwise covariate.
    :param vox_covar_file_pattern: unix-style wildcard expression uniquely identifying the vox_covar file in each run.
    :param use_proc_run: processing run to use for this subject/scan
    :return: mvm datatable
    """

    # check between var specification
    if between:
        for bv in between.keys():
            for scan, var_pair in scans_dict.items():
                if bv not in var_pair.keys():
                    raise BetweenVarMismatchError('Mismatch: {} not specified for {}'.format(bv, scan.scan_id))

    mvmheader = ['Subj']
    scans_dict_sorted = OrderedDict(sorted(scans_dict.items()))
    if between:
        between_vars = OrderedDict(sorted(between.items()))
        mvmheader.extend(between_vars.keys())
    else:
        between_vars = {}
    if covars:
        quant_covars = covars
        mvmheader.extend(quant_covars)
    else:
        quant_covars = []
    if within:
        within_vars = OrderedDict(sorted(within.items()))
        mvmheader.extend(within_vars.keys())
    else:
        within_vars = {}
    if vox_covar:
        mvmheader.append(vox_covar)
    mvmheader.append('InputFile')

    mvmtable = [mvmheader]

    subbrick_names = None

    if type(subbrick_mapping) == int:
        raise NotImplementedError("Zero within subjs vars not yet implemented")
    else:
        subbrick_mapping = OrderedDict(sorted(subbrick_mapping.items()))
        subbricks = {frozenset(k): i for k, i in subbrick_mapping.items()}
        vals_to_perm = within_vars.values()
        for perm in itertools.product(*vals_to_perm):
            subbrick_val = subbricks[frozenset(perm)]
            for s, vars in scans_dict_sorted.items():
                between_vals = [vars[k] for k in between_vars.keys()]
                quant_covars_vals = [vars[k] for k in quant_covars]
                run = s.proc_runs[use_proc_run]
                if not subbrick_names:
                    subbrick_names = mri_utils.get_subBrick_Map(run.active_stats_file)
                subj_filepaths = []
                if vox_covar:
                    vox_covar_file = run.get_files(pattern=vox_covar_file_pattern, require_singlet=True)
                    vox_covar_file = '"{}"'.format(os.path.abspath(vox_covar_file))
                    subj_filepaths.append(vox_covar_file)
                stats_file = '"{}[{}]"'.format(os.path.abspath(run.active_stats_file), subbrick_names[subbrick_val])
                subj_filepaths.append(stats_file)
                mvmtable.append([s.scan_id] + between_vals + quant_covars_vals + list(perm) + subj_filepaths)

    return mvmtable