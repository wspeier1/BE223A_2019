#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 22:16:15 2019

@author: keane
"""
import numpy as np

def get_tip_point(hemisphere_dict,mx,my, slice_marker,mloc_dict):
    closest_pin_index={} #closest pin point index per slice
    closest_pin_distance ={} #closest pin point distance from center
    tip_points = {}  #output xy pair for each hemi
    tip_slice = {}
# =============================================================================
#     MERGE THE UPPER QUADRANTS TOGETHER AND THEN THE LOWER QUADRANTS
#  This will account for pins that straddle the lines on a PIR oriented image
#  (other orientations will require some extra checking). For a PIR image, the 
#  nose aligns with our quadrant 0/1 boundary line (A-P). This should allow us
#  to let Q0/1 work as one unit and 2/3 as the lower half
# =============================================================================
    
    combined_dict={}
    combined_dict[0]=[]
    combined_dict[1]=[]
    
    #put the 01 quads together 
    combined_slice_dict={}
    combined_slice_dict[0]=[]
    combined_slice_dict[1]=[]
    
    for ii in range(0,4):
        for vals in hemisphere_dict[ii]:
            if (ii <2):
                combined_dict[0].extend([vals])
            else:
                combined_dict[1].extend([vals])
                
        for vals in slice_marker[ii]:
            if (ii <2):
                combined_slice_dict[0].extend([vals])
            else:
                combined_slice_dict[1].extend([vals])
    
    for key in combined_dict.keys(): #loop through both hemis
        distance_hull=[]
        for counter,npoints in enumerate(combined_dict[key]):
            print('counter=',counter)
            slice_number = combined_slice_dict[key][counter]
            dx_hull_metal = np.abs(mx[slice_number][0] - npoints[1])
            dy_hull_metal = np.abs(my[slice_number][0] - npoints[0])
            distance_hull.append(np.sqrt(np.power(dx_hull_metal,2) + 
                                     np.power(dy_hull_metal,2)))
        lowest_distance_index = np.argmin(distance_hull)
        #for this slice, lowest_distance is the one closest to the center
        closest_pin_distance[key] = distance_hull[lowest_distance_index]
        closest_pin_index[key] = lowest_distance_index
    
    
        smallest_distance = 99999 #this will be replaced with the dictionary
        for key_closest in closest_pin_index.keys():
            test_value = closest_pin_distance[key_closest] 
            if (test_value < smallest_distance):
                smallest_index = key_closest
                smallest_distance = test_value 
        print('smallest key for closest point is ',smallest_index)
    

        #the smallest point can be found with mloc_dict[key] and 
        #closest_pin_index[key]. This will give the xy point for this slice 
        #that is closest to the hull center point
        #mloc_dict[smallest_index][closest_pin_index[smallest_index]]
        #tip_points[key] = mloc_dict[combined_slice_dict[key][closest_pin_index[smallest_index]]]
        #tip_points =  mloc_dict[smallest_index][closest_pin_index[smallest_index]]
        tip_points[key] = combined_dict[key][closest_pin_index[key]]
        tip_slice[key] = combined_slice_dict[key][closest_pin_index[key]]
        
    return tip_points, tip_slice