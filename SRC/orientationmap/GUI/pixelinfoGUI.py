# -*- python -*-
# $RCSfile: pixelinfoGUI.py,v $
# $Revision: 1.7.18.2 $
# $Author: langer $
# $Date: 2014/09/27 22:34:43 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import switchboard
from ooflib.SWIG.orientationmap import orientmapdata
from ooflib.common import debug
from ooflib.common.IO import parameter
#from ooflib.common.IO.GUI import pixelinfoGUI
from ooflib.common.IO.GUI import pixelinfoplugin
from ooflib.engine.IO import orientationmatrix
import gtk
import math

class OrientMapPixelInfoPlugIn(pixelinfoplugin.PixelInfoPlugIn):
    ordering=4
    nrows = 1
    def __init__(self, toolbox, table, row):
        debug.mainthreadTest()
        pixelinfoplugin.PixelInfoPlugIn.__init__(self, toolbox)

        self.label = gtk.Label('Orientation=')
        self.label.set_alignment(1.0, 0.5)
        table.attach(self.label, 0,1, row,row+1, xpadding=5, xoptions=gtk.FILL)

        self.vbox = gtk.VBox()
        self.param = parameter.ConvertibleRegisteredParameter(
            'dummy', orientationmatrix.Orientation)
        self.widget = self.param.makeWidget() # RegisteredClassFactory
        self.widget.makeReadOnly()
        self.text = gtk.Entry()
        self.text.set_editable(0)
        self.vbox.pack_start(self.text, expand=0, fill=0)
        self.current_mode = 'text'
        table.attach(self.vbox, 1,2, row,row+1,
                     xpadding=5, xoptions=gtk.EXPAND|gtk.FILL)
        self.sbcbs = [
            switchboard.requestCallbackMain(
            'materials changed in microstructure', self.materialchanged),
            switchboard.requestCallbackMain('OrientationMap changed',
                                            self.materialchanged),
            switchboard.requestCallbackMain('material changed',
                                            self.materialchanged),
            switchboard.requestCallbackMain('prop_added_to_material',
                                            self.materialchanged),
            switchboard.requestCallbackMain('prop_removed_from_material',
                                            self.materialchanged),
            switchboard.requestCallbackMain(self.widget, self.widgetcb)
            ]

        self.update(None)

    def set_mode(self, mode):
        if self.current_mode != mode:
            if mode == 'text':
                self.vbox.remove(self.widget.gtk)
                self.vbox.pack_start(self.text, expand=0, fill=0)
                self.text.show()
            elif mode == 'widget':
                self.vbox.remove(self.text)
                self.vbox.pack_start(self.widget.gtk, expand=0, fill=0)
                self.widget.show()
            self.current_mode = mode
                                                              
    def close(self):
        map(switchboard.removeCallback, self.sbcbs)
        pixelinfoplugin.PixelInfoPlugIn.close(self)

    def materialchanged(self, *args, **kwargs):
        # Generic switchboard callback, called when materials or
        # properties change, or materials are assigned to or removed
        # from pixels, or the material map changes in a
        # Microstructure.  We could check here to see if the change
        # affects the actual object that we're displaying, but it's
        # not worth the effort.
        self.update(self.toolbox.currentPixel())

    def update(self, where):
        debug.mainthreadTest()
        microstructure = self.toolbox.findMicrostructure()
        if microstructure and where is not None:
            orientsource = orientmapdata.getOrientationAtPoint(
                microstructure, where)
            if orientsource:
                orientation, source = orientsource
                # orientation is a COrientation instance.  It has to
                # be converted into an orientationmatrix.Orientation
                # object so that we can make (ab)use of the
                # ConvertibleRegisteredClass machinery.
                abg = orientation.abg()
                if self.param.value is not None:
                    klass = self.param.value.__class__
                    reg = self.param.value.getRegistration()
                else:
                    reg = orientationmatrix.Orientation.registry[0]
                    klass = reg.subclass
                base = orientationmatrix.Abg(
                    *[a*180./math.pi for a in (abg.alpha(), abg.beta(),
                                               abg.gamma())])
                newvalue = klass(*reg.from_base(None, base))
                self.param.value = newvalue
                self.widget.set(newvalue, interactive=False)
                self.set_mode("widget")
                self.label.set_text('Orientation=\n(%s)' % source)
            else:                       # orientsource is None
                self.text.set_text("<No Orientation>")
                self.set_mode("text")
                self.label.set_text('Orientation=')
        else:                      # microstructure is None or where is None
            self.text.set_text("<No Microstructure>")
            self.set_mode("text")
            self.label.set_text('Orientation=')

    def widgetcb(self, *args, **kwargs):
        self.param.value = self.widget.get_value()

    def clear(self):
        debug.mainthreadTest()
        self.set_mode("text")
        self.text.set_text("---")

    def nonsense(self):
        debug.mainthreadTest()
        self.set_mode("text")
        self.text.set_text("???")
                
                
                    
        
pixelinfoplugin.registerPlugInClass(OrientMapPixelInfoPlugIn)
