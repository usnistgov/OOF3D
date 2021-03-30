# -*- python -*-
# $RCSfile: deformationwidget.py,v $
# $Revision: 1.8.18.2 $
# $Author: langer $
# $Date: 2014/05/15 15:06:16 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.engine import deformation
from ooflib.common.IO.GUI import regclassfactory
from ooflib.engine.IO.GUI import meshparamwidgets

class DeformationTypeWidget(regclassfactory.RegisteredClassFactory,
                       meshparamwidgets.IndexableWidget,
                       meshparamwidgets.InvariandWidget):
    def __init__(self, value, scope, name, verbose=False):
        regclassfactory.RegisteredClassFactory.__init__(
            self, deformation.DeformationType.registry, obj=value,
            scope=scope, name=name, verbose=verbose)

def _makeDeformationParameterWidget(self, scope=None, verbose=False):
    return DeformationTypeWidget(self.value, scope=scope, name=self.name,
                                 verbose=verbose)

deformation.DeformationTypeParameter.makeWidget = _makeDeformationParameterWidget

#Note: Sometimes "param" is used in place of "self"
