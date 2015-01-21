# -*- python -*-
# $RCSfile: meshcstoolbox.py,v $
# $Revision: 1.17.18.1 $
# $Author: langer $
# $Date: 2013/11/08 20:44:59 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# A toolbox for selecting cross-section paths in the graphics window.
# Should be able to create and remove paths, name them, and take a
# path and output data for the topmost contourable layer of the
# graphics window.

from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common import timestamp
from ooflib.common import debug
from ooflib.common import toolbox
from ooflib.common.IO import automatic
from ooflib.common.IO import oofmenu
from ooflib.common.IO import whoville
from ooflib.engine import meshcrosssection
from ooflib.engine.IO import meshmenu
from ooflib.engine import mesh

# The toolbox maintains a notion of a current mesh.  The toolbox can
# add a path to a mesh, delete a path from a mesh, and actually draw
# the current topmost contourable output on the path.  The topmost
# contourable output implies a particular mesh.  Could also maintain a
# notion of a current path.

class CrossSectionToolbox(toolbox.Toolbox):
    def __init__(self, gfxwindow):
        toolbox.Toolbox.__init__(self, "Mesh_Cross_Section", gfxwindow)
        self.current_mesh = None    # Topmost mesh.
        self.current_output = None  # Topmost contourable layer.
        self.whoset = ('Mesh',)     # Cross-sections live on meshes.

        self.sb_callbacks = [
            switchboard.requestCallback( (self.gfxwindow(),
                                          "layers changed"),
                                         self.newLayers),
            switchboard.requestCallback( (self.gfxwindow(),
                                          "new contourmap layer"),
                                         self.newLayers)
            ]

    def selectCS(self, csname):
        meshobj = self.current_mesh
        menuitem = meshmenu.csmenu.Select
        menuitem.callWithDefaults(mesh=meshobj.path(), cross_section=csname)

    def deselectCS(self):
        meshobj = self.current_mesh
        menuitem = meshmenu.csmenu.Deselect
        menuitem.callWithDefaults(mesh=meshobj.path())

    def makeMenu(self, menu):
        menu.setOption('no_doc',1)

    # Called when the GUI counterpart becomes current, or when the
    # layers change.
    def activate(self):
        # Find the topmost contourable layer. 
        layer = self.gfxwindow().topcontourable()
        if layer:
            self.current_layer = layer
            self.current_mesh = layer.who().resolve(self.gfxwindow())
        else:
            self.current_layer = None
            self.current_mesh = apply(self.gfxwindow().topwho, self.whoset)

    # Given the indicated start and end point, make a CS and add it
    # to the mesh.  Eventually there will be more of these.  Call
    # is triggered by the MouseUp in the graphical toolbox.
    def makeCS(self, start, end):
        cs = meshcrosssection.StraightCrossSection(
            start=start, end=end)
        namepar = meshmenu.csnameparam
        meshpar = meshmenu.csmeshparam
        if self.current_mesh:
            meshpar.set(mesh.meshes.getPath(self.current_mesh) )
            namepar.set(automatic.automatic)
            meshmenu.csmenu.New.callWithDefaults(
                cross_section=cs)
        
    def newLayers(self):
        self.activate()

    def stop_callbacks(self):
        for s in self.sb_callbacks:
            switchboard.removeCallback(s)
        self.sb_callbacks = []
    tip="You couldn't hit the side of barn."
    discussion="""<para>
    This toolbox doesn't have any of its own menu items, so this text
    that you're reading right now shouldn't appear in the
    documentation.  If it does, please file a bug report.
    </para>"""

toolbox.registerToolboxClass(CrossSectionToolbox, 3.0)


