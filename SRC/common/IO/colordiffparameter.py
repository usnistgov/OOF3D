# -*- python -*-
# $RCSfile: colordiffparameter.py,v $
# $Revision: 1.7.18.2 $
# $Author: langer $
# $Date: 2014/09/27 22:34:00 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

import types
from ooflib.SWIG.common import colordifference
from ooflib.common.IO import parameter


class ColorDifferenceParameter(parameter.RegisteredParameter):
    def __init__(self, name, value=colordifference.deltargb(0.0, 0.0, 0.0),
                 default=colordifference.deltargb(0.0, 0.0, 0.0), tip=None,
                 auxData={}):
        parameter.RegisteredParameter.__init__(
            self, name, colordifference.ColorDifferencePtr, 
            value=value, default=default, tip=tip, auxData=auxData)
