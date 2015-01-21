# -*- python -*-
# $RCSfile: bitoverlaydisplay.py,v $
# $Revision: 1.28.18.27 $
# $Author: langer $
# $Date: 2014/09/22 20:53:10 $

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
from ooflib.SWIG.common.IO import canvaslayers
from ooflib.common import color
from ooflib.common import debug
from ooflib.common import registeredclass
from ooflib.common.IO import bitmapdisplay
from ooflib.common.IO import display
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump

# The BitmapOverlayDisplayMethod is used to display objects that have
# a getPixelSet() method in their Who class.  getPixelSet() can return
# None, in which case nothing is drawn.  The bitmap marks pixels to be
# drawn as an overlay on the topmost image in the display.  The pixels
# are drawn with a single color and transparency.

class BitmapOverlayDisplayMethod(display.DisplayMethod):
    def __init__(self, color, tintOpacity):
        self.color = color
        self.tintOpacity = tintOpacity
        display.DisplayMethod.__init__(self)
        self.pixchangesignal = switchboard.requestCallback(
            "pixel selection changed", self.pixChangedCB)

    def destroy(self, destroy_canvaslayer):
        switchboard.removeCallback(self.pixchangesignal)
        display.DisplayMethod.destroy(self, destroy_canvaslayer)

    # def draw(self, gfxwindow, canvas): # Obsolete in 3D
    #     bitmap = self.who().resolve(gfxwindow).getBitmap() # BitmapOverlay obj.
    #     if bitmap is None or bitmap.empty():
    #         return
    #     bitmap.setColor(self.color)
    #     bitmap.setTintAlpha(self.tintOpacity)
    #     if config.dimension() == 3:
    #         bitmap.setVoxelAlpha(self.voxelOpacity)
    #     canvas.draw_alpha_image(bitmap, coord.origin, bitmap.size())

    def newLayer(self):
        return canvaslayers.OverlayVoxels(self.gfxwindow.oofcanvas,
                                          "BitmapOverlay")

    def layersChanged(self):
        # When layers have changed, every overlayer must connect to the
        # overlayer below it, or to the image, if it's the bottom
        # overlayer.  The image's layersChanged method connects to the
        # top overlayer.
        # getOverlayers() returns an empty list if there is no image
        # layer for the overlayers to overlie.
        overlayers = self.gfxwindow.getOverlayers()
        try:
            which = overlayers.index(self)
        except ValueError:
            # this isn't an active overlayer
            self.canvaslayer.disconnect()
            return
        imageLayer = self.gfxwindow.topImage()
        if which == 0:
            # This is the bottom overlayer.
            imageLayer.canvaslayer.connectBottomOverlayer(self.canvaslayer)
        else:
            self.canvaslayer.connectToOverlayer(overlayers[which-1].canvaslayer)

    def setParams(self):
        self.canvaslayer.setTintOpacity(self.tintOpacity)
        self.canvaslayer.setColor(self.color)

    def whoChanged(self):
        who = self.who().resolve(self.gfxwindow)
        if who is not None:
            pixset = who.getPixelSet()
            if pixset is not None:
                self.canvaslayer.setPixelSet(pixset)
                return True
        self.canvaslayer.clearPixelSet()
        return True

    def pixChangedCB(self, who):    # switchboard "pixel selection changed"
        if self.who() is not None and who is self.who().resolve(self.gfxwindow):
            if self.canvaslayer:
                self.canvaslayer.setModified()

    # def getTimeStamp(self, gfxwindow):
    #     return self.timestamp

    def isOverlayer(self):
        return True
    # def isEmpty(self, gfxwindow):
    #     bitmap = self.who().resolve(gfxwindow).getBitmap()
    #     return bitmap is None or bitmap.empty()

if config.dimension()==2:
    bitoverlayparams=[color.ColorParameter('color', tip="Bitmap color."),
            parameter.FloatRangeParameter('tintOpacity', (0., 1., 0.01), 0.6,
                                          tip="Opacity of the overlay.")]
elif config.dimension()==3:
    bitoverlayparams=[color.ColorParameter('color', tip="Bitmap color."),
            parameter.FloatRangeParameter('tintOpacity', (0., 1., 0.01), 0.0,
                                          tip="Opacity of the tint."),
                      ]
    

bitmapOverlay = registeredclass.Registration(
    'BitmapOverlay',
    display.DisplayMethod,
    BitmapOverlayDisplayMethod,
    params=bitoverlayparams,
    ordering=0,
    layerordering=display.SemiPlanar,
    whoclasses=('Pixel Selection', 'Active Area'),
    tip="Special bitmap display method for overlays.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/common/reg/bitoverlaydisplay.xml')
    )

