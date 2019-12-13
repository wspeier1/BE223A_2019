import numpy as np
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.feature import canny
from skimage.draw import circle_perimeter
from typing import List, Tuple
from scipy.spatial import ConvexHull
from scipy import ndimage
from matplotlib.path import Path
import helper_functions.reshape_data as rd
import helper_functions.manipulate_hull as mh
import progressbar


def remove_ct_blocks(
  ct_data: np.ndarray,
  transverse_percent_remove: float,
  coronal_percent_remove: float,
  sagital_percent_remove: float,
  ) -> np.ndarray:
  """ Removes blocks from ct data not used for pin tip isolation
  
  Arguments:
      ct_data {np.ndarray} -- preoperative ct image
      transverse_percent_remove {float} -- percent [0, 100] to remove
        along transverse plane
      coronal_percent_remove {float} -- percent [0, 100] to remove
        along coronal plane
      sagital_percent_remove {float} -- percent [0, 100] to remove
        along sagital plane
  
  Returns:
      np.ndarray -- block removed ct image
  """
  i_s, j_s, k_s = ct_data.shape

  top_i = int((i_s * transverse_percent_remove / 200) + i_s/2)
  bot_i =  int(- (i_s * transverse_percent_remove / 200) + i_s/2)

  top_j = int((j_s * transverse_percent_remove / 200) + j_s/2)
  bot_j =  int(- (j_s * transverse_percent_remove / 200) + j_s/2)

  top_k = int((k_s * coronal_percent_remove / 200) + k_s/2)
  bot_k =  int(- (k_s * coronal_percent_remove / 200) + k_s/2)

  fill_val = ct_data.min()
  filt_data = ct_data.copy()

  filt_data[bot_i:top_i,:,:] = fill_val

  filt_data[:,top_j:,:] = fill_val
  filt_data[:,:bot_j:,:] = fill_val

  filt_data[:,:,bot_k:top_k] = fill_val
  return filt_data

def min_max_normalize(data, scale=1):
  """ normalizes numpy array to values [0, 1] * scale
  
  Arguments:
      data {np.ndarray} -- data to normalize
  
  Keyword Arguments:
      scale {int} --  factor to multiply data by (default: {1})
  
  Returns:
      np.ndarray -- normalized, scaled data
  """
  min_val = np.nan_to_num(data).min()
  nan_fill = np.nan_to_num(data, nan=min_val)
  max_val = nan_fill.max()
  
  if max_val > 4000:
    print('Setting points > 3500 to 3500')
    nan_fill[nan_fill > 3500] = 3500

  print('Normalizing from:', nan_fill.min(), nan_fill.max())
  pos_val = nan_fill - nan_fill.min()
  norm = scale * pos_val / pos_val.max()
  print('To range:', norm.min(), norm.max())
  return norm


def isolate_pin_tips(
    ct_data: np.ndarray,
    threshold: float,
    hough_radii: List[float],
  ):
  """ **UNUSED FUNCTION** filters for just pin tips set to 1 from ct_data

  Function takes ct data, normalizes it from 0 to 1, and
  iterates through each slice on the first axis of the data.

  This should go through all coronal slices. Each slice is filtered
  for values above a threshold. This data is passed through a canny filter.
  Circles are found using hough circles. Perimiter of circles set to 1
  
  Arguments:
      ct_data {np.ndarray} -- Pre operative ct data
      threshold {float} -- threshold between 0 to 1 for max filtering
      hough_radii {List[float]} -- array of radii to check for circles
  
  Returns:
      np.ndarray -- array of same shape as ct_data with 1 for features
  """
  min_max_filt = min_max_normalize(ct_data)
  pin_tip_matrix = np.zeros(ct_data.shape)

  for i in range(ct_data.shape[0]):
    image_raw = np.nan_to_num(rd.get_slice(min_max_filt, 'i', i))
    max_filt_img = image_raw.copy()
    max_filt_img[max_filt_img < .6] = 0

    canny_filt = canny(max_filt_img, sigma=1)
    # Detect two radii
    hough_radii = hough_radii
    hough_res = hough_circle(canny_filt, hough_radii)
    # Select the most prominent 3 circles
    _, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii,
                                              total_num_peaks=2)

    for center_y, center_x, radius in zip(cy, cx, radii):
        circy, circx = circle_perimeter(center_y, center_x, radius,
                                        shape=image_raw.shape)
        for (k, j) in zip(circx, circy):
          pin_tip_matrix[i, j, k] = 1

  return pin_tip_matrix

def filter_in_hull(long_data: np.ndarray, hull: ConvexHull, filt_out: bool = False, chunk_size: int = 500):
  """ Removes data points within a specified convexHull
  
  Arguments:
      long_data {np.ndarray} -- Nx4 array of numpy coordinates
      hull {ConvexHull} -- Computed ConvexHull object
  
  Keyword Arguments:
      filt_out {bool} -- Set to true to remove points OUTSIDE hull 
        (default: {False})
  
  Returns:
      np.ndarray -- Nx4 filtered long_data
  """
  if long_data.shape[1] != 4:
    raise ValueError('Data must be of shape Nx4, found: ' + str(long_data.shape))
  coords = long_data[:,:3]
  is_in_hull = mh.check_in_hull_parallel(coords, hull, chunk_size=chunk_size)
  if filt_out:
    return long_data[is_in_hull]
  else:
    return long_data[~is_in_hull]

def is_above(point, equation) -> bool:
  """ Check if an x,y pair of coordinates lies below a line
  
  Arguments:
      point {List} -- point to check
      equation {Function} -- function to evaluate x coorindate 
        and return max y coordinate. Exmaple: y = lambda x: x + 1
  
  Returns:
      bool -- If point is below or above
  """
  max_point = equation(point[0])
  if point[1] < max_point:
    return True
  return False

def remove_lower_regions(long_data, shape, init_point=160, end_point=200):
  """ Removes section of CT not in Fluoro based on plane
  Plane is constant in Z, starts at y = init_point, 
  and ends at x = end_point. 
  
  Arguments:
      long_data {np.n darray} -- data of shape 4xN
      shape {Tuple} -- Tuple of ct voxel space shape
  
  Keyword Arguments:
      init_point {int} -- max y point at x=0 (default: {160})
      end_point {int} --  max y point at x at max(default: {200})
  
  Returns:
      np.ndarray -- returns filtered long data
  """
  # y - 160 = m(x - 0)
  # 200 - 160 = m(256 - 0)
  slope = (end_point - init_point)/(shape[0])
  plain = lambda x: (slope * (x)) + init_point

  res = []
  i = 0
  for point in progressbar.progressbar(long_data):
    res.append(is_above(point, plain))
    if i > 5:
      break
  return long_data[res]

def get_skull_vertices(
    filt_ct_data: np.ndarray,
    ct_shape: Tuple,
    thresh: float = 0,
    sigma: float = 1.0,
  ) -> Tuple:
  """ Returns vertices of convex hull from isolated
  
  Arguments:
      filt_ct_data {np.ndarray} -- CT Data filtered for area including skull
      ct_shape {Tuple} -- shape of ct voxels
  
  Keyword Arguments:
      thresh {float} --  Threshold on gaussian filtered data 
        range [-9 to 9](default: {0})
      sigma {float} --  gaussian filter standard deviation (default: {1.0})
  
  Raises:
      ValueError: Raises error if unable to binarize image
  
  Returns:
      Tuple(np.ndarray) -- Skull vertices, full skull. Each in
      4xN arrays.
  """

  g_filt = ndimage.gaussian_laplace(filt_ct_data, sigma=sigma)
  norm = g_filt.copy()
  norm[np.where(g_filt < thresh)] = 1
  norm[np.where(g_filt >= thresh)] = 0

  full_skull = rd.voxels_to_4D(norm, is_norm=True)

  hull_norm = ConvexHull(full_skull[:,:3])
  skull_vertices = full_skull[hull_norm.vertices]
  if not set(skull_vertices[:,3].tolist()) == set([1]):
    print(set(skull_vertices[:,3].tolist()))
    raise ValueError('Not binary')
  return (skull_vertices, full_skull)

def get_largest_connected_components(
    ct_data: np.ndarray,
    num_comp: int,
  ) -> np.ndarray:
  """ Finds n largest connected components in voxel space data
  
  Arguments:
      ct_data {np.ndarray} -- Voxel space CT data
      num_comp {int} -- number of largest components
  
  Returns:
      np.ndarray -- voxel space of just largest components in binary
  """
  # Label connected components
  label_im, nb_labels = ndimage.label(ct_data)

  # Find size of components
  sizes = ndimage.sum(ct_data, label_im, range(nb_labels + 1))

  # Get largest
  if len(sizes) == 1:
    n_largest = sizes[0]
  else:
    n_largest = sizes[(-sizes).argsort()[num_comp-1]]

  mask = sizes >= n_largest

  # Return largest connected component
  binary_img = mask[label_im]
  return binary_img.astype(float)

def threshold_long(long_data: np.ndarray, threshold: float):
    return long_data[np.where(long_data[:,3] > threshold)]
