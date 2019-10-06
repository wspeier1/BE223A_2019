% clear;
% clc;

V1 = niftiread('U:\Teaching\UCLA\2019S_BE224B\project\data\subject_1\preopCT_subject_1.nii');
V2 = niftiread('U:\Teaching\UCLA\2019S_BE224B\project\data\subject_1\postopCT_subject_1.nii');
V11 = normalize(squeeze(sum(V1, 3)));
V22 = normalize(squeeze(sum(V2, 3)));
Vf= normalize(V11 + V22);
% Vf= mat2gray(Vf);


V3 = mat2gray(imread('U:\Teaching\UCLA\2019S_BE224B\project\data\subject_1\fluoro_subject_1.jpg'));
% cpselect(V3, Vf);
mytform = fitgeotrans(movingPoints, fixedPoints, 'similarity');
registered = imwarp(V3, mytform,'OutputView', imref2d(size(Vf)));

fused = imfuse(registered, Vf);

imshow(registered);
V4 = niftiread('U:\Teaching\UCLA\2019S_BE224B\project\data\subject_1\hull_subject_1.nii');
elec = zeros(16,3);
for i =1:1:16
    [elec(i,1),elec(i,2)]=getpts;
end

elec2=elec;
elec(:,1)=elec2(:,2);
elec(:,2)=elec2(:,1);
k = size(V4,3);
for i=1:1:16
    for m=1:1:k
        V4(elec(i,1),elec(i,2),m) = 1;
        if((V4(elec(i,1),elec(i,2),m)~= 0))
            elec(i,3)=m;
        elseif((V4(elec(i,1)+1,elec(i,2),m)~= 0))
            elec(i,3)=m;
            elec(i,2)=elec(i,2);
            elec(i,1)=elec(i,1)+1;
        elseif(V4(elec(i,1)-1,elec(i,2),m)~= 0)
            elec(i,3)=m;
            elec(i,2)=elec(i,2);
            elec(i,1)=elec(i,1)-1;
        elseif(V4(elec(i,1),elec(i,2)+1,m)~= 0)
            elec(i,3)=m;
            elec(i,2)=elec(i,2)+1;
            elec(i,1)=elec(i,1);
        elseif(V4(elec(i,1),elec(i,2)-1,m)~= 0)
            elec(i,3)=m;
            elec(i,2)=elec(i,2)-1;
            elec(i,1)=elec(i,1);   
        elseif(V4(elec(i,1)+1,elec(i,2)+1,m)~= 0)
            elec(i,3)=m;
            elec(i,2)=elec(i,2)+1;
            elec(i,1)=elec(i,1)+1;
        elseif(V4(elec(i,1)-1,elec(i,2)-1,m)~= 0)
            elec(i,3)=m;
            elec(i,2)=elec(i,2)-1;
            elec(i,1)=elec(i,1)-1;
        elseif(V4(elec(i,1)+1,elec(i,2)-1,m)~= 0)
            elec(i,3)=m;
            elec(i,2)=elec(i,2)-1;
            elec(i,1)=elec(i,1)+1;
        elseif(V4(elec(i,1)-1,elec(i,2)+1,m)~= 0)
            elec(i,3)=m;
            elec(i,2)=elec(i,2)+1;
            elec(i,1)=elec(i,1)-1;
        end
    end

end
niftiwrite(V4, 'U:\Teaching\UCLA\2019S_BE224B\project\data\subject_1\linesMRI4.nii');

