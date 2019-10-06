import sys
import nibabel as nib
import numpy as np

def main():
	image_data = nib.load(sys.argv[1])
	data = image_data.get_data()
	data[np.isnan(data)] = 0
	new_image = nib.Nifti1Image(data, affine=np.eye(4))
	nib.save(new_image, sys.argv[2])

main()
