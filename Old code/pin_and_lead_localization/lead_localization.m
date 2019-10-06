function elecmatrix = lead_localization(filename)
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

h=fspecial('log',10,1.5);
temp=zeros(size(v2,1),size(v2,3));
for i=1:size(v2,2)
    temp(:,:)=v2(:,i,:);
    temp=conv2(temp,-h,'same');
    temp=conv2(temp,-h,'same');
    v2(:,i,:)=temp;
end
mask=(v2/max(v2(:)))>.4;
se = strel('disk',8);
mask=imclose(mask,se);
cc=bwconncomp(mask);
numPixels=cellfun(@numel,cc.PixelIdxList);
origin=[0,0,0,1]*inv(T);
origin=origin(1,1:3);

pixels=[];
for i=1:length(cc.PixelIdxList)
    [x,y,z]=ind2sub(size(mask),cc.PixelIdxList{i});
    a=[x,y,z];
    dists=sqrt(sum((a-ones(size(a,1),1)*origin).^2,2));
    mindist=min(dists);
    %     for j=1:size(a,1)
    %         mindist=min([mindist,sqrt(sum((a(j,:)-origin).^2))]);
    %     end
    if(and(mindist<50,size(cc.PixelIdxList{i},1)>10))
        a2=a(dists<50,:);
        a0=mean(a2,1);
        da=bsxfun(@minus,a2,a0);
        c=(da'*da)/size(a,1);
        [r,~]=svd(c,0);
        x2=da*r(:,1);
        x_min=min(x2);
        x_max=max(x2);
        dx=x_max-x_min;
        xa=(x_min-0.05*dx)*r(:,1)'+a0;
        xb=(x_max+0.05*dx)*r(:,1)'+a0;
        xa=repmat(xa,size(a,1),1);
        xb=repmat(xb,size(a,1),1);
        a3=xa-xb;
        a4=a-xb;
        d=sqrt(sum(cross(a3,a4,2).^2,2))./sqrt(sum(xa.^2,2));
        
        pixels=[pixels;cc.PixelIdxList{i}(d<1)];
    end
end
% [biggest,idx]=max(numPixels);
% mask2=zeros(size(mask));
% mask2(cc.PixelIdxList{idx})=1;
% [x,y,z]=ind2sub(size(mask),cc.PixelIdxList{idx});
[x,y,z]=ind2sub(size(mask),pixels);
elecmatrix=[x,y,z,ones(length(x),1)]*T;
elecmatrix=elecmatrix(:,1:3);

oind=strfind(filename,'\');
outfile=filename(1:oind(end))+"depthelectrodes.mat";
save(outfile,'elecmatrix');