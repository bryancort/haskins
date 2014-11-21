def __main__():
    import glob, os
    from mri_automation import processing, a40_pid_pairs

    for s in glob.glob('/data3/pid/New/*_dicom'):
        processing.org_scan_files(s, s, are_dcms=False, **a40_pid_pairs)

if __name__ == '__main__':
    __main__()