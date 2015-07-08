#!/usr/bin/env bash

# -options not working for contrasts

gen_group_command.py -command 3dANOVA3 \
-write_script pidANOVA3_call.tcsh \
-prefix pidANOVA3.results \
-dsets /data3/a202/group_analysis/W?_all_subjects_pid/????_t1*/????_t1*.pid/stats.????_t1*_REML+tlrc.HEAD \
-dsets /data3/a202/group_analysis/W?_all_subjects_pid/????_t2*/????_t2*.pid/stats.????_t2*_REML+tlrc.HEAD \
-subs_betas 'vis_word_mis#0_Coef' 'aud_word_mis#0_Coef'
-options \
-amean 1 T1 \
-amean 2 T2 \
-bmean 1 vis \
-bmean 2 aud \
-abmean 1 1 T1_vis \
-abmean 1 2 T1_aud \
-abmean 2 1 T2_vis \
-abmean 2 2 T1_aud \
-acontr -1 1 T2-T1 \
-bcontr -1 1 aud-vis \
-aBdiff -1 1 : 1 T2-T1_vis \
-aBdiff -1 1 : 2 T2-T1_aud \
-Abdiff -1 1 : 1 T1_aud-vis \
-Abdiff -1 1 : 2 T2_aud-vis \
-bucket ./pidANOVA3.results