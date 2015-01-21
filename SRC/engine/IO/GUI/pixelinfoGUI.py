# -*- python -*-
# $RCSfile: pixelinfoGUI.py,v $
# $Revision: 1.14.10.2 $
# $Author: langer $
# $Date: 2013/11/08 20:45:12 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import guitop
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.engine import material
from ooflib.common import debug
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import pixelinfoplugin
import gtk

class MaterialPlugIn(pixelinfoplugin.PixelInfoPlugIn):
    ordering = 3
    nrows = 1
    def __init__(self, toolbox, table, row):
        debug.mainthreadTest()
        pixelinfoplugin.PixelInfoPlugIn.__init__(self, toolbox)

        label=gtk.Label('material=')
        label.set_alignment(1.0, 0.5)
        table.attach(label, 0,1, row,row+1, xpadding=5, xoptions=gtk.FILL)
        self.materialtext = gtk.Entry()
        gtklogger.setWidgetName(self.materialtext, 'material')
        self.materialtext.set_size_request(12*guitop.top().charsize, -1)
        self.materialtext.set_editable(0)
        table.attach(self.materialtext, 1,2, row,row+1,
                     xpadding=5, xoptions=gtk.EXPAND|gtk.FILL)
        self.sbcb = switchboard.requestCallbackMain(
            'materials changed in microstructure', self.matchanged)

    def close(self):
        switchboard.removeCallback(self.sbcb)
        pixelinfoplugin.PixelInfoPlugIn.close(self)

    def update(self, where):
        debug.mainthreadTest()
        microstructure = self.toolbox.findMicrostructure()
        if microstructure and where is not None:
            mat = material.getMaterialFromPoint(microstructure, where)
            if mat:
                self.materialtext.set_text(mat.name())
                return
        self.materialtext.set_text('<No material>')

    def clear(self):
        debug.mainthreadTest()
        self.materialtext.set_text("")

    def nonsense(self):
        debug.mainthreadTest()
        self.materialtext.set_text('???')

    def matchanged(self, ms):
        if ms is self.toolbox.findMicrostructure():
            self.update(self.toolbox.currentPixel())

pixelinfoplugin.registerPlugInClass(MaterialPlugIn)
