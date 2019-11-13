import numpy as np
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.feature import canny
from skimage.draw import circle_perimeter
from typing import List
import helper_functions.reshape_data as rd


def remove_ct_blocks(
  ct_data: np.ndarray,
  transverse_percent_remove: float,
  coronal_percent_remove: float,
  sagital_percent_remove: float,
  ) -> np.ndarray:
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
  """ filters for just pin tips set to 1 from ct_data

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
        for (j, k) in zip(circx, circy):
          pin_tip_matrix[i, j, k] = 1

  return pin_tip_matrix