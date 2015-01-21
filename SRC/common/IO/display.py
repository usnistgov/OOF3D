# -*- python -*-
# $RCSfile: display.py,v $
# $Revision: 1.109.4.82 $
# $Author: langer $
# $Date: 2014/12/05 21:29:11 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

## Display objects and friends.  A *Display* is basically a collection
## of DisplayMethods, sharing the same output device.  The layers are
## drawn in turn.

#####################################

## Display Object Overview

## TODO 3.1: Update these comments.

# Each layer in the graphics window is defined by a DisplayMethod
# instance.  (Subclasses of DisplayMethod are defined elsewhere.)  The
# source of the data for each DisplayMethod is a Who object.

# OBOLETE COMMENT: There can be many DisplayMethods for a single Who,
# and the user may want to change each DisplayMethod's Who at the same
# time, so DisplayMethods are grouped into LayerSets, and the Who is
# associated with the LayerSet instead of with the DisplayMethod
# directly.  Each DisplayMethod knows its LayerSet, and each LayerSet
# contains a list of its DisplayMethods.  The graphics window, or
# rather its non-gui component, the GhostGfxWindow, maintains a list
# of LayerSets.

# OBSOLETE COMMENT The Display is an object contained in a
# GhostGfxWindow that manages the DisplayLayers.  (It's not clear at
# this time why it's a separate class, and whether or not its
# functionality should be merged into the GhostGfxWindow class.  The
# separation may just be a historical artifact.  Resolving that is a
# TODO 3.1.)  The Display keeps a list of DisplayMethods, containing
# all the methods of all the LayerSets in the GhostGfxWindow.  The
# Display's list determines the order in which the layers are drawn.
# The LayerSets' lists have nothing to do with drawing order.

# OBSOLETE COMMENT Layers are added to a graphics window when the
# LayerEditor calls GhostGfxWindow.incorporateLayer with a new
# DisplayMethod as an argument.

# OBSOLETE COMMENT If the GhostGfxWindow has no currently selected
# layer, a clone of the new LayerSet is added to the Display.  If
# there is a currently selected layer, its LayerSet is replaced with a
# clone of the new LayerSet.

#####################################

from ooflib.SWIG.common import config
from ooflib.SWIG.common import lock
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import switchboard
#from ooflib.SWIG.common import timestamp
from ooflib.common import debug
from ooflib.common import mainthread
from ooflib.common import registeredclass
from ooflib.common import subthread
from ooflib.common.IO import parameter
from ooflib.common.IO import placeholder
from ooflib.common.IO import whoville
from ooflib.common.IO import xmlmenudump
import string
import types
import weakref

## This is helpful for debugging extra redraw calls, which might be
## expensive.
# def debuggery():
#     debug.fmsg("redraw")
#     debug.dumpCaller(4)
# switchboard.requestCallback("redraw", debuggery)

############

# LayerOrderings are used to determine the default position of a layer
# in the display.  Displays that fill planes are drawn first, followed
# by those that partially fill planes, etc.

class LayerOrdering:
    def __init__(self, order, suborder=0.):
        self.order = order
        self.suborder = suborder
    def __cmp__(self, other):
        if self.order < other.order: return -1
        if self.order > other.order: return 1
        if self.suborder < other.suborder: return -1
        if self.suborder > other.suborder: return 1
        return 0
    def __call__(self, suborder):
        return LayerOrdering(self.order, suborder)

def layercomparator(a, b):
    aordering = a.layerordering()
    bordering = b.layerordering()
    return aordering.__cmp__(bordering)

Abysmal = LayerOrdering(-1000)          # shouldn't ever appear
Volume = LayerOrdering(-1.)
Planar = LayerOrdering(0.)              # filled meshes, or images
SemiPlanar = LayerOrdering(1.)          # partially filled meshes or images
Linear = LayerOrdering(2.)              # mesh boundaries
SemiLinear = LayerOrdering(3.)          # partial mesh boundaries
PointLike = LayerOrdering(4.)           # single pixels or nodes

############

class DisplayMethodParameter(parameter.RegisteredParameter):
    def __init__(self, name, value=None, default=None, tip=None, auxData={}):
        parameter.RegisteredParameter.__init__(self, name, DisplayMethod,
                                               value, default, tip, auxData)

    def clone(self):
        return self.__class__(self.name, self.value, self.default, self.tip)

#############

# DisplayMethods are things like ContourPlots, Bitmaps, etc --
# different ways of displaying different types of Who objects on the
# canvas.  They must have a 'draw' function, and the Registration for
# each DisplayMethod class must have a 'whoclasses' attribute which
# lists the names of the WhoClasses that the DisplayMethod accepts.
## TODO 3.1: Update this comment for vtk based CanvasLayers.

# TODO 3.1: Now that this has been pared down because there are no longer
# multiple devices, this is basically a wrapper for the
# OOF3DCanvasLayer. Should the relevant functions just be added to a
# .spy file?  NO -- the class structure would be too complicated:
# different C++ base classes for a single python RegisteredClass?

## TODO 3.1 LOCK: If a DisplayMethod ought to lock its Who source, it will
## have to run the pipeline up through the point where the source is
## read by calling Update() from the switchboard callback that
## indicated that the source had changed.  Then the switchboard
## callback and the lock can run on a subthread, and the final call to
## Render() can run on the main thread without having to access the
## Who object.

## TODO 3.1: DisplayMethod instances should keep all their switchboard
## signals in a list stored in the base class, so that they can all be
## removed together by the base class destroy() method.  Since some
## DisplayMethods use multiple inheritance, it's hard to ensure that
## all the subclass correct destroy() methods are called. (Maybe we
## should just use super()?)

class DisplayMethod(registeredclass.RegisteredClass):
    registry = []
    def __init__(self):
        # "hidden" is controlled by the menu callback functions
        # GhostGfxWindow.hideLayer() and GhostGfxWindow.showLayer(),
        # and reflects whether or not the user wants the layer to be
        # visible.  Whether or not the layer is *actually* visible is
        # determined by OOFCanvasLayer::showing_, which is controlled
        # by OOFCanvasLayer::show() and OOFCanvasLayer::hide().
        self.hidden = False

        self.listed = True     # is it listed in gfxwindow layer list?
        self.frozen = False
        self.canvaslayer = None
        self.gfxwindow = None   # set by build()

        self._who = None
        self.whoChangedSignal = None  # switchboard "who changed" callback
        self.whoRenamedSignal = None
        
        self.gridSize = 0

    # From cvs messages: DisplayMethod.destroy() wasn't being called,
    # which was leaving some switchboard signals in place after their
    # callback functions were destroyed when a graphics window was
    # closed.  Explicitly destroying the layers in
    # GhostGfxWindow.close() fixed the problem, except that it crashed
    # the program if a graphics window was closed via the window
    # manager (as opposed to closing it via the File menu).  This was
    # due to a race condition: gtk was sending 'destroy' events to all
    # of the window components while the Close() menu item was
    # running.  The solution was to pass an extra argument to
    # DisplayMethod.destroy() indicating whether or not the gtk
    # shutdown procedure has begun.  All calls to destroy() should have
    # destroy_canvaslayer=True, except for calls from
    # GhostGfxWindow.close().

    def destroy(self, destroy_canvaslayer=True):
        self.gfxwindow = None   # TODO OPT: Is this necessary?
        if self.whoChangedSignal:
            switchboard.removeCallback(self.whoChangedSignal)
            switchboard.removeCallback(self.whoRenamedSignal)
        if destroy_canvaslayer and self.canvaslayer is not None:
            mainthread.runBlock(self.canvaslayer.destroy)
            self.canvaslayer = None

    # Derived classes must redefine this (2D only):
    def draw(self, canvas):
        pass

    # In 3D, derived classes *must* redefine this method, which
    # returns an appropriate OOFCanvasLayer instance.
    def newLayer(self):
        raise ooferror.ErrPyProgrammingError("%s.newLayer is not defined!"
                                             % self.__class__.__name__)

    # Derived classes which can have contours should redefine these
    # next three functions.
    def contour_capable(self):
        return 0 # Must be zero, and not "None", arithmetic is done on
                 # it.  TODO OPT: Maybe this function should have a
                 # different name, then.
    
    
    # Should return the bounds of the contours.
    def get_contourmap_info(self):
        pass

    # Should actually draw the colorbar on the passed-in canvas.
    def draw_contourmap(self, canvas):
        pass

    # Other contour-map-management functions -- only implemented
    # in subclasses of ContourDisplay.
    def explicit_contour_hide(self):
        pass
        
    # Image layers and overlayers redefine these.  This isn't very OO.
    def isImage(self):
        return False
    def isOverlayer(self):
        return False

    # Layers that need to modify themselves or rebuild a graphics
    # pipeline should redefine this method.  It's called when layers
    # are added, removed, hidden, or shown in the graphics window.
    def layersChanged(self):
        pass
      
    def getGridSize(self):
      return self.gridSize

    # Frozen layers won't be *redrawn*, but they will be drawn on a new
    # canvas.  These functions should be redefined in derived classes
    # that need to do more computation (such as storing the time) when
    # freezing.
    def freeze(self):
        self.frozen = True

    def unfreeze(self):
        self.frozen = False

    def refreeze(self, layer):
        # Copy frozen status from another layer.
        self.frozen = layer.frozen
    
    def incomputable(self):
        # Subclasses may override incomputable().  incomputable() must
        # return None if the DisplayMethod is actually computable, or
        # return a string explaining why the method is incomputable.
        # For example, a method that displays a field defined on a
        # mesh would return 'Field not defined' if that field weren't
        # defined on the mesh self.who().
        who = self.who().resolve(self.gfxwindow)
        if who is None:
            return "Nothing to draw"
        if not self.acceptsWho(who):
            return "DisplayMethod can't display %s objects" \
                   % who.getClass().name()

    def animatable(self):
        return False            # redefined in AnimationLayer

    def pickable(self):
        return self.canvaslayer is not None and self.canvaslayer.pickable()

    def clone(self, gfxwindow):
        self.setDefaultParams()
        bozo = self.getRegistration()()
        bozo.hidden = self.hidden
        bozo.listed = self.listed
        bozo.frozen = self.frozen
        bozo.gfxwindow = gfxwindow
        return bozo

    def name(self):
        return self.getRegistration().name()

    #=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

    def who(self):
        return self._who     # _who may be an unresolved WhoProxy.

    def acceptsWho(self, who):
        return (who is not None and self.acceptsWhoClass(who.getClass()))

    def acceptsWhoClass(self, whoclass):
        return whoclass.name() in self.getRegistration().whoclasses
        
    def setWho(self, hoo):
        if hoo is self._who:
            return True
        self._who = hoo
        if self.whoChangedSignal:
            switchboard.removeCallback(self.whoChangedSignal)
            switchboard.removeCallback(self.whoRenamedSignal)
            self.whoChangedSignal = None
        if hoo is not None:
            # whoChanged should return True if it did *not* do
            # everything that setParams does.  Some subclasses can't
            # separate the jobs of whoChanged and setParams.  They
            # should define both functions and have them do the same
            # thing, but return False from whoChanged().
            status = self.whoChanged()
            self.whoChangedSignal = switchboard.requestCallback(
                ("who changed", hoo.classname), self._whoChangedCB)
            self.whoRenamedSignal = switchboard.requestCallback(
                ("rename who", hoo.classname), self._whoRenamedCB)
            return status
        ## TODO OPT: If hoo is None, clear the layer.

    def _whoChangedCB(self, who):
        # switchboard "who changed" signal.  who is a real Who, not a
        # WhoProxy.
        if who is not None and who is self.who().resolve(self.gfxwindow):
            self.whoChanged()

    def _whoRenamedCB(self, oldpath, newname):
        who = self.who().resolve(self.gfxwindow)
        if who is not None and who.name() == newname:
           self.gfxwindow.updateLayerList(self)
           
    def whoChanged(self):
        # Redefine this in derived classes if necessary.  It's called
        # whenever a new Who object is defined or the current Who
        # object is modified, or, if the Who object is a proxy, when
        # the layers have changed and the proxy resolution may be
        # different.  The argument is a real Who object, not a
        # WhoProxy, but it can also be None.  Also see the comment in
        # setWho, above, about the return value.
        return True

    def copyWho(self, otherlayer):
        self.setWho(otherlayer._who)

    def build(self, gfxwindow):
        # Called by GhostGfxWindow.incorporateLayer().  newLayer()
        # must be defined in the derived class.
        self.gfxwindow = gfxwindow
        self.canvaslayer = self.newLayer()
        if self.hidden:
            self.canvaslayer.hide(True)
        else:
            self.canvaslayer.show(True)

    #=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

    def setParams(self):
        # Set parameter values in the canvaslayer, copying them from
        # the Parameters.  This must be redefined in subclasses that
        # have parameters.
        pass

    def copyParams(self, otherlayer):
        # Copy all parameter values from the other layer, setting this
        # layer's Parameters.  This may be redefined in subclasses if
        # the generic mechanism used here is somehow insufficient.
        vals = otherlayer.getParamValues()
        for param, val in zip(self.getRegistration().params, vals):
            assert hasattr(self, param.name)
            setattr(self, param.name, val)

    #=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

    def redraw(self):
        # Derived classes may redefine this.
        self.canvaslayer.setModified()

    def timeChanged(self):
        # Redefine this in layers that need to do more computation
        # when the display time changes.
        pass

    #=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

    def writeVTK(self, filename):
        self.canvaslayer.writeVTK(filename)

    #=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

    # Distinct methods with the same values should not compare
    # equally, so override RegisteredClass's __eq__.
    def __eq__(self, other):
        return id(self)==id(other)
    
    # The former __eq__, negated, for equivalence testing.
    def inequivalent(self, other):
        return other is None or \
               not (other.__class__ is self.__class__ 
                    and other.who() is self.who() 
                    and registeredclass.RegisteredClass.__eq__(self, other))

    #=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

    def hide(self):
        self.canvaslayer.hide()

    def show(self):
        self.canvaslayer.show()

    def modified(self):
        ## Explicitly tell a layer that it's been modified.  This will
        ## force a redraw.
        self.canvaslayer.setModified()

    # TODO MERGE: raise_layer and lower_layer don't make sense in 3D.
    # The 2D version will have to do something here.
    if config.dimension() == 2:
        def raise_layer(self, howfar=1):
            pass

        def lower_layer(self, howfar=1):
            pass

    def layerordering(self):
        return self.getRegistration().layerordering

    # The short name is just the classname and the "what", if there is
    # one.  Used by the gfxwindow's layer display, if the appropriate
    # setting is set.
    def short_name(self):
        try:
            what = self.what
        except AttributeError:
            return self.__class__.__name__
        else:
            return "%s(%s)" % (self.__class__.__name__, what.shortrepr())

######################

class AnimationLayer(object):
    def __init__(self, when):
        self.when = when
        self.animating = False
    def animatable(self):
        return (not self.frozen and self.when is placeholder.latest
                and not self.incomputable())
    def beginAnimation(self):
        self.animating = True
    def endAnimation(self):
        self.animating = False
    def animationTimes(self):
        # Return a list of available times.
        raise ooferror.ErrPyProgrammingError(
            "Someone forgot to redefine animationTimes for",
            self.__class__.__name__)


######################

# Routine to add lists of DisplayMethods sorted by their target
# objects to the xml documentation for the DisplayMethod base class.

def _addMethodList(text, obj):
    regdict = {}
    for reg in DisplayMethod.registry:
        for whoclass in reg.whoclasses:
            try:
                classlist = regdict[whoclass]
            except KeyError:
                regdict[whoclass] = classlist = []
            classlist.append(reg)
    whoclasses = regdict.keys()
    whoclasses.sort()
    lines = ["""
    <para>Here is a list of the types of displayable objects and the
    DisplayMethods that apply to them:
    <itemizedlist>
        """]
    for whoclass in whoclasses:
        lines.append("<listitem><para>%s" % whoclass)
        lines.append("<itemizedlist spacing='compact' id='DisplayMethods:%s'>" % whoclass)
        for reg in regdict[whoclass]:
            lines.append("<listitem><simpara><link linkend='%s'>%s (%s</link>) -- %s</simpara></listitem>"
                         % (xmlmenudump.registrationID(reg), reg.name(),
                         reg.subclass.__name__, reg.tip))

        lines.append("</itemizedlist></para></listitem>")

    lines.append("</itemizedlist></para>")
    return text + string.join(lines, '\n')

DisplayMethod.tip = "Methods for drawing &oof2; objects in the graphics window."
DisplayMethod.discussion = xmlmenudump.loadFile(
    'DISCUSSIONS/common/reg/displaymethod.xml', _addMethodList)

