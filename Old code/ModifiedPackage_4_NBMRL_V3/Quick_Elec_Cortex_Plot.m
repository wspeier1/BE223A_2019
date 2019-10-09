% Quick Electrodes and Cortex Plot

% Need to load cortex.mat and electrodes cell array


figure;
% Plot Cortex
%Hp = patch('vertices',cortex.vert,'faces',cortex.faces(:,[1 3 2]),'facecolor',[.65 .65 .65],'edgecolor','none');
Hp = patch('vertices',cortex.vert,'faces',cortex.tri(:,[1 3 2]),'facecolor',[.65 .65 .65],'edgecolor','none');
axis equal; axis off;
camlight('headlight','infinite');
material dull

% Hp = patch('vertices',skull_DBS.vert','faces',skull_DBS.tri([1 3 2],:),'facecolor',[.65 .65 .65],'edgecolor','none');
% axis equal; axis off;
% camlight('headlight','infinite');
% material dull


CortElecLoc2 = project2verts( CortElecLoc, cortex.vert );


% Plot Electrodes
elec = reshape(cell2mat(CortElecLoc2),3,length(CortElecLoc2))';
hold on; plot3(elec(:,1),elec(:,2),elec(:,3),'r.','MarkerSize',40);

