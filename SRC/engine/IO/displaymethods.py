# -*- python -*-
# $RCSfile: displaymethods.py,v $
# $Revision: 1.147.2.81 $
# $Author: langer $
# $Date: 2014/11/25 22:08:32 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Simple display methods for Skeletons and Meshes.  Simpler than
# contour plots, in any case.

import sys

from ooflib.SWIG.common import config
from ooflib.SWIG.common import coord
from ooflib.SWIG.common import lock
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common.IO import canvaslayers
from ooflib.SWIG.common.IO import gridlayers
from ooflib.SWIG.common.IO import vtkutils
from ooflib.SWIG.engine import cskeletonmodifier
from ooflib.SWIG.engine import field
from ooflib.SWIG.engine import mastercoord
from ooflib.SWIG.engine import ooferror2
from ooflib.SWIG.engine import skeletonfilter
from ooflib.SWIG.common import smallmatrix
from ooflib.SWIG.engine.IO import gridsource
from ooflib.common import color
from ooflib.common import debug
from ooflib.common import mainthread
from ooflib.common import parallel_enable
from ooflib.common import primitives
from ooflib.common import registeredclass
from ooflib.common import runtimeflags
from ooflib.common import utils
from ooflib.common.IO import automatic
from ooflib.common.IO import colormap
from ooflib.common.IO import display
from ooflib.common.IO import ghostgfxwindow
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import placeholder
from ooflib.common.IO import reporter
from ooflib.common.IO import xmlmenudump
from ooflib.engine import mesh
from ooflib.engine import skeletoncontext
from ooflib.engine.IO import materialparameter
from ooflib.engine.IO import meshparameters
from ooflib.engine.IO import output
from ooflib.engine.IO import outputDefs
import ooflib.SWIG.engine.material

if parallel_enable.enabled():
    from ooflib.SWIG.common import mpitools

FloatRangeParameter = parameter.FloatRangeParameter
IntRangeParameter = parameter.IntRangeParameter
AutoNumericParameter = parameter.AutoNumericParameter

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class MeshNodePosition(registeredclass.RegisteredClass):
    registry = []

class Original(MeshNodePosition):
    def factor(self):
        return 0.0

class Actual(MeshNodePosition):
    def factor(self):
        return 1.0

class Enhanced(MeshNodePosition):
    def __init__(self, scaleFactor):
        self.scaleFactor = scaleFactor
    def factor(self):
        return self.scaleFactor

registeredclass.Registration(
    'Original',
    MeshNodePosition,
    Original,
    ordering=0,
    tip="Display nodes at their original undisplaced positions.")

registeredclass.Registration(
    'Actual',
    MeshNodePosition,
    Actual,
    ordering=1,
    tip="Display nodes at their actual displaced positions.")

registeredclass.Registration(
    'Enhanced',
    MeshNodePosition,
    Enhanced,
    ordering=1,
    params=[
        parameter.FloatParameter(
            'scaleFactor', 1.0,
            tip="Node displacements will be multiplied by this amount.")
        ],
    tip="Display nodes with exaggerated displacements.")

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

## Default values of display parameters for SkeletonEdgeDisplay and
## MeshEdgeDisplay, and menu items to set them.  The same Parameter
## objects are used in all commands so that the values are shared.

if config.dimension() == 2:
    defaultSkeletonWidth = 0
    defaultMeshWidth = 0
    widthRange = (0,10)
# In vtk, line widths of 0 cause errors
elif config.dimension() == 3:
    defaultSkeletonWidth = 1
    defaultMeshWidth = 1
    widthRange = (1,10)
defaultSkeletonColor = color.black
defaultMeshColor = color.black
defaultSkeletonFilter = skeletonfilter.NullFilter()
defaultMeshFilter = skeletonfilter.MaterialFilter('<Any>')

skelColorParam = color.ColorParameter('color', defaultSkeletonColor,
                                      tip=parameter.emptyTipString)
skelWidthParam = IntRangeParameter('width', widthRange, defaultSkeletonWidth,
                                   tip="Line thickness, in pixels.")

meshColorParam = color.ColorParameter('color', defaultMeshColor,
                                      tip=parameter.emptyTipString)
meshWidthParam = IntRangeParameter('width', widthRange, defaultMeshWidth,
                                   tip="Line thickness, in pixels.")

# Use the same filter parameter for all Mesh displays ...
meshFilterParam = parameter.RegisteredParameter(
    'filter', skeletonfilter.SkeletonFilterPtr,
    defaultMeshFilter,
    tip = "Visualization filter for the Mesh.")

# ... and another for all Skeleton displays.
skelFilterParam = parameter.RegisteredParameter(
    'filter', skeletonfilter.SkeletonFilterPtr,
    defaultSkeletonFilter,
    tip = "Visualization filter for the Skeleton.")

# Common mesh display parameters.

meshdispparams = [
    placeholder.TimeParameter(
        'when',
        value=placeholder.latest,
        tip='Time at which to plot'),
    parameter.RegisteredParameter(
        'where', MeshNodePosition, value=Actual(),
        tip="Plot at displaced or original position?")
]

# Menu items that just set the default values of the parameters to be
# used the next time a new graphics window is opened don't actually
# need to do anything in the callback.
def _dummy(*args, **kwargs):
    pass
    
mainmenu.gfxdefaultsmenu.Skeletons.addItem(oofmenu.OOFMenuItem(
    'Skeleton_Edges',
    callback=_dummy,
    ordering = 0,
    params=[skelColorParam,
            skelWidthParam,
            ],
    help="Set the default parameters for Skeleton edge displays.",
    discussion="""<para>

    Set the default parameters for
    <link linkend="RegisteredClass-SkeletonEdgeDisplay"><classname>SkeletonEdgeDisplays</classname></link>.
    See <xref linkend="RegisteredClass-SkeletonEdgeDisplay"/> for the details.      This command may be placed in the &oof2rc; file
    to set a default value for all &oof2; sessions.

    </para>"""))

mainmenu.gfxdefaultsmenu.Meshes.addItem(oofmenu.OOFMenuItem(
    'Mesh_Edges',
    callback=_dummy,
    ordering=0,
    params=[meshColorParam, meshWidthParam],
    help="Set the default parameters for Mesh edge displays.",
    discussion="""<para>

    Set the default parameters for
    <link linkend="RegisteredClass-MeshEdgeDisplay"><classname>MeshEdgeDisplays</classname></link>.
    See <xref linkend="RegisteredClass-MeshEdgeDisplay"/> for the details.
    This command may be placed in the &oof2rc; file to set a default value
    for all &oof2; sessions.

    </para>"""))

mainmenu.gfxdefaultsmenu.Skeletons.addItem(oofmenu.OOFMenuItem(
    'Filter',
    callback=_dummy,
    ordering=100,
    params=[skelFilterParam],
    help="Set the default visualization filter for Skeleton displays."))

mainmenu.gfxdefaultsmenu.Meshes.addItem(oofmenu.OOFMenuItem(
    'Filter',
    callback=_dummy,
    ordering=100,
    params=[meshFilterParam],
    help="Set the default visualization filter for Mesh displays."))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Skeleton and Mesh display methods are very similar, except for how
# they get some of their data.  These two base classes encapsulate the
# *differences* between Skeletons and Meshes, as far as displaying is
# concerned.  They're mixed in with other base classes to create the
# actual DisplayMethods.  The common base class SkelMeshDisplayMethod
# encapsulates the similarities.

class SkelMeshDisplayMethod(display.DisplayMethod):
    def __init__(self, filter):
        self.filter = filter
        display.DisplayMethod.__init__(self)

class SkeletonDisplayMethod(SkelMeshDisplayMethod):
    def __init__(self, filter):
        SkelMeshDisplayMethod.__init__(self, filter)
        self.skelDataChangedSignal = switchboard.requestCallback(
            "Skeleton changed", self.skelDataChangedCB)

    def destroy(self, destroy_canvaslayer):
        switchboard.removeCallback(self.skelDataChangedSignal)
        super(SkeletonDisplayMethod, self).destroy(destroy_canvaslayer)
        # SkelMeshDisplayMethod.destroy(self, destroy_canvaslayer)

    def polygons(self, gfxwindow, skelcontext): # used only in 2D
        skeleton = skelcontext.getObject()
        if parallel_enable.enabled():
            nodes = skeleton.all_skeletons["nodes"]
            elements = skeleton.all_skeletons["elements"]
            polys = []
            for i in range(mpitools.Size()):
                for el in elements[i]:
                    polys.append([primitives.Point(*nodes[i][ni])
                                  for ni in el])
            return  polys
        else:
            return [el.perimeter() for el in skeleton.elements()]

    def vtkSource(self):
        return gridsource.newSkeletonGridSource()
    
    def setSource(self):
        themesh = self.who().resolve(self.gfxwindow)
        self.source.setSkeleton(themesh.getObject())
        self.source.setFilter(self.filter)
        self.filter.setSource(self.source)

    def skelDataChangedCB(self, skeletonname): # sb "Skeleton changed"
        # Calling source.Modified here forces the layer to be redrawn
        # if the Skeleton changes.
        ## TODO 3.1: This is arguably the wrong place to handle the
        ## switchboard signal.  The SkeletonGridSource object itself
        ## should do it.
        hoo = self.who()
        if hoo and hoo.resolve(self.gfxwindow).path() == skeletonname:
            self.source.Modified()


class MeshDisplayMethod(display.AnimationLayer, SkelMeshDisplayMethod):
    # A display method that displays data from a Mesh at positions
    # determined by the mesh.  self.where is a MeshNodePosition.
    def __init__(self, filter, when):
        self.freezetime = None
        display.AnimationLayer.__init__(self, when)
        SkelMeshDisplayMethod.__init__(self, filter)
        self.meshDataChangedSignal = switchboard.requestCallback(
            "mesh data changed", self.meshDataChangedCB)
    def destroy(self, destroy_canvaslayer):
        switchboard.removeCallback(self.meshDataChangedSignal)
        super(MeshDisplayMethod, self).destroy(destroy_canvaslayer)
        # SkelMeshDisplayMethod.destroy(self, destroy_canvaslayer)
    def incomputable(self):
        themesh = self.who().resolve(self.gfxwindow)
        return (display.DisplayMethod.incomputable(self) or
                not themesh.boundedTime(self.when))
    def clone(self, layerset=None):
        bozo = display.DisplayMethod.clone(self, layerset)
        bozo.freezetime = self.freezetime
        return bozo
    def freeze(self):
        meshctxt = self.who().resolve(self.gfxwindow)
        if meshctxt:
            self.freezetime = meshctxt.getTime(self.when)
        display.DisplayMethod.freeze(self)
    def unfreeze(self):
        self.freezetime = None
        display.DisplayMethod.unfreeze(self)
    def refreeze(self, layer):
        if isinstance(layer, MeshDisplayMethod):
            self.freezetime = layer.freezetime
        else:
            self.freezetime = None
        display.DisplayMethod.refreeze(self, layer)

    ## TODO OPT: Why does getTime have a meshctxt arg?  Is it ever called
    ## with a different mesh than the one returned by self.who()?  If
    ## all DisplayMethods had getTime() (with no args) then it might
    ## be easier to initialize GhostGfxWindow.displayTime.
    def getTime(self, meshctxt):
        if self.freezetime is not None:
            return self.freezetime
        if self.when == placeholder.latest:
            return self.gfxwindow.displayTime
        return meshctxt.getTime(self.when)

    def timeChanged(self):
        hoo = self.who()
        if self.source and hoo:
            self.source.setTime(self.getTime(hoo))

    def animationTimes(self):
        meshctxt = self.who().resolve(self.gfxwindow)
        return meshctxt.cachedTimes()
        
    def polygons(self, gfxwindow, meshctxt): # used only in 2D
        themesh = meshctxt.getObject()
        meshctxt.restoreCachedData(self.getTime(meshctxt))
        try:
            # PARALLEL_RCL: Make changes here to display parallel mesh
            # There is an issue with clicking on the skeleton or mesh
            # graphics: only the nodes or elements for the front-end
            # process get the cursor or mark

            if parallel_enable.enabled():
                # This snippet taken from SkeletonDisplayMethod
                nodes = themesh.all_meshskeletons["nodes"]
                elements = themesh.all_meshskeletons["elements"]
                polys = []
                for i in range(mpitools.Size()):
                    for el in elements[i]:
                        polys.append([primitives.Point(*nodes[i][ni])
                                      for ni in el])
                return polys
            else:
                edges = [element.perimeter() for element in themesh.elements()]
                flatedges = utils.flatten(edges)

                ## TODO MER: 2D version needs to change to get rid of
                ## PositionOutputs.  'where' is now a MeshNodePosition
                ## object.
                # corners tells where on each edge to evaluate self.where
                corners = [[0.0]]*len(flatedges)
                # evaluate position output for all edges at once
                polys = self.where.evaluate(themesh, flatedges, corners)
                # give the corner list the same structure as the edge list: a
                # list of lists, where each sublist is the list of corners of
                # an element.
                polys = utils.unflatten(edges, polys)
                if len(polys) == 0:
                    mainthread.runBlock(
                        reporter.warn,
                        ("No mesh elements drawn! Are there no materials assigned?",))
                return polys
        finally:
            meshctxt.releaseCachedData()

    def vtkSource(self):
        return gridsource.newMeshGridSource()
    def setSource(self):
        themesh = self.who().resolve(self.gfxwindow)
        self.source.setMesh(themesh.getObject())
        self.source.setTime(self.getTime(themesh))
        self.source.setSkeleton(themesh.getParent().getObject())
        self.source.setFilter(self.filter)
        self.filter.setSource(self.source)
        self.source.setEnhancement(self.where.factor())
        # TODO 3.1: This has to do something with the "when" parameter.
        # Where should restoreCachedData be called?

    def meshDataChangedCB(self, meshctxt): # sb "mesh data changed"
        # Calling source.Modified here forces the layer to be redrawn
        # if the mesh data (eg, displacement field values) changes.
        ## TODO MER: This is arguably the wrong place to handle the
        ## switchboard signal.  The MeshGridSource object itself
        ## should do it.
        hoo = self.who()
        if hoo and meshctxt is hoo.resolve(self.gfxwindow):
            self.source.Modified()

    # Routines for converting between displaced and undisplaced
    # coordinates using this layer's MeshNodePosition object
    # ("self.where").  This is here primarily so that the mesh info
    # displays can be drawn in displaced coordinates -- since this
    # method refers to the topmost mesh display, only that display
    # (i.e. this object) knows the right MeshNodePosition to use.
    def displaced_from_undisplaced(self, gfxwindow, orig): # 2D only
        meshctxt = self.who().resolve(gfxwindow)
        femesh = meshctxt.getObject()
        felem = meshctxt.enclosingElement(orig)
        return self._displaced(femesh, felem, realpos=orig)

    # _displaced 
    def _displaced(self, mesh, elem, realpos=None, masterpos=None): # 2D only
        masterpos = masterpos or elem.to_master(realpos)
        realpos = realpos or elem.from_master(masterpos)
        disp = elem.outputField(mesh, field.getField("Displacement"), masterpos)
        # 'disp' is an OutputValue wrapping a VectorOutputVal
        vdisp = disp.valuePtr()   # the underlying VectorOutputVal
        return realpos + self.where.factor()*coord.Coord(*vdisp)

    def undisplaced(self, mesh, elem, pos): # 2D only
        # Search master space for an x such that f(x)=pos, and return
        # the real space location of x. 'pos' is a position in real
        # space.

        delta = 0.001 # Small compared to master space.
        if config.dimension() == 2:
            mtx = smallmatrix.SmallMatrix(2,2)
            rhs = smallmatrix.SmallMatrix(2,1)
            delta_x = mastercoord.MasterCoord(delta, 0.0)
            delta_y = mastercoord.MasterCoord(0.0, delta)
        elif config.dimension() == 3:
            mtx = smallmatrix.SmallMatrix(3,3)
            rhs = smallmatrix.SmallMatrix(3,1)
            delta_x = mastercoord.MasterCoord(delta, 0.0, 0.0)
            delta_y = mastercoord.MasterCoord(0.0, delta, 0.0)
            delta_z = mastercoord.MasterCoord(0.0, 0.0, delta)
        
        res = elem.center()     # master space position

        done = False
        # Magic numbers.  The function can actually fail, because for
        # higher-order elements, the displacement mapping is
        # parabolic, and the range of the parabolic mapping might not
        # include the point pos, if it's too far away from the
        # element.  So, if we've gone for more than maxiters
        # iterations, raise an exception.
        tolerance = 1.0e-10
        maxiters = 50

        count = 0
        while not done:
            count += 1
            if count > maxiters:
                raise ooferror2.ErrConvergenceFailure(
                    "Displacement inversion", maxiters)

            fwd = self._displaced(mesh, elem, masterpos=res)
            fwddx = self._displaced(mesh, elem, masterpos=res+delta_x)
            fwddy = self._displaced(mesh, elem, masterpos=res+delta_y)
            dfdx = (fwddx-fwd)/delta
            dfdy = (fwddy-fwd)/delta
            if config.dimension() == 3:
                fwddz = self._displaced(mesh, elem, masterpos=res+delta_z)
                dfdz = (fwddz-fwd)/delta

            diff = pos-fwd

            rhs.setitem(0,0,diff[0])
            rhs.setitem(1,0,diff[1])
            if config.dimension() == 3:
                rhs.setitem(2,0,diff[2])
            
            mtx.setitem(0,0,dfdx[0])
            mtx.setitem(0,1,dfdy[0])
            mtx.setitem(1,0,dfdx[1])
            mtx.setitem(1,1,dfdy[1])
            if config.dimension() == 3:
                mtx.setitem(0,2,dfdz[0])
                mtx.setitem(1,2,dfdz[1])
                mtx.setitem(2,0,dfdx[2])
                mtx.setitem(2,1,dfdy[2])
                mtx.setitem(2,2,dfdz[2])

            ## TODO OPT: For a 2x2 matrix, is it faster to write out the
            ## solution, rather than using a general purpose routine?
            r = mtx.solve(rhs)

            if config.dimension() == 2:
                resid = (rhs[0,0]**2+rhs[1,0]**2)
                res = mastercoord.MasterCoord(res[0]+rhs[0,0],
                                              res[1]+rhs[1,0])
            elif config.dimension() == 3:
                resid = (rhs[0,0]**2+rhs[1,0]**2+rhs[2,0]**2)
                res = mastercoord.MasterCoord(res[0]+rhs[0,0],
                                              res[1]+rhs[1,0],
                                              res[2]+rhs[2,0])

            if resid<tolerance:
                done = True

        return elem.from_master(res)

# end class MeshDisplayMethod

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class EdgeDisplay(object):
    def newLayer(self):
        self.source = self.vtkSource()
        canvaslayer = gridlayers.WireGridCanvasLayer(
            self.gfxwindow.oofcanvas, self.name(), self.source)
        return canvaslayer
    def setParams(self):
        self.setSource()
        self.canvaslayer.set_lineWidth(self.width)
        self.canvaslayer.set_color(self.color)

    def whoChanged(self):
        if self.source:
            self.setSource()
        return True             # still need to call setParams

    def draw(self, gfxwindow, canvas): # only used in 2D
        themesh = self.who().resolve(gfxwindow)
        ##canvas.comment("EdgeDisplay")
        # if config.dimension() == 2:
        self.canvaslayer.set_lineColor(self.color)
        self.canvaslayer.set_lineWidth(self.width)
        polygons = self.polygons(gfxwindow, themesh)
        for polygonset in polygons:
            self.canvaslayer.draw_polygon(primitives.Polygon(polygonset))

#=--=##=--=##=--=#

class MeshEdgeDisplay(EdgeDisplay, MeshDisplayMethod):
    # EdgeDisplay draws the edges of the Elements
    def __init__(self, when, where,
                 width=defaultMeshWidth, color=defaultMeshColor,
                 filter=defaultMeshFilter): 
        ## TODO 3.1: Use a to-be-written MeshFilter class instead of
        ## SkeletonFilter when displaying Meshes, to allow filtering
        ## on Field values, etc.
        self.where = where
        self.width = width
        self.color = color
        MeshDisplayMethod.__init__(self, filter, when)

    def setParams(self):
        self.source.setEnhancement(self.where.factor())
        EdgeDisplay.setParams(self)

    def draw(self, gfxwindow, canvas):
        EdgeDisplay.draw(self, gfxwindow, canvas)

meshedges = registeredclass.Registration(
    'Element Edges',
    display.DisplayMethod,
    MeshEdgeDisplay,
    ordering=0.0,
    layerordering=display.Linear,
    params = meshdispparams + [meshColorParam, meshWidthParam, meshFilterParam],
    whoclasses = ('Mesh',),
    tip="Draw the edges of Mesh Elements.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/meshedgedisplay.xml')
    )
    
#=--=##=--=##=--=#

class SkeletonEdgeDisplay(EdgeDisplay, SkeletonDisplayMethod):
    def __init__(self, width=defaultSkeletonWidth, color=defaultSkeletonColor,
                 filter=defaultSkeletonFilter):
        self.width = width
        self.color = color
        SkeletonDisplayMethod.__init__(self, filter)

skeledges = registeredclass.Registration(
    'Element Edges',
    display.DisplayMethod,
    SkeletonEdgeDisplay,
    ordering=0.0,
    layerordering=display.Linear,
    params=[skelColorParam, skelWidthParam, skelFilterParam],
    whoclasses = ('Skeleton',),
    tip="Draw the edges of Skeleton Elements.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/skeletonedgedisplay.xml')
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

## TODO MER: Rewrite for 3D

class PerimeterDisplay(MeshDisplayMethod):
    def __init__(self, when, where, width=0, color=color.black):
        self.where = where
        self.width = width
        self.color = color
        MeshDisplayMethod.__init__(self, when)
    def draw(self, gfxwindow, canvas):
        themesh = self.who().resolve(gfxwindow)
        femesh = themesh.getObject()
        themesh.restoreCachedData(self.getTime(themesh))
        try:
            #canvas.comment("PerimeterDisplay")
            canvas.set_lineColor(self.color)
            canvas.set_lineWidth(self.width)
            for element in femesh.elements():
                el_edges = element.perimeter()
                for edge in el_edges:
                    ## TODO 3.1: Update to use MeshNodePosition instead of
                    ## PositionOutput.
                    if element.exterior(edge.startpt(), edge.endpt()):
                        pts = self.where.evaluate(femesh, [edge], [[0.0, 1.0]])
                        canvas.draw_segment(primitives.Segment(pts[0], pts[1]))
        finally:
            themesh.releaseCachedData()

if config.dimension() == 2:
    registeredclass.Registration(
        'Perimeter',
        display.DisplayMethod,
        PerimeterDisplay,
        ordering=1.0,
        layerordering=display.SemiLinear,
        params=meshdispparams + [skelColorParam, skelWidthParam],
        whoclasses = ('Mesh',),
        tip="Outline the perimeter of the Mesh",
        discussion=xmlmenudump.loadFile(
            'DISCUSSIONS/engine/reg/perimeterdisplay.xml')
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

## TODO MER: This hasn't been modified for 3D at all.

#Interface branch
class InterfaceElementDisplay(MeshDisplayMethod):
    def __init__(self, when, where,
                 boundary, #=placeholder.every.IDstring,
                 material, #=materialparameter.InterfaceAnyMaterialParameter.extranames[0],
                 width=0, color=color.black):
        self.where = where
        self.boundary=boundary
        self.material=material
        self.width = width
        self.color = color
        MeshDisplayMethod.__init__(self, when)
    def draw(self, gfxwindow, canvas):
        meshctxt = self.who().resolve(gfxwindow)
        femesh = meshctxt.getObject()
        #canvas.comment("InterfaceElementDisplay")
        canvas.set_lineColor(self.color)
        canvas.set_lineWidth(self.width)
        ANYstring=materialparameter.InterfaceAnyMaterialParameter.extranames[0]
        NONEstring=materialparameter.InterfaceAnyMaterialParameter.extranames[1]
        try:
            meshctxt.restoreCachedData(self.getTime(meshctxt))
            if self.boundary==placeholder.every.IDstring:
                for edgement in femesh.edgement_iterator():
                    if self.material!=ANYstring:
                        if edgement.material():
                            matname=edgement.material().name()
                        else:
                            matname=NONEstring
                        if self.material!=matname:
                            continue
                    el_edges = edgement.perimeter()
                    for edge in el_edges:
                        ## TODO 3.1: Update to use MeshNodePosition
                        ## instead of PositionOutput.
                        pts = self.where.evaluate(femesh, [edge], [[0.0, 1.0]])
                        canvas.draw_segment(primitives.Segment(pts[0], pts[1]))
            else:               # boundary != every
                for edgement in femesh.edgement_iterator():
                    if self.material!=ANYstring:
                        if edgement.material():
                            matname=edgement.material().name()
                        else:
                            matname=NONEstring
                        if self.material!=matname:
                            continue
                    if self.boundary not in edgement.namelist():
                        continue
                    el_edges = edgement.perimeter()
                    for edge in el_edges:
                        ## TODO 3.1: Update to use MeshNodePosition
                        ## instead of PositionOutput.
                        pts = self.where.evaluate(femesh, [edge], [[0.0, 1.0]])
                        canvas.draw_segment(primitives.Segment(pts[0], pts[1]))
        finally:
            meshctxt.releaseCachedData()

if runtimeflags.surface_mode:
    registeredclass.Registration(
        'InterfaceElement',
        display.DisplayMethod,
        InterfaceElementDisplay,
        ordering=10,
        layerordering=display.SemiLinear,
        params=meshdispparams + [
            meshparameters.MeshEdgeBdyParameterExtra(
                'boundary', placeholder.every.IDstring,
                tip='Only display edges on this boundary or interface.'),
            materialparameter.InterfaceAnyMaterialParameter(
                'material',
                materialparameter.InterfaceAnyMaterialParameter.extranames[0],
                tip="Only display edges with this material assigned to them."),
            ## TODO 3.1: Add settable defaults
            color.ColorParameter('color', color.RGBColor(0.5, 0.3, 0.5),
                                 tip=parameter.emptyTipString),
            meshWidthParam,
            meshFilterParam
            ],
        whoclasses = ('Mesh',),
        tip="Highlight the edgements (1-D elements) on the Mesh."
        ##                                 discussion=xmlmenudump.loadFile(
        ##        'DISCUSSIONS/engine/reg/perimeterdisplay.xml')
        )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SolidFillMeshDisplay(object):  # For Skeletons too.
    def newLayer(self):
        self.source = self.vtkSource()
        canvaslayer = gridlayers.SolidFilledGridCanvasLayer(
            self.gfxwindow.oofcanvas, self.name(), self.source)
        return canvaslayer
    def whoChanged(self):
        # setSource() is defined in SkeletonDisplayMethod or
        # MeshDisplayMethod, one of which must be an additional base
        # class for any subclass of SolidFilledGridCanvasLayer.
        self.setSource()
        themesh = self.who().resolve(self.gfxwindow)
        # Subclasses must define setCellData(), which sets the
        # vtkCellData values to be plotted.
        self.setCellData(themesh)
        self.setLUT()
        return True

    def setLUT(self):
        # Subclasses must define getLUT(), which returns the color
        # lookup table, and getRange(), which returns the min and max
        # values to be plotted.
        ctxt = self.who()
        if ctxt is None:
            debug.fmsg("Failed to find who object")
            return
        themesh = ctxt.resolve(self.gfxwindow)
        dmin, dmax = self.getRange(themesh)
        mainthread.runBlock(
            self.canvaslayer.set_lookupTable,
            (self.getLUT(themesh), dmin, dmax))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# TODO 3.1: Add menu items to set defaultNoMaterial and defaultNoColor.
# MicrostructureMaterialDisplay should share its color parameters with
# the Skeleton and Mesh MaterialDisplays.

defaultNoMaterial = color.black # color used for elements with no material
defaultNoColor = color.blue     # color used for materials with no color

class MaterialDisplay(SolidFillMeshDisplay):
    def __init__(self, no_material=defaultNoMaterial, no_color=defaultNoColor):
        SolidFillMeshDisplay.__init__(self)
        self.no_color = no_color
        self.no_material = no_material
        self.matchangeSignals = [
            switchboard.requestCallback("material changed",
                                        self.matlChangedCB),
            switchboard.requestCallback("materials changed in microstructure",
                                        self.matlAssignmentsChangedCB)]
    def destroy(self, destroy_canvaslayer):
        map(switchboard.removeCallback, self.matchangeSignals)
        super(MaterialDisplay, self).destroy(destroy_canvaslayer)

    def draw(self, gfxwindow, canvas): # 2D only
        #canvas.comment("Material Color")
        if config.dimension() == 2:
            themesh = self.who().resolve(gfxwindow)
            polygons = self.polygons(gfxwindow, themesh)
            # colorcache is a dictionary of colors keyed by Material.  It
            # prevents us from having to call material.fetchProperty for
            # each element.
            colorcache = {}
            for polygon, material in zip(polygons,
                                         self.materials(gfxwindow, themesh)):
                if material is not None:
                    try:
                        # If material has been seen already, retrieve its color.
                        color = colorcache[material]
                    except KeyError:
                        # This material hasn't been seen yet.
                        try:
                            colorprop = material.fetchProperty('Color')
                            color = colorprop.color()
                        except ooferror.ErrNoSuchProperty:
                            color = None
                        colorcache[material] = color
                    if color is not None:
                        canvas.set_fillColor(color)
                        canvas.fill_polygon(primitives.Polygon(polygon))
 
    def setParams(self):
        self.setSource()
        self.setLUT()

    def getLUT(self, themesh):
        return ooflib.SWIG.engine.material.getMaterialColorLookupTable(
            themesh.getMicrostructure(), self.no_color, self.no_material)
    def getRange(self, themesh):
        return (0, themesh.getMicrostructure().nCategories())
    def setCellData(self, themesh):
        # cellData() is defined in subclasses and is different for
        # Skeletons and Meshes.
        self.canvaslayer.set_CellData(self.cellData(themesh))
    def matlAssignmentsChangedCB(self, ms):
        # sb "materials changed in microstructure"
        themesh = self.who().resolve(self.gfxwindow)
        if themesh.getMicrostructure() is ms:
            self.setCellData(themesh)
            self.setLUT()
    def matlChangedCB(self, *args, **kwargs): # sb "material changed"
        self.setLUT()

class SkeletonMaterialDisplay(MaterialDisplay, SkeletonDisplayMethod):
    def __init__(self, no_material=defaultNoMaterial, no_color=defaultNoColor,
                 filter=defaultSkeletonFilter):
        MaterialDisplay.__init__(self, no_material, no_color)
        SkeletonDisplayMethod.__init__(self, filter)
    def destroy(self, destroy_canvaslayer):
        super(SkeletonMaterialDisplay, self).destroy(destroy_canvaslayer)
    def materials(self, gfxwindow, skelctxt): # 2D only
        skel = skelctxt.getObject()
        return [element.material(skel) for element in skel.element_iterator()]
    def cellData(self, skelctxt):
        return skelctxt.getObject().getMaterialCellData(self.filter)

class MeshMaterialDisplay(MaterialDisplay, MeshDisplayMethod):
    def __init__(self, when, where,
                 no_material=defaultNoMaterial, no_color=defaultNoColor,
                 filter=defaultMeshFilter):
        self.where = where
        MaterialDisplay.__init__(self, no_material, no_color)
        MeshDisplayMethod.__init__(self, filter, when)
    def destroy(self, destroy_canvaslayer):
        super(MeshMaterialDisplay, self).destroy(destroy_canvaslayer)
    def cellData(self, meshctxt):
        return meshctxt.getObject().getMaterialCellData(
            meshctxt.getObject().skeleton, self.filter)
        
    def materials(self, gfxwindow, meshctxt): # 2D only
        # Because MeshDisplayMethod.polygons only returns the borders
        # of elements with an assigned material, this should only
        # return the non-trivial materials.
        themesh = meshctxt.getObject()
        allmats = [element.material() for element in themesh.elements()]
        return allmats
    
matcolorparams = [
    color.ColorParameter('no_material', defaultNoMaterial,
                         tip="Color to use if an element has no material."),
    color.ColorParameter('no_color', defaultNoColor,
                         tip="Color to use if a material has no color.")
]
    
registeredclass.Registration(
    'Material Color',
    display.DisplayMethod,
    SkeletonMaterialDisplay,
    layerordering=display.Planar(1),
    ordering=0.1,
    params=matcolorparams + [skelFilterParam],
    whoclasses=('Skeleton',),
    tip="Fill each Element with the color of its assigned Material.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/skeletonmaterialdisplay.xml')
    )

registeredclass.Registration(
    'Material Color',
    display.DisplayMethod,
    MeshMaterialDisplay,
    ordering=0.11,
    layerordering=display.Planar(2),
    params=meshdispparams + matcolorparams + [meshFilterParam],
    whoclasses=('Mesh',),
    tip="Fill each Element with the color of its assigned Material.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/meshmaterialdisplay.xml')
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#


class SkeletonQualityDisplay(SolidFillMeshDisplay, SkeletonDisplayMethod):
    contourmaplevels = 32
    def __init__(self, alpha, min, max, colormap, filter):
        self.alpha = alpha
        self.colormap = colormap
        self.max = max          # parameter value
        self.min = min          # parameter value
        self.vmax = None
        self.vmin = None
        self.contourmaphidden = False
        self.lock = lock.Lock()
        SolidFillMeshDisplay.__init__(self)
        SkeletonDisplayMethod.__init__(self, filter)

    def destroy(self, destroy_canvaslayer):
        super(SkeletonQualityDisplay, self).destroy(destroy_canvaslayer)

    def contour_capable(self):
        return True

    def draw(self, gfxwindow, canvas): # 2D only
        self.lock.acquire()
        try:
            #canvas.comment("Skeleton Energy")
            skel = self.who().resolve(gfxwindow).getObject()
            # get polygons and element energy in one pass
            polyenergy = [(el.perimeter(), el.energyTotal(skel, self.alpha))
                        for el in skel.element_iterator()
                        if not el.illegal()]
            # find actual range of data
            self.vmax = self.vmin = polyenergy[0][1]
            for (p,e) in polyenergy[1:]:
                if e > self.vmax:
                    self.vmax = e
                if e < self.vmin:
                    self.vmin = e
            # Set plot limits to either the actual data extremes, or
            # to the passed in values.  Store the actual limits in
            # vmin and vmax.
            if self.max == automatic.automatic:
                dmax = self.vmax
            else:
                dmax = self.max
                self.vmax = dmax
            if self.min == automatic.automatic:
                dmin = self.vmin
            else:
                dmin = self.min
                self.vmin = dmin
            if dmax == dmin:
                dmax += 1.0
                self.vmax += 1.0
                dmin -= 1.0
                self.vmin -= 1.0
            canvas.set_colormap(self.colormap)
            for polygon, energy in polyenergy:
                canvas.set_fillColor((energy-dmin)/(dmax-dmin))
                canvas.fill_polygon(primitives.Polygon(polygon))
        finally:
            self.lock.release()

    def getLUT(self, skelctxt):
        return self.colormap.getVtkLookupTable(self.contourmaplevels)

    def getRange(self, skelctxt):
        # self.vmin and self.vmax are set by self.cellData(), which
        # should have been called before getRange().
        assert self.vmin is not None
        if self.min == automatic.automatic:
            vmin = self.vmin
        else:
            vmin = self.min
        if self.max == automatic.automatic:
            vmax = self.vmax
        else:
            vmax = self.max
        return vmin, vmax
        
    def setCellData(self, skelctxt):
        data = self.cellData(skelctxt)
        self.canvaslayer.set_CellData(data)

    def cellData(self, skelctxt):
        vals = skelctxt.getObject().getEnergyCellData(self.alpha, self.filter)
        if vals.size() > 0:
            self.vmin, self.vmax = vtkutils.getDataArrayRange(vals)
        else:
            self.vmin = self.vmax = 0.0
        return vals

    def setParams(self):
        self.setSource()
        self.setLUT()
        self.setCellData(self.who().resolve(self.gfxwindow))
        self.source.Modified()  # because filter may have changed

    def skelDataChangedCB(self, skeletonname): # sb "Skeleton changed"
        hoo = self.who()
        if hoo:
            skelctxt = hoo.resolve(self.gfxwindow)
            if skelctxt.path() == skeletonname:
                #self.setSource()
                self.setCellData(skelctxt)
                self.setLUT()
                self.source.Modified()
        
registeredclass.Registration(
    'SkeletonQuality',
    display.DisplayMethod,
    SkeletonQualityDisplay,
    ordering=100,
    layerordering=display.Planar(1.1),
    whoclasses=('Skeleton',),
    params=[cskeletonmodifier.alphaParameter,
            parameter.RegisteredParameter('colormap', colormap.ColorMap,
                                          colormap.ThermalMap(),
                                          tip="color scheme"),
            AutoNumericParameter('min', automatic.automatic,
                               tip="lowest energy to display, or 'automatic'"),
            AutoNumericParameter('max', automatic.automatic,
                              tip="highest energy to display, or 'automatic'"),
            skelFilterParam
            ],
    tip="Color each element according to its effective energy.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/skelqualdisplay.xml')
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

def defaultSkeletonEdgeDisplay():
    # Call the Registration, so that the current values of the params
    # are used.
    return skeledges()

ghostgfxwindow.DefaultLayer(skeletoncontext.skeletonContexts,
                            defaultSkeletonEdgeDisplay)

def defaultMeshEdgeDisplay():
    return meshedges()

ghostgfxwindow.DefaultLayer(mesh.meshes, defaultMeshEdgeDisplay)
