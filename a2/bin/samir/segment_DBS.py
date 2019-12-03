""" Finds DBS leads in postop CT

Usage:
python segment_DBS.py -c [path_to_CT]\
   --hull [path_to_hull_mat]\
   -o [folder_to_write_output]\
   -s [subject_name]

Add -p flag to view results as matplotlib image

"""
import os
import sys
from typing import Tuple
import argparse
import nibabel as nib
from scipy.spatial import ConvexHull
import helper_functions.visualizations as vis
import helper_functions.reshape_data as rd
import helper_functions.filter_CT as fct
import helper_functions.manipulate_hull as mh
import matplotlib.pyplot as plt

def segment_DBS(
    ct: str,
    hull: str,
    output_dir: str,
    subject: str,
    preview: bool,
    save: bool = True
  ) -> nib.nifti1:
    """ Segment out DBS Leads
    
    Arguments:
        ct {str} -- path to CT nifti
        hull {str} -- path to .mat cortical hull
        output_dir {str} -- path to save output to (folder)
        subject {str} -- name of subject for output file name
        preview {bool} -- whether to show a preview
        save {bool} -- whether to save output or not
    
    Returns:
        Tuple(nib.nifti1, nib.nifti1) -- 2 nibabel nifti1 objects containing: skull vertices, full dense skull
    """
    print('\nLOADING CT')
    # Load Preop_CT
    postop_CT = nib.load(ct)
    postop_CT_data = postop_CT.get_fdata()

    print('\nLOADING HULL')
    # Load Hull
    hull_idx = mh.load_hull_from_mat(hull, postop_CT)

    print('\nCREATING CONVEX HULL')
    # Create convex hull object
    point_cloud = hull_idx[:,:3]
    hull_hull = ConvexHull(point_cloud)

    print('\nNORMALIZING AND RESHAPING CT DATA')
    # Get long CT Data
    long_data = rd.voxels_to_4D(fct.min_max_normalize(postop_CT_data), is_norm=True)

    print('\nFILTERING CT FOR REGIONS INSIDE CORTICAL HULL')
    # Filter long CT Data for data within hull
    hull_filt_in = fct.filter_in_hull(long_data, hull_hull, filt_out=True)

    print('\nAPPLYING MIN THRESHOLD TO ISOLATE LEADS')
    # Transform to voxel space
    post_inside_hull_vox = rd.long_to_voxels(
      hull_filt_in,
      postop_CT_data.shape
    )

    t = .7
    thresh_filt = post_inside_hull_vox.copy()
    thresh_filt[thresh_filt < t] = 0
    thresh_filt[thresh_filt >= t] = 1


    print('\nFINDING LARGEST CONNECTED COMPONENTS')
    DBS_leads_vox = fct.get_largest_connected_components(
      thresh_filt,
      num_comp=2
    )

    print('\nSHOWING PREVIEW')
    if preview:
      vis.compare_filtered_original(postop_CT_data, DBS_leads_vox)
      plt.show()
    
    file_name = os.path.join(
        output_dir,
        subject + '_DBS.nii'
    )
    print('\nSAVING DBS LEADS OUTPUT TO:', file_name)
    DBS_leads = nib.nifti1.Nifti1Image(DBS_leads_vox, postop_CT.affine, header=postop_CT.header)
    if save:
      nib.nifti1.save(DBS_leads, file_name)

    return DBS_leads

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Segment DBS Leads from Postoperative CT Scans")
  parser.add_argument('-c', '--ct', dest='ct', help='Path to nifti file containing postoperative CT scan', required=True)
  parser.add_argument('--hull', dest='hull', help='Path to mat file with hull coordinates', required=True)
  parser.add_argument('-o', '--output-dir', dest='output_dir', help='Directory to send output files to', default='output')
  parser.add_argument('-s', '--subject-name', dest='subject', help='Desired name for subject', required=True)
  parser.add_argument('-p', '--preview', dest='preview', help='Show preview', action='store_true')

  args = parser.parse_args()
  segment_DBS(
    args.ct,
    args.hull,
    args.output_dir,
    args.subject,
    args.preview,
    save=True
  )
