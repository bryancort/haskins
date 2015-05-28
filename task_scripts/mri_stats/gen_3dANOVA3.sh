#!/usr/bin/env bash

gen_group_command.py -command 3dANOVA3 \
-write_script pidANOVA3_call.tcsh \
-prefix pidANOVA3.results \
-dsets /data3/a202/group_analysis/W2_all_subjects_pid/????_t1*/????_t1*.pid/stats.????_t1*_REML+tlrc.HEAD \
-dsets /data3/a202/group_analysis/W2_all_subjects_pid/????_t2*/????_t2*.pid/stats.????_t2*_REML+tlrc.HEAD \
-subs_betas 'vis_mismatch#0_Coef' 'aud_mismatch#0_Coef'
#-options                                    \
#-acontr 1 1 1 1 1 -5 WORDS_PSW_vs_FF \
#-acontr 1 1 1 1 0 -4 WORDS_vs_FF \
#-acontr 0 0 0 0 1 -1 PSW_vs_FF