# -------------------------------------------------------------------------------
# Name:        a40_2
# Purpose:      psychopy implementation of emily myers' a40-2 experiment
#
# Author:      Bryan Cort
#
# Created:     12/13/2014
# -------------------------------------------------------------------------------

from core import experiment
from core.interface import MenuPage
from core.stims import Stimulus
from utils import file_utils, base_utils
import psychopy
import os
import glob
import time
import random
import itertools
import traceback
import shutil

# todo: move this setup to __init__?
# visual params
background_color = [0, 0, 0]
foreground_color = [1, 1, 1]
window_units = 'norm'
fullscr = 0
window_scale = [1, 1]

# experimental params
run_nums = [1, 2, 3, 4, 5, 6, 7, 8]
inter_trial_interval = 0.0
trial_duration = 12.0

trial_output = ['ttype', 'trialnumber', 'response', 'displayed']

#path params
config_dir = os.path.normpath('config')
data_dir = os.path.normpath('data')
stims_dir = os.path.normpath('stims')

subj_id_temp_filepath = os.path.join(config_dir, '.last_id.txt')
stims_list_filepath = os.path.join(config_dir, 'stim_order_list.txt')


class RunChoiceMenu(Menu):
    def __init__(self, win, results={'run': None}, run_ids=run_nums):
        Menu.__init__(self, win, results)

        runChoiceMenuText = 'Select a run: '
        runChoiceMenuMap = {}
        for rn in run_ids:
            runChoiceMenuText += '\n[{}]'.format(rn)
            runChoiceMenuMap[str(rn)] = ({'run': rn}, None)
        runChoiceMenuText += '\ne[x]it'
        runChoiceMenuMap['x'] = {'run': None}, None
        runChoicePage = MenuPage(displayvalue=TextStimulus(value=runChoiceMenuText,
                                                                                 color=foreground_color),
                                            keymap=runChoiceMenuMap, menu=self)
        self.set_start_page(runChoicePage)

    def reset(self):
        self.__init__()


def __main__():
    try:
        if os.path.getmtime(subj_id_temp_filepath) - time.time() > 7200.0:  # 2 hours
            os.remove(subj_id_temp_filepath)
        subj_id_dict = {'subject id': ''}
        if os.path.exists(subj_id_temp_filepath):
            with open(subj_id_temp_filepath, 'rU') as f:
                subj_id_dict['subject id'] = f.read()
        while True:
            subj_id_dlg = psychopy.gui.DlgFromDict(subj_id_dict)
            if subj_id_dlg.OK:
                break
        subj_id = subj_id_dict['subject id']
        print subj_id
        with open(subj_id_temp_filepath, 'w') as f:
            f.write(subj_id)

        win = psychopy.visual.Window(allowGUI=False, winType='pyglet', colorSpace='rgb', color=background_color,
                                     units=window_units, fullscr=fullscr, viewScale=window_scale)
        run_menu = RunChoiceMenu(win)
        run = run_menu.run()['run']
        print run

        #construct trials
        stimfile_table = file_utils.readTable2(stims_list_filepath)
        stim_dict = base_utils.dicts_from_table(stimfile_table, row_nums_as_keys=True)
        trials = []
        for trial_num in stim_dict:
            run_id = 'run{}'.format(run)
            filepath = stim_dict[trial_num][run_id]
            trials.append(experiment.Trial(trialnumber=int(trial_num), ttype='run{}'.format(run), output=trial_output,
                                   duration=trial_duration, iti=inter_trial_interval,
                                   stims=(SoundStimulus(name=filepath, stype='sound', value=filepath))))
        trials.sort()
        #run trials
        pass
    except:
        print 'Error while getting subject id and run number'
        raise
    finally:
        pass


if __name__ == '__main__':
    __main__()