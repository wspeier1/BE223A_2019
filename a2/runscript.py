# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 17:36:12 2019

@author: hwz62
"""

subject_folder='subject_1'

import sys
sys.path.insert(1, './bin/samir')
import segment_skull as skull
ct=subject_folder+'/preopCT_subject_1.nii'
hull=subject_folder+'/hull.mat'
out=subject_folder+'/SKULL_NII'
subject='subject_1'
preview=True
skull.segment_skull(ct,hull,out,subject,preview)

sys.path.insert(1, './bin/Anil')
import pin_tips_extract as ptx #import the class
path_to_fluro = subject_folder+"/fluoro_subject_1.tif" #path to file
fluro_object = ptx.PinTips(path_to_fluro) #create object (constructor takes the file path as parameter)
#extract the coordinates (variable will contain a tuple of arrays corresponding to x and y coordinates)
pin_coord = fluro_object.extract_pin()

import electrode_segmentation2
import numpy as np
#will need to change for Bill's input
raw_patient = np.array(['subject_1/fluoro_subject_1c.tif',
                        'subject_2/fluoro_subject_2b.jpg',
                        'subject_3/fluoro_subject_3.jpg',
                        'subject_4/fluoro_subject_4.jpg',
                        'subject_5/fluoro_subject_5.jpg'])
save_path = np.array(['patient_1.txt',
                      'patient_2.txt',
                      'patient_3.txt',
                      'patient_4.txt',
                      'patient_5.txt'])
out=electrode_segmentation2.electrode_detection(raw_patient[0],save_path[0])