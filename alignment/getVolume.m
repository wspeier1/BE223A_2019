function [V] = getVolume(branch)
%GETVOLUME calculate remaining volume
%
%   branch��input branches
%   V��Volume


k=branch(4:6,:)-branch(1:3,:);
V=sum(k(1,:).*k(2,:).*k(3,:));


end

