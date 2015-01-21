# -*- python -*-
# $RCSfile: pixelinfo.py,v $
# $Revision: 1.22.18.11 $
# $Author: fyc $
# $Date: 2014/07/22 17:56:01 $


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.SWIG.common import switchboard
# from ooflib.SWIG.common import timestamp
from ooflib.SWIG.common.IO import view
from ooflib.SWIG.common.IO import vtkutils
from ooflib.common import debug
from ooflib.common import primitives
from ooflib.common import toolbox
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import reporter


# Despite the name "PixelInfoToolbox", this class works for both 2D
# and 3D

def toolboxName():
    if config.dimension() == 2:
        return "Pixel_Info"
    else:
        return "Voxel_Info"
    

class PixelInfoToolbox(toolbox.Toolbox):
    def __init__(self, gfxwindow):
        self.point = None               # location of last query
        # self.timestamp = timestamp.TimeStamp()
        toolbox.Toolbox.__init__(self, toolboxName(), gfxwindow)
        self.lastMS = None

        self.sbcallbacks = [
            switchboard.requestCallback((self.gfxwindow(), "layers changed"),
                                        self.newLayers),
            ]

    def close(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        self.sbcallbacks = []
        
    def makeMenu(self, menu):
        self.menu = menu
        if config.dimension() == 2:
            pixelname = 'pixel'
        else:
            pixelname = 'voxel'
        positionparams = [
            primitives.PointParameter(
                'point', tip='The position of the queried %s.' % pixelname)
            ]
        if config.dimension() == 3:
            positionparams.append(view.ViewParameter('view'))
        # positionparams=[
        #     parameter.IntParameter('x', 0, tip="The x coordinate."),
        #     parameter.IntParameter('y', 0, tip="The y coordinate.")]
        # if config.dimension() == 3:
        #     positionparams.append(
        #         parameter.IntParameter('z', 0, tip="The z coordinate."))
        helpstring = "Query the %s at the given point." % pixelname

        menu.addItem(oofmenu.OOFMenuItem(
            'Query',
            callback=self.queryPixel,
            params=positionparams,
            help=helpstring,
            discussion="""<para>
            Display information about the %s at the given screen
            coordinate.  In GUI mode, the information appears in the
            <link linkend='Section:Graphics:PixelInfo'>Pixel
            Info</link> toolbox in the graphics window.  This command
            has no effect when the GUI is not running.
            </para>""" % pixelname
            ))
        menu.addItem(oofmenu.OOFMenuItem(
                'QueryDirectly',
                callback=self.queryPixelDirectly,
                params=[primitives.PointParameter(
                        'voxel', tip="The coordinates of the queried voxel.")],
                help="Query the voxel at the given position in the image.",
                discussion="""<para>
                Display information about the voxel at the given
                position.  In GUI mode, the information appears in the
                <link linkend='Section:Graphics:PixelInfo'>PIxel
                Info</link> toolbox in the graphics window.  This
                command has no effect when the GUI is not running.
                </para>"""
                ))
        menu.addItem(oofmenu.OOFMenuItem(
            'Clear',
            callback=self.clearPixel,
            params=[],
            help="Reset the pixel info toolbox.",
            discussion="""<para>
            Clear any displayed information from previous mouse clicks.
            In GUI mode, this clears the <link
            linkend='Section:Graphics:PixelInfo'>Pixel Info</link>
            toolbox in the graphics window.  This command has no
            effect if the GUI is not running.
            </para>"""
            ))

    if config.dimension() == 3:
        def queryPixel(self, menuitem, point, view): # menu callback
            # "point" is a screen coordinate.
            # self.timestamp.increment()
            bitmap = self.gfxwindow().topwho('Microstructure', 'Image')
            ## TODO OPT: use findClickedPosition instead?
            cell = self.gfxwindow().findClickedCell(bitmap, point, view)
            if cell is not None:
                self.mousepoint = vtkutils.cell2coord(cell)
                self.point = self.findMicrostructure().pixelFromPoint(
                    self.mousepoint)
            else:
                self.point = None
            switchboard.notify(self) # caught by GUI toolbox, PixelInfoDisplay
            switchboard.notify('redraw')

        def queryPixelDirectly(self, menuitem, voxel):
            # This gets the voxel coordinates directly, instead of
            # screen coordinates.
            bitmap = self.gfxwindow().topwho('Microstructure', 'Image')
            self.point = voxel
            switchboard.notify(self)
            switchboard.notify('redraw')
    else:
        def queryPixel(self, menuitem, point):
            self.timestep.increment()
            self.point = point
            switchboard.notify(self)
            switchboard.notify('redraw')

    def clearPixel(self, menuitem): # Menu callback.
        # self.timestamp.increment()
        self.point = None
        switchboard.notify(self)
        switchboard.notify('redraw')
        
    def currentPixel(self):
        return self.point

    def findMicrostructure(self):
        ## This used to check for Skeletons and Meshes, too, and use
        ## their getMicrostructure function.  That led to some
        ## confusing situations, when a Skeleton was displayed over an
        ## Image from a different Microstructure, for example.  So now
        ## it doesn't return anything when no Microstructure or Image
        ## is displayed.
        who = self.gfxwindow().topwho('Microstructure', 'Image')
        if who is not None:
            return who.getMicrostructure()
        return None

    def newLayers(self):        # switchboard (gfxwindow, "layers changed")
        ms = self.findMicrostructure()
        if ms is not self.lastMS:
            self.lastMS = ms
            switchboard.notify(self)

    # def getTimeStamp(self):
    #     return self.timestamp

    if config.dimension() == 2:
        noun = 'pixel'
    else:
        noun = 'voxel'
    tip="Get information about a %s." % noun
    discussion="""<para>
    Get information about a %s, based on mouse input.
    </para>""" % noun
    
toolbox.registerToolboxClass(PixelInfoToolbox, ordering=1.0)
