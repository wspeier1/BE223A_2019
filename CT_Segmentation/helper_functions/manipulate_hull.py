from scipy.io import loadmat
from scipy.spatial import ConvexHull
import numpy as np
from typing import Tuple, List
import multiprocessing as mp
import helper_functions.reshape_data as rd
import progressbar

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

  # Calculate transformation from milimeter to voxel indices
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

def isInHull(coords, convex_hull):
    '''
    Datermine if the list of points P lies inside the hull
    :return: list
    List of boolean where true means that the point is inside the convex hull
    Taken from stack overflow user Cunningham in their answer:
    https://stackoverflow.com/a/52405173
    '''
    A = convex_hull.equations[:,0:-1]
    b = np.transpose(np.array([convex_hull.equations[:,-1]]))
    isInHull = np.all((A @ np.transpose(coords)) <= np.tile(-b,(1,len(coords))),axis=0)
    return isInHull

  
def check_in_hull_parallel(coords, convex_hull, chunk_size: int=50) -> List[bool]:
  """ Checks if coordinates within hull
  Splits coordinates in to subsets (chunks) of size chunk_size
  in order to run in parallel. returns boolean array
  
  Arguments:
      coords {[type]} -- array of shape 3xN
      hull {[type]} -- scipy.ConvexHull object created from hull
  
  Keyword Arguments:
      chunk_size {int} -- length of chunk (default: {50})
  
  Returns:
      List[bool] -- List of if chunk is in hull
  """

  # Split numpy array in to chunks
  print('...Splitting data in to chunks')
  splitted = np.array_split(coords, int(len(coords)/chunk_size))
  print('\tDone. Chunks created:', len(splitted))

  # Send as input to mp.pool.map
  print('...Creating inputs')
  inputs = [(pts, convex_hull) for pts in splitted]
  print('\tDone')

  #print(inputs)
  results = []
  print('...Computing if chunks in Hull')
  with mp.Pool() as pool:
    results = pool.starmap(isInHull, inputs)
  print('\tDone')

  return np.concatenate(results)

  
def calculate_hull_centroid(convex_hull, point_cloud):
  verts = point_cloud[convex_hull.vertices]
  return np.sum(verts, axis=0)/len(verts)

def scale_position(
    hull_point: np.ndarray,
    centroid: np.ndarray,
    scale_factor: float,
  ) -> np.ndarray:
  vec = hull_point[:3] - centroid
  position_scaled = hull_point.copy()
  position_scaled[:3] = (scale_factor * vec) + centroid
  return position_scaled

def scale_hull(hull_data: np.ndarray, scale_factor: float):
  points = hull_data[:,:3]
  hull = ConvexHull(points)
  centroid = calculate_hull_centroid(hull, points)
  print(centroid)
  scaled = hull_data.copy()
  for i in progressbar.progressbar(range(hull_data.shape[0])):
    scaled[i] = scale_position(
        hull_data[i],
        centroid,
        scale_factor,
      )
  return scaled

