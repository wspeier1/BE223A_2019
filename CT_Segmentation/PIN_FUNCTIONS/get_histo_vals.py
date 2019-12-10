'''
Get histogram of image and output the appropriate high values for metal objects

'''
import cv2
from skimage import exposure #histogram equalization
import numpy as np
import matplotlib.pyplot as plt
import pdb

def get_histo_vals(full_data,numbins):
    
    nsize = np.shape(full_data)
    print('Size of data for NaN correction is: ',nsize)
    
    npoints = nsize[0]*nsize[1]*nsize[2]
    print('total pixels is ', npoints)
    
    
    # go through each slice and produce a histogram, then put them together
    

    #skip any NaN values when computing histogram
    [histvals,binsize]=np.histogram(full_data[~np.isnan(full_data)], \
    bins=np.arange(-1400, 6000, 24))
    
    plt.figure()
    plt.hist(histvals,binsize)
    tname = 'Slice'
    plt.title(tname)
    
    print('lowest values and bin#: ',histvals[0:10], binsize[0:10])
    print('highest values and bin#: ', histvals[-200:-1],binsize[-200:-1])

    #get the lowest value found for the data and the highest that has x number
    #of points to it
    np.size(histvals)
    lowvals = np.where(histvals[0:100] > 10)
    highvals = np.where(histvals > 10)
    print('lowvals= ',lowvals)
    print('lowvals[0] is ', lowvals[0][0])
    print('size of highvals is ', np.size(highvals))
    print('type &highvals= ',type(highvals),highvals[0][-200:-1])
    
    lowest_pixel_value = binsize[lowvals[0][0]]
    if (np.size(highvals) == 0):
        #leave highest value alone
        highest_pixel_value = binsize[highvals[0][-1]]
    else:
        print('!!!!! Found a VERY high voxel value')
        highest_pixel_value = 999999
    print('lowest value and highest value: ', lowest_pixel_value, highest_pixel_value)
    

    
    for ii in range(0,nsize[2]):
        full_data[:,:,ii] = exposure.equalize_hist(full_data[:,:,ii])
    

    return full_data
    
    
    hist,bins=np.histogram(full_data,numbins)
    plt.hist(hist,bins)
    print(np.shape(hist))
    print(np.shape(bins))
    print('hist: ',hist)
    print('bins:',bins)
    print(np.sum(hist))
    index=np.where(hist > 5)
    print(len(index[0]))
    print('hist value is ',hist[index[0][-1]])
    print('index is: ',index)
    topval = bins[-1]
    print('topval is ',topval)
    print('top cutoff is ',topval - topval*.35)
    topval - bins[0]
    
    for ii in range(0,len(bins)-1):
        print(bins[ii],hist[ii])
    
    
    return 0