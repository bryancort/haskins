def __main__():
    from utils import mri_utils
    mri_utils.gen_snapshots(out_dir="/data1/A182/mri_subjects/tb7065/rois/func_roi_vwfa",
                            out_prefix="test_snapshot",
                            underlay="Sag3DMPRAGEs002a1001_ns+orig.HEAD",
                            overlay="stats.tb7065_REML+orig.HEAD'[26]'")

    # mri_utils.gen_snapshots(out_dir="/data1/A182/mri_subjects/tb7065/rois/func_roi_vwfa",
    #                         out_prefix="test_snapshot",
    #                         underlay="/data1/A182/mri_subjects/tb7065/rois/func_roi_ang/Sag3DMPRAGEs002a1001_ns+orig.HEAD",
    #                         overlay="/data1/a182/mri_subjects/tb7065/tb7065.fastloc/stats.tb7065_REML+orig.HEAD'[26]'")

    #HISTORY
    # from utils import file_utils
    # file_utils.change_all_references("/data1/A182/", "tb1037", "tb0137",
    #                         ("*idTable.txt", "*afni*tb1037*.tcsh", "*epi_review.tb1037", "*tb0137*.HEAD"))
    # file_utils.change_all_references("/data1/A182/", "tb1037", "tb0137",
    #                         ("*idTable.txt", "*afni*tb1037*.tcsh", "*epi_review.tb1037", "*tb0137*.HEAD"))
    pass


if __name__ == '__main__':
    __main__()