# -*- python -*-
# $RCSfile: animationtimes.py,v $
# $Revision: 1.4.4.3 $
# $Author: fyc $
# $Date: 2014/07/28 22:16:38 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.common import registeredclass
from ooflib.common.IO import animationtimes
from ooflib.common.IO import display
from ooflib.common.IO import placeholder
from ooflib.common.IO import whoville
from ooflib.common.IO import xmlmenudump
import ooflib.engine.mesh

class MeshTimes(animationtimes.AnimationTimes):
    # Use times stored in a given Mesh
    def __init__(self, mesh):
        self.mesh = mesh
    def times(self, start, finish, gfxwindow):
        meshctxt = ooflib.engine.mesh.meshes[self.mesh]
        starttime = meshctxt.getTime(start)
        endtime = meshctxt.getTime(finish)
        for t in meshctxt.cachedTimes():
            if starttime <= t <= endtime:
                yield t

registeredclass.Registration(
    "Times From One Mesh",
    animationtimes.AnimationTimes,
    MeshTimes,
    ordering=0,
    ## TODO 3.1: Restrict to meshes actually displayed in the gfx
    ## window!  This might be hard to do.
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip="The name of the Mesh.")],
    tip="Get frame times from stored data in a Mesh.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/meshtimes.xml'))

class AllMeshTimes(animationtimes.AnimationTimes):
    # Use times stored in all animated Meshes in the window
    def times(self, start, finish, gfxwindow):
        # Return a list of times between start and finish for all the
        # animatable layers in the graphics window.
        thymes = gfxwindow.findAnimationTimes()
        if thymes:
            if start is placeholder.earliest:
                if finish is placeholder.latest:
                    return thymes
                if finish is placeholder.earliest:
                    return [thymes[0]]
                return [t for t in thymes if t <= finish]
            if finish is placeholder.latest:
                if start is placeholder.latest:
                    return [thymes[-1]]
                return [t for t in thymes if t >= start]
        return [t for t in thymes if start <= t <= finish]
        
registeredclass.Registration(
    "Times From All Meshes",
    animationtimes.AnimationTimes,
    AllMeshTimes,
    ordering=1,
    tip="Get frame times from stored data in all Meshes.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/allmeshtimes.xml'))


