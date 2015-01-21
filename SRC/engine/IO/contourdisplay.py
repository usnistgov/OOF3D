# -*- python -*-
# $RCSfile: contourdisplay.py,v $
# $Revision: 1.94.4.32 $
# $Author: langer $
# $Date: 2014/11/24 21:44:53 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.SWIG.common import lock
from ooflib.SWIG.common import progress
from ooflib.SWIG.common.IO import gridlayers
from ooflib.SWIG.engine import skeletonfilter
from ooflib.common import color
from ooflib.common import debug
from ooflib.common import mainthread
from ooflib.common import primitives
from ooflib.common import registeredclass
from ooflib.common import subthread
from ooflib.common import utils
from ooflib.common.IO import automatic
from ooflib.common.IO import colormap
from ooflib.common.IO import display
from ooflib.common.IO import parameter
from ooflib.common.IO import placeholder
from ooflib.common.IO import reporter
from ooflib.common.IO import xmlmenudump
from ooflib.engine.IO import displaymethods
from ooflib.engine.IO import output
from ooflib.engine.IO import outputDefs

if config.dimension() == 2:
    from ooflib.SWIG.engine.IO import contour
else:
    from ooflib.SWIG.common.IO import vtkutils

import types


RegisteredParameter = parameter.RegisteredParameter
IntParameter = parameter.IntParameter
IntRangeParameter = parameter.IntRangeParameter
FloatParameter = parameter.FloatParameter
AutoNumericParameter = parameter.AutoNumericParameter
ValueSetParameter = parameter.ValueSetParameter

# ZDisplayParams does not include the "level" one, because it needs to
# have different defaults for the ContourDisplay and for the other z
# displays, such as the MeshCenterFillDisplay.

# TODO 3.1 : Add a vector plot DisplayMethod, and maybe an ellipsoid plot
# for symmetric tensors.

zdisplayparams = [
    placeholder.TimeParameter('when', 
                              value=placeholder.latest,
                              tip='Time at which to plot'),
    output.ScalarOutputParameter('what', tip='Quantity to be plotted'),
    RegisteredParameter('where', displaymethods.MeshNodePosition,
                        value=displaymethods.Actual(),
                        tip="Plot at displaced or original position?"),
    AutoNumericParameter('min_contour', automatic.automatic, 
                         tip="level of lowest contour, or 'automatic'"),
    AutoNumericParameter('max_contour', automatic.automatic,
                         tip="level of highest contour, or 'automatic'"),
    RegisteredParameter('filter', skeletonfilter.SkeletonFilterPtr,
                        skeletonfilter.NullFilter())
    ]


class ZDisplay(displaymethods.MeshDisplayMethod):
    def __init__(self, when, what, where, min_contour, max_contour, levels, 
                 filter):
        self.what = what.clone()   # Should be clones, or not?
        self.where = where
        self.min_contour = min_contour
        self.max_contour = max_contour
        self.levels = levels
        self.lock = lock.SLock()
        self.contourmaphidden = False
        self.contourmap_user_hide = 0
        displaymethods.MeshDisplayMethod.__init__(self, filter, when)

    def contour_capable(self):
        return True
    
    # def explicit_contour_hide(self):
    #     self.contourmap_user_hide = 1
    #     self.hide_contourmap()
        
    # def hide_contourmap(self):
    #     self.contourmaphidden = True

    # def show_contourmap(self):
    #     self.contourmaphidden = False

    def incomputable(self):
        hoo = self.who()
        if hoo is None:
            return True
        mesh = hoo.resolve(self.gfxwindow)
        return (self.what.incomputable(mesh) or 
               displaymethods.MeshDisplayMethod.incomputable(self))

    
contourparams = zdisplayparams + [
    ValueSetParameter('levels', 11,
                      tip="number of levels or list of levels (in [])"),
    IntParameter('nbins', 5, tip="number of internal subdivisions per element")
    ]


class ContourDisplay(ZDisplay):
    def __init__(self, when, what, where, min_contour, max_contour, levels,
                 nbins, filter):
        self.nbins = nbins
        ZDisplay.__init__(self, when, what, where, min_contour, max_contour,
                          levels, filter)

    # Given the inputs.
    def find_levels(self, mesh, what): # 2D only
        assert config.dimension() == 2
        nlevels = self.levels
        clevels = None
        if type(nlevels) == types.ListType or type(nlevels) == types.TupleType:
            clevels = nlevels
            nlevels = len(clevels)

        # Make a list of mastercoords of all nodes of all elements
        ## TODO OPT: Rework this to use generators instead of passing
        ## lists around.  It may be faster for large meshes.
        nodepoints = []
        for element in mesh.elements():
            master = element.masterelement()
            el_mpos = []                # master coords of nodes in this element
            for n in range(master.nnodes()):
                el_mpos.append(master.get_protonode(n).mastercoord())
            nodepoints.append(el_mpos)

        # Evaluate the function at the nodes

        values = [float(x) for x in 
                  what.evaluate(mesh, mesh.elements(), nodepoints)]
        # Get function values grouped by element
        evalues = utils.unflatten(nodepoints, values)

        # TODO OPT: This is a lot of evaluation work -- are
        # these values cached somewhere, and can they be reused?
        
##        vmax = max(values)
##        for (vals, element) in zip(evalues, mesh.elements()):
##            if vmax in vals:
##                debug.fmsg('max found in element', element, vals)
##                break

        # Determine contour levels, if necessary
        if clevels is None:             # contours not specified by user
            # Find range of values.  This is just approximate, since the
            # interpolation within an element may give a value outside of
            # the range spanned by the nodal values.
            if self.min_contour == automatic.automatic:
                vmin = float(min(values))
            else:
                vmin = float(self.min_contour)
                
            if self.max_contour == automatic.automatic:
                vmax = float(max(values))
            else:
                vmax = float(self.max_contour)

            if nlevels == 1:
                clevels = [0.5*(vmax + vmin)]
            else:
                dz = (vmax - vmin)/(nlevels - 1)
                clevels = [vmin + i*dz for i in range(nlevels)]

        return clevels, evalues

##    def draw_subcells(self, mesh, device): # for debugging, presumably
##        for element in mesh.elements():
##            cells = \
##                  element.masterelement().contourCells(self.nbins)
##            device.set_lineWidth(0)
##            device.set_lineColor(color.red)
##            for cell in cells:
##                cellpoints = self.where.evaluate(mesh, [element],
##                                                 [cell.corners])
##                device.draw_polygon(primitives.Polygon(cellpoints))
##            device.set_lineColor(color.black)


#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#


if config.dimension() == 2:
    class PlainContourDisplay(ContourDisplay):
        def __init__(self, when, what, where,
                     min_contour=automatic.automatic,
                     max_contour=automatic.automatic,
                     levels=11, nbins=5, width=0, color=color.black):
            ContourDisplay.__init__(self, when, what, where,
                                    min_contour, max_contour,
                                    levels, nbins)
            self.width = width
            self.color = color
            self.contour_max = None
            self.contour_min = None
            self.contour_levels = None
        def get_contourmap_info(self):
            return (self.contour_min, self.contour_max, self.contour_levels)

        # Called on a subthread, "device" is a buffered device, so
        # commands to it do not need to be on the main thread.
        def draw(self, gfxwindow, device):
            self.lock.acquire()
            meshctxt = mainthread.runBlock(self.who().resolve, (gfxwindow,))
            mesh = meshctxt.getObject()
            meshctxt.restoreCachedData(self.getTime(meshctxt))
            prog = progress.getProgress("Contour plot", progress.DEFINITE)
            try:
                meshctxt.precompute_all_subproblems()
                # self.draw_subcells(mesh, device)
                device.comment("PlainContourDisplay")
                device.set_lineWidth(self.width)
                device.set_lineColor(self.color)

                # clevels is a list of contour values.
                # evalues is a list of lists of function values for the
                # nodes of each element.
                clevels, evalues = self.find_levels(mesh, self.what)
                ecount = 0
                for element in mesh.elements():
                    ## TODO MERGE: hideEmptyElements used to be a
                    ## gfxwindow setting, but in 3D it was removed.
                    ## Mesh filters now accomplish the same thing.
                    if (not gfxwindow.settings.hideEmptyElements) or \
                           ( element.material() is not None ) :
                        (contours, elmin, elmax)  = contour.findContours(
                            mesh, element, self.where,
                            self.what, clevels,
                            self.nbins, 0)
                        for cntr in contours:
                            for loop in cntr.loops:
                                device.draw_polygon(loop)
                            for curve in cntr.curves:
                                device.draw_curve(curve)
                    ecount += 1
                    prog.setFraction((1.*ecount)/mesh.nelements())
                    prog.setMessage("drawing %d/%d elements" %
                                    (ecount, mesh.nelements()))
                self.contour_min = min(clevels)
                self.contour_max = max(clevels)
                self.contour_levels = clevels
                contour.clearCache()
            finally:
                self.lock.release()
                meshctxt.releaseCachedData()

        # Called on a subthread.
        def draw_contourmap(self, gfxwindow, device):
            self.lock.acquire()
            try:
                if self.contour_max is not None: # contours have been drawn
                    aspect_ratio = gfxwindow.settings.aspectratio
                    height = self.contour_max - self.contour_min
                    width = height/aspect_ratio

                    # device.comment("Contourbar minimum: %s" % self.contour_min)
                    # device.comment("Contourbar maximum: %s" % self.contour_max)
                    device.set_lineWidth(self.width)
                    device.set_lineColor(self.color)

                    for lvl in self.contour_levels:
                        r_lvl = lvl - self.contour_min
                        device.draw_curve( primitives.Curve(
                            [primitives.Point(0.0, r_lvl),
                             primitives.Point(width, r_lvl)] ))
            finally:
                self.lock.release()

    defaultLineWidth = 0
    widthRange = (0,10)

    registeredclass.Registration(
        'Contour Line',
        display.DisplayMethod,
        PlainContourDisplay,
        ordering=3.0,
        layerordering=display.Linear(1),
        whoclasses=('Mesh',),
        params = contourparams +
        [IntRangeParameter('width', widthRange, defaultLineWidth, tip="line width"),
         color.ColorParameter('color', color.black, tip="line color")],
        tip="Draw contour lines for the given output data.",
        discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/plaincontour.xml')
        )


#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#=*=#

## TODO 3.1: Allow the elements to be subdivided, finer than the actual
## Mesh.  Use nbins.

class FilledContourDisplay(ContourDisplay):
    def __init__(self, when, what, where,
                 min_contour=automatic.automatic,
                 max_contour=automatic.automatic,
                 levels=11, nbins=5,
                 colormap=colormap.ThermalMap(),
                 filter=displaymethods.defaultMeshFilter):
        ContourDisplay.__init__(self, when, what, where,
                                min_contour, max_contour, levels, nbins, filter)
        self.colormap = colormap
        # contour_min and contour_max are the actual limits used for
        # the contour color map.  min_contour and max_contour are the
        # limits provided by the user, and may be 'automatic'.
        self.contour_max = None
        self.contour_min = None
        self.contour_levels = None
        self.datarange = None

    # Return the colormap info generated by the previous "draw".
    def get_contourmap_info(self):
        return (self.contour_min, self.contour_max, self.contour_levels)

    # Called on a subthread, "device" is buffered.
    def draw(self, gfxwindow, device): # 2D only
        self.lock.acquire()
        meshctxt = mainthread.runBlock(self.who().resolve, (gfxwindow,))
        mesh = meshctxt.getObject()
        meshctxt.restoreCachedData(self.getTime(meshctxt))
        prog = progress.getProgress("Contour plot", progress.DEFINITE)
        try:
            self.contour_max = None
            self.contour_min = None
            self.contour_levels = []
            meshctxt.precompute_all_subproblems()
            # device.comment("FilledContourDisplay")
            # clevels is a list of contour values.
            # evalues is a list of lists of function values
            # for the nodes of each element.
            clevels, evalues = self.find_levels(mesh, self.what)
            minval = min(clevels)
            maxval = max(clevels)
            nlevels = len(clevels)
            valrange = maxval - minval
            if valrange == 0.0:
                valrange = 1
            factor = 1./valrange
            offset = -minval*factor

            device.set_colormap(self.colormap)
            ecount = 0
            for element, values in zip(mesh.elements(), evalues):
                ## TODO MERGE: hideEmptyElements used to be a
                ## gfxwindow setting, but in 3D it was removed.
                ## Mesh filters now accomplish the same thing.
                if ( not gfxwindow.settings.hideEmptyElements ) or \
                       ( element.material() is not None ) :
                    (contours, elmin, elmax)  = contour.findContours(
                        mesh, element, self.where,
                        self.what, clevels,
                        self.nbins, 1)

                    # Before drawing anything, fill the element with the
                    # largest contour value below its lowest detected value.
                    vmin = min(values)
                    prevcntour = None
                    for cntour in contours:
                        if cntour.value > elmin:
                            if prevcntour:
                                device.set_fillColor(
                                    offset + prevcntour.value*factor)
                            else:
                                device.set_fillColor(0.0)
                            break
                        prevcntour = cntour
                    else:
                        # If all of the contours were below the
                        # element, fill the element with the color
                        # from the top of the colormap.
                        device.set_fillColor(1.0)
                    # Find element perimeter
                    edges = element.perimeter()
                    mcorners = [[0.0]]*element.ncorners()
                    corners = self.where.evaluate(mesh, edges, mcorners)
                    device.fill_polygon(primitives.pontify(
                            primitives.Polygon(corners)))

                    # Now fill contours
                    for cntour in contours:
                        # This is harder than it looks.
                        if len(cntour.loops) == 1:
                            device.set_fillColor(
                                offset + cntour.value*factor)
                            device.fill_polygon(cntour.loops[0])
                        elif len(cntour.loops) > 1:
                            device.set_fillColor(
                                offset + cntour.value*factor)
                            # Compound Polygon fill
                            device.fill_polygon(cntour.loops)
                ecount += 1
                prog.setFraction((1.0*ecount)/mesh.nelements())
                prog.setMessage("drawing %d/%d elements" %
                                (ecount, mesh.nelements()))
            #  self.draw_subcells(mesh, device)
            contour.clearCache()
                
            self.contour_min = minval
            self.contour_max = maxval
            self.contour_levels = clevels

        finally:
            self.lock.release()
            meshctxt.releaseCachedData()

    def draw_contourmap(self, gfxwindow, device):
        # If the drawing failed, then contour_max won't have been set
        # yet.
        self.lock.acquire()
        try:
            if self.contour_max is not None:
                if config.dimension() == 2:
                    aspect_ratio = gfxwindow.settings.aspectratio
                    height = self.contour_max - self.contour_min
                    width = height/aspect_ratio

                    # device.comment("Colorbar minimum: %s" % self.contour_min)
                    # device.comment("Colorbar maximum: %s" % self.contour_max)
                    device.set_colormap(self.colormap)

                    for low, high in utils.list_pairs(self.contour_levels):
                        # Subtract "contour_min" off the y coords, so that
                        # the drawn object will include the point (0,0) --
                        # otherwise, the canvas bounds are wrong.
                        r_low = low-self.contour_min
                        r_high = high-self.contour_min

                        rect_bndy = map( lambda x: primitives.Point(x[0],x[1]),
                                         [ (0.0, r_low), (0.0, r_high),
                                           (width, r_high), (width, r_low) ] )

                        rectangle = primitives.Polygon(rect_bndy)
                        # In the collapsed case, height can be zero.  This is
                        # not hugely informative, but should be handled without
                        # crashing.
                        if height>0.0:
                            device.set_fillColor(r_low/height)
                        else:
                            device.set_fillColor(0.0)

                        device.fill_polygon(rectangle)
                elif config.dimension() == 3:
                    if self.lookuptable:
                        device.draw_scalarbar(self.lookuptable)
        finally:
            self.lock.release()


    def newLayer(self):
        self.source = self.vtkSource()
        return gridlayers.ContourGridCanvasLayer(
            self.gfxwindow.oofcanvas, "FilledContour", self.source)

    def setParams(self):
        self.setSource()
        ## TODO OPT: Calling setData() here is inefficient.  Some
        ## parameters require the data to be recomputed, but some do
        ## not.
        self.setData(self.who().resolve(self.gfxwindow))
        if self.datarange is not None:
            self.setContourLevels()
        
    def setContourLevels(self):
        # This is the part of setParams that can't be done unless the
        # data has already been computed.  It's also repeated whenever
        # the data changes.
        if self.min_contour is automatic.automatic:
            self.contour_min = self.datarange[0]
        else:
            self.contour_min = self.min_contour
        if self.max_contour is automatic.automatic:
            self.contour_max = self.datarange[1]
        else:
            self.contour_max = self.max_contour

        self.canvaslayer.set_nContours(self.levels, self.contour_min,
                                       self.contour_max)
        lut = self.colormap.getVtkLookupTable(self.levels)
        mainthread.runBlock(self.canvaslayer.set_lookupTable,
                            (lut, self.contour_min, self.contour_max))

    def whoChanged(self):
        self.setData(self.who().resolve(self.gfxwindow))
        return True

    def meshDataChangedCB(self, meshctxt):
        # Called in response to the "mesh data changed" switchboard
        # signal, set up in MeshDisplayMethod.__init__().
        hoo = self.who()
        if hoo and meshctxt is hoo.resolve(self.gfxwindow):
            self.setData(meshctxt)
        ContourDisplay.meshDataChangedCB(self, meshctxt)

    def timeChanged(self):
        hoo = self.who()
        if hoo:
            self.setData(hoo.resolve(self.gfxwindow))
            if self.source:
                self.source.setTime(self.getTime(self.gfxwindow))

    def setData(self, meshctxt):
        # Called by whoChanged(), meshDataChangedCB(), and timeChanged().
        ## TODO OPT: This should check to make sure that something
        ## actually has changed before doing any calculations.
        meshctxt.precompute_all_subproblems()
        mesh = meshctxt.getObject()
        skel = mesh.skeleton
        nodepoints = []
        # TODO 3.1 OPT: Move this to C++. It copies a lot of data.
        # The difficulty will be that Output.evaluate is only defined
        # in python.  Does the whole Output mechanism have to be
        # translated?  Can we define the connections and data flow in
        # Python but have the data operations all be in C++?

        # Find the coordinates where the output should be computed.
        #
        # Instead of applying the filter every time we iterate over
        # the elements, it's sufficient to just use it here, and later
        # pass an empty list of coords to the elements that have been
        # filtered out.
        for element in mesh.elements():
            if self.filter.acceptable(element.get_skeleton_element(), skel):
                master = element.masterelement()
                el_mpos = [master.get_protonode(n).mastercoord()
                           for n in range(master.nnodes())]
            else:
                el_mpos = []
            nodepoints.append(el_mpos)
        meshctxt.restoreCachedData(self.getTime(meshctxt))
        try:
            # Calling Output.evaluate with domain=None here is ugly
            # but probably safe.  The domain is only used if necessary
            # to convert surface elements to bulk elements, but we're
            # passing in bulk elements, so the conversion won't be
            # necessary.
            values = [float(x) for x in
                      self.what.evaluate(mesh, None, mesh.elements(),
                                         nodepoints)]
        finally:
            meshctxt.releaseCachedData()
        ptdata = vtkutils.fillDataArray(values)
        self.canvaslayer.set_pointData(ptdata)
        # TODO OPT: This is inefficient.
        self.datarange = (min(values), max(values))
        self.setContourLevels()
        self.redraw()
                                       
registeredclass.Registration(
    'Filled Contour',
    display.DisplayMethod,
    FilledContourDisplay,
    ordering=3.1,
    layerordering=display.Planar(3),
    whoclasses = ('Mesh',),
    params =
    contourparams +
    [RegisteredParameter('colormap',
                         colormap.ColorMap,
                         colormap.ThermalMap(),
                         tip="color scheme")
     ],
    tip="Draw a filled contour plot of the given output data.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/filledcontour.xml')
    )

