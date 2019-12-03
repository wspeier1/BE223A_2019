function index_2d = close_point(point_2d,project_point_2d)
    % find the closest point for each project points
    index_2d = zeros(1,size(project_point_2d,2));
    for i = 1:size(project_point_2d,2)
        x = point_2d(1,:) - project_point_2d(1,i);
        y = point_2d(2,:) - project_point_2d(2,i);
        l2 = x.^2 + y.^2;
        [~,index_2d(i)] = min(l2);
    end
end
        
