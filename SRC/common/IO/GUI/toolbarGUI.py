# -*- python -*-
# $RCSfile: toolbarGUI.py,v $
# $Revision: 1.3.10.30 $
# $Author: langer $
# $Date: 2014/07/31 18:32:50 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

import gobject
import gtk

from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common.IO import viewertoolbox
from ooflib.common.IO.GUI import chooser
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import gtkutils
from ooflib.common.IO.GUI import mousehandler
from ooflib.common.IO.GUI import tooltips


class ToolBar:
    def __init__(self, gfxwindow):
        self.gfxwindow = gfxwindow
        
        ## TODO 3.1: buttonrow should really have a gtklogger name
        ## assigned to it.  That would require all of the gui scripts
        ## to be updated.
        buttonrow = gtk.HBox()

        self.selectbutton = gtk.RadioButton(label='Select')
        buttonrow.pack_start(self.selectbutton, expand=0, fill=0)
        gtklogger.setWidgetName(self.selectbutton, 'select')
        gtklogger.connect(self.selectbutton, 'clicked', self.selectCB)
        tooltips.set_tooltip_text(
            self.selectbutton,
            "Click on the graphics window to select objects"
            " according to the current selection mode.")

        tumblebutton = gtk.RadioButton(label='Tumble', group=self.selectbutton)
        buttonrow.pack_start(tumblebutton, expand=0, fill=0)
        gtklogger.setWidgetName(tumblebutton, 'tumble')
        gtklogger.connect(tumblebutton, 'clicked', self.tumbleCB)
        tooltips.set_tooltip_text(
            tumblebutton,
            "Click and drag on the graphics window to rotate the view.")

        dollybutton = gtk.RadioButton(label='Dolly', group=self.selectbutton)
        buttonrow.pack_start(dollybutton, expand=0, fill=0)
        gtklogger.setWidgetName(dollybutton, 'dolly')
        gtklogger.connect(dollybutton, 'clicked', self.dollyCB)
        tooltips.set_tooltip_text(
            dollybutton,
            "Click and drag on the graphics window to move the viewpoint"
            " closer to or further from the displayed objects.")

        trackbutton = gtk.RadioButton(label='Track', group=self.selectbutton)
        buttonrow.pack_start(trackbutton, expand=0, fill=0)
        gtklogger.setWidgetName(trackbutton, 'track')
        gtklogger.connect(trackbutton, 'clicked', self.trackCB)
        tooltips.set_tooltip_text(
            trackbutton,
            "Click and drag on the graphics window to move the"
            " displayed objects.")
        
        self.fillbutton = gtk.Button("Fill")
        gtklogger.setWidgetName(self.fillbutton, "fill")
        buttonrow.pack_start(self.fillbutton, expand=0, fill=0)
        tooltips.set_tooltip_text(
            self.fillbutton,
            "Dolly in or out such that visible objects approximately"
            " fill the viewport")
        gtklogger.connect(self.fillbutton, "clicked", self.fillCB)


        viewbox = gtk.HBox()
        buttonrow.pack_end(viewbox, expand=0, fill=0)

        self.prevButton = gtkutils.StockButton(gtk.STOCK_GO_BACK)
        viewbox.pack_start(self.prevButton, expand=0, fill=0)
        gtklogger.setWidgetName(self.prevButton, "PrevView")
        gtklogger.connect(self.prevButton, 'clicked', self.prevViewCB)
        tooltips.set_tooltip_text(self.prevButton, 
                                  "Reinstate the previous view.")

        self.viewChooser = chooser.ChooserWidget(viewertoolbox.viewNames(),
                                                 callback=self.setView,
                                                 name="viewChooser")
        viewbox.pack_start(self.viewChooser.gtk, expand=0, fill=0)
        self.gfxwindow.addSwitchboardCallback(
            switchboard.requestCallbackMain("view changed", self.viewChangedCB),
            switchboard.requestCallbackMain("view restored", self.viewChangedCB)
        )

        self.nextButton = gtkutils.StockButton(gtk.STOCK_GO_FORWARD)
        viewbox.pack_start(self.nextButton, expand=0, fill=0)
        gtklogger.setWidgetName(self.nextButton, "NextView")
        gtklogger.connect(self.nextButton, 'clicked', self.nextViewCB)
        tooltips.set_tooltip_text(self.nextButton, "Reinstate the next view.")

        # TODO 3.1: more useful things in the toolbar?
        self.gtk = buttonrow

        self.tumbleHandler = TumbleMouseHandler(gfxwindow)
        self.dollyHandler = DollyMouseHandler(gfxwindow)
        self.trackHandler = TrackMouseHandler(gfxwindow)

    def setSelect(self):
        self.selectbutton.set_active(True)

    def selectCB(self, button):
        if button.get_active():
            self.gfxwindow.current_toolbox.activate()
        else:
            # TODO 3.1: Is this necessary?  It doesn't seem to be
            # harmful.
            self.gfxwindow.current_toolbox.deactivate()

    def tumbleCB(self, button):
        if button.get_active():
            self.gfxwindow.setMouseHandler(self.tumbleHandler)

    def dollyCB(self, button):
        if button.get_active():
            self.gfxwindow.setMouseHandler(self.dollyHandler)

    def trackCB(self, button):
        if button.get_active():
            self.gfxwindow.setMouseHandler(self.trackHandler)

    def fillCB(self, *args):
        self.gfxwindow.oofcanvas.dolly_fill()
        # self.gfxwindow.oofcanvas.set_sample_distances()
        self.gfxwindow.updateview()

    def setView(self, *args):   # view chooser callback
        viewname = self.viewChooser.get_value()
        vtb = self.gfxwindow.getToolboxByName("Viewer")
        vtb.setView(viewname)

    # switchboard "view changed" or "view restored"
    def viewChangedCB(self, gfxwindow):
        if gfxwindow == self.gfxwindow:
            name, names = viewertoolbox.retrieveViewNames(gfxwindow)
            self.viewChooser.update(names)
            self.viewChooser.set_state(name)

    def prevViewCB(self, *args):
        vtb = self.gfxwindow.getToolboxGUIByName("Viewer")
        vtb.historian.prevCB()

    def nextViewCB(self, *args):
        vtb = self.gfxwindow.getToolboxGUIByName("Viewer")
        vtb.historian.nextCB()

    def sensitize(self, vtb):
        # called from ViewerToolBox3DGUI.sensitize()
        self.prevButton.set_sensitive(vtb.historian.prevSensitive())
        self.nextButton.set_sensitive(vtb.historian.nextSensitive())

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class ViewManipulatorMouseHandler(mousehandler.MouseHandler):
    def __init__(self, gfxwindow):
        self.gfxwindow = gfxwindow
        self.downed = False

    def up(self, x, y, shift, ctrl):
        self.downed = False
        # The View menuitem callback is viewCB in gfxwindow3d.py.
        # There's also a no-op stub in ghostgfxwindow.py.
        self.gfxwindow.menu.Settings.Camera.View(
            view=self.gfxwindow.oofcanvas.get_view())

    def down(self, x, y, shift, ctrl):
        self.downed = True

    def acceptEvent(self, eventtype):
        return (eventtype == 'down' or 
               (self.downed and eventtype in ('move', 'up')))


class TumbleMouseHandler(ViewManipulatorMouseHandler):
    def move(self, x, y, shift, ctrl):
        self.gfxwindow.oofcanvas.mouse_tumble(x,y)
        self.gfxwindow.updateview()


class DollyMouseHandler(ViewManipulatorMouseHandler):
    def move(self, x, y, shift, ctrl):
        self.gfxwindow.oofcanvas.mouse_dolly(x,y)
        self.gfxwindow.updateview()

    def up(self, x, y, shift, ctrl):
        # self.gfxwindow.oofcanvas.set_sample_distances()
        ViewManipulatorMouseHandler.up(self,x,y,shift,ctrl)
        

class TrackMouseHandler(ViewManipulatorMouseHandler):
    def move(self, x, y, shift, ctrl):
        self.gfxwindow.oofcanvas.mouse_track(x,y)
        self.gfxwindow.updateview()






