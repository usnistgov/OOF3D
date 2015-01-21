# -*- python -*-
# $RCSfile: rationalwide.py,v $
# $Revision: 1.8.12.2 $
# $Author: langer $
# $Date: 2014/08/20 02:21:23 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
assert config.dimension() == 2

from ooflib.common import registeredclass
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump
from ooflib.engine import rationalize
from ooflib.engine import skeleton
from ooflib.engine import skeletonelement
import math

ProvisionalTriangle = skeletonelement.ProvisionalTriangle

class QuadSplit(rationalize.Rationalizer):
    #
    #              D____C
    #              /    |   Find the biggest angle and if it is bigger than
    #             /     |   the specified threshold, split the quad
    #            /      |
    #           /_______|             D____C
    #          A        B   ====>     /\   |
    #                                /  \  |
    #                               /    \ |
    #                              /______\|
    #                             A        B
    #

    def __init__(self, angle):
        self.angle = angle
        self.threshold = math.cos(angle*math.pi/180.0)

    def findAndFix(self, skel, element):
        if element.nnodes() == 4:  # Applies only for quads
            which = element.getBiggestAngle()
            if element.cosCornerAngle(which) <= self.threshold:
                # Returns a list of ProvisionalChange objects
                return self.fix(skel, element, which)
        return []

    def fixAll(self, skel, element):
        if element.nnodes() == 4:
            which = element.getBiggestAngle()
            return self.fix(skel, element, which)
        return []

    def fix(self, skel, element, which):
        nodes = element.nodes
        parents = element.getParents()
        if which%2 == 0:
            triangles = (ProvisionalTriangle([nodes[0], nodes[1], nodes[2]],
                                             parents=parents),
                         ProvisionalTriangle([nodes[0], nodes[2], nodes[3]],
                                             parents=parents))
        else:
            triangles = (ProvisionalTriangle([nodes[1], nodes[2], nodes[3]],
                                             parents=parents),
                         ProvisionalTriangle([nodes[0], nodes[1], nodes[3]],
                                             parents=parents))
        change = skeleton.ProvisionalChanges(skel)
        change.removeElements(element)
        change.insertElements(*triangles)
        return [change]
    
registeredclass.Registration(
    'Split Wide Quads',
    rationalize.Rationalizer,
    QuadSplit,
    gerund = 'splitting wide quads',
    ordering=1,
    params=[
    parameter.FloatRangeParameter('angle', (90.0, 180.0, 1.0), value = 150.0,
                                  tip = 'Maximum acceptable interior angle')
    ],
    tip = 'Split quadrilaterals with large interior angles.',
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/ration_wide.xml'))
