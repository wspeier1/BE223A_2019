function [best_TransVec, best_dis, best_distance, best_data_out] = icp_dist(point_3d,point_2d,plane_z,s, search_range)
    % point_3d: 3d point set to be register for translation
    % point_2d: 2d point set
    % plane_z: value indicate the position of plane on z-axis
    % s: initial search distance 
    % search_range: range of search
    [project_point_2d] = Project_point(point_3d,plane_z);
    temp_point_3d = point_3d;
    [~,best_TransVec,best_data_out, best_dis]=icp(point_2d,project_point_2d);
    best_distance = 0;
    for distance = s-search_range:(2*search_range/1000):s+search_range
        temp_point_3d(3,:)=point_3d(3,:)+distance;
        [project_point_2d] = Project_point(temp_point_3d,plane_z);
        [~,TransVec,data_out, dis]=icp(point_2d,project_point_2d);
        if dis<best_dis
            best_dis=dis;
            best_TransVec=TransVec;
            best_distance=distance;
            best_data_out = data_out;
        end
    end
end


% testing 
%scatter(point_2d(1,:), point_2d(2,:), repmat([10],1, 10),repmat([1],1, 10))
%hold
%scatter(project_point_2d(1,:)+best_TransVec(1,1), project_point_2d(2,:)+best_TransVec(2,1), repmat([10],1, 10),repmat([2],1, 10))
