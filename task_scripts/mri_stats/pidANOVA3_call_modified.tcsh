#!/bin/tcsh

# apply any data directories with variables
set data1 = /data3/a202/group_analysis

# note: factor A is time, B is modality, C is subject
# generated script if anova was type 5, manually changed to type 4 to account for within subjs time variable
# being split between files instead of between sub bricks

3dANOVA3 -type 4                                                                                                      \
    -alevels 2                                                                                                        \
    -blevels 2                                                                                                        \
    -clevels 30                                                                                                       \
    -dset  1  1  1                                                                                                    \
    "$data1/W1_all_subjects_pid/1003_t1/1003_t1.pid/stats.1003_t1_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  2  1                                                                                                    \
    "$data1/W1_all_subjects_pid/1003_t1/1003_t1.pid/stats.1003_t1_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  1  2                                                                                                    \
    "$data1/W1_all_subjects_pid/1004_t1/1004_t1.pid/stats.1004_t1_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  2  2                                                                                                    \
    "$data1/W1_all_subjects_pid/1004_t1/1004_t1.pid/stats.1004_t1_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  1  3                                                                                                    \
    "$data1/W1_all_subjects_pid/1005_t1/1005_t1.pid/stats.1005_t1_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  2  3                                                                                                    \
    "$data1/W1_all_subjects_pid/1005_t1/1005_t1.pid/stats.1005_t1_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  1  4                                                                                                    \
    "$data1/W1_all_subjects_pid/1006_t1/1006_t1.pid/stats.1006_t1_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  2  4                                                                                                    \
    "$data1/W1_all_subjects_pid/1006_t1/1006_t1.pid/stats.1006_t1_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  1  5                                                                                                    \
    "$data1/W1_all_subjects_pid/1007_t1/1007_t1.pid/stats.1007_t1_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  2  5                                                                                                    \
    "$data1/W1_all_subjects_pid/1007_t1/1007_t1.pid/stats.1007_t1_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  1  6                                                                                                    \
    "$data1/W1_all_subjects_pid/1009_t1/1009_t1.pid/stats.1009_t1_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  2  6                                                                                                    \
    "$data1/W1_all_subjects_pid/1009_t1/1009_t1.pid/stats.1009_t1_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  1  7                                                                                                    \
    "$data1/W1_all_subjects_pid/1016_t1/1016_t1.pid/stats.1016_t1_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  2  7                                                                                                    \
    "$data1/W1_all_subjects_pid/1016_t1/1016_t1.pid/stats.1016_t1_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  1  8                                                                                                    \
    "$data1/W1_all_subjects_pid/1018_t1/1018_t1.pid/stats.1018_t1_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  2  8                                                                                                    \
    "$data1/W1_all_subjects_pid/1018_t1/1018_t1.pid/stats.1018_t1_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  1  9                                                                                                    \
    "$data1/W1_all_subjects_pid/1019_t1/1019_t1.pid/stats.1019_t1_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  2  9                                                                                                    \
    "$data1/W1_all_subjects_pid/1019_t1/1019_t1.pid/stats.1019_t1_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  1 10                                                                                                    \
    "$data1/W1_all_subjects_pid/1021_t1/1021_t1.pid/stats.1021_t1_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  2 10                                                                                                    \
    "$data1/W1_all_subjects_pid/1021_t1/1021_t1.pid/stats.1021_t1_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  1 11                                                                                                    \
    "$data1/W1_all_subjects_pid/1022_t1/1022_t1.pid/stats.1022_t1_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  2 11                                                                                                    \
    "$data1/W1_all_subjects_pid/1022_t1/1022_t1.pid/stats.1022_t1_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  1 12                                                                                                    \
    "$data1/W1_all_subjects_pid/1023_t1run2/1023_t1run2.pid/stats.1023_t1run2_REML+tlrc.HEAD[vis_word_mis#0_Coef]"    \
                                                                                                                      \
    -dset  1  2 12                                                                                                    \
    "$data1/W1_all_subjects_pid/1023_t1run2/1023_t1run2.pid/stats.1023_t1run2_REML+tlrc.HEAD[aud_word_mis#0_Coef]"    \
                                                                                                                      \
    -dset  1  1 13                                                                                                    \
    "$data1/W1_all_subjects_pid/1024_t1run2/1024_t1run2.pid/stats.1024_t1run2_REML+tlrc.HEAD[vis_word_mis#0_Coef]"    \
                                                                                                                      \
    -dset  1  2 13                                                                                                    \
    "$data1/W1_all_subjects_pid/1024_t1run2/1024_t1run2.pid/stats.1024_t1run2_REML+tlrc.HEAD[aud_word_mis#0_Coef]"    \
                                                                                                                      \
    -dset  1  1 14                                                                                                    \
    "$data1/W1_all_subjects_pid/1031_t1/1031_t1.pid/stats.1031_t1_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  2 14                                                                                                    \
    "$data1/W1_all_subjects_pid/1031_t1/1031_t1.pid/stats.1031_t1_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  1 15                                                                                                    \
    "$data1/W2_all_subjects_pid/2006_t1_run2/2006_t1_run2.pid/stats.2006_t1_run2_REML+tlrc.HEAD[vis_word_mis#0_Coef]" \
                                                                                                                      \
    -dset  1  2 15                                                                                                    \
    "$data1/W2_all_subjects_pid/2006_t1_run2/2006_t1_run2.pid/stats.2006_t1_run2_REML+tlrc.HEAD[aud_word_mis#0_Coef]" \
                                                                                                                      \
    -dset  1  1 16                                                                                                    \
    "$data1/W2_all_subjects_pid/2011_t1/2011_t1.pid/stats.2011_t1_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  2 16                                                                                                    \
    "$data1/W2_all_subjects_pid/2011_t1/2011_t1.pid/stats.2011_t1_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  1 17                                                                                                    \
    "$data1/W2_all_subjects_pid/2029_t1/2029_t1.pid/stats.2029_t1_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  2 17                                                                                                    \
    "$data1/W2_all_subjects_pid/2029_t1/2029_t1.pid/stats.2029_t1_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  1 18                                                                                                    \
    "$data1/W2_all_subjects_pid/2035_t1/2035_t1.pid/stats.2035_t1_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  2 18                                                                                                    \
    "$data1/W2_all_subjects_pid/2035_t1/2035_t1.pid/stats.2035_t1_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  1 19                                                                                                    \
    "$data1/W2_all_subjects_pid/2036_t1/2036_t1.pid/stats.2036_t1_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  2 19                                                                                                    \
    "$data1/W2_all_subjects_pid/2036_t1/2036_t1.pid/stats.2036_t1_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  1 20                                                                                                    \
    "$data1/W2_all_subjects_pid/2037_t1/2037_t1.pid/stats.2037_t1_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  2 20                                                                                                    \
    "$data1/W2_all_subjects_pid/2037_t1/2037_t1.pid/stats.2037_t1_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  1 21                                                                                                    \
    "$data1/W2_all_subjects_pid/2038_t1/2038_t1.pid/stats.2038_t1_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  2 21                                                                                                    \
    "$data1/W2_all_subjects_pid/2038_t1/2038_t1.pid/stats.2038_t1_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  1 22                                                                                                    \
    "$data1/W2_all_subjects_pid/2046_t1/2046_t1.pid/stats.2046_t1_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  2 22                                                                                                    \
    "$data1/W2_all_subjects_pid/2046_t1/2046_t1.pid/stats.2046_t1_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  1 23                                                                                                    \
    "$data1/W2_all_subjects_pid/2048_t1/2048_t1.pid/stats.2048_t1_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  2 23                                                                                                    \
    "$data1/W2_all_subjects_pid/2048_t1/2048_t1.pid/stats.2048_t1_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  1 24                                                                                                    \
    "$data1/W2_all_subjects_pid/2052_t1/2052_t1.pid/stats.2052_t1_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  2 24                                                                                                    \
    "$data1/W2_all_subjects_pid/2052_t1/2052_t1.pid/stats.2052_t1_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  1 25                                                                                                    \
    "$data1/W2_all_subjects_pid/2054_t1/2054_t1.pid/stats.2054_t1_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  2 25                                                                                                    \
    "$data1/W2_all_subjects_pid/2054_t1/2054_t1.pid/stats.2054_t1_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  1 26                                                                                                    \
    "$data1/W2_all_subjects_pid/2058_t1/2058_t1.pid/stats.2058_t1_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  2 26                                                                                                    \
    "$data1/W2_all_subjects_pid/2058_t1/2058_t1.pid/stats.2058_t1_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  1 27                                                                                                    \
    "$data1/W2_all_subjects_pid/2060_t1/2060_t1.pid/stats.2060_t1_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  2 27                                                                                                    \
    "$data1/W2_all_subjects_pid/2060_t1/2060_t1.pid/stats.2060_t1_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  1 28                                                                                                    \
    "$data1/W2_all_subjects_pid/2061_t1/2061_t1.pid/stats.2061_t1_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  2 28                                                                                                    \
    "$data1/W2_all_subjects_pid/2061_t1/2061_t1.pid/stats.2061_t1_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  1 29                                                                                                    \
    "$data1/W2_all_subjects_pid/2067_t1/2067_t1.pid/stats.2067_t1_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  2 29                                                                                                    \
    "$data1/W2_all_subjects_pid/2067_t1/2067_t1.pid/stats.2067_t1_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  1 30                                                                                                    \
    "$data1/W2_all_subjects_pid/2070_t1/2070_t1.pid/stats.2070_t1_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  1  2 30                                                                                                    \
    "$data1/W2_all_subjects_pid/2070_t1/2070_t1.pid/stats.2070_t1_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  1  1                                                                                                    \
    "$data1/W1_all_subjects_pid/1003_t2/1003_t2.pid/stats.1003_t2_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  2  1                                                                                                    \
    "$data1/W1_all_subjects_pid/1003_t2/1003_t2.pid/stats.1003_t2_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  1  2                                                                                                    \
    "$data1/W1_all_subjects_pid/1004_t2/1004_t2.pid/stats.1004_t2_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  2  2                                                                                                    \
    "$data1/W1_all_subjects_pid/1004_t2/1004_t2.pid/stats.1004_t2_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  1  3                                                                                                    \
    "$data1/W1_all_subjects_pid/1005_t2/1005_t2.pid/stats.1005_t2_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  2  3                                                                                                    \
    "$data1/W1_all_subjects_pid/1005_t2/1005_t2.pid/stats.1005_t2_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  1  4                                                                                                    \
    "$data1/W1_all_subjects_pid/1006_t2/1006_t2.pid/stats.1006_t2_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  2  4                                                                                                    \
    "$data1/W1_all_subjects_pid/1006_t2/1006_t2.pid/stats.1006_t2_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  1  5                                                                                                    \
    "$data1/W1_all_subjects_pid/1007_t2/1007_t2.pid/stats.1007_t2_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  2  5                                                                                                    \
    "$data1/W1_all_subjects_pid/1007_t2/1007_t2.pid/stats.1007_t2_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  1  6                                                                                                    \
    "$data1/W1_all_subjects_pid/1009_t2/1009_t2.pid/stats.1009_t2_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  2  6                                                                                                    \
    "$data1/W1_all_subjects_pid/1009_t2/1009_t2.pid/stats.1009_t2_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  1  7                                                                                                    \
    "$data1/W1_all_subjects_pid/1016_t2/1016_t2.pid/stats.1016_t2_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  2  7                                                                                                    \
    "$data1/W1_all_subjects_pid/1016_t2/1016_t2.pid/stats.1016_t2_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  1  8                                                                                                    \
    "$data1/W1_all_subjects_pid/1018_t2/1018_t2.pid/stats.1018_t2_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  2  8                                                                                                    \
    "$data1/W1_all_subjects_pid/1018_t2/1018_t2.pid/stats.1018_t2_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  1  9                                                                                                    \
    "$data1/W1_all_subjects_pid/1019_t2/1019_t2.pid/stats.1019_t2_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  2  9                                                                                                    \
    "$data1/W1_all_subjects_pid/1019_t2/1019_t2.pid/stats.1019_t2_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  1 10                                                                                                    \
    "$data1/W1_all_subjects_pid/1021_t2/1021_t2.pid/stats.1021_t2_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  2 10                                                                                                    \
    "$data1/W1_all_subjects_pid/1021_t2/1021_t2.pid/stats.1021_t2_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  1 11                                                                                                    \
    "$data1/W1_all_subjects_pid/1022_t2/1022_t2.pid/stats.1022_t2_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  2 11                                                                                                    \
    "$data1/W1_all_subjects_pid/1022_t2/1022_t2.pid/stats.1022_t2_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  1 12                                                                                                    \
    "$data1/W1_all_subjects_pid/1023_t2/1023_t2.pid/stats.1023_t2_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  2 12                                                                                                    \
    "$data1/W1_all_subjects_pid/1023_t2/1023_t2.pid/stats.1023_t2_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  1 13                                                                                                    \
    "$data1/W1_all_subjects_pid/1024_t2/1024_t2.pid/stats.1024_t2_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  2 13                                                                                                    \
    "$data1/W1_all_subjects_pid/1024_t2/1024_t2.pid/stats.1024_t2_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  1 14                                                                                                    \
    "$data1/W1_all_subjects_pid/1031_t2/1031_t2.pid/stats.1031_t2_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  2 14                                                                                                    \
    "$data1/W1_all_subjects_pid/1031_t2/1031_t2.pid/stats.1031_t2_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  1 15                                                                                                    \
    "$data1/W2_all_subjects_pid/2006_t2/2006_t2.pid/stats.2006_t2_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  2 15                                                                                                    \
    "$data1/W2_all_subjects_pid/2006_t2/2006_t2.pid/stats.2006_t2_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  1 16                                                                                                    \
    "$data1/W2_all_subjects_pid/2011_t2_run2/2011_t2_run2.pid/stats.2011_t2_run2_REML+tlrc.HEAD[vis_word_mis#0_Coef]" \
                                                                                                                      \
    -dset  2  2 16                                                                                                    \
    "$data1/W2_all_subjects_pid/2011_t2_run2/2011_t2_run2.pid/stats.2011_t2_run2_REML+tlrc.HEAD[aud_word_mis#0_Coef]" \
                                                                                                                      \
    -dset  2  1 17                                                                                                    \
    "$data1/W2_all_subjects_pid/2029_t2/2029_t2.pid/stats.2029_t2_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  2 17                                                                                                    \
    "$data1/W2_all_subjects_pid/2029_t2/2029_t2.pid/stats.2029_t2_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  1 18                                                                                                    \
    "$data1/W2_all_subjects_pid/2035_t2/2035_t2.pid/stats.2035_t2_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  2 18                                                                                                    \
    "$data1/W2_all_subjects_pid/2035_t2/2035_t2.pid/stats.2035_t2_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  1 19                                                                                                    \
    "$data1/W2_all_subjects_pid/2036_t2/2036_t2.pid/stats.2036_t2_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  2 19                                                                                                    \
    "$data1/W2_all_subjects_pid/2036_t2/2036_t2.pid/stats.2036_t2_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  1 20                                                                                                    \
    "$data1/W2_all_subjects_pid/2037_t2/2037_t2.pid/stats.2037_t2_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  2 20                                                                                                    \
    "$data1/W2_all_subjects_pid/2037_t2/2037_t2.pid/stats.2037_t2_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  1 21                                                                                                    \
    "$data1/W2_all_subjects_pid/2038_t2/2038_t2.pid/stats.2038_t2_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  2 21                                                                                                    \
    "$data1/W2_all_subjects_pid/2038_t2/2038_t2.pid/stats.2038_t2_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  1 22                                                                                                    \
    "$data1/W2_all_subjects_pid/2046_t2/2046_t2.pid/stats.2046_t2_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  2 22                                                                                                    \
    "$data1/W2_all_subjects_pid/2046_t2/2046_t2.pid/stats.2046_t2_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  1 23                                                                                                    \
    "$data1/W2_all_subjects_pid/2048_t2/2048_t2.pid/stats.2048_t2_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  2 23                                                                                                    \
    "$data1/W2_all_subjects_pid/2048_t2/2048_t2.pid/stats.2048_t2_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  1 24                                                                                                    \
    "$data1/W2_all_subjects_pid/2052_t2/2052_t2.pid/stats.2052_t2_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  2 24                                                                                                    \
    "$data1/W2_all_subjects_pid/2052_t2/2052_t2.pid/stats.2052_t2_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  1 25                                                                                                    \
    "$data1/W2_all_subjects_pid/2054_t2/2054_t2.pid/stats.2054_t2_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  2 25                                                                                                    \
    "$data1/W2_all_subjects_pid/2054_t2/2054_t2.pid/stats.2054_t2_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  1 26                                                                                                    \
    "$data1/W2_all_subjects_pid/2058_t2/2058_t2.pid/stats.2058_t2_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  2 26                                                                                                    \
    "$data1/W2_all_subjects_pid/2058_t2/2058_t2.pid/stats.2058_t2_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  1 27                                                                                                    \
    "$data1/W2_all_subjects_pid/2060_t2/2060_t2.pid/stats.2060_t2_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  2 27                                                                                                    \
    "$data1/W2_all_subjects_pid/2060_t2/2060_t2.pid/stats.2060_t2_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  1 28                                                                                                    \
    "$data1/W2_all_subjects_pid/2061_t2/2061_t2.pid/stats.2061_t2_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  2 28                                                                                                    \
    "$data1/W2_all_subjects_pid/2061_t2/2061_t2.pid/stats.2061_t2_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  1 29                                                                                                    \
    "$data1/W2_all_subjects_pid/2067_t2/2067_t2.pid/stats.2067_t2_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  2 29                                                                                                    \
    "$data1/W2_all_subjects_pid/2067_t2/2067_t2.pid/stats.2067_t2_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  1 30                                                                                                    \
    "$data1/W2_all_subjects_pid/2070_t2/2070_t2.pid/stats.2070_t2_REML+tlrc.HEAD[vis_word_mis#0_Coef]"                \
                                                                                                                      \
    -dset  2  2 30                                                                                                    \
    "$data1/W2_all_subjects_pid/2070_t2/2070_t2.pid/stats.2070_t2_REML+tlrc.HEAD[aud_word_mis#0_Coef]"                \
    -amean 1 T1 \
    -amean 2 T2 \
    -bmean 1 vis \
    -bmean 2 aud \
    -abmean 1 1 T1_vis \
    -abmean 1 2 T1_aud \
    -abmean 2 1 T2_vis \
    -abmean 2 2 T2_aud \
    -acontr -1 1 T2-T1 \
    -bcontr -1 1 aud-vis \
    -aBdiff 1 2 : 1 T2-T1_vis \
    -aBdiff 1 2 : 2 T2-T1_aud \
    -Abdiff 1 : 1 2 T1_aud-vis \
    -Abdiff 2 : 1 2 T2_aud-vis \
    -bucket ./pidANOVA3.results
