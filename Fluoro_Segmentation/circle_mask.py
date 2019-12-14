import os
import sys
import numpy as np
from skimage.draw import circle
from skimage.feature import canny
from skimage.transform import hough_circle, hough_circle_peaks

#generate a circle Mask is a np.matrix that has the same shape as matrix
def circleMask(matrix, center, radius):    
    filter = np.zeros(matrix.shape, dtype = np.uint8)
    cy, cx = center
    rr, cc = circle(cy, cx, radius)
    filter[rr, cc] = 1
    return filter


"""
this function filter all the contents outside the fluoro area
takes in a pre-loaded image, and return an filtered image
design: 
1. perform canny
2. form a mask against exterior
3. point-wise multiplication
"""
def preprocess_exterior(img):
    edges = canny(img, sigma=3, low_threshold=10, high_threshold=50)
    # Detect two radii
    hough_radii = np.arange(200,600,1)
    hough_res = hough_circle(edges, hough_radii)
    # Select the most prominent 1 circles
    accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii, total_num_peaks=1)
    big_rad = radii[0]
    big_central_coordinate = (cy[0],cx[0])
    print("big_radius = ", big_rad )
    print("big_central_coordinate = ", big_central_coordinate)

    prominent_mask = circleMask(img, big_central_coordinate, big_rad)
    processed_img = np.multiply(img, prominent_mask)
    """
    fig, ax = plt.subplots(ncols=2, nrows=1, figsize=(20, 20))
    ax[0].imshow(img, cmap=plt.cm.gray)
    ax[1].imshow(processed_img, cmap=plt.cm.gray)
    plt.show()
    """
    return processed_img