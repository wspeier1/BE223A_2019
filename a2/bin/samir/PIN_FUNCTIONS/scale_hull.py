
'''
################################################################################
Expand hull scale to allow it to overlap the CT bone. The hull data in the
original file is a bit conservative at most points and usually sits within the
skull boundary, so pins may not contact it. Scale it up to make it within the
bone or maybe a bit on the outer bone

################################################################################
'''
def scale_hull(hz, mx,my,centroid,sf = 1.02):
    import numpy as np

    xpoints = []
    ypoints = []


    sf = 1.02 #scale factor

    expanded_hull_dict={}
    for hslice in range(0,hz):
        if hslice not in centroid:
            #print('no key for this slice ',hslice)
            continue
        numvals = len(centroid[hslice])
        if (numvals > 0):
            for ii in range(0, numvals):
                row = centroid[hslice][ii][0]
                col = centroid[hslice][ii][1]
                #row  = np.round(centroid[hslice][ii][0] * sf)
                #col = np.round(centroid[hslice][ii][1] * sf)
                ypoints.append(row)
                xpoints.append(col)
                if ((row - my[hslice]) <=0):
                    #push this point to -row
                    row = np.round(row * 1.0/sf)
                else:
                    row = np.round(row * sf)
                
                if ((col - mx[hslice]) <=0):
                    col = np.round(col * 1.0/sf)
                else:
                    col = np.round(col * sf)

                if (hslice not in expanded_hull_dict):
                    expanded_hull_dict[hslice]=[]
                    expanded_hull_dict[hslice].append([row ,col])
                else:
                    expanded_hull_dict[hslice].append([row ,col]) 


    return expanded_hull_dict
