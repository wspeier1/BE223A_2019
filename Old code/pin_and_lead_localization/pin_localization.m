function elecmatrix = pin_localization(filename)
% v=niftiread('U:\Research\Alon\ECoG Localization\coregisteted_postopCT_DBS_ls02.nii');
% info=niftiinfo('U:\Research\Alon\ECoG Localization\coregisteted_postopCT_DBS_ls02.nii');
% v=niftiread(filename);
nii=load_untouch_nii(filename);
v=nii.img;
% info=niftiinfo(filename);
T=[nii.hdr.hist.srow_x;nii.hdr.hist.srow_y;nii.hdr.hist.srow_z;[0,0,0,1]]';
v2=(v-min(v(:)))/(max(v(:))-min(v(:)));
v2(isnan(v2))=0;
v2=single(v2);

% v3=medfilt3(v2,[11,11,11]);
v4=v2;

h=fspecial('log',15,2);
temp=zeros(size(v2,2),size(v2,3));
% temp2=zeros(size(v2,1),size(v2,3));
for i=1:size(v2,1)
    temp(:,:)=v2(i,:,:);
%     temp2(:,:)=v3(:,i,:);
    temp=conv2(temp,-h,'same');
    temp=conv2(temp,-h,'same');
    v4(i,:,:)=temp;
end
temp=zeros(size(v2,1),size(v2,3));
for i=1:size(v2,2)
    temp(:,:)=v4(:,i,:);
%     temp2(:,:)=v3(:,i,:);
    temp=conv2(temp,-h,'same');
    temp=conv2(temp,-h,'same');
    v4(:,i,:)=temp;
end
temp=zeros(size(v2,1),size(v2,2));
for i=1:size(v2,3)
    temp(:,:)=v4(:,:,i);
%     temp2(:,:)=v3(:,i,:);
    temp=conv2(temp,-h,'same');
    temp=conv2(temp,-h,'same');
    v4(:,:,i)=temp;
end
mask=(v4/max(v4(:)))>.5;
se = strel('sphere',12);
% mask=imclose(mask,se);
mask2=imdilate(mask,se);
cc=bwconncomp(mask2);
numPixels=cellfun(@numel,cc.PixelIdxList);
% origin=[0,0,0,1]*inv(info.Transform.T);
origin=[0,0,0,1]*inv(T);
origin=origin(1,1:3);

pixels=[];
pixels2=[];
for i=1:length(cc.PixelIdxList)
%     mindist=length(mask(:));
%     minind=-1;
    idx=cc.PixelIdxList{i}(mask(cc.PixelIdxList{i})==1);
    [x,y,z]=ind2sub(size(mask),idx);
%     [x,y,z]=ind2sub(size(mask),cc.PixelIdxList{i});
    a=[x,y,z];
    %     for j=1:size(cc.PixelIdxList{i},1)
    %         [mindist,minind]=min([mindist,sqrt(sum((a(j,:)-origin).^2))]);
    %     end
    [mindist,minind]=min(sqrt(sum((a-ones(size(a,1),1)*origin).^2,2)));
    %     if(and(mindist<250,size(cc.PixelIdxList{i},1)>10))
    if(and(mindist<250,size(idx,1)>20))
        %     [~,vol]=convhull(x,y,z);
        %     [length(x) mindist length(x)/vol]
        pixels=[pixels;idx];
        pixels2=[pixels2;idx(minind)];
        %         pixels=[pixels;cc.PixelIdxList{i}(minind)];
        %         pixels=[pixels;cc.PixelIdxList{i}];
    end
end

% [biggest,idx]=max(numPixels);
% mask2=zeros(size(mask));
% mask2(cc.PixelIdxList{idx})=1;
% [x,y,z]=ind2sub(size(mask),cc.PixelIdxList{idx});
[x,y,z]=ind2sub(size(mask),pixels2);

ind=[1,2,3,4];
minvol=Inf;
for i=1:length(pixels2)
    for j=setdiff(1:length(pixels2),i)
        for k=setdiff(1:length(pixels2),[i,j])
            for m=setdiff(1:length(pixels2),[i,j,k])
                [~,vol]=convhull(x([i,j,k,m]),y([i,j,k,m]),z([i,j,k,m]));
                if(vol<minvol)
                    ind=[i,j,k,m];
                    minvol=vol;
                end
            end
        end
    end
end
x=x(ind);
y=y(ind);
z=z(ind);


% elecmatrix=[x,y,z,ones(length(x),1)]*info.Transform.T;
elecmatrix=[x,y,z,ones(length(x),1)]*T;
elecmatrix=elecmatrix(:,1:3);

oind=strfind(filename,'\');
outfile=filename(1:oind(end))+"PinTips.mat";
save(outfile,'elecmatrix');