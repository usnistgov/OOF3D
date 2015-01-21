# -*- python -*-
# $RCSfile: meshinfo.py,v $
# $Revision: 1.69.2.19 $
# $Author: langer $
# $Date: 2012/10/24 15:18:18 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.common import debug
from ooflib.common import toolbox
from ooflib.engine.IO import genericinfotoolbox

class MeshInfoMode(genericinfotoolbox.GenericInfoMode):
    pass

class MeshElementInfoMode(MeshInfoMode):
    targetName = "Element"
    def resolveQuery(self, meshctxt, indx):
        return meshctxt.getObject().getElement(indx)

class MeshNodeInfoMode(MeshInfoMode):
    targetName = "Node"
    def resolveQuery(self, meshctxt, indx):
        return meshctxt.getObject().getNode(indx)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class MeshInfoToolbox(genericinfotoolbox.GenericInfoToolbox):
    whoClassName = 'Mesh'
    def __init__(self, gfxwindow):
        genericinfotoolbox.GenericInfoToolbox.__init__(
            self, gfxwindow, 'Mesh_Info', self.makeInfoModes())

        # The mesh info toolbox has a special attribute, "meshlayer",
        # which refers to the display layer in which the referred-to
        # mesh is displayed.  The reason for needing the actual layer
        # is that the toolbox *display* needs to be able to draw the
        # selected objects (elements, nodes) at their displaced
        # position, possibly including any enhancements, and the mesh
        # display layer's source object has all of that data.  Mesh
        # display layers provide coordinate transformation routines
        # that convert undisplaced to displaced points, and vice
        # versa.
        self.meshlayer = None
        
    def makeInfoModes(self):
        return [MeshElementInfoMode(self), MeshNodeInfoMode(self)]

    def activate(self):
        genericinfotoolbox.GenericInfoToolbox.activate(self)
        self.meshlayer = self.gfxwindow().topwholayer("Mesh")

    def newLayers(self):        # sb "layers changed" callback
        genericinfotoolbox.GenericInfoToolbox.newLayers(self)
        self.meshlayer = self.gfxwindow().topwholayer("Mesh")

    tip = "Get information about a Mesh."
    discussion="""<para>
    Get information about a &mesh;, including &field; values, based on
    mouse input.
    </para>"""

toolbox.registerToolboxClass(MeshInfoToolbox, ordering=3.0)
