function [center_circle_2d,radius_circle_2d] = Project_ball_multi(b_c,b_r,plane_z)
% �Ѷ�������ͶӰ��ע��b_cΪN�У���ʾN����


%1.������Բ���ķ���
e_=b_c;
L_b_c=sqrt(sum(e_.^2));
e=e_./L_b_c;%��λ������

%2.��Բ���뾶

L_tangent=realsqrt(abs(L_b_c.^2-b_r.^2));

r_circle=b_r.*L_tangent./L_b_c; %<-------Բ���뾶

%3.��Բ������
% k=realsqrt(abs(L_tangent.^2-r_circle.^2));
k=r_circle.*(L_tangent./b_r);
c_circle=k.*e;%<-----------Բ������

%4.��ͶӰ
M=size(e,2);
e_plane=repmat([0;0;1],1,M);

e1_=cross(e,e_plane);

e2_=cross(e1_,e);
e2_L=sqrt(sum(e2_.^2));
flag=e2_L<1e-6;%��һ����Ϊ�˴������ĺ�ͶӰ������ߺ�Z��ƽ�е�����
                %����������£�e1��[0;0;1]ƽ�У�e2Ϊ[0;0;0]��
                %e1��[0;0;1]ƽ��ʱ��e2����Ϊ[0;1;0];
    
e2_L(flag)=1;
e2=e2_./e2_L;

e2(1,flag)=0;
e2(2,flag)=1;
e2(3,flag)=0;



Point_3D_axis=[c_circle+r_circle.*e2,c_circle-r_circle.*e2];

Point_2D_dim = Project_point(Point_3D_axis,plane_z);
radius_circle_2d=0.5*realsqrt(sum((Point_2D_dim(:,1:M)-Point_2D_dim(:,M+1:end)).^2));

center_circle_2d=0.5*(Point_2D_dim(:,1:M)+Point_2D_dim(:,M+1:end));


end

