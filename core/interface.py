# -------------------------------------------------------------------------------
# Name:        core.interface
# Purpose:      basic menu page and menu sequence implementations
#
# Author:      Bryan Cort
#
# Created:     11/17/2014
# -------------------------------------------------------------------------------

from psychopy import *
from core.experiment import ExpUtilError


class MenuPage:
    def __init__(self, displayvalue, keymap, menu):
        """
        Individual menu page

        :param displayvalue: stimulus object to display on screen for the menu.
        :param keymap: mapping of {response key : ({keys_to_mod: new_key_values}, next menu)}
            the results dict of menu
        :param modvalue: name of the value this menu should set or modify
        :param menu: menu that owns this page
        """
        self.displayvalue = displayvalue
        self.keymap = keymap
        self.menu = menu

    def act(self, clear=True):
        window = self.menu.win
        self.displayvalue.present(window, clear=clear)
        event.clearEvents()
        kp = event.waitKeys(keyList=self.keymap.keys())[0]
        # return value to modify, new value, new menu
        mod_dict, next_page = self.keymap[kp]
        return mod_dict, next_page


class Menu:
    def __init__(self, win, results={}):
        """
        Whole menu representation

        :param win: window to display menu pages in
        :param results: initial (base or default) result mapping
        """
        self.win = win
        self.results = {k: v for k, v in results.iteritems()}
        self.active_page = None

    def set_start_page(self, page):
        self.active_page = page

    def run(self):
        if not self.win:
            raise ExpUtilError("Menu object needs a window to display in")
        elif not self.active_page:
            raise ExpUtilError("No active page set for menu")
        while self.active_page:
            results_mod, next_page = self.active_page.act()
            for k, v in results_mod.iteritems():
                self.results[k] = v
            self.active_page = next_page
        self.win.flip()
        return self.results