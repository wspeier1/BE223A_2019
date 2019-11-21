# Fluro Segmentation
-- Yadav, Anil

## Pin Tips Segmentation

### Usage

	- Note: The algorithm requires initial seed point (x,y) to work. The seed point is the area where pin tips could be potentially found.

To segment the Pin Tips from a given subject, run the following:
```
import pin_tips_extract as ptx #import the class
path_to_fluro = "subject/fluoro_subject_1.tif" #path to file
fluro_object = ptx.PinTips(path_to_fluro) #create object (constructor takes the file path as parameter)

#extract the coordinates (variable will contain a tuple of arrays corresponding to x and y coordinates)
pin_coord = fluro_object.extract_pin()
```

### Packages Used
- Numpy (matrix manipulation)
- Scikit-Image (image processing)
- matplotlib (visualization)