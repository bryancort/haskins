# -------------------------------------------------------------------------------
# Name:        utils.pathni
# Purpose:      AFNI file management utilities
#
# Author:      Bryan Cort
#
# Created:     16/03/2015
# -------------------------------------------------------------------------------

class PathniError(Exception):
    pass

def get_headfile(pair):
    """
    :param pair: pair of files to check
    :return: HEAD file if pair is valid, None if pair is not valid
    """
    if len(pair) != 2:
        raise PathniError("Pair must be of length 2, was length {} containing files:\n{}".format(len(pair), pair))
    if pair[0].rstrip(".HEAD") == pair[1].rstrip(".BRIK"):
        return pair[0]
    elif pair[0].rstrip(".BRIK") == pair[1].rstrip(".HEAD"):
        return pair[1]
    return  None