import codecs
import time
import itertools
import fnmatch
from utils import exceptions

__author__ = 'cort'


def subtable(table, keep_header=True, **kwargs):
    """
    Generates a subtable comprised of only those rows which have ARG in column named KW for all kwargs

    :param table: table to generate subtable from
    :param keep_header: keep or discard the first row (header) of the table
    :param kwargs: kw, arg pairs; each row is checked against every pair, and only rows with value arg in column kw
    (for all kw, arg pairs) are included in subtable
    :return: subtable of all rows that matched all kw, arg criteria
    """
    subtable = []
    if keep_header:
        subtable.append(list(table[0]))
    for line in table[1:]:
        for kw, val in kwargs.iteritems():
            if line[getColumn(table, kw)] != val:
                break
        else:
            subtable.append(list(line))
    return subtable


def dicts_from_table(table, row_nums_as_keys=False, key_col_name=None, key_col=0):
    """
    Creates a dict of dicts from a table, with form {key_col: {other_col_names: other_col_values}}

    :param table: table to parse to dicts
    :param row_nums_as_keys: use row numbers as keys. overrides other key options
    :param key_col_name: use named column as key. overrides key_col
    :param key_col: use column with this index as key
    """
    header = table[0]
    values = table[1:]
    d = {}
    if row_nums_as_keys:
        for i, row in enumerate(values, start=1):
            d[i] = {header[ii]: row[ii] for ii in range(0, len(header))}
    else:
        if key_col_name:
            try:
                key_col = header.index(key_col_name)
            except ValueError:
                print '{} is not a valid column name in {}'.format(key_col_name, header)
                raise
        for row in values:
            d[row[key_col]] = {header[ii]: row[ii] for ii in range(0, len(header)) if ii != key_col}
    return d


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


def getLocalTime(hr_min=True):
    """
    Returns local time in the format YEAR_MONTH_DAY_HOUR_MINUTE
    """
    t = time.localtime()
    localtime = '{}_{}_{}'.format(str(t[0]), str(t[1]), str(t[2]))
    if hr_min:
        localtime = '{}_{}h_{}m'.format(localtime, str(t[3]), str(t[4]))

    return localtime


def getColumn(table, colName):
    """
    :param table:
    :param colName:
    :return: integer index of the named column if it exists, else None
    """
    names = list(table[0])
    try:
        col = names.index(colName)
    except ValueError:
        col = None
    except:
        raise
    return col


def getNamedLines(f, names, encodings=('utf-16-le', 'utf-8', 'utf-16-be'), checkTo=None):
    """
    Reads a file and returns a map of names:lines for each name in names.
    Args
        f: 		the file to read
        names:  names of lines to return (checks for the string at the beginning of each line)
    Returns
        {name : [lines]} mapping for each name in names
    """

    fieldMap = {}
    for encoding in encodings:
        with codecs.open(f, 'rU', encoding=encoding) as infile:
            ln = 0
            for name in names:
                fieldMap[name] = []
            line = 1
            while line:
                line = infile.readline()
                ln += 1
                for name in names:
                    if line.find(name) == 0:
                        fieldMap[name].append(line)
                if checkTo and ln > checkTo: break
            if [] not in fieldMap.values():
                return fieldMap


def __main__():
    pass

if __name__ == '__main__':
    __main__()