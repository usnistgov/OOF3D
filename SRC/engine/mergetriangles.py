# -*- python -*-
# $RCSfile: mergetriangles.py,v $
# $Revision: 1.28.2.2 $
# $Author: langer $
# $Date: 2013/11/08 20:44:31 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modifed
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.SWIG.common import config
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
from ooflib.engine import skeletonmodifier
from ooflib.engine import skeletonelement
from ooflib.engine.IO import skeletonmenu
import random

#          /|\             /\
#         / | \           /  \
#        /t1|  \  ===>   / q  \
#        \  |t2/         \    /
#         \ | /           \  /
#          \|/             \/
#
#       If the dominant pixels of t1 and t2 are identical
#       and the merge with its sister t2 reduces
#       element energy(average), merging t1 and t2 into a single quad
#       is definately beneficial.

ProvisionalQuad = skeletonelement.ProvisionalQuad

#########################################################################

class MergeTriangles(skeletonmodifier.SkeletonModifier):
    def __init__(self, targets, criterion):
        self.targets = targets
        self.criterion = criterion

    def apply(self, oldskeleton, context):
        prog = progress.getProgress("Merge", progress.DEFINITE)
        try:
            skel = oldskeleton.properCopy(skeletonpath=context.path())
            elements = self.targets(skel, context, copy=1)
            random.shuffle(elements)
            # A dict. keyed by element to prevent considering merging
            # element which does not exist any more.
            processed = {}  # Merged triangles
            done = 0  # No. of triangles merged.
            savedE = 0.0  # Saved energy from the merge
            nel = len(elements)
            for i in range(nel):
                element = elements[i]
                if (element not in processed and 
                    element.nnodes()==3 and element.active(skel)):
                    changes = self.mergeTriangles(element, skel, processed)
                    bestchange = self.criterion(changes, skel)
                    if bestchange is not None:
                        done += 2
                        savedE += bestchange.deltaE(skel,
                                                    self.criterion.alpha)
                        bestchange.accept(skel)
                        # Now that these two are merged, we need to indicate
                        # that these are not to be looked at again.
                        for e in bestchange.removed:
                            processed[e] = 1
                if prog.stopped():
                    return None
                else:
                    prog.setFraction(1.0*(i+1)/nel)
                    prog.setMessage("%d/%d" % (i+1, nel))

            reporter.report("Merged %d triangles, saving energy %f" %\
                            (done, savedE))
            skel.cleanUp()
            return skel
        finally:
            prog.finish()

#            node1
#              /|\ sister            /\
#      element/ | \                 /  \
#            /  |  \nodeA   ===>   / Q  \
#      nodeB \  |  /               \    /
#             \ | /                 \  /
#              \|/                   \/
#              node0
    def mergeTriangles(self, element, skel, processed):
        saved = [None]*3    # saved energy through the merge
        newels = [None]*3   # new provisional elements from the merge
        sisters = [None]*3  # sisters

        changes = []
        for i in range(3):
            node0 = element.nodes[i]
            node1 = element.nodes[(i+1)%3]
            sister = element.getSister(skel, node0, node1)
            # These are not welcome here.
            if (sister is None or sister.nnodes()!=3 or
                sister in processed or
                element.dominantPixel(skel.MS)!=sister.dominantPixel(skel.MS)):
                continue
            j = sister.nodes.index(node0)
            nodeA = sister.nodes[(j+1)%3]
            nodeB = element.nodes[(i+2)%3]
            nlist = [node0, nodeA, node1, nodeB]
            parents = element.getParents() + sister.getParents()
            change = skeleton.ProvisionalChanges(skel)
            change.removeElements(element, sister)
            change.insertElements(ProvisionalQuad(nlist, parents=parents))
            changes.append(change)
        return changes

###################################################
    
registeredclass.Registration(
    'Merge Triangles',
    skeletonmodifier.SkeletonModifier,
    MergeTriangles, ordering = 5,
    params=[parameter.RegisteredParameter('targets',
                                          skeletonmodifier.SkelModTargets,
                                          tip = 'Which elements to modify.'),
            parameter.RegisteredParameter('criterion',
                                          skeletonmodifier.SkelModCriterion,
                                          tip='Acceptance criterion.')
    ],
    tip="Merge neighboring homogeneous triangles to form quadrilaterals.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/merge.xml')
    )
