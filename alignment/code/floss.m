function loss = floss(point_2d,project_point_2d, lambda, theta_x, theta_y, theta_z, index_2d)
    % calculate the loss
    % distance for the closet point
    loss = 0;
    for i = 1:size(project_point_2d,2)
        x= sum((point_2d(1,index_2d)-project_point_2d(1,:)).^2);
        y= sum((point_2d(2,index_2d)-project_point_2d(2,:)).^2);
        loss = x+y;
    end
    loss = loss/size(project_point_2d,2);
    loss = loss + 1/2*lambda*(theta_x^2+theta_y^2+theta_z^2);
end

            