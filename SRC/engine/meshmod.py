# -*- python -*-
# $RCSfile: meshmod.py,v $
# $Revision: 1.19.2.1 $
# $Author: langer $
# $Date: 2013/11/08 20:44:33 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Mesh modification operations.  There shouldn't be too many of these,
# since most modifications are performed on a Skeleton instead.

from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import registeredclass
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump
from ooflib.engine import materialmanager
from ooflib.engine import meshstatus
from ooflib.engine import skeletoncontext
from ooflib.engine.IO import materialmenu
from ooflib.engine.IO import materialparameter
from ooflib.engine.IO import skeletongroupparams

##############

class MeshModification(registeredclass.RegisteredClass):
    registry = []
    # Subclasses must define an "apply" function.
    # Also, if a Subclass needs a different type of progress bar,
    # it should be overridden.
    def get_progressbar_type(self):
        return "continuous"
    # setStatus and signal are called after the modifier is applied.
    # They should set the mesh status and send the appropriate
    # switchboard signals.
    def setStatus(self, meshcontext):
        pass
    def signal(self, meshcontext):
        pass

    tip = "Tools to modify a Mesh."
    discussion = """<para>
    <classname>MeshModification</classname> objects modify &meshes;.
    They are used as the <varname>modifier</varname> argument of the
    <xref linkend='MenuItem-OOF.Mesh.Modify'/> command.
    </para>"""


class RebuildMesh(MeshModification):
    def apply(self, meshcontext):
        meshcontext.rebuildMesh()
    def signal(self, meshcontext):
        switchboard.notify("mesh changed", meshcontext)
        switchboard.notify("mesh boundaries changed", meshcontext.getObject())
        switchboard.notify("redraw")
    def setStatus(self, meshcontext):
        meshcontext.setStatus(meshstatus.Unsolved("Rebuilt"))

registeredclass.Registration(
    'Rebuild',
    MeshModification,
    RebuildMesh,
    ordering=1,
    tip="Rebuild a Mesh after its Skeleton has changed.",
    discussion=xmlmenudump.loadFile("DISCUSSIONS/engine/reg/rebuildmesh.xml")
    )
