# -*- python -*-
# $RCSfile: splitquads.py,v $
# $Revision: 1.35.2.1 $
# $Author: langer $
# $Date: 2013/11/08 20:44:52 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.SWIG.common import config
assert config.dimension() == 2

from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import progress
from ooflib.common import registeredclass
from ooflib.common.IO import parameter
from ooflib.common.IO import reporter
from ooflib.common.IO import xmlmenudump
if config.dimension() == 2:
    from ooflib.engine import skeleton
elif config.dimension() == 3:
    from ooflib.engine import skeleton3d as skeleton
from ooflib.engine import skeletonelement
from ooflib.engine import skeletonmodifier

ProvisionalTriangle = skeletonelement.ProvisionalTriangle

# Utility routines for dividing a quad into two triangles.

#   3-----2
#   |\    |
#   | \   |
#   |  \  |
#   |   \ |
#   |    \|
#   0-----1

def slashLeft(skel, element):
    change = skeleton.ProvisionalChanges(skel)
    nodes = element.nodes
    parent = element.getParents()[:1]
    change.removeElements(element)
    change.insertElements(ProvisionalTriangle([nodes[0], nodes[1], nodes[3]],
                                              parents=parent),
                          ProvisionalTriangle([nodes[1], nodes[2], nodes[3]],
                                              parents=parent))
    return change

#   3-----2
#   |    /|
#   |   / |
#   |  /  |
#   | /   |
#   |/    |
#   0-----1

def slashRight(skel, element):
    change = skeleton.ProvisionalChanges(skel)
    nodes = element.nodes
    parent = element.getParents()[:1]
    change.removeElements(element)
    change.insertElements(ProvisionalTriangle([nodes[0], nodes[1], nodes[2]],
                                              parents=parent),
                          ProvisionalTriangle([nodes[0], nodes[2], nodes[3]],
                                              parents=parent))
    return change

############################

# The SplitQuadMethod registered class decides which ways of dividing
# a quadrilateral into two triangles should be considered by the
# SplitQuads SkeletonModifier.  The subclasses of SplitQuadMethod only
# need to provide a function getSplittings(skeleton, element) which
# returns a tuple containg zero or more of the functions slashLeft,
# slashRight.  SplitQuadMethod.__call__ evaluates the fitness of the
# proposed divisions and accepts the best one, if it improves the
# fitness of the mesh.

class SplitQuadMethod(registeredclass.RegisteredClass):
    registry = []

    def __call__(self, skel, element):
        changes = []
        slashfunctions = self.getSplittings(skel, element)
        for slashfunc in slashfunctions:
            changes.append(slashfunc(skel, element))
        return changes

    tip = "How to split quadrilateral elements?"
    discussion = """<para>
    Values of the <varname>split_how</varname> parameter used in
    <xref linkend='RegisteredClass-SplitQuads'/>.
    </para>"""

#############################
        
class GeographicQ2T(SplitQuadMethod):
    #  Looks for a quad in situation like this ...
    #                    ________
    #                   |        |
    #                   |   A    |           A, B    : pixel categories
    #             ______|________|_____      0,1,2,3 : node numbers
    #            /      3        2     \
    #           /   B   |   ?    |  A   \
    #          /________0________1_______\
    #                   \       /
    #                    \  B  /
    #                     \___/   
    #       
    # The heterogeneous element in the middle may(hopefully) have
    # pixel distribution like this ...
    #                ___________
    #               |BAAAAAAAAA|
    #               |BBBBBBAAAA|
    #               |BBBBBBBBBA|
    #                ----------
    #
    # GeographicQ2T does the extra work of examining its neighbors and
    # is clearly an exceptional case for more general approach,
    # TrialAndErrorQ2T. However, when users want to consider
    # "Quad2Tri" only for the above geographic situations(to eliminate
    # stairway boundaries), it's quite useful.

    # The element "signatures" used here are quadruples that indicate
    # whether the quad should be split to the left (from node 1 to
    # node 3) or to the right (from node 0 to node 2).  signature[i]
    # is 0 if neighbor i is different from neighbor i+1.  It's 1 if
    # they're the same, and None if neighbor i doesn't exist.  We can
    # try to split the element if the signature is (0,1,0,1) or
    # (1,0,1,0), with at most one None in any position.
        

    leftSignatures = ([0,1,0,1], [None,1,0,1], [0,None,0,1],
                      [0,1,None,1], [0,1,0,None])
    rightSignatures =  ([1,0,1,0], [None,0,1,0], [1,None,1,0],
                        [1,0,None,0], [1,0,1,None])
    
    def getSplittings(self, skel, element):
        neighbors = element.edgeNeighbors(skel)
        nbrcategories = [None]*4
        for i in range(4):
            if neighbors[i] is not None:
                nbrcategories[i] = neighbors[i].dominantPixel(skel.MS)

        signature = [None]*4
        for i in range(4):
            if nbrcategories[i] is not None:
                signature[i] = nbrcategories[i]==nbrcategories[(i+1)%4]

        if signature in GeographicQ2T.leftSignatures:
            return (slashLeft,)
        elif signature in GeographicQ2T.rightSignatures:
            return (slashRight,)
        else:
            return ()

registeredclass.Registration(
    'Geographic',
    SplitQuadMethod,
    GeographicQ2T,
    ordering=0,
    tip="Split a quad based on its neighbors.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/geographic.xml'))

##########################

class TrialAndErrorQ2T(SplitQuadMethod):
    def getSplittings(self, skel, element):
        return (slashLeft, slashRight)

registeredclass.Registration(
    "Trial and Error",
    SplitQuadMethod,
    TrialAndErrorQ2T,
    ordering=1,
    tip="Split a quad along both of its diagonals and choose the better one.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/trial_error.xml'))

    
##########################################################################

# SplitQuadCheckers have a __call__ method that returns 0 or 1,
# indicating whether or not the given element should be considered for
# splitting.  It will never be called for a non-quadrilateral element,
# so there's no need to check for nnodes==4.

####################################################################

class SplitQuads(skeletonmodifier.SkeletonModifier):
    def __init__(self, targets, split_how, criterion):
        self.targets = targets  # which quads to consider
        self.criterion = criterion  # acceptance criterion
        self.split_how = split_how  # how to split

    def apply(self, oldskeleton, context):
        prog = progress.getProgress("SplitQuads", progress.DEFINITE)
        try:
            skel = oldskeleton.properCopy(skeletonpath=context.path())
            elements = self.targets(skel, context, copy=1)
            done = 0  # No. of quads split.
            savedE = 0.0  # Saved energy from the merge
            nel = len(elements)
            for i in range(nel):        
                element = elements[i]
                if element.nnodes()==4 and element.active(skel):
                    changes = self.split_how(skel, element)
                    bestchange = self.criterion(changes, skel)
                    if bestchange is not None:
                        done += 1
                        savedE += bestchange.deltaE(skel,
                                                    self.criterion.alpha)
                        bestchange.accept(skel)                
                if prog.stopped():  
                    return None
                prog.setFraction(1.0*(i+1)/nel)
                prog.setMessage("%d/%d elements" % (i+1, nel))
            reporter.report("%d quadrilateral%s split." % (done, 's'*(done!=1)))
            skel.cleanUp()
            return skel
        finally:
            prog.finish()

registeredclass.Registration(
    'Split Quads',
    skeletonmodifier.SkeletonModifier,
    SplitQuads,
    ordering=2,
    params=[parameter.RegisteredParameter('targets',
                                          skeletonmodifier.SkelModTargets,
                                          tip = 'Which elements to modify.'),
            parameter.RegisteredParameter('criterion',
                                          skeletonmodifier.SkelModCriterion,
                                          tip='Acceptance criterion'),
            parameter.RegisteredParameter('split_how',
                                          SplitQuadMethod,
                                          GeographicQ2T(),
                                          tip = 'How to choose the split direction.')
    ],
    tip="Split quadrilateral elements into two triangles.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/splitquads.xml'))
