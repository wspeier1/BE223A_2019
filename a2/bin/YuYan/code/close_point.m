function index_2d = close_point(point_2d,project_point_2d)
    % find the closest point in project_point_2d for each point in point_2d
    index_2d = zeros(1,size(point_2d,2));
    for i = 1:size(point_2d,2)
        x = point_2d(1,i) - project_point_2d(1,:);
        y = point_2d(2,i) - project_point_2d(2,:);
        l2 = x.^2 + y.^2;
        [~,index_2d(i)] = min(l2);
    end
end
        
