# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 17:36:12 2019

@author: hwz62
"""

import segment_skull as skull
ct='subject_1/preopCT_subject_1.nii'
hull='subject_1/hull.mat'
out='SKULL_NII'
subject='subject_1'
preview=True
segment_skull.segment_skull(ct,hull,out,subject,preview)
skull.segment_skull(ct,hull,out,subject,preview)

run Anil/main.py

run Tina/electrode_segmentation.py