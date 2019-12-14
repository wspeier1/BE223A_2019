# required packages are cv2, numpy, matplotlib.pyplot
# input is fluoroscopy image in .tif format (note .jpg format doesn't work)

import cv2 
import numpy as np 
import matplotlib.pyplot as plt
import math

# input needs to be a list of of filepaths, output will save to the according folder
input_images = ["/Users/Jenny/final testing/fluoro_subject_1c/fluoro_subject_1c.tif",
                "/Users/Jenny/final testing/fluoro_subject_2/fluoro_subject_2.tif",
                "/Users/Jenny/final testing/fluoro_subject_3/fluoro_subject_3.tif",
                "/Users/Jenny/final testing/fluoro_subject_4/fluoro_subject_4.tif",
                "/Users/Jenny/final testing/fluoro_subject_5/fluoro_subject_5.tif",
                "/Users/Jenny/final testing/DBS_bG02/DBS_bG02.tif",
                "/Users/Jenny/final testing/DBS_bG03/DBS_bG03.tif",
                "/Users/Jenny/final testing/DBS_bG06/DBS_bG06.tif",
                "/Users/Jenny/final testing/DBS_bG09/DBS_bG09.tif",
                "/Users/Jenny/final testing/DBS_bG10/DBS_bG10.tif",
                "/Users/Jenny/final testing/DBS_bG12/DBS_bG12.tif",
                "/Users/Jenny/final testing/DBS_bG13/DBS_bG13.tif",
                "/Users/Jenny/final testing/DBS_bG17/DBS_bG17.tif",
                "/Users/Jenny/final testing/DBS_bG18/DBS_bG18.tif",
                "/Users/Jenny/final testing/DBS_bG19/DBS_bG19.tif"]

# input is a list of input images, each element is a filepath
def fluoro_DBS (tif_images):
   for subject in tif_images:
      input_image = subject
      
      folder_name = "/".join((input_image).split("/")[:-1])
      output_path = folder_name + '/'
      
      # step 1 detect center of stereotactic frame
      center_of_frame = detect_circle(subject)
      print("center of frame is at ", center_of_frame)
      
      # step 2 detect vertical long lines as candidates
      DBS_lead, candidates = vertical_long_lines(subject, output_path,center_of_frame)
      other_half = on_same_line(DBS_lead, candidates)
      print("bottom half is ", DBS_lead)
      print("candidates are ", candidates)
      print("other half is ", other_half)
      
      # step 3 find two halves of DBS lead
      final_points = check_top_half(DBS_lead, other_half, center_of_frame)
      print("in fluoro, DBS lead is located at", final_points, "(x1,y1,x2,y2)")
      
      # step 4 connect them & output
      draw_lead_on_image(final_points,input_image, output_path)
      x1 = final_points[0][0][0]
      y1 = final_points[0][0][1]
      x2 = final_points[0][0][2]
      y2 = final_points[0][0][3]
      fill_in_pixels(x1,x2,y1,y2,output_path) 
      

# ******************************************************************************
# step 1 find frame, terminal end of DBS lead is always near the center of
# this circular frame

def detect_circle(input_fluoro):
   # Read image. 
   img_c = cv2.imread(input_fluoro, cv2.IMREAD_COLOR) 
   
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
   # min radius is ~80, max radius is ~150
   
   # filter to only circles in a certain region
   filtered_circles = list(filter(lambda x: x[0] >= 500 and x[0] <= 1100
                                  and x[1] >= 400 and x[1] <= 1000, detected_circles[0]))
   
   return filtered_circles[0]

# ******************************************************************************
# step 2 line detection
# out of all straight lines detected, 2 additional parameters are used to
# narrow down DBS lead: first vertical line of slope >= 1.5; second
# end point is near the center of the fram

def vertical_long_lines (input_fluoro, output_path, center_of_frame):
   img_l = cv2.imread(input_fluoro) 
   # Convert the img_l to grayscale 
   gray = cv2.cvtColor(img_l,cv2.COLOR_BGR2GRAY) 
  
   # Apply edge detection method on the image, output binary image
   edges = cv2.Canny(gray,80,150,apertureSize = 3) 
   # edges is a numpy.ndarray of original image size

   lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, maxLineGap=50)

   # filter 1/3: find only vertical lines
   vertical_lines = []
   for line in lines:
      x1 = (line[0])[0]
      y1 = (line[0])[1]
      x2 = (line[0])[2]
      y2 = (line[0])[3]
    
      # not perfectly vertical, avoid division by 0, (most likely left border)
      if x1 != x2: 
      
         slope = (y2-y1)/(x2-x1) # equation to calculate slope
        
         # fairly vertical line (slope >=1.5, exclude horizontal lines:
         if slope != 0 and (abs(slope)) >= 1.5: 
            vertical_lines.append(line) # add this line to filtered list
            vertical_array = np.asarray(vertical_lines)
            
   # filter 2/3: find point closest to center of circle
   # receive center point of circle from circle-finding detection
   circle_center_x = int(center_of_frame[0])
   circle_center_y = int(center_of_frame[1])
   circle_center = [circle_center_x, circle_center_y]
   
   # function to find DBS lead coordinates
   DBS_lead = list_distances(vertical_lines,circle_center)
   
   # filter 3/3: find line with similar slope
   # convert list into numpy array
   other_half = on_same_line(DBS_lead, vertical_lines)
   
   return DBS_lead, other_half
   
def on_same_line (half_DBS, all_lines):
   top_half = []
   std_x1 = half_DBS[0][0]
   std_y1 = half_DBS[0][1]
   std_x2 = half_DBS[0][2]
   std_y2 = half_DBS[0][3]
   DBS_slope = (std_y2 - std_y1) / (std_x2 - std_x1)
   DBS_y_int = std_y1 - DBS_slope * std_x1
       
   for line in all_lines:
      x1 = line[0][0]
      y1 = line[0][1]
      x2 = line[0][2]
      y2 = line[0][3]
      
      # if this line is highly similar to standard, eliminate this
      # because it's the same segment
      if not ((abs (x1-std_x1)) < 17 and (abs (x2-std_x2)) < 17 and
              (abs (y1-std_y1)) < 17 and (abs (x2-std_x2)) < 17):     
         
         # given x1, and x2, predict y1, and y2 on the same line
         calc_y1 = DBS_slope * x1 + DBS_y_int
         calc_y2 = DBS_slope * x2 + DBS_y_int
         
         # if given line is close to predicted line, then append this to list
         if ((abs (calc_y1 - y1)) <= 20) and ((abs (calc_y2 - y2)) <= 20):
            top_half.append(line)
               
   return np.asarray(top_half)
   
# define calculate_distance function, accepts 4 parameters, point_x and
# point_y are x and y coordinates of the given point, center_x and center_y
# are x and y coordinates of the center of the circle. Function returns 
# the cartesian distance between these two points
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



# *****************************************************************************

# Step 3 examine the output of bottom half, and top half, separated by 
# circular frame

# function check_top_half examines the output of these 4 filters, there are 3 possible scenarios:
# scenario 1: length of top_half is 1, then only found original input bottom half, can't find top half.
# there are two scenarios in this case,
# A. if line is too far away from center of circle, then just extend to the center of the circle
# B. if line is too short, (only found the bottom half), then extend to certain length

# scenario 2: length of top half is more than 2, then found the top portion of DBS lead, simply connect
# this top portion with bottom portion

def predict_other_root(x1,y1,x2,y2):
   # equation of a straight line is y = mx + b
   m = (y2 - y1) / (x2 - x1)
   b = y1 - m * x1   
   
   dy = lambda distance, m: m*dx(distance,m)
   dx = lambda distance, m: math.sqrt(distance/(m**2+1))
    
   distance = 480**2
   point_b = (x1+dx(distance,m), y1+dy(distance,m))
    
   calc_x = int(point_b[0])
   calc_y = int(point_b[1])
    
   return [[[x1, y1, calc_x, calc_y]]]
 
def check_top_half (bottom, top_list, circle_center):
   length = len(top_list)
    
   std_x1 = bottom[0][0]
   std_y1 = bottom[0][1]
   std_x2 = bottom[0][2]
   std_y2 = bottom[0][3]
   circle_x = circle_center[0]
   circle_y = circle_center[1]
    
   # scenario 1: only found original input, can't find the other half
   if length == 1:
      x1 = top_list[0][0][0]
      y1 = top_list[0][0][1]
      x2 = top_list[0][0][2]
      y2 = top_list[0][0][3]
      
      # option A: line is too far away from center of the circle, then extend to the center
      if calculate_distance(x1,y1,circle_x,circle_y) > 150: 
         return [[[circle_x, circle_y, x2, y2]]]
      
      # option B: line is close to center of circle, but too short, extend to length 480
      # from the bottom point (center of the circle)
      else:
         print("x1 is ", x1)
         print("y1 is ", y1)
         print("x2 is ", x2)
         print("y2 is ", y2)
         return predict_other_root(x1,y1,x2,y2)
      
   # scenario 2: length of top half bigger 2, found the other half of DBS lead,
   elif length >= 2:
      # then connect the top portion with bottom portion
      x1 = bottom[0][0]
      y1 = bottom[0][1]
      x2 = top_list[0][0][2]
      y2 = top_list[0][0][3]
      return [[[x1,y1,x2,y2]]]
   
   # scenario 3: length of top half is 0, couldn't find the other half of DBS lead,
   elif length == 0:
      # then extend the bottom half toward the skull, until length is 480
      return predict_other_root(std_x1,std_y1,std_x2,std_y2)   
    
# ******************************************************************************

# step 4 fill in line pixels between 2 end points

def draw_lead_on_image(endpoints, original, output_path):
   final_out_path = output_path + "DBS_leads_fluoro" + ".jpg"
   # draw final DBS_lead
   original_image = cv2.imread(original,cv2.IMREAD_COLOR)
   cv2.line(original_image, (endpoints[0][0][0], endpoints[0][0][1]),
            (endpoints[0][0][2], endpoints[0][0][3]), (0, 0, 255), 3, cv2.LINE_AA)
   cv2.imwrite(final_out_path, original_image)

# function fill_in_pixels 
def fill_in_pixels (x1,x2,y1,y2,output_path):
   DBS_lead_out = output_path + "DBS_lead_fluoro" +".txt"
   line_output = open(DBS_lead_out, 'w')   
   # equation of a straight line is y = mx + b
   m = (y2 - y1) / (x2 - x1)
   b = y1 - m * x1   
   
   for i in range(int(x1), int(x2+1)):
      calc_y = int(m*i + b)
      coordinate = [i,calc_y]
      
      # write output to file
      line_output.write(str(coordinate))
      line_output.write('\n')
      
   line_output.close()

fluoro_DBS(input_images)