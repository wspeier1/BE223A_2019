function plot_cortex( cortex, color)
%UNTITLED6 Summary of this function goes here
%   Detailed explanation goes here

if isempty(color)
    color = [.65 .65 .65];
end

if isfield(cortex, 'tri')
    trifield = 'tri';
elseif isfield(cortex, 'faces')
    trifield = 'faces';
else
    warning('No face data provieded.'); return;
end

patch('vertices',cortex.vert,'faces',cortex.(trifield)(:,[1 3 2]),'facecolor', color,'edgecolor','none');
axis equal; axis off;
camlight('headlight','infinite');

end

