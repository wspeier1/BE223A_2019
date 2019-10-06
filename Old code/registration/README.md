# 224B

# Dependencies

- Python 3.6 or higher
- Modules: os, cv2, pandas, pydicom, PIL, SITK
- Installation of Fiji image viewing system

# Preparation

This implementation is able to handle 2D dicom images or pngs corresponding to two time series (usually baseline scan and first interval scan). 

# Master CSV

A csv is required that should be titled Master.
The first column should include patient ID's, then the name of the first imaging file, and then the name of the second imaging file. E.g. (A01, A011234, A012345).

# Masks

Masks to segment the area of interest should be provided. It is recommended to create these in ImageJ with the freehand tool, then Edit > Selection > Create mask, then File > Save as > PNG. Be sure to save the mask as the same name as the original imaging file in the Mask1/ or Mask2/ folder (see documentation below). Note using the shift key allows selection of multiple areas.

# Program

The os.chdir should be changed to the location of the folder where all input and output for this process will be stored. All components should be moved into this folder including the sitk.py scripts and the master.csv. 

The first module of the program sets up folders that will include all relevant parts of the program. After these are set, this module should be silenced with a hash.

Dicom images should be placed into folders Image1/ and Image2/.

Mask images should be placed into folders Mask1/ and Mask2/.

There are 3 registration processes that are included, sitk1, sitk b-spline, and sitk exhaustive. Additional documentation may be found on the sitk page. The composite image from each approach will be saved for each series and designated by -1, -bs (b-spline), or -ex (exhaustive).

# Options

The default comparison metric is joint histogram mutual information. To change this requires navigating to each sitk python script and looking for the following line:

R.SetMetricAsJointHistogramMutualInformation()
