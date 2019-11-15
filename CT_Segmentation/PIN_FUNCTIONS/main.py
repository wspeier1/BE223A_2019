import os
import numpy as np

from copy import copy, deepcopy  #to copy matrices

import matplotlib.pyplot as plt
import matplotlib.animation as animation #just for animating a plot

#generic toolset for transformations
import scipy.misc
from scipy import ndimage
import scipy.io as sio
from scipy import signal  #for convolution filtering
import cv2 as cv2

from get_dirs import get_dirs
from get_nii_files import get_nii_files
from replace_nan import replace_nan
from create_binary_nifti import create_binary_nifti
from convert_mat_hull import convert_mat_hull
from load_hull_file import load_hull_file
from apply_marker_to_metal import apply_marker_to_metal
from get_center_hull import get_center_hull
from scale_hull import scale_hull
from find_metal_mass import find_metal_mass

def main():
    #get_dirs('/home/kgonzalez/BE223A_2019/data')

    #
    # Debug settings
    #
    run_all = 1 #set to 1 to go through every code block
    show_figs = 1
    write_figs = 1

    #set up image output directory
    output_image_base = '/home/kgonzalez/BE223A_2019/CT_Segmentation/PIN_NII'


### MAIN DIRECTORY NAMES
    gdir = '/home/kgonzalez/BE223A_2019/data/'
    main_directory = gdir

    sub_dirs = sorted(os.listdir(main_directory))
    print(sub_dirs)

    file_dict={}  #hold all of the nii files
    path_dict = {}

    for ii in range(0,len(sub_dirs)):
        print(sub_dirs[ii])

        current_path = os.path.join(main_directory,sub_dirs[ii])
        file_list = os.listdir(current_path)
        print(file_list)

        extension = '.nii'
        counter = 0    #numbered listing of .nii files found
        for jj in range(len(file_list)):
            if file_list[jj].endswith('.nii'):
                print('found file: ',file_list[jj])


                file_dict[ii,counter]= file_list[jj]
                path_dict[ii,counter] = current_path
                counter = counter + 1


#now we have all the nii files in the folders

#
# Get all of the patient directories below our main folder
#
    dir_list,file_list = get_dirs(gdir)
    for ii in dir_list:
        print(ii)

    #Build list of all PreOP CT NIFTI files found
    nii_files = get_nii_files(main_directory,dir_list, file_list, "preopCT",".nii")
    
    
    
###############################################################################

    #
    #Alter this for custom single runs
    #
    start_index =0
    stop_index = 0
    if (run_all == 1):
        stop_index = len(nii_files)
    #stop_index = len(nii_files)
    print('number of loops will be', stop_index)
    

    for loop in range(start_index,stop_index):
        print('-----PATIENT FOLDERS AVAILABLE-----')
        folder_key=[]
        for ii in enumerate(nii_files):
            print(ii[0],ii[1])
            folder_key.append( ii[1])
    
        print('enter patient #')
        patient_id = loop #input() 1 is subject 5
    
    
        nii_input_file = os.path.join(main_directory,
                                  folder_key[patient_id],
                                  nii_files[folder_key[patient_id]])
        print(nii_input_file)
        
        #######################################################################
        #data for writing image files out
        #######################################################################
        image_folder_id=nii_files[folder_key[patient_id]]
        im_filename, file_extension = os.path.splitext(image_folder_id)
        print('Suggested image folder name: ',im_filename)
        image_directory =os.path.join(output_image_base,im_filename)
        if not os.path.exists(image_directory):
            print('BASE path does not exist. trying to make')
            os.mkdir(image_directory)
    
    ###############################################################################
    #
    #    Kernels and other operators 
    #
        
        kernel_circle = [ [0,1,0], [1,1,1],[0,1,0]]
        kernel_square = [ [1,1,1],[1,1,1],[1,1,1] ]
        print(np.matrix(kernel_circle))
        
        prewitt_x = [[-1, 0 ,1],[-1,0,1],[-1 ,0 ,1]]
        prewitt_y = [[-1,-1,-1],[0,0,0], [1,1,1]]
        print(np.matrix(prewitt_x))
        print(np.matrix(prewitt_y))
        
    ###############################################################################
    
    ################################################################################
    #Get stacked image with all of the NaNs removed and simple metal location found
    ################################################################################
    
        #
        #import numpy as np
        #
        import nibabel as nib
        import matplotlib.pyplot as plt
        
        #input patient full file name from previous block
        f = nii_input_file
        img = nib.load(f)
        data = img.get_fdata()
        
        # Show original image
        print('NII filename opened is ',f)
        
        
        ### DEBUG PLOT AND CIRCLES ONLY
        fig, ax = plt.subplots()
        snum = 134 #axial slicing
        plt.imshow(data[:,:,snum],cmap='hot')
        plt.xlabel('columns')
        plt.ylabel('rows')
        plt.title('Axial Slice image')
        plt.colorbar()
        
        circle1 = plt.Circle((200,200), 10,color='b', fill=False)
        ax.set_aspect(1)
        ax.add_artist(circle1)
        plt.show()
        
        #Zoomed area view
        #
        
        fig = plt.gcf()
        ax = fig.gca()
        plt.imshow(data[200:230,160:175,snum], cmap='hot')
        plt.xlabel('columns')
        plt.ylabel('rows')
        plt.title('Zoomed Area')
        plt.colorbar()
        plt.show()
        
        
        sum = np.sum(data[215:220,145:155,snum])
        avg = np.average(data[215:220,145:155,140])
        print('average is ', avg)
        
        
        plt.figure()
        plt.imshow(data[215:230,145:170,snum])
        plt.colorbar()
        plt.title('Zoomed into metal part')
        
        
        
        
        # 
        # Remove any NaN values before running over this data
        #
        sx,sy,sz = np.shape(data)
        
        for ii in range(0,sz):
            #replace all NaN values with a default value
            new_data = replace_nan(data[:,:,ii], lowval=-1600)   
            if(ii ==0):
                stacked = new_data
            else:
                stacked = np.dstack([stacked,new_data])
        
        print('NaN Removal on original data Complete')
        
        plt.figure()
        plt.imshow(stacked[:,:,140],cmap='jet')
        plt.title('STACKED 140z')
        
        
        #
        # Create a binary NIFTI file the same size as our input data
        #
        numrows, numcols, depth = np.shape(stacked)
    
        output_nii=create_binary_nifti(numrows,numcols, depth)
        
        
    ###############################################################################
    #
    #   Load Hull file containing cortical surface boundaries
    #
        
        #print(dir_list)
        #print(file_list)
        
        #check for NII hull files first, otherwise check to see if a .mat version is
        #available
        #
        hull_nii_files = get_nii_files(main_directory,dir_list, file_list, "hull",".nii")
        hull_mat_files = get_nii_files(main_directory, dir_list,file_list, "hull", ".mat")
        
        print('folder is ',folder_key[patient_id])
        
        
        
        
        if (hull_nii_files.get(folder_key[patient_id],'NONE') != 'NONE'):
            hull_present = 1
            print(hull_nii_files[folder_key[patient_id]])
            a=folder_key[patient_id]
            hull_nii_files[a]
            print('folder key hull is ',hull_nii_files[folder_key[patient_id]])
        
            #patientid = 'subject_5'
            print(folder_key[patient_id])
            hull_file = os.path.join(main_directory ,
                                    folder_key[patient_id],
                                    hull_nii_files.get(folder_key[patient_id],'NONE'))
            hull_data = load_hull_file(hull_file)
            print(np.shape(hull_data))
        
        elif(hull_mat_files.get(folder_key[patient_id],'NONE') != 'NONE'):
            print('found a .mat HULL file: ',hull_mat_files.get(folder_key[patient_id]))
            #
            #get the information needed to retrieve and format .mat hull data
            #
            [mrow,mcol, mz] = np.shape(data)
            [sx,sy,sz,hh]=img.get_sform()
        
            hull_path = os.path.join(main_directory, folder_key[patient_id])
            hull_file_name = hull_mat_files.get(folder_key[patient_id])
            hull_data = convert_mat_hull(hull_path,
                                         hull_file_name,
                                         mrow, mcol, mz,
                                         sx,sy,sz,hh)
            hull_present = 1
        
        else:
            print('!!!!No HULL available for use!!!!!')
            hull_present = 0    
        
    ###############################################################################
    #
    #    --------------------------------------------------------------------------------
    #    Apply a filter to the data before detecting metallic components
    #    --------------------------------------------------------------------------------
    #
        
    
        
        
        
        # Taking a matrix of size 3 as the kernel 
        kernel = np.ones((3,3), np.float) 
        
        
        # The first parameter is the original image, 
        # kernel is the matrix with which image is  
        # convolved and third parameter is the number  
        # of iterations, which will determine how much  
        # you want to erode/dilate a given image.  
        #img_slice = stacked[:,:,144]
        #img_erosion = cv2.erode(img_slice, kernel, iterations=1) 
        #img_erode_dilate = cv2.dilate(img_erosion, kernel, iterations=1)
        #img_dilation = cv2.dilate(img_slice, kernel, iterations=1)
        
        
        #-------------------------------------------------------------------------------
        # Apply erosion and dilation
        #-------------------------------------------------------------------------------
        sx,sy,sz = np.shape(stacked)
        
        pz = deepcopy(stacked)
        erd_data = deepcopy(stacked)
        
        # do an erosion followed by dilation. Try a prewitt edge detection filter for
        #comparison
        for ii in range(0,sz):
            erd_data[:,:,ii] =cv2.erode(stacked[:,:,ii],kernel, iterations=1)
            pz[:,:,ii] = ndimage.prewitt(stacked[:,:,ii])
            erd_data[:,:,ii] = cv2.dilate(erd_data[:,:,ii],kernel,iterations=1)
        
        print('COMPLETED OPEN SEQUENCE')
        
        #try a dilation in the orthogonal slice plane
        #for ii in range(0,sy):
        #    erd_data[:,ii,:] =cv2.dilate(stacked[:,ii,:],kernel, iterations=1)
        
        
        #subtraction of original and opened image
        diff_data = np.subtract(erd_data,stacked)
        plt.figure()
        plt.imshow(diff_data[:,:,140],cmap='jet')
        plt.colorbar()
        plt.title('DIFFERENCE OPEN - ORIGINAL slice@z=140')
        
        plt.figure()
        plt.imshow(erd_data[:,:,140],cmap='jet')
        plt.title('OPENED IMAGE @z')
        
        plt.figure()
        plt.imshow(stacked[:,:,140],cmap='jet')
        plt.title('ORIGINAL IMAGE @z')
        
        plt.figure()
        plt.imshow(pz[:,:,140],cmap='jet')
        plt.colorbar()
        plt.title('Prewitt Edge along Z')
        
        plt.figure()
        diffp = np.subtract(stacked,pz)
        plt.imshow(diffp[:,:,140],cmap='jet')
        plt.colorbar()
        plt.title('Prewitt - original')
            
            
    ###############################################################################        
    #'''
    ################################################################################
    #Assign hull points from cube to dictionary. Dictionary points can be used to 
    #overlay onto images for a quick display
    #
    ################################################################################
    #    '''
        hull_dict={} #init dictionary
        centroid={}  #hold centroid vals
        
        hx,hy,hz = np.shape(hull_data)
        
        for hullslice in range(0,hz):
            hindex = np.argwhere(hull_data[:,:,hullslice] > 0.0)
            #print(np.shape(hindex))
            #print('len of hindex is ',len(hindex))
        
            if (len(hindex) == 0):
                #print('no hull found in slice ', hullslice)
                continue  #skip this one, no hull points found
        
            for ii in range(0,len(hindex)):
                hrow = hindex[ii][0]
                hcol = hindex[ii][1]
                #print('slice,row,col = ',hullslice, hrow, hcol)
        
                if hullslice not in hull_dict.keys():
                    hull_dict[hullslice]=[]
                    hull_dict[hullslice].append([hrow, hcol])
        
                    centroid[hullslice]=[]
                    centroid[hullslice].append([hrow,hcol])
        
                              
                else:
                    hull_dict[hullslice].append([hrow, hcol]) 
        
                    centroid[hullslice].append([hrow, hcol])
        
        print('Hull points transfered to dictionary')
        
        #
        # Get centroid values for row and column
        #
        
        
        
        #print('Applying hull points to erd data')
        if (write_figs == 1):
            hull_directory = os.path.join(image_directory,'HULL_OVERLAY')
            apply_marker_to_metal(hull_dict, 
                                erd_data, 0,
                                cmapin='bone',
                                marker_color='r',
                                write_to_disk =1,
                                output_folder = hull_directory)        
            
            
    ###############################################################################
    #    '''
        ################################################################################
    #    # Expand the hull to fit skull a bit more. If no hull nifit was found, 
    #    #skip this step for now
        ################################################################################
    #    '''
        hx,hy,hz = np.shape(stacked) #get size of newly created stack image
        if (hull_present == 1):
            total_slices = hz #total number of slices in the data
            mx,my,dx,dy = get_center_hull(hz, hull_dict)
        
            #debug outputs
            print('dx type is ',type(dx))
            print('mx type is ', type(mx))
            
            for ii in mx:
                print(ii)
        
            print('All keys found')
        
        
            #
            # Scale up the input hull by sf %
            #
            sf= 1.20 #1.02
            expanded_hull_dict = scale_hull(hz, mx, my,centroid,sf)
        
            #print(mx,my)
            #print(len(expanded_hull_dict))
        
        
            if (write_figs == 1):
                scaled_hull_directory = os.path.join(image_directory,
                                                     'SCALED_HULL_OVERLAY')
                apply_marker_to_metal(expanded_hull_dict, 
                                    stacked,0,
                                    cmapin='bone',
                                    marker_color='g',
                                    write_to_disk =1,
                                    output_folder = scaled_hull_directory)
    
    
    ###############################################################################
    #'''
    #CHECK THE CENTER POINT OF HULLS
    #'''
        center_dict={}
        for ii in mx.keys():
            center_dict[ii]=[]
            center_dict[ii].append([my[ii][0],mx[ii][0]])
        
        if (show_figs == 1):
            center_hull_directory = os.path.join(image_directory,
                                                     'HULL_CENTER_POINT_OVERLAY')
            apply_marker_to_metal(center_dict, 
                                stacked,0,
                                cmapin='bone',
                                marker_color='r',
                                write_to_disk=1,
                                output_folder = center_hull_directory)            
    
    ###############################################################################
    
    ################################################################################
    # ERD METAL LOCATIONS
    ################################################################################
    
        print('STARTING METAL LOCATION')
        sx,sy,sz = np.shape(erd_data)
        metal_points_erd=[]
        mloc_dict={}
        for ii in range(0,sz):
            slicenum = ii  #current slice
            onethirdslice = sz/3 #for a progress indicator
        
            if ((ii%50) == 0):
                print('ii now at ',ii)
            #replace all NaN values with a default value
            new_data_erd = erd_data[:,:,ii] #replace_nan(erd_data[:,:,ii], lowval=-1600)   
            #print('nan replaced')
            #stacked =np.dstack(stacked,new_data)
            loc_erd = find_metal_mass(new_data_erd,
                                    expanded_hull_dict,
                                    slicenum,
                                    dx,
                                    dy,
                                    mx,
                                    my,
                                    metal_value = 2000, 
                                    depth=1,
                                    lower_val=0.95,   
                                    upper_val = 1.50)
            #output of find_metal_mass is row, col, slice#
        
        
            print('loc_erd shape @ slice is ',np.shape(loc_erd),ii)
            if (len(loc_erd) ==0):
                #this is an empty list, due to not having any metallic signatures
                continue  #jump to the next slice
            else:
                #print('loc erd is ',loc_erd)
                for metal_pair in range(0,len(loc_erd)): #metal_pair in loc_erd:
                    if (metal_pair > 1):
                        #print('MANY LOC_ERD PAIRS')
                        pass
                    #print(type(metal_pair))
                    #print(metal_pair)
                    rownum = loc_erd[metal_pair][0]
                    colnum = loc_erd[metal_pair][1]
                    #assign the metal points for this slice to one key of the dictionary
        
        
        
                    if slicenum not in mloc_dict.keys():
                        mloc_dict[slicenum] =[]
                        mloc_dict[slicenum].append([rownum,colnum])
                    else:
                        mloc_dict[slicenum].append([rownum, colnum])
        
        print('Metal Points ERD Complete')
        print('#points to plot: ', len(mloc_dict.keys()))
        
        
        if (write_figs == 1):
            print('Applying metal markers to base images')
            metal_marker_directory = os.path.join(image_directory,
                                                     'METAL_POINT_OVERLAY')
            apply_marker_to_metal(mloc_dict,
                                  erd_data,
                                  1,
                                  'bone',    #cmap style
                                  'r', #marker color
                                  expanded_hull_dict,
                                  'g',
                                  write_to_disk=1,
                                  output_folder = metal_marker_directory)
    
    
    ###############################################################################
    
    ################################################################################
    #ASSIGN PIN POINTS TO NEW IMAGE
    ################################################################################
    
    
    #Find any pin points from above that live inside the hull
    
        for key in mloc_dict.keys():
            points = mloc_dict[key]
            for ii in range(0,len(points)):
                output_nii[points[ii][0],points[ii][1],key] = 1
    
    
    ###############################################################################
    ################################################################################
    # Save to a NIFTI file
    ################################################################################
    
    
    #nii_input_file = os.path.join(main_directory,
    #                              folder_key[patient_id],nii_files[folder_key[patient_id]])
    #print(nii_input_file)
    #>>> base=os.path.basename('/root/dir/sub/file.ext')
    #>>> base
    #'file.ext'
    #>>> os.path.splitext(base)
    #('file', '.ext')
    #>>> os.path.splitext(base)[0]
    
    
        #output_nii
        print(folder_key[patient_id])
        print(nii_files[folder_key[patient_id]])
        basename = os.path.basename(nii_files[folder_key[patient_id]])
        print(basename)
        rawname = os.path.splitext(basename)
        print(rawname[0])
        output_name = rawname[0] + '_PIN_TIPS.nii'
        
        output_img = nib.Nifti1Image(output_nii, img.affine, img.header)
        nifti_out_folder = '/home/kgonzalez/BE223A_2019/CT_Segmentation/PIN_NII'
        
        output_file = os.path.join(nifti_out_folder, output_name)  #'pin_output.nii')
        nib.save(output_img, output_file) #save the new NIFTI file
            
            