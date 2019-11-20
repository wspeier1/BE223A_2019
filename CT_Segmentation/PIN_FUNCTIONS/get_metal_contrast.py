'''
Get histogram of image and output the appropriate high values for metal objects

'''
import numpy as np
import matplotlib.pyplot as plt

def get_metal_contrast(full_data,numbins):
    
    nsize = np.shape(full_data)
    
    npoints = nsize[0]*nsize[1]*nsize[2]
    print('total pixels is ', npoints)
    
    
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