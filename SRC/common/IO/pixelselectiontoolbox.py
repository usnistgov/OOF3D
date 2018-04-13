# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.common import debug
from ooflib.common import toolbox
from ooflib.common import pixelselection
from ooflib.common.IO import genericselecttoolbox
from ooflib.common.IO import pixelselectionmenu

# See NOTES/selection_machinery.txt

# The GUI version of the toolbox contains a RegisteredClassFactory for
# the SelectionMethods.  It installs itself as the graphics window's
# MouseHandler.  When it gets a 'down' mouse event, it starts storing
# the events' positions.  When it gets an 'up' event, it checks the
# 'events' setting for current SelectionMethod in the factory,
# constructs an OOFMenu argument list with the method's parameters,
# and invokes the non-GUI menu item, which creates the actual method
# does the selection.

def toolboxName():
    if config.dimension() == 3:
        return 'Voxel_Selection'
    else:
        return 'Pixel_Selection'
    

class PixelSelectToolbox(genericselecttoolbox.GenericSelectToolbox):
    def __init__(self, gfxwindow):
        genericselecttoolbox.GenericSelectToolbox.__init__(
            self,
            name=toolboxName(),
            method=pixelselection.VoxelSelectionMethod,
            menu=pixelselectionmenu.selectmenu,
            gfxwindow=gfxwindow)

    def getSelectionSource(self):
        # Return the Microstructure of the top Microstructure or Image
        # layer.
        who = self.gfxwindow().topwho('Microstructure', 'Image')
        if who is not None:
            if who.getClassName() == 'Microstructure':
                return who
            return who.getParent() # Microstructure is the parent of Image

    # The following two functions are used when generating xml output.
    def objName(self):
        return 'Pixel'
    def sourceName(self):
        return '&micro; or &image;'

    tip = "Select pixels in a Microstructure."
    discussion = """<para>
    Commands for <link
    linkend='Section:Concepts:Microstructure:PixelSelection'>selecting</link>
    pixels in a &micro;, based on mouse input.
    </para>"""
    
toolbox.registerToolboxClass(PixelSelectToolbox, ordering = 1.5)


