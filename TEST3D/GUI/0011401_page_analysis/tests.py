# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.2 $
# $Author: fyc $
# $Date: 2014/07/10 20:07:12 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from generics import *

def SetAnalysisCheck(analysises=None):
    return (chooserCheck('OOF3D:Analysis Page:Name:Retrieve', analysises))
    
def SetAnalysisSelect(analysis=None):
    return (chooserStateCheck('OOF3D:Analysis Page:Name:Retrieve', analysis))

def SetDestinationCheck(destinations=None):
    return (chooserCheck('OOF3D:Analysis Page:Destination:Chooser', destinations))
    
def SetDestinationSelect(destination=None):
    return (chooserStateCheck('OOF3D:Analysis Page:Destination:Chooser', destination))