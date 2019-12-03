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

% brute dist
[theta_x, theta_y, theta_z] = optimization( point_2d,  point_3d, plane_z, 1000, 0.005,10);


% icp 
s=-4;
[best_TransVec, best_dis, best_distance, best_out] = icp_dist(point_3d,point_2d,plane_z,s, 5);

TransVec = -best_TransVec/plane_z*(best_distance-20);

plot(point_2d(1,:),point_2d(2,:),'r.',best_out(1,:),best_out(2,:),'b.'), axis equal


scatter3(point_3d(1,:),point_3d(2,:),point_3d(3,:) )
hold
S = repmat([10],1,10);
C = repmat([3],1,10);
scatter3(point_3d_roted(1,:),point_3d_roted(2,:),point_3d_roted(3,:),S,C )




