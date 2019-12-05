function [Q_u] = Q_upper(point_2d,point_3d,epsilon,r_lu,center_rot,plane_z)
%Q_UPPER get upper bound 
%   ��������Ϊ��2d�㼯��3d�㼯����������ת���䣬��ת���ģ�ͶӰƽ�������

[b_c,b_r] = get_ball(point_3d,r_lu,center_rot); %��ȡ��ȷ��������

[center_circle_2d,radius_circle_2d] = Project_ball_multi(b_c,b_r,plane_z);%

epsilon_=(epsilon+radius_circle_2d).^2;

M=size(b_c,2);%

Q_u=0;
for i=1:M
    c=center_circle_2d(:,i);
    epsilon_2=epsilon_(i);
    erro_2=sum((c-point_2d).^2);
    if(sum((erro_2<epsilon_2))>=1)
        Q_u=Q_u+1;
    end
    
end



end

