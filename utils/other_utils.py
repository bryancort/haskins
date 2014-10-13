# -------------------------------------------------------------------------------
# Name:        serverTools
# Purpose:      Collection of classes and functions for data management on the server
#
# Author:      Bryan Cort
#
# Created:     12/02/2014
# -------------------------------------------------------------------------------

import time


def msplit(s, *args):
    """
    As string.split, but splits on multiple characters
    :param s: string to split
    :param args: characters to split the string around
    :return: list of substrings
    """
    ns = s
    splitter = args[-1]
    for arg in args[:-1]:
        ns = ns.replace(arg, splitter)
    return ns.split(splitter)


def getLocalTime():
    """
    Returns local time in the format YEAR_MONTH_DAY_HOUR_MINUTE
    """
    t = time.localtime()
    return str(t[0]) + '_' + str(t[1]) + '_' + str(t[2]) + '_' + str(t[3]) + 'h_' + str(t[4]) + 'm'