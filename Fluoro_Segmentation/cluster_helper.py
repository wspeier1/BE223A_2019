import os
import sys
import matplotlib.pyplot as plt
import importlib


import numpy as np
from sklearn.linear_model import LinearRegression

# extractClusterPoints_helper will extract the an array of points that have
# the same label as the key.
#labels label the point in which cluster it belongs to 
#maxima points are the potential electrodes coordinates
def extractClusterPoints_helper (key, labels_list, maxima_list):
    cluster = []
    for i in range(0, len(labels_list)):
        if labels_list[i] == key:
            cluster.append(maxima_list[i])
    return np.array(cluster)

def extractClusterPoints(labels_list, maxima_list):
    # get # of clusters in the label, just get maximum index value from label list
    #extract each label 
    max_cluster = np.amax(labels_list) + 1
    pts_cluster = []
    for cluster in range(0,max_cluster):
        pts = extractClusterPoints_helper(cluster, labels_list, maxima_list)
        pts_cluster.append(pts)
    pts_cluster = np.array(pts_cluster)
    return pts_cluster


#testcases for extractClusterPoints
#extractClusterPoints(labels,bg10_maxima)