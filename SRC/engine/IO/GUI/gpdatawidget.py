# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.engine.property.plasticity import cstress
from ooflib.common.IO.GUI import regclassfactory
from ooflib.engine.IO.GUI import meshparamwidgets

class GPDataTypeWidget(regclassfactory.RegisteredClassFactory,
                       meshparamwidgets.IndexableWidget,
                       meshparamwidgets.InvariandWidget):
    def __init__(self, value, scope, name, verbose=False):
        regclassfactory.RegisteredClassFactory.__init__(
            self, cstress.GaussPointDataOutput.registry, obj=value,
            scope=scope, name=name, verbose=verbose)

def _makeGPDataOutputParameterWidget(self, scope=None, verbose=False):
    return GPDataTypeWidget(self.value, scope=scope, name=self.name,
                            verbose=verbose)

cstress.GaussPointDataOutputParameter.makeWidget = _makeGPDataOutputParameterWidget

#Note: Sometimes "param" is used in place of "self"
