#!/usr/bin/python

# BC: Added pull directory processing and now ignores case

import tkFileDialog
import fnmatch
from scipy import stats
import numpy as np
import os
import sys
import glob

#Trying to fix import issues in the compiled version
##from scipy.special import _ufuncs


class HebbSequencePair:
    """
    Simple data structure to hold two sequences and basic information about their experimental parameters and simple
    comparisons between them.

    Arguments (stored as class variables):
    heard: The sequence of sounds heard by the participant
    produced: The sequence of sounds produced by the participant
    pType: Hebb (repeated) or filler (non repeated)
    run: The experimental run containing this HebbSequencePair

    Class variables (all above args and the following):
    editDist: The edit distance (Levenshtein Distance; computed by the LD() function) between the two sequences
    absMatch: The number of sounds in the produced sequence which match the heard sequence on both identity and position
    """

    def __init__(self, heard, produced, pType, run):
        self.heard = heard
        self.produced = produced

        self.heard[:] = [x for x in self.heard if x]
        self.produced[:] = [x for x in self.produced if x]

        self.pType = pType
        self.run = run
        self.hebbNum = None

        self.editDist = LD(heard, produced)
        self.absMatch = 0
        for h, p in zip(self.heard, self.produced):
            if h == p:
                self.absMatch += 1

    def setHebbNum(self, hebbNum):
        self.hebbNum = hebbNum

    def __str__(self):
        return str(vars(self))

    def __repr__(self):
        return str(vars(self))


def LD(seq1, seq2):
    """
    Compares two sequences and returns the Levenshtein Distance (http://en.wikipedia.org/wiki/Levenshtein_distance)
    between them. Adapted from example code from that site. #// denotes comments from that example code; # denotes
    comments specific to this implementation.
    """

    #// for all i and j, d[i,j] will hold the Levenshtein distance between
    #// the first i characters of s and the first j characters of t

    seq1 = [i.lower() for i in seq1]
    seq2 = [i.lower() for i in seq2]

    #Rows: seq1, s1, i, m
    #Columns: seq2, s2, j, n

    #initialize the (len(seq1) + 1) by (len(seq2) + 1) array used for computing edit distance
    s1 = list(seq1[:])
    s2 = list(seq2[:])
    s1.insert(0, "")
    s2.insert(0, "")

    m = len(s1)
    n = len(s2)

    #generate the array with all 0's
    d = [[0 for item in s2] for item in s1]

    #// source prefixes can be transformed into empty string by
    #// dropping all characters
    #// target prefixes can be reached from empty source prefix
    #// by inserting every character

    #initialize the first row and column to their column and row indices, respectively; in the matrix,
    #this represents the edit distance between each sequence and an empty string
    for i in range(m):
        d[i][0] = i
    for j in range(n):
        d[0][j] = j

    for j in range(1, n):
        for i in range(1, m):
            if s1[i] == s2[j]:
                d[i][j] = d[i - 1][j - 1]  #// no operation required
            else:
                deletion = d[i - 1][j] + 1
                insertion = d[i][j - 1] + 1
                substitution = d[i - 1][j - 1] + 1

                d[i][j] = min(deletion, insertion, substitution)

    return d[m - 1][n - 1]


def __main__():
    if len(sys.argv) == 2:
        hebb_dir = os.path.normpath(sys.argv[1])


if __name__ == '__main__':
    __main__()


def tokenize2(fname):
    leading_path, _file_name = os.path.split(fname)
    file_name, file_ext = os.path.splitext(_file_name)
    tokens = file_name.replace('-', '_').split('_')
    return leading_path, file_name, file_ext, tokens


def proc_dir(dir_path):
    files = glob.glob(os.path.join(dir_path, "*.txt"))
    for f in files:
        leading_path, file_name, file_ext, tokens = tokenize2(f)
        subj_id = tokens[0]
        out_dir = leading_path
        hebb_file_path = f
        try:
            proc_hebb(subj_id, out_dir, hebb_file_path)
            print "Processed file {}".format(f)
        except:
            print "Skipping file {}".format(f)


def proc_hebb(subjID=None, outDir=None, hebb_file_path=None):
    if not subjID:
        subjID = raw_input("Enter the subject ID: ")
    if not outDir:
        outDir = tkFileDialog.askdirectory(title='Select the output directory: ')
    hebbEx = 'H*'
    seqMap = {'all': {}}
    seqLength = None
    prevRun = None
    n = 1

    #Read in subject response, expected response file
    if not hebb_file_path:
        hebb_file_path = tkFileDialog.askopenfilename(title="Select the input file:"), 'rU'
    with open(hebb_file_path) as infile, open(os.path.join(outDir, 'out.' + str(subjID) + '.txt'), 'w') as outfile:
        currLine = infile.readline()
        splitLine = currLine.split('\t')

        #Skip lines that are not data until we get to the first line with data
        while splitLine[0] != 'f' and not fnmatch.fnmatch(splitLine[0], hebbEx):
            currLine = infile.readline()
            splitLine = currLine.split('\t')

        hPairs = []  #list to hold the variable number of filler trials before each hebb trial and the hebb trial itself
        ##	seqLength = len(splitLine[3:])
        #Iterate over the file
        hCount = 0
        while currLine:
            pairType = splitLine[0]
            runNum = splitLine[1]
            if runNum != prevRun:  #reset hPairs so we don't pick up the last filler trials of a previous run
                hPairs = []
                prevRun = runNum
            heardSeq = splitLine[3:]
            heardSeq[-1] = heardSeq[-1].rstrip('\n')  #strip the end of line markers from the heard sound tokens
            currLine = infile.readline()
            splitLine = currLine.split('\t')
            prodSeq = splitLine[3:]
            prodSeq[-1] = prodSeq[-1].rstrip('\n')  #strip the end of line markers from the produced sound tokens

            hPairs.append(HebbSequencePair(heard=heardSeq, produced=prodSeq, pType=pairType, run=runNum))


            #If the current trial is a hebb trial, add it and all it's filler trials to the map for all runs and the map for its associated run
            if fnmatch.fnmatch(pairType, hebbEx):
                #set the hebb number for each HebbSequencePair
                hn = pairType.lstrip('H')
                if hn:
                    hebbNum = int(hn)
                else:
                    hCount += 1
                    hebbNum = hCount
                for pair in hPairs:
                    pair.setHebbNum(hebbNum)
                seqMap['all'][n] = hPairs
                n += 1
                #create the map for this run if it doesn't already exist
                if runNum not in seqMap.keys():
                    seqMap[runNum] = {}
                seqMap[runNum][hebbNum] = hPairs
                #reset the list for the next hebb number
                hPairs = []

            #Skip lines that are not data until we get to the next line with data
            while splitLine[0] != 'f' and not fnmatch.fnmatch(splitLine[0], hebbEx):
                currLine = infile.readline()
                if not currLine:  #we're at the end of the file
                    break
                splitLine = currLine.split('\t')

        seqLength = len(seqMap['all'][1][0].heard)

        #Write the output
        outfile.write('SubjNum\tRun\tTrialType\tHebbNumber\tEditDistance\tEditDistanceScore\tSlotDistanceScore')
        for hNum in sorted(seqMap['all'].keys()):
            for trialPair in seqMap['all'][hNum]:
                outfile.write('\n' + str(subjID) + '\t' + str(trialPair.run) + '\t' + str(trialPair.pType) + '\t' + str(
                    trialPair.hebbNum) \
                              + '\t' + str(trialPair.editDist) + '\t' + str(
                    seqLength - trialPair.editDist) + '\t' + str(
                    trialPair.absMatch))

        #Create means and regressions for every map in seqMap
        for run in sorted(seqMap.keys()):
            #Generate means and regression lines based on the Edit Distance Score
            outfile.write('\n\n\nEDIT DISTANCE SCORE RUN: ' + str(run) + '\n')

            outfile.write('\nMEANS\n')
            outfile.write('\t' + '\t'.join(map(str, sorted(seqMap[run].keys()))) + '\tConditionMeans\n')

            fillerMeans = []
            hebbMeans = []

            for hNum in sorted(seqMap[run].keys()):
                l1 = []
                l2 = []
                for trialPair in seqMap[run][hNum]:
                    if trialPair.pType == 'f':
                        l1.append((seqLength - trialPair.editDist) / float(seqLength))
                    elif fnmatch.fnmatch(trialPair.pType, hebbEx):
                        l2.append((seqLength - trialPair.editDist) / float(seqLength))
                fillerMeans.append(np.mean(l1))
                hebbMeans.append(np.mean(l2))

            regXFillers = range(1, len(seqMap[run].keys()) + 1)
            regXHebbs = range(1, len(seqMap[run].keys()) + 1)

            regYFillers = fillerMeans
            regYHebbs = hebbMeans

            fillerRegression = stats.linregress(regXFillers, regYFillers)
            hebbRegression = stats.linregress(regXHebbs, regYHebbs)

            outfile.write('FILLER\t' + '\t'.join(map(str, fillerMeans)) + '\t' + str(np.mean(fillerMeans)))
            outfile.write('\nHEBB\t' + '\t'.join(map(str, hebbMeans)) + '\t' + str(np.mean(hebbMeans)))

            outfile.write('\n\nREGRESSION\n')
            outfile.write('\tslope\tintercept\trValue\tpValue\tstdError\trSquared')
            outfile.write('\nFILLER\t' + '\t'.join(map(str, fillerRegression)) + '\t' + str(fillerRegression[2] ** 2))
            outfile.write('\nHEBB\t' + '\t'.join(map(str, hebbRegression)) + '\t' + str(hebbRegression[2] ** 2))

            #Generate means and regression lines based on the Absolute Match Score (Slot Distance Score)
            outfile.write('\n\n\nSLOT DISTANCE SCORE RUN: ' + str(run) + '\n')

            outfile.write('\nMEANS\n')
            outfile.write('\t' + '\t'.join(map(str, sorted(seqMap[run].keys()))) + '\tConditionMeans\n')

            fillerMeans = []
            hebbMeans = []

            for hNum in sorted(seqMap[run].keys()):
                l1 = []
                l2 = []
                for trialPair in seqMap[run][hNum]:
                    if trialPair.pType == 'f':
                        l1.append((trialPair.absMatch) / float(seqLength))
                    elif fnmatch.fnmatch(trialPair.pType, hebbEx):
                        l2.append((trialPair.absMatch) / float(seqLength))
                fillerMeans.append(np.mean(l1))
                hebbMeans.append(np.mean(l2))

            regXFillers = range(1, len(seqMap[run].keys()) + 1)
            regXHebbs = range(1, len(seqMap[run].keys()) + 1)

            regYFillers = fillerMeans
            regYHebbs = hebbMeans

            fillerRegression = stats.linregress(regXFillers, regYFillers)
            hebbRegression = stats.linregress(regXHebbs, regYHebbs)

            outfile.write('FILLER\t' + '\t'.join(map(str, fillerMeans)) + '\t' + str(np.mean(fillerMeans)))
            outfile.write('\nHEBB\t' + '\t'.join(map(str, hebbMeans)) + '\t' + str(np.mean(hebbMeans)))

            outfile.write('\n\nREGRESSION\n')
            outfile.write('\tslope\tintercept\trValue\tpValue\tstdError\trSquared')
            outfile.write('\nFILLER\t' + '\t'.join(map(str, fillerRegression)) + '\t' + str(fillerRegression[2] ** 2))
            outfile.write('\nHEBB\t' + '\t'.join(map(str, hebbRegression)) + '\t' + str(hebbRegression[2] ** 2))
