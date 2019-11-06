import numpy as np

def voxels_to_4D(ct_data):
  i, j, k = np.where(ct_data > 0)

  long_data = np.empty((len(i), 4), dtype=np.float64)
  q=0
  for x, y, z in zip(i,j,k):
      val = ct_data[x, y, z]
      long_data[q, :] = np.array([x, y, z,val])
      q+=1
  return long_data
