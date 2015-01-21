# -*- python -*-
# $RCSfile: adaptivemeshrefineWidget.py,v $
# $Revision: 1.15.2.2 $
# $Author: langer $
# $Date: 2013/11/08 20:45:05 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 


from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common.IO.GUI import chooser
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import whowidget
from ooflib.engine import errorestimator
from ooflib.engine import skeletoncontext
from ooflib.engine import subproblemcontext
from ooflib.engine.IO.GUI import meshparamwidgets
import ooflib.engine.mesh

import string

skeletonContexts = skeletoncontext.skeletonContexts

class AMRWhoParameterWidget(whowidget.WhoParameterWidget):
    def __init__(self, whoclass, value=None, scope=None, name=None):
        self.skelwidget = scope.findWidget(
            lambda x: isinstance(x, whowidget.WhoWidget)
            and x.whoclass is skeletonContexts)
        whowidget.WhoParameterWidgetBase.__init__(self, whoclass,
                                                  value=value, scope=scope,
                                                  name=name)

        # switchboard callbacks
        self.sbcallbacks = [
            switchboard.requestCallbackMain(self.skelwidget,
                                            self.skelwidgetChanged),
            switchboard.requestCallbackMain(('who changed', 'Skeleton'),
                                            self.skelModified),
            switchboard.requestCallbackMain('mesh status changed',
                                            self.meshStatusChanged)]
        
    def widgetCB(self, interactive):
        # Gives an "OK" sign only when the current skeleton object is
        # the base skeleton of the to-be-refined mesh.
        try:
            # Supplying skelwidget.get_value seems enough. If the
            # whoclass is a subproblem, the mesh and subproblem names
            # also get filled in the choosers.
            self.set_value(self.skelwidget.get_value())
            # If the following throws an exception, the skeleton
            # cannot be modified. Even if it does not throw an
            # exception, there may still be insufficient information
            # to do AMR.
            subproblem = subproblemcontext.subproblems[self.get_value()]
            # Already sure that the current skeleton object is the
            # base skeleton of the to-be-refined mesh.  
            meshctxt = subproblem.getParent()
            self.widgetChanged(not meshctxt.outOfSync(), interactive)
        except KeyError:
            self.widgetChanged(0, interactive)

    # Callback for "skelwidget" change in Skeleton Page.
    def skelwidgetChanged(self, *args, **kwargs):
        self.widgetCB(False)

    # Callback for skeleton modification (modify, undo, redo).
    def skelModified(self, *args, **kwargs):
        self.widgetCB(False)

    def meshStatusChanged(self, meshctxt):
        self.widgetCB(False)

    def cleanUp(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        whowidget.WhoParameterWidgetBase.cleanUp(self)
                        
def _AMRWhoParameter_makeWidget(self, scope=None):
    return AMRWhoParameterWidget(self.whoclass, self.value, scope=scope)

errorestimator.AMRWhoParameter.makeWidget = _AMRWhoParameter_makeWidget

# #AMR subproblem

# # This widget is for specifying a subproblem target for the AMR on the
# # FE Mesh page AMRWhoParameter defined above is for the refinement
# # target on the Skeleton page.
# class AMRMeshWhoParameterWidget(whowidget.WhoParameterWidget):
#     def __init__(self, whoclass, value=None, scope=None, name=None):
#         self.meshwidget = scope.findWidget(
#             lambda x: isinstance(x, whowidget.WhoWidget)
#             and x.whoclass is ooflib.engine.mesh.meshes)
#         #If we want the widgets associated with this parameter to
#         #always reflect the main widgets on the Task page,
#         #we have to have callbacks for all these
# ##        self.skelwidget = scope.findWidget(
# ##            lambda x: isinstance(x, whowidget.WhoWidget)
# ##            and x.whoclass is skeletonContexts)
# ##        self.mswidget = scope.findWidget(
# ##            lambda x: isinstance(x, whowidget.WhoWidget)
# ##            and x.whoclass is microStructures)
#         whowidget.WhoParameterWidgetBase.__init__(self, whoclass,
#                                                   value=value, scope=scope,
#                                                   name=name)

#         # switchboard callbacks
#         self.sbcallbacks = [
#             switchboard.requestCallbackMain(self.meshwidget,
#                                             self.meshwidgetChanged)
# ##            switchboard.requestCallbackMain(self.skelwidget,
# ##                                            self.meshwidgetChanged),
# ##            switchboard.requestCallbackMain(self.mswidget,
# ##                                            self.meshwidgetChanged)

# ##            switchboard.requestCallbackMain(('who changed', 'Skeleton'),
# ##                                            self.skelModified),
# ##            switchboard.requestCallbackMain('Mesh reverted',
# ##                                            self.meshReverted)
#             ]
        
#     def widgetCB(self, interactive):
#         try:
#             #AMR subproblem
#             #Supplying meshwidget.get_value seems enough. If the whoclass is a subproblem,
#             #the subproblem names also get filled in the choosers.
#             if self.meshwidget.get_value():
#                 self.set_value(self.meshwidget.get_value())
# ##            elif self.skelwidget.get_value(): #if there is no mesh
# ##                self.set_value(self.skelwidget.get_value())
# ##            elif self.mswidget.get_value(): #if there is no skeleton
# ##                self.set_value(self.mswidget.get_value())
#             #If the following throws an exception, the mesh cannot be modified. Even
#             #if it does not throw an exception, there may still be insufficient information to
#             #do AMR.
#             subproblem=subproblemcontext.subproblems[self.get_value()]
#             self.widgetChanged(1,interactive)
#         except KeyError:
#             self.widgetChanged(0, interactive)

#     # Callback for "meshwidget" change in FE Mesh Page.
#     def meshwidgetChanged(self, *args, **kwargs):
#         self.widgetCB(1)

# ##    # Callback for skeleton modification (modify, undo, redo).
# ##    def skelModified(self, *args, **kwargs):
# ##        self.widgetCB(1)
        
# ##    # Callback for reverted mesh.
# ##    def meshReverted(self, *args, **kwargs):
# ##        self.widgetCB(1)

#     def cleanUp(self):
#         map(switchboard.removeCallback, self.sbcallbacks)
#         whowidget.WhoParameterWidgetBase.cleanUp(self)
                        
# def _AMRMeshWhoParameter_makeWidget(self, scope=None):
#     return AMRMeshWhoParameterWidget(self.whoclass, self.value, scope=scope)

# adaptivemeshrefinement.AMRMeshWhoParameter.makeWidget = _AMRMeshWhoParameter_makeWidget

##################################

# class MeshSkeletonParameterWidget(parameterwidgets.ParameterWidget):
#     def __init__(self, scope=None, name=None):
#         self.meshwidget = scope.findWidget(
#             lambda x: isinstance(x, whowidget.WhoWidget)
#             and x.whoclass is ooflib.engine.mesh.meshes)
#         self.update()
#         self.widget = chooser.ChooserWidget(self.nameset,
#                                             callback=self.selection, name=name)
#         parameterwidgets.ParameterWidget.__init__(self, self.widget.gtk, scope)
#         self.widgetChanged(len(self.nameset) > 1, interactive=1)
#         self.set_value(self.nameset[0])  # initial value
#         # switchboard callbacks
#         self.sbcallbacks= [switchboard.requestCallbackMain(
#             ('new who', 'Mesh'), self.newMeshCreated)]
#     def update(self):
#         try:
#             self.mesh = ooflib.engine.mesh.meshes[self.meshwidget.get_value()]
#             # no. of stored skeletons in the mesh
#             nskels = len(self.mesh.skeleton_buffer)
#             # make a nameset.
#             # ["Base Skeleton 0", "Base Skeleton 1" ...]
#             self.nameset = ["Base Skeleton "+`i` for i in range(nskels)]
#         except KeyError:
#             self.nameset = [""]
#     def updateWidget(self):
#         self.widget.update(self.nameset)
#     def newMeshCreated(self, *args):
#         self.update()
#         self.updateWidget()
#     def selection(self, gtkobj, name):
#         self.value = name
#         index = int(string.split(name)[-1])
#         validity = self.mesh.skeleton_buffer.current() is not \
#                    self.mesh.skeleton_buffer[index]
#         self.widgetChanged(validity=validity, interactive=1)
#     def get_value(self):
#         return self.value
#     def set_value(self, value):
#         self.value = value
#         self.widget.set_state(value)
#     def cleanUp(self):
#         map(switchboard.removeCallback, self.sbcallbacks)
#         parameterwidgets.ParameterWidget.cleanUp(self)
        
# def _MeshSkeletonParameter_makeWidget(self, scope=None):
#     return MeshSkeletonParameterWidget(scope=scope, name=self.name)

# revertmesh.MeshSkeletonParameter.makeWidget = _MeshSkeletonParameter_makeWidget

#########################################

class ZZFluxParameterWidget(meshparamwidgets.SubProblemFluxParameterWidget):
    def __init__(self, param, scope, name=None):
        meshparamwidgets.SubProblemFluxParameterWidget.__init__(self, param,
                                                                scope, name)

        self.meshChangedCB()
        self.sbcallbacks += [switchboard.requestCallbackMain(
            ('new who', 'Mesh'), self.meshChangedCB)]

    def meshChangedCB(self, *args):
        mesh = self.getSource()           # really SubProblem
        if mesh:
            self.widgetChanged(mesh.has_solution(), interactive=1)
        
def _ZZFluxParameter_makeWidget(param, scope):
    return ZZFluxParameterWidget(param, scope=scope, name=param.name)

errorestimator.ZZFluxParameter.makeWidget = _ZZFluxParameter_makeWidget
