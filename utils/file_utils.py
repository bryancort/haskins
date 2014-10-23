# -------------------------------------------------------------------------------
# Name:        utils.file_utils
# Purpose:      file and directory management functions
#
# Author:      Bryan Cort
#
# Created:     20/10/2014
# -------------------------------------------------------------------------------

import types
import os
import shutil
import hashlib
import glob
import fnmatch

import numpy as np

from utils.exceptions import *


def readTable(fPath, delim='\t'):
    """
    Reads in a table as a nparray
    Args
        fPath:		filepath to the table
        delim:		column delimeter of the table
    Returns
        nparray representation of the table
    """
    #read in the id table file; this could be made its own function in thi
    table = np.genfromtxt(fPath, delimiter=delim, dtype=types.StringType)
    #not sure why these " are (sometimes?) inserted, but clear them here
    for elem in np.nditer(table, op_flags=['readwrite']):
        elem[...] = str(elem).replace('"', '')
    return table


def readTable2(fPath, delim='\t', lineDelim='\n', strip=('"', "'")):
    """
    Reads in a table from an input file.

    :param fPath: path the the text file to read the table from
    :param delim: delimiter to split the input file on
    :param strip: iterable of characters to strip from the input
    :return: table (simple list of lists) of the data in the input file
    """
    table = []
    with open(fPath, 'rU') as infile:
        for line in infile.read().split(lineDelim):
            if strip:
                for c in strip:
                    line = line.replace(c, '')
            table.append(line.split(delim))
    if table[-1] == ['']:
        return table[:-1]   # last line is always ['']
    else:
        return table



def writeTable(table, fPath, lineSep='\n', colSep='\t'):
    outtable = [colSep.join(entry) for entry in table]
    with open(fPath, 'w') as outfile:
        outfile.write(lineSep.join(outtable))







def hashCompare(f1, f2, readsize=1024):
    """
    Compares the md5 hashes of two (binary) file objects
    Args
        f1:			first file to hash and compare
        f2:			second file to hash and compare
        readsize:   step size (in bytes) used when reading from the files
    Returns
        True if the hashes are equal, false if not.
    """
    fin = 1
    hash1 = hashlib.md5()
    while fin:
        fin = f1.read(readsize)
        hash1.update(fin)
    fin = 1
    hash2 = hashlib.md5()
    while fin:
        fin = f2.read(readsize)
        hash2.update(fin)
    return hash1.digest() == hash2.digest()


def get_immediate_subdirectories(dir="."):
    """
    Returns a list of all the immediate subdirectory names (without leading path components)
    """
    return [name for name in os.listdir(dir) if os.path.isdir(os.path.join(dir, name))]


def getFiles(tree):
    """
    Returns a list of absolute filepaths to all files in the tree
    """
    files = []
    for t in os.walk(tree):
        for f in t[2]:
            files.append(os.path.abspath(os.path.join(t[0], f)))
    return files


def match_single_file(path=os.path.abspath('.'), pattern='*', except_on_fail=False):
    """
    :param path: Base directory to glob from
    :param pattern: Pattern to match on within the base directory
    :param except_on_fail: Raise an exception on failure to match a single file, or return None
    :return: path to single file if found, else None
    """
    files = glob.glob(os.path.join(path, pattern))
    if files:
        if len(files) == 1:
            return files[0]
    if except_on_fail:
        raise FileError('No single file match for {} at {}'.format(pattern, path))
    return None


def match_single_dir(path=os.path.abspath('.'), pattern='*', except_on_fail=False):
    """
    Tries to find a single subdirectory matching pattern in the top level of path.

    :param path: Directory to search (non-recursive)
    :param pattern: unix style wildcard pattern to match
    :param except_on_fail: Raise an exception on failure to match a single file, or return None
    :return: full path of matching directory iff one directory matches, else None
    """
    for root, dirs, files in os.walk(path):
        d = fnmatch.filter(dirs, pattern)
        if len(d) == 1:
            return os.path.join(root, d[0])
        else:
            if except_on_fail:
                raise FileError('No single directory match for {} at {}'.format(pattern, path))
            return None


def getSubTreeFiles(top, dirs):
    """
    Returns a list of absolute filepaths to all files in the tree with subtree names contained in dirs
    """
    files = []
    if os.path.basename(top) in dirs:
        return getFiles(top)
    else:
        for d in get_immediate_subdirectories(top):
            files.extend(getSubTreeFiles(os.path.join(top, d), dirs))
    return files


def move_files(source, dest, *args):
    """
    Moves files in source matching any unix-style wildcard pattern in *args to dest.

    :param source:  source directory
    :param dest:    destination directory
    :param args:    one or more patterns to match files in source to; only files which match a pattern will be moved
    """
    dest = os.path.normpath(dest)
    files = []
    for p in args:
        files.extend(glob.glob(os.path.join(source, p)))
    if files and not os.path.exists(dest):
        os.makedirs(dest)
    for f in files:
        shutil.move(f, dest)


def copy_files(source, dest, *args):
    """
    Copies files and/or directories in source matching any unix-style wildcard pattern in *args to dest.

    :param source:  source directory
    :param dest:    destination directory
    :param args:    one or more patterns to match files in source to; only files which match a pattern will be moved
    """
    dest = os.path.normpath(dest)
    paths = []
    for p in args:
        paths.extend(glob.glob(os.path.join(source, p)))
    if paths and not os.path.exists(dest):
        os.makedirs(dest)
    for f in paths:
        if os.path.isdir(f):
            shutil.copytree(f, os.path.join(dest, os.path.basename(f)))
        else:
            shutil.copy2(f, dest)


def rename_files(dest, oldSubstr, newSubstr):
    """
    Searches a directory (recursively) for all instances of oldSubstr in filenames and replaces them with newSubstr

    :param dest: Directory to search in
    :param oldSubstr: Substring to replace
    :param newSubstr: Substring to insert
    """
    dest = os.path.normpath(dest)
    for td, ds, fs in os.walk(dest, topdown=False):
        for f in fs:
            # basePath, leaf = os.path.split(f)
            if oldSubstr in f:
                newLeaf = f.replace(oldSubstr, newSubstr)
                oldPath = os.path.join(td, f)
                newPath = os.path.join(td, newLeaf)
                shutil.move(oldPath, newPath)
        basePath, leaf = os.path.split(td)
        if oldSubstr in leaf:
            newLeaf = leaf.replace(oldSubstr, newSubstr)
            newPath = os.path.join(basePath, newLeaf)
            shutil.move(td, newPath)
