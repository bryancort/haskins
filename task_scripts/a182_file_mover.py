# -------------------------------------------------------------------------------
# Name:        fileMover
# Purpose:      Renames and sorts files into the correct locations on the server
#
# Author:      Bryan Cort
#
# Created:     10/02/2014
#-------------------------------------------------------------------------------

import os
import shutil
import glob
import fnmatch
import tarfile
from utils import file_utils


def mapIDs(ftable='idTable.txt'):
    """
    Looks up MRI IDs and maps them to subject IDs. All ids are stored as strings.
    Args
        ftable:     Simple table of subject and mri IDs. Subject ids go in the first column, MRI ids go in subsequent columns. No restrictions on dimensions.
    Returns
        Dict mapping MRI ID : subject ID; currently also maps subject ID : subject ID
    """
    table = file_utils.readTable2(ftable)
    idMap = {}
    for row in table:
        for entry in row:
            if entry in idMap.keys():
                continue
            # This maps subjIDs to themselves; this is important for renaming functions to work on both MRI IDs and subject IDs
            idMap[str(entry)] = str(row[0])
    return idMap


def checkDir(dFile, targDir):
    """
    Checks for a file with the same subject, session, task, and file extension as dFile in targDir. Only meaningful for correctly named data files.
    Args
        dFile:      The file to check for
        targDir:    The directory to check in
    Returns
        True if a matching filename exists, False otherwise
    """
    fname = dFile.rsplit(os.path.sep, 1)[-1]  #should work for path names or file names with no path
    fparts = fname.rsplit('.', 1)
    fext = fparts[-1]
    tokens = fparts[0].split('_')
    subjID = tokens[0]
    session = tokens[1]
    task = tokens[2]
    fMatch = '{0}_{1}_{2}*.{3}'.format(subjID, session, task, fext)
    if glob.glob(targDir + os.path.sep + fMatch):
        return True
    return False


def tokenize(fname):
    """
    Parses a filename and returns tokens useful for reconstructing an informative filename
    Args
        fname: the filename to tokenize
    Returns
        (oldname, fext, tokens) tuple. Tokens are generated by stripping the file extension and then splitting the filename on _ and - characters.
    """
    #pull the extension off the filename and store the old name
    parts = fname.split('.', 1)
    oldname = parts[0]
    fext = parts[1]
    #Convert -'s into _'s and split the filename into tokens
    tokens = oldname.replace('-', '_').split('_')

    return (oldname, fext, tokens)


def tarStrain(d):
    """
    Looks for strain recordings for each participant and compresses them into a single .tar.gz
    Args
        d: Directory to look for strain recordings in
    """
    #find all the strain recordings
    strainRecs = glob.glob(os.path.join(d, '*StrainNaming*.wav'))
    recMap = {}
    for rec in strainRecs:
        recMap[rec] = rec.rsplit(os.path.sep, 1)[-1]  #pathname:filename
    #get all the unique ids
    ids = set()
    for f in recMap.values():
        ids.add(f[:4])  #TODO: improve this with actual regex/pattern matching later
    #check for existing archives for each id
    for n in ids:
        if not glob.glob(os.path.join(d, '{0}_?_strain*.tar.gz'.format(n))):
            #tar.gz all files for each id without an archive
            with tarfile.open(os.path.join(d, '{0}_Strain_Recordings.tar.gz'.format(n)), 'w:gz') as tar:
                for f in glob.glob(os.path.join(d, '{0}*StrainNaming*.wav'.format(n))):
                    tar.add(f, arcname=f.rsplit(os.path.sep, 1)[-1])


# TODO: Add tar.gz'ing for hebb2 if needed
def tarHebb(d):
    """
    Looks for hebb recordings for each participant and compresses them into a single .tar.gz
    Args
        d: Directory to look for hebb recordings in
    """
    #find all the hebb recordings
    hebbRecs = glob.glob(os.path.join(d, '[0-9][0-9][0-9][0-9]*[Hh][Ee][Bb][Bb]*.[wm][ap][v3]'))
    recMap = {}
    for rec in hebbRecs:
        recMap[rec] = rec.rsplit(os.path.sep, 1)[-1]  #pathname:filename
    #get all the unique ids
    ids = set()
    for f in recMap.values():
        ids.add(f[:4])  # TODO: improve this with actual regex/pattern matching later
    for n in ids:
        #check for existing archives for each id
        if not glob.glob(os.path.join(d, '*Hebb_{0}_?_hebb*.tar.gz'.format(n))):
            #tar.gz all files for each id without an archive
            with tarfile.open(os.path.join(d, 'HaskinsHebb-{0}-T.tar.gz'.format(n)), 'w:gz') as tar:
                for f in glob.glob(os.path.join(d, '{0}*[Hh][Ee][Bb][Bb]*.[wm][ap][v3]'.format(n))):
                    tar.add(f, arcname=f.rsplit(os.path.sep, 1)[-1])


def _id_filter(tokens, filters):
    """
    applies each filter to each token; if filter[0] matches a token, take the filter[1]:filter[2] substring of token and
    return it if it is the only match

    :param tokens: list of tokens to filter
    :param filters: filter triplets (pattern, start, stop) to apply
    :returns match: single token matching and filtered by a single filter,
    """
    _match = []
    for token in tokens:
        for pair in filters:
            if fnmatch.fnmatch(token, pair[0]):
                if pair[1]:
                    filtered = ''
                    for ind in pair[1]:
                        filtered += token[ind]
                    _match.append(filtered)
                else:
                    _match.append(token)
    if not _match:
        return 0
    match = _match.pop()
    if _match:
        return None
    return match


def main():
    dry_run = False

    #directory paths
    # todo: replace this with an argument parser and useful defaults
    base_dir = os.path.normpath("/data1/A182/A182BehavioralData")

    os.chdir(base_dir)

    transferDir = os.path.normpath("TRANSFER")
    rawdataDir = os.path.normpath("RAWDATA")
    dataDir = os.path.normpath("DATA")

    idMap = mapIDs()
    # FIXME: CODE CHECKS TASK NAME FOR THE STRING 'fmri' TO DECIDE WHETHER AN ID IS SUBJECT OR MRI
    pmap = {"tb????[-_]*.*": 'biopac',
            "*HaskinsHebb[-_]*[-_]*.[et][dxa][atr]*": 'hebb',
            "*HebbLouisa*.[et][dxa][atr]*": 'hebb2',
            "[0-9][0-9][0-9][0-9]_hebb_version[0-9].txt": 'hebb2',
            "out.[0-9][0-9][0-9][0-9].txt": 'hebb2',
            "*ALL_fMRI[-_]*[-_]*.*": 'SALfmri',
            "*ArtLex_A182ET[-_]*[-_]*.*": 'SALtrain',
            "[0-9][0-9][0-9][0-9][-_][0-9].[eE][dD][fF]": 'SALtrain',
            "*CC[0-9][0-9][0-9]*dat.*": 'SCC',
            "*SRT2[-_]*[-_][123].*": 'SRTT',    # fixme: also checking for SRTT to tag files as scans
            "st[0-9][0-9][0-9][0-9].*": 'stopsignal',
            "*[-_]Strain*.[tcl][xsao][tvrg]*": 'strain',  #covers txt, csv, log, .tar.gz files
            "A182Exp2[-_]VAL3[-_]*[-_]*.*": 'VAL3train',
            "????[-_][ABC].[tdcD][xasA][tvT]": 'zeo',  #covers txt, dat, and csv files
            "*VAL_fMRI[-_]*[-_]*.*": 'VAL3fmri'
    }

    id_filters = (('tb[0-9][0-9][0-9][0-9]', None),                 # anything with a tb number
                  ('[0-9][0-9][0-9][0-9]', None),                   # anything with *_idnum_* or idnum_*
                  ('out.[0-9][0-9][0-9][0-9]', (4, 5, 6, 7)),       # hebb processed files
                  ('CC[0-9][0-9][0-9][0-9]dat', (2, 3, 4, 5)),      # SCC
                  ('st[0-9][0-9][0-9][0-9]', (2, 3, 4, 5)))         # stopsignal

    session_filters = (('s[0-9]', (1,)),
                       ('[0-9]', None),
                       ('out.[0-9][0-9][0-9][0-9]', (0, 1, 2)),
                       ('version[0-9]', (0, 7)))

    #read in all the files and map full path name : filename
    transfer_files = []
    for triple in os.walk(transferDir):
        #tar.gz any hebb recordings
        tarHebb(triple[0])
        #tar.gz any strain recordings
        tarStrain(triple[0])
        #get a simple list of all the file paths
        transfer_files.extend(glob.glob(os.path.join(triple[0], '*.*')))

    moved_raw = []
    moved_data = []
    duplicate_raw = []
    duplicate_data = []
    unmatched_files = []
    no_id_files = []
    full_log = []

    try:
        for transfer_file in transfer_files:
            full_log.append(transfer_file)
            try:
                task = None
                transfer_file_name = os.path.split(transfer_file)[1]
                for pattern in pmap:
                    if fnmatch.fnmatch(transfer_file_name, pattern):
                        task = pmap[pattern]
                if task:
                    transfer_file_name_noext, transfer_file_ext, transfer_file_tokens = tokenize(transfer_file_name)
                    scan_id = _id_filter(transfer_file_tokens, id_filters)
                    try:
                        if 'fmri' in task or 'SRTT' in task:
                            subj_id = idMap['tb' + scan_id]
                        else:
                            subj_id = idMap[scan_id]
                    except KeyError:
                        no_id_files.append(transfer_file)
                        full_log.append("No subject ID mapped to {}".format(scan_id))
                        continue
                    session_id = _id_filter(transfer_file_tokens, session_filters)
                    if session_id == 0:
                        session_id = 1
                    if session_id == None:
                        print "Warning: multiple session ID matches for {}".format(transfer_file)
                    new_file_name = "{}_{}_{}_[{}].{}".format(subj_id, session_id, task, transfer_file_name_noext,
                                                              transfer_file_ext)

                    if not checkDir(new_file_name, rawdataDir):
                        new_file_path = os.path.join(rawdataDir, new_file_name)
                        if not dry_run:
                            shutil.copy(transfer_file, new_file_path)
                        moved_raw.append("{} --> {}".format(transfer_file, new_file_path))
                        full_log.append("Added to RAWDATA")
                    else:
                        duplicate_raw.append(transfer_file)
                        full_log.append("Already in RAWDATA")
                    if not checkDir(new_file_name, os.path.join(dataDir, task)):
                        new_file_path = os.path.join(dataDir, task, new_file_name)
                        if not dry_run:
                            shutil.copy(transfer_file, new_file_path)
                        moved_data.append("{} --> {}".format(transfer_file, new_file_path))
                        full_log.append("Added to DATA")
                    else:
                        duplicate_data.append(transfer_file)
                        full_log.append("Already in DATA")
                else:
                    unmatched_files.append(transfer_file)
                    full_log.append("No matching task")

            except Exception as e:
                print "Unhandled exception while processing {}".format(transfer_file)
    except:
        raise
    finally:
        with open('rawdataTransferLog.txt', 'w') as rawlog:
            rawlog.write("\n".join(moved_raw))
        with open('dataTransferLog.txt', 'w') as datalog:
            datalog.write("\n".join(moved_data))
        with open('unmatched_task_files.txt', 'w') as unmatchedlog:
            unmatchedlog.write("\n".join(unmatched_files))
        with open('unmatched_id_files.txt', 'w') as no_id_log:
            no_id_log.write("\n".join(no_id_files))
        with open('full_log.txt', 'w') as full_log_file:
            full_log_file.write("\n".join(full_log))
        print '{} total files'.format(len(transfer_files))
        print '{} files moved to {}'.format(len(moved_raw), rawdataDir)
        print '{} files moved to {}'.format(len(moved_data), dataDir)
        print '{} duplicate files not moved to {}'.format(len(duplicate_raw), rawdataDir)
        print '{} duplicate files not moved to {}'.format(len(duplicate_data), dataDir)
        print '{} files could not be matched to a task'.format(len(unmatched_files))
        print '{} files could not be matched to an ID'.format(len(no_id_files))


if __name__ == '__main__':
    main()
