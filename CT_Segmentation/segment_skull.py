""" Finds Skull and segments out of CT Scan

Usage:
python segment_skull.py -c [path_to_CT]\
   --hull [path_to_hull_mat]\
   -o [folder_to_write_output]\
   -s [subject_name]

Add -p flag to view results as matplotlib image

"""
import os
import argparse
import nibabel as nib
from scipy.spatial import ConvexHull
import helper_functions.visualizations as vis
import helper_functions.reshape_data as rd
import helper_functions.filter_CT as fct
import helper_functions.manipulate_hull as mh
import matplotlib.pyplot as plt

def segment_skull(
    ct: str,
    hull: str,
    output_dir: str,
    subject: str,
    preview: bool,
  ):
    print('\nLOADING CT')
    # Load Preop_CT
    preop_CT = nib.load(ct)
    preop_CT_data = preop_CT.get_fdata()

    print('\nLOADING HULL')
    # Load Hull
    hull_idx = mh.load_hull_from_mat(hull, preop_CT)

    print('\nCREATING CONVEX HULL')
    # Create convex hull object
    point_cloud = hull_idx[:,:3]
    hull_hull = ConvexHull(point_cloud)

    print('\nNORMALIZING AND RESHAPING CT DATA')
    # Get long CT Data
    long_data = rd.voxels_to_4D(fct.min_max_normalize(preop_CT_data), is_norm=True)

    print('\nSCALING HULL')
    # Scale Hull by 110% (1.1)
    scaled = mh.scale_hull(hull_idx, 1.1)
    scaled_hull = ConvexHull(scaled[:,:3])

    print('\nFILTERING CT FOR REGIONS OUTSIDE ORIGINAL HULL')
    # Filter long CT Data for data within hull
    hull_filt_in = fct.filter_in_hull(long_data, hull_hull, filt_out=False)

    print('\nFILTERING CT FOR REGIONS INSIDE SCALED HULL')
    hull_filt_both = fct.filter_in_hull(hull_filt_in, scaled_hull, filt_out=True)

    print('\nFILTERING CT FOR UPPER REGIONS USED IN CT')
    # Remove lower portion from below points in linear plane drawn from y(x=0) = 100 --> y(x=256) = 160
    lower_removed = fct.remove_lower_regions(hull_filt_both, preop_CT_data.shape, init_point=100, end_point=150)
    voxel_rem = rd.long_to_voxels(lower_removed, preop_CT_data.shape)

    print('\nSHOWING PREVIEW')
    if preview:
      vis.compare_filtered_original(preop_CT_data, voxel_rem)
      plt.show()
    
    file_name = os.path.join(
        args.output_dir,
        args.subject + '_skull.nii'
    )
    print('\nSAVING OUTPUT TO:', file_name)
    feature_CT = nib.nifti2.Nifti2Image(voxel_rem, preop_CT.affine, header=preop_CT.header)
    nib.nifti2.save(feature_CT, file_name)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Segment Skull from Preoperative CT Scans")
  parser.add_argument('-c', '--ct', dest='ct', help='Path to nifti file containing preoperative CT scan', required=True)
  parser.add_argument('--hull', dest='hull', help='Path to mat file with hull coordinates', required=True)
  parser.add_argument('-o', '--output-dir', dest='output_dir', help='Directory to send output files to', default='output')
  parser.add_argument('-s', '--subject-name', dest='subject', help='Desired name for subject', required=True)
  parser.add_argument('-p', '--preview', dest='preview', help='Show preview', action='store_true')

  args = parser.parse_args()
  segment_skull(
    args.ct,
    args.hull,
    args.output_dir,
    args.subject,
    args.preview
  )