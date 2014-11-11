# -------------------------------------------------------------------------------
# Name:        core.experiment
# Purpose:      experiment, block, trial classes
#
# Author:      Bryan Cort
#
# Created:     10/17/2014
# -------------------------------------------------------------------------------

from utils import file_utils, base_utils, exceptions
from psychopy import *


class ExpUtilError(Exception):
    pass


class Listable(object):
    def __init__(self, output='all', key=None):
        """
        param output:   The attributes to write with gen_header_list and gen_attr_list.
        param key:      Key to sort the lists returned by gen_header_list and gen_attr_list with. NOT IMPLEMENTED.
        """
        self.output = output
        self.key = key

    def gen_header_list(self, key=None):
        """
        Returns a list of all attribute name specified by self.output.
        """
        headerlist = []
        key = self.key if not key else key

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

    def gen_attr_list(self, key=None):
        """
        Returns a list of all attributes specified by self.output and sorted by their attribute names in gen_header_list().
        """
        attrlist = []
        key = self.key if not key else key
        for k in self.gen_header_list():
            attrlist.append(str(getattr(self, k)))
        return attrlist

#specifically for HoggingStaticPeriod
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
            import logging      # we only do this if we need it - circular import
            logging.warn('We overshot the intended duration of %s by %.4fs. '
                         'The intervening code took too long to execute.' % (self.name, abs(timeRemaining)))
            return 0
        else:
            wait(timeRemaining, hogCPUperiod=timeRemaining)
            return 1


# fixme: super ugly, was rushed
class Menu:
    def __init__(self, displayvalue, keymap, modvalue, window=None):
        """

        :param displayvalue:    Stimulus object to display on screen for the menu.
        :param keymap:          Mapping of {response key : (new value, next menu)}
        :param modvalue:        Name of the value this menu should set or modify
        :param window:          window to display the menu in
        """
        self.displayvalue = displayvalue
        self.keymap = keymap
        self.modvalue = modvalue
        self.window = window

    def act(self, window=None, clear=True):
        if not window:
            window = self.window
            if not window:
                raise ExpUtilError('Menu requires a window to act in')
        self.displayvalue.present(window, clear=clear)
        event.clearEvents()
        kp = event.waitKeys(keyList=self.keymap.keys())[0]
        # return value to modify, new value, new menu
        return self.modvalue, self.keymap[kp][0], self.keymap[kp][1]


class Stimulus:
    def __init__(self, name=None, stype='text', value=None, onset=0.0, offset=None, stimduration=None, inst=None,
                 action=None, **kwargs):
        """
        :param name:            Name of the stimulus. String or None.
        :param stype:           Type of the stimulus. One of [text, sound, iamge, video, other]. If other, inst must be
                                passed directly.
        :param value:           Value of the stimulus. String to be displayed (for text type stims) or string file path (for
                                sound and video type stims) or None (for other type stims).
        :param onset:           Onset of the stimulus in seconds.
        :param offset:          Offset of the stimulus in seconds. Must be > onset.
        :param stimduration:    Total duration of the stimulus.
        :param inst:            Instantiation of the stimulus. text, iamge, sound, and video type stimuli can be
                                instantiated from the value parameter. other type stims must be manually instantiated
                                and set.
        :param action:          Method to call on 'other' type stims to present them.
        :param kwargs:          Keyword args to be passed to the appropriate psychopy object when instantiate is called.
        """
        self.name = name
        self.stype = stype
        self.value = value
        self.onset = onset
        self.offset = offset
        self.stimduration = stimduration
        self.inst = inst
        self.action = action
        self.kwargs = kwargs

    def __str__(self):
        if self.name:
            return self.name
        elif self.value:
            return self.value
        else:
            return '{}_Stimulus'.format(self.stype)

    def __repr__(self):
        if self.name:
            return self.name
        elif self.value:
            return self.value
        else:
            return '{}_Stimulus'.format(self.stype)

    def instantiate(self, window):
        """
        Placeholder. Subclasses must override this method.

        Uses the stype and value attributes to create an appropriate psychopy object for displaying on the screen.
        To display the stim in a window, you must call Stimulus.present(window).

        :param window:  psychopy.visual.Window associated with the instantiation
        """
        raise ExpUtilError("{} does not implement instantiate().".format(self.__class__.__name__))

    def present(self, window, duration=None, clear=False, **kwargs):
        """
        Placeholder. Subclasses must override this method.

        This method displays stimuli in a psychopy visual.Window (if a window is required for the stimulus).
        Default behaviour is mostly unchanged from the underlying psychopy implementations. Many of these options can
        be accessed by passing the appropriate psychopy keyword arguments. However, some functionality cannot be changed
        in this way. For finer control, work with Stimulus.inst and call the psychopy methods directly.

        :param window: 		Window to present the stimulus in. Psychopy.visual.Window
                                or None (if the stim does not require a window, ie., sound type stims.)
        :param duration:    Duration to present the stimulus for. Static stimuli will remain on the screen
                                for this duration, dynamic stimuli will end after duration has elapsed
                                (if duration is less than the full display time of the stimulus).
                                int, float, or None.
        :param clear:       Preserves (or not) the previous window state before presenting the stim.
                                True clears the window after presenting the stimulus, false restores the previous state.
        :param **kwargs     Keyword args to pass to the psychopy method called by this method
        """
        raise ExpUtilError("{} does not implement present().".format(self.__class__.__name__))

    def prepare(self, window, **kwargs):
        """
        Placeholder. Subclasses must override this method.

        This writes stimuli to the back buffer of a psychopy.visual.Window, allowing multiple stimuli to be displayed
        when flip() is called on the window.
        """
        raise ExpUtilError("{} does not implement prepare().".format(self.__class__.__name__))

    def _deinst(self):
        """
        Sets self.inst to None to allow garbage collection. Might be unnecessary.
        """
        self.inst = None


class TextStimulus(Stimulus):
    def instantiate(self, window):
        """
        Creates a psychopy.visual.TextStim for display in window. Text to display contained in self.value. Any kwargs
        passed to self.__init__ will be passed on to this instantiation.

        :param window:  psychopy.visual.window associated with the TextStimulus.
        """
        self.inst = visual.TextStim(text=self.value, win=window, **self.kwargs)

    def present(self, window, duration=None, clear=False, hogtime=0.2, **kwargs):
        """
        Draws the instantiation of the stimulus to the (back) buffer of window. If duration is specified,
        flips the window, waits for duration, and flips the window again. If duration is not specified, flips the window
        and returns.

        This method should not be used to present stimuli for which rts are being collected.
        For this case, either work directly with the instantiation of the stimulus, or
        subclass and override this method.If the stimulus is not yet instantiated, calls self.instantiate(). In this case,
        self.inst will be reset to None after the stim is presented.

        :param window: 		Window to present the stimulus in.
        :param duration:    Duration to present the stimulus for. If None, defaults to self.stimduration.
        :param clear:       Preserves (or not) the previous window state before presenting the stim.
                                True clears the window after presenting the stimulus, false restores the previous state.
        :param hogtime:     Time during the stimulus presentation to hog cpu.
        :param **kwargs     Additional keyword args to pass to self.inst.draw()
        """
        if not self.inst:
            self.instantiate(window)
        self.inst.draw(win=window, **kwargs)
        window.flip(clearBuffer=clear)    #back buffer now has the previous contents of screen if clear = False
        if not duration:
            duration = self.stimduration
        if duration:
            core.wait(duration, hogCPUperiod=hogtime)
            window.flip()                   #Restore the previous window state if clear = False; back buffer is clear
        # self._deinst()

    def prepare(self, window, **kwargs):
        """
        Instantiates (if required) and draws the TextStimulus to the back buffer of window by calling draw() on the
        instantiation.

        :param window:  psychopy.visual.window to draw to.
        :param kwargs:  additional keyword arguments to pass to self.inst.draw()
        """
        if not self.inst:
            self.instantiate(window)
        self.inst.draw(win=window, **kwargs)
        # self._deinst()


class ImageStimulus(Stimulus):
    def instantiate(self, window):
        """
        Creates a psychopy.visual.ImageStim for display in window. Image file to display contained in self.value.
        Any kwargs passed to self.__init__ will be passed on to this instantiation.

        :param window:  psychopy.visual.window associated with the ImageStimulus.
        """
        self.inst = visual.ImageStim(image=self.value, win=window, **self.kwargs)

    def present(self, window, duration=None, clear=False, hogtime=0.2, **kwargs):
        """
        Draws the instantiation of the stimulus to the (back) buffer of window. If duration is specified, flips the window,
        waits for duration, and flips the window again. If duration is not specified, flips the window and returns.

        :param window: 		Window to present the image in.
        :param duration:    Duration to present the image for. If None, defaults to self.stimduration.
        :param clear:       Preserves (or not) the previous window state before presenting the stim.
                                True clears the window after presenting the stimulus, false restores the previous state.
        :param hogtime:     Time during the stimulus presentation to hog cpu.
        :param **kwargs     Additional keyword args to pass to self.inst.draw()
        """
        if not self.inst:
            self.instantiate(window)
        self.inst.draw(win=window, **kwargs)
        window.flip(clearBuffer=clear)    # back buffer now has the previous contents of screen if clear = False
        if not duration:
            duration = self.stimduration
        if duration:
            core.wait(duration, hogCPUperiod=hogtime)
            window.flip()   # Restore the previous window state if clear = False; back buffer is clear
        # self._deinst()

    def prepare(self, window, **kwargs):
        """
        Instantiates (if required) and draws the ImageStimulus to the back buffer of window by calling draw() on the
        instantiation.

        :param window:  psychopy.visual.window to draw to.
        :param kwargs:  additional keyword arguments to pass to self.inst.draw()
        """
        if not self.inst:
            self.instantiate(window)
        self.inst.draw(win=window, **kwargs)
        # self._deinst()


class SoundStimulus(Stimulus):
    def instantiate(self, window=None):
        """
        Creates a psychopy.sound.Sound for display in window. Text to display contained in self.value. Any kwargs
        passed to self.__init__ will be passed on to this instantiation.

        :param window:  psychopy.visual.window associated with the SoundStimulus. Not required or referenced, but
        included for interchangeability between stimulus types.
        """
        self.inst = sound.Sound(value=self.value, **self.kwargs)

    def present(self, window=None, duration=None, clear=False, hold=False, **kwargs):
        """
        Plays the sound for the specified duration, starting at the beginning of the sound file and calling core.wait()
        for the duration specified. If no duration is specified, plays the full sound file but does not call core.wait()

        This method should not be used to present stimuli for which rts are being collected.
        For this case, either work directly with the instantiation of the stimulus, or
        subclass and override this method.

        :param window: 		psychopy.visual.window associated with the SoundStimulus. Unlike visual stims, can be None.
        :param duration:    Duration to play the sound for. If greater than the duration of the audio file, fills the
                            remaining time with silence.
        :param clear:       Preserves (or not) the previous window state before presenting the stim.
                                True clears the window after presenting the stimulus, false restores the previous state.
        :param hold:        Hold execution with core.wait() for the duration of the sound.
        :param **kwargs     Keyword args to pass to the psychopy method called by this method
        """
        if not self.inst:
            self.instantiate(window)
        if hold:
            duration = self.inst.getDuration()
        self.inst.play()
        if duration:
            core.wait(duration)
            self.inst.stop()
        if clear and window:
            window.flip()
        # self._deinst()


class VideoStimulus(Stimulus):
    def instantiate(self, window):
        """
        Creates a psychopy.visual.MovieStim for display in window. Movie file referenced by self.value. Any kwargs
        passed to self.__init__ will be passed on to this instantiation.

        :param window:  psychopy.visual.window associated with the VideoStimulus.
        """
        self.inst = visual.MovieStim(filename=self.value, win=window, **self.kwargs)

    def present(self, window, duration=None, clear=False, **kwargs):
        """
        Plays video. If duration is specified, plays up to that duration, otherwise plays the full movie.

        This method should not be used to present stimuli for which rts are being collected.
        For this case, either work directly with the instantiation of the stimulus, or
        subclass and override this method.

        :param window: 		Window to play the video in.
        :param duration:    Duration to play the video for. If greater than the duration of the video file, displays the
                            final frame for the remaining time.
        :param clear:       Preserves (or not) the previous window state before presenting the stim.
                                True clears the window after presenting the stimulus, false restores the previous state.
        :param **kwargs     Additional keyword args to pass to the psychopy method called by this method
        """
        restoreWin = None
        if not self.inst:
            self.instantiate(window)
        if not clear:
            #better way to implement this? Some way to grab all objects from a buffer, instead of pixel by pixel?
            restoreWin = visual.BufferImageStim(win=window, buffer='front')
        mov = self.inst

        movPlayTime = duration if duration else mov.duration
        mov.autoDraw = True
        mov.seek(0.0)
        mov.draw()
        movClock = core.Clock()
        window.callOnFlip(movClock.reset)
        window.flip()
        mov.play()
        while movClock.getTime() < movPlayTime:
            mov.draw()
            window.flip()
        if not clear:
            restoreWin.draw()
        window.flip()
        # self._deinst()


class OtherStimulus(Stimulus):
    def present(self, window, duration=None, clear=False, **kwargs):
        """
        Presents the stimulus by calling (from self.inst) the method stored in self.action.

        This method should not be used to present stimuli for which rts are being collected.
        For this case, either work directly with the instantiation of the stimulus, or
        subclass and override this method.

        :param window: 		Window to present the stimulus in.
        :param duration:    Duration to wait after calling the method referenced by self.action.
        :param clear:       Preserves (or not) the previous window state before presenting the stim.
                                True clears the window after presenting the stimulus, false restores the previous state.
        :param **kwargs     Keyword args to pass to the method referenced by self.action.
        """
        restoreWin = None
        if not self.inst:
            self.instantiate(window)
        if window:
            if not clear:
                restoreWin = visual.BufferImageStim(win=window, buffer='front')
            getattr(self.inst, self.action)(window, **kwargs)
        else:
            getattr(self.inst, self.action)(**kwargs)
        window.flip()
        if duration:
            core.wait(duration)
        if not clear and window:
            restoreWin.draw()
        window.flip()
        # self._deinst()


class Trial(Listable):
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
        raise NotImplementedError("run() not implemented for parent class Trial")

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


def fixcross(value='+', color=(1, 1, 1), **kwargs):
    """
    Wrapper for psychopy.visual.visual.TextStim. See psychopy API at http://www.psychopy.org/api/api.html
    """
    return TextStimulus(value=value, color=color, **kwargs)


# def main():
#     pass
#
# if __name__ == '__main__':
#     main()

