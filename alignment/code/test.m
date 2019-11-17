% testing for trans
clc;clear;close all;%rng('default') 
point_3d(1,:)=10*rand(10,1);
point_3d(2,:)=10*rand(10,1);
point_3d(3,:)=10*rand(10,1)-20;
% rotation
r=rand(3,1);
center_rot=[0;0;-20];
epsilon=0.05;
plane_z=-50;
R=rotationVectorToMatrix(r);
point_3d_roted=R*(point_3d-center_rot)+center_rot;

[point_2d] = Project_point(point_3d_roted,plane_z);
% create translation
point_3d = point_3d_roted;
trans=rand(3,1)*5;
point_3d = point_3d + trans;
% icp 
s=-2;
[best_TransVec, best_dis, best_distance] = icp_dist(point_3d,point_2d,plane_z,s, 5);

TransVec = -best_TransVec/plane_z*(best_distance-20);






