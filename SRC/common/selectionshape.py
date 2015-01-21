# -*- python -*-
# $RCSfile: selectionshape.py,v $
# $Revision: 1.1.2.2 $
# $Author: langer $
# $Date: 2014/09/15 19:53:58 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.common import primitives
from ooflib.common import registeredclass
from ooflib.common.IO import parameter

class SelectionShape(registeredclass.RegisteredClass):
    registry = []

class BoxSelectionShape(SelectionShape):
    def __init__(self, point0, point1):
        self.point0 = point0
        self.point1 = point1
    def scaled(self, factors):   # factors is a Point
        return BoxSelectionShape(self.point0.scale(factors),
                                 self.point1.scale(factors))

registeredclass.Registration(
    'Box',
    SelectionShape,
    BoxSelectionShape,
    ordering=0,
    params=[primitives.PointParameter(
            "point0", tip="One corner of the box."),
            primitives.PointParameter(
            "point1", tip="The diagonally opposite corner of the box.")
            ],
    tip="Select a rectangular region defined by diagonally opposing corners.")

class CircleSelectionShape(SelectionShape):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
    def scaled(self, factors):
        avgscale = factors.x + factors.y
        if config.dimension() == 3:
            avgscale += factors.z
        avgscale = avgscale/config.dimension()
        return CircleSelectionShape(self.center.scale(factors),
                                    self.radius*avgscale)

registeredclass.Registration(
    "Circle",
    SelectionShape,
    CircleSelectionShape,
    ordering=1,
    params=[primitives.PointParameter("center",
                                      tip="The center of the circle."),
            parameter.FloatParameter("radius", 0.0)],
    tip="Select a circular or spherical region.")

class EllipseSelectionShape(SelectionShape):
    def __init__(self, point0, point1):
        self.point0 = point0
        self.point1 = point1
    def scaled(self, factors):
        return EllipseSelectionShape(self.point0.scale(factors),
                                     self.point1.scale(factors))

registeredclass.Registration(
    "Ellipse",
    SelectionShape,
    EllipseSelectionShape,
    ordering=2,
    params=[primitives.PointParameter(
            "point0", tip="One corner of the bounding box."),
            primitives.PointParameter(
            "point1",
            tip="The diagonally opposite corner of the bounding box.")],
    tip="Select an elliptical region.")
