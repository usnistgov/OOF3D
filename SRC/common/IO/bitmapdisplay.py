# -*- python -*-
# $RCSfile: bitmapdisplay.py,v $
# $Revision: 1.16.18.21 $
# $Author: langer $
# $Date: 2014/12/05 21:29:10 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.SWIG.common import coord
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common import voxelfilter
from ooflib.SWIG.common.IO import canvaslayers
from ooflib.common import debug
from ooflib.common import registeredclass
from ooflib.common.IO import display
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump

class BitmapDisplayMethod(display.DisplayMethod):
    def __init__(self, filter):
        self.filter = filter
        display.DisplayMethod.__init__(self)

    def draw(self, gfxwindow, canvas): # Obsolete in 3D
        bitmapobj = self.who().getObject(gfxwindow)
        self.canvaslayer.draw_image(bitmapobj, coord.origin, bitmapobj.size())

    def layerName(self):        # redefine in derived classes
        return "Bitmap"

    def newLayer(self):
        return canvaslayers.ImageCanvasLayer(
            self.gfxwindow.oofcanvas, self.layerName())

    def layersChanged(self):
        overlayers = self.gfxwindow.getOverlayers()
        topImage = self.gfxwindow.topImage()
        if topImage is self:
            self.canvaslayer.show(False) # hidden layers are never the top image
            if not overlayers:
                self.canvaslayer.noOverlayers()
            else:
                self.canvaslayer.connectTopOverlayer(overlayers[-1].canvaslayer)
        else:
            self.canvaslayer.hide(False)

    def whoChanged(self):
        # The who object itself has been modified, or a new one
        # assigned.  This is the switchboard callback for "who
        # changed", and is also called by setWho().
        bitmapobj = self.who().getObject(self.gfxwindow)
        self.canvaslayer.set_image(bitmapobj, coord.origin, bitmapobj.size())
        self.setMicrostructure()
        return True             # call setParams

    def setParams(self):
        self.canvaslayer.set_filter(self.filter)
        self.setMicrostructure()
        
    def setMicrostructure(self):
        who = self.who()
        if who:
            self.filter.setMicrostructure(who.getMicrostructure())

    def isImage(self):
        return True
    

bitmapDisplay = registeredclass.Registration(
    'Bitmap',
    display.DisplayMethod,
    BitmapDisplayMethod,
    ordering=-100,
    layerordering=display.Planar,
    params = [
        parameter.RegisteredParameter(
            "filter",
            voxelfilter.VoxelFilterPtr,
            voxelfilter.AllVoxels(),
            tip="Voxels to include in the display.")
        ],
    whoclasses = ('Image',),
    tip="Display an Image as a bitmap.",
    discussion = xmlmenudump.loadFile(
        'DISCUSSIONS/common/reg/bitmapdisplay.xml')
    )

