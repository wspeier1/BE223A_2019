
'''
FIND METAL COMPONENTS-----------------------------------------------------------
'''
def find_metal_mass(section,
                    scaled_hull_dict,
                    slicenum,
                    dx,
                    dy,
                    mx,
                    my,
                    metal_value,
                    depth,
                    lower_val=0.95,
                    upper_val=1.1,
                    image_orient = 'PIR'):
    
    import numpy as np
    from is_point_in_hull import is_point_in_hull
    
    #upper_val = 1.15 #110% of incoming value
    #lower_val = 0.85
    
    #if PIR orientation, the python order should be rows start from Ant and
    #go to Post, the columns should start superior and move towards inferior.
    #The slice should start at 0 being Left and move to the Right
    #print('Image Orientation being used is: ', image_orient)
#    if (image_orient == 'PIR'):
#        print('row = A-P,col = S-I, z = L-R')
#    else:
#        print('!!! DIFFERING orientation found !!!')
    
    
    
    row1,col1 = np.shape(section) #section.shape() #should be just one slice
    #output_coordinates = set()

    output_coordinates = []

    #
    # Check to see if we have a hull in this slice. If we don't, skip this
    # slice, for now.
    #
    if slicenum not in scaled_hull_dict.keys():
        #print('NO HULL FOR THIS SLICE FOUND: ', slicenum)
        return output_coordinates


    #print('in find_metal_mass, row and col are ',row1, col1)
    for row in range(0,row1):
        for col in range(0,col1):
            #find a voxel that is surrounded on all 4 sides by the 
            #metal_value voxels depth wide
            pixel_x = col
            pixel_y = row

            if ((row - depth) >= 0):
                if ((col - depth) >= 0):
                    #if we're not on the boundaries, check to see if we have 
                    #voxel values around us within 10% of the metal_value

                    #if pixel - col depth : pixel + col depth AND
                    #if pixel - row depth: pixel + row depth are all within the
                    #range for metal, keep this pixel as a possible match

                    #avg_cols = np.average(section[row,col-depth:col+depth])
                    #avg_rows = np.average(section[row-depth:row+depth,col])
                    
                    # DEBUG -- averaging may not work well for our OPENED image
                    avg_cols = section[row,col]
                    avg_rows = section[row,col]
                    #print('row,col: avgc, avgr ', pixel_y, pixel_x,
                    #      avg_cols, avg_rows)
                    if ( (avg_cols >= (lower_val*metal_value) and (avg_cols <= (upper_val*metal_value))) \
                        and \
                        ((avg_rows >= (lower_val*metal_value)) and (avg_cols <= (upper_val*metal_value))) \
                        ):

                        #
                        # Check to see if this point is also within the hull
                        #
                        valid_point = 0
                        valid_point = is_point_in_hull(scaled_hull_dict,
                                                       slicenum,
                                                       mx,
                                                       my,
                                                       dx,
                                                       dy,
                                                       pixel_x,
                                                       pixel_y)
                        
                        #valid_point =1 #DEBUG ONLY!!!

                        #print('found one pixel')
                        #append a list of values per pixel instead of adding to 
                        #a large list of xy
                        if (valid_point == 1):

                            coordinate=[]
                            coordinate.append([pixel_y,pixel_x]) 
                            output_coordinates.append([pixel_y,pixel_x]) #coordinate)
                        #output_coordinates.append(pixel_y)
                        #output_coordinates.append(pixel_x)
                        
                    #sum_value = np.sum(section[row-depth:row+depth,col-depth:col+depth])
                    #print('sum_value ',sum_value)
    return output_coordinates

