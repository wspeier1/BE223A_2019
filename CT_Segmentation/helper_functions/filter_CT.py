import numpy as np

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


  filt_data = ct_data.copy()

  filt_data[bot_i:top_i,:,:] = 0

  filt_data[:,top_j:,:] = 0
  filt_data[:,:bot_j:,:] = 0

  filt_data[:,:,bot_k:top_k] = 0

  return filt_data

def remove_pin_holders(ct_data):
  return 1
