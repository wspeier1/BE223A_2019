#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 00:00:17 2019

@author: alcummings
"""

from __future__ import print_function
from __future__ import division


import SimpleITK as sitk
import sys
import os
from math import pi

def command_iteration(method) :
    if (method.GetOptimizerIteration()==0):
        print("Scales: ", method.GetOptimizerScales())
    print("{0:3} = {1:7.5f} : {2}".format(method.GetOptimizerIteration(),
                                           method.GetMetricValue(),
                                           method.GetOptimizerPosition()))


if len ( sys.argv ) < 4:
    print( "Usage: {0} <fixedImageFilter> <movingImageFile>  <outputTransformFile>".format(sys.argv[0]))
    sys.exit ( 1 )

fixed = sitk.ReadImage(sys.argv[1], sitk.sitkFloat32)

moving = sitk.ReadImage(sys.argv[2], sitk.sitkFloat32)

R = sitk.ImageRegistrationMethod()

R.SetMetricAsJointHistogramMutualInformation()

sample_per_axis=12
if fixed.GetDimension() == 2:
    tx = sitk.Euler2DTransform()
    # Set the number of samples (radius) in each dimension, with a
    # default step size of 1.0
    R.SetOptimizerAsExhaustive([sample_per_axis//2,0,0])
    # Utilize the scale to set the step size for each dimension
    R.SetOptimizerScales([2.0*pi/sample_per_axis, 1.0,1.0])
elif fixed.GetDimension() == 3:
    tx = sitk.Euler3DTransform()
    R.SetOptimizerAsExhaustive([sample_per_axis//2,sample_per_axis//2,sample_per_axis//4,0,0,0])
    R.SetOptimizerScales([2.0*pi/sample_per_axis,2.0*pi/sample_per_axis,2.0*pi/sample_per_axis,1.0,1.0,1.0])

# Initialize the transform with a translation and the center of
# rotation from the moments of intensity.
tx = sitk.CenteredTransformInitializer(fixed, moving, tx)

R.SetInitialTransform(tx)

R.SetInterpolator(sitk.sitkLinear)

R.AddCommand( sitk.sitkIterationEvent, lambda: command_iteration(R) )

outTx = R.Execute(fixed, moving)

print("-------")
print(outTx)
print("Optimizer stop condition: {0}".format(R.GetOptimizerStopConditionDescription()))
print(" Iteration: {0}".format(R.GetOptimizerIteration()))
print(" Metric value: {0}".format(R.GetMetricValue()))


sitk.WriteTransform(outTx,  sys.argv[3])

if ( not "SITK_NOSHOW" in os.environ ):

    resampler = sitk.ResampleImageFilter()
    resampler.SetReferenceImage(fixed);
    resampler.SetInterpolator(sitk.sitkLinear)
    resampler.SetDefaultPixelValue(1)
    resampler.SetTransform(outTx)

    out = resampler.Execute(moving)

    simg1 = sitk.Cast(sitk.RescaleIntensity(fixed), sitk.sitkUInt8)
    simg2 = sitk.Cast(sitk.RescaleIntensity(out), sitk.sitkUInt8)
    cimg = sitk.Compose(simg1, simg2, simg1//2.+simg2//2.)
    sitk.Show( cimg, "ImageRegistrationExhaustive Composition" )
