# -*- python -*-
# $RCSfile: pixelinfoGUI.py,v $
# $Revision: 1.23.18.10 $
# $Author: langer $
# $Date: 2014/11/05 16:55:02 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.SWIG.common import guitop
from ooflib.SWIG.common import switchboard
from ooflib.common import color
from ooflib.common import debug
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import pixelinfoplugin
from ooflib.common.IO.GUI import tooltips

if config.dimension() == 2:
    from ooflib.SWIG.image import oofimage
elif config.dimension() == 3:
    from ooflib.SWIG.image import oofimage3d as oofimage

import gtk

class ImagePlugIn(pixelinfoplugin.PixelInfoPlugIn):
    ordering = 1
    nrows = 5
    def __init__(self, toolbox, table, row):
        debug.mainthreadTest()
        pixelinfoplugin.PixelInfoPlugIn.__init__(self, toolbox)

        # colorv is set by "update" and "nonsense", it can be None (no
        # color), "Nonsense", or a color.Color object.
        # Statefulness is needed to remain consistency when a user
        # switches from RGB to HSV or vice versa.
        self.colorv = None
        
        label = gtk.Label('image=')
        label.set_alignment(1.0, 0.5)
        table.attach(label, 0,1, row,row+1, xpadding=5, xoptions=gtk.FILL)
        self.imagetext = gtk.Entry()
        gtklogger.setWidgetName(self.imagetext, "Image")
        self.imagetext.set_size_request(12*guitop.top().charsize, -1)
        self.imagetext.set_editable(0)
        table.attach(self.imagetext, 1,2, row,row+1,
                     xpadding=5, xoptions=gtk.EXPAND|gtk.FILL)

        selectorbox = gtk.HBox()
        self.rgb_selector = gtk.RadioButton(group=None,label="RGB")
        tooltips.set_tooltip_text(self.rgb_selector,
                             "View color values in Red-Green-Blue format.")
        selectorbox.add(self.rgb_selector)
        self.hsv_selector = gtk.RadioButton(group=self.rgb_selector,
                                            label="HSV")
        tooltips.set_tooltip_text(
            self.hsv_selector,
            "View color values in Hue-Saturation-Value format.")
        selectorbox.add(self.hsv_selector)
        self.rgb_selector.set_active(1) # Default.

        # Because this is a two-element group of radio buttons, only
        # need to connect to the toggle signal on one of the buttons.
        # If more buttons get added, this strategy will fail.
        gtklogger.setWidgetName(self.rgb_selector, "RGB selector")
        # "toggle" signal is not actually logged.
        # gtklogger.connect(self.rgb_selector, "toggled", self.selector_cb)

        gtklogger.setWidgetName(self.hsv_selector, "HSV selector")
        gtklogger.connect(self.rgb_selector, "clicked", self.selector_cb)
        gtklogger.connect(self.hsv_selector, "clicked", self.selector_cb)
        

        table.attach(selectorbox, 0,2, row+1, row+2,
                     xoptions=gtk.EXPAND|gtk.FILL)
        
        self.label1 = gtk.Label('red=')
        self.label1.set_alignment(1.0, 0.5)
        table.attach(self.label1, 0,1, row+2,row+3,
                     xpadding=5, xoptions=gtk.FILL)
        self.text1 = gtk.Entry()
        gtklogger.setWidgetName(self.text1,'Text 1')
        self.text1.set_size_request(10*guitop.top().digitsize, -1)
        self.text1.set_editable(0)
        table.attach(self.text1, 1,2, row+2,row+3,
                     xpadding=5, xoptions=gtk.EXPAND|gtk.FILL)

        self.label2 = gtk.Label('green=')
        self.label2.set_alignment(1.0, 0.5)
        table.attach(self.label2, 0,1, row+3,row+4,
                     xpadding=5, xoptions=gtk.FILL)
        self.text2 = gtk.Entry()
        gtklogger.setWidgetName(self.text2,'Text 2')
        self.text2.set_size_request(10*guitop.top().digitsize, -1)
        self.text2.set_editable(0)
        table.attach(self.text2, 1,2, row+3,row+4,
                     xpadding=5, xoptions=gtk.EXPAND|gtk.FILL)

        self.label3 = gtk.Label('blue=')
        self.label3.set_alignment(1.0, 0.5)
        table.attach(self.label3, 0,1, row+4,row+5,
                     xpadding=5, xoptions=gtk.FILL)
        self.text3 = gtk.Entry()
        gtklogger.setWidgetName(self.text3,'Text 3')
        self.text3.set_size_request(10*guitop.top().digitsize, -1)
        self.text3.set_editable(0)
        table.attach(self.text3, 1,2, row+4,row+5,
                     xpadding=5, xoptions=gtk.EXPAND|gtk.FILL)

        self.sbcallbacks = [
            switchboard.requestCallbackMain('modified image',
                                            self.image_changed)
            ]

    def close(self):
        map(switchboard.removeCallback, self.sbcallbacks)

    def update(self, where):
        debug.mainthreadTest()
        # If the topmost Image in the display is obscured by a
        # Microstructure, then Image data is not displayed in the
        # toolbox.  This is because it wouldn't be clear which Image
        # the data is from, if the Microstructure has more than one
        # Image or if the Image is from a different Microstructure.
        image = self.toolbox.gfxwindow().topmost('Image', 'Microstructure')

        if config.dimension() == 2:
            imagetype = oofimage.OOFImagePtr
        elif config.dimension() == 3:
            imagetype = oofimage.OOFImage3DPtr
        if isinstance(image, imagetype) and where is not None:
            self.colorv = image[where]
            imagecontext = self.toolbox.gfxwindow().topwho('Image')
            self.imagetext.set_text(imagecontext.path())
        else:
            self.colorv = None
            self.imagetext.set_text('(No image)')
        self.color_display()

    # GTK callback for selection toggles.
    def selector_cb(self, gtkobj):
        self.color_display()

    def clear(self):
        self.colorv = None
        self.imagetext.set_text("")
        self.color_display()

    def color_display(self):
        debug.mainthreadTest()
        # First do labels, then do colors.
        if self.rgb_selector.get_active():
            self.label1.set_text("red=")
            self.label2.set_text("green=")
            self.label3.set_text("blue=")
        else:
            self.label1.set_text("hue=")
            self.label2.set_text("saturation=")
            self.label3.set_text("value=")

        if self.colorv == "Nonsense":
            return
            
        if self.colorv is not None:
            (c1,c2,c3) = (self.colorv.getRed(),
                          self.colorv.getGreen(),
                          self.colorv.getBlue())
            if not self.rgb_selector.get_active():
                (c1,c2,c3) = color.hsv_from_rgb(c1,c2,c3)
            self.text1.set_text(`c1`)
            self.text2.set_text(`c2`)
            self.text3.set_text(`c3`)
            
        else:
            self.text1.set_text("")
            self.text2.set_text("")
            self.text3.set_text("")

    
    def image_changed(self, modifier, image):
        self.update(self.toolbox.currentPixel())

    def nonsense(self):
        debug.mainthreadTest()
        self.colorv = "Nonsense"
        debug.mainthreadTest()
        self.imagetext.set_text('???')
        self.text1.set_text('???')
        self.text2.set_text('???')
        self.text3.set_text('???')


pixelinfoplugin.registerPlugInClass(ImagePlugIn)

