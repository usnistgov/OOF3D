# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.2 $
# $Author: fyc $
# $Date: 2014/02/19 22:16:10 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from generics import *

def layersNumberCheck(number):
    return len(GraphicsListedLayersWhats('Graphics_1')) == number
    
def layerWhatCheck(*names):
    return GraphicsListedLayersWhats('Graphics_1') == names

def skeletonMicrostructureListCheck(*names):
    return chooserCheck('OOF3D:Skeleton Page:Microstructure', names)

def currentSkeletonMicrostructureCheck(name):
    return chooserStateCheck('OOF3D:Skeleton Page:Microstructure', name)
    
def skeletonListCheck(*names):
    return chooserCheck('OOF3D:Skeleton Page:Skeleton', names)

def currentSkeletonCheck(name):
    return chooserStateCheck('OOF3D:Skeleton Page:Skeleton', name)
