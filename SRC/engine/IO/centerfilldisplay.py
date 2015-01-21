# -*- python -*-
# $RCSfile: centerfilldisplay.py,v $
# $Revision: 1.10.2.3 $
# $Author: fyc $
# $Date: 2014/07/28 22:16:46 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Mesh for drawing elements with a uniform fill based on the
# evaluation of their "what" at the element center.  Although it
# doesn't draw contour lines, it's a subclass ContourDisplay in order
# to get access to the functionality of the contour map.

from ooflib.SWIG.common import config
from ooflib.common import debug
from ooflib.common import primitives
from ooflib.common import registeredclass
from ooflib.common import utils
from ooflib.common.IO import automatic
from ooflib.common.IO import colormap
from ooflib.common.IO import display
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump
from ooflib.engine.IO import contourdisplay
from ooflib.engine.IO import displaymethods
from ooflib.engine.IO import output
from ooflib.engine.IO import outputDefs
from types import *
import sys

MeshDisplayMethod = displaymethods.MeshDisplayMethod

## TODO MER: Implement for 3D

class CenterFillDisplay(contourdisplay.ZDisplay):
    # The "draw" function should set contour_max, contour_min, and
    # contour_levels, which will be used by the draw_contourmap function.
    def draw(self, gfxwindow, device):
        self.contour_max = None
        self.contour_min = None
        self.contour_levels = None
        
        meshctxt = self.who().resolve(gfxwindow)
        themesh = meshctxt.mesh()
        # device.comment("SolidFill")
        device.set_colormap(self.colormap)
        polygons = self.polygons(gfxwindow, meshctxt)
        elements = tuple(themesh.element_iterator())
        evaluationpoints = [[el.center()] for el in elements]
        values = map(float,
                     self.what.evaluate(themesh, elements, evaluationpoints))
        max_value = max(values)
        min_value = min(values)

        # Perform equivalent of "find_levels" computation -- at the
        # end of this, contour_levels, contour_max, and contour_min
        # must be set from self.min, self.max, and self.levels,
        # provided by the user.
        if type(self.levels)==TupleType:
            self.contour_levels = list(self.levels).sort()
        elif type(self.levels)==ListType: 
            self.contour_levels = self.levels[:].sort()


        # Respect min and max.
        if self.min == automatic.automatic:
            self.contour_min = float(min_value)
        else:
            self.contour_min = float(self.min)
            
        if self.max == automatic.automatic:
            self.contour_max = float(max_value)
        else:
            self.contour_max = float(self.max)
            
        # If levels is an int, then make that many evenly-spaced levels.
        if type(self.levels)==IntType:
            if self.levels == 1:
                self.contour_levels = [0.5*(self.contour_max + self.contour_min)]
            else:
                dz = (self.contour_max-self.contour_min)/(self.levels-1.0)
                self.contour_levels = [self.contour_min + i*dz for
                                       i in range(self.levels)]

        else:
            # Levels must have been automatic -- create a level
            # for each actual data level that is between the
            # established max and min.

            data_levels = set(values)
            self.contour_levels = [x for x in data_levels
                                   if x >= self.contour_min
                                   and x <= self.contour_max ]
            

        # print "CenterFillDisplay: "
        # print self.contour_min, self.contour_max, self.contour_levels
        # HACK: If the values are equal, put the actual value in
        # the middle of an arbitrary range.
        # if max_value==min_value:
        #    max_value += 1.0
        #     min_value -= 1.0

        # Actually draw things.
        for polygon, value in zip(polygons, values):
            if value is not None:
                if self.contour_max == self.contour_min:
                    cmap_value = 0.5 # arbitrary.
                else:
                     # Find the largest contour level not larger than v.
                     last_v = self.contour_levels[0]
                     for v in self.contour_levels:
                         if v > value:
                             break
                         last_v = v

                     cmap_value = (last_v-self.contour_min)/(self.contour_max-self.contour_min)

                device.set_fillColor(cmap_value)
                # device.set_fillColor((value-min_value)/(max_value-min_value))
                device.fill_polygon(primitives.Polygon(polygon))

    # These two functions should maybe belong somewhere higher up in
    # the hierarchy, because it's duplicated across several classes.
    # This display hierarchy needs more work.
    def get_contourmap_info(self):
        return (self.contour_min, self.contour_max, self.contour_levels)


    def draw_contourmap(self, gfxwindow, device):
        # If the drawing failed, then contour_max won't have been set
        # yet.
        self.lock.acquire()
        try:
            if self.contour_max is not None:
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
        finally:
            self.lock.release()             
        

# The ZDisplay class specializes this to the case of meshes.  This may
# complicate generalization to a hypothetical Skeleton version.
class MeshCenterFillDisplay(CenterFillDisplay,
                            contourdisplay.ZDisplay):
    def __init__(self, when, where, what, min, max, levels,
                 colormap=colormap.ThermalMap()):
        self.colormap = colormap
        contourdisplay.ZDisplay.__init__(self, when, what, where,
                                         min, max, levels)


        
if config.dimension() == 2:
    registeredclass.Registration(
        'Solid Fill',
        display.DisplayMethod,
        MeshCenterFillDisplay,
        ordering=2.0,
        layerordering=display.Planar,
        params=
        contourdisplay.zdisplayparams + [
            parameter.AutomaticValueSetParameter(
                'levels', automatic.automatic,
                tip="Number of levels or list of levels (in []), or automatic"),
            parameter.RegisteredParameter(
                'colormap', colormap.ColorMap,
                colormap.ThermalMap(), tip="Fill color.")
            ],
        whoclasses = ('Mesh',),
        tip="Quick and dirty contour plot.",
        discussion=xmlmenudump.loadFile(
            'DISCUSSIONS/engine/reg/centerfilldisplay.xml')
                                 )

# SkeletonCenterFillDisplay isn't useful unless there are Outputs that
# can be evaluated on a Skeleton.

##class SkeletonCenterFillDisplay(CenterFillDisplay, SkeletonDisplayMethod): 
##    def __init__(self, what, colormap=colormap.ThermalMap()):
##        self.what = what
##        self.colormap = colormap

##registeredclass.Registration('SolidFill',
##             display.DisplayMethod,
##             SkeletonCenterFillDisplay,
##             ordering=2.01,
##             params=[
##    ScalarOutputParameter('what', tip='Quantity to be plotted'),
##    RegisteredParameter('colormap', colormap.ColorMap,
##                         colormap.ThermalMap())],
##             whoclasses = ('Mesh')
##             )

######################
