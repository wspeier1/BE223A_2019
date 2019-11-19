function [theta_x, theta_y, theta_z] = optimization( point_2d,  point_3d, plane_z, epoch, learning_rate, batch_size)
    % optimization given point_2d and rotated point_3d
    theta_x=rand(1,1);
    theta_y=rand(1,1);
    theta_z=rand(1,1);
    b = fix(size(point_2d,2)/batch_size);
    for e = 1:epoch
        for i = 1:b
            project_point_2d = Project_point(point_3d+[theta_x; theta_y;theta_z],plane_z);
            loss = floss(point_2d,project_point_2d,0.1, theta_x, theta_y, theta_z);
            point_2d_one = point_2d(:,((b-1)*batch_size+1):(b*batch_size));
            [gradient_x, gradient_y, gradient_z] = gradient(point_2d_one , project_point_2d, point_3d,theta_x,theta_y, theta_z, plane_z,0.1);
            theta_x = theta_x - learning_rate*gradient_x;
            theta_y = theta_y - learning_rate*gradient_y;
            theta_z = theta_z - learning_rate*gradient_z;
            %if isnan(theta_x)
            %    break
            %end
        end
        if mod(size(point_2d,2), batch_size)~=0
            project_point_2d = Project_point(point_3d+[theta_x; theta_y;theta_z],plane_z);
            loss = floss(point_2d,project_point_2d,0.1, theta_x, theta_y, theta_z);
            [gradient_x, gradient_y, gradient_z] = gradient( point_2d(:,(b*batch_size+1):size(point_2d,2)), project_point_2d, point_3d,theta_x,theta_y, theta_z, plane_z,0.1);
            theta_x = theta_x - learning_rate*gradient_x;
            theta_y = theta_y - learning_rate*gradient_y;
            theta_z = theta_z - learning_rate*gradient_z;
        end
        loss
    end
end
            
