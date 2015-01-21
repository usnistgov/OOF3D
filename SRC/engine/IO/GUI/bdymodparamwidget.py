# -*- python -*-
# $RCSfile: bdymodparamwidget.py,v $
# $Revision: 1.10.12.3 $
# $Author: langer $
# $Date: 2014/05/08 14:39:03 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Special widget for boundary modifier parameters -- has some
# intelligence to know whether its result should be a
# PointBoundaryModifier or an EdgeBoundaryModifier.

from ooflib.common.IO.GUI import regclassfactory
from ooflib.engine import boundarymodifier

class BoundaryModParamWidget(regclassfactory.RegisteredClassFactory):
    def __init__(self, registry, obj=None, title=None,
                 callback=None, fill=0, expand=0, scope=None, name=None,
                 verbose=False,
                 *args, **kwargs):
        # scope.parent is the ParameterDialog box in which we live.
        # The "boundary" value was set by
        # SkeletonBoundaryPage.modifyBoundaryCB before creating the
        # dialog containing this widget.
        self.boundary = scope.parent.boundary
        regclassfactory.RegisteredClassFactory.__init__(
            self, registry, obj=obj, title=title, callback=callback,
            fill=fill, expand=expand, scope=scope, name=name,
            verbose=verbose,
            *args, **kwargs)

    def includeRegistration(self, registration):
        return isinstance(self.boundary, registration.targets)


def _makeBMPWidget(self, scope, verbose=False):
    return BoundaryModParamWidget(self.registry,
                                  obj=self.value, scope=scope, name=self.name,
                                  verbose=verbose)

boundarymodifier.BoundaryModifierParameter.makeWidget = _makeBMPWidget
