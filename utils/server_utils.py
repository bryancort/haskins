# -------------------------------------------------------------------------------
# Name:        serverTools
# Purpose:      Collection of classes and functions for data management on the server
#
# Author:      Bryan Cort
#
# Created:     12/02/2014
# -------------------------------------------------------------------------------

import os
import glob
import file_utils


class FilePathError(Exception):
    pass


class A182File:
    """
    Representation of A182 behavioral data files.
    Stores identification info, and additional flags (missing/extra/expected)
    Args
        taskCfg:	Task configuration object
        task:       Name of the experimental task for the file
        subjID:     Subject ID number
        session:	Session number
        fType:		File type string
        flag:       Flag indicating the status of the file
        fPath:		Path to the file. Providing this arg will automatically generate subjID, session, fType,
                    and task from the filename
    """

    def __init__(self, taskCfg=None, task=None, subjID=None, session=None, fExt=None, fType=None, note=None,
                 fPath=None):
        self.task = task
        self.taskCfg = taskCfg
        if taskCfg:
            self.task = self.taskCfg.task
        self.subjID = subjID
        self.session = session
        self.fExt = fExt
        self.fType = fType
        self.note = note
        self.prevName = None
        self.fPath = fPath

        if self.fPath:
            fname = self.fPath.rsplit(os.path.sep, 1)[1]
            parts = fname.split('.', 1)
            #Use the map defined in taskCfg to get the task-specific filetype for this file extension
            self.fExt = parts[1]
            tags = parts[0].split('_')
            self.subjID = tags[0]
            self.session = tags[1]
            self.task = tags[2]
            self.prevName = tags[3]

    def mapType(self, taskCfg):
        """
        Gets the filetype from the taskConfig
        Args
            taskCfg: The taskConfig object associated with this file
        """
        self.taskCfg = taskCfg
        self.fType = self.taskCfg.extMap[self.fExt]

    def __eq__(self, other):
        """
        Checks the calling A182File and one other A182File for equality
        Args
            other: The A182File to compare against self
        Returns
            True iff subjID, session, task, and fType are all equal between files, False otherwise
        """
        return (self.subjID, self.session, self.task, self.fType) == (
            other.subjID, other.session, other.task, other.fType)

    def __repr__(self):
        if self.fPath:
            return self.fPath
        elif self.subjID and self.session and self.task and self.fType:
            return '_'.join([self.subjID, self.session, self.task, self.fType])
        else:
            return 'PLACEHOLDER'


class TaskConfig:
    """
    Holds information about files expected for particular A182 tasks
    Args
        configFileEntry: Full row (as a list) from the configuration file
    Attributes:
        task:       	Name of the task
        sessions:       List of expected session numbers (ie., [1,2,3])
        sessionsFiles:  List of file types expected per run
        taskFiles:  	List of expected non-run fileypes (ie., scan sheets, or anything that applies to the task but
                        not individual runs)
        extMap:     	Map of file extensions to filetypes (some tasks have multiple file extensions corresponding to
                        1 filetype, ie zeo)
    """

    def __init__(self, configFileEntry):
        self.task = configFileEntry[0]
        self.sessions = configFileEntry[1].split(',')
        if configFileEntry[2]:
            self.sessionsFiles = configFileEntry[2].split(',')
        else:
            self.sessionsFiles = []
        if configFileEntry[3]:
            self.taskFiles = configFileEntry[3].split(',')
        else:
            self.taskFiles = []
        self.extMap = {}

        mapEntries = configFileEntry[4].split(',')
        for entry in mapEntries:
            pairs = entry.split(':')
            val = pairs[0]
            keys = pairs[1].split(' ')
            for key in keys:
                self.extMap[key] = val

    def __repr__(self):
        return str(self.__dict__)


class Subject:
    """
    Class to store information about A182 behavioral data files for particular subjects. Requires a haskins subject ID
    on init.
    Args
        subjID:         Haskins subject ID for this subject
        taskConfigs:    List of task configurations which generated the list of expected files; if none, no action,
                        if list of TaskConfigs, calls genFileList
    Attributes
        subjID:         Haskins subject ID for this subject
        allFiles:       Set of all files found for this subject
        expectedFiles:  Set of files expected for this subject given the taskConfigs
        matchingFiles:  Subset of expectedFiles that were found for this subject
        missingFiles:   Subset of expectedFiles that were not found for this subject
        extraFiles:     Subset of allfiles not in expected files
        cfgMap:         Mapping of task:taskConfigs
    Methods
        getAllFiles:    Generates the set of all files for the Subject
        genExpFiles:    Generates the set of expected files for the Subject
        genFileSets:	Generates the sets of all, expected, matching, missing, and extra files
    """

    def __init__(self, subjID, taskConfigs=(), files=()):
        self.log = []
        self.subjID = subjID
        self.allFiles = []
        for f in files:
            self.allFiles.append(A182File(fPath=f))
        self.expectedFiles = []
        self.matchingFiles = []
        self.missingFiles = []
        self.extraFiles = []
        self.cfgMap = {}
        for tc in taskConfigs:
            self.cfgMap[tc.task] = tc
        self.genExpectedFiles()

    def genExpectedFiles(self):
        """
        Generates the set of expected files for a subject
        """
        for taskCfg in self.cfgMap.values():
            for tFile in taskCfg.taskFiles:
                self.expectedFiles.append(A182File(taskCfg=taskCfg, subjID=self.subjID, session='T', fType=tFile))
            for sess in taskCfg.sessions:
                for sFile in taskCfg.sessionsFiles:
                    self.expectedFiles.append(A182File(taskCfg=taskCfg, subjID=self.subjID, session=sess, fType=sFile))

    def errlog(self, entry):
        """
        Appends to the error log for this subject
        """
        self.log.append(str(entry))

    def check(self):
        """
        Checks expected vs actual files for self and populates matching, missing, and extra file lists
        """
        for f in self.allFiles:
            try:
                f.mapType(self.cfgMap[f.task])
                if f in self.expectedFiles and f not in self.matchingFiles:
                    self.matchingFiles.append(f)
                else:
                    self.extraFiles.append(f)
            except Exception as e:
                f.note = "Exception type: {0} with value {1} for file {2}".format(type(e), str(e), f.fPath)
                print f.note
                self.errlog(f.note)
                self.extraFiles.append(f)

        for f in self.expectedFiles:
            if f not in self.allFiles:
                self.missingFiles.append(f)

    def __repr__(self):
        return str(self.__dict__)


def mapIDs(ftable='idTable.txt'):
    """
    Looks up MRI IDs and maps them to subject IDs. All ids are stored as strings.
    Args
        ftable:     Simple table of subject and mri IDs. Subject ids in first column, MRI ids  in subsequent columns.
    Returns
        Dict mapping MRI ID : subject ID; currently also maps subject ID : subject ID
    """
    table = file_utils.readTable(ftable)
    idMap = {}
    for row in table:
        for entry in row:
            if entry in idMap.keys():
                continue
            idMap[str(entry)] = str(row[0])
    return idMap


def checkDir(dFile, targDir):
    """
    Checks for a file with the same subject, session, task, and file extension as dFile in targDir.
    Only meaningful for correctly named data files.
    Args
        dFile:      The file to check for
        targDir:    The directory to check in
    Returns
        True if a matching filename exists, False otherwise
    """
    fname = dFile.rsplit(os.path.sep, 1)[-1]  # should work for path names or file names with no path
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
        (oldname, fext, tokens) tuple. Tokens are generated by stripping the file extension and then splitting the
        filename on _ and - characters.
    """
    #pull the extension off the filename and store the old name
    parts = fname.split('.', 1)
    oldname = parts[0]
    fext = parts[1]
    #Convert -'s into _'s and split the filename into tokens
    tokens = oldname.replace('-', '_').split('_')

    return (oldname, fext, tokens)


def getSubjIDs(d, pattern='*'):
    """
    Finds all uniques subject IDs with data files matching pattern in directory d.
    Args
        d: The directory to check for subject data files
    Returns
        Set of all haskins IDs with data files in d
    """
    #find all the files in d that match pattern
    recs = glob.glob(os.path.join(d, pattern))
    #get all the unique ids
    ids = set()
    for f in recs:
        ids.add(f.rsplit(os.path.sep, 1)[1][:4])
    return ids


def getSubjFiles(d, sid, pattern='*'):
    """
    Recurses through the directory and all subdirectories to find all files for a subject sid matching pattern.
    Args
        d:          top of the directory tree to search
        sid:        subject id to get files for
        pattern:    pattern to match; begins matching after sid, so only filename[5:] is matched on
    Returns
        List of paths to all files matching pattern for sid.
    """
    fs = []
    for triple in os.walk(d):
        fs.extend(glob.glob(os.path.join(triple[0], '{0}{1}'.format(str(sid), pattern))))
    return fs