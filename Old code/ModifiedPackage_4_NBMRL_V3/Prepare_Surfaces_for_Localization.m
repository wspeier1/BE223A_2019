%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Prepare_for_Localization 
% need T1 image and freesurface cortical reconstructions
% 3D surfaces from co-registered Pre and Post-op CT scans
% outputs include Skull-frame (from pre-op CT), Skull-DBS (from post-op CT), 
% cortex (from pre-op MRI) and cortical hull (from pre-op MRI)                                           %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% this is the main subject directory
Subj_dir = '/Users/yuyan/Desktop/Papers/Course/programming lab MII A/assignment/BE223A_2019/data/subject_4';
cd(Subj_dir) % goes to subject'd directory
mkdir Electrode_Locations % this creates a subdirectory that will be used to store electrode locations subsequently clearv%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Cortex (surface and cortical hull) - need freesurfer matlab in the matlab
% path
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% (1) cortical surface, make sure that instead of "sample" you enter the
% name of cortical reconstruction folder, "cortical_reconstruct"
[cortex.vert_lh,cortex.tri_lh]= read_surf('./Pre_opMRI/cortical_reconstruct/surf/lh.pial'); % Reading left side pial surface --> change "sample" to "cortical_reconstruct"
[cortex.vert_rh,cortex.tri_rh]= read_surf('./Pre_opMRI/cortical_reconstruct/surf/rh.pial'); % Reading right side pial surface --> change "sample" to "cortical_reconstruct"

% Generating entire cortex
cortex.vert = [cortex.vert_lh; cortex.vert_rh]; % Combining both hemispheres
cortex.tri = [cortex.tri_lh; (cortex.tri_rh + length(cortex.vert_lh))]; % Combining faces (Have to add to number of faces)

cortex.tri=cortex.tri+1; % freesurfer starts at 0 for indexing

% Reading in structural MRI parameters
f=MRIread('./Pre_opMRI/cortical_reconstruct/mri/T1.mgz'); % change "sample" to cortical_reconsturct

% Translating into the appropriate space
for k=1:size(cortex.vert,1)
    a=f.vox2ras/f.tkrvox2ras*[cortex.vert(k,:) 1]';
    cortex.vert(k,:)=a(1:3)';
end

% save the cortical surface in subject's direcotry
save('./cortex_indiv.mat','cortex');


%% (2) cortical hull
% T1_class is the gray matter surface created by freesurfer and stored as
% ribbon.mgz, you should convert this to nifti

grayfilename = [Subj_dir,'/Pre_opMRI/cortical_reconstruct/mri/T1_class.nii']; %--> change "sample" to "cortical_reconstruct"
outputdir='hull';
[~,~] = get_hull(grayfilename,outputdir,3,21,.3);
%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%\ CT 3D rendered Skull, stereotactic frame and DBS leads
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Skull_frame
[skull.vert,skull.tri] = obj_display_editMR010514('skull.obj');
save('skull.mat','skull')
% Skull_DBS
[skull_DBS.vert,skull_DBS.tri] = obj_display_editMR010514('skull_and_DBSleads.obj');
save('skull_DBS.mat','skull_DBS')












