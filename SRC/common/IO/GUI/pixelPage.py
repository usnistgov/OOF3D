# -*- python -*-
# $RCSfile: pixelPage.py,v $
# $Revision: 1.39.10.4 $
# $Author: langer $
# $Date: 2013/11/15 22:03:17 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# GUI page for manipulating pixel selections.

from ooflib.SWIG.common import config
from ooflib.SWIG.common import switchboard
from ooflib.common import utils
from ooflib.common import subthread
from ooflib.common import mainthread
from ooflib.common import debug
from ooflib.common import microstructure
from ooflib.common import pixelselectionmod
from ooflib.common.IO import mainmenu
from ooflib.common.IO.GUI import fixedwidthtext
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import gtkutils
from ooflib.common.IO.GUI import historian
from ooflib.common.IO.GUI import oofGUI
from ooflib.common.IO.GUI import regclassfactory
from ooflib.common.IO.GUI import tooltips
from ooflib.common.IO.GUI import whowidget
import gtk

if config.dimension()==2:
    pixstring = "pixel"
    Pixstring = "Pixel"
elif config.dimension()==3:
    pixstring = "voxel"
    Pixstring = "Voxel"

class SelectionPage(oofGUI.MainPage):
    # Pixel selection manipulation
    def __init__(self):
        debug.mainthreadTest()
        oofGUI.MainPage.__init__(
            self,
            name="%s Selection"%Pixstring, ordering=71,
            tip="Modify the set of selected %ss."%pixstring)

        mainbox = gtk.VBox(spacing=2)
        self.gtk.add(mainbox)

        # Microstructure widget, centered at the top of the page.
        align = gtk.Alignment(xalign=0.5)
        mainbox.pack_start(align, expand=0, fill=0)
        centerbox = gtk.HBox(spacing=3)
        align.add(centerbox)
        label = gtk.Label('Microstructure=')
        label.set_alignment(1.0, 0.5)
        centerbox.pack_start(label, expand=0, fill=0)
        self.mswidget = whowidget.WhoWidget(microstructure.microStructures,
                                            scope=self)
        centerbox.pack_start(self.mswidget.gtk[0], expand=0, fill=0)
        
        mainpane = gtk.HPaned()
        gtklogger.setWidgetName(mainpane, 'Pane')
        mainbox.pack_start(mainpane, expand=1, fill=1)
        gtklogger.connect_passive(mainpane, 'notify::position')

        # Pixel selection status in the left half of the main pane
        pssframe = gtk.Frame( "%s Selection Status"%Pixstring)
        pssframe.set_shadow_type(gtk.SHADOW_IN)
        mainpane.pack1(pssframe, resize=1, shrink=0)
        self.datascroll = gtk.ScrolledWindow()
        gtklogger.logScrollBars(self.datascroll, "DataScroll")
        pssframe.add(self.datascroll)
        self.datascroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.psdata = fixedwidthtext.FixedWidthTextView()
        gtklogger.setWidgetName(self.psdata, 'DataView')
        self.psdata.set_editable(0)
        self.psdata.set_cursor_visible(False)
        self.psdata.set_wrap_mode(gtk.WRAP_WORD)
        self.datascroll.add_with_viewport(self.psdata)

        # Selection method in the right half of the main pane
        modframe = gtk.Frame("%s Selection Modification"%Pixstring)
        gtklogger.setWidgetName(modframe, "SelectionModification")
        modframe.set_shadow_type(gtk.SHADOW_IN)
        mainpane.pack2(modframe, resize=0, shrink=0)
        vbox = gtk.VBox()
        modframe.add(vbox)
##        scroll = gtk.ScrolledWindow()
##        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
##        vbox.add(scroll)
        self.selectionModFactory = regclassfactory.RegisteredClassFactory(
            pixelselectionmod.SelectionModifier.registry, title="Method:",
            scope=self, name="Method")
        vbox.pack_start(self.selectionModFactory.gtk, expand=1, fill=1)
##        scroll.add_with_viewport(self.selectionModFactory.gtk)
        self.historian = historian.Historian(self.selectionModFactory.set,
                                             self.sensitizeHistory,
                                             setCBkwargs={'interactive':1})
        self.selectionModFactory.set_callback(self.historian.stateChangeCB)
        
        # Prev, OK, and Next buttons
        hbox = gtk.HBox()
        vbox.pack_start(hbox, expand=0, fill=0, padding=2)
        self.prevmethodbutton = gtkutils.prevButton()
        gtklogger.connect(self.prevmethodbutton, 'clicked',
                          self.historian.prevCB)
        hbox.pack_start(self.prevmethodbutton, expand=0, fill=0, padding=2)
        tooltips.set_tooltip_text(self.prevmethodbutton,
                     'Recall the previous selection modification operation.')
        self.okbutton = gtk.Button(stock=gtk.STOCK_OK)
        gtklogger.setWidgetName(self.okbutton, "OK")
        hbox.pack_start(self.okbutton, expand=1, fill=1, padding=2)
        gtklogger.connect(self.okbutton, 'clicked', self.okbuttonCB)
        tooltips.set_tooltip_text(self.okbutton,
              'Perform the selection modification operation defined above.')
        self.nextmethodbutton = gtkutils.nextButton()
        gtklogger.connect(self.nextmethodbutton, 'clicked',
                          self.historian.nextCB)
        hbox.pack_start(self.nextmethodbutton, expand=0, fill=0, padding=2)
        tooltips.set_tooltip_text(self.nextmethodbutton,
                        "Recall the next selection modification operation.")

        # Undo, Redo, and Clear buttons
        hbox = gtk.HBox()
        vbox.pack_start(hbox, expand=0, fill=0, padding=2)
        self.undobutton = gtk.Button(stock=gtk.STOCK_UNDO)
        self.redobutton = gtk.Button(stock=gtk.STOCK_REDO)
        hbox.pack_start(self.undobutton, expand=1, fill=0)
        hbox.pack_start(self.redobutton, expand=1, fill=0)
        gtklogger.setWidgetName(self.undobutton, "Undo")
        gtklogger.setWidgetName(self.redobutton, "Redo")
        gtklogger.connect(self.undobutton, 'clicked', self.undoCB)
        gtklogger.connect(self.redobutton, 'clicked', self.redoCB)
        tooltips.set_tooltip_text(
            self.undobutton,
            "Undo the previous %s selection operation."%pixstring)
        tooltips.set_tooltip_text(
            self.redobutton,
            "Redo an undone %s selection operation."%pixstring)
        self.clearbutton = gtk.Button(stock=gtk.STOCK_CLEAR)
        hbox.pack_start(self.clearbutton, expand=1, fill=0)
        gtklogger.setWidgetName(self.clearbutton, "Clear")
        gtklogger.connect(self.clearbutton, 'clicked', self.clearCB)
        tooltips.set_tooltip_text(self.clearbutton,
                                  "Unselect all %ss."%pixstring)

        self.sbcallbacks = [
            switchboard.requestCallbackMain(self.mswidget,
                                            self.mswidgetCB),
            switchboard.requestCallbackMain('pixel selection changed',
                                            self.selectionChanged),
            switchboard.requestCallbackMain('modified pixel selection',
                                            self.updateHistory),
            switchboard.requestCallbackMain(
                pixelselectionmod.SelectionModifier,
                self.updateSelectionModifiers),
            switchboard.requestCallbackMain(('validity',
                                             self.selectionModFactory),
                                            self.validityChangeCB),
            switchboard.requestCallbackMain("made reservation",
                                            self.reservationCB),
            switchboard.requestCallbackMain("cancelled reservation",
                                            self.reservationCB)
            ]

        self.updatePSInfo()
        self.sensitize()
        self.sensitizeHistory()

    def selectionChanged(self, who): # switchboard 'pixel selection changed'
        self.sensitize()
        self.updatePSInfo()
        
    def validityChangeCB(self, validity):
        self.sensitize()

    def reservationCB(self, context):
        if context is self.getSelectionContext()[1]:
            self.sensitize()

    def getCurrentMSName(self):
        return self.mswidget.get_value()
    
    def getCurrentMS(self):
        try:
            return microstructure.microStructures[self.getCurrentMSName()]
        except KeyError:
            pass
    def getSelectionContext(self):
        ms = self.getCurrentMS()
        if ms:
            return (ms, ms.getSelectionContext())
        return (None, None)
    
    def mswidgetCB(self, *args, **kwargs):
        self.updatePSInfo()
        self.sensitize()



    def updatePSInfo(self):
        debug.mainthreadTest()
        subthread.execute(self.updatePSInfo_subthread)

    def updatePSInfo_subthread(self):
        (ms, selection) = mainthread.runBlock(self.getSelectionContext)
        if selection is not None:
            selection.begin_reading()
            try:
                pssize = selection.size()
            finally:
                selection.end_reading()
            mssize = ms.getObject().sizeInPixels()
            if config.dimension() == 2:
                msg = "%d of %d pixels selected" % (pssize, mssize[0]*mssize[1])
            elif config.dimension() == 3:
                msg = "%d of %d voxels selected" % (pssize, mssize[0]*mssize[1]*mssize[2])
        else:
            msg = "No Microstructure selected."
        mainthread.runBlock(self.psdata.get_buffer().set_text, (msg,))
        gtklogger.checkpoint("pixel page updated")

    def sensitize(self):
        debug.mainthreadTest()
        subthread.execute(self.sensitize_subthread)

    def sensitize_subthread(self):

        def set_button_sensitivity(u, r, c):
            self.undobutton.set_sensitive(u)
            self.redobutton.set_sensitive(r)
            self.clearbutton.set_sensitive(c)

        def set_ok_sensitivity(selection):
            ok =  (selection is not None
                   and not selection.query_reservation()
                   and self.selectionModFactory.isValid())
            self.okbutton.set_sensitive(ok)

        (ms, selection) = mainthread.runBlock(self.getSelectionContext)
        if selection is not None:
            available = not selection.query_reservation()
            selection.begin_reading()
            try:
                u = available and selection.undoable()
                r = available and selection.redoable()
                c = available and selection.clearable()
            finally:
                selection.end_reading()
        else:
            (u,r,c) = (0,0,0)
        mainthread.runBlock(set_button_sensitivity, (u,r,c))
        mainthread.runBlock(set_ok_sensitivity, (selection,) )
        


    def updateSelectionModifiers(self): # SB: New selection modifier created
        self.selectionModFactory.update(
            pixelselectionmod.SelectionModifier.registry)

    def sensitizeHistory(self):
        debug.mainthreadTest()
        self.nextmethodbutton.set_sensitive(self.historian.nextSensitive())
        self.prevmethodbutton.set_sensitive(self.historian.prevSensitive())

    def updateHistory(self, selectionModifier): # sb 'modified pixel selection'
        if selectionModifier is not None:
            self.historian.record(selectionModifier)

    def undoCB(self, button):
        mainmenu.OOF.PixelSelection.Undo(microstructure=self.getCurrentMSName())
    def redoCB(self, button):
        mainmenu.OOF.PixelSelection.Redo(microstructure=self.getCurrentMSName())
    def clearCB(self, button):
        mainmenu.OOF.PixelSelection.Clear(
            microstructure=self.getCurrentMSName())

    def okbuttonCB(self, *args):
        # Actually perform the current selection modification operation.
        modmeth = self.selectionModFactory.getRegistration()
        if modmeth is not None:
            # Copy parameters from widgets to the registration.
            self.selectionModFactory.set_defaults()
            # Invoke the method by calling the corresponding menu
            # item.  The menu item and method registration share a
            # parameter list.
            menuitem = getattr(mainmenu.OOF.PixelSelection,
                               utils.space2underscore(modmeth.name()))
            menuitem.callWithDefaults(microstructure=self.getCurrentMSName())

####################################
        
sp = SelectionPage()
