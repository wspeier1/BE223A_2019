clc;clear;close all;%rng('default')
%CT pintips
Pin = niftiread("./PIN_NII/preopCT_subject_1_PIN_TIPS.nii");
[points(:,1) points(:,2) points(:,3)]=ind2sub(size(Pin), find(Pin));
pintips_3d=points';

%fluoro skull
skull=importdata('skull.txt');
width = max(skull(:,2));
height = max(skull(:,1));
widthfactor=256/width;
heightfactor=256/height;
scalingfactor=mean([widthfactor,heightfactor]);
for i =1:length(skull)
    skull(i,1)=floor(skull(i,1)*scalingfactor)+1;
    skull(i,2)=floor(skull(i,2)*scalingfactor)+1;
end

%Fluoro pintips
point_2d=importdata('pt_fluoro.txt')';
point_2d_perm=randperm(length(point_2d),length(pintips_3d));
point_2d_red=[point_2d(1,point_2d_perm)',point_2d(2,point_2d_perm)']'; %need to scale down points
for i=1:length(point_2d_red)
    point_2d_red(1,i)=floor(point_2d_red(1,i)*scalingfactor)+1;
    point_2d_red(2,i)=floor(point_2d_red(2,i)*scalingfactor)+1;
end

%CT skull
ctskull=niftiread("./samir/SKULL_NII/subject_1_skull.nii");
[points2(:,1) points2(:,2) points2(:,3)]=ind2sub(size(ctskull), find(ctskull));
skullpoint_3d=points2';

skullcurve=[];
for i=1:length(skullpoint_3d)
    if skullpoint_3d(3,i)>70&&skullpoint_3d(3,i)<110
        skullcurve=[skullcurve, skullpoint_3d(:,i)];
    end
end

allfluoro=[skull' point_2d_red];
%allct=[pintips_3d skullpoint_3d];
allct=[pintips_3d skullcurve];
%allfluoro=point_2d_red;
%allct=pintips_3d;

subnum=50;
%subselectct=randperm(min([length(allfluoro),length(allct)]),subnum);
subselectct=randperm(length(allct),subnum);
subselectfluoro=randperm(length(allfluoro),subnum);

subfluoro=[];
subct=[];
for i=1:subnum
    subfluoro=cat(2,subfluoro,allfluoro(:,subselectfluoro(i)));
    subct=cat(2,subct,allct(:,subselectct(i)));
end


% [theta_x, theta_y, theta_z] = optimization( subfluoro,  subct, -60, 5000, 0.01, 1);
% for i=1:length(subct)
%     subct(1,i)=subct(1,i)-theta_x;
%     subct(2,i)=subct(1,i)-theta_y;
%     subct(3,i)=subct(1,i)-theta_z;
% end


r=[0,0,-pi/2];
%r=rand(3,1)
center_rot=[0;0;100];
epsilon=0.5;
plane_z=-60;
R=rotationVectorToMatrix(r);
point_3d_roted=R*(pintips_3d-center_rot)+center_rot;

tic
[best_r] = RotationSearch(subfluoro,pintips_3d,epsilon,center_rot,plane_z,2)
toc
error_degree=acosd(0.5*(trace(R'*rotationVectorToMatrix(best_r))-1))