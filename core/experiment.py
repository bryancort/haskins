# -------------------------------------------------------------------------------
# Name:        core.experiment
# Purpose:      experiment, block, trial classes
#
# Author:      Bryan Cort
#
# Created:     10/17/2014
# -------------------------------------------------------------------------------

from psychopy import event, core

from mixins import Keyed, Comparable


class ExpUtilError(Exception):
    pass


class Listable(object):
    def __init__(self, output='all', sort_key=None):
        """
        param output:   The attributes to write with gen_header_list and gen_attr_list.
        param key:      Key to sort the lists returned by gen_header_list and gen_attr_list with. NOT IMPLEMENTED.
        """
        self.output = output
        self.sort_key = sort_key

    def gen_header_list(self, sort_key=None):
        """
        Returns a list of all attribute name specified by self.output.
        """
        headerlist = []
        sort_key = self.sort_key if not sort_key else sort_key

        if self.output == 'all':
            for k in self.__dict__.iterkeys():
                if k != 'output' and k[0] != '_':
                    headerlist.append(k)
        elif self.output:
            for k in self.output:
                if hasattr(self, k):
                    headerlist.append(k)
        else:
            raise ExpUtilError('output parameter for a Listable object must be \'all\' or a non-empty list of strings.')
        headerlist.sort()
        return headerlist

    def gen_attr_list(self, sort_key=None):
        """
        Returns a list of all attributes specified by self.output and sorted by their attribute names in gen_header_list().
        """
        attrlist = []
        sort_key = self.sort_key if not sort_key else sort_key
        for k in self.gen_header_list():
            attrlist.append(str(getattr(self, k)))
        return attrlist

# specifically for HoggingStaticPeriod
from psychopy.core import StaticPeriod, wait
from psychopy.constants import *


class HoggingStaticPeriod(StaticPeriod):
    def complete(self):
        """Completes the period, using up whatever time is remaining with a call to wait()

        :return: 1 for success, 0 for fail (the period overran)
        """
        self.status = FINISHED
        timeRemaining = self.countdown.getTime()
        if self.win:
            self.win.setRecordFrameIntervals(self._winWasRecordingIntervals)
        if timeRemaining < 0:
            import logging  # we only do this if we need it - circular import

            logging.warn('We overshot the intended duration of %s by %.4fs. '
                         'The intervening code took too long to execute.' % (self.name, abs(timeRemaining)))
            return 0
        else:
            wait(timeRemaining, hogCPUperiod=timeRemaining)
            return 1


class Trial(Listable, Keyed, Comparable):
    def __init__(self, trialnumber=None, abstrialnumber=None, ttype=None, duration=None, iti=0.0, message=None,
                 stims=(), response=None, correctresponse=None, rt=None, accuracy=None, output='all', displayed=0):
        """
        :param trialnumber:         Number of the trial within the containing block. Int, String, or None.
        :param abstrialnumber:	    Absolute number of the trial (does not reset between blocks). Int, String, or None.
        :param ttype:		        Trial type. String or None.
        :param duration:            Duration of the trial. Int, Float or None.
        :param iti:                 Intertrial interval
        :param message:             Message to display before the trial is run. Stimulus or None.
        :param stims:               List of Stimulus objects to display in the trial.
        :param response:            Subject's response to the trial. String or None.
        :param correctresponse:     Expected response to this trial
        :param rt:                  Subject's reaction time for the trial. String, Float, or None.
        :param accuracy:            Subject's accuracy on the trial. String or None.
        :param output:              Trial attributes to record in the output file. 'all', List of Strings, or None.
                                        NB: Default ('all') is very verbose.
        :param displayed:           Whether trial was displayed or not
        """
        Listable.__init__(self, output)
        self.iti = iti
        self.trialnumber = trialnumber
        self.abstrialnumber = abstrialnumber
        self.ttype = ttype
        self.duration = duration
        self.message = message
        self.stims = stims
        self.response = response
        self.correctresponse = correctresponse
        self.rt = rt
        self.accuracy = accuracy
        self.output = output
        self.displayed = displayed

    def run(self):
        raise NotImplementedError("{} does not implement run().".format(self.__class__.__name__))

    def __key__(self):
        return self.trialnumber

    def __str__(self):
        return 'Trial_num_{}_type_{}'.format(str(self.trialnumber), str(self.ttype))

    def __repr__(self):
        return 'Trial_num_{}_type_{}'.format(str(self.trialnumber), str(self.ttype))


class Block(Listable):
    def __init__(self, blockname=None, btype=None, intro=(), trials=(), output='all'):
        """
        :param blockname: Number of the block. Integer, String or None.
        :param btype:       Type of the block. String or None.
        :param intro:       List of stims to display as an intro to the block.
        :param trials:      List of trials in the Block.
        :param output:      Block attributes to record in the output file. 'all', List of Strings, or None.
                                NB: Default ('all') is very verbose.
        """
        Listable.__init__(self, output)
        self.blockname = blockname
        self.btype = btype
        self.intro = intro
        self.trials = trials
        self.output = output

    def __str__(self):
        return 'Block_num_{}_type_{}'.format(str(self.blockname), str(self.btype))

    def __repr__(self):
        return 'Block_num_{}_type_{}'.format(str(self.blockname), str(self.btype))


class Experiment(Listable):
    def __init__(self, name=None, intro=(), subject=None, blocks=(), output='all'):
        """
        :param name:    Name of the experiment. String or None.
        :param intro:   Instructions to show before running any blocks. Stimulus or None.
        :param subject: Name or ID number of the subject being run in this instance of the experiment. String or None.
        :param blocks:  List of Blocks to run in order. List will be sorted before being run. (???)
        :param output:  Experiment attributes to record in the output file. 'all', list of Strings, or None.
                            NB: Default ('all') is very verbose.
        """
        Listable.__init__(self, output)
        self.name = name
        self.intro = intro
        self.subject = subject
        self.blocks = blocks
        self.output = output

    def __str__(self):
        return '{}_Experiment'.format(str(self.name))

    def __repr__(self):
        return '{}_Experiment'.format(str(self.name))


class TrialSequenceRunner:
    def __init__(self, trials, window, outfile, running_outfile=None, outfile_sep='\t', hogging_period=True):
        """
        Class for running trial sequences with precise timing

        :param trials: iterable of trials to run
        :param window: window to run trials in
        :param outfile: file to save output to at the end of the run
        :param running_outfile: file to save output to after each trial (in case of experiment crash/data loss)
        :param outfile_sep: separator to use when formatting the output files
        :param hogging_period: use a hogging static period (True) or a regular static period (False). rt collection
            requires a hogging static period.
        """
        self.window = window
        self.outfile = outfile
        self.running_outfile = running_outfile
        self.outfile_sep = outfile_sep
        self.trials = trials
        self.period = None
        if hogging_period:  # todo: might want to move screenHz into params
            self.period = HoggingStaticPeriod(win=self.window, screenHz=60, name='HoggingStaticPeriod')
        else:
            self.period = StaticPeriod(win=self.window, screenHz=60, name='StaticPeriod')

        self._next_trial = trials[0]
        self._current_trial = None
        self._last_trial = None

        self.clock = core.Clock()

        # self._load_next_trial()

    def _save_last_trial(self):
        """
        save the previous trial's data to the running save file
        """
        if self.running_outfile:
            with open(self.running_outfile, 'a') as running_outfile:
                running_outfile.write('\n')
                running_outfile.write(self.outfile_sep.join(self._last_trial.gen_attr_list()))

    def _save_all_trials(self):
        """
        save data from all trials in self.trials to self.outfile
        """
        # self._write_outfile_header(self.outfile)
        with open(self.outfile, 'w') as final_outfile:
            final_outfile.write(self.outfile_sep.join(self.trials[0].gen_header_list()))
            for t in self.trials:
                final_outfile.write('\n')
                final_outfile.write(self.outfile_sep.join(t.gen_attr_list()))

    def _write_outfile_header(self, outfile):
        """
        writes the header info from the first trial in self.trials to outfile

        :param outfile: output file to write header to
        """
        with open(outfile, 'w') as selected_outfile:
            selected_outfile.write(self.outfile_sep.join(self.trials[0].gen_header_list()))

    def _load_next_trial(self):
        """
        call prepare() on all stims for the next trial and start a static period when the window is flipped
        """
        for stim in self._next_trial.stims:
            stim.prepare(window=self.window)

    def _run_next_trial(self):
        """
        run self._next_trial
        """
        self.period.complete()  # complete the current trial
        self.period.start(duration=self._next_trial.duration)
        print self.clock.getTime()
        self.window.flip()
        if self._next_trial:
            self._additional_trial_init()

        last_responses = event.getKeys(timeStamped=self.clock)
        event.clearEvents()
        self.clock.reset()

        self._last_trial = self._current_trial
        self._current_trial = self._next_trial

        if self._last_trial:
            self._last_trial.response = last_responses
            self._save_last_trial()
        try:
            self._next_trial = self.trials[self.trials.index(self._current_trial) + 1]
            self._load_next_trial()
        except IndexError:  # we've reached the end of the sequence
            self._next_trial = None
            self.period.complete()
            print self.clock.getTime()
            last_responses = event.getKeys(timeStamped=self.clock)
            event.clearEvents()
            self._last_trial = self._current_trial
            self._current_trial = self._next_trial
            self._last_trial.response = last_responses
            self._save_last_trial()
        except:
            raise

    def _additional_trial_init(self):
        """
        override to run additional code after the initial flip() call in _run_next_trial().
        """
        pass

    def run_trials(self, delay=12.0, delay_msg_stim=None, start_signal_keys=None, start_signal_wait_stim=None):
        """
        run all trials in the sequence and save the data

        :param delay: time to wait before beginning trials
        :param delay_msg_stim: stim to display while waiting to being trials
        :param start_signal_keys: list of keys to listen for to begin the run. if none, run begins immediately
        :param start_signal_wait_stim: stim to display while waiting for the start signal
        """
        if start_signal_keys:
            if start_signal_wait_stim:
                start_signal_wait_stim.present(window=self.window, clear=True)
            event.waitKeys(keyList=start_signal_keys)
        self.period.start(delay)
        #debug
        self.clock.reset()
        print self.clock.getTime()
        if delay_msg_stim:
            delay_msg_stim.present(window=self.window, clear=True)
        if self.running_outfile:
            self._write_outfile_header(self.running_outfile)
        self.window.callOnFlip(self.clock.reset)
        self.window.clearBuffer()
        self._load_next_trial()
        self.period.complete()
        self.period.start(self._next_trial.duration)
        print self.clock.getTime()
        self.window.flip()
        self._load_next_trial()     # this shouldn't be necessary, but for some reason the fixation cross was not being
        self.window.flip()          # drawn in front of the darker rect on the first trial.
        self._additional_trial_init()
        event.clearEvents()
        self._current_trial = self._next_trial
        self._next_trial = self.trials[self.trials.index(self._current_trial) + 1]
        self._load_next_trial()
        while self._next_trial:
            self._run_next_trial()
        self._save_all_trials()


def main():
    pass

if __name__ == '__main__':
    main()

