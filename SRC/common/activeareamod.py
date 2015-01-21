# -*- python -*-
# $RCSfile: activeareamod.py,v $
# $Revision: 1.22.18.4 $
# $Author: langer $
# $Date: 2014/07/29 18:40:25 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.SWIG.common import config
from ooflib.SWIG.common import pixelselectioncourier
from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import pixelselectionmod
from ooflib.common import registeredclass
from ooflib.common import selectionshape
from ooflib.common.IO import parameter
from ooflib.common.IO import pixelgroupparam
from ooflib.common.IO import whoville
from ooflib.common.IO import xmlmenudump
import ooflib.common.microstructure

## Selecting pixels in the active area object makes them *inactive*.
## So activate==unselect, deactivate==select.

## TODO 3.1: activeareamod.py and pixelselectionmod.py do very similar
## things in very different ways.  They should be unified, or at least
## work the same way.  For example, the menu callback for (almost) all
## pixel selection modifications is doSelectionMod() in
## pixelselectionmod.py.  Every active area modifier has its own
## callback.  doSelectionMod() issues a bunch of switchboard signals,
## including "pixel selection changed".  Each active area modifier
## callback calls either ActiveArea.selectWithoutCheck or
## ActiveArea.unselectWithoutCheck, which issue "pixel selection
## changed" but no other signals.

def modify(menuitem, microstructure, **params):
    registration = menuitem.data
    modifier = registration(**params)
    ms = ooflib.common.microstructure.microStructures[microstructure].getObject()
    context = ms.activearea
    context.begin_writing()
    modifier(ms)
    context.end_writing()
    switchboard.notify('active area modified', modifier)
    switchboard.notify('redraw')
   

##########################

class ActiveAreaModifier(registeredclass.RegisteredClass):
    registry = []
    def __call__(self):
        pass

##########################

class ActivateAll(ActiveAreaModifier):
    def __call__(self, microstructure):
        microstructure.activearea.start()
        microstructure.activearea.clear()

registeredclass.Registration(
    'Activate All', ActiveAreaModifier,
    ActivateAll,
    ordering=0.0,
    tip="Activate all pixels.",
    discussion=
    "<para>Make the entire domain of the current &micro; active.</para>"
    )

##########################

GroupSelection = pixelselectioncourier.GroupSelection

class ActivateOnlySelection(ActiveAreaModifier):
    def __call__(self, microstructure):
        activearea = microstructure.activearea
        pixelselection = microstructure.pixelselection
        activearea.start()
        activearea.clear()              # everything is active
        activearea.invert()             # everything is inactive
        pixgrp = pixelselection.getSelectionAsGroup()
        courier = GroupSelection(microstructure, pixgrp)
        activearea.activate(courier)

registeredclass.Registration(
    'Activate Selection Only',
    ActiveAreaModifier,
    ActivateOnlySelection,
    ordering=0.1,
    tip="Activate the selected pixels, deactivating everything else.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/common/menu/activate_selection_only.xml')
    )

class ActivateSelection(ActiveAreaModifier):
    def __call__(self, microstructure):
        activearea = microstructure.activearea
        pixelselection = microstructure.pixelselection
        activearea.start()
        pixgrp = pixelselection.getSelectionAsGroup()
        activearea.activate(GroupSelection(microstructure, pixgrp))

registeredclass.Registration(
    'Activate Selection',
    ActiveAreaModifier,
    ActivateSelection,
    ordering=0.5,
    tip='Activate the the selected pixels.',
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/common/menu/activate_selection.xml')
    )

class ActivateOnlyGroup(ActiveAreaModifier):
    def __init__(self, group):
        self.group = group
    def __call__(self, microstructure):
        grp = microstructure.findGroup(self.group)
        if grp:
            activearea = microstructure.activearea
            activearea.start()
            activearea.clear()
            activearea.invert()
            activearea.activate(GroupSelection(microstructure, grp))

registeredclass.Registration(
    'Activate Pixel Group Only',
    ActiveAreaModifier,
    ActivateOnlyGroup,
    ordering=0.6,
    params=[
    pixelgroupparam.PixelGroupParameter('group',
                                        tip="A pixel group to be activated.")],
    tip="Activate only the pixels in the given pixel group, deactivating everything else.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/common/menu/activate_pixel_group_only.xml')
    )

class ActivateGroup(ActiveAreaModifier):
    def __init__(self, group):
        self.group = group
    def __call__(self, microstructure):
        grp = microstructure.findGroup(self.group)
        if grp:
            activearea = microstructure.activearea
            activearea.start()
            activearea.activate(GroupSelection(microstructure, grp))

registeredclass.Registration(
    'Activate Pixel Group',
    ActiveAreaModifier,
    ActivateGroup,
    ordering=0.7,
    params=[
    pixelgroupparam.PixelGroupParameter('group',
                                        tip="Pixel group to be activated.")],
    tip="Activate the pixels in a pixel group.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/common/menu/activate_group.xml')
    )

##########################

## DeactivateOnlySelection probably isn't really needed.

##class DeactivateOnlySelection(ActiveAreaModifier):
##    def __call__(self, microstructure):
##        activearea = microstructure.activearea
##        pixelselection = microstructure.pixelselection
##        activearea.start()
##        activearea.clear()              # everything is active
##        activearea.deactivate(pixelselection.getSelection())

##registeredclass.Registration('Deactivate Selection Only', ActiveAreaModifier,
##                             DeactivateOnlySelection,
##                             ordering=1.0,
##                             tip='Deactivate the region under the selected pixels, activating everything else.')
        
class DeactivateSelection(ActiveAreaModifier):
    def __call__(self, microstructure):
        activearea = microstructure.activearea
        pixelselection = microstructure.pixelselection
        activearea.start()
        pixgrp = pixelselection.getSelectionAsGroup()
        activearea.deactivate(GroupSelection(microstructure, pixgrp))
        

registeredclass.Registration(
    'Deactivate Selection',
    ActiveAreaModifier,
    DeactivateSelection,
    ordering=1.5,
    tip='Deactivate the selected pixels.',
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/common/menu/deactivate_selection.xml')
    )

class DeactivateGroup(ActiveAreaModifier):
    def __init__(self, group):
        self.group = group
    def __call__(self, microstructure):
        grp = microstructure.findGroup(self.group)
        if grp:
            activearea = microstructure.activearea
            activearea.start()
            activearea.deactivate(GroupSelection(microstructure, grp))

registeredclass.Registration(
    'Deactivate Group',
    ActiveAreaModifier,
    DeactivateGroup,
    ordering=1.6,
    params=[
    pixelgroupparam.PixelGroupParameter('group',
                                        tip="Pixel group to be deactivated.")],
    tip='Deactivate the pixels in a pixel group.',
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/menu/deactivate_group.xml')
    )

############################

ShrinkSelection = pixelselectioncourier.ShrinkSelection
class ExpandActiveArea(ActiveAreaModifier):
    def __init__(self, radius):
        self.radius = radius
    def __call__(self, microstructure):
        activearea = microstructure.activearea
        activearea.start()
        activegrp = activearea.getSelectionAsGroup()
        activearea.activate(
            pixelselectioncourier.ShrinkSelection(microstructure,
                                                  activegrp, self.radius))

registeredclass.Registration(
    'Expand',
    ActiveAreaModifier,
    ExpandActiveArea,
    ordering=3.0,
    params=[parameter.FloatParameter(
            'radius', 1.0,
            tip="The radius of expansion in pixel units.")],
    tip="Expand the active area by a given distance.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/common/menu/expand_activearea.xml')
    )

##############################

ExpandSelection = pixelselectioncourier.ExpandSelection
class ShrinkActiveArea(ActiveAreaModifier):
    def __init__(self, radius):
        self.radius = radius
    def __call__(self, microstructure):
        activearea = microstructure.activearea
        activearea.start()
        activegrp = activearea.getSelectionAsGroup()
        activearea.deactivate(
            pixelselectioncourier.ExpandSelection(microstructure,
                                                  activegrp, self.radius))

registeredclass.Registration(
    'Shrink',
    ActiveAreaModifier,
    ShrinkActiveArea,
    ordering=3.1,
    params=[
    parameter.FloatParameter(
            'radius', 1.0,
            tip="The radius of shrinkage in pixel units.")
    ],
    tip="Shrink the active area by a given distance.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/common/menu/shrink_activearea.xml')
    )

##############################

class PixelActivationOperator(registeredclass.RegisteredClass):
    registry = []

class Activate(PixelActivationOperator):
    def operate(self, activearea, courier):
        activearea.activate(courier)

class ActivateOnly(PixelActivationOperator):
    def operate(self, activearea, courier):
        activearea.clearAndActivate(courier)

class Deactivate(PixelActivationOperator):
    def operate(self, activearea, courier):
        activearea.deactivate(courier)

registeredclass.Registration(
    'Activate',
    PixelActivationOperator,
    Activate,
    ordering=0,
    tip="Activate new pixels, leaving previously activated ones active.")

registeredclass.Registration(
    'Activate Only',
    PixelActivationOperator,
    ActivateOnly,
    ordering=1,
    tip="Activate new pixels after deactivating previously active ones.")

registeredclass.Registration(
    'Deactivate',
    PixelActivationOperator,
    Deactivate,
    ordering=2,
    tip="Deactivate pixels")

class ActivateRegion(ActiveAreaModifier):
    def __init__(self, shape, operator):
        self.shape = shape
        self.operator = operator
    def __call__(self, ms):
        activearea = ms.activearea
        activearea.start()
        courier = pixelselectionmod.couriers[self.shape.__class__](self.shape,
                                                                   ms)
        self.operator.operate(ms.activearea, courier)

registeredclass.Registration(
    "Region",
    ActiveAreaModifier,
    ActivateRegion,
    ordering=2.0,
    params=[
        parameter.RegisteredParameter(
            'shape', selectionshape.SelectionShape,
            tip="The shape of the region to activate."),
        parameter.RegisteredParameter(
            'operator', PixelActivationOperator,
            tip="How to use the region to modify the active volume.")
    ],
    tip="Modify the current active area via boolean operations using the"
    " voxels within a geometrically defined region."
)

##############################

class InvertActiveArea(ActiveAreaModifier):
    def __call__(self, microstructure):
        microstructure.activearea.start()
        microstructure.activearea.invert()

registeredclass.Registration(
    'Invert',
    ActiveAreaModifier,
    InvertActiveArea,
    ordering=4.0,
    tip="Switch active and inactive pixels",
    discussion="""<para>

    Invert the current &active; by activating the inactive pixels and
    deactivating the active ones.

    </para>"""
    )

##############################

class CopyActiveArea(ActiveAreaModifier):
    def __init__(self, source):
        self.source = source            # source Microstructure
    def __call__(self, microstructure):
        sourceMS = ooflib.common.microstructure.microStructures[self.source]
        microstructure.activearea.start()
        microstructure.activearea.getObject().setFromGroup(
            sourceMS.getObject().activearea.getSelectionAsGroup())
        ## TODO OPT: Does this have to send "pixel selection changed"?

registeredclass.Registration(
    'Copy',
    ActiveAreaModifier,
    CopyActiveArea,
    ordering=5.0,
    params=[whoville.WhoParameter(
            'source',
            ooflib.common.microstructure.microStructures,
            tip='Copy the active area from this Microstructure.')],
    tip="Copy the active area from another Microstructure.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/common/menu/copy_activearea.xml')
    )
