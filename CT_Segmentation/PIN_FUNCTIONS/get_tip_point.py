#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 22:16:15 2019

@author: keane
"""
import numpy as np

def get_tip_point(hemisphere_dict):
    closest_pin_index={} #closest pin point index per slice
    closest_pin_distance ={} #closest pin point distance from center
    for key in mloc_dict.keys():#this is every slice
        points = mloc_dict[key] #all the xy metal points in this slice
        distance_hull = []
        for counter, npoints in enumerate(points):
            dx_hull_metal = np.abs(mx[key][0] - npoints[1])
            dy_hull_metal = np.abs(my[key][0] - npoints[0])
            distance_hull.append(np.sqrt(np.power(dx_hull_metal,2) + 
                                     np.power(dy_hull_metal,2)))
        lowest_distance_index = np.argmin(distance_hull)
        #for this slice, lowest_distance is the one closest to the center
        closest_pin_distance[key] = distance_hull[lowest_distance_index]
        closest_pin_index[key] = lowest_distance_index
# Now we have all the closest pin values per each slice (as key). Get the 
#smallest of these and that will be output to the NIFTI file
    smallest_distance = 99999 #this will be replaced with the dictionary
    for key in closest_pin_index.keys():
        test_value = closest_pin_distance[key] 
        if (test_value < smallest_distance):
            smallest_index = key
            smallest_distance = test_value 
    print('smallest key for closest point is ',smallest_index)
    #the smallest point can be found with mloc_dict[key] and 
    #closest_pin_index[key]. This will give the xy point for this slice 
    #that is closest to the hull center point
    #mloc_dict[smallest_index][closest_pin_index[smallest_index]]
    tip_points =  mloc_dict[smallest_index][closest_pin_index[smallest_index]]
    output_nii_point_only[tip_points[0],tip_points[1],smallest_index] = 1
        
    return 0