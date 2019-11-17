
# CT Segmentation section
-- Keane and Samir

## Skull Segmentation

### Directory Structure
- __segment_skull.py__: script that ties together pipeline to segment skull out of CT and save as nifti file
- __helper_functions/__: Folder containing functions used in pipeline to segment skull
- __Segment_CT-SA.ipynb__: Notebook used to test/generate skull segmentation pipeline. Use to view intermediaries.

### Usage
To segment the skull from a a given subject run the following in bash:
```
python segment_skull.py \
  --ct [PATH_TO_CT] \
  --hull [PATH_TO_HULL_MAT] \
  --output-dir [DIRECTORY_TO_SAVE_OUTPUT] \
  --subject-name [SUBJECT_NAME] \
  -p
```
  - The flag `-p` is used to show a preview image of the segmentation

### Packages Used
- Nibabel
- Numpy
- Scipy
- matplotlib
- progressbar2
