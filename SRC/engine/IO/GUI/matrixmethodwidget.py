# -*- python -*-
# $RCSfile: matrixmethodwidget.py,v $
# $Revision: 1.3.2.2 $
# $Author: langer $
# $Date: 2014/05/08 14:39:04 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common.IO import parameter
from ooflib.common.IO.GUI import regclassfactory
from ooflib.common.IO.GUI import whowidget
from ooflib.engine import matrixmethod
from ooflib.engine import subproblemcontext
from ooflib.engine import symstate
from ooflib.engine import timestepper


class AsymmetricMatrixMethodFactory(regclassfactory.RegisteredClassFactory):
    def includeRegistration(self, reg):
        return not reg.symmetricOnly

def _makeAsymMtxMethodWidget(self, scope=None, verbose=False):
    return AsymmetricMatrixMethodFactory(self.registry, obj=self.value,
                                         scope=scope, name=self.name,
                                         verbose=verbose)

matrixmethod.AsymmetricMatrixMethodParam.makeWidget = _makeAsymMtxMethodWidget

# # Widget for choosing the MatrixMethod to use with a TimeStepper.  The
# # widget is assumed to be a subwidget for a TimeStepper widget, so
# # that it will be rebuilt if the TimeStepper changes.  If it's not a
# # subwidget, then it will need to use switchboard callbacks to notice
# # if the TimeStepper changes.

# class MatrixMethodFactory(regclassfactory.RegisteredClassFactory):
#     def __init__(self, registry, obj=None, scope=None, name=None):
#         self.subprobwidget = scope.findWidget(
#             lambda w: (isinstance(w, whowidget.WhoWidget)
#                        and w.whoclass is subproblemcontext.subproblems))
#         self.subprobctxt = self.getSubProb()
#         self.stepdriverwidget = scope.findWidget(
#             lambda w: (isinstance(w, regclassfactory.RegisteredClassFactory)
#                        and w.registry is timestepper.StepDriver.registry))
#         self.timestepperwidget = self.findTimeStepperWidget(scope)
#         regclassfactory.RegisteredClassFactory.__init__(
#             self, registry, obj=obj, scope=scope, name=name)
#         self.sbcbs = [switchboard.requestCallbackMain(self.subprobwidget,
#                                                      self.updateCB),
#                       switchboard.requestCallbackMain(self.timestepperwidget,
#                                                       self.updateCB),
#                       switchboard.requestCallbackMain(self.stepdriverwidget,
#                                                       self.updateWidgetCB)]
#     def cleanUp(self):
#         map(switchboard.removeCallback, self.sbcbs)
#         regclassfactory.RegisteredClassFactory.cleanUp(self)
#     def getSubProb(self):
#         if self.subprobwidget.isValid():
#             return subproblemcontext.subproblems[self.subprobwidget.get_value()]
#     def updateCB(self, *args, **kwargs):
#         self.subprobctxt = self.getSubProb()
#         self.update(self.registry)
#     def updateWidgetCB(self, *args, **kwargs):
#         # When the StepDriver changes, the TimeStepper widget changes
#         self.timestepperwidget = self.findTimeStepperWidget(self.parent)
#         self.update(self.registry)
#     def findTimeStepperWidget(self, scope):
#         return scope.findWidget(
#             lambda w: (isinstance(w, regclassfactory.RegisteredClassFactory)
#                        and w.registry is timestepper.TimeStepper.registry))
#     def includeRegistration(self, reg):
#         # If the matrix is not symmetric or the time stepper creates
#         # asymmetric effective matrices, then exclude the solvers
#         # which *are* symmetric.

#         stepperreg = (self.timestepperwidget and 
#                       self.timestepperwidget.getRegistration())
#         if not self.subprobctxt:
#             asym = False
#         else:
#             # Not all StepDrivers have a TimeStepper argument -- the
#             # StaticDriver always uses a StaticStepper, so there's no
#             # parameter widget to be found.  In that case,
#             # self.timestepperwidget is None and the StepDriver
#             # registration is the one with the "asymmetric" function.
#             if stepperreg:
#                 asym = stepperreg.asymmetric(self.subprobctxt)
#             else:
#                 asym = self.stepdriverwidget.getRegistration().asymmetric(
#                     self.subprobctxt)
#         if asym:
#             return not reg.symmetricOnly
#         return True

# def _makeMatrixMethodWidget(self, scope=None):
#     return MatrixMethodFactory(self.registry, obj=self.value,
#                                scope=scope, name=self.name)

# matrixmethod.MatrixMethodParam.makeWidget = _makeMatrixMethodWidget
