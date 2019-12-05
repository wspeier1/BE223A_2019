clc;clear;close all;%rng('default') 
Pin = niftiread("C:/Users/hwz62/Desktop/alignment/PIN_NII/preopCT_subject_1_PIN_TIPS.nii");
[points(:,1) points(:,2) points(:,3)]=ind2sub([256 256 176], find(Pin));
point_3d=points';


%center_rot and plane_z are values I put in initially to make it run
%sensibly. To do: think about geometry of these points to put reasonable
%values in there.

r=[0,0,-pi/2];
center_rot=[0;0;-300];
epsilon=0.5;
plane_z=-500;
R=rotationVectorToMatrix(r);
point_3d_roted=R*(point_3d-center_rot)+center_rot; %Superfluous? +center/-center gets same result???

%[point_2d] = Project_point(point_3d_roted,plane_z);
%point_2d=[point_2d,100*rand(2,10)];
%point_3d=[point_3d,100*rand(3,10)-[0;0;35]];% outlier

point_2d=importdata('pt_fluoro.txt')';
point_2d_perm=randperm(length(point_2d),length(point_3d));
point_2d_red=[point_2d(1,point_2d_perm)',point_2d(2,point_2d_perm)']'; %need to scale down points

tic
[best_r] = RotationSearch(point_2d_red,point_3d,epsilon,center_rot,plane_z,2)
toc
error_degree=acosd(0.5*(trace(R'*rotationVectorToMatrix(best_r))-1))