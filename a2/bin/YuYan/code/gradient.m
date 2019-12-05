function [gradient_x, gradient_y, gradient_z] = gradient( point_2d, project_point_2d, point_3d,theta_x,theta_y, theta_z, plane_z, lambda, index_2d)
    % calculate the gradient
    % theta: translation
    % project_2d_one is just one point in point_2d
    % regularize
    dx = 2*(project_point_2d(1,:)-point_2d(1,index_2d));
    gradient_x = sum(dx./(point_3d(3,:)+theta_z)*plane_z)/size(point_3d,2)+ lambda*theta_x ;
    dy = 2*(project_point_2d(2,:)-point_2d(2,index_2d));
    gradient_y = sum(dy./(point_3d(3,:)+theta_z)*plane_z)/size(point_3d,2)+ lambda*theta_y;
    gradient_z_x = -2*sum((dx.*(point_3d(1,:)+theta_x)*plane_z)./((point_3d(3,:)+theta_z).^2))/size(point_3d,2);
    gradient_z_y = -2*sum((dy.*(point_3d(2,:)+theta_y)*plane_z)./((point_3d(3,:)+theta_z).^2))/size(point_3d,2);
    gradient_z = gradient_z_x + gradient_z_y+ lambda*theta_z;
end

    