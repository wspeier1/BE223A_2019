
'''
################################################################################
Check to see if xy location is within the expanded hull slice area
################################################################################
'''

def is_point_in_hull(scaled_hull_dict,
                     slicenum,  #slice 
                     meanx,     #mean of this hull slice
                     meany,
                     dx,
                     dy,
                     pixel_x,   #tip coordinates
                     pixel_y):
    import numpy as np
    
    
    point_valid = 0
    valid_pixel_distance = 10 #pixel line that is allowed from hull
    #
    # hull dictionary is slice with all row, cols matching
    #meany[hslice].
    if slicenum not in meanx.keys():
        #print("In is_point_in_hull, Key not found: ", slicenum)
        return point_valid
    #this is the mean center of the hull data for this slice
    center =[meany[slicenum], meanx[slicenum]] 

    #get distance from tip pixel to center of hull
    distance_tip_center_row = np.abs(pixel_y - np.abs(center[0]))
    distance_tip_center_col = np.abs(pixel_x - np.abs(center[1]))

    distance_tip_center = np.sqrt( np.power(distance_tip_center_row,2) + 
                              np.power(distance_tip_center_col,2))


    #find distance between tip point and all hull points
    #expanded_hull_dict[hslice].append([row ,col]) -- shape
    #
    #The hull points away from the tip pixels,but at a closer distance may bias
    #the detection. You can have hull shrink towards the center and all of those
    #points will usually be much closer than the hull-tip connection.
    nrows = 255 #size of 2D image
    ncol = 255
    
    ############################################################################
    #find the closest group of hull points
    ############################################################################

    smallest_value = 1000
    smallest_index=[]
    hull_to_tip=[]
    for ii in range(0,len(scaled_hull_dict[slicenum])):
        hx = scaled_hull_dict[slicenum][ii][1] #hull coordinates for each hullpt
        hy = scaled_hull_dict[slicenum][ii][0]       
        #distance between hull point in xy and tip points
        distance_hull_tipx = np.abs(pixel_x - hx)
        distance_hull_tipy = np.abs(pixel_y - hy)

        #if ((dx < nx*0.2) and (dy < ny*.2)):

        length_hull_tip = np.sqrt(np.power(distance_hull_tipx,2) + 
                                  np.power(distance_hull_tipy,2))
        hull_to_tip=length_hull_tip

        if (hull_to_tip < smallest_value):
            smallest_value = hull_to_tip
            smallest_index = ii
    #print('SMALLEST distance from hull to tip is ',smallest_value, smallest_index)
    ############################################################################
    ############################################################################

    #tip_hull_distance = 1000
    smallest_length = 1000
    for ii in range(smallest_index-1,smallest_index): #range(0,len(scaled_hull_dict[slicenum])):    
        hx = scaled_hull_dict[slicenum][ii][1] #hull coordinates for each hullpt
        hy = scaled_hull_dict[slicenum][ii][0]


        #Length of line between hull point and mean center
        length_hull_center_x = np.abs(hx - np.abs(center[1]))
        length_hull_center_y = np.abs(hy - np.abs(center[0]))
        length_hull_center = np.sqrt( np.power(length_hull_center_x,2) + np.power(length_hull_center_y,2)  )

        #distance between hull point in xy and tip points
        distance_hull_tipx = np.abs(pixel_x - hx)
        distance_hull_tipy = np.abs(pixel_y - hy)

        length_hull_tip = np.sqrt(np.power(distance_hull_tipx,2) + np.power(distance_hull_tipy,2))
        
        skip_point = 0
        if (length_hull_tip >= valid_pixel_distance):
            #keep hull points far away from taking up cpu
            skip_point = 1
            continue

        #if (length_hull_center < smallest_length):
        #    smallest_length = length_hull_center
        #    print('new smallest length = ',smallest_length)
        #else:
        #    print('Found a length hull center > 1000', length_hull_center)
            #keep the smallest tip to hull distance        
    if (skip_point == 0):
        print('skip point not activated')
        point_valid = 1

        #if (distance_tip_center <= (smallest_length*1.05)): #(tip_hull_distance*1.1)):
        #    #this should be a valid point
        #    point_valid = 1
        #    print('point valid')

        #    print('dist.tip_center & smallest length: ',
        #        distance_tip_center, smallest_length )




#
    return point_valid


