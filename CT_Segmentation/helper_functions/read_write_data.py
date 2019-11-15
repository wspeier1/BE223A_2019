from scipy.io import loadmat
import numpy as np
from typing import Tuple
import helper_functions.reshape_data as rd

def load_hull_from_mat(
    hull_path: str,
    ct_object,
  ) -> np.ndarray:
  if hull_path.split('.')[-1] != 'mat':
    raise ValueError('Must input path to a file ending in .mat')

  # Import hull .mat file
  hull_mat = loadmat(hull_path)
  hull_coords = hull_mat['mask_indices']

  # Create array of vectors [[x, y, z, 1]...]
  one = np.ones((hull_coords.shape[0], 1))
  hull_4d = np.hstack((hull_coords, one))

  # Calculate transformation from milimeter to voxel
  aff = np.linalg.inv(ct_object.affine)
  hull_idx = np.rint(np.dot(hull_4d, aff.T))

  return hull_idx

def load_hull_voxel_matrix(
    hull_path: str,
    ct_object,
  ) -> np.ndarray:
  hull_idx = load_hull_from_mat(hull_path, ct_object)
  voxel_space_hull = rd.long_to_voxels(
    long_data=hull_idx, 
    output_shape=ct_object.get_fdata().shape,
    fill_value=0
    )
  return voxel_space_hull


  