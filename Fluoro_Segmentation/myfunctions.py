import numpy as np 
import matplotlib as plt


def showArray (array_path1,array_path2):
    for i in range (len(array_path1)):
        path1 = np.load(array_path1[i],mmap_mode = 'r+')
        path2 = np.load(array_path2[i],mmap_mode = 'r+')
        fig, ax = plt.subplots(ncols=2, nrows=1, figsize=(20, 10))
        ax[0].imshow(path1, cmap=plt.cm.gray)
        ax[1].imshow(path2, cmap=plt.cm.gray)
        
        
def loadAll (array_path):
	im = []
	for i in range (len(array_path)):
		im.append(np.load(array_path[i]))
	#	print("successfully loaded", array_path[i])
#	print("successfully loaded all")
	return im

def findXY (matrix):
    row,col = matrix.shape
    lst = []
    for r in range(row):
        for c in range(col):
            if matrix[r][c] == 1:
                lst.append((r,c))
    return lst