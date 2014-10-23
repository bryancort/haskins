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

import subprocess
import os
import glob
from mixins import Comparable, Keyed
from utils.mri_utils import BetweenVarMismatchError
from utils import mri_utils, file_utils


class AfniDataDir(object):
    def __init__(self, code_exec_dir):
        super(AfniDataDir, self).__init__()
        self.code_exec_dir = code_exec_dir

    def execute_cmd(self, cmd):
        curr_dir = os.getcwd()
        os.chdir(self.code_exec_dir)
        subprocess.call(cmd, shell=True)
        os.chdir(curr_dir)


class ProcRun(AfniDataDir): # todo: make Keyed
    def __init__(self, scan, proc_tag, active_stats_file_tag='REML'):
        self.scan = scan
        self.proc_tag = proc_tag
        self.run_dir = None
        self.run_script = None
        self.run_script_output = None
        self.active_stats_file = None  # .HEAD or .nii file
        self._find_run_files(self.scan, self.proc_tag)
        self.set_active_stats_file(active_stats_file_tag)
        super(ProcRun, self).__init__(code_exec_dir=self.run_dir)

    def _find_run_files(self, scan, proc_tag):
        self.run_dir = file_utils.match_single_dir(path=scan.data_dir, pattern='*{}*'.format(proc_tag),
                                                         except_on_fail=True)
        leaf_name = os.path.split(self.run_dir)[1]
        script_name = 'afni_{}.tcsh'.format(leaf_name).replace('.results', '')
        script_output_name = 'output.{}'.format(script_name)
        self.run_script = file_utils.match_single_file(path=scan.data_dir, pattern=script_name)
        self.run_script_output = file_utils.match_single_file(path=scan.data_dir, pattern=script_output_name)
        # todo: implement actual logging here
        if not self.run_script:
            print 'WARNING: could not find a unique run script for {} run of {}'.format(self.proc_tag, self.scan)
        if not self.run_script_output:
            print 'WARNING: could not find a unique run script output for {} run of {}'.format(self.proc_tag, self.scan)

    def set_active_stats_file(self, stats_file_tag):
        stats_head = file_utils.match_single_file(self.run_dir, 'stats.*{}+*.HEAD'.format(stats_file_tag))
        stats_brik = file_utils.match_single_file(self.run_dir, 'stats.*{}+*.BRIK'.format(stats_file_tag))
        stats_nii = file_utils.match_single_file(self.run_dir, 'stats.*{}+*.nii'.format(stats_file_tag))
        if stats_head and stats_brik:
            self.active_stats_file = stats_head
        elif stats_nii:
            self.active_stats_file = stats_nii
        else:
            raise file_utils.FileError("Could not find unique head/brik pair or nii stats files for {} in {} "
                                             "with tag {}".format(self.scan, self.run_dir, stats_file_tag))

    def get_files(self, pattern, require_singlet=False):
        if require_singlet:
            return file_utils.match_single_file(path=self.run_dir, pattern=pattern)
        else:
            return glob.glob(os.path.join(self.run_dir, pattern))

    def __str__(self):
        return 'Proc Run {} of {} located at {}'.format(self.proc_tag, self.scan, self.run_dir)

    def __repr__(self):  # fixme: need a real __repr__ here
        return 'Proc Run {} of {} located at {}'.format(self.proc_tag, self.scan, self.run_dir)


class Scan(AfniDataDir, Comparable, Keyed):
    def __init__(self, scan_id, data_dir):
        self.scan_id = scan_id
        self.data_dir = data_dir  # rightmost component should match scan_id
        self.proc_runs = {}
        super(Scan, self).__init__(code_exec_dir=self.data_dir)

    def add_proc_run(self, proc_tag, run_name=None):
        if not run_name:
            run_name = proc_tag
        self.proc_runs[run_name] = ProcRun(self, proc_tag)

    def __key__(self):
        return self.scan_id


def gen_mvm_table(scans_dict, within, between, subbrick_mapping=1, covars=None, vox_covar=None,
                  vox_covar_file_pattern=None, use_proc_run='results'):
    """
    Generates table to pass to the -dataTable option of 3dMVM

    :param scans_dict: dict of {scan: ({between_var_level: between_var_value}} (dict of dicts)
    :param within: dict of {var_name:(var_levels,)} for within subject vars
    :param between: dict of {var_name:(var_levels,)} for between subject vars
    :param subbrick_mapping: dict of witin_var_combination:subbrick_name} all combos of within subj vars or int value of
        subbrick to use if
    :param covars: covariates to include in the MVM. currently not implemented
    :param vox_covar: voxel-wise covar; corresponds to -vVars opt in 3dMVM. Mirrors the current 3dMVM implementation of
        allowing only one voxelwise covariate.
    :param vox_covar_file_pattern: unix-style wildcard expression uniquely identifying the vox_covar file in each run.
    :param use_proc_run: processing run to use for this subject/scan
    :return: mvm datatable
    """

    #check between var specification
    for bv in between.keys():
        for scan, var_pair in scans_dict.items():
            if bv not in var_pair.keys():
                raise BetweenVarMismatchError('Mismatch: {} not specified for {}'.format(bv, scan.scan_id))

    if covars:
        raise NotImplementedError("Non-voxelwise covariates not yet implemented")
    mvmheader = ['Subj']
    scans_dict_sorted = OrderedDict(sorted(scans_dict.items()))
    if within:
        within_vars = OrderedDict(sorted(within.items()))
        mvmheader.extend(within_vars.keys())
    else:
        within_vars = {}
    if between:
        between_vars = OrderedDict(sorted(between.items()))
        mvmheader.extend(between_vars.keys())
    else:
        between_vars = {}
    if vox_covar:
        mvmheader.append(vox_covar)

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
                run = s.proc_runs[use_proc_run]
                if not subbrick_names:
                    subbrick_names = mri_utils.get_subBrick_Map(run.active_stats_file)
                subj_filepaths = []
                if vox_covar:
                    vox_covar_file = run.get_files(pattern=vox_covar_file_pattern, require_singlet=True)
                    subj_filepaths.append(vox_covar_file)
                stats_file = "{}'[{}]'".format(run.active_stats_file, subbrick_names[subbrick_val])
                subj_filepaths.append(stats_file)
                mvmtable.append([s.scan_id] + list(perm) + between_vals + subj_filepaths + ['InputFile'])

    return mvmtable

    # mvmtable = [mvmheader]
    # configTable = readTable2(configFile)
    # conditionTable = readTable2(conditionFile)
    # basetable = subtable(configTable, keep_header=True, **kwargs)
    # s1 = basetable[1][0]    # [0][0] is the header
    # stats1 = get_stats_file(s1, statsDir)
    # subBrickMap = get_subBrick_Map(stats1)
    #
    # id_ind = getColumn(basetable, 'id')
    # site_ind = getColumn(basetable, 'site')
    #
    # for lang, mod, lex in itertools.product(langs, mods, lexs):
    #     for line in basetable[1:]:
    #         subj = line[id_ind]
    #         site = line[site_ind]
    #         statsfile = get_stats_file(subj, statsDir)
    #         subBrickName = subBrickMap[get_subBrick_number(conditionTable, Lang=lang, Mod=mod, Lex=lex)]
    #         mvmtable.append([subj, lang, mod, lex, site, "{}'[{}]'".format(statsfile, subBrickName)])   # fixme: type?

