skull=importdata('skull.txt');

width = max(skull(:,2));
height = max(skull(:,1));

widthfactor=256/width;
heightfactor=256/height;

for i =1:length(skull)
    skull(i,1)=round(skull(i,1)*heightfactor);
    skull(i,2)=round(skull(i,2)*widthfactor);
end
