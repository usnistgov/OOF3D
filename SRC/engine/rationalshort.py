# -*- python -*-
# $RCSfile: rationalshort.py,v $
# $Revision: 1.12.12.2 $
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

from ooflib.common import debug
from ooflib.common import registeredclass
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump
from ooflib.engine import rationalize

class RemoveShortSide(rationalize.Rationalizer):
    #
    #       C  _________
    #         |        / B   If a segment C-D is too short,
    #       D  \      /      it's better to merge C&D to form a triangle.
    #           \    /
    #            \  /
    #             \/      ===>     C ________
    #             A                  \      / B
    #                                 \    /
    #                                  \  /
    #                                   \/
    #                                    A
    #
    #
    #    A  __________________ D      
    #      |                  |  ==>   (A,B)________________ (C,D)
    #    B |__________________|C              collapse a quad

    def __init__(self, ratio):
        self.ratio = ratio

    def findAndFix(self, skel, element):
        changes = []
        if element.nnodes() == 4:       # only applies to quads
            edgeLengths = [(length, indx) for indx, length in
                            enumerate(element.getEdgeLengthsList())]
            edgeLengths.sort()
            # See if the shortest edge is much shorter than the rest
            if edgeLengths[1][0] >= self.ratio*edgeLengths[0][0]:
                which = edgeLengths[0][1]
                # Returns a list of ProvisionalChange objects
                changes = self.fix(skel, element, which)
            # See if there are two short edges opposite each other
            if edgeLengths[2][0] >= self.ratio*edgeLengths[1][0]:
                indxdiff = edgeLengths[0][1] - edgeLengths[1][1]
                if indxdiff == 2 or indxdiff == -2:
                    changes.extend(self.fix2(skel, element, edgeLengths[0][1]))
        return changes

    def fixAll(self, skel, element):
        if element.nnodes() == 4:
            which = element.getShortestEdge()
            edgeLengths = [(length, indx) for indx, length in
                            enumerate(element.getEdgeLengthsList())]
            edgeLengths.sort()
            changes = self.fix(skel, element, edgeLengths[0][1])
            indxdiff = edgeLengths[0][1] - edgeLengths[1][1]
            if indxdiff == 2 or indxdiff == -2:
                changes.extend(self.fix2(skel, element, edgeLengths[0][1]))
            return changes
        return []

    def fix(self, skel, element, which):
        node0 = element.nodes[which]
        node1 = element.nodes[(which+1)%4]
        return [skel.mergeNodePairs((node0, node1)),
                skel.mergeNodePairs((node1, node0))]

    def fix2(self, skel, element, which):
        nodes = [element.nodes[(which+i)%4] for i in range(4)]
        return [skel.mergeNodePairs((nodes[0], nodes[1]), (nodes[2], nodes[3])),
            skel.mergeNodePairs((nodes[1], nodes[0]), (nodes[2], nodes[3])),
            skel.mergeNodePairs((nodes[1], nodes[0]), (nodes[3], nodes[2])),
            skel.mergeNodePairs((nodes[0], nodes[1]), (nodes[3], nodes[2]))]

registeredclass.Registration(
    'Remove Short Sides',
    rationalize.Rationalizer,
    RemoveShortSide,
    gerund = 'removing short sides',
    ordering=0,
    params=[
    parameter.FloatParameter('ratio', value = 5.0,
                             tip = 'Maximum acceptable ratio of the lengths of the second shortest and the shortest sides.')
    ],
    tip = "Eliminate the shortest side of a quadrilateral.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/ration_short.xml'))
