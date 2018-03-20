# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 


# Each way of selecting pixels is described by a VoxelSelectionMethod
# subclass.  VoxelSelectionMethod is a RegisteredClass.  Instances of
# the subclasses are used as arguments to the Select command in the
# VoxelSelection menu, defined in pixelselectionmenu.py.  Selection
# methods that can use mouse input can have GUIs assigned to them.
# See SelectionMethodGUI and selectionGUIfor in genericselectGUI.py.

# See NOTES/selection_machinery.txt

from ooflib.SWIG.common import config
if config.dimension() == 2:
    from ooflib.SWIG.common import brushstyle
from ooflib.SWIG.common import coord
from ooflib.SWIG.common import geometry
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import pixelselectioncourier
from ooflib.SWIG.common.IO import vtkutils
from ooflib.common import debug
from ooflib.common import primitives
from ooflib.common import registeredclass
from ooflib.common.IO import parameter
from ooflib.common.IO import pointparameter
from ooflib.common.IO import xmlmenudump
import math

###################

# Base class for generic methods for selecting objects in the graphics
# window.  Subclasses should have registries.  Registrations should
# have a 'whoclasses' member that is a list or tuple of the names of the
# WhoClasses that the selector operates on.

class GenericSelectionMethod(registeredclass.RegisteredClass):
    def getSource(self, gfxwindow):
        return gfxwindow.topwho(*self.registration.whoclasses)
    def getSourceName(self, gfxwindow):
        src = self.getSource(gfxwindow)
        if src is not None:
            return src.path()

#################

# Base class for voxel selection methods

class VoxelSelectionMethod(GenericSelectionMethod):
    registry = []
    
    # def select(self, immidge, pointlist, selector):
    #     # immidge is the Who for the OOFImage or Microstructure on
    #     # which to operate.  pointlist is the list of points received
    #     # from the mouse.  selector is the function to call with the
    #     # list of selected pixels.
    #     pass

    # Source is a Microstructure or Image.  Selection is the
    # Microstructure's PixelSelection object. Operator is a
    # PixelSelectionOperator, from pixelselectionmod.py.  Called from
    # pixelselectionmenu.select(), which is the callback for the menu
    # item OOF.VOxelSelection.Select.
    def select(self, source, selection, operator):
        raise ooferror.ErrPyProgrammingError(
            "'select' isn't defined for " + self.registration.name)

    
## TODO: Rename to VoxelSelectionRegistration

class PixelSelectionRegistration(registeredclass.Registration):
    def __init__(self, name, subclass, ordering, params=[], secret=0, **kwargs):
        registeredclass.Registration.__init__(
            self,
            name=name,
            registeredclass=VoxelSelectionMethod,
            subclass=subclass,
            ordering=ordering,
            params=params,
            secret=secret,
            **kwargs)

###################

# Select a single pixel.  Although the select function is written to
# accept a list of points, it only receives one point because the
# registration only requests 'up'.

class PointSelector(VoxelSelectionMethod):
    def __init__(self, point):
        self.point = point
    def select(self, source, selection, operator):
        ms = source.getMicrostructure()
        operator.operate(selection,
                         pixelselectioncourier.PointSelection(ms, self.point))

PixelSelectionRegistration(
    'Point',
    PointSelector,
    ordering=0.1,
    whoclasses=['Microstructure', 'Image'],
    params=[pointparameter.PointParameter('point')],
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
## the rubber bands.  NEW OOF3D MOUSEHANDLER AND TOOLBOX ARCHITECTURE
## CAN DO THIS, PROBABLY.


class RectangularPrismSelector(VoxelSelectionMethod):
    def __init__(self, corner0, corner1):
        self.corner0 = corner0
        self.corner1 = corner1
    def select(self, source, selection, operator):
        # operator is a PixelSelectionOperator from pixelselectionmod.py
        ms = source.getMicrostructure()
        operator.operate(
            selection,
            pixelselectioncourier.BoxSelection(
                ms,
                geometry.CRectangularPrism(self.corner0, self.corner1)))

PixelSelectionRegistration(
    'Box',
    RectangularPrismSelector,
    ordering=0.2,
    params=[pointparameter.PointParameter('corner0'),
            pointparameter.PointParameter('corner1')],
    whoclasses=['Microstructure', 'Image'],
    tip="Click to select a box-shaped region."
    )


