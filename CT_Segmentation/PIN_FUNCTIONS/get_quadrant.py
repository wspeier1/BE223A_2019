#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 23:38:46 2019

@author: keane
"""
import numpy as np
from copy import copy, deepcopy  #to copy dictionaries


def get_quadrant(mloc_dict,mx,my,nz):
    
    previous_slice=-1
    center = []
    quad_total={}
    for key in mloc_dict.keys():
        quad_list=[]
        #assume all pin dictionary keys are in same quadrant
        for numpairs in mloc_dict[key]:
            #each slice may have multiple matching points, for one or more
            #pins
            rowvalue = numpairs[0] - my[key][0]
            colvalue = numpairs[1] - mx[key][0]
            
# =============================================================================
# QUADRANTS are      1    0
#                    2    3
# where quadrant 0 is row point of metal point - the hull center, which should
# give a negative value (python ordering) and the column point of the metal 
# point should be positive (python ordering)
# These are based on the python imaging format for the data, with a standard 
# P-I-R orientation (other orientations may require additional testing)
#
#
#
#            
# =============================================================================
            
            if ( (rowvalue <=0) and (colvalue >= 0)):
                quad_list.append(0)
            elif ( (rowvalue < 0) and (colvalue < 0)):
                quad = 1
                quad_list.append(1)
            elif ( (rowvalue > 0) and (colvalue < 0)):
                quad = 2
                quad_list.append(2)
            else:
                quad = 3
                quad_list.append(3)
        quad_total[key]=quad_list
        #at this point, you may have all points in one quadrant or in many 
        #quadrants
        #group the slices together and separate by hemisphere (q0q1 or q2q3)
    slice_list=[]
    for ii in mloc_dict.keys():
        slice_list.append(ii)

    slice_diff = np.diff(slice_list) #the difference between slices
    slice_change = np.where(slice_diff > 10)
    #to convert this tuple output into an int, use
    #result = [int(x) for x, in slice_change]
    
    #if(len(slice_change > 0)):
    #    #this is where a new pin starts
    #    slice_list[slice_change]
    #if we go more than 10 slices between metal points, they're likely not 
    #part of the same pin and this should constitute a new pin or set
    
    mid_slice = slice_list[slice_change[0][0]+1]#np.floor(nz/2) #this will be the cutoff to catch a new pin pair
    ### better way to extract the array value as scalar????
# =============================================================================
# Break up the pins per hemisphere by the quadrant they're in
# =============================================================================
    full_list={} #setup for the first hemisphere of points
    full_list[0]=[] #initial setup with two pin list areas
    full_list[1]=[]
    #full_points are the row,col values for points, with one list for each 
    #quadrant
    slice_marker={}
    slice_marker[0]=[]
    slice_marker[1]=[]
    slice_marker[2]=[]
    slice_marker[3]=[]
    full_points={}
    full_points[0] = []
    full_points[1] = []
    full_points[2] = []
    full_points[3] = []
    
    lower_hemisphere = {}
    upper_hemisphere = {}
    first_quad = 99 #placeholder for the first quadrant found in the hemisphere
    for count,ii in enumerate(mloc_dict.keys()):
        if (ii ==  mid_slice):
            full_list={} #container for all the rc points in this hemisphere
            #copy out the lower hemisphere and reuse the container
            lower_hemisphere = deepcopy(full_points)
            lower_marker = deepcopy(slice_marker)
            slice_marker ={}
            slice_marker[0]=[]
            slice_marker[1]=[]
            slice_marker[2]=[]
            slice_marker[3]=[]
            full_points={}
            full_points[0] = []
            full_points[1] = []
            full_points[2] = []
            full_points[3] = []
        if (ii == mid_slice):
            #set up a list container in the dictionary. Each of these will 
            #hold the contents from the first or second quadrant
            #
            # NEEDS additional code for cases that straddle the boundaries and
            # for the possibility of additional objects
            #
            full_list[0]=[]
            full_list[1]=[]
        if (ii <= mid_slice):
            #this is the first hemisphere, break out the quadrants found. 
            #ideally, there should only be two pins found per hemisphere
            #get all the points per each quadrant, they should belong to one 
            #pin each
            #--quick check to see if only one quadrant here
            qcheck = set(quad_total[ii])
            qcheck = list(qcheck)
            if (len(qcheck) ==1):
                if (first_quad == 99):
                    first_quad = qcheck
                
                for jcounter,jj in enumerate(quad_total[ii]):
                    full_points[qcheck[0]].append(mloc_dict[ii][jcounter])
                    slice_marker[qcheck[0]].append(ii)
                    #full_list[qcheck[0]].append(jj)
            elif (len(qcheck) ==2): #there are points from different quadrants here
                qcheck = set(quad_total[ii])
                qcheck = list(qcheck)
                num_vals = len(qcheck)
# =============================================================================
#                 ASSUMPTION is for only two pin quadrants to be found
# =============================================================================
                for jcounter,jj in enumerate(quad_total[ii]):
                    if (jj == qcheck[0]):
                        full_points[qcheck[0]].append(mloc_dict[ii][jcounter])
                        slice_marker[qcheck[0]].append(ii)
                    else:
                        full_points[qcheck[1]].append(mloc_dict[ii][jcounter])
                        slice_marker[qcheck[1]].append(ii)
            else:
                print('!!!! Found a 3rd or empty quadrant return !!!!')

        else:
            qcheck = set(quad_total[ii])
            qcheck = list(qcheck)
            if (len(qcheck) ==1):
                
                for jcounter,jj in enumerate(quad_total[ii]):
                    full_points[qcheck[0]].append(mloc_dict[ii][jcounter])
                    slice_marker[qcheck[0]].append(ii)
                    #full_list[qcheck[0]].append(jj)
            elif (len(qcheck) ==2): #there are points from different quadrants here
                qcheck = set(quad_total[ii])
                qcheck = list(qcheck)
                num_vals = len(qcheck)
# =============================================================================
#                 ASSUMPTION is for only two pin quadrants to be found
# =============================================================================
                for jcounter,jj in enumerate(quad_total[ii]):
                    if (jj == qcheck[0]):
                        full_points[qcheck[0]].append(mloc_dict[ii][jcounter])
                        slice_marker[qcheck[0]].append(ii)
                    else:
                        full_points[qcheck[1]].append(mloc_dict[ii][jcounter])
                        slice_marker[qcheck[1]].append(ii)
            else:
                print('!!!! Found a 3rd or empty quadrant return !!!!')

    upper_hemisphere = deepcopy(full_points)
    upper_marker = deepcopy(slice_marker)

    return lower_hemisphere, upper_hemisphere,lower_marker, upper_marker