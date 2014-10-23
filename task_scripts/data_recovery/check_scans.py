# -------------------------------------------------------------------------------
# Name:        check_scans
# Purpose:      Reads in tab separated list of scans and checks them against .../dicom/incoming
#
# Author:      Bryan Cort
#
# Created:     16/10/2014
# -------------------------------------------------------------------------------

import fnmatch
from utils import file_utils
from task_scripts.data_recovery import _scans_list_filepath, _dicoms_dir_path, _dicoms_BU_dir_path


class MissingScanFilesError(Exception):
    pass


def check_listed_scans(scans_list_filepath=_scans_list_filepath, dicoms_dir_path=_dicoms_dir_path):
    """
    Parses a list of strings for scan numbers and looks recursively for those scans in the specified directory

    :rtype : object
    :param scans_list_filepath: path to file containing list of scans
    :param dicoms_dir_path: path to directory to check for the scans
    :return: list of scans for which no matches were found
    """
    with open(scans_list_filepath) as scans_list_file:
        text = scans_list_file.read().replace(' ', '')
        lines = text.split('\n')
        entries = []
        for line in lines:
            entries.extend(line.split('\t'))
    entries = list(set(fnmatch.filter(entries, 't[ab][0-9][0-9][0-9][0-9]')))
    all_files = file_utils.getFiles(dicoms_dir_path)
    results = {}
    short_results = {}
    for entry in entries:
        results[entry] = fnmatch.filter(all_files, '*{}*'.format(entry))
        short_results[entry] = fnmatch.filter(all_files, '*{}*.tgz'.format(entry))
    missing_scans = []
    for k, v in short_results.iteritems():
        if not v and not results[k]:
            missing_scans.append(k)
        elif v and not results[k]:
            raise MissingScanFilesError('{} has files but no full archives.'.format(k))
    return missing_scans


def __main__():
    print ' '.join(check_listed_scans())
    print ' '.join(check_listed_scans(dicoms_dir_path=_dicoms_BU_dir_path))


if __name__ == '__main__':
    __main__()