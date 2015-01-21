# -*- python -*-
# $RCSfile: meshcsdisplay.py,v $
# $Revision: 1.24.10.3 $
# $Author: langer $
# $Date: 2013/11/08 20:44:59 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.SWIG.common import ooferror
from ooflib.common import color
from ooflib.common import primitives
from ooflib.common import registeredclass
from ooflib.common.IO import automatic
from ooflib.common.IO import display
from ooflib.common.IO import ghostgfxwindow
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import placeholder
from ooflib.common.IO import xmlmenudump
from ooflib.engine.IO import meshcsparams
import types

# Layer for showing the mesh cross-sections.
class MeshCrossSectionDisplay(display.DisplayMethod):
    def __init__(self, cross_sections, color, linewidth):
        display.DisplayMethod.__init__(self)
        self.cross_sections = cross_sections
        self.color = color
        self.linewidth = linewidth
        
    def draw(self, gfxwindow, device):
        mesh = self.who().resolve(gfxwindow)
        device.set_lineColor(self.color)
        device.set_lineWidth(self.linewidth)

        if self.cross_sections == placeholder.selection:
            cstoolbox = gfxwindow.getToolboxByName('Mesh_Cross_Section')
            cs = mesh.selectedCS()
            if cs:
                device.draw_segment(primitives.Segment(cs.start, cs.end))
                
        else: # List of cs names.
            for k in self.cross_sections:
                try:
                    b = mesh.cross_sections[k]
                except KeyError:
                    pass
                else:
                    device.draw_segment(
                        primitives.Segment(b.start, b.end) )

defaultMeshCSColor = color.gray50
defaultMeshCSLineWidth = 1
if config.dimension() == 2:
    widthRange = (0,10)
# In vtk, line widths of 0 cause errors
elif config.dimension() == 3:
    widthRange = (1,10)

def _setMeshCSDefaults(menuitem, color, linewidth):
    global defaultMeshCSColor
    global defaultMeshCSLineWidth
    defaultMeshCSColor = color
    defaultMeshCSLineWidth = linewidth

meshcsdispparams = [
    color.ColorParameter('color', value=defaultMeshCSColor,
                         tip="In which color?"),
    parameter.IntRangeParameter('linewidth', widthRange, defaultMeshCSLineWidth,
                                tip="Thickness of the line.")]

mainmenu.gfxdefaultsmenu.Meshes.addItem(oofmenu.OOFMenuItem(
    "Cross_Section",
    callback=_setMeshCSDefaults,
    params=meshcsdispparams,
    ordering=3,
    help="Set default parameters for Mesh Cross Section displays.",
    discussion="""<para>

    Set default parameters for
    <link linkend="RegisteredClass-MeshCrossSectionDisplay"><classname>MeshCrossSectionDisplays</classname></link>.
    See <xref linkend="RegisteredClass-MeshCrossSectionDisplay"/> for the
    details.  This command may be put into your &oof2rc; file to set
    defaults for all &oof2; sessions.
    
    </para>"""))
                  
meshCrossSectionDisplay = registeredclass.Registration(
    'Cross Section',
    display.DisplayMethod,
    MeshCrossSectionDisplay,
    params=[meshcsparams.MeshCrossSectionSetParameter(
            'cross_sections', placeholder.selection,
            tip="Which cross-section to display?")] + meshcsdispparams,
    ordering=5.0,
    layerordering=display.SemiLinear,
    whoclasses=('Mesh',),
    tip="Determine which cross sections are displayed, and how.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/meshcsdisplay.xml',)
    )


def defaultMeshCrossSectionDisplay():
    return meshCrossSectionDisplay(color=defaultMeshCSColor,
                                   linewidth=defaultMeshCSLineWidth)

ghostgfxwindow.PredefinedLayer('Mesh', '<contourable>',
                               defaultMeshCrossSectionDisplay)
