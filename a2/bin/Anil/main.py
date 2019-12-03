#import the file
import pin_tips_extract as ptx
import sys
import csv

def main_func(path_to_fluro):

	#create an object
	fluro_object = ptx.PinTips(path_to_fluro)

	#extract the coordinates (variable will contain a tuple of arrays corresponding to x and y coordinates)
	pin_coord = fluro_object.extract_pin()

	
	#write data to a file
	with open('pin_tips_coords.csv', mode='w', newline='') as file:
		csv_writer = csv.writer(file, delimiter=',')
		for i in range(len(pin_coord[0])):
			csv_writer.writerow([pin_coord[0][i], pin_coord[1][i]])
	
	return pin_coord

path_to_fluro = "subject_1/fluoro_subject_1c.tif"

if __name__ == '__main__':
	main_func(path_to_fluro)