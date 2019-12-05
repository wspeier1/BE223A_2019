function loss = floss(point_2d,project_point_2d, index_2d)
    % calculate the loss based on
    % distance for the closet point of each point in point_2d
    % index_2d: index of corresponding cloest point in Project_point_2d
    % 
    loss = 0;
    for i = 1:size(point_2d,2)
        x= sum((point_2d(1,:)-project_point_2d(1,index_2d)).^2);
        y= sum((point_2d(2,:)-project_point_2d(2,index_2d)).^2);
        loss = x+y;
    end
    loss = loss/size(point_2d,2);
    %loss = loss + 1/2*lambda*(theta_x^2+theta_y^2+theta_z^2);
end

            