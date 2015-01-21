# -*- python -*-
# $RCSfile: skeletongroupwidgets.py,v $
# $Revision: 1.57.10.18 $
# $Author: langer $
# $Date: 2014/09/17 17:48:02 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import utils
from ooflib.common.IO import placeholder
from ooflib.common.IO.GUI import chooser
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import whowidget
from ooflib.engine import boundarybuilder
from ooflib.engine import boundarymodifier
from ooflib.engine import mesh
from ooflib.engine import skeletoncontext
from ooflib.engine.IO import skeletongroupparams
from ooflib.engine.IO.GUI import bdymodparamwidget

# Special widgets for the SkeletonGroup parameters.

# The "defaults" argument is used by the "Aggregate" widget, to
# provide a mechanism for picking sets of SkeletonSelectables which
# are not groups.  Currently only "<selection>" is available, but
# other examples could include "all", "none", and possibly others.

class SkeletonGroupWidget(parameterwidgets.ParameterWidget):
    def __init__(self, groups=[], defaults=utils.OrderedSet(), scope=None,
                 name=None, verbose=False):
        self.defaults = defaults
        self.widget = chooser.ChooserWidget(groups, self.selectCB,
                                            name=name)
        parameterwidgets.ParameterWidget.__init__(self, self.widget.gtk,
                                                  scope, verbose=verbose)
        self.skelmeshwidget = scope.findWidget(
            lambda w: (isinstance(w, whowidget.WhoWidget) and
                       (w.whoclass is skeletoncontext.skeletonContexts
                        or w.whoclass is mesh.meshes)))
        assert self.skelmeshwidget is not None
        self.sbcallbacks = [switchboard.requestCallbackMain(self.skelmeshwidget,
                                                            self.skelwidgetCB)]
        self.update()
        self.sbcallbacks += [
            switchboard.requestCallbackMain("groupset member added",
                                            self.grpCB),
            switchboard.requestCallbackMain("groupset member renamed",
                                            self.grpCB),
            switchboard.requestCallbackMain("groupset changed", self.grpCB)
            ]
        self.widgetChanged(self.widget.nChoices() > 0, interactive=0)

    def get_value(self):
        return self.widget.get_value()

    def selectCB(self, gtkobj, result):
        self.widgetChanged(self.widget.nChoices() > 0, interactive=1)

    def skelwidgetCB(self, interactive):
        self.update()
        self.widgetChanged(self.widget.nChoices() > 0, interactive)
    def grpCB(self, *args, **kwargs):
        self.update()
        self.widgetChanged(self.widget.nChoices() > 0, interactive=0)

    def getSkeleton(self):
        skelname = self.skelmeshwidget.get_value(depth=2)
        try:
            return skeletoncontext.skeletonContexts[skelname]
        except KeyError:
            return None

    def update(self):
        self.redraw(self.getSkeleton())

    def cleanUp(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        parameterwidgets.ParameterWidget.cleanUp(self)

class SkeletonAggregateWidget(SkeletonGroupWidget):
    def get_value(self):
        rval = self.widget.get_value()
        return placeholder.getPlaceHolderFromString(rval)

# Dictionary, indexed by widget class, of the function to use to get a
# segment set from the relevant aggregate name.  Used by
# DirectorWidget in boundarybuilderGUI.py.  It's not possible to just
# stick these functions into the widget classes, because then they'd
# need a "self" arg, which can't be provided when the functions are
# called directly in boundarybuilder.py.  See boundarybuilder.py and
# boundarybuilderGUI.py.
segmentExtractor = {}
faceExtractor = {}

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class NodeGroupWidget(SkeletonGroupWidget):
    def __init__(self, param, groups=[], scope=None, name=None, verbose=False):
        SkeletonGroupWidget.__init__(self, groups, scope=scope, name=name,
                                     verbose=verbose)

    def redraw(self, skeletoncontext):
        if skeletoncontext:
            self.widget.update(list(
                self.defaults.union(skeletoncontext.nodegroups.allGroups())))
        else:
            self.widget.update(list(self.defaults))

def _makeNodeGroupWidget(self, scope=None, verbose=False):
    return NodeGroupWidget(self, scope=scope, name=self.name, verbose=verbose)

skeletongroupparams.NodeGroupParameter.makeWidget = _makeNodeGroupWidget


class NodeAggregateWidget(SkeletonAggregateWidget, NodeGroupWidget):
    def __init__(self, param, groups=[], scope=None, name=None, verbose=False):
        SkeletonGroupWidget.__init__(
            self, groups,
            defaults=utils.OrderedSet([placeholder.selection.IDstring]),
            scope=scope, name=name, verbose=verbose)
        
def _makeNodeAggregateWidget(self, scope=None, verbose=False):
    return NodeAggregateWidget(self, scope=scope, name=self.name, 
                               verbose=verbose)

skeletongroupparams.NodeAggregateParameter.makeWidget = _makeNodeAggregateWidget

segmentExtractor[NodeAggregateWidget] = \
                                  boundarybuilder.segments_from_node_aggregate

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SegmentGroupWidget(SkeletonGroupWidget):
    def __init__(self, param, groups=[], scope=None, name=None, verbose=False):
        SkeletonGroupWidget.__init__(self, groups, scope=scope, name=name,
                                     verbose=verbose)

    def redraw(self, skeletoncontext):
        if skeletoncontext:
            self.widget.update(list(
                self.defaults.union(skeletoncontext.segmentgroups.allGroups())))
        else:
            self.widget.update(list(self.defaults))

def _makeSegmentGroupWidget(self, scope=None, verbose=False):
    return SegmentGroupWidget(self, scope=scope, name=self.name, 
                              verbose=verbose)

skeletongroupparams.SegmentGroupParameter.makeWidget = _makeSegmentGroupWidget



class SegmentAggregateWidget(SkeletonAggregateWidget, SegmentGroupWidget):
    def __init__(self, param, groups=[], scope=None, name=None, verbose=False):
        SkeletonGroupWidget.__init__(
            self, groups,
            defaults=utils.OrderedSet(
                [placeholder.selection.IDstring]),
            scope=scope, name=name, verbose=verbose)
        
def _makeSegmentAggregateWidget(self, scope=None, verbose=False):
    return SegmentAggregateWidget(self, scope=scope, name=self.name,
                                  verbose=verbose)

skeletongroupparams.SegmentAggregateParameter.makeWidget = \
                                                   _makeSegmentAggregateWidget

segmentExtractor[SegmentAggregateWidget] = \
                  skeletoncontext.SkeletonContext.segments_from_seg_aggregate


# Special context-aware segment aggregate widget for use in boundary
# modifiers.  This widget can tell whether or not the intended
# modification to the current boundary will result in a sequence-able
# segment set, and will only report itself as "valid" if this is true.
# Note that it is necessary to actually attempt the operation,
# sequence-ability cannot be deduced from the segment aggregate alone
# -- it may "tee" into the boundary, creating a branch, and fail even
# though the aggregate itself can be sequenced, or it may consist of
# two separate branches at the two end-points of the boundary, and
# thus succeed even though the aggregate itself cannot be sequenced.
# 
# This widget lives in a modal dialog box, and is a subwidget for a
# parameter to the boundary modifier, so the only real "dynamism" is
# that the value of the widget itself (i.e. the aggregate selection)
# can change.  We can get the skeleton and the modifier at init-time.

class BdyModSegmentAggregateWidget(SegmentAggregateWidget):
    def __init__(self, param, groups=[], scope=None, name=None,
                 verbose=False):
        SegmentAggregateWidget.__init__(self, param, groups, 
                                        scope=scope, name=name, verbose=verbose)
        # self.skelwidget has been set by the parent.  The modifier
        # widget will not change during our lifetime, since changing
        # it causes a new aggregate widget to be created.
        self.modifierwidget = scope.findWidget(
            lambda w: isinstance(w, bdymodparamwidget.BoundaryModParamWidget))
        
        # The modifierwidget's scope's parent is the ParameterDialog
        # box, which has the boundary name.
        self.bdy_name = self.modifierwidget.scope.parent.boundary.name
        self.widgetChanged(self.local_validity(), interactive=0)
        
    def selectCB(self, gtkobj, result):
        self.widgetChanged(self.local_validity(), interactive=1)
        
    def local_validity(self):
        if self.widget.nChoices()>0 and self.modifierwidget \
               and self.skelmeshwidget:
            grp = self.get_value()
            mod_reg = self.modifierwidget.getRegistration()
            mod_obj = mod_reg(group=grp)
            skelctxt = skeletoncontext.skeletonContexts[
                self.skelmeshwidget.get_value(depth=2)]
            return mod_obj.attempt(skelctxt, self.bdy_name)

def _makeBMSegmentAggregateWidget(self, scope=None, verbose=False):
    return BdyModSegmentAggregateWidget(self, scope=scope, name=self.name,
                                        verbose=verbose)

boundarymodifier.BdyModSegmentAggregateParameter.makeWidget = \
                                               _makeBMSegmentAggregateWidget

segmentExtractor[BdyModSegmentAggregateWidget] = \
                 skeletoncontext.SkeletonContext.segments_from_seg_aggregate

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class FaceGroupWidget(SkeletonGroupWidget):
    def __init__(self, param, groups=[], scope=None, name=None, verbose=False):
        SkeletonGroupWidget.__init__(self, groups, scope=scope, name=name,
                                     verbose=verbose)

    def redraw(self, skeletoncontext):
        if skeletoncontext:
            self.widget.update(list(
                self.defaults.union(skeletoncontext.facegroups.allGroups())))
        else:
            self.widget.update(list(self.defaults))

def _makeFaceGroupWidget(self, scope=None, verbose=False):
    return FaceGroupWidget(self, scope=scope, name=self.name, verbose=verbose)

skeletongroupparams.FaceGroupParameter.makeWidget = _makeFaceGroupWidget


class FaceAggregateWidget(SkeletonAggregateWidget, FaceGroupWidget):
    def __init__(self, param, groups=[], scope=None, name=None, verbose=False):
        SkeletonGroupWidget.__init__(
            self, groups,
            defaults=utils.OrderedSet(
                [placeholder.selection.IDstring]),
            scope=scope, name=name, verbose=verbose)
        
def _makeFaceAggregateWidget(self, scope=None, verbose=False):
    return FaceAggregateWidget(self, scope=scope, name=self.name, 
                               verbose=verbose)

skeletongroupparams.FaceAggregateParameter.makeWidget = _makeFaceAggregateWidget

segmentExtractor[FaceAggregateWidget] = \
                                boundarybuilder.segments_from_face_aggregate
faceExtractor[FaceAggregateWidget] = \
                    skeletoncontext.SkeletonContext.faces_from_face_aggregate

# See comments at BdyModSegmentAggregateWidget

class BdyModFaceAggregateWidget(FaceAggregateWidget):
    def __init__(self, param, groups=[], scope=None, name=None, verbose=False):
        FaceAggregateWidget.__init__(
            self, param, groups, scope=scope, name=name, verbose=verbose)
        # self.skelwidget has been set by the parent.  The modifier
        # widget will not change during our lifetime, since changing
        # it causes a new aggregate widget to be created.
        self.modifierwidget = scope.findWidget(
            lambda w: isinstance(w, bdymodparamwidget.BoundaryModParamWidget))
        
        # The modifierwidget's scope's parent is the ParameterDialog
        # box, which has the boundary name.
        self.bdy_name = self.modifierwidget.scope.parent.boundary.name
        self.widgetChanged(self.local_validity(), interactive=0)
        
    def selectCB(self, gtkobj, result):
        self.widgetChanged(self.local_validity(), interactive=1)
        
    def local_validity(self):
        if self.widget.nChoices()>0 and self.modifierwidget \
               and self.skelmeshwidget:
            grp = self.get_value()
            mod_reg = self.modifierwidget.getRegistration()
            mod_obj = mod_reg(group=grp)
            skelctxt = skeletoncontext.skeletonContexts[
                self.skelmeshwidget.get_value(depth=2)]
            return mod_obj.attempt(skelctxt, self.bdy_name)

def _makeBMFaceAggregateWidget(self, scope=None, verbose=False):
    return BdyModFaceAggregateWidget(self, scope=scope, name=self.name,
                                     verbose=verbose)

boundarymodifier.BdyModFaceAggregateParameter.makeWidget = \
                                                _makeBMFaceAggregateWidget
faceExtractor[BdyModFaceAggregateWidget] = \
                     skeletoncontext.SkeletonContext.faces_from_face_aggregate


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class ElementGroupWidget(SkeletonGroupWidget):
    def __init__(self, param, groups=[], scope=None, name=None, verbose=False):
        SkeletonGroupWidget.__init__(self, groups, defaults=utils.OrderedSet(),
                                     scope=scope, name=name, verbose=verbose)

    def redraw(self, skeletoncontext):
        if skeletoncontext:
            self.widget.update(list(
                self.defaults.union(skeletoncontext.elementgroups.allGroups())))
        else:
            self.widget.update(list(self.defaults))

def _makeElementGroupWidget(self, scope=None, verbose=False):
    return ElementGroupWidget(self, scope=scope, name=self.name, 
                              verbose=verbose)

skeletongroupparams.ElementGroupParameter.makeWidget = _makeElementGroupWidget


class ElementAggregateWidget(SkeletonAggregateWidget, ElementGroupWidget):
    def __init__(self, param, groups=[], scope=None, name=None, verbose=False):
        SkeletonGroupWidget.__init__(
            self, groups,
            defaults=utils.OrderedSet(
                [placeholder.selection.IDstring]),
            scope=scope, name=name,
            verbose=verbose)

def _makeElementAggregateWidget(self, scope=None, verbose=False):
    return ElementAggregateWidget(self, scope=scope, name=self.name,
                                  verbose=verbose)

skeletongroupparams.ElementAggregateParameter.makeWidget = \
                                                 _makeElementAggregateWidget

segmentExtractor[ElementAggregateWidget] = \
                                  boundarybuilder.segments_from_el_aggregate
faceExtractor[ElementAggregateWidget] = boundarybuilder.faces_from_el_aggregate

# ## ### #### ##### ###### ####### ######## ####### ###### ##### #### ### ## #

# Scope-aware widget for picking the boundary from the local skeleton
# context.

class SkeletonBoundaryWidgetBase(parameterwidgets.ParameterWidget):
    def __init__(self, param, boundaries=[], scope=None, name=None,
                 verbose=False):
        self.widget = chooser.ChooserWidget(boundaries, self.selectCB,
                                            name=name)
        parameterwidgets.ParameterWidget.__init__(self, self.widget.gtk, scope,
                                                  verbose=verbose)
        self.skelwidget = scope.findWidget(
            lambda w: isinstance(w, whowidget.WhoWidget)
            and (w.whoclass is skeletoncontext.skeletonContexts))
        self.update()

        self.sbcallbacks = [
            switchboard.requestCallbackMain(self.skelwidget,
                                            self.skelwidgetCB),
            switchboard.requestCallbackMain("new boundary configuration",
                                            self.update),
            switchboard.requestCallbackMain("new boundary created",
                                            self.update),
            switchboard.requestCallbackMain("boundary removed",
                                            self.update),
            switchboard.requestCallbackMain("boundary renamed",
                                            self.update)
            ]
        if param.value is not None:
            self.widget.set_state(param.value)
        self.widgetChanged(self.widget.nChoices() > 0, interactive=0)            

    def get_value(self):
        return self.widget.get_value()
    def selectCB(self, gtkobj, result):
        self.widgetChanged(self.widget.nChoices() > 0, interactive=1)
    def skelwidgetCB(self, interactive):
        self.update()
        self.widgetChanged(self.widget.nChoices() > 0, interactive)

    def update(self, *args, **kwargs):
        try:
            skel = skeletoncontext.skeletonContexts[self.skelwidget.get_value()]
        except KeyError:
            skel = None

        self.redraw(skel)

    def redraw(self, skel):
        if skel:
            self.widget.update(self.names(skel))
        else:
            self.widget.update([])

    def cleanUp(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        parameterwidgets.ParameterWidget.cleanUp(self)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SkeletonBoundaryWidget(SkeletonBoundaryWidgetBase):
    def names(self, skel):
        return skel.allBoundaryNamesSorted()
        
def _makeSkeletonBoundaryWidget(self, scope=None, verbose=False):
    return SkeletonBoundaryWidget(self, scope=scope, name=self.name,
                                  verbose=verbose)

skeletongroupparams.SkeletonBoundaryParameter.makeWidget = \
                                                _makeSkeletonBoundaryWidget

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SkeletonEdgeBoundaryWidget(SkeletonBoundaryWidgetBase):
    def names(self, skel):
        nms = skel.edgeboundaries.keys()
        nms.sort()
        return nms
        
def _makeSkeletonEdgeBoundaryWidget(self, scope=None, verbose=False):
    return SkeletonEdgeBoundaryWidget(self, scope=scope, name=self.name,
                                      verbose=verbose)

skeletongroupparams.SkeletonEdgeBoundaryParameter.makeWidget = \
                                                _makeSkeletonEdgeBoundaryWidget

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SkeletonFaceBoundaryWidget(SkeletonBoundaryWidgetBase):
    def names(self, skel):
        nms = skel.faceboundaries.keys()
        nms.sort()
        return nms
        
def _makeSkeletonFaceBoundaryWidget(self, scope=None, verbose=False):
    return SkeletonFaceBoundaryWidget(self, scope=scope, name=self.name,
                                      verbose=verbose)

skeletongroupparams.SkeletonFaceBoundaryParameter.makeWidget = \
                                                _makeSkeletonFaceBoundaryWidget

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SkeletonPointBoundaryWidget(SkeletonBoundaryWidgetBase):
    def names(self, skel):
        nms = skel.pointboundaries.keys()
        nms.sort()
        return nms
        
def _makeSkeletonPointBoundaryWidget(self, scope=None, verbose=False):
    return SkeletonPointBoundaryWidget(self, scope=scope, name=self.name,
                                       verbose=verbose)

skeletongroupparams.SkeletonPointBoundaryParameter.makeWidget = \
                                                _makeSkeletonPointBoundaryWidget

