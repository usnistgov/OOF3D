# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import labeltree
from ooflib.common import toolbox
from ooflib.common import pixelselection
from ooflib.common.IO import genericselecttoolbox
from ooflib.common.IO import whoville
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
            menu = pixelselectionmenu.selectmenu,
            gfxwindow=gfxwindow)

    # def signal(self, method, pointlist, who):
    #     debug.dumpTrace()
    #     switchboard.notify("pixel selection changed", who)
    #     switchboard.notify("new pixel selection", method, pointlist)
    #     switchboard.notify("redraw")

    def getSelectionSource(self):
        # Return the Microstructure of the top Microstructure or Image
        # layer.
        who = self.gfxwindow().topwho('Microstructure', 'Image')
        if who is not None:
            if who.getClassName() == 'Microstructure':
                return who
            return who.getParent() # Microstructure is the parent of Image

    # def sourceParams(self):
    #     return [whoville.AnyWhoParameter('source',
    #                                      tip="Microstructure or Image")]

    # def setSourceParams(self, menuitem, source):
    #     menuitem.get_arg('source').value = source.path()

    # def getSourceObject(self, params, gfxwindow):
    #     # Used by GenericSelectionToolbox.getSelection()
        
    #     # We're expecting a MicroStructure or an Image.

    #     # params is a dictionary of parameter values that was passed
    #     # to the menu item that was automatically created from a
    #     # PixelSelectionRegistration by
    #     # GenericSelectToolbox.rebuildMenus().  rebuildMenus() used
    #     # the derived sourceParams function to add the 'source'
    #     # parameter to the parameter list.

    #     # gfxwindow is the GfxWindow or GhostGfxWindow that the
    #     # selection was initiated in.  It might not be needed here
    #     # anymore.
        
    #     whopath = labeltree.makePath(params['source'])
    #     if len(whopath) == 1:
    #         return whoville.getClass('Microstructure')[whopath]
    #     if len(whopath) == 2:
    #         return whoville.getClass('Image')[whopath]

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


