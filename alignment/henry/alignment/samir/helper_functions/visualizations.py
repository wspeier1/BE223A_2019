import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy.stats as stats
import helper_functions.reshape_data as rd 
import helper_functions.filter_CT as fct
from typing import List, Tuple

def quick_plot_3D(
  ct_data,
  ax: Axes3D = None,
  step_size: int = 50,
  is_long: bool = False,
  is_norm: bool = False,
  base_color: Tuple = (0, 0, 0),
  alpha_max: float = 1.0,
  ):
  """ Plots subsampled CT/MRI data
  
  Arguments:
      ct_data {Nibabel object data} -- Data from a nibabel object using the .get_fdata() method
        to shorten compute time, send the voxel_to_4D output and set the is_long variable to True.
  
  Keyword Arguments:
      step_size {int} -- sample step size 
        For example this function defaults to 1 point in 50 (default: {50})
      is_long {bool} -- set if precomputed 4D vector array using voxels_to_4D, shortens computation
      is_norm {bool} -- set if data is already normalized from 0 to 1 (default: False)
      base_color {Tuple} -- three value'd tuple of RGB values 
      alpha_max {float} -- value between 0 and 1 for transparancy
  """
  if not is_long:
    long_data = rd.voxels_to_4D(ct_data, is_norm)
  else:
    long_data = ct_data

  if is_norm:
    vals = long_data[::step_size, 3]
  else:
    vals = fct.min_max_normalize(long_data[::step_size, 3])

  if ax is None:
    fig = plt.figure(figsize=(16,16))
    ax = fig.add_subplot(111, projection='3d')


  colors = [(base_color[0], base_color[1],base_color[2], n * alpha_max) for n in vals]
  ax.scatter3D(long_data[::step_size, 0], long_data[::step_size, 1], long_data[::step_size, 2], c=colors)
  return ax

def compare_filtered_original(
    original_ct_data: np.ndarray,
    filtered_ct_data: np.ndarray,
  ):
  twoD_originals = [
    rd.project_ct_2D(original_ct_data, axis=0),
    rd.project_ct_2D(original_ct_data, axis=1),
    rd.project_ct_2D(original_ct_data, axis=2)
  ]
  twoD_filtered= [
    rd.project_ct_2D(filtered_ct_data, axis=0),
    rd.project_ct_2D(filtered_ct_data, axis=1),
    rd.project_ct_2D(filtered_ct_data, axis=2)
  ]

  _, axes = plt.subplots(nrows=2, ncols=3, figsize=(16, 8))
  for i in range(3):
    axes[0, i].imshow(twoD_originals[i])
    axes[1, i].imshow(twoD_filtered[i])
  return axes


def plot_slice(ct_data, direction: str, slice: int, ax = None):
  if ax is None:
    _, ax = plt.subplots(figsize=(8,8))

  ax.imshow(rd.get_slice(ct_data, direction, slice)) 

def compare_slices(
  data: List[np.ndarray],
  directions: List[str],
  slices: List[int],
  figsize=None,
  ):

  if len(data) != len(slices):
    raise ValueError('# of data matrices must equal # of slices specified')
  if len(data) != len(directions):
    raise ValueError('# of data matrices must equal # of directions specified')
  
  num_comparisons = len(slices)
  if not figsize:
    figsize = (8 * num_comparisons, 8)
  
  _, axes = plt.subplots(ncols=num_comparisons, nrows=1, figsize=figsize)

  for i in range(num_comparisons):
    ax = axes[i]
    ax.imshow(
      rd.get_slice(data[i], directions[i], slices[i])
    )
  return axes
  
  
