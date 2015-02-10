#!/bin/bash

export AFNI_DETACH=NO

echo "Beginning snapshots";
`which Xvfb` :1 -screen 0 1024x768x24 &

parentDir=`pwd`

for aDir in $@
do
	cd $aDir;
	if [ ! -e snapshots ]; then
		mkdir snapshots;
	fi
	
	#resting state
	if [ -e $aDir.rest ]; then
		cd ${aDir}.rest
		1dplot -jpg ../snapshots/${aDir}_rest_motion_plots.jpg -volreg -censor censor_${aDir}_combined_2.1D dfile_rall.1D
		cd ../;
	fi
	
	#fastlocalizer
	if [ -e $aDir.fastloc ]; then
		cd ${aDir}.fastloc
		centerC=`3dCM anat_final.${aDir}+orig`;

		DISPLAY=:1 afni -com "OPEN_WINDOW A.axialimage  mont=6x6:3 geom=600x600+800+600" \
		 -com "CLOSE_WINDOW A.sagittalimage" \
		 -com "SWITCH_UNDERLAY anat_final.${aDir}+orig" \
		 -com "SET_FUNC_AUTORANGE A.-" \
		 -com "SET_FUNC_RANGE A.10" \
		 -com "SWITCH_OVERLAY stats.${aDir}+orig" \
		 -com "SET_DICOM_XYZ A ${centerC}" \
		 -com "SET_SUBBRICKS A -1 13 14" \
		 -com "SET_THRESHNEW A .001 *p" \
		 -com "SAVE_JPEG A.axialimage ../snapshots/${aDir}_fastloc_print.jpg" \
		 -com "SET_SUBBRICKS A -1 16 17" \
		 -com "SET_THRESHNEW A .001 *p" \
		 -com "SAVE_JPEG A.axialimage ../snapshots/${aDir}_fastloc_speech.jpg" \
		 -com "SET_SUBBRICKS A -1 19 20" \
		 -com "SET_THRESHNEW A .001 *p" \
		 -com "SAVE_JPEG A.axialimage ../snapshots/${aDir}_fastloc_falsefont.jpg" \
		 -com "SET_SUBBRICKS A -1 22 23" \
		 -com "SET_THRESHNEW A .001 *p" \
		 -com "SAVE_JPEG A.axialimage ../snapshots/${aDir}_fastloc_vocodspeech.jpg" \
		 -com "SET_SUBBRICKS A -1 31 32" \
		 -com "SET_THRESHNEW A .001 *p" \
		 -com "SAVE_JPEG A.axialimage ../snapshots/${aDir}_fastloc_print-speech.jpg" \
		 -com "QUIT"   
		
		  1dplot -jpg ../snapshots/${aDir}_fastloc_motion_plots.jpg -volreg -censor censor_${aDir}_combined_2.1D dfile_rall.1D
		  cd ../;
	fi
	
	if [ -e $aDir.srtt ]; then
		cd $aDir.srtt
		centerC=`3dCM anat_final.${aDir}+orig`

		DISPLAY=:1 afni -com "OPEN_WINDOW A.axialimage  mont=6x6:3 geom=600x600+800+600" \
		 -com "CLOSE_WINDOW A.sagittalimage" \
		 -com "SWITCH_UNDERLAY anat_final.${aDir}+orig" \
		 -com "SET_FUNC_AUTORANGE A.+" \
		 -com "SWITCH_OVERLAY stats.${aDir}_REML+orig" \
		 -com "SET_DICOM_XYZ A ${centerC}" \
		 -com "SET_SUBBRICKS A -1 20 20" \
		 -com "SET_THRESHNEW A .001 *p" \
		 -com "SAVE_JPEG A.axialimage ../snapshots/${aDir}_srtt_uns-base.jpg" \
		 -com "SET_SUBBRICKS A -1 23 23" \
		 -com "SET_THRESHNEW A .001 *p" \
		 -com "SAVE_JPEG A.axialimage ../snapshots/${aDir}_srtt_str-base.jpg" \
		 -com "SET_SUBBRICKS A -1 26 26" \
		 -com "SET_THRESHNEW A .001 *p" \
		 -com "SAVE_JPEG A.axialimage ../snapshots/${aDir}_srtt_str-uns.jpg" \
		 -com "QUIT"   
		
		  1dplot -jpg ../snapshots/${aDir}_srtt_motion_plots.jpg -volreg -censor censor_${aDir}_combined_2.1D dfile_rall.1D
		  cd ../;
	fi
	
	#story
	if [ -e $aDir.story ]; then
		cd $aDir.story
		centerC=`3dCM anat_final.${aDir}+orig`
		
		DISPLAY=:1 afni -com "OPEN_WINDOW A.axialimage  mont=6x6:3 geom=600x600+800+600" \
		 -com "CLOSE_WINDOW A.sagittalimage" \
		 -com "SWITCH_UNDERLAY anat_final.${aDir}+orig" \
		 -com "SET_FUNC_AUTORANGE A.+" \
		 -com "SWITCH_OVERLAY stats.${aDir}+orig" \
		 -com "SET_DICOM_XYZ A ${centerC}" \
		 -com "SET_SUBBRICKS A -1 8 8" \
		 -com "SET_THRESHNEW A .001 *p" \
		 -com "SAVE_JPEG A.axialimage ../snapshots/${aDir}_story_audio-baseline.jpg" \
		 -com "SET_SUBBRICKS A -1 11 11" \
		 -com "SET_THRESHNEW A .001 *p" \
		 -com "SAVE_JPEG A.axialimage ../snapshots/${aDir}_story_visual-baseline.jpg" \
		 -com "SET_SUBBRICKS A -1 14 14" \
		 -com "SET_THRESHNEW A .001 *p" \
		 -com "SAVE_JPEG A.axialimage ../snapshots/${aDir}_story_audio-visual.jpg" \
		 -com "QUIT"   
		 
		 1dplot -jpg ../snapshots/${aDir}_story_motion_plots.jpg -volreg -censor censor_${aDir}_combined_2.1D dfile_rall.1D
		 cd ..
	fi

    #sal
	if [ -e $aDir.sal ]; then
		cd $aDir.sal
		centerC=`3dCM anat_final.${aDir}+tlrc`
		
		DISPLAY=:1 afni -com "OPEN_WINDOW A.axialimage  mont=6x6:3 geom=600x600+800+600" \
		 -com "CLOSE_WINDOW A.sagittalimage" \
		 -com "SWITCH_UNDERLAY anat_final.${aDir}+tlrc" \
		 -com "SET_FUNC_AUTORANGE A.+" \
		 -com "SWITCH_OVERLAY stats.${aDir}_REML+tlrc" \
		 -com "SET_DICOM_XYZ A ${centerC}" \
		 -com "SET_SUBBRICKS A -1 61 62" \
		 -com "SET_THRESHNEW A .01 *p" \
		 -com "SAVE_JPEG A.axialimage ../snapshots/${aDir}_sal_Consolidated.jpg" \
		 -com "SET_SUBBRICKS A -1 64 65" \
		 -com "SET_THRESHNEW A .01 *p" \
		 -com "SAVE_JPEG A.axialimage ../snapshots/${aDir}_sal_Unconsolidated.jpg" \
		 -com "SET_SUBBRICKS A -1 76 77" \
		 -com "SET_THRESHNEW A .01 *p" \
		 -com "SAVE_JPEG A.axialimage ../snapshots/${aDir}_sal_Con-Unc.jpg" \
		 -com "QUIT"   
		 
		 1dplot -jpg ../snapshots/${aDir}_sal_motion_plots.jpg -volreg -censor censor_${aDir}_combined_2.1D dfile_rall.1D
		 cd ..
	fi
	
	#val
	if [ -e $aDir.val ]; then
		cd $aDir.val
		centerC=`3dCM anat_final.${aDir}+orig`
		
		DISPLAY=:1 afni -com "OPEN_WINDOW A.axialimage  mont=6x6:3 geom=600x600+800+600" \
		 -com "CLOSE_WINDOW A.sagittalimage" \
		 -com "SWITCH_UNDERLAY anat_final.${aDir}+orig" \
		 -com "SET_FUNC_AUTORANGE A.+" \
		 -com "SWITCH_OVERLAY stats.${aDir}_REML+orig" \
		 -com "SET_DICOM_XYZ A ${centerC}" \
		 -com "SET_SUBBRICKS A -1 23 23" \
		 -com "SET_THRESHNEW A .01 *p" \
		 -com "SAVE_JPEG A.axialimage ../snapshots/${aDir}_val_con_psw1.jpg" \
		 -com "SET_SUBBRICKS A -1 26 26" \
		 -com "SET_THRESHNEW A .01 *p" \
		 -com "SAVE_JPEG A.axialimage ../snapshots/${aDir}_val_exc_psw.jpg" \
		 -com "SET_SUBBRICKS A -1 38 38" \
		 -com "SET_THRESHNEW A .01 *p" \
		 -com "SAVE_JPEG A.axialimage ../snapshots/${aDir}_val_real_word.jpg" \
		 -com "QUIT"   
		 
		 1dplot -jpg ../snapshots/${aDir}_val_motion_plots.jpg -volreg -censor censor_${aDir}_combined_2.1D dfile_rall.1D
		 cd ..
	fi

	#dti
        if [ -e dti ]; then
                cd dti/processed
                centerC=`3dCM DTIColorMap_run1+orig`

               DISPLAY=:1  afni -com "OPEN_WINDOW A.axialimage  mont=6x6:2 geom=600x600+800+600" \
                 -com "CLOSE_WINDOW A.sagittalimage" \
                 -com "SWITCH_UNDERLAY DTIColorMap_run1+orig" \
                 -com "SET_DICOM_XYZ A ${centerC}" \
                 -com "SAVE_JPEG A.axialimage ../../snapshots/${aDir}_DTI.jpg" \
                 -com "QUIT"
		cd ../../
        fi

cd $parentDir;
	
done

killall Xvfb
