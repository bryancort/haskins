#!/usr/bin/env bash

python ../gen_mvm.py \
--mri_dir sample_mri_subjects \
--within_vars_spec_file sample_within.txt \
--between_vars_spec_file sample_between.txt \
--body_entry_spec_file sample_body.txt \
--output_dir ../gen_mvm_sample_outputs \
--proc_run .scale \
--output_table_name sample_mvm_table.txt \
--output_call_name sample_mvm_call.sh \
--quant_covars dummy_covar1,dummy_covar2 \
--quant_covars_centers 20,30 \
--vox_covar SFNR \
--vox_covar_pattern *SFNR*.HEAD