function [Best_rotation, Best_translation, new_loss, point_3d, center_rot] = ...
    Batch_optimize(Best_rotation,Best_translation, ...
    new_loss,point_2d,point_3d,epsilon,center_rot,plane_z,time_tolerance,min_iter)
    % iteratively optimize the rotation and translation
    % input:
    % Best_rotation: Best rotation matrix for now
    % Best_translation: best translation matrix for now
    % time_tolerance: how many time we want the rotation optimization run
    % minute units
    % min_iter: minimum iteration

    n_iter = 0;
    while 1
        n_iter = n_iter +1;
        old_loss = new_loss;
        % rotation search
        [best_r] = RotationSearch(point_2d,point_3d,epsilon,center_rot,plane_z,1, time_tolerance*60);
        R=rotationVectorToMatrix(best_r);
        point_3d=R*(point_3d-center_rot)+center_rot;
        % translation search
        [theta_x, theta_y, theta_z, new_loss]=optimization(point_2d,point_3d,plane_z,1000,0.01);
        point_3d = point_3d + [theta_x;theta_y;theta_z];
        center_rot = center_rot + [theta_x;theta_y;theta_z];
        % update
        Best_rotation = Best_rotation * R;
        Best_translation = Best_translation + [theta_x;theta_y;theta_z];
        new_loss
        % plotting
        close all
        [point_2d_proj] = Project_point(point_3d,plane_z);
        plot(point_2d(1,:), point_2d(2,:),'o')
        hold
        plot(point_2d_proj(1,:), point_2d_proj(2,:),'x')
        %close
        if old_loss - new_loss <10 && n_iter>min_iter
            break
        end
    end