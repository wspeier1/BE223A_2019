#!/usr/bin/env python
# coding: utf-8

# In[84]:


# %load headers_files.py
import os
import pandas as pd
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.transforms as mtransforms
from nilearn.plotting import view_img, view_img_on_surf
import nibabel as nib
import cv2
from scipy.spatial.transform import Rotation as R
from nilearn.image import resample_img 
from skimage import data, color
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.feature import canny
from skimage.draw import circle_perimeter, circle
from skimage.util import img_as_ubyte
from skimage import feature
from scipy import ndimage as ndi 


# In[85]:


#declaration of variables
patient = np.array(['subject_1/fluoro_subject_1c.tif',
                    'subject_2/fluoro_subject_2b.jpg',
                    'subject_3/fluoro_subject_3.jpg',
                    'subject_4/fluoro_subject_4.jpg',
                    'subject_5/fluoro_subject_5.jpg'])
black_pixel = 0
white_pixel_max = 255
white_pixel_min = 210


# In[86]:


# %load myfunctions.py
def showArray (array_path1,array_path2):
    for i in range (len(array_path1)):
        path1 = np.load(array_path1[i],mmap_mode = 'r+')
        path2 = np.load(array_path2[i],mmap_mode = 'r+')
        fig, ax = plt.subplots(ncols=2, nrows=1, figsize=(20, 10))
        ax[0].imshow(path1, cmap=plt.cm.gray)
        ax[1].imshow(path2, cmap=plt.cm.gray)

def loadAll (array_path):
    im = []
    for i in range (len(array_path)):
        im.append(np.load(array_path[i]))
    return im

def findXY (matrix):
    row,col = matrix.shape
    lst = []
    for r in range(row):
        for c in range(col):
            if matrix[r][c] == 1:
                lst.append((r,c))
    return lst


# In[95]:


def findOnes (matrix):
    row,col = matrix.shape
    lst = []
    for r in range(row):
        for c in range(col):
            if matrix[r][c] == 1:
                lst.append((r,c))
    return lst

def shiftXY(points, r, c):
   # r,c = shiftCoordinate
    for i in range(len(points)):
        y,x = points[i]
        shifty = y + r
        shiftx = x + c   
        points[i] = (shifty, shiftx)    
    return points

#this function accepts 3 inputs: 2dmatrix, int radius away from the central
def removePerimeter(matrix, radius, marginal):
    #make sure this lower bound of radius is at least 2.
    centerx = radius 
    centery = centerx
    if radius >= marginal:
        for radii in range(radius - marginal, radius):   
            circy, circx = circle_perimeter(centery, centerx, radii,shape=matrix.shape)
            matrix[circy, circx] = 0
            print('been here when r = ',radii)
    else:
        print("Marginal perimeter reduction exceed radius")
    return matrix


#generate a circle Mask is a np.matrix that has the same shape as matrix
def circleMask(matrix, center, radius):    
    filter = np.zeros(matrix.shape, dtype = np.uint8)
    cy, cx = center
    rr, cc = circle(cy, cx, radius)
    filter[rr, cc] = 1
    return filter


# In[88]:



#this function will takes an python matrix as input and output a list of points
def curve_extraction_helper(matrix, shiftedxy, radius, perimeter_margin = 3):
    #blur
    shifty, shiftx = shiftedxy
    #smooth the image
    matrix_blur = ndi.gaussian_filter(matrix, 6)
    #canny this
    edge = feature.canny(matrix_blur)
    fig, ax = plt.subplots(ncols=1, nrows=2, figsize=(20, 20))
    ax[0].imshow(matrix, cmap=plt.cm.gray)
    ax[1].imshow(edge, cmap=plt.cm.gray)
   
    """
    # Detect circles with size of hough_radii 
    hough_radii = np.arange(300,400, 1)
    hough_res = hough_circle(edge, hough_radii)
    
    # Select the most prominent 1 circles
    accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii, total_num_peaks=1)
    print("detected center: ",(cy,cx))
    print("detected radii: ",radii)
    
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 10))
    for center_y, center_x, radius in zip(cy, cx, radii):   
        circy, circx = circle_perimeter(center_y, center_x, radius,shape=edge.shape)
        if edge[circy, circx].all() == 1:
            print("at least 1 here")

        edge[circy, circx] = 0
    ax.imshow(edge, cmap=plt.cm.gray)
    plt.show()
    
    """
    #originally plan to use perimeter, but it didn't work well
    """
    edge_withoutPerimeter = removePerimeter(edge, radius, perimeter_margin) 
    """
    adjustedRad = radius - perimeter_margin
    mask = circleMask(edge, (radius, radius), adjustedRad)
    edge_withoutPerimeter = np.multiply(edge, mask)
    """
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 10))
    ax.imshow(edge_withoutPerimeter, cmap=plt.cm.gray)
    """
    #remove points that are on the hough
    listCurve = findOnes(edge_withoutPerimeter)
    shiftedlist = shiftXY(listCurve, shifty, shiftx)
    return shiftedlist
    #export the points in (x,y) lists


# In[99]:


def reshape_image(raw_patient):
    #generate pixels
    # approach one, using cv2 
    img = cv2.imread(raw_patient, 0)
        # Load picture and detect edges
    edges = canny(img, sigma=3, low_threshold=10, high_threshold=50)
        # Detect two radii
    hough_radii = np.arange(200,600, 1)
    hough_res = hough_circle(edges, hough_radii)
        # Select the most prominent 1 circles
    accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii, total_num_peaks=1)
    mask_internal = np.zeros((2*radii[0], 2*radii[0]), dtype=np.uint8)
    y_min = cy[0] - radii[0]
    x_min = cx[0] - radii[0]
        
    #filtering the ones only in the pixels 
    for y in range(0,(2*radii[0])):
        for x in range (0,(2*radii[0])):
            mask_internal[y, x] =  img[y+y_min, x+x_min]

    # change the internal white pixels to black
    for y in range(0,(2*radii[0])):
        for x in range (0,(2*radii[0])):
            if mask_internal[y,x] >= white_pixel_min and mask_internal[y, x] <= white_pixel_max:
                mask_internal[y,x] = black_pixel
    #np.save('Data/Modified_fluoro2/patient_'+str(i)+'.npy', mask_internal)
    return (mask_internal ,(y_min, x_min), radii[0])


# In[113]:


# curve_extraction takes 2 parameters, input_path and output_path:
# output path should be formatted as'Data/Curvature_fluoro/patient_'+str(0)+'.npy'
def curve_extraction(input_path, output_path):
    img, (y_min, x_min), radii = reshape_image(input_path)
    shifted_list = curve_extraction_helper(img, (y_min, x_min), radii)
    np.save(output_path, shifted_list)


# In[120]:


input_path = patient[0]
output_path = 'Data/Curvature_fluoro/patient_'+str(0)+'.npy'
curve_extraction(raw_img, output_path)


# In[117]:


"""
raw_img = 'Data/Raw_fluoro/fluoro_subject_1c.tif'
img, (y_min, x_min), radii = reshape_image(raw_img)
shifted_list = curve_extraction_helper(img,(y_min, x_min), radii)

shifted_list
y_min
np.save('Data/Curvature_fluoro/patient_'+str(0)+'.npy', shifted_list)
"""


# In[115]:


"""
patient_modified2 = np.array(['Data/Modified_fluoro2/patient_0.npy',
                              'Data/Modified_fluoro2/patient_1.npy',
                              'Data/Modified_fluoro2/patient_2.npy',
                              'Data/Modified_fluoro2/patient_3.npy',
                              'Data/Modified_fluoro2/patient_4.npy'])
patient = loadAll(patient_modified2)
radius = int(len(patient[0])/2)

shifted_list = curve_extraction(patient[0],(radius, radius), radius)
shifted_list
"""


# In[ ]:


"""
color = (0, 0 , 255)
cx = int (len(patient[0])/2)
img = patient[0].copy
#return np.multiply(matrix, data):
"""


# In[ ]:


"""
filter = np.array([[1,0,1],[0,0,0]])
data = np.array([[1,0,0],[1,1,1]])
valid_data = np.multiply(filter,data)
valid_data
"""


# In[ ]:





# In[ ]:





# In[ ]:




