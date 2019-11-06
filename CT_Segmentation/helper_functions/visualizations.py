import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy.stats as stats
from ..helper_functions.reshape_data import voxels_to_4D

def quick_plot_3D(
  ct_data,
  step_size: int = 50,
  ):
  long_data = voxels_to_4D(ct_data)

  fig = plt.figure(figsize=(16,16))
  ax = fig.add_subplot(111, projection='3d')
  step_size = 50

  vals = long_data[::step_size, 3]

  norm = (vals-min(vals))/(max(vals)-min(vals))
  colors = [(0, 0, 0, n) for n in norm]
  ax.scatter3D(long_data[::step_size, 0], long_data[::step_size, 1], long_data[::step_size, 2], c=colors)
