#!/usr/bin/env python
# coding: utf-8

# Electrode Segmentation
# ==============
# 

# References:
# 1. [Basics of Image Processing in Python](https://www.analyticsvidhya.com/blog/2014/12/image-processing-python-basics/) //detecting stars
# 2. [Blob Detection Techniques](https://scikit-image.org/docs/dev/auto_examples/features_detection/plot_blob.html)

# Compare and Contrast different Blob detection techniques [2]
#     Blob Detection
#     Blobs are bright on dark or dark on bright regions in an image. In this example, blobs are detected using 3 algorithms. The image used in this case is the Hubble eXtreme Deep Field. Each bright dot in the image is a star or a galaxy.
# 
#     Laplacian of Gaussian (LoG)
#     This is the most accurate and slowest approach. It computes the Laplacian of Gaussian images with successively increasing standard deviation and stacks them up in a cube. Blobs are local maximas in this cube. Detecting larger blobs is especially slower because of larger kernel sizes during convolution. Only bright blobs on dark backgrounds are detected. See skimage.feature.blob_log() for usage.
# 
#     Difference of Gaussian (DoG)
#     This is a faster approximation of LoG approach. In this case the image is blurred with increasing standard deviations and the difference between two successively blurred images are stacked up in a cube. This method suffers from the same disadvantage as LoG approach for detecting larger blobs. Blobs are again assumed to be bright on dark. See skimage.feature.blob_dog() for usage.
# 
#     Determinant of Hessian (DoH)
#     This is the fastest approach. It detects blobs by finding maximas in the matrix of the Determinant of Hessian of the image. The detection speed is independent of the size of blobs as internally the implementation uses box filters instead of convolutions. Bright on dark as well as dark on bright blobs are detected. The downside is that small blobs (<3px) are not detected accurately. See skimage.feature.blob_doh() for usage.

# In[1]:


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


# - find maxima with tolerance of 24

# In[2]:


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

def filterRange(lst, x_min, x_max, y_min, y_max):
    newlst = []
    for (y,x) in lst:
        if (x >= x_min and x<= x_max) and (y >= y_min and y <= y_max):
            newlst.append((y,x))
    return newlst
# In[7]:


# electrode_detection will take in 2 inputs of raw image's path and 
# return a list of central points for electrodes. 
# input format: (string file_path)
# output type: [(int y,int x)]. 
def electrode_detection(input_path, output_path):
    # approach one, using cv2 
    img = cv.imread(input_path, 0)
    # Load picture and detect edges

    edges = canny(img, sigma=2, low_threshold=35, high_threshold=40)
    #plot the graph to get a better feeling
    """
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 10))
    ax.imshow(edges, cmap=plt.cm.gray)
    plt.show()
    """
    # Detect circles with size of hough_radii 
    hough_radii = np.arange(5,40, 1)
    hough_res = hough_circle(edges, hough_radii)

    # Select the most prominent 30 circles
    accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii, total_num_peaks=30)
    #this returns the list of points that are on the perimeters, and change the value to white 
    #for better visualization
        
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 10))
    for center_y, center_x, radius in zip(cy, cx, radii):   
        circy, circx = circle_perimeter(center_y, center_x, radius,shape=img.shape)
        img[circy, circx] = 255
 #   ax.imshow(img, cmap=plt.cm.gray)
 #  plt.show()
    lst = list(zip(cy,cx))
    lst = filterRange(lst, 400, 800, 120,480)
    np.save(output_path, lst)
# In[9]:


#generate pixels
raw_patient = np.array(['Data/Raw_fluoro/fluoro_subject_1c.tif',
                        'Data/Raw_fluoro/fluoro_subject_2b.jpg',
                        'Data/Raw_fluoro/fluoro_subject_3.jpg',
                        'Data/Raw_fluoro/fluoro_subject_4.jpg',
                        'Data/Raw_fluoro/fluoro_subject_5.jpg'])

save_path = np.array(['Data/Electrode_fluoro/patient_0.npy',
                      'Data/Electrode_fluoro/patient_1.npy',
                      'Data/Electrode_fluoro/patient_2.npy',
                      'Data/Electrode_fluoro/patient_3.npy',
                      'Data/Electrode_fluoro/patient_4.npy'])


# In[11]:


#electrode_detection(raw_patient[0],save_path[0])


# In[5]:





# In[ ]:




