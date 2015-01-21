# -*- python -*-
# $RCSfile: skeletoninfo.py,v $
# $Revision: 1.40.10.19 $
# $Author: langer $
# $Date: 2014/11/05 16:54:41 $


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.engine import ooferror2
from ooflib.common import debug
from ooflib.common import toolbox
from ooflib.engine.IO import genericinfotoolbox

class SkeletonInfoMode(genericinfotoolbox.GenericInfoMode):
    pass

class SkeletonElementInfoMode(SkeletonInfoMode):
    targetName = "Element"
    def resolveQuery(self, skelctxt, indx):
        if indx < 0 or indx > skelctxt.getObject().nelements():
            raise ooferror2.ErrUserError("Element index out of range.")
        el = skelctxt.getObject().getElement(indx)
        # el.dumpFaceInfo(skelctxt.getObject());
        return el

class SkeletonNodeInfoMode(genericinfotoolbox.GenericInfoMode):
    targetName = "Node"
    def resolveQuery(self, skelctxt, indx):
        if indx < 0 or indx > skelctxt.getObject().nnodes():
            raise ooferror2.ErrUserError("Node index out of range.")
        return skelctxt.getObject().getNode(indx)

class SkeletonSegmentInfoMode(genericinfotoolbox.GenericInfoMode):
    targetName = "Segment"
    def resolveQuery(self, skelctxt, indx):
        seg = skelctxt.getObject().getSegmentByUid(indx)
        if not seg:
            raise ooferror2.ErrUserError("Invalid segment id")
        return seg

if config.dimension() == 3:
    class SkeletonFaceInfoMode(genericinfotoolbox.GenericInfoMode):
        targetName = "Face"
        def resolveQuery(self, skelctxt, indx):
            face = skelctxt.getObject().getFaceByUid(indx)
            if face is None:
                raise ooferror2.ErrUserError("Invalid face id")
            return face

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SkeletonInfoToolbox(genericinfotoolbox.GenericInfoToolbox):
    whoClassName = 'Skeleton'
    def __init__(self, gfxwindow):
        genericinfotoolbox.GenericInfoToolbox.__init__(
            self, gfxwindow, 'Skeleton_Info', self.makeInfoModes())

    def makeInfoModes(self):
        modes = [SkeletonElementInfoMode(self),
                 SkeletonNodeInfoMode(self),
                 SkeletonSegmentInfoMode(self)]
        if config.dimension() == 3:
            modes.append(SkeletonFaceInfoMode(self))
        return modes

    tip="Get information about Skeleton components."
    discussion="""<para>
    Get information about &skel; components, based on mouse input.
    </para>"""

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
    
toolbox.registerToolboxClass(SkeletonInfoToolbox, ordering=2.0)
