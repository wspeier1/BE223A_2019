#---------------------------------------------------------------
# part 1. setup freesurfer and navigate to subject's directory. - (command-L clears terminal text) 
#---------------------------------------------------------------


cd ..
cd ..
# in the below line of code, change "Hiro_sample_images/Pre_opMRI" to "the file location" of the file that youre interested in
cd /Users/soroush/Desktop/Pre_opMRI

#these two lines will set up free surfer
export FREESURFER_HOME=/Applications/freesurfer
export SUBJECTS_DIR=/Users/soroush/Desktop/Pre_opMRI
source $FREESURFER_HOME/SetUPFreeSurfer.sh


#---------------------------------------------------------------
# part 2. code for constructing corital surface. copy code from part 1 to the desired "file location" preprocess and convert to nifti format, make sure that you change the name of the MRI file to "T1" before running the below code, also make sure that "the file location" (which you specified above, matches the location of the T1 file of interest)
#---------------------------------------------------------------

mri_convert --input_volume T1.nii --output_volume T1_Temp.nii
fslchfiletype  NIFTI_GZ T1_temp.nii T1.nii.gz 

recon-all -i T1.nii.gz -subjid cortical_reconstruct -all



#--------------------------------------------------------------------
#part3. copy code from part 1, (you do not need code from part 2) to send free surfer to the desired "file location".  make sure the cortical reconstruction  is named "cortical_reconstruct", this step is not essential, we're just making sure the cortical reconstruction worked (Can be skipped)
#---------------------------------------------------------------------

freeview -f  cortical_reconstruct/surf/rh.pial:annot=aparc.annot:name=pial_aparc:visible=0 \
cortical_reconstruct/surf/rh.inflated:overlay=rh.thickness:overlay_threshold=0.1,3::name=inflated_thickness:visible=0 \
cortical_reconstruct/surf/rh.inflated:visible=0 \
cortical_reconstruct/surf/rh.white:visible=0 \
cortical_reconstruct/surf/rh.pial \
--viewport 3d

#--------------------------------------------------------------------------
#part4.  copy code from part 1 to designate "file location", convert these file to create cortical hull in the next steps. to check if this step worked, go into pre_opMRI->cortical_reconstruct->mri-> look for the three ".nii" files below
#--------------------------------------------------------------------------

mri_convert -i cortical_reconstruct/mri/lh.ribbon.mgz -o cortical_reconstruct/mri/gray_left.nii -it mgz -ot nii
mri_convert -i cortical_reconstruct/mri/rh.ribbon.mgz -o cortical_reconstruct/mri/gray_right.nii -it mgz -ot nii
mri_convert -i cortical_reconstruct/mri/ribbon.mgz -o cortical_reconstruct/mri/T1_class.nii -it mgz -ot nii
