#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
For a given hull file (3d), process each slice and downsample the points to 
speed up the operation and limit the points to a more inner bone line
'''
import numpy as np
import matplotlib.pyplot as plt
import pdb

def downsample_dense_skull(hull_data, slicenum=0):
    
    #get size of input hull data
    [nrow,ncol] = np.shape(hull_data)
    #
    # Create a new hull output of 0s
    #
    downsampled_hull_data = np.zeros([nrow,ncol])
    
    
    #pdb.set_trace()
    
    
    
    [rows,cols] = np.where(hull_data[:,:] > 0)
    
    
    # Get the mean center point of the hull
    mr = np.mean(rows)
    mc = np.mean(cols)
    
# =============================================================================
#     Get the angles present in this slice of data
# =============================================================================
    
    dx = []
    dy = []
    alpha=[]
    for ii in range(0,len(rows)):
        dx.append(mc - cols[ii])
        dy.append(mr- rows[ii])
        
        
# =============================================================================
# Find the angle associated with each hull point, from the mean center of the
# hull. Angles will go from 0 to 360 degrees, starting from 0 degrees on the 
# x axis (y=0) CCW to 360 degrees. Each 90 degree quadrant will be broken up to
#make the simple angles go to 360
# =============================================================================

        if ( (dx[ii] >= 0) and (dy[ii] >= 0)):
            #QUADRANT 1
            angle = np.arctan2(np.abs(dy[ii]),np.abs(dx[ii])) * 180.0/np.pi
        elif ( (dx[ii] <= 0) and (dy[ii] >= 0)):
            #QUADRANT 2
            angle = np.arctan2(np.abs(dy[ii]),np.abs(dx[ii])) * 180.0/np.pi + 90.0      
        elif ( (dx[ii] <= 0) and (dy[ii] <= 0)):
            #QUADRANT 3
            angle = np.arctan2(np.abs(dy[ii]),np.abs(dx[ii])) * 180.0/np.pi + 180.0   
        elif ( (dx[ii] >= 0) and (dy[ii] <= 0)):
            #QUADRANT 4
            angle = np.arctan2(np.abs(dy[ii]),np.abs(dx[ii])) * 180.0/np.pi + 270.0
        else:
            print('!!!!! Found an UNHANDLED ANGLE CALCULATION !!!!!')
        alpha.append(angle)
    
    alpha = np.sort(alpha) #put them in 0-360 degree order
    
    atol = np.mean(np.diff(np.sort(alpha)))
    print('mean dtheta  = ',atol)
    
    atol2 = 0.05 #difference between angle loop and angles found in hull allowed
    
    counter = 0
    
    #istep = 0
    
    alphaval={} #hold the 
    
    stored=[]
    counter=0
    for ii in np.arange(0,360,0.5):
        if (ii == 0):
            istep = 0
        else:
            istep = istep +1
        for jj in range(0,len(alpha)):
            if ( (alpha[jj] >= (ii - atol2)) and 
                (alpha[jj] <= (ii+atol2))):
                #this angle found earlier matches, keep it and add to the list
                if istep in alphaval.keys():
                    alphaval[istep].append(jj)
                else:
                    alphaval[istep]=[]
                    alphaval[istep].append(jj)
                    
                stored.append(jj)
                counter = counter + 1
    
    print('Length of stored is ', len(stored))
    stored=set(stored) #get only unique values
    stored=list(stored)
    
    
#    plt.figure()
#    #plt.imshow(hull_data[:,:,slicenum],cmap = 'bone')
#    plt.plot(cols[stored],rows[stored], color='red',
#             markersize=1,marker='.',linestyle='none')
#    #plt.plot(mc,mr,color='green',markersize=16, marker='o')
#    plt.title('Stored full points')
#    plt.show()
    
# =============================================================================
#     Get a single point around each angle arc around the hull
# =============================================================================
    midval=[]
    for anglestep in range(0,max(alphaval.keys())): #len(alphaval)):
        #each alphaval step is a small angle increment
        if anglestep in alphaval.keys():
            vals=[]
            vals.append(alphaval.get(anglestep)) #values()
            #
            # Get the middle distance point
            dvals=[]
            for num_angles in range(0,len(vals)):
                #for every angle in the list, find the distances to get the 
                #smallest one
                distance = np.sqrt( np.power(dy[vals[num_angles][0]],2) + 
                np.power(dx[vals[num_angles][0]],2))
                dvals.append(distance) #add this distance to the list
            #get the middle distance to keep
            svals = np.sort(dvals)
            middle=int(len(svals)/2) #get the index to the middle distance
            midval.extend(vals[middle])
            
    
#    plt.figure()
#    plt.plot(rows[midval],cols[midval],'r.', linestyle='none')
#    plt.show()
    
    
# =============================================================================
#     Fill in the new hull values with 1s
# =============================================================================
    downsampled_hull_data[rows[midval],cols[midval]] =1

    
    
    return downsampled_hull_data