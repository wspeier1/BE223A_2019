% Quick Electrodes and Cortex Plot

% Need to load cortex.mat and electrodes cell array

function Quick_Elec_Cortex_annot_Plot
close all;
f=figure('color','w');

sub = 'bS18';
side = 'r'; % r: right , l: left
plane = 's'; % s: surface only, i: inner plane, too (only for preSMA case)

load(['U:\Users\jeongwoochoi\Study\UCLA\ECoG localization\data\',sub,'\cortex_indiv.mat']);
load(['U:\Users\jeongwoochoi\Study\UCLA\ECoG localization\data\',sub,'\electrode_locs.mat']); % final coordiates of electrodes saved by clicking on the fluoro


% Loading cortical parcellation information
if side == 'l'
    [vertices,label,colortable]=read_annotation(['U:\Users\jeongwoochoi\Study\UCLA\ECoG localization\data\',sub,'\label\lh.aparc.annot']);
else
    [vertices,label,colortable]=read_annotation(['U:\Users\jeongwoochoi\Study\UCLA\ECoG localization\data\',sub,'\label\rh.aparc.annot']);    
end

color_ind = 255*ones(length(vertices),3);  
colortable.table(1,[1 2 3]) = [255 255 255]; % making undefined regions (e.g., subcortical region in the medial plane) white color

for i = 1:length(colortable.table)
    if find(label == colortable.table(i,5))
        ind_2 = find(label == colortable.table(i,5));
        for ii = 1:length(ind_2)
            color_ind(ind_2(ii),:) = colortable.table(i,1:3); % color codes for each cortical ROI
        end
    end
end

% plot cortical parcellation with different colors
if side == 'l'
    Hp = patch('vertices',cortex.vert(1:length(cortex.vert_lh),:),'faces',cortex.tri_lh(:,[1 3 2])+1,'facevertexcdata',color_ind/255,'facecolor','flat','edgecolor','none','facelighting','gouraud');
else side == 'r'
    Hp = patch('vertices',cortex.vert(length(cortex.vert_lh)+1:end,:),'faces',cortex.tri_rh(:,[1 3 2])+1,'facevertexcdata',color_ind/255,'facecolor','flat','edgecolor','none','facelighting','gouraud');
end
axis equal; axis off;
camlight('headlight','infinite');

% adding a slide bar to control the transparency of cortex
b = uicontrol('Parent',f,'Style','slider','Position',[150,20,250,20],'min',0, 'max',1,'value',1,'callback',@fa_update);

% Plot Electrodes
elec = reshape(cell2mat(CortElecLoc),3,length(CortElecLoc))';
hold on; plot3(elec(1:8,1),elec(1:8,2),elec(1:8,3),'w.','MarkerSize',40); % plot Motor strip
hold on; plot3(elec(9:end,1),elec(9:end,2),elec(9:end,3),'w.','MarkerSize',40); % plot 2nd strip (preSMA or rIFG)

if plane == 'i'
load(['U:\Users\jeongwoochoi\Study\UCLA\ECoG localization\data\',sub,'\pc_coord.mat']);
load(['U:\Users\jeongwoochoi\Study\UCLA\ECoG localization\data\',sub,'\cc_coord.mat']);    
hold on; plot3([0,0],[0,0],[0,0],'k.','MarkerSize',25); % plot AC
hold on; plot3([pc_coord(1),pc_coord(1)],[pc_coord(2),pc_coord(2)],[pc_coord(3),pc_coord(3)],'k.','MarkerSize',25); % plot PC
hold on; plot3([0,pc_coord(1)],[0,pc_coord(2)],[0,pc_coord(3)],'k','linewidth',2); % plot AC-PC line
hold on; plot3([cc_coord(1),cc_coord(1)],[cc_coord(2),cc_coord(2)],[cc_coord(3),cc_coord(3)],'k.','MarkerSize',25); % plot iCC 
hold on; plot3([0,0],[0,3*pc_coord(3)],[0,-3*pc_coord(2)],'k--','linewidth',1.5); % plot VAC line
hold on; plot3([0,0]+cc_coord(1),[0,3*pc_coord(3)]+cc_coord(2),[0,-3*pc_coord(2)]+cc_coord(3),'k--','linewidth',1.5); % plot iCC line
end



function fa_update(source,callbackdata)
val = source.Value;
alpha(val);
