% DBS
% CT
DBS_CT = niftiread("subject_4_DBS.nii");
[DBS_points(:,1), DBS_points(:,2), DBS_points(:,3)]=ind2sub(size(DBS_CT), find(DBS_CT));
DBS_3d=DBS_points';
% flouro
DBS_2d=importdata('DBS_lead_4.txt')';
% put flouro in center
DBS_2d = DBS_2d - [512; 640];
% use one strip
%DBS_3d = DBS_3d(:,1:87);

% Pin tips
% CT
Pin = niftiread("./preopCT_subject_1_PIN_TIPS.nii");
[points(:,1), points(:,2), points(:,3)]=ind2sub(size(Pin), find(Pin));
pintips_3d=points';

%Fluoro pintips
pintips_2d=importdata('pt_fluoro.txt')';
pintips_2d = pintips_2d - [512; 640];


% random initial
r=[0,0,pi];
scaling = 3;
init_t = [-128;-128;-100];
center_rot=init_t;
epsilon=10;

plane_z=-300;
R=rotationVectorToMatrix(r);
DBS_3d = (DBS_3d + init_t)*scaling;
DBS_3d=R*(DBS_3d-center_rot)+center_rot;
pintips_3d = (pintips_3d + init_t)*scaling;
pintips_3d=R*(pintips_3d-center_rot)+center_rot;

% sampling for equal comparison 
if size(DBS_2d, 2)> size(pintips_2d,2)
    inx = randsample(size(DBS_2d, 2),size(pintips_2d,2));
    DBS_2d = DBS_2d(:,inx);
else
    inx = randsample(size(pintips_2d, 2),size(DBS_2d,2));
    pintips_2d = pintips_2d(:,inx);
end
% downsampling for quick analysis
num_sample = 100;
if size(pintips_3d, 2)> num_sample
    inx = randsample(size(pintips_3d, 2),num_sample);
    pintips_3d = pintips_3d(:,inx);
end
if size(DBS_3d, 2)> num_sample
    inx = randsample(size(DBS_3d, 2),num_sample);
    DBS_3d = DBS_3d(:,inx);
end



% visualize
close
plot3(DBS_2d(1,:),DBS_2d(2,:),repmat([plane_z], [1,size(DBS_2d,2) ]),'o')
hold
plot3(DBS_3d(1,:),DBS_3d(2,:),DBS_3d(3,:),'x')
plot3(pintips_2d(1,:),pintips_2d(2,:),repmat([plane_z], [1,size(pintips_2d,2) ]),'o')
plot3(pintips_3d(1,:),pintips_3d(2,:),pintips_3d(3,:),'x')


close
[point_2d_proj] = Project_point(DBS_3d,plane_z);
[point_2d_proj_pin] = Project_point(pintips_3d,plane_z);
plot(DBS_2d(1,:), DBS_2d(2,:),'o')
hold
plot(pinntips_2d(1,:), pintips_2d(2,:),'o')
plot(point_2d_proj(1,:), point_2d_proj(2,:),'x')
plot(point_2d_proj_pin(1,:), point_2d_proj_pin(2,:),'x')

close

DBS_3d = [DBS_3d, pintips_3d];
DBS_2d = [DBS_2ds, pintips_2d];

% initialize
[~, ~, ~, old_loss]=optimization(DBS_2d,DBS_3d,plane_z,1000,0.01);
new_loss = old_loss - 11;


% keep track of the Translation and Rotation
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% FOR HENRY %
% Best_rotation and Best_translation is not the final rotation and
% transformation you also need to consider the preprosessing at the
% begining including r, init_t and scaling
Best_rotation = eye(3);
Best_translation = [0;0;0];

% rough search
[Best_rotation, Best_translation, new_loss, DBS_2d, DBS_3d] = Batch_optimize(Best_rotation,Best_translation, ...
    new_loss,DBS_2d,DBS_3d,10,center_rot,plane_z,1,10);
close all

% detail search
[Best_rotation, Best_translation, new_loss, DBS_2d, DBS_3d] = Batch_optimize(Best_rotation,Best_translation, ...
    new_loss,DBS_2d,DBS_3d,1,center_rot,plane_z,1,10);
close all



