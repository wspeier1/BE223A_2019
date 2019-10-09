% Reflect Electrode Positions about the interhemispheric plane
% interhemispheric plane is marked manually

% method from http://gamedev.stackexchange.com/a/43692

% plot x-plane
Xlim=xlim; Ylim=ylim; Zlim=zlim;
hold on; plot3(zeros(100,100), repmat(linspace(Ylim(1),Ylim(2)),100,1), repmat(linspace(Zlim(1),Zlim(2)),100,1)', 'r.');

% click on the midline plane with camera position along it
pos1=get(gca,'CurrentPoint');
% click on another the midline plane with camera position along it
pos2=get(gca,'CurrentPoint');

% plot pos1 and pos2
hold on; plot3(pos1(:,1), pos1(:,2), pos1(:,3), 'g');
hold on; plot3(pos2(:,1), pos2(:,2), pos2(:,3), 'g');

norm = cross((pos1(2,:)-pos1(1,:)), (pos2(1,:)-pos1(1,:)));
norm=norm/dot(norm, norm)^0.5;
d = dot(-norm,pos1(1,:));

CortElecLocRef = cellfun(@(A) (A - 2*(dot(A,norm)+d)*norm), CortElecLoc, 'UniformOutput', false);
