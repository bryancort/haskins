# -------------------------------------------------------------------------------
# Name:        core.experiment
# Purpose:      experiment, block, trial classes
#
# Author:      Bryan Cort
#
# Created:     10/17/2014
# -------------------------------------------------------------------------------

from core.stims import TextStimulus
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


# fixme: super ugly, was rushed


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
    def __init__(self, trials, window, outfile, running_outfile=None, outfile_sep='\t'):
        self.window = window
        self.outfile = outfile
        self.running_outfile = running_outfile
        self.outfile_sep = outfile_sep
        self.trials = trials
        self.current_trial = None
        self.next_trial = None
        self.last_trial = None

    def _load_next_trial(self):
        """
        call prepare() on all stims for the next trial
        """
        for stim in self.next_trial.stims:
            stim.prepare(window=self.window)
        self.window.callOnFlip()

    def _save_last_trial(self):
        """
        save the previous trial's data to the running save file
        """
        if self.running_outfile:
            with open(self.running_outfile, 'a') as running_outfile:
                running_outfile.write(self.outfile_sep.join(self.last_trial.gen_attr_list()))

    def _save_all_trials(self):
        pass

    def _write_outfile_header(self, outfile):
        with open(outfile, 'w') as selected_outfile:
            selected_outfile.write(self.outfile_sep.join(self.trials[0].gen_header_list()))

    def run_trials(self):
        """
        run a trial sequence

        """
        pass


def fixcross(value='+', color=(1, 1, 1), **kwargs):
    """
    Wrapper for psychopy.visual.visual.TextStim. See psychopy API at http://www.psychopy.org/api/api.html
    """
    return TextStimulus(value=value, color=color, **kwargs)


def main():
    pass

if __name__ == '__main__':
    main()

