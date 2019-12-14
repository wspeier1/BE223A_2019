# %load headers_files.py
import os
import sys
import pandas as pd
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
import cv2 as cv
from scipy.spatial.transform import Rotation as R
from nilearn.image import resample_img 

from skimage import data, color
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.feature import canny
from skimage.draw import circle_perimeter, circle
from skimage.util import img_as_ubyte
from skimage import feature
from scipy import ndimage as ndi 

from Fluoro_segmentation.circle_mask import circleMask, preprocess_exterior
from Fluoro_segmentation import myfunctions 
#import validate
from Fluoro_segmentation import linear_regression
from Fluoro_segmentation import find_spectral_clusters
from Fluoro_segmentation import cluster_helper

# electrode_detection will take in 2 inputs of raw image's path and 
# return a list of central points for electrodes. 
# input format: (string file_path)
# output type: [(int y,int x)]. 
def electrode_detection1_helper( processed, output_path,
								low_rad=5 , high_rad=35 , interval = 1,
								sigma = 2, low_threshold=20, high_threshold=35):    
    #blur works better for patient 13
	img = cv.medianBlur(processed,5)
    
    # Load picture and detect edges
	edges = canny(img, sigma, low_threshold, high_threshold)
	"""
    edges = canny(img, sigma=2, low_threshold=35, high_threshold=40) # this works well for patient0, best so far 71%
    edges = canny(img, sigma=2, low_threshold=30, high_threshold=40) # attempt2, 4 points
    edges = canny(img, sigma=2, low_threshold=10, high_threshold=50) # attempt3, 7 points for patient 13
    #plot the graph to get a better feeling
	"""
	fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 10))
	ax.imshow(edges, cmap=plt.cm.gray)
	plt.show()
    
    # Detect circles with size of hough_radii 
	hough_radii = np.arange(low_rad,high_rad, 1)   #after optimizations
	"""
	hough_radii = np.arange(5,40, 1)   #works well for patient 0
	"""
	hough_res = hough_circle(edges, hough_radii)
	
    # Select the most prominent 30 circles
    # worked with most of the patients (attempt1)
	accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii, total_num_peaks=45)
	
    # Select the most prominent 60 circles, did not improve much!
    # worked with most of the patients (attempt2),
    #accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii, total_num_peaks=60)
    
    # Select the most prominent 30 circles, did not improve much, too little peak signals
    # worked with most of the patients (attempt2)

	#accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii, total_num_peaks=40)
    #this returns the list of points that are on the perimeters, and change the value to white 
    #for better visualization
	
	fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 10))
	for center_y, center_x, radius in zip(cy, cx, radii):   
		circy, circx = circle_perimeter(center_y, center_x, radius,shape=img.shape)
		img[circy, circx] = 255
	ax.imshow(img, cmap=plt.cm.gray)
	plt.show()
	 
	lst = list(zip(cy,cx))
	cluster_num = 2
	center, labels = find_spectral_clusters.find_spectral_clusters(lst, cluster_num)
	clusters = cluster_helper.extractClusterPoints(labels, lst)           
	
	#changed to input_path, shows the best cluster overlaying on the original image 
	good_cluster, slope_1, intercept_1, best_r_squared_1 = linear_regression.select_cluster(clusters, processed)
	#lst = linear_regression.remove_far_points_from_line(good_cluster, (slope_1, intercept_1) , 30)
    #linear_regression.draw_electrodes(lst, slope_1,intercept_1,patient_path)
	#lst = filterRange(lst, 400, 800, 120,480)
	print("good cluster: \n",good_cluster)
	np.save(output_path, good_cluster)
	return good_cluster

def electrode_detection(input_path, output_path):
	img = cv.imread(input_path, 0)
	#recommend preprocessing 
	#print("shape of img ", img.shape)
	#preprocess img to remove patient information 
	img = preprocess_exterior(img)
	
	good_cluster = electrode_detection1_helper(img, output_path)
	
	implot = plt.imshow(img)
	# put a blue dot at (10, 20)
	plt.scatter([10], [20])
	# put a red dot, size 40, at 2 locations:
	plt.scatter(good_cluster[:,1], good_cluster[:,0], c='r', s=30)
	plt.show()
	
	return good_cluster
	
	
	#return electrode_detection2_helper(img, output_path)
	#return electrode_detection3_helper(img, output_path)
	
	
	
	
