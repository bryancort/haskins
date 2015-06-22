#!/usr/bin/python

# BC: Added pull directory processing and now ignores case

import tkFileDialog
import fnmatch
from scipy import stats
import numpy as np
import os
import sys
import glob
import traceback
import mixins
from utils import file_utils

# Trying to fix import issues in the compiled version
# #from scipy.special import _ufuncs

sep = '\t'


class HebbSequencePair(mixins.ListableMixin):
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

    def __init__(self, heard_seq, produced_seq, pair_id, pair_num, hebb_num, run_num, subject_id=None):
        self.heard_seq = heard_seq[:]
        self.produced_seq = produced_seq[:]

        self.pair_id = pair_id
        self.pair_type = 'filler' if self.pair_id == 'f' else 'hebb'
        self.run_num = run_num

        self.hebb_num = hebb_num
        self.subject_id = subject_id
        self.pair_num = pair_num

        self.pair_regression_id = "r{}_h{}_{}".format(self.run_num, self.hebb_num, self.pair_type)

        heard_seq_length = len(self.heard_seq)
        self.edit_dist = LD(self.heard_seq, self.produced_seq)
        self.edit_dist_score = heard_seq_length - int(self.edit_dist)
        self.slot_dist_score = 0
        for h, p in zip(self.heard_seq, self.produced_seq):
            if h.lower() == p.lower():
                self.slot_dist_score += 1

        self.edit_dist_score_acc = float(self.edit_dist_score) / float(heard_seq_length)
        self.slot_dist_score_acc = float(self.slot_dist_score) / float(heard_seq_length)
        float(heard_seq_length)

    def __str__(self):
        return str(vars(self))

    def __repr__(self):
        return str(vars(self))


# todo: dev/test non-int groups
def regress_runs(data, include_vars_dict, grouping_var, response_var):
    """
    Generates the regression line and accompanying stats for a dataset.
    :param data: list of objects to use in the regression.
    :param include_vars_dict: map of {var: value} to include. Will include only data points with value of var.
    :param grouping_var: group points and average their data based on this var. Data points will be ordered based on
        sort(grouping_var values). Currently must be an int. Final regression is plotted using the group as the x-var
        and the mean of the values in that group as the y-var, for each point in points that meets the criteria
        (specified by include_vars_dict)
    :param response_var: y-axis response variable; must be numeric.
    """
    regress_data_dict = {}
    for d in data:
        for var, val in include_vars_dict.iteritems():
            if not hasattr(d, var) or not getattr(d, var) == val:
                break
        else:
            group, datum = getattr(d, grouping_var), getattr(d, response_var)
            if group in regress_data_dict:
                regress_data_dict[group].append(datum)
            else:
                regress_data_dict[group] = [datum]
                # regress_data_dict[getattr(d, grouping_var)] = getattr(d, response_var)
    # means = {group: np.mean(regress_data[group]) for group, values in sorted(regress_data.iteritems())}
    means_dict = {}
    count = 0
    for group in sorted(regress_data_dict):
        count += 1
        means_dict[count] = np.mean(regress_data_dict[group])
    regression = stats.linregress([float(g) for g in sorted(means_dict)], [means_dict[g] for g in sorted(means_dict)])
    return means_dict, regression


def parse_regression(regression, sep=None):
    regression_str = sep.join([str(r) for r in regression]) + sep + str(regression[2] ** 2)
    return regression_str


def _format_regressions(filler_means, hebb_means, filler_regr, hebb_regr, sep="\t", linesep='\n'):
    regressions_output = ""
    regressions_output += "MEANS"
    len_diff = len(filler_means) - len(hebb_means)
    str_means_filler = [str(mean) for mean in filler_means] + [''] + (-1*len_diff)*[''] + [str(np.mean(filler_means))]
    str_means_hebb = [str(mean) for mean in hebb_means] + [''] + len_diff*[''] + [str(np.mean(hebb_means))]
    assert len(str_means_filler) == len(str_means_hebb)
    mean_nums = range(1, len(str_means_filler) - 1)
    mean_nums = [str(_num) for _num in mean_nums] + [''] + ['ConditionMeans']
    regressions_output += "{}{}".format(sep, sep.join(mean_nums))
    regressions_output += "{}FILLER{}{}".format(linesep, sep, sep.join(str_means_filler))
    regressions_output += "{}HEBB{}{}".format(linesep, sep, sep.join(str_means_hebb))
    regressions_output += "\n\nREGRESSION\n"
    regressions_output += "\t".join(["", "slope", "intercept", "rValue", "pValue", "stdError", "rSquared"])
    regressions_output += "{}FILLER{}{}".format(linesep, sep, parse_regression(filler_regr, sep=sep))
    regressions_output += "{}HEBB{}{}".format(linesep, sep, parse_regression(hebb_regr, sep=sep))
    return regressions_output


def LD(seq1, seq2):
    """
    Compares two sequences and returns the Levenshtein Distance (http://en.wikipedia.org/wiki/Levenshtein_distance)
    between them. Adapted from example code from that site. #// denotes comments from that example code; # denotes
    comments specific to this implementation.
    """

    # // for all i and j, d[i,j] will hold the Levenshtein distance between
    # // the first i characters of s and the first j characters of t

    seq1 = [i.lower() for i in seq1]
    seq2 = [i.lower() for i in seq2]

    # Rows: seq1, s1, i, m
    # Columns: seq2, s2, j, n

    # initialize the (len(seq1) + 1) by (len(seq2) + 1) array used for computing edit distance
    s1 = list(seq1[:])
    s2 = list(seq2[:])
    s1.insert(0, "")
    s2.insert(0, "")

    m = len(s1)
    n = len(s2)

    # generate the array with all 0's
    d = [[0 for item in s2] for item in s1]

    # // source prefixes can be transformed into empty string by
    # // dropping all characters
    # // target prefixes can be reached from empty source prefix
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


def tokenize2(fname):
    leading_path, _file_name = os.path.split(fname)
    file_name, file_ext = os.path.splitext(_file_name)
    tokens = file_name.replace('-', '_').split('_')
    return leading_path, file_name, file_ext, tokens


def trim_seq(seq):
    _seq = seq[:]
    try:
        while not _seq[-1]:
            _seq.pop()
        while not _seq[0]:
            _seq.pop(0)
        return _seq
    except IndexError:  # we ran out of entries (the whole list was blank)
        return ['']


def find_hebb_num(responses_table, response_index, pair_type_col=0, hebb_ex='H*', strip_chars='H', partial_hebb='7'):
    i = response_index
    while i < len(responses_table):
        if fnmatch.fnmatch(responses_table[i][pair_type_col], hebb_ex):
            hebb_num = responses_table[i][pair_type_col].strip(strip_chars)
            return hebb_num
        elif not ''.join(responses_table[i]):
            return partial_hebb
        i += 1
    return partial_hebb


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
            traceback.print_exc()
            print "Skipping file {}".format(f)
            raise


def proc_hebb(subj_id=None, out_dir=None, hebb_file_path=None, hebb_ex='H*', filler_ex='f',
              pair_type_ind=0, run_num_ind=1, run_trial_num_ind=2, seq_start_ind=4,
              output_attrs=('subject_id', 'run_num', 'pair_id', 'hebb_num', 'edit_dist', 'edit_dist_score',
                            'slot_dist_score')):
    if not subj_id:
        subj_id = raw_input("Enter the subject ID: ")
    if not out_dir:
        out_dir = tkFileDialog.askdirectory(title='Select the output directory: ')
    # Read in subject response, expected response file
    if not hebb_file_path:
        hebb_file_path = tkFileDialog.askopenfilename(title="Select the input file:")

    responses_table = file_utils.readTable2(fPath=hebb_file_path)
    response_pairs = []
    pair_count = 0
    for ind, line in enumerate(responses_table):
        if fnmatch.fnmatch(line[pair_type_ind], hebb_ex) or fnmatch.fnmatch(line[pair_type_ind], filler_ex):
            pair_count += 1
            heard_seq = trim_seq(line[seq_start_ind:])
            produced_seq = trim_seq(responses_table[ind + 1][seq_start_ind:])
            hebb_num = find_hebb_num(responses_table=responses_table, response_index=ind, pair_type_col=pair_type_ind,
                                     hebb_ex=hebb_ex)
            response_pairs.append(HebbSequencePair(heard_seq=heard_seq, produced_seq=produced_seq,
                                                   pair_id=line[pair_type_ind], pair_num=pair_count, hebb_num=hebb_num,
                                                   run_num=line[run_num_ind], subject_id=subj_id))
        else:
            continue
    _output_table = [response_pairs[0].gen_header_list(output_attrs)]
    for hebb_pair in response_pairs:
        _output_table.append(hebb_pair.gen_attr_list(output_attrs))

    _output_str = '\n'.join(['\t'.join(line) for line in _output_table])

    regressions_output = ''

    runs = []
    for pair in response_pairs:
        if pair.run_num not in runs:
            runs.append(str(pair.run_num))

    # do the filler regressions and the hebb regressions
    filler_edit_dist_regressions_dict = {
        'all': regress_runs(data=response_pairs, include_vars_dict={'pair_type': 'filler'},
                            grouping_var='pair_regression_id',
                            response_var='edit_dist_score_acc')}
    hebb_edit_dist_regressions_dict = {'all': regress_runs(data=response_pairs, include_vars_dict={'pair_type': 'hebb'},
                                                           grouping_var='pair_regression_id',
                                                           response_var='edit_dist_score_acc')}
    filler_slot_dist_regressions_dict = {
        'all': regress_runs(data=response_pairs, include_vars_dict={'pair_type': 'filler'},
                            grouping_var='pair_regression_id',
                            response_var='slot_dist_score_acc')}
    hebb_slot_dist_regressions_dict = {'all': regress_runs(data=response_pairs, include_vars_dict={'pair_type': 'hebb'},
                                                           grouping_var='pair_regression_id',
                                                           response_var='slot_dist_score_acc')}
    for run in runs:
        filler_edit_dist_regressions_dict[run] = regress_runs(data=response_pairs,
                                                              include_vars_dict={'pair_type': 'filler', 'run_num': run},
                                                              grouping_var='pair_regression_id',
                                                              response_var='edit_dist_score_acc')
        hebb_edit_dist_regressions_dict[run] = regress_runs(data=response_pairs,
                                                            include_vars_dict={'pair_type': 'hebb', 'run_num': run},
                                                            grouping_var='pair_regression_id',
                                                            response_var='edit_dist_score_acc')
        regressions_output += '\n\nEDIT DISTANCE SCORE RUN: {}\n\n'.format(run)
        means_filler = [filler_edit_dist_regressions_dict[run][0][k] for k in filler_edit_dist_regressions_dict[run][0]]
        means_hebb = [hebb_edit_dist_regressions_dict[run][0][k] for k in hebb_edit_dist_regressions_dict[run][0]]

        regressions_output += _format_regressions(means_filler, means_hebb,
                                                  filler_edit_dist_regressions_dict[run][1],
                                                  hebb_edit_dist_regressions_dict[run][1])

        filler_slot_dist_regressions_dict[run] = regress_runs(data=response_pairs,
                                                              include_vars_dict={'pair_type': 'filler', 'run_num': run},
                                                              grouping_var='hebb_num',
                                                              response_var='slot_dist_score_acc')
        hebb_slot_dist_regressions_dict[run] = regress_runs(data=response_pairs,
                                                            include_vars_dict={'pair_type': 'hebb', 'run_num': run},
                                                            grouping_var='hebb_num', response_var='slot_dist_score_acc')

        regressions_output += '\n\nSLOT DISTANCE SCORE RUN: {}\n\n'.format(run)
        means_filler = [filler_slot_dist_regressions_dict[run][0][k] for k in filler_slot_dist_regressions_dict[run][0]]
        means_hebb = [hebb_slot_dist_regressions_dict[run][0][k] for k in hebb_slot_dist_regressions_dict[run][0]]

        regressions_output += _format_regressions(means_filler, means_hebb,
                                                  filler_slot_dist_regressions_dict[run][1],
                                                  hebb_slot_dist_regressions_dict[run][1])

    run = 'all'
    regressions_output += '\n\nEDIT DISTANCE SCORE RUN: {}\n\n'.format(run)
    means_filler = [filler_edit_dist_regressions_dict[run][0][k] for k in filler_edit_dist_regressions_dict[run][0]]
    means_hebb = [hebb_edit_dist_regressions_dict[run][0][k] for k in hebb_edit_dist_regressions_dict[run][0]]

    regressions_output += _format_regressions(means_filler, means_hebb,
                                              filler_edit_dist_regressions_dict[run][1],
                                              hebb_edit_dist_regressions_dict[run][1])

    regressions_output += '\n\nSLOT DISTANCE SCORE RUN: {}\n\n'.format(run)
    means_filler = [filler_slot_dist_regressions_dict[run][0][k] for k in filler_slot_dist_regressions_dict[run][0]]
    means_hebb = [hebb_slot_dist_regressions_dict[run][0][k] for k in hebb_slot_dist_regressions_dict[run][0]]

    regressions_output += _format_regressions(means_filler, means_hebb,
                                              filler_slot_dist_regressions_dict[run][1],
                                              hebb_slot_dist_regressions_dict[run][1])


    _output_str += regressions_output
    with open(os.path.join(out_dir, 'out_' + str(subj_id) + '.txt'), 'w') as outfile:
        outfile.write(_output_str)


def __main__():
    if len(sys.argv) == 2:
        hebb_dir = os.path.normpath(sys.argv[1])
        proc_dir(hebb_dir)
    else:
        # proc_dir(os.path.normpath("""C:\Users\cort\Desktop\hebb_test"""))
        proc_hebb()


if __name__ == '__main__':
    __main__()