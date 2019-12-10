#import the file
import localize_pins as ptx

#provide path to the root folder that has sub folders of all subjects
path_to_root = "C:/user/all_subject_data"
#path to ouput folder
output = "C:/user/output/"

#create an object
fluro_object = ptx.PinTips_All(path_to_root, output)

#extract the coordinates (variable will contain a tuple of arrays corresponding to x and y coordinates)
fluro_object.extract_pin()


