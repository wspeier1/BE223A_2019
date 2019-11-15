import numpy as np
from typing import Tuple

def voxels_to_4D(ct_data, is_norm=False) -> np.ndarray:
  """ Reshapes voxel space nifti data to a set of 4D vectors
  
  Arguments:
      ct_data -- result of .get_fdata() method on nibabel import
  
  Returns:
      [np.ndarray] -- A 4 x # of non-zero voxel numpy array
  """
  
  if is_norm:
    i, j, k = np.where(ct_data > 0)
  else:
    i, j, k = np.where(~np.isnan(ct_data))
  long_data = np.empty((len(i), 4), dtype=np.float64)
  q = 0
  for x, y, z in zip(i,j,k):
      val = ct_data[x, y, z]
      long_data[q, :] = np.array([x, y, z, val])
      q += 1
  return long_data

def long_to_voxels(
    long_data: np.ndarray,
    output_shape: Tuple,
    fill_value: float = 0.0,
  ):
  matrix = np.zeros(output_shape) + fill_value
  for q in range(long_data.shape[0]):
    i, j, k, val = long_data[q]
    matrix[int(i), int(j), int(k)] = val
  return matrix

def voxels_to_4D_sample(data, step_size: int) -> np.ndarray:
  i, j, k = np.where(data > 0)
  i_short = i[::step_size]
  j_short = j[::step_size]
  k_short = k[::step_size]
  long_data = np.empty((len(i_short), 4), dtype=np.float64)
  q = 0
  for x, y, z in zip(i_short, j_short, k_short):
      val = data[x, y, z]
      long_data[q, :] = np.array([x, y, z, val])
      q += 1
  return long_data

def project_ct_2D(ct_data, axis: int):
    projection = np.nanmean(ct_data, axis=axis)
    return projection

def get_slice(ct_data, direction: str, slice: int) -> np.ndarray:
  if direction == 'i':
    return ct_data[slice,:,:]
  elif direction == 'j':
    return ct_data[:,slice,:]
  elif direction == 'k':
    return ct_data[:,:,slice]
  else:
    raise ValueError('Direction must be one of i, j, or k')
