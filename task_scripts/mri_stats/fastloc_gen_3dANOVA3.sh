#!/usr/bin/env bash

gen_group_command.py -command 3dANOVA3 \
-write_script fastlocANOVA3_call.tcsh \
-prefix fastlocANOVA3.results \
-dsets /data3/a202/group_analysis/W?_all_subjects_fastloc/????_t1*/????_t1*.fastloc/stats.????_t1*_REML+tlrc.HEAD \
-dsets /data3/a202/group_analysis/W?_all_subjects_fastloc/????_t2*/????_t2*.fastloc/stats.????_t2*_REML+tlrc.HEAD \
-subs_betas 'VIS_UNREL_no#0_Coef' 'AUDIO_UNREL_no#0_Coef' 'FALSE_FONT_no#0_Coef' 'VOCOD_no#0_Coef'
#-options                                    \
#-acontr 1 1 1 1 1 -5 WORDS_PSW_vs_FF \
#-acontr 1 1 1 1 0 -4 WORDS_vs_FF \
#-acontr 0 0 0 0 1 -1 PSW_vs_FF