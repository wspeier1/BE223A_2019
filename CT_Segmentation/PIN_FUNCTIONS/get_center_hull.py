'''
################################################################################
Get center point of a set of hull values
################################################################################
'''

def get_center_hull(hz, hull_data):
    import numpy as np
    
    xpoints = {}
    ypoints ={}
    
    meany={}
    meanx={}
    dx ={}
    dy = {}
    tempcentroid={}
    for hslice in range(0,hz): #hz is number of slices
        if hslice not in hull_data:
            continue
        numvals = len(hull_data[hslice])
        if (numvals > 0):
            for ii in range(0, numvals):
                row = hull_data[hslice][ii][0]
                col = hull_data[hslice][ii][1]


                if(hslice not in ypoints):
                    ypoints[hslice]=[]
                    ypoints[hslice].append(row)


                else:
                    ypoints[hslice].append(row)

                if (hslice not in xpoints):
                    xpoints[hslice]=[]
                    xpoints[hslice].append(col)
                else:
                    xpoints[hslice].append(col)
        
        #print('mean of hull ypoints: ',np.mean(ypoints[hslice]))
        meany[hslice]=[]
        meanx[hslice]=[]
        meany[hslice].append(np.mean(ypoints[hslice]))
        meanx[hslice].append(np.mean(xpoints[hslice]))

        #get distance from mean to each point in hull slice
        numx = len(xpoints[hslice])
        dx[hslice]=[]
        dy[hslice]=[]
        for ii in range(0,numx):
            distancex = np.abs(meanx[hslice] - xpoints[hslice][ii])
            distancey = np.abs(meany[hslice] - ypoints[hslice][ii])

            dx[hslice].append(distancex)
            dy[hslice].append(distancey)





    return meanx, meany,dx,dy

