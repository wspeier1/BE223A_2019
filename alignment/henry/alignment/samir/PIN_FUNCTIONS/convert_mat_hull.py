
'''
MATLAB HULL FILE IMPORT AND TRANSFORM TO NII SPACE

'''
def convert_mat_hull(hull_path,
                     hull_file_name,
                     mrow,mcol,mz,
                     sx,sy,sz,hh):
    from numpy.linalg import inv
    import numpy as np
    import os
    import scipy.io as sio
    import matplotlib.pyplot as plt

    print('reading hull .mat file from ', hull_path)
    #test_path = '/content/gdrive/My Drive/BIOENG223A_FALL_2019/data/DBS_bG02'
    #hull_file_name = 'hull.mat'

    hull_file = os.path.join(hull_path, hull_file_name)
    print(hull_file)

    hull_data = sio.loadmat(hull_file)
    print('data shape is',np.shape(hull_data))
    print(type(hull_data))
    print(hull_data.keys()) #'mask_indices' is the main key for this dict
    mdata =hull_data['mask_indices']
    print('mdata type ',type(mdata))
    print('mdata shape',np.shape(mdata))
    [hrows, hcols]= np.shape(mdata)  #get the size of the hull data


    #print(img)   #show the NII image header info available
    #[sx,sy,sz,hh]=img.get_sform()  #pull srow data, hh is the homologous row


    #put the arrays together in one 2D stack. Column stack will put srow's in column
    T=np.column_stack((sx,sy,sz,hh))
    print(T)

    #Multiply the data by the transform
    #mdata needs a column of ones to make it n x 4 to multiply with a 4x4
    Xcol = np.ones((hrows,1))
    hdata = np.hstack((mdata,Xcol))

    #new transformed data, should be the xzy image coordinates (needs rounding)
    hull_form = np.dot(hdata,inv(T)) 

    print(np.shape(hull_form))
    hull_form = np.around(hull_form,0)

    #print(hull_form[100:110,:])

    '''
    From the NIFTI header,it will show these transform sets
    srow_x          : [-4.7020197e-02 -2.6496649e-03  9.9777776e-01 -8.0972633e+01]
    srow_y          : [-9.98893976e-01  1.24692917e-04 -4.69677448e-02  1.05718796e+02]
    srow_z          : [ 0.0000000e+00 -9.9999642e-01 -2.6496649e-03  1.1021884e+02]

    In MATLAB, they'll appear as this when loaded with the NIFTI read
    T =

    -0.0470   -0.9989         0         0
    -0.0026    0.0001   -1.0000         0
    0.9978   -0.0470   -0.0026         0
    -80.9726  105.7188  110.2188    1.0000


    The INVERSE of T can be used to go from .mat coordinates (CT) to image that 
    allows the hull to exist in the plane with the NIFTI data
    -- use matlab data  [data ones(size(data,1))] * inv(T) to spit out new xyz
    coordinates. Round these new values and set a zeros matrix the size of your
    image to get a 1 wherever there's an xyz point



    '''


    #data is the original NII image loaded in. We want to make another image of this
    #same size to hold the hull points
    #print('size of expected data is ', np.shape(data))
    #[mrow,mcol, mz] = np.shape(data) 
    new_hull = np.zeros((mrow,mcol, mz))

    [number_h_rows,number_h_cols]= np.shape(hull_form)
    for ii in range(0,number_h_rows):
        [xx,yy,zz,dump] = hull_form[ii,:].astype(int)
        #print('xx,yy,zz: ', xx,yy,zz)
        new_hull[xx,yy,zz]= 1


    #sanity check, see if a hull shows up on a middle slice
    plt.figure()
    plt.imshow(new_hull[:,:,np.int(mz/2)],cmap='jet')




    '''
    The below can be used to plot the original .mat hull image data
    %matplotlib inline
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    xdata = mdata[:,0]
    ydata = mdata[:,1]
    zdata = mdata[:,2]

    ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Reds');
    plt.xlabel('X')
    plt.ylabel('Y')

    plt.show()
    plt.figure()
    plt.imshow(mdata[:,0],mdata[:,1])
    '''

    return new_hull




