function [theta_x, theta_y, theta_z, loss] = optimization( point_2d, ...
    point_3d, plane_z, epoch, learning_rate)
    % optimization for  translation 
    % epoch: number of iteration 
    
    theta_x=rand(1,1);
    theta_y=rand(1,1);
    theta_z=rand(1,1);
    for e = 1:epoch
        project_point_2d = Project_point((point_3d+[theta_x; theta_y;theta_z]),plane_z);
        index_2d = close_point(point_2d,project_point_2d);
        [gradient_x, gradient_y, gradient_z] = gradient(point_2d , project_point_2d, point_3d,theta_x,theta_y, theta_z, plane_z, index_2d);
        theta_x = theta_x - learning_rate*gradient_x;
        theta_y = theta_y - learning_rate*gradient_y;
        theta_z = theta_z - learning_rate*gradient_z;
        loss = floss(point_2d,project_point_2d, index_2d);
            %if isnan(theta_x)
            %    break
            %end
        %loss;
    end
end
