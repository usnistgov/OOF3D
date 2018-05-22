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
from ooflib.SWIG.common import voxelfilter
from ooflib.SWIG.common.IO import canvaslayers
from ooflib.common import color
from ooflib.common import debug
from ooflib.common import registeredclass
from ooflib.common.IO import bitmapdisplay
from ooflib.common.IO import display
from ooflib.common.IO import ghostgfxwindow
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import pixelinfodisplay # for Top Bitmap
from ooflib.common.IO import whoville

class PixelSelectionDisplay(display.DisplayMethod):
    def __init__(self, color, opacity):
        self.color = color
        self.opacity = opacity
        self.filter = None
        self.sbcallbacks = [
            switchboard.requestCallback("voxel filter changed",
                                        self.filterChanged),
            switchboard.requestCallback("pixel selection changed",
                                        self.selectionChanged)
            ]
        display.DisplayMethod.__init__(self)

    def newLayer(self):
        return canvaslayers.MonochromeVoxelLayer(self.gfxwindow.oofcanvas,
                                                 "PixelSelection")

    def whoChanged(self):
        # Called by GhostGfxWindow when layers have changed.  If this
        # layer is using a WhoProxy, its referent may have
        # changed. 'who' can be an Image or a Microstructure.
        selctxt = self.selectionContext()
        # Find a BitmapDisplayMethod that displays the requested
        # Microstructure or one of its Images
        for layer in self.gfxwindow.layers:
            if (isinstance(layer, bitmapdisplay.BitmapDisplayMethod) and
                not isinstance(layer.who(), whoville.WhoProxy) and
                layer.who().getSelectionContext() is selctxt):
                self.canvaslayer.set_image_layer(layer.canvaslayer)
                # Set the filter to display the selected voxels in any
                # other bitmap display of the same microstructure.
                # The filter is the intersection of a SelectedVoxels
                # filter with the union of the filters for the other
                # layers.
                ## TODO: This first pass ignores the filters in the
                ## other layers.
                # Keep a reference to prevent the filter from being
                # destroyed too soon.
                self.filter = voxelfilter.SelectedVoxels()
                self.canvaslayer.set_filter(self.filter)
                self.setMicrostructure()
                break
        else:
            # No BitmapDisplayMethod was found. Don't display
            # anything.
            ## TODO: Using setEmpty isn't really the right thing to
            ## call here, but it works.  We can't use hide() or show()
            ## because the user might have explicitly hidden the
            ## layer.  The problem with setEmpty is just that it was
            ## introduced as a hack, and if the need for the hack goes
            ## away, setEmpty might go away too.
            self.canvaslayer.setEmpty(True)

        # Returning True here tells GhostGfxWindow.incorporateLayer to
        # call setParams.
        return True
        

    def destroy(self, destroy_canvaslayer):
        map(switchboard.removeCallback, self.sbcallbacks)
        display.DisplayMethod.destroy(self, destroy_canvaslayer)

    def filterChanged(self, filter, *args, **kwargs):
        if filter == self.filter:
            self.filter.setModified()
            self.canvaslayer.filterModified()

    def selectionContext(self):
        who = self.who().resolve(self.gfxwindow)
        if who is not None:
            return who.getSelectionContext()

    def selectionChanged(self, selection):
        if selection is self.selectionContext():
            self.canvaslayer.setEmpty(selection.empty())
            self.canvaslayer.setModified()

    def setParams(self):
        self.canvaslayer.set_color(self.color)
        self.canvaslayer.set_opacity(self.opacity)

    def setMicrostructure(self):
        who = self.who().resolve(self.gfxwindow)
        if who:
            self.filter.setMicrostructure(who.getMicrostructure())
            self.canvaslayer.setEmpty(self.selectionContext().empty())

defaultPixelSelectionColor = color.RGBColor(1.0, 0.22, 0.09)
defaultOpacity = 0.9

pixelSelectParams = [
    color.ColorParameter('color', defaultPixelSelectionColor,
                         tip='Color of selected voxels.'),
    parameter.FloatRangeParameter('opacity', (0., 1.0, 0.01), defaultOpacity,
                                  tip="Opacity of the color")
]

pixelSelectionDisplay = registeredclass.Registration(
    'Pixel Selection',
    display.DisplayMethod,
    PixelSelectionDisplay,
    params=pixelSelectParams,
    ordering = 0,
    layerordering=display.SemiPlanar(0.1),
    whoclasses=('Microstructure', 'Image', 'Top Bitmap'),
    tip="Indicator for selected voxels.")


def _setDefaultPixelSelectionParams(menuitem, color, opacity):
    global defaultPixelSelectionColor
    global defaultOpacity
    defaultPixelSelectionColor = color
    defaultOpacity = opacity




mainmenu.gfxdefaultsmenu.Pixels.addItem(oofmenu.OOFMenuItem(
    'Pixel_Selection',
    callback=_setDefaultPixelSelectionParams,
    params = pixelSelectParams,
    help="Set default parameters for displaying selected pixels.",
    discussion="""<para>

    Set default parameters for the <xref
    linkend="RegisteredClass:PixelSelectionDisplay"/> that is used
    to display <link linkend="Section:Concepts:Microstructure:PixelSelection">pixel selections</link>.
    This command can be put in the &oof2rc; file to set defaults for all
    &oof2; sessions.

    </para>"""))

# def predefinedPixelSelectionLayer():
#     return bitoverlaydisplay.bitmapOverlay(color=defaultPixelSelectionColor,
#                                            tintOpacity=defaultTintOpacity)

# ghostgfxwindow.PredefinedLayer('Pixel Selection', '<top microstructure>',
#                                predefinedPixelSelectionLayer)


def predefinedPixelSelectionLayer():
    return pixelSelectionDisplay(color=defaultPixelSelectionColor,
                                 opacity=defaultOpacity)

ghostgfxwindow.PredefinedLayer('Top Bitmap', '<top bitmap>',
                               predefinedPixelSelectionLayer)
