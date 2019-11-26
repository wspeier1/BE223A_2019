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

allfluoro=[skull' point_2d_red];
allct=[pintips_3d skullpoint_3d];
%allfluoro=point_2d_red;
%allct=pintips_3d;

subnum=50;
subselect=randperm(min([length(allfluoro),length(allct)]),subnum);
subfluoro=[];
subct=[];
for i=1:length(subselect)
    subfluoro=cat(2,subfluoro,allfluoro(:,subselect(i)));
    subct=cat(2,subct,allct(:,subselect(i)));
end

%%%%%%%%%%%%%%%%%%%%%%%%%%
%START OF FINDING PRIOR ROTATION PART
%%%%%%%%%%%%%%%%%%%%%%%%%%

%rot=[0,0,pi/2];
rot=[0,0,-pi/2];
%rot=rand(3,1)
%rot=[0.8240,0.8522,-0.4673];

center_rot=[0;0;600];
R=rotationVectorToMatrix(rot);
ct_roted=R*(subct-center_rot)+center_rot;
ct_flat=Project_point(ct_roted,-100);

subplot(1,2,1);
f1=scatter(ct_flat(1,:),ct_flat(2,:));
subplot(1,2,2);
f2=scatter(subfluoro(1,:),subfluoro(2,:));