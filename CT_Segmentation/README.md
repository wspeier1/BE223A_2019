
# CT Segmentation section
-- Keane and Samir

## Skull and DBS Segmentation

### Directory Structure
- __segment_skull.py__: script that ties together pipeline to segment skull out of CT and save as nifti file
- __segment_DBS.py__: script that ties together pipeline to segment dbs out of postop CT and save as nifti file
- __helper_functions/__: Folder containing functions used in pipeline to segment skull and DBS leads
- __Segment_CT-SA.ipynb__: Notebook used to test/generate skull segmentation pipeline. Use to view intermediaries.
- __Segment_DBS-SA.ipynb__: Notebook used to test/generate DBS segmentation pipeline. Use to view intermediaries.

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

To segment the DBS leads from a a given subject run the following in bash:
```
python segment_DBS.py \
  --ct [PATH_TO_POSTOP_CT] \
  --hull [PATH_TO_HULL_MAT] \
  --output-dir [DIRECTORY_TO_SAVE_OUTPUT] \
  --subject-name [SUBJECT_NAME] \
  -p
```
  - The flag `-p` is used to show a preview image of the segmentation

For both skull and DBS python scripts, the wrapper function can be imported as a python function within other scripts, you may need to add regions to your python import path if running from outside this folder. For example, if you tried to import these functions from the directory above this one, you would run:
```python
import sys
sys.path.append('CT_Segmentation') # Replace with path to this folder

import CT_Segmentation.segment_skull as sk
import CT_Segmentation.segment_DBS as sdbs
```


### Packages Used
- Nibabel
- Numpy
- Scipy
- matplotlib
- progressbar2
