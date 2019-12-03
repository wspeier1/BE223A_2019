function [theta_x, theta_y, theta_z] = optimization( point_2d,  point_3d, plane_z, epoch, learning_rate, batch_size)
    % optimization given point_2d and rotated point_3d
    % sample call:
    % [theta_x, theta_y, theta_z] = optimization( subfluoro,  subct, -60, 5000, 0.01, 1)
    theta_x=rand(1,1);
    theta_y=rand(1,1);
    theta_z=rand(1,1);
    for e = 1:epoch
        project_point_2d = Project_point(point_3d+[theta_x; theta_y;theta_z],plane_z);
        index_2d = close_point(point_2d,project_point_2d);
        loss = floss(point_2d,project_point_2d,0.1, theta_x, theta_y, theta_z, index_2d);
        [gradient_x, gradient_y, gradient_z] = gradient(point_2d , project_point_2d, point_3d,theta_x,theta_y, theta_z, plane_z,0.1, index_2d);
        theta_x = theta_x - learning_rate*gradient_x;
        theta_y = theta_y - learning_rate*gradient_y;
        theta_z = theta_z - learning_rate*gradient_z;
            %if isnan(theta_x)
            %    break
            %end
        loss
    end
end
