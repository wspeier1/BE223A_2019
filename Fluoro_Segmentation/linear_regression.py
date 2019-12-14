# input is 2 clusters of electrodes, in np.array format
# function does linear regression on both clusters
# output are coefficients for y = ax+b, and R^2

import cv2
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
import math
# this line calls function linear_regression, user should change input
# input is of type np.array

#input_cluster_1 = np.array([(149, 470),(134, 528),(122, 586),(128,642),(125, 706),(129,768),(128,821),(140,877)])
#linear_regression(input_cluster_1)
# this line calls input image, user should change input
#image_file_path = "/Users/Jenny/Desktop/BE 223A/github /data/fluorscopies/DBS_bG17.tif"



#*****************************************************************************************
degree = 1
cluster_1_color = 'blue'
# cluster_2_color = 'red'

# plot points & draw line
def draw_electrodes(cluster_1, slope_1, intercept_1, processed):
	image = processed
	#plt.imshow(image)
	plt.plot(image)

	for point in cluster_1:
		y1 = point[0]
		x1 = point[1]
		plt.scatter(x1, y1, s = 5, c = cluster_1_color)
		
	x_array = np.arange(0,1200,1)
	plot_y_1 = slope_1*(x_array) + intercept_1
	plt.plot(x_array, plot_y_1, cluster_1_color)
	"""
	plt.xlim(0,1280)
	plt.ylim(1024,0)
	"""
	plt.show()
	

#slope_1, intercept_1, r_value_1, p_value_1, std_err_1 = scipy.stats.linregress(x1, y1)
#r_squared_1 = r_value_1**2
#input_cluster = [(y,x)]
#image = path of .npy files
def linear_regression(input_cluster, image):
	y1 = input_cluster[:,0]
	x1 = input_cluster[:,1]
	slope_1, intercept_1, r_value_1, p_value_1, std_err_1 = scipy.stats.linregress(x1, y1)
	
	r_squared_1 = r_value_1**2
	print("slope is ", slope_1)
	print("intercept is ", intercept_1)
	print("r squared is ", r_squared_1)
    
	#draw_electrodes(input_cluster, slope_1, intercept_1, image) # <<<----------- comment out this line if you don't want the plot
	return slope_1, intercept_1, r_squared_1

#line is given in (a,b,c) where ax+by+c= 0
def mindist_pt_to_line(pt , line):
    (x0, y0) = pt
    (a,b,c) = line
    # closest coordinate on the line to pt 
    #x = ((b*((b*x0)-(a*y0)))-(a*c))/(a**2 + b**2)
    #y = ((a*(((-1)*b*x0)+(a*y0)))-(b*c))/(a**2 + b**2)
    #print("closest pt on line = ", (x,y))
    min_distance = abs(a*x0 + b*y0 + c)/math.sqrt(a**2 + b**2)
    return min_distance

#remove_far_points_from_line takes 3 arguments, list of points (y,x), line = (a,b) where y = ax + b, d distance of pt away from line
#it will return list of pts that has a maximum distance d away from line
def remove_far_points_from_line(lst, line ,d ):
	filter = []
	(a,b) = line #where y = ax + b
	formated_line = (a, -1, b) #where formated line is represented as ax + yb + c = 0
	for pts in lst:
		(y,x) = pts
		if (mindist_pt_to_line((x,y),formated_line) <= d ) :
			filter.append(pts)
	filter = np.array(filter)
	return filter


#this selects the best cluster out of all the cluster using regression
def select_cluster(clusters, image):
	max_rsquared = 0 
	best_cluster = []
	best_slope = 0
	best_intercept = 0
	for cluster in clusters:
		slope, intercept, r_squared = linear_regression(cluster, image)
		#filter this cluster out
		if (len(cluster) > 3):
			print("r_squared : ", r_squared)
			if r_squared > max_rsquared:
				best_cluster = cluster
				max_rsquared = r_squared 
				best_slope = slope
				best_intercept = intercept
	#draw_electrodes(best_cluster, best_slope, best_intercept, image)
	return best_cluster, best_slope, best_intercept, max_rsquared  
