#import the file
import pin_tips_extract as ptx

#path to file
path_to_fluro = "subject/fluoro_subject_1.tif"

#create an object
fluro_object = ptx.PinTips(path_to_fluro)

#extract the coordinates (variable will contain a tuple of arrays corresponding to x and y coordinates)
pin_coord = fluro_object.extract_pin()

print(pin_coord)
