function loss = floss(point_2d,project_point_2d, lambda, theta_x, theta_y, theta_z)
    % calculate the loss
    % brute distance, calculate distance from all pairwise point
    loss = 0;
    for i = 1:size(point_2d,2)
        for j = 1:size(project_point_2d,2)
            loss= loss + sum((point_2d(:,i)-project_point_2d(:,j)).^2);
        end
    end
    loss = loss/size(point_2d,2)/size(project_point_2d,2);
    loss = loss + 1/2*lambda*(theta_x^2+theta_y^2+theta_z^2);
end

            