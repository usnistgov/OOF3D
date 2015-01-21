# -*- python -*-
# $RCSfile: pixelselectionmethod.py,v $
# $Revision: 1.30.18.13 $
# $Author: langer $
# $Date: 2014/11/05 16:54:16 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 


# Each way of selecting pixels is described by a SelectionMethod
# subclass.  SelectionMethod is a RegisteredClass.  The
# PixelSelectToolbox builds an OOFMenu with a menu item for each
# subclass.  The arguments to the menu item are the parameters for the
# SelectionMethod plus a list of Points.  Invoking the menu item
# creates an instance of the method and calls its select() function on
# the list of points.

# Each Registration for a SelectionMethod subclass needs to have an
# 'events' attribute, which consists of a list of strings indicating
# which mouse events it requires.  Allowed events are 'down', 'move',
# and 'up'.

# If a SelectionMethod requires a rubberband to be drawn in graphics
# mode, its Registration must have a getRubberBand function added to
# it when graphics code is loaded.  See
# common/IO/GUI/pixelselecttoolboxGUI.py for examples.

from ooflib.SWIG.common import config
if config.dimension() == 2:
    from ooflib.SWIG.common import brushstyle
from ooflib.SWIG.common import pixelselectioncourier
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common.IO import vtkutils
from ooflib.common import debug
from ooflib.common import primitives
from ooflib.common import registeredclass
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump
import math

###################

# Base class for pixel selection methods

class SelectionMethod(registeredclass.RegisteredClass):
    registry = []
    
    def select(self, immidge, pointlist, selector):
        # immidge is the Who for the OOFImage or Microstructure on
        # which to operate.  pointlist is the list of points received
        # from the mouse.  selector is the function to call with the
        # list of selected pixels.
        pass

class PixelSelectionRegistration(registeredclass.Registration):
    def __init__(self, name, subclass, ordering, params=[], secret=0, **kwargs):
        registeredclass.Registration.__init__(self,
                                              name=name,
                                              registeredclass=SelectionMethod,
                                              subclass=subclass,
                                              ordering=ordering,
                                              params=params,
                                              secret=secret,
                                              **kwargs)

###################

# Select a single pixel.  Although the select function is written to
# accept a list of points, it only receives one point because the
# registration only requests 'up'.

class PointSelector(SelectionMethod):
    def select(self, immidge, gfxwindow, pointlist, view, selector):
        # 'selector' is a PixelSelectionContext method, 'select',
        # 'unselect', 'toggle', etc.
        ms = immidge.getMicrostructure()
        if config.dimension() == 2:
            mpt = pointlist[0]
            selector(pixelselectioncourier.PointSelection(ms, mpt))
        else:                   # 3D
            ## This needs to use findClickedCellCenter instead of
            ## findClickedPosition.  findClickedPosition will return a
            ## coord on the boundary of a voxel, which might be
            ## ambiguous in PointSelection if not all of the voxels in
            ## the image are displayed.  If the point in the center of
            ## the voxel is returned instead, it will always be
            ## resolved correctly.
            mpt = gfxwindow.findClickedCellCenter(immidge, pointlist[0], view)
            if mpt is not None:
                selector(pixelselectioncourier.PointSelection(ms, mpt))
            else:
                selector(pixelselectioncourier.PointlessSelection(ms));

PixelSelectionRegistration(
    'Point',
    PointSelector,
    ordering=0.1,
    events=['up'],
    whoclasses=['Microstructure', 'Image'],
    tip="Select a single pixel.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/reg/pointselect.xml')
    )

######################

def sign(x):
    if x>=0:
        return 1
    else:
        return -1

if config.dimension() == 2:

    BrushSelection = pixelselectioncourier.BrushSelection
    class BrushSelector(SelectionMethod):
        def __init__(self, style):
            self.style = style

        def select(self, immidge, pointlist, selector):
            self.ms = immidge.getMicrostructure()
            points = []
            prev = pointlist[0]
            prevIPoint = self.ms.pixelFromPoint(prev)
            points.append(prev)
            for current in pointlist[1:]:
                currentIPoint = self.ms.pixelFromPoint(current)
                if prevIPoint == currentIPoint:
                    continue
                else:
                    if self.contiguous(prev, current):
                        points.append(current)
                    else:
                        points += self.fillTheGap(prev, current)
                    prev = current
                    prevIPoint = currentIPoint
            selector(BrushSelection(self.ms, self.style,
                                    filter(self.okPoints,points)))

        def contiguous(self, prev, next):
            # To simplify things, two points are assumed to be contiguous,
            # if their iPoint counterparts are contiguous.        
            iprev = self.ms.pixelFromPoint(prev)
            inext = self.ms.pixelFromPoint(next)
            dx = abs(inext.x - iprev.x)
            dy = abs(inext.y - iprev.y)
            return (dx <= 1) and (dy <= 1)

        def fillTheGap(self, prev, next):
            dx = next.x - prev.x
            dy = next.y - prev.y
            points = []
            if abs(dx) >= abs(dy):  # Sample along the x-axis
                slope = (next.y - prev.y)/(next.x - prev.x)
                h = sign(dx)*self.ms.sizeOfPixels()[0]  # Sampling increment
                i = 1
                x = prev.x+i*h
                while sign(next.x - x)==sign(dx):
                    y = slope*(x - prev.x) + prev.y
                    points.append(primitives.Point(x,y))
                    i += 1
                    x = prev.x+i*h
                points.append(next)
            else:
                slope = (next.x - prev.x)/(next.y - prev.y)
                h = sign(dy)*self.ms.sizeOfPixels()[1]
                i = 1
                y = prev.y+i*h
                while sign(next.y - y)==sign(dy):
                    x = slope*(y - prev.y) + prev.x
                    points.append(primitives.Point(x,y))
                    i += 1
                    y = prev.y+i*h
                points.append(next)
            return points

        def okPoints(self, p):
            if (p.x >= 0.0 and p.x <= self.ms.size().x) and \
            (p.y >= 0.0 and p.y <= self.ms.size().y):
                return 1
            return 0

    brushSelectorRegistration = PixelSelectionRegistration(
        'Brush',
        BrushSelector,
        ordering=0.101,
        events=['down', 'move', 'up'],
        params=[parameter.RegisteredParameter('style', brushstyle.BrushStyle,
                                              tip=parameter.emptyTipString)],
        whoclasses=['Microstructure', 'Image'],
        tip="Drag to select multiple pixels with a brush.",
        discussion=xmlmenudump.loadFile(
            'DISCUSSIONS/common/reg/brushselect.xml')
        )

    ####################

    BoxSelection = pixelselectioncourier.BoxSelection
    class RectangleSelector(SelectionMethod):
        def select(self, immidge, pointlist, selector):
            # Select pixels whose centers are in the rectangle defined by
            # the points. 
            ms = immidge.getMicrostructure()
            isize = ms.sizeInPixels()
            psize = primitives.Point(*ms.sizeOfPixels())
            selector(BoxSelection(ms, pointlist[0], pointlist[-1]))

    rectangleSelectorRegistration = PixelSelectionRegistration(
        'Rectangle',
        RectangleSelector,
        ordering=0.2,
        events=['down', 'up'],
        whoclasses=['Microstructure', 'Image'],
        tip="Drag to select a rectangular region.",
        discussion=xmlmenudump.loadFile('DISCUSSIONS/common/reg/rectangle.xml')
        )

    CircleSelection = pixelselectioncourier.CircleSelection
    class CircleSelector(SelectionMethod):
        def select(self, immidge, pointlist, selector):
            ms = immidge.getMicrostructure()
            isize = ms.sizeInPixels()
            psize = primitives.Point(*ms.sizeOfPixels())
            center = pointlist[0]
            radius = pointlist[-1] - center
            rr = radius.x*radius.x + radius.y*radius.y
            r = math.sqrt(rr)
            selector(CircleSelection(ms, center, r)) #, ll, ur


    circleSelectorRegistration = PixelSelectionRegistration(
        'Circle',
        CircleSelector,
        ordering=0.3,
        events=['down', 'up'],
        whoclasses=['Microstructure', 'Image'],
        tip="Drag to select a circular region.",
        discussion=xmlmenudump.loadFile(
            'DISCUSSIONS/common/reg/circleselect.xml')
        )

    EllipseSelection = pixelselectioncourier.EllipseSelection
    class EllipseSelector(SelectionMethod):
        def select(self, immidge, pointlist, selector):
            ms = immidge.getMicrostructure()
            isize = ms.sizeInPixels()
            psize = primitives.Point(*ms.sizeOfPixels())
            ll = primitives.Point(min(pointlist[0].x, pointlist[-1].x),
                                  min(pointlist[0].y, pointlist[-1].y))
            ur = primitives.Point(max(pointlist[0].x, pointlist[-1].x),
                                  max(pointlist[0].y, pointlist[-1].y))
            selector(EllipseSelection(ms, ll, ur))

    ellipseSelectorRegistration = PixelSelectionRegistration(
        'Ellipse',
        EllipseSelector,
        ordering=0.4,
        events=['down', 'up'],
        whoclasses=['Microstructure', 'Image'],
        tip="Drag to select an elliptical region.",
        discussion=xmlmenudump.loadFile(
            'DISCUSSIONS/common/reg/ellipseselect.xml')
        )


## TODO MAYBE: Add TriangleSelector, or maybe a PolygonSelector.  This
## is tricky because the GenericSelectToolboxGUI isn't set up for this
## case.  GenericSelectToolboxGUI expects a simple mouse down, mouse
## move, mouse up sequence.  Selecting a triangle is best down with
## three clicks, which doesn't fit the sequence.  Fixing this will
## involve giving the SelectionMethod a more active role in the
## process.  It will have to tell PixelSelectToolboxGUI.finish_up that
## it isn't really finished until after the third mouse up, and fix up
## the rubber bands.
