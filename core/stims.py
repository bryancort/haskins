# -------------------------------------------------------------------------------
# Name:        core.stims
# Purpose:      wrappers for various psychopy stims
#
# Author:      Bryan Cort
#
# Created:     11/17/2014
# -------------------------------------------------------------------------------

from psychopy import *


class Stimulus:
    def __init__(self, name=None, stype='text', value=None, onset=0.0, offset=None, stimduration=None, inst=None,
                 action=None, **kwargs):
        """
        :param name:            Name of the stimulus. String or None.
        :param stype:           Type of the stimulus. One of [text, sound, image, video, other]. If other, inst must be
                                passed directly.
        :param value:           Value of the stimulus. String to be displayed (for text type stims) or string file path (for
                                sound and video type stims) or None (for other type stims).
        :param onset:           Onset of the stimulus in seconds.
        :param offset:          Offset of the stimulus in seconds. Must be > onset.
        :param stimduration:    Total duration of the stimulus.
        :param inst:            Instantiation of the stimulus. text, image, sound, and video type stimuli can be
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
        raise NotImplementedError("{} does not implement instantiate().".format(self.__class__.__name__))

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
        raise NotImplementedError("{} does not implement present().".format(self.__class__.__name__))


    def prepare(self, window, **kwargs):
        """
        Instantiates (if required) and draws the TextStimulus to the back buffer of window by calling draw() on the
        instantiation.

        :param window:  psychopy.visual.window to draw to.
        :param kwargs:  additional keyword arguments to pass to self.inst.draw()
        """
        if not self.inst:
            self.instantiate(window)

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
        if not self.inst:
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
        window.flip(clearBuffer=clear)  #back buffer now has the previous contents of screen if clear = False
        if not duration:
            duration = self.stimduration
        if duration:
            core.wait(duration, hogCPUperiod=hogtime)
            window.flip()  #Restore the previous window state if clear = False; back buffer is clear
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
        if not self.inst:
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
        window.flip(clearBuffer=clear)  # back buffer now has the previous contents of screen if clear = False
        if not duration:
            duration = self.stimduration
        if duration:
            core.wait(duration, hogCPUperiod=hogtime)
            window.flip()  # Restore the previous window state if clear = False; back buffer is clear
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
        if not self.inst:
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
        :param **kwargs     Keyword args to pass to the psychopy.sound.play()
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
        if not self.inst:
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


def fixcross(value='+', color=(1, 1, 1), **kwargs):
    """
    Wrapper for psychopy.visual.visual.TextStim. See psychopy API at http://www.psychopy.org/api/api.html
    """
    return TextStimulus(value=value, color=color, **kwargs)