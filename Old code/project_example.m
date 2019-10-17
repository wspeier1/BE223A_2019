fluoro=imread('C:\Users\wspeier\Documents\GitHub\BE223A_2019\data\example\IM-0001-0001.tif');

figure
imshow(fluoro(:,:,3))
hold on
center=round([size(fluoro,2)/2,size(fluoro,1)/2,10000]);
plot3(center(1),center(2),center(3),'o')

elecmatrix=[
    465 154 0
    519 135 0
    574 122 0
    632 117 0
    684 110 0];

plot3(elecmatrix(:,1),elecmatrix(:,2),elecmatrix(:,3),'o');

lines=cell(size(elecmatrix,1),1);
for i=1:size(elecmatrix,1)
    lines{i}=zeros(center(3),3);
    for j=1:center(3)
        lines{i}(j,:)=(center(3)-j)/center(3)*center+j/center(3)*elecmatrix(i,:);
    end
    plot3(lines{i}(:,1),lines{i}(:,2),lines{i}(:,3));
end

load('C:\Users\wspeier\Documents\GitHub\BE223A_2019\data\example\hull.mat')
s=6;
rx=pi/2;
ry=pi/2;
rz=0;
t=[center(1) center(2) center(3)/2];
T=[ 1       0        0        0
    0       cos(rx)  -sin(rx) 0
    0       sin(rx)  cos(rx)  0
    0       0        0        1];
T2=[cos(ry) 0        sin(ry) 0
    0       1        0        0
    -sin(ry) 0        cos(ry)  0
    0       0        0        1];
T3=[cos(rz) -sin(rz) 0        0
    sin(rz) cos(rz)  0        0
    0       0        1        0
    0       0        0        1];
T4=[s       0        0        t(1)
    0       s        0        t(2)
    0       0        s        t(3)
    0       0        0        1];
mask_indices2=[mask_indices,ones(size(mask_indices,1),1)]*T'*T2'*T4';
plot3(mask_indices2(:,1),mask_indices2(:,2),mask_indices2(:,3),'.')

point=[660.4 325.2 5353
    636.3 330.5 5404
    609.5 331.9 5383
    584.2 338 5385
    560 348.4 5429];
opoint=[point,ones(size(point,1),1)]*inv(T4')*inv(T2')*inv(T');
%opoint=mask_indices2*inv(T4')*inv(T2')*inv(T');
figure
hold on
plot3(mask_indices(:,1),mask_indices(:,2),mask_indices(:,3),'.')
plot3(opoint(:,1),opoint(:,2),opoint(:,3),'o');
