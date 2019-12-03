'''
################################################################################
Create the binary NIFTI file to be updated later
-- needs sizes for new data, original NIFTI header
################################################################################
'''
def create_binary_nifti(numrows,numcols, depth):

    import numpy as np

    binary_data=np.zeros((numrows, numcols, depth))

    print('Created 3D cube with sizes r x c x d: ', numrows, numcols, depth)

    return binary_data

