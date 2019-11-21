import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from skimage import io, feature
from skimage.filters import threshold_local

"""
Class -> PinTips()
----------------------
Required Parameter -> Path to File
Optional Parameter -> Boundary Box for Pin Tips
-------------------------
"""
class PinTips(object):
	def __init__(self, fluro_img=None, boundary_box=(530, 325, 66)):
		"""
		Constructor sets up the image and the boundary box
		"""
		if fluro_img:
			#read data as array (extract only one channel)
			self.fluro = io.imread(fluro_img)[:,:,0]
			self.shape = self.fluro.shape
			self.img_flag = True
			self.boundary = boundary_box
			"""
			Private Method -> "_adaptive_threshold()
			-------------------------------------
			Required Parameter -> Image to be Thresholded
			Optional Paramter -> Block Size for Local Thresholdng 
			-----------------------------------------------------
			"""
			self.binarized = self._adaptive_threshold(self.fluro)
		else:
			self.img_flag = False
			print("Image Required")
			return 	None
		

	def _adaptive_threshold(self, image, block_size=555):
		"""
		Returns the local thresholded images 
		"""
		if self.img_flag:
			adaptive_threshold = threshold_local(image, block_size, offset=10)
			binary_adaptive = image < adaptive_threshold
			return binary_adaptive*1
		else:
			return "Image Required"

	def draw_boundary(self, x_point, y_point, width):
		"""
		Returns the coordinate location of the boundary box
		"""
		left, right = (x_point-width, y_point), (x_point+width, y_point)
		down, top = (x_point, y_point+width), (x_point, y_point-width)
		return (left,right,top,down)
		
	def visualize(self, image=None, coords=False):
		"""
		Display the fluoro image, with the option of showing the boundary box coordinates
		"""
		if self.img_flag:		
			fig, axis = plt.subplots(nrows=1, ncols=1, figsize=(5,5))
			axis.imshow(image, cmap='gray')
		
			if coords:
				left, right, top, down = self.draw_boundary(self.boundary[1], self.boundary[0], self.boundary[2])
				axis.plot(self.boundary[1], self.boundary[0], 'ro')
				axis.plot(left[0], left[1], 'bo')
				#print(left)
				axis.plot(right[0], right[1], 'bo')
				#print(right)
				axis.plot(top[0], top[1], 'bo')
				#print(top)
				axis.plot(down[0], down[1], 'bo')
				#print(down)
			plt.show()
		else:
			return "Image Required"

	def extract_pin(self):
		"""
		Returns the row range and col range for the pin tips patch size
		"""
		if self.img_flag:
			left, right, top, down = self.draw_boundary(self.boundary[1], self.boundary[0], self.boundary[2])
			row_range = (top[1],down[1])
			col_range = (left[0],right[0])
			#mask for segmented image
			segmented = np.zeros(self.shape)

			for row_index in range(row_range[0], row_range[1]+1):
				for col_index in range(col_range[0], col_range[1]+1):
					segmented[row_index, col_index] = self.binarized[row_index, col_index]

			edges = feature.canny(segmented, sigma=1.5)

			#save results as image format
			matplotlib.image.imsave('pin_tip_edges.png', edges)
			matplotlib.image.imsave('segmented_pin_tips.png', segmented)

			"""
			fig, axis = plt.subplots(nrows=1, ncols=2, figsize=(5,5))
			axis[0].imshow(edges, cmap='gray')
			axis[1].imshow(segmented, cmap='gray')
			plt.show()
			"""
			return self._get_index(segmented)
		else:
			return "Image Required"

	def _get_index(self, binary_image=None):
		"""
		Return a tuple of arrays: first array is all Xs and second array is Ys
		"""
		index = np.where(binary_image==1)
		return index
