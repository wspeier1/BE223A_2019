import numpy as np
from typing import Tuple
import progressbar

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
  for x, y, z in progressbar.progressbar(zip(i,j,k)):
      val = ct_data[x, y, z]
      long_data[q, :] = np.array([x, y, z, val])
      q += 1
  return long_data

def long_to_voxels(
    long_data: np.ndarray,
    output_shape: Tuple,
    fill_value: float = 0.0,
  ) -> np.ndarray:
  """ Turns data of shape 4xn to nxm space of original CT scan
  
  Arguments:
      long_data {np.ndarray} -- 4xn ndarray
      output_shape {Tuple} -- desired shape to match ct scan voxels
  
  Keyword Arguments:
      fill_value {float} -- data to fill for voxels not in long_data (default: {0.0})
  
  Returns:
       np.ndarray -- array of shape "output_shape"
  """
  matrix = np.zeros(output_shape) + fill_value
  for q in range(long_data.shape[0]):
    i, j, k, val = long_data[q]
    matrix[int(i), int(j), int(k)] = val
  return matrix

def voxels_to_4D_sample(data: np.ndarray, step_size: int) -> np.ndarray:
  """ Turns voxel space in to array of shape 4xN, filters out some points
  removes points corresponding to minimum value in voxel space data
  
  Arguments:
      data {np.ndarray} -- voxel space data
      step_size {int} -- number of points to skip in each direction of voxel space
  
  Returns:
      np.ndarray -- 4xN array
  """
  i, j, k = np.where(data > data.min())
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
  """ Flattens CT data by taking mean of an axis
  
  Arguments:
      ct_data {np.ndarray} -- voxel space ct data
      axis {int} -- axis to take mean of can be: 0, 1, 2
  
  Returns:
      np.ndarray -- flattened data
  """
  projection = np.nanmean(ct_data, axis=axis)
  return projection

def get_slice(ct_data: np.ndarray, direction: str, slice: int) -> np.ndarray:
  """ Get a 2D slice of 3D voxel data
  
  Arguments:
      ct_data {np.ndarray} -- voxel space CT data
      direction {str} -- direction (i, j, k) of slice
      slice {int} -- slice number
  
  Raises:
      ValueError: incorrect direction specified
  
  Returns:
      np.ndarray -- 2D image
  """
  if direction == 'i':
    return ct_data[slice,:,:]
  elif direction == 'j':
    return ct_data[:,slice,:]
  elif direction == 'k':
    return ct_data[:,:,slice]
  else:
    raise ValueError('Direction must be one of i, j, or k')
