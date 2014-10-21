import time
import itertools
import fnmatch
from utils import exceptions

__author__ = 'cort'



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


def mfilter(strs, *patterns):
    """
    as fnmatch.filter, but accepts multiple patterns. keeps items that match one or more of *patterns

    :param strs: list of stings to filter
    :param args: patterns to match with filter
    :return: filtered list
    """
    return list(set(itertools.chain.from_iterable([fnmatch.filter(strs, p) for p in patterns])))


def filter_singlet(strings, pattern, except_on_fail=False):     # todo: test
    """
    Filters a list down to a single item if possible, or returns None or raises an exception if there are multiple or
    no matches

    :param strings: list of strings to filter
    :param pattern: pattern to filter against
    :param except_on_fail: raise an exception (if true) or return None (if false) on failure to match a single item
    :return: matching item, or None
    :except: FileError
    """
    filtered_strings = fnmatch.filter(strings, pattern)
    if len(filtered_strings) == 1:
        return filtered_strings[0]
    elif not except_on_fail:
        return None
    else:
        raise exceptions.FileError('filter_singlet found {} matches'.format(len(filtered_strings)))


def getLocalTime():
    """
    Returns local time in the format YEAR_MONTH_DAY_HOUR_MINUTE
    """
    t = time.localtime()
    return str(t[0]) + '_' + str(t[1]) + '_' + str(t[2]) + '_' + str(t[3]) + 'h_' + str(t[4]) + 'm'