# -*- python -*-
# $RCSfile: voxelinfoGUI.py,v $
# $Revision: 1.2.18.9 $
# $Author: langer $
# $Date: 2013/11/08 20:43:04 $

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
from ooflib.common import debug
from ooflib.common import primitives
from ooflib.common.IO import pixelinfo
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import gtkutils
from ooflib.common.IO.GUI import mousehandler
from ooflib.common.IO.GUI import pixelinfoplugin
from ooflib.common.IO.GUI import toolboxGUI

import gtk


class VoxelInfoToolboxGUI(toolboxGUI.GfxToolbox, mousehandler.MouseHandler):
    def __init__(self, pixelinfotoolbox):
        debug.mainthreadTest()
        toolboxGUI.GfxToolbox.__init__(self, "Voxel Info", pixelinfotoolbox)
        mainbox = gtk.VBox()
        self.gtk.add(mainbox)

        self.table = gtk.Table(rows=4, columns=2)
        mainbox.pack_start(self.table, expand=0, fill=0)
        
        label = gtk.Label('x=')
        label.set_alignment(1.0, 0.5)
        self.table.attach(label, 0,1, 0,1, xpadding=5, xoptions=gtk.FILL)
        self.xtext = gtk.Entry()
        gtklogger.setWidgetName(self.xtext, "X")
        self.xtext.set_size_request(10*guitop.top().digitsize, -1)
        self.table.attach(self.xtext, 1,2, 0,1,
                          xpadding=5, xoptions=gtk.EXPAND|gtk.FILL)
        label = gtk.Label('y=')
        label.set_alignment(1.0, 0.5)
        self.table.attach(label, 0,1, 1,2, xpadding=5, xoptions=gtk.FILL)
        self.ytext = gtk.Entry()
        gtklogger.setWidgetName(self.ytext, "Y")
        self.ytext.set_size_request(10*guitop.top().digitsize, -1)
        self.table.attach(self.ytext, 1,2, 1,2,
                          xpadding=5, xoptions=gtk.EXPAND|gtk.FILL)
        label = gtk.Label('z=')
        label.set_alignment(1.0, 0.5)
        self.table.attach(label, 0,1, 2,3, xpadding=5, xoptions=gtk.FILL)
        self.ztext = gtk.Entry()
        gtklogger.setWidgetName(self.ztext, "Z")
        self.ztext.set_size_request(10*guitop.top().digitsize, -1)
        self.table.attach(self.ztext, 1,2, 2,3,
                          xpadding=5, xoptions=gtk.EXPAND|gtk.FILL)


        self.xtsignal = gtklogger.connect(self.xtext, 'changed',
                                          self.pointChanged)
        self.ytsignal = gtklogger.connect(self.ytext, 'changed',
                                          self.pointChanged)
        self.ztsignal = gtklogger.connect(self.ztext, 'changed',
                                          self.pointChanged)

        box = gtk.HBox(homogeneous=True, spacing=2)
        self.updatebutton = gtkutils.StockButton(gtk.STOCK_REFRESH, 'Update')
        box.pack_start(self.updatebutton, expand=1, fill=1)
        gtklogger.setWidgetName(self.updatebutton, "Update")
        gtklogger.connect(self.updatebutton, 'clicked', self.updateButtonCB)
        self.clearbutton = gtkutils.StockButton(gtk.STOCK_CLEAR, 'Clear')
        box.pack_start(self.clearbutton, expand=1, fill=1)
        gtklogger.setWidgetName(self.clearbutton, "Clear")
        gtklogger.connect(self.clearbutton, 'clicked', self.clearButtonCB)
        self.table.attach(box, 0,2, 3,4,
                          xpadding=5, xoptions=gtk.EXPAND|gtk.FILL, yoptions=0)

        self.updatebutton.set_sensitive(0)
        self.clearbutton.set_sensitive(0)
        self.buildGUI()
        
        self.sbcallbacks = [
            switchboard.requestCallbackMain(pixelinfotoolbox,
                                            self.update),
            switchboard.requestCallbackMain('new pixelinfo plugin',
                                            self.buildGUI),
            switchboard.requestCallbackMain((self.gfxwindow(),
                                             'layers changed'), self.update)
            ]


    def buildGUI(self):
        debug.mainthreadTest()
        self.table.resize(rows=4, columns=2)
        row = 4
        self.plugins = []
        for pluginclass in pixelinfoplugin.plugInClasses:
            self.table.resize(row + 1 + pluginclass.nrows, 2)
            # A gtk or pygtk bug requires xpadding to be set
            # explicitly if ypadding is set here.
            self.table.attach(gtk.HSeparator(), 0,2, row,row+1,
                              xoptions=gtk.EXPAND|gtk.FILL,
                              xpadding=0, ypadding=3)
            self.plugins.append(pluginclass(self, self.table, row+1))
            row += pluginclass.nrows+1

    def activate(self):
        if not self.active:
            toolboxGUI.GfxToolbox.activate(self)
            self.gfxwindow().setMouseHandler(self)
            self.gfxwindow().toolbar.setSelect()
            self.update()

    def deactivate(self):
        if self.active:
            toolboxGUI.GfxToolbox.deactivate(self)
            self.gfxwindow().removeMouseHandler()

    def close(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        for plugin in self.plugins:
            plugin.close()
        self.plugins = []

    def acceptEvent(self, eventtype):
        return eventtype == 'up'

    # It's possible to click on the background of the canvas, but
    # outside the image/microstructure.  In this case, do nothing --
    # the behavior is then the same as if you click outside the drawn
    # area.
    def up(self, x, y, shift, ctrl):
        msOrImage = self.gfxwindow().topmost('Microstructure', 'Image')
        if msOrImage:
            if config.dimension() == 3:
                canvas = self.toolbox.gfxwindow().oofcanvas
                view = canvas.get_view()
                pt = canvas.display2Physical(view, x, y)
                if pt is not None:
                    self.toolbox.menu.Query(point=pt, view=view)
            else:
                pt = primitives.iPoint(x, y)
                self.toolbox.menu.Query(point=pt)
            # p = self.gfxwindow().oofcanvas.screen_coords_to_3D_coords(x,y)
            # if p is not None:
            #     where = msOrImage.pixelFromPoint(
            #         primitives.Point(p[0],p[1],p[2]));
            #     if where is not None:
            #         self.toolbox.menu.Query(x=where[0], y=where[1], z=where[2])
        else:
            for plugin in self.plugins:
                plugin.nonsense();
            

    def currentPixel(self):
        return self.toolbox.currentPixel()
    
    def update(self):
        debug.mainthreadTest()
        self.xtsignal.block()
        self.ytsignal.block()
        self.ztsignal.block()
        try:
            where = self.currentPixel()

            if where is not None:
                self.clearbutton.set_sensitive(1)
            else:
                self.xtext.set_text('')
                self.ytext.set_text('')
                self.ztext.set_text('')
                self.clearbutton.set_sensitive(0)
                for plugin in self.plugins:
                    plugin.clear()

            msOrImage = self.gfxwindow().topmost('Microstructure', 'Image')
            if where is not None and msOrImage is not None:
                self.xtext.set_text(`where.x`)
                self.ytext.set_text(`where.y`)
                self.ztext.set_text(`where.z`)
                size = msOrImage.sizeInPixels()
                if where is not None:
                    for plugin in self.plugins:
                        plugin.update(where)
                else:
                    for plugin in self.plugins:
                        plugin.nonsense()
            else:
                for plugin in self.plugins:
                    plugin.nonsense()

                self.updatebutton.set_sensitive(0)
        finally:
            self.xtsignal.unblock()
            self.ytsignal.unblock()
            self.ztsignal.unblock()

        gtklogger.checkpoint(self.gfxwindow().name + " " +
                             self._name + " updated")

    def updateButtonCB(self, button):
        debug.mainthreadTest()
        self.updatebutton.set_sensitive(0)
        x = int(self.xtext.get_text())
        y = int(self.ytext.get_text())
        z = int(self.ztext.get_text())
        msOrImage = self.gfxwindow().topmost('Microstructure', 'Image')
        size = msOrImage.sizeInPixels()
        if x < 0 or x >= size.x or y < 0 or y >= size.y \
               or z < 0 or z >= size.z: # illegal point
            self.update()               # restore original values
            return
        self.toolbox.menu.QueryDirectly(voxel=primitives.iPoint(x, y, z))

    def clearButtonCB(self, button):
        self.toolbox.menu.Clear()

    def pointChanged(self, *args):
        debug.mainthreadTest()
        self.updatebutton.set_sensitive(1)

    def findMicrostructure(self):
        return self.toolbox.findMicrostructure()



def _makeGUI(self):
    return VoxelInfoToolboxGUI(self)

pixelinfo.PixelInfoToolbox.makeGUI = _makeGUI






