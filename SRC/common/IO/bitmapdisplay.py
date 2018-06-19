# -*- python -*-

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
    def __init__(self, filter, opacity):
        self.filter = filter
        self.autoOpacityFactor = 1.0
        self.opacity = opacity
        self.sbcallbacks = [
            switchboard.requestCallback("voxel filter changed",
                                        self.filterChanged),
            switchboard.requestCallback("autoopacity", self.autoOpacityCB)
        ]
        display.DisplayMethod.__init__(self)

    def draw(self, gfxwindow, canvas): # Obsolete in 3D
        bitmapobj = self.who().getObject(gfxwindow)
        self.canvaslayer.draw_image(bitmapobj, coord.origin, bitmapobj.size())

    def layerName(self):        # redefine in derived classes
        return "Bitmap"

    def destroy(self, destroy_canvaslayer):
        map(switchboard.removeCallback, self.sbcallbacks)
        self.sbcallbacks = []
        display.DisplayMethod.destroy(self, destroy_canvaslayer)

    def newLayer(self):
        layer = canvaslayers.ImageCanvasLayer(
            self.gfxwindow.oofcanvas, self.layerName())
        layer.setEmpty(False)
        return layer

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
        self.canvaslayer.set_opacity(self.getOpacity())
        self.setMicrostructure()

    def getOpacity(self):
        return self.opacity * self.autoOpacityFactor

    def filterChanged(self, filter, *args, **kwargs):
        if filter == self.filter:
            # It may not be necessary to call both of these, but it
            # doesn't hurt.
            self.filter.setModified();
            self.canvaslayer.filterModified()
        
    def setMicrostructure(self):
        who = self.who()
        if who:
            self.filter.setMicrostructure(who.getMicrostructure())

    def isImage(self):
        return True

    def autoOpacityCB(self, gfxwindow, factor):
        if gfxwindow is self.gfxwindow:
            self.autoOpacityFactor = factor
            self.canvaslayer.set_opacity(self.getOpacity())
    
defaultImageOpacity = 1.0
opacityRange = (0, 1, 0.05)

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
            tip="Voxels to include in the display."),
        parameter.FloatRangeParameter(
            "opacity",
            opacityRange,
            defaultImageOpacity,
            tip='Opacity of the image.')          
        ],
    whoclasses = ('Image',),
    tip="Display an Image as a bitmap.",
    discussion = xmlmenudump.loadFile(
        'DISCUSSIONS/common/reg/bitmapdisplay.xml')
    )

