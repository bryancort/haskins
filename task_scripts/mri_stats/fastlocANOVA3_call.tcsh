#!/bin/tcsh

# apply any data directories with variables
set data1 = /data3/a202/group_analysis

# note: factor A is group, B is condition, C is subject

3dANOVA3 -type 5                                                                                                                \
    -alevels 2                                                                                                                  \
    -blevels 4                                                                                                                  \
    -clevels 27                                                                                                                 \
    -dset  1  1  1                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1003_t1/1003_t1.fastloc/stats.1003_t1_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  1  2  1                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1003_t1/1003_t1.fastloc/stats.1003_t1_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  1  3  1                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1003_t1/1003_t1.fastloc/stats.1003_t1_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  1  4  1                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1003_t1/1003_t1.fastloc/stats.1003_t1_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  1  1  2                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1004_t1/1004_t1.fastloc/stats.1004_t1_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  1  2  2                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1004_t1/1004_t1.fastloc/stats.1004_t1_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  1  3  2                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1004_t1/1004_t1.fastloc/stats.1004_t1_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  1  4  2                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1004_t1/1004_t1.fastloc/stats.1004_t1_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  1  1  3                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1005_t1/1005_t1.fastloc/stats.1005_t1_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  1  2  3                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1005_t1/1005_t1.fastloc/stats.1005_t1_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  1  3  3                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1005_t1/1005_t1.fastloc/stats.1005_t1_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  1  4  3                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1005_t1/1005_t1.fastloc/stats.1005_t1_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  1  1  4                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1006_t1/1006_t1.fastloc/stats.1006_t1_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  1  2  4                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1006_t1/1006_t1.fastloc/stats.1006_t1_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  1  3  4                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1006_t1/1006_t1.fastloc/stats.1006_t1_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  1  4  4                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1006_t1/1006_t1.fastloc/stats.1006_t1_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  1  1  5                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1007_t1/1007_t1.fastloc/stats.1007_t1_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  1  2  5                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1007_t1/1007_t1.fastloc/stats.1007_t1_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  1  3  5                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1007_t1/1007_t1.fastloc/stats.1007_t1_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  1  4  5                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1007_t1/1007_t1.fastloc/stats.1007_t1_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  1  1  6                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1009_t1/1009_t1.fastloc/stats.1009_t1_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  1  2  6                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1009_t1/1009_t1.fastloc/stats.1009_t1_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  1  3  6                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1009_t1/1009_t1.fastloc/stats.1009_t1_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  1  4  6                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1009_t1/1009_t1.fastloc/stats.1009_t1_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  1  1  7                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1016_t1/1016_t1.fastloc/stats.1016_t1_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  1  2  7                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1016_t1/1016_t1.fastloc/stats.1016_t1_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  1  3  7                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1016_t1/1016_t1.fastloc/stats.1016_t1_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  1  4  7                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1016_t1/1016_t1.fastloc/stats.1016_t1_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  1  1  8                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1018_t1/1018_t1.fastloc/stats.1018_t1_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  1  2  8                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1018_t1/1018_t1.fastloc/stats.1018_t1_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  1  3  8                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1018_t1/1018_t1.fastloc/stats.1018_t1_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  1  4  8                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1018_t1/1018_t1.fastloc/stats.1018_t1_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  1  1  9                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1019_t1/1019_t1.fastloc/stats.1019_t1_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  1  2  9                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1019_t1/1019_t1.fastloc/stats.1019_t1_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  1  3  9                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1019_t1/1019_t1.fastloc/stats.1019_t1_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  1  4  9                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1019_t1/1019_t1.fastloc/stats.1019_t1_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  1  1 10                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1021_t1/1021_t1.fastloc/stats.1021_t1_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  1  2 10                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1021_t1/1021_t1.fastloc/stats.1021_t1_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  1  3 10                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1021_t1/1021_t1.fastloc/stats.1021_t1_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  1  4 10                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1021_t1/1021_t1.fastloc/stats.1021_t1_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  1  1 11                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1022_t1/1022_t1.fastloc/stats.1022_t1_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  1  2 11                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1022_t1/1022_t1.fastloc/stats.1022_t1_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  1  3 11                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1022_t1/1022_t1.fastloc/stats.1022_t1_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  1  4 11                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1022_t1/1022_t1.fastloc/stats.1022_t1_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  1  1 12                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1023_t1/1023_t1.fastloc/stats.1023_t1_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  1  2 12                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1023_t1/1023_t1.fastloc/stats.1023_t1_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  1  3 12                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1023_t1/1023_t1.fastloc/stats.1023_t1_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  1  4 12                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1023_t1/1023_t1.fastloc/stats.1023_t1_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  1  1 13                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1024_t1/1024_t1.fastloc/stats.1024_t1_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  1  2 13                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1024_t1/1024_t1.fastloc/stats.1024_t1_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  1  3 13                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1024_t1/1024_t1.fastloc/stats.1024_t1_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  1  4 13                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1024_t1/1024_t1.fastloc/stats.1024_t1_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  1  1 14                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1031_t1/1031_t1.fastloc/stats.1031_t1_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  1  2 14                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1031_t1/1031_t1.fastloc/stats.1031_t1_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  1  3 14                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1031_t1/1031_t1.fastloc/stats.1031_t1_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  1  4 14                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1031_t1/1031_t1.fastloc/stats.1031_t1_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  1  1 15                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2006_t1_run2/2006_t1_run2.fastloc/stats.2006_t1_run2_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"   \
                                                                                                                                \
    -dset  1  2 15                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2006_t1_run2/2006_t1_run2.fastloc/stats.2006_t1_run2_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]" \
                                                                                                                                \
    -dset  1  3 15                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2006_t1_run2/2006_t1_run2.fastloc/stats.2006_t1_run2_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"  \
                                                                                                                                \
    -dset  1  4 15                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2006_t1_run2/2006_t1_run2.fastloc/stats.2006_t1_run2_REML+tlrc.HEAD[VOCOD_no#0_Coef]"       \
                                                                                                                                \
    -dset  1  1 16                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2011_t1/2011_t1.fastloc/stats.2011_t1_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  1  2 16                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2011_t1/2011_t1.fastloc/stats.2011_t1_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  1  3 16                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2011_t1/2011_t1.fastloc/stats.2011_t1_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  1  4 16                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2011_t1/2011_t1.fastloc/stats.2011_t1_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  1  1 17                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2029_t1/2029_t1.fastloc/stats.2029_t1_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  1  2 17                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2029_t1/2029_t1.fastloc/stats.2029_t1_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  1  3 17                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2029_t1/2029_t1.fastloc/stats.2029_t1_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  1  4 17                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2029_t1/2029_t1.fastloc/stats.2029_t1_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  1  1 18                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2035_t1/2035_t1.fastloc/stats.2035_t1_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  1  2 18                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2035_t1/2035_t1.fastloc/stats.2035_t1_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  1  3 18                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2035_t1/2035_t1.fastloc/stats.2035_t1_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  1  4 18                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2035_t1/2035_t1.fastloc/stats.2035_t1_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  1  1 19                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2036_t1/2036_t1.fastloc/stats.2036_t1_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  1  2 19                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2036_t1/2036_t1.fastloc/stats.2036_t1_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  1  3 19                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2036_t1/2036_t1.fastloc/stats.2036_t1_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  1  4 19                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2036_t1/2036_t1.fastloc/stats.2036_t1_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  1  1 20                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2037_t1/2037_t1.fastloc/stats.2037_t1_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  1  2 20                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2037_t1/2037_t1.fastloc/stats.2037_t1_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  1  3 20                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2037_t1/2037_t1.fastloc/stats.2037_t1_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  1  4 20                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2037_t1/2037_t1.fastloc/stats.2037_t1_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  1  1 21                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2038_t1/2038_t1.fastloc/stats.2038_t1_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  1  2 21                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2038_t1/2038_t1.fastloc/stats.2038_t1_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  1  3 21                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2038_t1/2038_t1.fastloc/stats.2038_t1_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  1  4 21                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2038_t1/2038_t1.fastloc/stats.2038_t1_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  1  1 22                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2040_t1/2040_t1.fastloc/stats.2040_t1_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  1  2 22                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2040_t1/2040_t1.fastloc/stats.2040_t1_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  1  3 22                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2040_t1/2040_t1.fastloc/stats.2040_t1_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  1  4 22                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2040_t1/2040_t1.fastloc/stats.2040_t1_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  1  1 23                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2048_t1/2048_t1.fastloc/stats.2048_t1_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  1  2 23                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2048_t1/2048_t1.fastloc/stats.2048_t1_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  1  3 23                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2048_t1/2048_t1.fastloc/stats.2048_t1_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  1  4 23                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2048_t1/2048_t1.fastloc/stats.2048_t1_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  1  1 24                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2052_t1/2052_t1.fastloc/stats.2052_t1_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  1  2 24                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2052_t1/2052_t1.fastloc/stats.2052_t1_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  1  3 24                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2052_t1/2052_t1.fastloc/stats.2052_t1_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  1  4 24                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2052_t1/2052_t1.fastloc/stats.2052_t1_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  1  1 25                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2054_t1/2054_t1.fastloc/stats.2054_t1_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  1  2 25                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2054_t1/2054_t1.fastloc/stats.2054_t1_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  1  3 25                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2054_t1/2054_t1.fastloc/stats.2054_t1_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  1  4 25                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2054_t1/2054_t1.fastloc/stats.2054_t1_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  1  1 26                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2061_t1/2061_t1.fastloc/stats.2061_t1_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  1  2 26                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2061_t1/2061_t1.fastloc/stats.2061_t1_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  1  3 26                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2061_t1/2061_t1.fastloc/stats.2061_t1_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  1  4 26                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2061_t1/2061_t1.fastloc/stats.2061_t1_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  1  1 27                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2067_t1/2067_t1.fastloc/stats.2067_t1_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  1  2 27                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2067_t1/2067_t1.fastloc/stats.2067_t1_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  1  3 27                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2067_t1/2067_t1.fastloc/stats.2067_t1_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  1  4 27                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2067_t1/2067_t1.fastloc/stats.2067_t1_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  2  1  1                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1003_t2/1003_t2.fastloc/stats.1003_t2_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  2  2  1                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1003_t2/1003_t2.fastloc/stats.1003_t2_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  2  3  1                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1003_t2/1003_t2.fastloc/stats.1003_t2_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  2  4  1                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1003_t2/1003_t2.fastloc/stats.1003_t2_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  2  1  2                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1004_t2/1004_t2.fastloc/stats.1004_t2_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  2  2  2                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1004_t2/1004_t2.fastloc/stats.1004_t2_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  2  3  2                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1004_t2/1004_t2.fastloc/stats.1004_t2_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  2  4  2                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1004_t2/1004_t2.fastloc/stats.1004_t2_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  2  1  3                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1005_t2/1005_t2.fastloc/stats.1005_t2_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  2  2  3                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1005_t2/1005_t2.fastloc/stats.1005_t2_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  2  3  3                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1005_t2/1005_t2.fastloc/stats.1005_t2_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  2  4  3                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1005_t2/1005_t2.fastloc/stats.1005_t2_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  2  1  4                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1006_t2/1006_t2.fastloc/stats.1006_t2_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  2  2  4                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1006_t2/1006_t2.fastloc/stats.1006_t2_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  2  3  4                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1006_t2/1006_t2.fastloc/stats.1006_t2_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  2  4  4                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1006_t2/1006_t2.fastloc/stats.1006_t2_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  2  1  5                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1007_t2/1007_t2.fastloc/stats.1007_t2_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  2  2  5                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1007_t2/1007_t2.fastloc/stats.1007_t2_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  2  3  5                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1007_t2/1007_t2.fastloc/stats.1007_t2_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  2  4  5                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1007_t2/1007_t2.fastloc/stats.1007_t2_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  2  1  6                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1009_t2/1009_t2.fastloc/stats.1009_t2_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  2  2  6                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1009_t2/1009_t2.fastloc/stats.1009_t2_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  2  3  6                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1009_t2/1009_t2.fastloc/stats.1009_t2_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  2  4  6                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1009_t2/1009_t2.fastloc/stats.1009_t2_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  2  1  7                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1016_t2/1016_t2.fastloc/stats.1016_t2_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  2  2  7                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1016_t2/1016_t2.fastloc/stats.1016_t2_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  2  3  7                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1016_t2/1016_t2.fastloc/stats.1016_t2_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  2  4  7                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1016_t2/1016_t2.fastloc/stats.1016_t2_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  2  1  8                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1018_t2/1018_t2.fastloc/stats.1018_t2_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  2  2  8                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1018_t2/1018_t2.fastloc/stats.1018_t2_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  2  3  8                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1018_t2/1018_t2.fastloc/stats.1018_t2_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  2  4  8                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1018_t2/1018_t2.fastloc/stats.1018_t2_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  2  1  9                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1019_t2/1019_t2.fastloc/stats.1019_t2_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  2  2  9                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1019_t2/1019_t2.fastloc/stats.1019_t2_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  2  3  9                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1019_t2/1019_t2.fastloc/stats.1019_t2_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  2  4  9                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1019_t2/1019_t2.fastloc/stats.1019_t2_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  2  1 10                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1021_t2/1021_t2.fastloc/stats.1021_t2_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  2  2 10                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1021_t2/1021_t2.fastloc/stats.1021_t2_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  2  3 10                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1021_t2/1021_t2.fastloc/stats.1021_t2_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  2  4 10                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1021_t2/1021_t2.fastloc/stats.1021_t2_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  2  1 11                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1022_t2/1022_t2.fastloc/stats.1022_t2_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  2  2 11                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1022_t2/1022_t2.fastloc/stats.1022_t2_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  2  3 11                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1022_t2/1022_t2.fastloc/stats.1022_t2_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  2  4 11                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1022_t2/1022_t2.fastloc/stats.1022_t2_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  2  1 12                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1023_t2/1023_t2.fastloc/stats.1023_t2_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  2  2 12                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1023_t2/1023_t2.fastloc/stats.1023_t2_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  2  3 12                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1023_t2/1023_t2.fastloc/stats.1023_t2_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  2  4 12                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1023_t2/1023_t2.fastloc/stats.1023_t2_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  2  1 13                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1024_t2/1024_t2.fastloc/stats.1024_t2_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  2  2 13                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1024_t2/1024_t2.fastloc/stats.1024_t2_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  2  3 13                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1024_t2/1024_t2.fastloc/stats.1024_t2_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  2  4 13                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1024_t2/1024_t2.fastloc/stats.1024_t2_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  2  1 14                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1031_t2/1031_t2.fastloc/stats.1031_t2_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  2  2 14                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1031_t2/1031_t2.fastloc/stats.1031_t2_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  2  3 14                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1031_t2/1031_t2.fastloc/stats.1031_t2_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  2  4 14                                                                                                              \
    "$data1/W1_all_subjects_fastloc/1031_t2/1031_t2.fastloc/stats.1031_t2_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  2  1 15                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2006_t2/2006_t2.fastloc/stats.2006_t2_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  2  2 15                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2006_t2/2006_t2.fastloc/stats.2006_t2_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  2  3 15                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2006_t2/2006_t2.fastloc/stats.2006_t2_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  2  4 15                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2006_t2/2006_t2.fastloc/stats.2006_t2_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  2  1 16                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2011_t2_run2/2011_t2_run2.fastloc/stats.2011_t2_run2_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"   \
                                                                                                                                \
    -dset  2  2 16                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2011_t2_run2/2011_t2_run2.fastloc/stats.2011_t2_run2_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]" \
                                                                                                                                \
    -dset  2  3 16                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2011_t2_run2/2011_t2_run2.fastloc/stats.2011_t2_run2_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"  \
                                                                                                                                \
    -dset  2  4 16                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2011_t2_run2/2011_t2_run2.fastloc/stats.2011_t2_run2_REML+tlrc.HEAD[VOCOD_no#0_Coef]"       \
                                                                                                                                \
    -dset  2  1 17                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2029_t2/2029_t2.fastloc/stats.2029_t2_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  2  2 17                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2029_t2/2029_t2.fastloc/stats.2029_t2_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  2  3 17                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2029_t2/2029_t2.fastloc/stats.2029_t2_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  2  4 17                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2029_t2/2029_t2.fastloc/stats.2029_t2_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  2  1 18                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2035_t2/2035_t2.fastloc/stats.2035_t2_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  2  2 18                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2035_t2/2035_t2.fastloc/stats.2035_t2_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  2  3 18                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2035_t2/2035_t2.fastloc/stats.2035_t2_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  2  4 18                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2035_t2/2035_t2.fastloc/stats.2035_t2_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  2  1 19                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2036_t2/2036_t2.fastloc/stats.2036_t2_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  2  2 19                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2036_t2/2036_t2.fastloc/stats.2036_t2_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  2  3 19                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2036_t2/2036_t2.fastloc/stats.2036_t2_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  2  4 19                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2036_t2/2036_t2.fastloc/stats.2036_t2_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  2  1 20                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2037_t2/2037_t2.fastloc/stats.2037_t2_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  2  2 20                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2037_t2/2037_t2.fastloc/stats.2037_t2_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  2  3 20                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2037_t2/2037_t2.fastloc/stats.2037_t2_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  2  4 20                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2037_t2/2037_t2.fastloc/stats.2037_t2_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  2  1 21                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2038_t2/2038_t2.fastloc/stats.2038_t2_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  2  2 21                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2038_t2/2038_t2.fastloc/stats.2038_t2_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  2  3 21                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2038_t2/2038_t2.fastloc/stats.2038_t2_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  2  4 21                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2038_t2/2038_t2.fastloc/stats.2038_t2_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  2  1 22                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2040_t2/2040_t2.fastloc/stats.2040_t2_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  2  2 22                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2040_t2/2040_t2.fastloc/stats.2040_t2_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  2  3 22                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2040_t2/2040_t2.fastloc/stats.2040_t2_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  2  4 22                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2040_t2/2040_t2.fastloc/stats.2040_t2_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  2  1 23                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2048_t2/2048_t2.fastloc/stats.2048_t2_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  2  2 23                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2048_t2/2048_t2.fastloc/stats.2048_t2_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  2  3 23                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2048_t2/2048_t2.fastloc/stats.2048_t2_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  2  4 23                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2048_t2/2048_t2.fastloc/stats.2048_t2_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  2  1 24                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2052_t2/2052_t2.fastloc/stats.2052_t2_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  2  2 24                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2052_t2/2052_t2.fastloc/stats.2052_t2_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  2  3 24                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2052_t2/2052_t2.fastloc/stats.2052_t2_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  2  4 24                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2052_t2/2052_t2.fastloc/stats.2052_t2_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  2  1 25                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2054_t2/2054_t2.fastloc/stats.2054_t2_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  2  2 25                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2054_t2/2054_t2.fastloc/stats.2054_t2_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  2  3 25                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2054_t2/2054_t2.fastloc/stats.2054_t2_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  2  4 25                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2054_t2/2054_t2.fastloc/stats.2054_t2_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  2  1 26                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2061_t2/2061_t2.fastloc/stats.2061_t2_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  2  2 26                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2061_t2/2061_t2.fastloc/stats.2061_t2_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  2  3 26                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2061_t2/2061_t2.fastloc/stats.2061_t2_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  2  4 26                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2061_t2/2061_t2.fastloc/stats.2061_t2_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -dset  2  1 27                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2067_t2/2067_t2.fastloc/stats.2067_t2_REML+tlrc.HEAD[VIS_UNREL_no#0_Coef]"                  \
                                                                                                                                \
    -dset  2  2 27                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2067_t2/2067_t2.fastloc/stats.2067_t2_REML+tlrc.HEAD[AUDIO_UNREL_no#0_Coef]"                \
                                                                                                                                \
    -dset  2  3 27                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2067_t2/2067_t2.fastloc/stats.2067_t2_REML+tlrc.HEAD[FALSE_FONT_no#0_Coef]"                 \
                                                                                                                                \
    -dset  2  4 27                                                                                                              \
    "$data1/W2_all_subjects_fastloc/2067_t2/2067_t2.fastloc/stats.2067_t2_REML+tlrc.HEAD[VOCOD_no#0_Coef]"                      \
                                                                                                                                \
    -amean 1 amean1                                                                                                             \
    -bmean 1 bmean1                                                                                                             \
    -bucket ./fastlocANOVA3.results

