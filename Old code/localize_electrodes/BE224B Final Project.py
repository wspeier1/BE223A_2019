# -*- coding: utf-8 -*-
"""
BE 224B Final Project
Name: Yannan Lin
"""

import cv2
import math
import numpy as np
import nibabel as nib
from PIL import Image
from mayavi import mlab
import matplotlib.pyplot as plt

################ define functions ########################
# roate image
def rotate(img, angle):
    """
    Function to rotate an image
    
    input: img, angle
    output: dst
    
    This function takes in two input parameters: an image
    and the angle (integer) and outputs a rotated image
    by the specifed angle.
    
    """
    rows,cols = img.shape
    M = cv2.getRotationMatrix2D((cols/2,rows/2),angle,1)
    dst = cv2.warpAffine(img,M,(cols,rows))
    return dst 

# enable picker on a mayavi object to find coordinates
def picker_callback(picker_obj):
    """
    Function to enable picker on a mayavi object
    
    input: picker_obj
    output: print out coordinates of the point picked by 
    a mouse
    
    A mayavi object needs to be defined before running
    this function. Once the object is displayed in the
    mayavi scene, the console will output the coordinates
    of point from the mouse click on the mayavi scene. 
    
    """
    print(picker_obj.get("pick_position"))
    
# calcualte distance between two 3d points
def PointDistance(x1, y1, z1, x2, y2, z2):  
    """
    Function to calculate distance between two 3d points
    
    input: x1, y1, z1, x2, y2, z2
    output: point_dis
    
    This function takes in the coordinates of two 3d points
    sequentially and calculates the distance between these
    two points.
    
    """
    point_dis = math.sqrt(math.pow(x2 - x1, 2) +
                math.pow(y2 - y1, 2) +
                math.pow(z2 - z1, 2)* 1.0) 
    return point_dis

# get cooridnates of all points on hull
def points_hull(hull_data):
    """
    Function to find coordinates of all points on a hull
    
    input: hull_data
    output: coord_list
    
    This function returns a list of coordinates of all the 
    points on the input hull data.
    
    """
    coord_list = []
    for x in range(hull_data.shape[0]):
        for y in range(hull_data.shape[1]):
            for z in range(hull_data.shape[2]):    
                if hull_data[x,y,z] > 0:
                    coord_list.append([x,y,z])
    return coord_list

# reshape electrode_coord_list
def reshape_electrode_coord_list(electrode_x,electrode_y,electrode_z):
    """
    Function to reshape the electrode coordinates list
    
    input: electrode_x,electrode_y,electrode_z
    output: electrode_coord_list
    
    This function works to reshape the electrode coordinates list
    into the following format: [[x1,y1,z1], [x2,y2,z2]....].
        
    """
    electrode_coord_list = []
    for i in range(len(electrode_x)):
        electrode_coord_list.append([electrode_x[i],electrode_y[i],electrode_z[i]])
    return electrode_coord_list

# get electrode coordiantes in 3d space method 1
def get_electrode_coord(electrode_coord_list, coord_list):
    """
    Function to get the coordinates of the point on the hull 
    that has the shorest distance to the electrode on the 
    2d fluoroscopic image
    
    input: electrode_coord_list, coord_lis
    output: min_coord_list
    
    Electrode_coord_list is a list of coordinates of the 
    electrode on the fluoroscopic image. Coord_list is a 
    list of coordinates of all the points on a hull.
    For each set of electrode cooridnates in the 
    electrode_coord_list, the point on the hull that has
    the shorest distance to the electrode will be returned
    and saved in the min_coord_list.
    
    """
    min_list = [] #coordiantes of the nearest point on surface to each electrode
    min_coord_list = []
    for a in range(len(electrode_coord_list)):
        min_dist = 100000 #reset min_dist to 100000
        for i in range(len(coord_list)):
            dis = PointDistance(coord_list[i][0], 
                                      coord_list[i][1], 
                                      coord_list[i][2], 
                                      electrode_coord_list[a][0],
                                      electrode_coord_list[a][1],
                                      electrode_coord_list[a][2])
            
            #get the coordiante of the nearest point on the surface to each electrode
            if dis < min_dist:
                min_dist = dis
                min_list = [coord_list[i][0], coord_list[i][1], coord_list[i][2]]   
        min_coord_list.append(min_list)
    return min_coord_list

#  get electrode coordiantes in 3d space method 2
def get_electrode_coord_2(electrode_coord_list,coord_list):
    """
    Function to get the coordinates of 2d points on the 3d surface
    
    input: electrode_coord_list,coord_list
    output: projected_coord_list
    
    Electrode_coord_list is a list of coordinates of the 
    electrode on the fluoroscopic image. Coord_list is a 
    list of coordinates of all the points on a hull.
    For each set of electrode cooridnates in the 
    electrode_coord_list, a ray perpendicular to the fluoroscopy
    will be generated and the intersection of the ray with the
    hull surface will be saved into the projected_coord_list.
        
    """
    projected_coord_list = []
    
    for i in range(len(electrode_coord_list)):
        electrode_coord = electrode_coord_list[i]
    
        ray_point_list = []
        start_point = electrode_coord
        for i in range(256):
            ray_point_list.append([start_point[0], start_point[1], i])
            
        for i in range(len(ray_point_list)):
            if ray_point_list[i] in coord_list:
                projected_coord_list.append(ray_point_list[i])
                break #only pick the first intersection point 
                
    return projected_coord_list
    
######################### load data ################################
hull_1 = nib.load('/Users/apple/Desktop/data/subject1/hull_subject_1.nii')
hull_2 = nib.load('/Users/apple/Desktop/data/subject2/hull_subject_2.nii')
hull_3 = nib.load('/Users/apple/Desktop/data/subject3/hull_subject_3.nii')
hull_4 = nib.load('/Users/apple/Desktop/data/subject4/hull_subject_4.nii')
hull_5 = nib.load('/Users/apple/Desktop/data/subject5/hull_subject_5.nii')
hull_data_1 = np.array(hull_1.get_fdata())
hull_data_2 = np.array(hull_2.get_fdata())
hull_data_3 = np.array(hull_3.get_fdata())
hull_data_4 = np.array(hull_4.get_fdata())
hull_data_5 = np.array(hull_5.get_fdata())

postct_1 = nib.load('/Users/apple/Desktop/data/subject1/postopCT_subject_1.nii')
postct_2 = nib.load('/Users/apple/Desktop/data/subject2/postopCT_subject_2.nii')
postct_3 = nib.load('/Users/apple/Desktop/data/subject3/postopCT_subject_3.nii')
postct_4 = nib.load('/Users/apple/Desktop/data/subject4/postopCT_subject_4.nii')
postct_5 = nib.load('/Users/apple/Desktop/data/subject5/postopCT_subject_5.nii')
postct_data_1 = np.array(postct_1.get_fdata())
postct_data_2 = np.array(postct_2.get_fdata())
postct_data_3 = np.array(postct_3.get_fdata())
postct_data_4 = np.array(postct_4.get_fdata())
postct_data_5 = np.array(postct_5.get_fdata())

prect_1 = nib.load('/Users/apple/Desktop/data/subject1/preopCT_subject_1.nii')
prect_2 = nib.load('/Users/apple/Desktop/data/subject2/preopCT_subject_2.nii')
prect_3 = nib.load('/Users/apple/Desktop/data/subject3/preopCT_subject_3.nii')
prect_4 = nib.load('/Users/apple/Desktop/data/subject4/preopCT_subject_4.nii')
prect_5 = nib.load('/Users/apple/Desktop/data/subject5/preopCT_subject_5.nii')
prect_data_1 = np.array(prect_1.get_fdata())
prect_data_2 = np.array(prect_2.get_fdata())
prect_data_3 = np.array(prect_3.get_fdata())
prect_data_4 = np.array(prect_4.get_fdata())
prect_data_5 = np.array(prect_5.get_fdata())

fluoro_1 = np.array(Image.open('/Users/apple/Desktop/data/subject1/fluoro_subject_1.jpg'))
fluoro_2 = np.array(Image.open('/Users/apple/Desktop/data/subject2/fluoro_subject_2.jpg'))
fluoro_3 = np.array(Image.open('/Users/apple/Desktop/data/subject3/fluoro_subject_3.jpg'))
fluoro_4 = np.array(Image.open('/Users/apple/Desktop/data/subject4/fluoro_subject_4.jpg'))
fluoro_5 = np.array(Image.open('/Users/apple/Desktop/data/subject5/fluoro_subject_5.jpg'))

fluoro_1 = cv2.cvtColor(fluoro_1, cv2.COLOR_BGR2GRAY)
fluoro_1 = cv2.resize(fluoro_1,(256,256))
fluoro_2 = cv2.cvtColor(fluoro_2, cv2.COLOR_BGR2GRAY)
fluoro_2 = cv2.resize(fluoro_2,(256,256))
fluoro_3 = cv2.cvtColor(fluoro_3, cv2.COLOR_BGR2GRAY)
fluoro_3 = cv2.resize(fluoro_3,(256,256))
fluoro_4 = cv2.cvtColor(fluoro_4, cv2.COLOR_BGR2GRAY)
fluoro_4 = cv2.resize(fluoro_4,(256,256))
fluoro_5 = cv2.cvtColor(fluoro_5, cv2.COLOR_BGR2GRAY)
fluoro_5 = cv2.resize(fluoro_5,(256,256))

######################## remove nan in files #############################
all_files = [hull_data_1, hull_data_2, hull_data_3, hull_data_4, hull_data_5,
             postct_data_1, postct_data_2, postct_data_3, postct_data_4, postct_data_5,
             prect_data_1, prect_data_2, prect_data_3, prect_data_4, prect_data_5]

for i in range(len(all_files)):
    where_are_NaNs = np.isnan(all_files[i])
    all_files[i][where_are_NaNs] = 0
    
############################################################
###################### subject 1 ###########################
############################################################

##################### step 1 ###############################
# manually find coordinates of marks
# ct pin tip
pin_ct_x = 200
pin_ct_y = 146
pin_ct_z = 47
# ct lead tip
lead_ct_x = 129
lead_ct_y = 125
lead_ct_z = 69

##################### step 2 ###############################

fluoro_1 = rotate(fluoro_1, 90)

##################### step 3 ###############################

# allign fluoro with ct
fluoro_1 = cv2.resize(fluoro_1,(150,150))
shift_down = 296
shift_right = 226
fluoro_1_new = np.vstack((np.ones((shift_down,)+fluoro_1.shape[1:], 
                                   dtype=fluoro_1.dtype), 
                                    fluoro_1))
fluoro_1_newnew = np.hstack((np.ones(fluoro_1_new.shape[:1]+(shift_right,),
                                      dtype=fluoro_1_new.dtype), 
                                    fluoro_1_new))

plt.imshow(fluoro_1_newnew)
plt.show()

fig = mlab.figure(bgcolor=(1, 1, 1), size=(500, 500))
fig.on_mouse_pick(picker_callback)
mlab.imshow(fluoro_1_newnew)

source_1 = mlab.pipeline.scalar_field(prect_data_1)
surface = mlab.pipeline.iso_surface(source_1, 
                          contours=[256,], 
                          opacity=0.5, 
                          colormap = 'black-white')

source_2 = mlab.pipeline.scalar_field(postct_data_1[:,:128,:])
surface = mlab.pipeline.iso_surface(source_2, 
                          contours=[256,], 
                          opacity=0.8, 
                          colormap = 'black-white')
x = [pin_ct_x,pin_ct_x,lead_ct_x,lead_ct_x]
y = [pin_ct_y,pin_ct_y,lead_ct_y,lead_ct_y]
z = [pin_ct_z,0,lead_ct_z,0]
mlab.points3d(x,y,z, color = (0.2,1,.2), scale_factor=10)


##################### step 4 ###############################

# manually find coordinates of electrodes on fluoro
electrode_1 = [176.0, 80.0, 0.0]
electrode_2 = [169.0, 75.0, 0.0]
electrode_3 = [161.0, 72.0, 0.0]
electrode_4 = [154.0, 69.0, 0.]
electrode_5 = [146.0, 67.0, 0.0]
electrode_6 = [138.0, 67.0, 0.0]
electrode_7 = [130.0, 67.0, 0.0]
electrode_8 = [122.0, 66.0, 0.0]
electrode_9 = [110.0, 67.0, 0.0]
electrode_10 = [108.0, 72.0, 0.0]
electrode_11 = [109.0, 77.0, 0.]
electrode_12 = [110.0, 84.0, 0.0]
electrode_13 = [111.0, 92.0, 0.0]
electrode_14 = [113.0, 99.0, 0.0]
electrode_15 = [116.0, 107.0, 0.0]
electrode_16 = [118.0, 116.0, 0.0]

electrode_x = [electrode_1[0],electrode_2[0],electrode_3[0],electrode_4[0],
               electrode_5[0],electrode_6[0],electrode_7[0],electrode_8[0],
               electrode_9[0],electrode_10[0],electrode_11[0],electrode_12[0],
               electrode_13[0],electrode_14[0],electrode_15[0],electrode_16[0]]
electrode_y = [electrode_1[1],electrode_2[1],electrode_3[1],electrode_4[1],
               electrode_5[1],electrode_6[1],electrode_7[1],electrode_8[1],
               electrode_9[1],electrode_10[1],electrode_11[1],electrode_12[1],
               electrode_13[1],electrode_14[1],electrode_15[1],electrode_16[1]]
electrode_z = [electrode_1[2],electrode_2[2],electrode_3[2],electrode_4[2],
               electrode_5[2],electrode_6[2],electrode_7[2],electrode_8[2],
               electrode_9[2],electrode_10[2],electrode_11[2],electrode_12[2],
               electrode_13[2],electrode_14[2],electrode_15[2],electrode_16[2]]

fig = mlab.figure(bgcolor=(1, 1, 1), size=(500, 500))
fig.on_mouse_pick(picker_callback)
mlab.imshow(fluoro_1_newnew)

mlab.points3d(electrode_x,electrode_y,electrode_z, color = (0.5,1,.2), scale_factor=10)

##################### step 5 ###############################

#count points on hull
x,y,z = hull_data_1.shape
coord_list = points_hull(hull_data_1)
# print(len(coord_list)) 53803

# reshape electrode_coord_list
electrode_coord_list =reshape_electrode_coord_list(electrode_x,electrode_y,electrode_z)

# get electrode coordiantes in 3d space method 1
min_coord_list = get_electrode_coord(electrode_coord_list, coord_list)
 
# get electrode coordiantes in 3d space method 2
intersection_coord_list = get_electrode_coord_2(electrode_coord_list,coord_list)

##################### step 6 ###############################

# plot eletrodes on hull
# method 1
fig = mlab.figure(bgcolor=(1, 1, 1), size=(500, 500))
source_2 = mlab.pipeline.scalar_field(hull_data_1)
surface = mlab.pipeline.iso_surface(source_2, 
                          contours=[1,], 
                          opacity=1, 
                          colormap = 'black-white')
x = [min_coord_list[0][0],min_coord_list[1][0],min_coord_list[2][0],
     min_coord_list[3][0],min_coord_list[4][0],min_coord_list[5][0],
     min_coord_list[6][0],min_coord_list[7][0],min_coord_list[8][0],
     min_coord_list[9][0],min_coord_list[10][0],min_coord_list[11][0],
     min_coord_list[12][0],min_coord_list[13][0],min_coord_list[14][0],
     min_coord_list[15][0]]
y = [min_coord_list[0][1],min_coord_list[1][1],min_coord_list[2][1],
     min_coord_list[3][1],min_coord_list[4][1],min_coord_list[5][1],
     min_coord_list[6][1],min_coord_list[7][1],min_coord_list[8][1],
     min_coord_list[9][1],min_coord_list[10][1],min_coord_list[11][1],
     min_coord_list[12][1],min_coord_list[13][1],min_coord_list[14][1],
     min_coord_list[15][1]]
z = [min_coord_list[0][2],min_coord_list[1][2],min_coord_list[2][2],
     min_coord_list[3][2],min_coord_list[4][2],min_coord_list[5][2],
     min_coord_list[6][2],min_coord_list[7][2],min_coord_list[8][2],
     min_coord_list[9][2],min_coord_list[10][2],min_coord_list[11][2],
     min_coord_list[12][2],min_coord_list[13][2],min_coord_list[14][2],
     min_coord_list[15][2]]
mlab.points3d(x,y,z, color = (0.5,1,.2), scale_factor=5)

# method 2
fig = mlab.figure(bgcolor=(1, 1, 1), size=(500, 500))
source_2 = mlab.pipeline.scalar_field(hull_data_1)
surface = mlab.pipeline.iso_surface(source_2, 
                          contours=[1,], 
                          opacity=1, 
                          colormap = 'black-white')
x = [intersection_coord_list[0][0],intersection_coord_list[1][0],intersection_coord_list[2][0],
     intersection_coord_list[3][0],intersection_coord_list[4][0],intersection_coord_list[5][0],
     intersection_coord_list[6][0],intersection_coord_list[7][0],intersection_coord_list[8][0],
     intersection_coord_list[9][0],intersection_coord_list[10][0],intersection_coord_list[11][0],
     intersection_coord_list[12][0],intersection_coord_list[13][0],intersection_coord_list[14][0],
     intersection_coord_list[15][0]]
y = [intersection_coord_list[0][1],intersection_coord_list[1][1],intersection_coord_list[2][1],
     intersection_coord_list[3][1],intersection_coord_list[4][1],intersection_coord_list[5][1],
     intersection_coord_list[6][1],intersection_coord_list[7][1],intersection_coord_list[8][1],
     intersection_coord_list[9][1],intersection_coord_list[10][1],intersection_coord_list[11][1],
     intersection_coord_list[12][1],intersection_coord_list[13][1],intersection_coord_list[14][1],
     intersection_coord_list[15][1]]
z = [intersection_coord_list[0][2],intersection_coord_list[1][2],intersection_coord_list[2][2],
     intersection_coord_list[3][2],intersection_coord_list[4][2],intersection_coord_list[5][2],
     intersection_coord_list[6][2],intersection_coord_list[7][2],intersection_coord_list[8][2],
     intersection_coord_list[9][2],intersection_coord_list[10][2],intersection_coord_list[11][2],
     intersection_coord_list[12][2],intersection_coord_list[13][2],intersection_coord_list[14][2],
     intersection_coord_list[15][2]]
mlab.points3d(x,y,z, color = (0.5,1,.2), scale_factor=5)

############################################################
###################### subject 2 ###########################
############################################################

##################### step 1 ###############################
# manually find coordinates of marks
# ct lead tip
lead_ct_x = 135
lead_ct_y = 110
lead_ct_z = 69

##################### step 2 ###############################

fluoro_2 = np.fliplr(rotate(fluoro_2, 230))

##################### step 3 ###############################

# allign fluoro with ct
fluoro_2 = cv2.resize(fluoro_2,(150,150))
shift_down = 281
shift_right = 146
fluoro_2_new = np.vstack((np.ones((shift_down,)+fluoro_2.shape[1:], 
                                   dtype=fluoro_2.dtype), 
                                    fluoro_2))
fluoro_2_newnew = np.hstack((np.ones(fluoro_2_new.shape[:1]+(shift_right,),
                                      dtype=fluoro_2_new.dtype), 
                                    fluoro_2_new))

plt.imshow(fluoro_2_newnew)
plt.show()

fig = mlab.figure(bgcolor=(1, 1, 1), size=(500, 500))
fig.on_mouse_pick(picker_callback)
mlab.imshow(fluoro_2_newnew)

source_1 = mlab.pipeline.scalar_field(prect_data_2)
surface = mlab.pipeline.iso_surface(source_1, 
                          contours=[256,], 
                          opacity=0.5, 
                          colormap = 'black-white')

source_2 = mlab.pipeline.scalar_field(postct_data_2[:,:128,:])
surface = mlab.pipeline.iso_surface(source_2, 
                          contours=[256,], 
                          opacity=0.8, 
                          colormap = 'black-white')
x = [lead_ct_x,lead_ct_x]
y = [lead_ct_y,lead_ct_y]
z = [lead_ct_z,0]
mlab.points3d(x,y,z, color = (0.2,1,.2), scale_factor=10)


##################### step 4 ###############################

# manually find coordinates of electrodes on fluoro
electrode_1 = [166, 69.0, 0.0]
electrode_2 = [159, 65.0, 0.0]
electrode_3 = [154, 61.0, 0.0]
electrode_4 = [124, 55.0, 0.0]
electrode_5 = [118, 55.0, 0.0]

electrode_x = [electrode_1[0],electrode_2[0],electrode_3[0],electrode_4[0],
               electrode_5[0]]
electrode_y = [electrode_1[1],electrode_2[1],electrode_3[1],electrode_4[1],
               electrode_5[1]]
electrode_z = [electrode_1[2],electrode_2[2],electrode_3[2],electrode_4[2],
               electrode_5[2]]

fig = mlab.figure(bgcolor=(1, 1, 1), size=(500, 500))
fig.on_mouse_pick(picker_callback)
mlab.imshow(fluoro_2_newnew)

mlab.points3d(electrode_x,electrode_y,electrode_z, color = (0.5,1,.2), scale_factor=5)

##################### step 5 ###############################

#count points on hull
x,y,z = hull_data_2.shape
coord_list = points_hull(hull_data_2)
# print(len(coord_list)) 53803

# reshape electrode_coord_list
electrode_coord_list =reshape_electrode_coord_list(electrode_x,electrode_y,electrode_z)

# get electrode coordiantes in 3d space method 1
min_coord_list = get_electrode_coord(electrode_coord_list, coord_list)
 
# get electrode coordiantes in 3d space method 2
intersection_coord_list = get_electrode_coord_2(electrode_coord_list,coord_list)

##################### step 6 ###############################

# plot eletrodes on hull
# method 1
fig = mlab.figure(bgcolor=(1, 1, 1), size=(500, 500))
source_2 = mlab.pipeline.scalar_field(hull_data_2)
surface = mlab.pipeline.iso_surface(source_2, 
                          contours=[1,], 
                          opacity=0.2, 
                          colormap = 'black-white')
x = [min_coord_list[0][0],min_coord_list[1][0],min_coord_list[2][0],
     min_coord_list[3][0],min_coord_list[4][0]]
y = [min_coord_list[0][1],min_coord_list[1][1],min_coord_list[2][1],
     min_coord_list[3][1],min_coord_list[4][1]]
z = [min_coord_list[0][2],min_coord_list[1][2],min_coord_list[2][2],
     min_coord_list[3][2],min_coord_list[4][2]]
mlab.points3d(x,y,z, color = (0.5,1,.2), scale_factor=4)

# method 2
fig = mlab.figure(bgcolor=(1, 1, 1), size=(500, 500))
source_2 = mlab.pipeline.scalar_field(hull_data_2)
surface = mlab.pipeline.iso_surface(source_2, 
                          contours=[1,], 
                          opacity=0.2, 
                          colormap = 'black-white')
x = [intersection_coord_list[0][0],intersection_coord_list[1][0],intersection_coord_list[2][0],
     intersection_coord_list[3][0],intersection_coord_list[4][0]]
y = [intersection_coord_list[0][1],intersection_coord_list[1][1],intersection_coord_list[2][1],
     intersection_coord_list[3][1],intersection_coord_list[4][1]]
z = [intersection_coord_list[0][2],intersection_coord_list[1][2],intersection_coord_list[2][2],
     intersection_coord_list[3][2],intersection_coord_list[4][2]]
mlab.points3d(x,y,z, color = (0.5,1,.2), scale_factor=4)

############################################################
###################### subject 3 ###########################
############################################################

##################### step 1 ###############################
# manually find coordinates of marks
# ct pin tip
pin_ct_x = 210
pin_ct_y = 135
pin_ct_z = 37
# ct lead tip
lead_ct_x = 134
lead_ct_y = 115
lead_ct_z = 68

##################### step 2 ###############################

fluoro_3 = rotate(fluoro_3, 90)

##################### step 3 ###############################

# allign fluoro with ct
fluoro_3 = cv2.resize(fluoro_3,(150,150))
shift_down = 306
shift_right = 210
fluoro_3_new = np.vstack((np.ones((shift_down,)+fluoro_3.shape[1:], 
                                   dtype=fluoro_3.dtype), 
                                    fluoro_3))
fluoro_3_newnew = np.hstack((np.ones(fluoro_3_new.shape[:1]+(shift_right,),
                                      dtype=fluoro_3_new.dtype), 
                                    fluoro_3_new))

plt.imshow(fluoro_3_newnew)
plt.show()

fig = mlab.figure(bgcolor=(1, 1, 1), size=(500, 500))
fig.on_mouse_pick(picker_callback)
mlab.imshow(fluoro_3_newnew)

source_1 = mlab.pipeline.scalar_field(prect_data_3)
surface = mlab.pipeline.iso_surface(source_1, 
                          contours=[256,], 
                          opacity=0.5, 
                          colormap = 'black-white')

source_2 = mlab.pipeline.scalar_field(postct_data_3[:,:128,:])
surface = mlab.pipeline.iso_surface(source_2, 
                          contours=[256,], 
                          opacity=0.8, 
                          colormap = 'black-white')
x = [pin_ct_x,pin_ct_x,lead_ct_x,lead_ct_x]
y = [pin_ct_y,pin_ct_y,lead_ct_y,lead_ct_y]
z = [pin_ct_z,0,lead_ct_z,0]
mlab.points3d(x,y,z, color = (0.2,1,.2), scale_factor=10)

##################### step 4 ###############################

# manually find coordinates of electrodes on fluoro
electrode_1 = [176.0, 80.0, 0.0]
electrode_2 = [170.0, 75.0, 0.0]
electrode_3 = [163.0, 71.0, 0.0]
electrode_4 = [155.0, 69.0, 0.0]
electrode_5 = [146.0, 67.0, 0.0]
electrode_6 = [139.0, 65.0, 0.]
electrode_7 = [131.0, 65.0, 0.]
electrode_8 = [123.0, 65.0, 0.]
electrode_9 = [111.0, 66.0, 0.0]
electrode_10 = [109.0, 70.0, 0.0]
electrode_11 = [109.0, 76.0, 0.0]
electrode_12 = [110.0, 84.0, 0.0]
electrode_13 = [111.0, 91.0, 0.0]
electrode_14 = [114.0, 99.0, 0.0]
electrode_15 = [116.0, 106.0, 0.0]
electrode_16 = [118.0, 114.0, 0.0]

electrode_x = [electrode_1[0],electrode_2[0],electrode_3[0],electrode_4[0],
               electrode_5[0],electrode_6[0],electrode_7[0],electrode_8[0],
               electrode_9[0],electrode_10[0],electrode_11[0],electrode_12[0],
               electrode_13[0],electrode_14[0],electrode_15[0],electrode_16[0]]
electrode_y = [electrode_1[1],electrode_2[1],electrode_3[1],electrode_4[1],
               electrode_5[1],electrode_6[1],electrode_7[1],electrode_8[1],
               electrode_9[1],electrode_10[1],electrode_11[1],electrode_12[1],
               electrode_13[1],electrode_14[1],electrode_15[1],electrode_16[1]]
electrode_z = [electrode_1[2],electrode_2[2],electrode_3[2],electrode_4[2],
               electrode_5[2],electrode_6[2],electrode_7[2],electrode_8[2],
               electrode_9[2],electrode_10[2],electrode_11[2],electrode_12[2],
               electrode_13[2],electrode_14[2],electrode_15[2],electrode_16[2]]

fig = mlab.figure(bgcolor=(1, 1, 1), size=(500, 500))
fig.on_mouse_pick(picker_callback)
mlab.imshow(fluoro_1_newnew)

mlab.points3d(electrode_x,electrode_y,electrode_z, color = (0.5,1,.2), scale_factor=10)

##################### step 5 ###############################

#count points on hull
x,y,z = hull_data_3.shape
coord_list = points_hull(hull_data_3)
# print(len(coord_list)) 53803

# reshape electrode_coord_list
electrode_coord_list =reshape_electrode_coord_list(electrode_x,electrode_y,electrode_z)

# get electrode coordiantes in 3d space method 1
min_coord_list = get_electrode_coord(electrode_coord_list, coord_list)
 
# get electrode coordiantes in 3d space method 2
intersection_coord_list = get_electrode_coord_2(electrode_coord_list,coord_list)

##################### step 6 ###############################

# plot eletrodes on hull
# method 1
fig = mlab.figure(bgcolor=(1, 1, 1), size=(500, 500))
source_2 = mlab.pipeline.scalar_field(hull_data_3)
surface = mlab.pipeline.iso_surface(source_2, 
                          contours=[1,], 
                          opacity=1, 
                          colormap = 'black-white')
x = [min_coord_list[0][0],min_coord_list[1][0],min_coord_list[2][0],
     min_coord_list[3][0],min_coord_list[4][0],min_coord_list[5][0],
     min_coord_list[6][0],min_coord_list[7][0],min_coord_list[8][0],
     min_coord_list[9][0],min_coord_list[10][0],min_coord_list[11][0],
     min_coord_list[12][0],min_coord_list[13][0],min_coord_list[14][0],
     min_coord_list[15][0]]
y = [min_coord_list[0][1],min_coord_list[1][1],min_coord_list[2][1],
     min_coord_list[3][1],min_coord_list[4][1],min_coord_list[5][1],
     min_coord_list[6][1],min_coord_list[7][1],min_coord_list[8][1],
     min_coord_list[9][1],min_coord_list[10][1],min_coord_list[11][1],
     min_coord_list[12][1],min_coord_list[13][1],min_coord_list[14][1],
     min_coord_list[15][1]]
z = [min_coord_list[0][2],min_coord_list[1][2],min_coord_list[2][2],
     min_coord_list[3][2],min_coord_list[4][2],min_coord_list[5][2],
     min_coord_list[6][2],min_coord_list[7][2],min_coord_list[8][2],
     min_coord_list[9][2],min_coord_list[10][2],min_coord_list[11][2],
     min_coord_list[12][2],min_coord_list[13][2],min_coord_list[14][2],
     min_coord_list[15][2]]
mlab.points3d(x,y,z, color = (0.5,1,.2), scale_factor=4)

# method 2
fig = mlab.figure(bgcolor=(1, 1, 1), size=(500, 500))
source_2 = mlab.pipeline.scalar_field(hull_data_3)
surface = mlab.pipeline.iso_surface(source_2, 
                          contours=[1,], 
                          opacity=1, 
                          colormap = 'black-white')
x = [intersection_coord_list[0][0],intersection_coord_list[1][0],intersection_coord_list[2][0],
     intersection_coord_list[3][0],intersection_coord_list[4][0],intersection_coord_list[5][0],
     intersection_coord_list[6][0],intersection_coord_list[7][0],intersection_coord_list[8][0],
     intersection_coord_list[9][0],intersection_coord_list[10][0],intersection_coord_list[11][0],
     intersection_coord_list[12][0],intersection_coord_list[13][0],intersection_coord_list[14][0],
     intersection_coord_list[15][0]]
y = [intersection_coord_list[0][1],intersection_coord_list[1][1],intersection_coord_list[2][1],
     intersection_coord_list[3][1],intersection_coord_list[4][1],intersection_coord_list[5][1],
     intersection_coord_list[6][1],intersection_coord_list[7][1],intersection_coord_list[8][1],
     intersection_coord_list[9][1],intersection_coord_list[10][1],intersection_coord_list[11][1],
     intersection_coord_list[12][1],intersection_coord_list[13][1],intersection_coord_list[14][1],
     intersection_coord_list[15][1]]
z = [intersection_coord_list[0][2],intersection_coord_list[1][2],intersection_coord_list[2][2],
     intersection_coord_list[3][2],intersection_coord_list[4][2],intersection_coord_list[5][2],
     intersection_coord_list[6][2],intersection_coord_list[7][2],intersection_coord_list[8][2],
     intersection_coord_list[9][2],intersection_coord_list[10][2],intersection_coord_list[11][2],
     intersection_coord_list[12][2],intersection_coord_list[13][2],intersection_coord_list[14][2],
     intersection_coord_list[15][2]]
mlab.points3d(x,y,z, color = (0.5,1,.2), scale_factor=4)

############################################################
###################### subject 4 ###########################
############################################################

##################### step 1 ###############################
# manually find coordinates of marks
# ct pin tip
pin_ct_x = 196
pin_ct_y = 129
pin_ct_z = 45
# ct lead tip
lead_ct_x = 122
lead_ct_y = 104
lead_ct_z = 64

##################### step 2 ###############################

fluoro_4 = np.fliplr(rotate(fluoro_4, 230))

##################### step 3 ###############################

# allign fluoro with ct
fluoro_4 = cv2.resize(fluoro_4,(150,150))
shift_down = 300
shift_right = 176
fluoro_4_new = np.vstack((np.ones((shift_down,)+fluoro_4.shape[1:], 
                                   dtype=fluoro_4.dtype), 
                                    fluoro_4))
fluoro_4_newnew = np.hstack((np.ones(fluoro_4_new.shape[:1]+(shift_right,),
                                      dtype=fluoro_4_new.dtype), 
                                    fluoro_4_new))

plt.imshow(fluoro_4_newnew)
plt.show()

fig = mlab.figure(bgcolor=(1, 1, 1), size=(500, 500))
fig.on_mouse_pick(picker_callback)
mlab.imshow(fluoro_4_newnew)

source_1 = mlab.pipeline.scalar_field(prect_data_4)
surface = mlab.pipeline.iso_surface(source_1, 
                          contours=[256,], 
                          opacity=0.5, 
                          colormap = 'black-white')

source_2 = mlab.pipeline.scalar_field(postct_data_4[:,:128,:])
surface = mlab.pipeline.iso_surface(source_2, 
                          contours=[256,], 
                          opacity=0.8, 
                          colormap = 'black-white')
x = [pin_ct_x,pin_ct_x,lead_ct_x,lead_ct_x]
y = [pin_ct_y,pin_ct_y,lead_ct_y,lead_ct_y]
z = [pin_ct_z,0,lead_ct_z,0]
mlab.points3d(x,y,z, color = (0.2,1,.2), scale_factor=10)

##################### step 4 ###############################

# manually find coordinates of electrodes on fluoro
electrode_1 = [172.0, 87.0, 0.0]
electrode_2 = [168.0, 91.0, 0.]
electrode_3 = [165.0, 95.0, 0.]
electrode_4 = [160.0, 98.0, 0.0]
electrode_5 = [140.0, 56.0, 0.0]
electrode_6 = [147.0, 59.0, 0.0]
electrode_7 = [159.0, 68.0, 0.0]

electrode_x = [electrode_1[0],electrode_2[0],electrode_3[0],electrode_4[0],
               electrode_5[0],electrode_6[0],electrode_7[0]]
electrode_y = [electrode_1[1],electrode_2[1],electrode_3[1],electrode_4[1],
               electrode_5[1],electrode_6[1],electrode_7[1]]
electrode_z = [electrode_1[2],electrode_2[2],electrode_3[2],electrode_4[2],
               electrode_5[2],electrode_6[2],electrode_7[2]]

fig = mlab.figure(bgcolor=(1, 1, 1), size=(500, 500))
fig.on_mouse_pick(picker_callback)
mlab.imshow(fluoro_4_newnew)

mlab.points3d(electrode_x,electrode_y,electrode_z, color = (0.5,1,.2), scale_factor=10)

##################### step 5 ###############################

#count points on hull
x,y,z = hull_data_4.shape
coord_list = points_hull(hull_data_4)
# print(len(coord_list)) 53803

# reshape electrode_coord_list
electrode_coord_list =reshape_electrode_coord_list(electrode_x,electrode_y,electrode_z)

# get electrode coordiantes in 3d space method 1
min_coord_list = get_electrode_coord(electrode_coord_list, coord_list)
 
# get electrode coordiantes in 3d space method 2
intersection_coord_list = get_electrode_coord_2(electrode_coord_list,coord_list)

##################### step 6 ###############################

# plot eletrodes on hull
# method 1
fig = mlab.figure(bgcolor=(1, 1, 1), size=(500, 500))
source_2 = mlab.pipeline.scalar_field(hull_data_4)
surface = mlab.pipeline.iso_surface(source_2, 
                          contours=[1,], 
                          opacity=0.2, 
                          colormap = 'black-white')
x = [min_coord_list[0][0],min_coord_list[1][0],min_coord_list[2][0],
     min_coord_list[3][0],min_coord_list[4][0],min_coord_list[5][0],
     min_coord_list[6][0]]
y = [min_coord_list[0][1],min_coord_list[1][1],min_coord_list[2][1],
     min_coord_list[3][1],min_coord_list[4][1],min_coord_list[5][1],
     min_coord_list[6][1]]
z = [min_coord_list[0][2],min_coord_list[1][2],min_coord_list[2][2],
     min_coord_list[3][2],min_coord_list[4][2],min_coord_list[5][2],
     min_coord_list[6][2]]
mlab.points3d(x,y,z, color = (0.5,1,.2), scale_factor=5)

# method 2
fig = mlab.figure(bgcolor=(1, 1, 1), size=(500, 500))
source_2 = mlab.pipeline.scalar_field(hull_data_4)
surface = mlab.pipeline.iso_surface(source_2, 
                          contours=[1,], 
                          opacity=0.2, 
                          colormap = 'black-white')
x = [intersection_coord_list[0][0],intersection_coord_list[1][0],intersection_coord_list[2][0],
     intersection_coord_list[3][0],intersection_coord_list[4][0],intersection_coord_list[5][0],
     intersection_coord_list[6][0]]
y = [intersection_coord_list[0][1],intersection_coord_list[1][1],intersection_coord_list[2][1],
     intersection_coord_list[3][1],intersection_coord_list[4][1],intersection_coord_list[5][1],
     intersection_coord_list[6][1]]
z = [intersection_coord_list[0][2],intersection_coord_list[1][2],intersection_coord_list[2][2],
     intersection_coord_list[3][2],intersection_coord_list[4][2],intersection_coord_list[5][2],
     intersection_coord_list[6][2]]
mlab.points3d(x,y,z, color = (0.5,1,.2), scale_factor=5)


############################################################
###################### subject 5 ###########################
############################################################

##################### step 1 ###############################
# manually find coordinates of marks
# ct pin tip
pin_ct_x = 198
pin_ct_y = 161
pin_ct_z = 38
# ct lead tip
lead_ct_x = 136
lead_ct_y = 132
lead_ct_z = 69

##################### step 2 ###############################

fluoro_5 = rotate(fluoro_5, 80)

##################### step 3 ###############################

# allign fluoro with ct
fluoro_5 = cv2.resize(fluoro_5,(150,150))
shift_down = 316
shift_right = 216
fluoro_5_new = np.vstack((np.ones((shift_down,)+fluoro_5.shape[1:], 
                                   dtype=fluoro_5.dtype), 
                                    fluoro_5))
fluoro_5_newnew = np.hstack((np.ones(fluoro_5_new.shape[:1]+(shift_right,),
                                      dtype=fluoro_5_new.dtype), 
                                    fluoro_5_new))

plt.imshow(fluoro_5_newnew)

fig = mlab.figure(bgcolor=(1, 1, 1), size=(500, 500))
fig.on_mouse_pick(picker_callback)
mlab.imshow(fluoro_5_newnew)

source_1 = mlab.pipeline.scalar_field(prect_data_5)
surface = mlab.pipeline.iso_surface(source_1, 
                          contours=[256,], 
                          opacity=0.5, 
                          colormap = 'black-white')

source_2 = mlab.pipeline.scalar_field(postct_data_5[:,:128,:])
surface = mlab.pipeline.iso_surface(source_2, 
                          contours=[256,], 
                          opacity=0.8, 
                          colormap = 'black-white')
x = [pin_ct_x,pin_ct_x,lead_ct_x,lead_ct_x]
y = [pin_ct_y,pin_ct_y,lead_ct_y,lead_ct_y]
z = [pin_ct_z,0,lead_ct_z,0]
mlab.points3d(x,y,z, color = (0.2,1,.2), scale_factor=10)


##################### step 4 ###############################

# manually find coordinates of electrodes on fluoro
electrode_1 = [133.0, 104.0, 0.0]
electrode_2 = [132.0, 96.0, 0.0]
electrode_3 = [204.0, 100.0, 0.0]
electrode_4 = [198.0, 97.0, 0.0]
electrode_5 = [192.0, 93.0, 0.0]
electrode_6 = [183.0, 89.0, 0.0]
electrode_7 = [173.0, 87.0, 0.0]
electrode_8 = [166.0, 87.0, 0.]
electrode_9 = [158.0, 86.0, 0.0]
electrode_10 = [149.0, 87.0, 0.]

electrode_x = [electrode_1[0],electrode_2[0],electrode_3[0],electrode_4[0],
               electrode_5[0],electrode_6[0],electrode_7[0],electrode_8[0],
               electrode_9[0],electrode_10[0]]
electrode_y = [electrode_1[1],electrode_2[1],electrode_3[1],electrode_4[1],
               electrode_5[1],electrode_6[1],electrode_7[1],electrode_8[1],
               electrode_9[1],electrode_10[1]]
electrode_z = [electrode_1[2],electrode_2[2],electrode_3[2],electrode_4[2],
               electrode_5[2],electrode_6[2],electrode_7[2],electrode_8[2],
               electrode_9[2],electrode_10[2]]

fig = mlab.figure(bgcolor=(1, 1, 1), size=(500, 500))
fig.on_mouse_pick(picker_callback)
mlab.imshow(fluoro_5_newnew)

mlab.points3d(electrode_x,electrode_y,electrode_z, color = (0.5,1,.2), scale_factor=10)

##################### step 5 ###############################

#count points on hull
x,y,z = hull_data_5.shape
coord_list = points_hull(hull_data_5)
# print(len(coord_list)) 53803

# reshape electrode_coord_list
electrode_coord_list =reshape_electrode_coord_list(electrode_x,electrode_y,electrode_z)

# get electrode coordiantes in 3d space method 1
min_coord_list = get_electrode_coord(electrode_coord_list, coord_list)
 
# get electrode coordiantes in 3d space method 2
intersection_coord_list = get_electrode_coord_2(electrode_coord_list,coord_list)

##################### step 6 ###############################

# plot eletrodes on hull
# method 1
fig = mlab.figure(bgcolor=(1, 1, 1), size=(500, 500))
source_2 = mlab.pipeline.scalar_field(hull_data_5)
surface = mlab.pipeline.iso_surface(source_2, 
                          contours=[1,], 
                          opacity=1, 
                          colormap = 'black-white')
x = [min_coord_list[0][0],min_coord_list[1][0],min_coord_list[2][0],
     min_coord_list[3][0],min_coord_list[4][0],min_coord_list[5][0],
     min_coord_list[6][0],min_coord_list[7][0],min_coord_list[8][0],
     min_coord_list[9][0]]
y = [min_coord_list[0][1],min_coord_list[1][1],min_coord_list[2][1],
     min_coord_list[3][1],min_coord_list[4][1],min_coord_list[5][1],
     min_coord_list[6][1],min_coord_list[7][1],min_coord_list[8][1],
     min_coord_list[9][1]]
z = [min_coord_list[0][2],min_coord_list[1][2],min_coord_list[2][2],
     min_coord_list[3][2],min_coord_list[4][2],min_coord_list[5][2],
     min_coord_list[6][2],min_coord_list[7][2],min_coord_list[8][2],
     min_coord_list[9][2]]
mlab.points3d(x,y,z, color = (0.5,1,.2), scale_factor=5)

# method 2
fig = mlab.figure(bgcolor=(1, 1, 1), size=(500, 500))
source_2 = mlab.pipeline.scalar_field(hull_data_5)
surface = mlab.pipeline.iso_surface(source_2, 
                          contours=[1,], 
                          opacity=1, 
                          colormap = 'black-white')
x = [intersection_coord_list[0][0],intersection_coord_list[1][0],intersection_coord_list[2][0],
     intersection_coord_list[3][0],intersection_coord_list[4][0],intersection_coord_list[5][0],
     intersection_coord_list[6][0],intersection_coord_list[7][0],intersection_coord_list[8][0],
     intersection_coord_list[9][0]]
y = [intersection_coord_list[0][1],intersection_coord_list[1][1],intersection_coord_list[2][1],
     intersection_coord_list[3][1],intersection_coord_list[4][1],intersection_coord_list[5][1],
     intersection_coord_list[6][1],intersection_coord_list[7][1],intersection_coord_list[8][1],
     intersection_coord_list[9][1]]
z = [intersection_coord_list[0][2],intersection_coord_list[1][2],intersection_coord_list[2][2],
     intersection_coord_list[3][2],intersection_coord_list[4][2],intersection_coord_list[5][2],
     intersection_coord_list[6][2],intersection_coord_list[7][2],intersection_coord_list[8][2],
     intersection_coord_list[9][2]]
mlab.points3d(x,y,z, color = (0.5,1,.2), scale_factor=5)

#############################################################
#############################################################
#############################################################

