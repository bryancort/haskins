# -------------------------------------------------------------------------------
# Name:        a40_2
# Purpose:      psychopy implementation of emily myers' a40-2 experiment
#
# Author:      Bryan Cort
#
# Created:     12/13/2014
# -------------------------------------------------------------------------------

from core import experiment, interface, stims
from utils import file_utils, base_utils
from psychopy import core, gui, visual
import os
import time


class A40P2TrialSequenceRunner(experiment.TrialSequenceRunner):
    def _additional_trial_init(self):
        self._next_trial.stims[0].present()

# todo: move this setup to __init__.py?
# visual params
background_color = [0, 0, 0]
foreground_color = [1, 1, 1]
window_units = 'norm'
fullscr = 0
window_scale = [1, 1]

# experimental params
run_nums = [1, 2, 3, 4, 5, 6, 7, 8]
inter_trial_interval = 0.0
trial_duration = 5.0
warmup_duration = 1.0

trial_output = ['ttype', 'trialnumber', 'response', 'displayed']

# path params
config_dir = os.path.normpath('config')
data_dir = os.path.normpath('data')
stims_dir = os.path.normpath('stim')

subj_id_temp_filepath = os.path.join(config_dir, '.last_id.txt')
stims_list_filepath = os.path.join(config_dir, 'stim_order_list.txt')


class RunChoiceMenu(interface.Menu):
    def __init__(self, win, results={'run': None}, run_ids=run_nums):
        interface.Menu.__init__(self, win, results)

        runChoiceMenuText = 'Select a run: '
        runChoiceMenuMap = {}
        for rn in run_ids:
            runChoiceMenuText += '\n[{}]'.format(rn)
            runChoiceMenuMap[str(rn)] = ({'run': rn}, None)
        runChoiceMenuText += '\ne[x]it'
        runChoiceMenuMap['x'] = {'run': None}, None
        runChoicePage = interface.MenuPage(displayvalue=stims.TextStimulus(value=runChoiceMenuText,
                                                                           color=foreground_color),
                                           keymap=runChoiceMenuMap, menu=self)
        self.set_start_page(runChoicePage)

    def reset(self):
        self.__init__()


def __main__():
    try:
        if time.time() - os.path.getmtime(subj_id_temp_filepath) > 7200.0:  # 2 hours
            os.remove(subj_id_temp_filepath)
        subj_id_dict = {'subject id': ''}
        if os.path.exists(subj_id_temp_filepath):
            with open(subj_id_temp_filepath, 'rU') as f:
                subj_id_dict['subject id'] = f.read()
        while True:
            subj_id_dlg = gui.DlgFromDict(subj_id_dict)
            if subj_id_dlg.OK:
                break
        subj_id = subj_id_dict['subject id']
        print subj_id
        with open(subj_id_temp_filepath, 'w') as f:
            f.write(subj_id)

        win = visual.Window(allowGUI=False, winType='pyglet', colorSpace='rgb', color=background_color,
                                     units=window_units, fullscr=fullscr, viewScale=window_scale)
        run_menu = RunChoiceMenu(win)
        run = run_menu.run()['run']
    except:
        print 'Error while getting subject id and run number'
        raise
        # print run

    try:
        outfile_name = '{}_run{}_{}.txt'.format(subj_id, run, base_utils.getLocalTime())
        outfile_path = os.path.join(data_dir, outfile_name)
        running_outfile_name = 'backup_{}'.format(outfile_name)
        running_outfile_path = os.path.join(data_dir, running_outfile_name)

        #construct trials
        stimfile_table = file_utils.readTable2(stims_list_filepath)
        stim_dict = base_utils.dicts_from_table(stimfile_table, row_nums_as_keys=True)
        trials = []
        for trial_num in stim_dict:
            run_id = 'run{}'.format(run)
            filename = stim_dict[trial_num][run_id]
            filepath = os.path.join(stims_dir, filename)
            trial_stims = (stims.SoundStimulus(name=filepath, stype='sound', value=filepath),)
            for stim in trial_stims:
                stim.instantiate(window=win)
            trials.append(experiment.Trial(trialnumber=int(trial_num), ttype='run{}'.format(run), output=trial_output,
                                           duration=trial_duration, iti=inter_trial_interval,
                                           stims=trial_stims))
        trials.sort()
    except:
        print 'Error while generating trials'
        raise

    try:
        sequence_runner = A40P2TrialSequenceRunner(trials=trials, window=win, outfile=outfile_path,
                                                   running_outfile=running_outfile_path)
        sequence_runner.run_trials(delay=warmup_duration)
    except:
        print 'Error while running trials'
        raise
    # finally:    # todo: send user back to menu here?
    #     core.quit()


if __name__ == '__main__':
    __main__()