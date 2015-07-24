# -------------------------------------------------------------------------------
# Name:        utils.pathni
# Purpose:      AFNI file management utilities
#
# Author:      Bryan Cort
#
# Created:     16/03/2015
# -------------------------------------------------------------------------------

# TODO: MOST OF THIS CAN LIKELY BE CONVERTED TO CLASS MRI_DATA + CLASS METHODS

import os

class PathniError(Exception):
    pass

afni_data_types = (".HEAD", ".BRIK", ".nii", ".nii.gz")
afni_spaces = ("+orig", "+tlrc")


def get_type(path, types=afni_data_types):
    for t in types:
        if path.endswith(t):
            return t
    return None


def get_space(path, spaces=afni_spaces):
    ftype = get_type(path)
    chop = len(ftype) if ftype else None
    space_string = path[:chop]
    for s in spaces:
        if space_string.endswith(s):
            return s
    return None

def get_headfile(pair):
    """
    :param pair: pair of files to check
    :return: HEAD file if pair is valid
    :raises: PathniError if pair was not valid
    """
    if len(pair) != 2:
        raise PathniError("Pair must be of length 2, was length {} containing files:\n{}".format(len(pair), pair))
    if pair[0].rstrip(".HEAD") == pair[1].rstrip(".BRIK"):
        return pair[0]
    elif pair[0].rstrip(".BRIK") == pair[1].rstrip(".HEAD"):
        return pair[1]
    raise PathniError("Invalid pair: {}".format(pair))


def brik_from_head(headfile):
    if os.path.exists(headfile):
        if has_brik(headfile):
            return "{}.BRIK".format(headfile[:-5])
        raise PathniError("No matching .BRIK file for {}".format(headfile))
    raise PathniError(".HEAD file {} does not exist".format(headfile))


def head_from_brik(brikfile):
    if os.path.exists(brikfile):
        if has_head(brikfile):
            return "{}.HEAD".format(brikfile[:-5])
        raise PathniError("No matching .HEAD file for {}".format(brikfile))
    raise PathniError(".BRIK file {} does not exist".format(brikfile))


def has_brik(headfile):
    return os.path.exists("{}.BRIK".format(headfile[:-5]))


def has_head(brikfile):
    return os.path.exists("{}.HEAD".format(brikfile[:-5]))


def is_headfile(path):
    return path[-5:] == ".HEAD"


def is_brikfile(path):
    return path[-5:] == ".BRIK"


def remove_pair(headfile):
    if os.path.exists(headfile):
        if has_brik(headfile):
            os.remove(brik_from_head(headfile))
            os.remove(headfile)
            return 1
        os.remove(headfile)
        raise PathniError("No matching .BRIK file for {}".format(headfile))
    raise PathniError(".HEAD file {} does not exist".format(headfile))


def get_tail(path):
    return "+" + os.path.basename(path).rsplit("+")[1]


# todo
def afni_3dcopy(headfile):
    pass


# def path_from_prefix(prefix, top_dir=None):
#     if top_dir:
#         prefix = os.path.join(top_dir, prefix)
#     matches = glob.glob("{}*".format(prefix))
#     if len(matches) == 2:
#         return get_headfile(matches)
#     elif len(matches) > 2:
#         raise PathniError("Multiple matches for prefix {}:\n{}".format(prefix, "\n".join(matches)))
#     elif len(matches) == 1:
#         return matches[0]
#     return None
#
#