# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
from scipy.sparse import csr_matrix

np.load("segmented_pin_tips.npy");
pt=np.load("segmented_pin_tips.npy");

A = csr_matrix(pt);
B,C=A.nonzero();

f=open('pt_fluoro.txt','w')
for i in range(len(B)):
    f.write("%d %d" % (B[i], C[i]))
    f.write('\n')
f.close()