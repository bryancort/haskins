#!/usr/bin/python
# -------------------------------------------------------------------------------
# Name:        task_scripts.conc_tables.py
# Purpose:      concatenates data files, optionally discarding the unnecessary headers
#
# Arguments:    By default, the script will run on the current directory and discard intermediate headers.
#               To run on a different directory, pass it as an argument to your call. To preserve
#               intermediate headers, pass --headers as an argument. eg., to run on ~/some_dir and
#               preserve headers, call:
#               python conc_tables.py ~/some_dir --headers
#
# Author:      Bryan Cort
#
# Created:     1/13/2015
# -------------------------------------------------------------------------------

import glob
import os
import sys

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

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

def __main__():
    no_headers = 1
    if "--headers" in sys.argv:
        no_headers = 0
        sys.argv.remove("--headers")
    if len(sys.argv) == 1:
        data_dir = get_script_path()
    else:
        data_dir = os.path.normpath(sys.argv[1])
    files = glob.glob(os.path.join(data_dir, "*.csv"))
    files.sort()
    if files:
        conc_table = readTable2(files[0], delim=',')
        for _file in files[1:]:
            _data = readTable2(_file, delim=",")
            conc_table.extend(_data[no_headers:])
        writeTable(conc_table, os.path.join(data_dir, "conc_data.csv"), colSep=",")
    else:
        print "No data files in {}; exiting".format(data_dir)


if __name__ == '__main__':
    __main__()