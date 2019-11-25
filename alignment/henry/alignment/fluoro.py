# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 18:18:31 2019

@author: hwz62
"""

# this notebook was written for beta testing on Wednesday Novemebr 20th.
# on subject_1c.tif
# required packages are cv2, numpy, matplotlib.pyplot
# input is fluoroscopy image in .tif format (note .jpg format doesn't work)

# this is the only parameter that needs to be changed! output is a text file
# containing coordinates of DBS lead as a straight line
# input_image = "/Users/Jenny/beta testing/fluoro_subject_1c.tif"
input_image = "C:/Users/hwz62/Desktop/alignment/fluoro_subject_5.tif"

import cv2 
import numpy as np 
import matplotlib.pyplot as plt

# ******************************************************************************
# step 1 find frame, terminal end of DBS lead is always near the center of
# this circular frame
  
# Read image. 
img_c = cv2.imread(input_image, cv2.IMREAD_COLOR) 
  
# Convert to grayscale. 
gray = cv2.cvtColor(img_c, cv2.COLOR_BGR2GRAY) 
  
# Blur using 3 * 3 kernel. 
gray_blurred = cv2.blur(gray, (3, 3)) 

# fluoroscopy images are not all the same size
# circles' radiuses are between 8% - 22% of image size (on the x-axis)
# subject1 is 755 x 947, most other subjects are 1024 x 1280

# find image size on the x-axis axis
one_ar_3d = np.asarray(img_c) # this is 3D array
one_arr = one_ar_3d[:,:,:0]
horizontal_size = np.shape(one_arr)[1]
min_radius = int(horizontal_size * 0.08)
max_radius = int(horizontal_size * 0.22)

# Apply Hough transform on the blurred image. 
detected_circles = cv2.HoughCircles(gray_blurred,  
                   cv2.HOUGH_GRADIENT, 1, 30, param1 = 50, 
               param2 = 40, minRadius = min_radius, maxRadius = max_radius) 
# min radius is 80, max radius is 150

# total number of circles found:
num_circles = (np.shape(detected_circles))[1]

# function subject_num extracts subject number, 
# input is .tif file pathname, output is subject number as 2 digits:
def subject_num (filepath):
   # this is last 2 characters before '.tif':
   last_two = (filepath.split("."))[0][-2:]
   if last_two[0] == '_':
      return last_two[1]
   else:
      return last_two

current_subject = subject_num(input_image)

# save this detected_circles, output as a text file
circle_out_path = "C:/Users/hwz62/Desktop/alignment/all_circles_" + str(current_subject) +".txt"
circle_pic = "C:/Users/hwz62/Desktop/alignment/detected circles " + str(current_subject) + ".tif"
output = open(circle_out_path,'w')
output.write("total number of circles found: ")
output.write(str(num_circles))
output.write('\n')
output.write('each row contains: x, y ,radius\n')
output.writelines(str(detected_circles))
output.close()

# draw circles that are detected:
list_of_centers = []

def drawing_circles (input_array):
   if input_array is not None:
        
        # convert the circle parameters a, b and r to integers.
        input_array = np.uint16(np.around(input_array))
        
        for point in input_array[0, :]:
            a, b, r = point[0], point[1], point[2]
            
            # a, b is the coorindate of center, append to list_of_centers
            center_x = a
            center_y = b
            # print("center of the circle is:", center_x, center_y)
            list_of_centers.append([center_x, center_y])
            
            # Draw the circumference of the circle.
            cv2.circle(img_c, (a, b), r, (0, 255, 0), 2)
            
            # Draw a small circle (of radius 1) to show the center.
            cv2.circle(img_c, (a, b), 1, (0, 0, 255), 3)
            # cv2.imshow("Detected Circle", img_c)
            # cv2.waitKey(0)
   cv2.imwrite(circle_pic,img_c)

drawing_circles(detected_circles)

# list_of_centers is a list
# return the first of the list because it has the largest accumulator value
center_of_frame = detected_circles[0][0]

# center_of_frame outputs [687.5 441.5 137.8] for subject_1c.tif, 
# which is x coordinate, y coordinate, and radius of center of the circle

print("total number of circles found: ", num_circles)
print("frame is located at: (x,y,radius)", center_of_frame)

# ******************************************************************************
# step 2 line detection
# out of all straight lines detected, 2 additional parameters are used to
# narrow down DBS lead: first vertical line of slope >= 2.5; second
# end point is near the center of the fram

img_l = cv2.imread(input_image) 
  
# Convert the img_l to grayscale 
gray = cv2.cvtColor(img_l,cv2.COLOR_BGR2GRAY) 
  
# Apply edge detection method on the image 
edges = cv2.Canny(gray,80,150,apertureSize = 3) 
# cv2.imwrite("/Users/Jenny/edges-80-150.jpg",edges)
# edges is a numpy.ndarray of original image size, (mask)

lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, maxLineGap=50)

lines_out_path = "/Users/Jenny/beta testing/lines_" + str(current_subject) +".jpg"

for line in lines:
   x1, y1, x2, y2 = line[0]
   cv2.line(img_l, (x1, y1), (x2, y2), (0, 0, 128), 2)
cv2.imwrite(lines_out_path, img_l)

# find only vertical lines
vertical_lines = []
for line in lines:
    x1 = (line[0])[0]
    y1 = (line[0])[1]
    x2 = (line[0])[2]
    y2 = (line[0])[3]
    
    # not perfectly vertical, avoid division by 0, (most likely left border)
    if x1 != x2: 
       
        slope = (y2-y1)/(x2-x1) # equation to calculate slope
        
        # fairly vertical line (slope >=2.5, exclude horizontal lines:
        if slope != 0 and (abs(slope)) >= 2.5: 
            vertical_lines.append(line) # add this line to filtered list
            
# find point closeset to center of circle
# receive center point of circle from circle-finding detection
circle_center_x = int(center_of_frame[0]) # 687
circle_center_y = int(center_of_frame[1]) # 441
circle_center = [circle_center_x, circle_center_y]
# circle_center = [687,441]

# define calculate_distance function, accepts 4 parameters, point_x and
# point_y are x and y coordinates of the given point, center_x and center_y
# are x and y coordinates of the center of the circle. Function returns 
# the cartesian distance between these two points
import math

def calculate_distance(point_x,point_y,center_x,center_y):
    distance = math.sqrt((point_x - center_x)**2 + (point_y - center_y)**2)
    return distance
 
# function list_distance accepts 2 parameters, list of lines (lol), 
# where each element contains 4 numbers: x, y cooridinates of two end points,
# and x,y cooridinate of center of the circle (center), 
# function returns a new list where the second element is the distance
# of the closest point to the center of the circle
def list_distances (lol, center):
    distances = []
    circle_x = center[0]
    circle_y = center[1]
    
    # loop over every line in lol
    for line in lol:
        point_a_x = line[0][0]
        point_a_y = line[0][1]
        point_b_x = line[0][2]
        point_b_y = line[0][3]
        
        # pass to helper function, accept shortest distance
        dist1 = calculate_distance(point_a_x, point_a_y, circle_x, circle_y)
        dist2 = calculate_distance(point_b_x, point_b_y, circle_x, circle_y)
        shortest = min(dist1,dist2)
        distances.append([line,shortest])
        
        # sort lines by their distance in ascending order
        distances.sort(key = lambda x: x[1])
    
    # this is list of x,y coordinates
    return distances[0][0]

# function to find DBS lead coordinates
DBS_lead = list_distances(vertical_lines,circle_center) 

# draw line onto image with numpy array function

# convert list into numpy array
vertical_array = np.asarray(DBS_lead)
# need to output this
print("DBS lead 2 ends points are at: ", vertical_array)

filtered_lines_out = "C:/Users/hwz62/Desktop/alignment/filtered_lines_" + str(current_subject) +".jpg"

a,b = vertical_array.shape
for i in range (a):
    cv2.line(gray, (vertical_array[i][0], vertical_array [i][1]),
            (vertical_array[i][2], vertical_array[i][3]), (0, 0, 255), 3, cv2.LINE_AA)
    cv2.imwrite(filtered_lines_out, gray)
    
# ******************************************************************************

# step 3 fill in line pixels between 2 end points

# vertical_array output is [[x1,y1,x2,y2]]
x1 = vertical_array[0][0]
y1 = vertical_array[0][1]
x2 = vertical_array[0][2]
y2 = vertical_array[0][3]

# equation of a straight line is y = mx + b
m = (y2 - y1) / (x2 - x1)
b = y1 - m * x1

image = cv2.imread(input_image)
plt.imshow(image)

DBS_lead_out = "C:/Users/hwz62/Desktop/alignment/DBS_lead_" + str(current_subject) +".txt"
line_output = open(DBS_lead_out, 'w')

# function fill_in_pixels 
def fill_in_pixels (x1,x2):
    for i in range(x1, x2+1):
        calc_y = int(m*i + b)
        coordinate = [i,calc_y]
        
        # write output to file
        line_output.write(str(coordinate))
        line_output.write('\n')
        
        # plot on image
        plt.scatter(i,calc_y, color = 'r')
    plt.show()

fill_in_pixels(x1,x2) 

line_output.close()
# output file is line_pixels_2.txt
# this is x-y coordinate of DBS lead
