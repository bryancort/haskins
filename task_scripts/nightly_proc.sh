#!/bin/bash

# Define a timestamp function
timestamp() {
  date +"%m_%d_%y"
}

# do something...
ts=`timestamp` # print timestamp

. /Users/cort/.bashrc
python /data1/scripts_refactor/haskins/task_scripts/a182_brain_nii_copy.py 2>&1 | tee /data1/logs/log_${ts}