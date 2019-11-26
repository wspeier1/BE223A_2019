%rot=[0,0,pi/2];
rot=[0,0,0.9*(pi/2)];

%rot=rand(3,1)

%rot=[0.8240,0.8522,-0.4673];

center_rot=[0;0;200];
plane_z=-60;

R=rotationVectorToMatrix(rot);
ct_roted=R*(subct-center_rot)+center_rot;

ct_flat=Project_point(ct_roted,plane_z);

%subplot(1,2,1);
%f1=scatter(ct_flat(1,:),ct_flat(2,:));
%subplot(1,2,2);
%f2=scatter(subfluoro(1,:),subfluoro(2,:));

scatter3(subfluoro(1,:),subfluoro(2,:),repmat(plane_z,[1,50]));
hold;
scatter3(ct_roted(1,:),ct_roted(2,:),ct_roted(3,:));