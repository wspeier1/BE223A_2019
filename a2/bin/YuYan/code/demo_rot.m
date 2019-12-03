clc;clear;close all;%rng('default') 
% load the data
%Pin = niftiread("/Users/yuyan/Desktop/Papers/Course/programming lab MII A/assignment/BE223A_2019/data/temp/coregisterd_preopCT_subject27_PIN_TIPS.nii");
%[point_3d(1,:),point_3d(2,:),point_3d(3,:)]=find(Pin);
% point_2d = ???

% initial rotation and translation
% Please change the initial rotation vector and translation vector and
% center of rotation(can be the center of the brain)
r=rand(3,1);
s = -25;
trans=[0; 0; s];
center_rot=[0;0;-30];epsilon=0.05;
plane_z=-50;
R=rotationVectorToMatrix(r);
point_3d=R*(point_3d-center_rot)+center_rot;
point_3d=point_3d + trans;
% create outlier
%point_2d=[point_2d,5*rand(2,10)];
%point_3d=[point_3d,10*rand(3,10)-[0;0;35]];% outlier

tic
% remember to deal with the point that fall out of plane
[best_r] = RotationSearch(point_2d,point_3d,epsilon,center_rot,plane_z,2)
toc
%error_degree=acosd(0.5*(trace(R'*rotationVectorToMatrix(best_r))-1))
% now optimize the translation
point_3d = rotationVectorToMatrix(best_r)*(point_3d-center_rot) + center_rot;
[project_point_2d] = Project_point(point_3d,plane_z);
% brutal force icp

[best_TransVec, best_dis, best_distance] = icp_dist(point_3d,point_2d,plane_z,s, 5);
TransVec = best_TransVec/plane_z*(distance+s);



