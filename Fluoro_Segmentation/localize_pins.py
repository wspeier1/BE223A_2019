import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import cv2
import os
import csv
import random
from skimage import draw
from skimage import filters
from skimage import io, feature, measure
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu, threshold_local
from skimage.morphology import binary_erosion, binary_dilation, area_closing, area_opening

class PinTips_All(object):
	"""
	Constructor sets up the input and output images
	"""
	def __init__(self, root_dir, output_dir):
		self.root = root_dir
		self.output_dir = output_dir

	#returns a circle kernel
	def draw_circle(self, size, radius):
		arr = np.zeros(size)
		stroke = 3
		inner_radius = radius - (stroke//2) + (stroke%2) - 1
		outer_radius = radius + ((stroke+1) // 2)
		ri, ci = draw.circle(arr.shape[0]//2, arr.shape[1]//2, radius=inner_radius, shape=arr.shape)
		ro, co = draw.circle(arr.shape[0]//2, arr.shape[1]//2, radius=outer_radius, shape=arr.shape)
		arr[ro, co] = 1
		arr[ri, ci] = 1
		return arr.astype(np.uint8)

	#returns image after erosion and dilation
	def _erode_dilate(self, image, file_name, folder_name):
		#get a cross kernel
		kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
		horiz_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15,1))

		#area closing removes all dark structures of an image
		opening = area_closing(image, 50000)

		erode = binary_erosion(opening)
		#erode 2 times with horizontal kernel 
		for i in range(2):
			erode = binary_erosion(erode, horiz_kernel)

		#dilate 2 times with elliptical kernel
		dilate = binary_dilation(erode, kernel)
		for i in range(2):
			dilate = binary_dilation(dilate, kernel)

		output_path = folder_name + "\\" + file_name

		matplotlib.image.imsave(output_path, dilate)

		return dilate

	def _find_contour(self, original_image, contour_image, file_name, folder_name, writer):
		contours = measure.find_contours(contour_image, 0.8)
		contour_len = {}

		for n, contour in enumerate(contours):
			contour_len[n] = len(contour)

		#get the contours that is smallest
		temp = min(contour_len.items(), key=lambda x: x[1])

		fig, ax = plt.subplots()
		ax.imshow(original_image)
		"""
		Writing coordinates to a file
		"""
		unique_rows = np.unique(contours[temp[0]], axis=0)
		if unique_rows.shape[0]>7:
			index = random.sample(range(1, unique_rows.shape[0]), 8)
		else:
			index = np.arange(4)

		coords = unique_rows[index] #coordinates to write to csv file
		writer.writerow({'Subject': file_name, 'X':[arg for arg in coords[:,0]], 'Y':[arg for arg in coords[:,1]]})
		ax.plot(contours[temp[0]][:, 1], contours[temp[0]][:, 0], 'bo',linewidth=0.5)

		ax.axis('image')
		ax.set_xticks([])
		ax.set_yticks([])
		output_path = folder_name + "\\" + file_name
		
		plt.savefig(output_path)

	def extract_pin(self, block_size=205, offset=10):
		sub_dirs = [os.path.join(self.root, o) for o in os.listdir(self.root) if os.path.isdir(os.path.join(self.root,o))]
		file_name_counter = 0

		#create folder to store numpy files
		npy_folder = "npy"
		npy_folder_path = self.output_dir+"\\"+npy_folder+"\\"
		os.mkdir(npy_folder_path)

		#create folder for pin segmentation
		pins_folder = "pins"
		pins_folder_path = self.output_dir+"\\"+pins_folder+"\\"
		os.mkdir(pins_folder_path)

		#create folder to store numpy files
		area_opening_folder = "area_opening"
		area_opening_path = self.output_dir+"\\"+area_opening_folder+"\\"
		os.mkdir(area_opening_path)

		with open('coords.csv', 'w', newline='') as csvfile:
			fieldnames = ['Subject','X', 'Y']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writeheader()

			for arg in sub_dirs:
				for root, subdirectory, files in os.walk(arg):
					for file in files:
						extension = os.path.splitext(file)[1]
						if extension == '.tif':
							url = arg + '\\' + file
							print("Reading file -", url)
							image = rgb2gray(io.imread(url))

							#block size is 201 and offset is 10
							global_thresh = threshold_otsu(image)
							binary_global = image < global_thresh
							binary_global = binary_global*1

							#perform erosion, dilation then look for contours
							file_name_png = "{}_{}.png".format(os.path.splitext(file)[0], file_name_counter)

							output_path = self.output_dir + file_name_png
							
							matplotlib.image.imsave(output_path, binary_global)

							file_name_npy = "{}_{}.npy".format(os.path.splitext(file)[0], file_name_counter)
							npy_output = npy_folder_path + file_name_npy
							np.save(npy_output, binary_global)

							processed = self._erode_dilate(binary_global, file_name_png, area_opening_path)

							self._find_contour(binary_global, processed, file_name_png, pins_folder_path, writer)

							file_name_counter += 1

							break

root = "C:\\Users\\AnilYadav\\Desktop\\Projects\\brain\\data"
output_dir = "C:\\Users\\AnilYadav\\Desktop\\Projects\\brain\\output\\"

pins = PinTips_All(root, output_dir)
pins.extract_pin()
