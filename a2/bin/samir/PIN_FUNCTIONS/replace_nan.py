'''
REPLACE NAN DATA----------------------------------------------------------------
'''
import numpy as np


def replace_nan(data, lowval=-1600):
    #a=np.isnan(data)
    #lowval = -1600
    new_data = data #only a slice should be sent in here
    new_data[np.isnan(new_data)]= lowval

    a = np.isnan(new_data)
    #print('sample value after nan replace (0,0) : ',new_data[0,0])
    sdata = new_data #new_data[215:220,145:155,140]
    row,col = np.shape(sdata)
    #print('nan replace shape is ', row,col)

    return sdata
