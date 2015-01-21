# -*- python -*-
# $RCSfile: bdyinitparamwidget.py,v $
# $Revision: 1.1.4.4 $
# $Author: langer $
# $Date: 2014/11/07 20:31:08 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.common import debug
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import regclassfactory
from ooflib.common.IO.GUI import whowidget
from ooflib.engine import bdycondition
from ooflib.engine import mesh
from ooflib.engine.IO import boundaryconditionmenu

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class BCNameWidget(parameterwidgets.StringWidget):
    pass

def _bcNameParameter_makeWidget(self, scope=None, verbose=False):
    return BCNameWidget(self, scope=scope, name=self.name, verbose=verbose)

boundaryconditionmenu.BCNameParameter.makeWidget = _bcNameParameter_makeWidget

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class FloatBCInitWidget(regclassfactory.RegisteredClassFactory):
    def __init__(self, obj=None, title=None, callback=None,
                 fill=0, expand=0, scope=None, name=None,
                 verbose=False,
                 *args, **kwargs):
        meshwidget = scope.findWidget(
            lambda x: isinstance(x, whowidget.WhoWidget)
            and x.whoclass is mesh.meshes)
        meshctxt = mesh.meshes[meshwidget.get_value()]
        bcwidget = scope.findWidget(
            lambda x: isinstance(x, BCNameWidget))
        bc = meshctxt.getBdyCondition(bcwidget.get_value())
        self.time_derivs = (bc.field.time_derivative()
                            in meshctxt.all_initializable_fields())
        regclassfactory.RegisteredClassFactory.__init__(
            self, bdycondition.FloatBCInitMethod.registry, obj=obj,
            title=title, callback=callback, fill=fill, expand=expand,
            scope=scope, name=name, verbose=verbose, *args, **kwargs)
    def includeRegistration(self, reg):
        return self.time_derivs == reg.time_derivative

def _floatBCInitParam_makeWidget(self, scope=None, verbose=False):
    return FloatBCInitWidget(self, scope=scope, name=self.name, verbose=verbose)

bdycondition.FloatBCInitParameter.makeWidget = _floatBCInitParam_makeWidget

