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
import shutil


class A40P2TrialSequenceRunner(experiment.TrialSequenceRunner):  # todo: test
    def _additional_trial_init(self):
        for stim in self._next_trial.stims:
            if stim.stype == 'sound':
                stim.present()


class RunChoiceMenu(interface.Menu):
    def __init__(self, win, results={'run': None}, run_ids=(1,), text_color=(1, 1, 1)):
        interface.Menu.__init__(self, win, results)

        runChoiceMenuText = 'Select a run: '
        runChoiceMenuMap = {}
        for rn in run_ids:
            runChoiceMenuText += '\n[{}]'.format(rn)
            runChoiceMenuMap[str(rn)] = ({'run': rn}, None)
        runChoiceMenuText += '\ne[x]it'
        runChoiceMenuMap['x'] = {'run': None}, None
        runChoicePage = interface.MenuPage(displayvalue=stims.TextStimulus(value=runChoiceMenuText,
                                                                           color=text_color),
                                           keymap=runChoiceMenuMap, menu=self)
        self.set_start_page(runChoicePage)

    def reset(self, window):
        self.__init__(win=window)


def _reformat_output(data_file_path, backup_dir, global_log=None, pulse_id='5', event_list=None):  # todo: test
    """
    reformat our output into something that's a little easier to work with

    :param data_file_path: data file to back up
    :param backup_dir: directory to send our raw data backups to
    :param global_log: path to global log file
    :param pulse_id: string id of magnet pulse
    :param event_list: event list from the TrialSequenceRunner whose trials we are logging
    """
    events = []
    try:
        if global_log:
            if event_list:
                events = event_list
    except:
        events = [experiment.ExperimentEvent(-1, 'ERROR REFORMATTING EVENT LOG')]
        raise  # todo: remove after testing

    data_file_dir, data_file_name = os.path.split(data_file_path)
    raw_backup_name = 'raw_{}'.format(data_file_name)
    shutil.copy2(data_file_path,
                 os.path.join(backup_dir, raw_backup_name))  # copy the raw data in case we screw something up
    data_table = file_utils.readTable2(data_file_path)
    header = data_table[0]
    if 'response' not in header:
        return 0
    else:
        response_index = base_utils.getColumn(data_table, 'response')
        stims_index = base_utils.getColumn(data_table, 'stims')
        data = data_table[1:]
        new_table_header = header[:]
        new_table_header[stims_index] = 'stim_file'
        new_table_header.remove('response')
        new_table_header += ['response_number', 'response_value', 'response_timestamp', 'trial_rt']
        new_table = [new_table_header]
        pulse_events = []
        for i, row in enumerate(data, start=1):
            base_time = _get_onsets(event_list, i)[1]
            temp_row = row[:]
            # fix our stim column since we're here anyway
            stims_str = row[stims_index].strip('()')
            stim_filename = stims_str.split(',')[0]
            temp_row[stims_index] = stim_filename.split(os.path.sep)[-1]
            responses_str = temp_row.pop(response_index).strip('[]()')
            if responses_str:
                responses = responses_str.split('), (')
                for ii in xrange(len(responses) - 1, -1, -1):
                    resp_split = responses[ii].split(',')
                    if resp_split[0] == pulse_id:
                        pulse_events.append(experiment.ExperimentEvent(float(resp_split[1]), 'magnet pulse'))
                        del responses[ii]
                if responses:
                    for num, resp in enumerate(responses, start=1):
                        resp_split = resp.split(',')
                        # getting the rt relative to stims; [0] would be rt relative to trial start. ~10ms difference
                        rel_rt = float(resp_split[1]) - base_time
                        new_table.append(temp_row[:] + [str(num), resp_split[0], resp_split[1], str(rel_rt)])
                else:
                    new_table.append(temp_row[:] + ['NA', 'NA', 'NA', 'NA'])
            else:
                new_table.append(temp_row[:] + ['NA', 'NA', 'NA', 'NA'])
        file_utils.writeTable(new_table, data_file_path)
        if global_log:
            events = events + pulse_events
            events.sort()
            events_str = '\n'.join([str(e) for e in events])
            with open(global_log, 'w') as global_log:
                global_log.write(events_str)
        return 1

# helper logging functions
def _get_onsets(events, trial_number, trial_match_str='Trial {} started', stims_match_str='Trial {} stims started'):
    """
    :param events: list of ExperimentEvent objects for this sequence
    :param trial_number: trial number to retrieve onsets for
    :param trial_match_str: string to match for trial onset
    :param stims_match_str: string to match for stims onset
    :return: trial onset, stims onset tuple
    """
    if not events:
        return 'NA', 'NA'
    trial_start = None
    stims_start = None
    trial_str = trial_match_str.format(trial_number)
    stims_str = stims_match_str.format(trial_number)
    for event in events:
        if event.event_string == trial_str:
            trial_start = event.timestamp
        if event.event_string == stims_str:
            stims_start = event.timestamp
        if trial_start and stims_start:
            return trial_start, stims_start
    return trial_start, stims_start

# todo: move this setup to __init__.py?
# visual params
background_color = [0, 0, 0]
foreground_color = [1, 1, 1]
window_units = 'norm'
fullscr = 1
window_scale = [1, 1]

# experimental params
run_nums = [1, 2, 3, 4, 5, 6]
inter_trial_interval = 0.0
trial_duration = 12.0

warmup_duration = 10.0
pulse_id = ['5']
quit_key = 'q'
mri_warmup_msg = 'starting run'
mri_warmup_stim = stims.TextStimulus(value=mri_warmup_msg, color=foreground_color)
start_wait_msg = 'waiting for mri'
start_wait_stim = stims.TextStimulus(value=start_wait_msg, color=foreground_color)

trial_output = ['ttype', 'trialnumber', 'response', 'stims', 'condition']

# path params
config_dir = os.path.normpath('config')
data_dir = os.path.normpath('data')
backup_dir = os.path.normpath('data/raw_backups')
stims_dir = os.path.normpath('stim')

if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

subj_id_temp_filepath = os.path.join(config_dir, '.last_id.txt')
stims_list_filepath = os.path.join(config_dir, 'stim_order_list.txt')


def __main__():
    run = None
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
        with open(subj_id_temp_filepath, 'w') as f:
            f.write(subj_id)

        win = visual.Window(allowGUI=False, winType='pyglet', colorSpace='rgb', color=background_color,
                            units=window_units, fullscr=fullscr, viewScale=window_scale)
        center_rect = visual.Rect(win=win, width=1.0, height=1.0, lineColor=(-.15, -.15, -.15),
                                  fillColor=(-.15, -.15, -.15))
        center_rect_stim = stims.ImageStimulus(name='center_rect', stype='rectangle', inst=center_rect)
        fix_cross = stims.fixcross('+', foreground_color, height=0.1, depth=1)
        fix_cross.instantiate(window=win)
        base_stims = (center_rect_stim, fix_cross)
        run_menu = RunChoiceMenu(win, run_ids=run_nums, text_color=foreground_color)
        run = run_menu.run()['run']
    except:
        print 'Error while getting subject id and run number'
        raise
    finally:
        if not run:
            core.quit()
    try:
        outfile_name = '{}_run{}_{}.txt'.format(subj_id, run, base_utils.getLocalTime())
        outfile_path = os.path.join(data_dir, outfile_name)
        running_outfile_name = 'backup_{}'.format(outfile_name)
        running_outfile_path = os.path.join(data_dir, running_outfile_name)
        event_log_name = 'EVENTS_{}_run{}_{}.txt'.format(subj_id, run, base_utils.getLocalTime())
        event_log_path = os.path.join(data_dir, event_log_name)

        run_id = 'run{}'.format(run)
        cond_file = file_utils.match_single_file(path=config_dir, pattern='*{}*'.format(run_id),
                                                 except_on_fail=True)
        cond_table = file_utils.readTable2(cond_file)
        cond_dict = base_utils.dicts_from_table(cond_table, row_nums_as_keys=False)

        # construct trials
        stimfile_table = file_utils.readTable2(stims_list_filepath)
        stim_dict = base_utils.dicts_from_table(stimfile_table, row_nums_as_keys=True)
        trials = []
        for trial_num in stim_dict:
            filename = stim_dict[trial_num][run_id]
            condition = cond_dict[filename]['condition']
            filepath = os.path.join(stims_dir, filename)
            try:
                trial_stims = (stims.SoundStimulus(name=filepath, stype='sound', value=filepath),) + base_stims
                for stim in trial_stims:
                    stim.instantiate(window=win)
                trials.append(
                    experiment.Trial(trialnumber=int(trial_num), ttype='run{}'.format(run), list_attrs=trial_output,
                                     duration=trial_duration, iti=inter_trial_interval,
                                     stims=trial_stims, condition=condition))
                # print '{} trial {} has file {}'.format(run_id, trial_num, filename)
            except ValueError as e:
                print 'ERROR: {} trial {} missing file {}'.format(run_id, trial_num, filename)
                raise
        trials.sort()
    except:
        print 'Error while generating trials'
        raise
    sequence_runner = None
    try:
        sequence_runner = A40P2TrialSequenceRunner(trials=trials, window=win, outfile=outfile_path,
                                                   running_outfile=running_outfile_path, quit_key=quit_key,
                                                   event_log_path=event_log_path)
        sequence_runner.run_trials(delay=warmup_duration, delay_msg_stim=mri_warmup_stim,
                                   start_signal_keys=pulse_id, start_signal_wait_stim=start_wait_stim)
    except experiment.InputError as e:
        print e.message
    except:
        print 'Error while running trials'
        raise
    try:
        global_log = event_log_path
        if os.path.exists(running_outfile_path):
            _reformat_output(running_outfile_path, backup_dir, global_log=global_log, event_list=sequence_runner.events)
            global_log = None
    except:
        print 'error reformatting backup data'
        raise
    try:
        if os.path.exists(outfile_path):
            _reformat_output(outfile_path, backup_dir, global_log=global_log, event_list=sequence_runner.events)
    except:
        print 'error reformatting primary data'
        raise


if __name__ == '__main__':
    __main__()