function plot_circle(center_circle_2d,radius_circle_2d)
%PLOT_CIRCLE �˴���ʾ�йش˺�����ժҪ
%   ��ʾ���Թ����е�����


theta=0:0.01:2*pi;
x_r=sin(theta);
y_r=cos(theta);

M=size(center_circle_2d,2);
hold on
for i=1:M
    plot(radius_circle_2d(:,i)*x_r+center_circle_2d(1,i),radius_circle_2d(:,i)*y_r+center_circle_2d(2,i),'r');
end
return
end

