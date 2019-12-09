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

DBS_3d = [DBS_3d, pintips_3d];
DBS_2d = [DBS_2d, pintips_2d];


% multiple random initial
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% For Henry   
% result will be store in B_best_rotation, B_best_translation,
% best_scaling. These are for 3D object, no other translation or rotation
% need to be considered.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

number_init = 10;
best_loss = 9000;
B_best_rotation = eye(3);
B_best_translation = [0;0;0];
best_scaling = 0;
for i=1:number_init
    % random initialization
    r=[rand,rand,rand]*2*pi;
    scaling = rand*5;
    init_t = [rand;rand;rand]*-200;
    center_rot=init_t;

    plane_z=-300;
    R=rotationVectorToMatrix(r);
    DBS_3d = (DBS_3d + init_t)*scaling;
    DBS_3d=R*(DBS_3d-center_rot)+center_rot;

    % visualize
    close
    plot3(DBS_2d(1,:),DBS_2d(2,:),repmat([plane_z], [1,size(DBS_2d,2) ]),'o')
    hold
    plot3(DBS_3d(1,:),DBS_3d(2,:),DBS_3d(3,:),'x')
    pause(3)

    close
    [point_2d_proj] = Project_point(DBS_3d,plane_z);
    plot(DBS_2d(1,:), DBS_2d(2,:),'o')
    hold
    plot(point_2d_proj(1,:), point_2d_proj(2,:),'x')
    pause(3)
    close


    % initialize
    [~, ~, ~, old_loss]=optimization(DBS_2d,DBS_3d,plane_z,1000,0.01);
    new_loss = old_loss - 11;

    Best_rotation = R;
    Best_translation = init_t;

    % rough search
    [Best_rotation, Best_translation, new_loss,  DBS_3d, center_rot] = Batch_optimize(Best_rotation,Best_translation, ...
        new_loss,DBS_2d,DBS_3d,10,center_rot,plane_z,1,10);
    close all

    % detail search
    [Best_rotation, Best_translation, new_loss,  DBS_3d, center_rot] = Batch_optimize(Best_rotation,Best_translation, ...
        new_loss,DBS_2d,DBS_3d,1,center_rot,plane_z,3,10);
    close all
    
    %final search
    [best_r] = RotationSearch(DBS_2d,DBS_3d,0.01,center_rot,plane_z,1, 30);
    
    % update the the best result
    if new_loss < best_loss
        best_loss = new_loss;
        B_best_rotation = Best_rotation;
        B_best_translation = Best_translation;
        best_scaling = scaling;
    end
    
end


