# -*- python -*-
# $RCSfile: skeletonbdydisplay.py,v $
# $Revision: 1.27.10.30 $
# $Author: langer $
# $Date: 2014/09/10 21:28:44 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common.IO import canvaslayers
from ooflib.common import color
from ooflib.common import debug
from ooflib.common import primitives
from ooflib.common import registeredclass
from ooflib.common.IO import automatic
from ooflib.common.IO import display
from ooflib.common.IO import ghostgfxwindow
from ooflib.common.IO import gfxmanager
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump
from ooflib.engine import skeletonboundary
import math
import string

# Special parameter class for skeleton boundaries.  Returns a
# list of strings corresponding to the names of boundaries in a
# given skeleton.  The custom class is primarily to allow for a
# special skeleton-smart widget.

class SkeletonBoundaryListParameter(parameter.ListOfStringsParameter):
    pass

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Base class for SkeletonBoundaryDisplay and
# SelectedSkeletonBoundaryDisplay.

class SkeletonBdyDisplayBase(display.DisplayMethod):
    def __init__(self, color, linewidth, glyphsize, resolution):
        self.color = color
        self.linewidth = linewidth
        self.glyphsize = glyphsize
        self.resolution = resolution
        display.DisplayMethod.__init__(self)
        self.sbcallbacks = [
            switchboard.requestCallback("new boundary configuration",
                                        self.newBdyConfigCB)
            ]

    def destroy(self, destroy_canvaslayer):
        map(switchboard.removeCallback, self.sbcallbacks)
        display.DisplayMethod.destroy(self, destroy_canvaslayer)

    def newBdyConfigCB(self, skelctxt):
        hoo = self.who()
        if hoo and hoo.resolve(self.gfxwindow) is skelctxt:
            self.whoChanged()

    def _newLayer(self, name):
        # The names given to the sublayers here must be the same as
        # the names returned by the SkelContextBoundary boundaryType()
        # methods.
        layer = canvaslayers.ComboCanvasLayer()
        canvas = self.gfxwindow.oofcanvas
        layer.addSublayer("face",
                          canvaslayers.FaceGlyphLayer(canvas, name+"-Face"))
        layer.addSublayer("edge",
                          canvaslayers.EdgeGlyphLayer(canvas, name+"-Edge"))
        layer.addSublayer("node",
                          canvaslayers.PointGlyphLayer(canvas, name+"-Point"))
        return layer

    def setParams(self):
        gsize = self.resolveGlyphSize(self.glyphsize)

        flayer = self.canvaslayer.getSublayer("face")
        flayer.set_color(self.color)
        flayer.set_glyphColor(self.color)
        flayer.set_coneGeometry(gsize, self.resolution)

        elayer = self.canvaslayer.getSublayer("edge")
        elayer.set_color(self.color)
        elayer.set_glyphColor(self.color)
        elayer.set_coneGeometry(gsize, self.resolution)
        elayer.set_lineWidth(self.linewidth)

        player = self.canvaslayer.getSublayer("node")
        player.set_glyphColor(self.color)
        player.set_sphereGeometry(gsize, self.resolution)

    def resolveGlyphSize(self, glyphsize):
        # If the glyph size is 'automatic', choose a reasonable value
        # based on the average element size.
        if glyphsize is automatic.automatic:
            skelctxt = self.who().resolve(self.gfxwindow)
            if skelctxt is None:
                return 1.0
            msctxt = skelctxt.parent
            sz = msctxt.getObject().size()
            vol = 1.
            for x in sz:        # loop over components of a Coord
                vol *= x
            elvol = vol/skelctxt.getObject().nelements() # avg element volume
            linsize = elvol**(1./config.dimension())     # avg element size
            return 0.5*linsize
        return glyphsize        # glyphsize is not 'automatic'
        
    # Double dispatch routines for canvas layer construction.
    # buildXXXXLayer() is called by buildDisplayLayer() in the
    # subclasses of SkelContextBoundary.
    def buildFaceLayer(self, bdy, skelctxt, canvaslayer):
        skel = skelctxt.getObject()
        b = bdy.boundary(skel)
        faces = b.getFaces()
        self._buildDirectedLayer(faces, canvaslayer)
    def buildEdgeLayer(self, bdy, skelctxt, canvaslayer):
        skel = skelctxt.getObject()
        b = bdy.boundary(skel)
        edges = b.getOrientedSegments()
        self._buildDirectedLayer(edges, canvaslayer)
    def _buildDirectedLayer(self, parts, canvaslayer):
        ## TODO OPT: Move this method to C++.  Then there would be no
        ## need to swig OrientedCSkeletonFaceSet, et al.
        for part in parts:
            canvaslayer.addDirectedCell(part.getCellType(),
                                        part.getPointIds(),
                                        part.get_direction_vector())
    def buildPointLayer(self, bdy, skelctxt, canvaslayer):
        skel = skelctxt.getObject()
        b = bdy.boundary(skel)
        points = b.getNodes()
        ## TODO OPT: Move this loop to C++.  Then there would be no
        ## need to swig OrientedCSkeletonFaceSet, et al.
        for pt in points:
            canvaslayer.addCell(pt.getCellType(), pt.getPointIds())
    
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Layer for showing the boundaries (point, edge, and face) of a
# skeleton.  The user specifies which boundaries to display via a
# parameter.

class SkeletonBoundaryDisplay(SkeletonBdyDisplayBase):
    def __init__(self, boundaries, color, linewidth, glyphsize, resolution):
        self.boundaries = boundaries
        SkeletonBdyDisplayBase.__init__(self, color, linewidth, glyphsize,
                                        resolution)

    def newLayer(self):
        return self._newLayer("SkeletonBoundary")

    def draw(self, gfxwindow, canvas): # 2D only
        skel = self.who().resolve(gfxwindow)
        skelobj = skel.getObject()
        canvas.set_lineColor(self.color)
        for k in self.boundaries:
            try:
                b = skelobj.edgeboundaries[k]
            except KeyError:
                pass
            else:
                for e in b.edges:
                    nodes = e.get_nodes()
                    canvas.set_lineWidth(self.linewidth)
                    canvas.draw_segment(primitives.Segment(
                            nodes[0].position(), nodes[1].position()))
                    # Boundaries are directed from 0 to 1.
                    center = (nodes[0].position() + nodes[1].position())/2
                    diff = (nodes[1].position() - nodes[0].position())
                    # Zero of angles is the y-axis, not the x-axis...
                    angle = math.atan2(-diff.x, diff.y)
                    canvas.set_lineWidth(self.arrowsize) # ?
                    canvas.draw_triangle(center, angle)
            
        canvas.set_lineWidth(self.dotsize)
        canvas.set_fillColor(self.color)
        for k in self.boundaries:
            try:
                b = skelobj.pointboundaries[k]
            except KeyError:
                pass
            else:
                for n in b.nodes:
                    canvas.draw_dot(n.position())

    # def getTimeStamp(self, gfxwindow):
    #     return max( self.timestamp,
    #                 self.who().resolve(gfxwindow).bdytimestamp )

    def whoChanged(self):
        skelctxt = self.who().resolve(self.gfxwindow)
        if not skelctxt:
            self.canvaslayer.clear()
            return
        skelobj = skelctxt.getObject()
        # Get total number of faces, edges, and nodes in the chosen bdys.
        counts = {}
        for bdyname in self.boundaries:
            bdy = skelctxt.getBoundary(bdyname)
            n = counts.get(bdy.boundaryType(), 0)
            n += bdy.size(skelobj)
            counts[bdy.boundaryType()] = n
        # Create the grids for the layers
        points = skelobj.getPoints()
        # Don't just loop over counts.items() here.  That won't
        # include newly empty layers that have to be cleared.
        for btype, layer in self.canvaslayer.sublayers.items():
            n = counts.get(btype, 0)
            if n > 0:
                layer.newGrid(points, n)
            else:
                layer.clear()
        # Create the cells in the grids.
        for bdyname in self.boundaries:
            bdy = skelctxt.getBoundary(bdyname)
            # bdy.buildDisplayLayer is the double dispatch routine
            # that calls the appropriate buildXXXXLayer routine in
            # SkeletonBdyDisplayBase.
            sublayer = self.canvaslayer.getSublayer(bdy.boundaryType())
            bdy.buildDisplayLayer(self, skelctxt, sublayer)
            sublayer.recomputeDirections()

        # setParams needs to be run when who changes because the glyph
        # size might be computed automatically from the element size.
        self.setParams()
        return False

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Layer for showing the selected Skeleton boundary.  The boundary is
# selected on the Skeleton Boundary Page.  Unlike
# SkeletonBoundaryDisplay, SelectedSkeletonBoundaryDisplay can only
# display one boundary at a time.  It still uses a ComboCanvasLayer so
# that it can switch between glyph types easily.

class SelectedSkeletonBoundaryDisplay(SkeletonBdyDisplayBase):
    def __init__(self, color, linewidth, glyphsize, resolution):
        SkeletonBdyDisplayBase.__init__(self, color, linewidth, glyphsize,
                                        resolution)
        self.sbcallbacks.extend([
            switchboard.requestCallback("boundary selected", 
                                        self.bdySelectedCB),
            switchboard.requestCallback("boundary unselected",
                                        self.bdyUnselectedCB)])

    def newLayer(self):
        return self._newLayer("SelectedSkeletonBoundary")
    
    def bdySelectedCB(self, skelctxt, bdyname): # sb "boundary selected"
        if skelctxt is self.who().resolve(self.gfxwindow):
            self.whoChanged()
            self.setParams()             # recomputes automatic glyph size
    def bdyUnselectedCB(self, skelctxt): # sb "boundary unselected"
        if skelctxt is self.who().resolve(self.gfxwindow):
            self.canvaslayer.clear()

    def whoChanged(self):
        skelctxt = self.who().resolve(self.gfxwindow)
        if not skelctxt:
            self.canvaslayer.clear()
            return True
        bdy = skelctxt.getSelectedBoundary()
        skelobj = skelctxt.getObject()
        if not bdy or bdy.size(skelobj) == 0:
            self.canvaslayer.clear()
            return True
        points = skelobj.getPoints()
        for btype, layer in self.canvaslayer.sublayers.items():
            if btype == bdy.boundaryType():
                layer.newGrid(points, bdy.size(skelobj))
                # buildDisplayLayer() calls buildEdgeLayer(),
                # buildFaceLayer(), or buildPointLayer() in
                # SkeletonBdyDisplayBase.
                bdy.buildDisplayLayer(self, skelctxt, layer)
                layer.recomputeDirections()
            else:
                layer.clear()
        # setParams needs to be run when who changes because the glyph
        # size might be computed automatically from the element size.
        self.setParams()
        return False
        
    def draw(self, gfxwindow, canvas): # 2D only
        skel = self.who().resolve(gfxwindow)
        skelobj = skel.getObject()
        bdy = skel.getSelectedBoundary()  # SkelContextBoundary
        if bdy is not None:
            # bdy.draw calls either drawEdgeBoundary(),
            # drawPointBoundary(), or drawFaceBoundary().  Those methods
            # used to be defined in this file, but they were deleted
            # in the move to 3D.  When the final merge occurs, 2D
            # graphics will be done in vtk like the 3D graphics is
            # now, and those methods won't be needed, so I'm not
            # restoring them now.
            bdy.draw(self, gfxwindow, canvas, skelobj)

    # def getTimeStamp(self, gfxwindow):
    #     skelcontext = self.who().resolve(gfxwindow)
    #     bdy = skelcontext.getSelectedBoundary()
    #     if bdy is not None:
    #         return max(self.timestamp, skelcontext.bdyselected,
    #                    skelcontext.getSelectedBoundary().timestamp)
    #     return max(self.timestamp, skelcontext.bdyselected)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Default parameters for boundary displays

defaultSkelBdyColor = color.orange
defaultSkelBdyLineWidth = 4

if config.dimension() == 2:
    widthRange = (0,10)
else:
    # In vtk, line widths of 0 cause errors
    widthRange = (1,10)

skelbdyparams = [
    color.ColorParameter('color', value=defaultSkelBdyColor,
                         tip="Color for the selected boundary."),
    parameter.IntRangeParameter('linewidth', widthRange,
                                defaultSkelBdyLineWidth,
                                tip="Line width for edge boundaries.")]

if config.dimension() == 2:
    defaultSkelBdyGlyphSize = 10
    skelbdyparams.append(
         parameter.IntRangeParameter('glyphsize', (0, 20),
                                     defaultSkelBdyGlyphSize,
                                     tip="Arrow size for edge boundaries."))

elif config.dimension() == 3:
    defaultSkelBdyGlyphSize = automatic.automatic
    defaultSkelBdyGlyphResolution = 20
    skelbdyparams.extend(
        [parameter.AutoNumericParameter(
                'glyphsize', 
                defaultSkelBdyGlyphSize,
                tip="Size of boundary markers."),
         parameter.IntParameter(
                'resolution',
                defaultSkelBdyGlyphResolution,
                tip='Number of polygons to use to draw markers.')]
         )
    

def _setSkelBdyParams(menuitem, color, linewidth, glyphsize, resolution):
    global defaultSkelBdyColor
    global defaultSkelBdyLineWidth
    global defaultSkelBdyGlyphSize
    global defaultSkelBdyGlyphResolution
    defaultSkelBdyColor = color
    defaultSkelBdyLineWidth = linewidth
    defaultSkelBdyGlyphSize = glyphsize
    defaultSkelBdyGlyphResolution = resolution

mainmenu.gfxdefaultsmenu.Skeletons.addItem(oofmenu.OOFMenuItem(
    "Boundary",
    callback=_setSkelBdyParams,
    params=skelbdyparams,
    ordering=4.5,
    help="Set default parameters for displaying skeleton boundaries.",
    discussion="""<para>

    This command sets the default parameters for the
    <xref linkend="RegisteredClass-SelectedSkeletonBoundaryDisplay"/>,
    which displays the currently
    <link linkend="Section-Tasks-SkeletonBoundaries">selected
    <classname>Skeleton</classname> boundaries</link>.  Put this command
    in the &oof2rc; file to set default values for all &oof2; sessions.
    
    </para>"""))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Registrations for boundary displays

registeredclass.Registration(
    'Boundaries',
    display.DisplayMethod,
    SkeletonBoundaryDisplay,
    params=([SkeletonBoundaryListParameter('boundaries', [],
                                           tip="Boundaries to display")]
            + skelbdyparams),
    ordering=1.0,
    layerordering=display.SemiLinear(2),
    whoclasses=('Skeleton',),
    tip="Display some or all of the boundaries of the Skeleton",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/skeletonbdydisplay.xml')
    )


selectedSkeletonBoundaryDisplay = registeredclass.Registration(
    'Selected Boundary',
    display.DisplayMethod,
    SelectedSkeletonBoundaryDisplay,
    params=skelbdyparams,
    ordering=2.3,
    layerordering=display.SemiLinear(2.1),
    whoclasses=('Skeleton',),
    tip="Display the currently selected boundary.",
    discussion = xmlmenudump.loadFile('DISCUSSIONS/engine/reg/skeletonselbdydisplay.xml')
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Predefined display method for the selected boundary

def defaultSelectedSkeletonBoundaryDisplay():
    return selectedSkeletonBoundaryDisplay(
        color=defaultSkelBdyColor,
        linewidth=defaultSkelBdyLineWidth,
        glyphsize=defaultSkelBdyGlyphSize,
        resolution=defaultSkelBdyGlyphResolution)


ghostgfxwindow.PredefinedLayer('Skeleton', '<topmost>',
                               defaultSelectedSkeletonBoundaryDisplay)
