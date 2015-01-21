# $RCSfile: activeareaPage.py,v $
# $Revision: 1.31.18.4 $
# $Author: langer $
# $Date: 2013/11/15 22:03:17 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

# GUI page for manipulating pixel groups.

from ooflib.SWIG.common import config
from ooflib.SWIG.common import switchboard
from ooflib.common import activeareamod
from ooflib.common import debug
from ooflib.SWIG.common import guitop
from ooflib.common import mainthread
from ooflib.common import microstructure
from ooflib.common import utils
from ooflib.common.IO import mainmenu
from ooflib.common.IO import reporter
from ooflib.common.IO.GUI import chooser
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import gtkutils
from ooflib.common.IO.GUI import historian
from ooflib.common.IO.GUI import oofGUI
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import regclassfactory
from ooflib.common.IO.GUI import tooltips
from ooflib.common.IO.GUI import whowidget
import gtk

if config.dimension()==2:
    spacestring = "area"
    Spacestring = "Area"
elif config.dimension()==3:
    spacestring = "volume"
    Spacestring = "Volume"    

class ActiveAreaPage(oofGUI.MainPage):
    def __init__(self):
        self.built = False
        oofGUI.MainPage.__init__(self, name="Active %s"%Spacestring,
                                 ordering=71.1,
                                 tip="Modify active %s."%spacestring)

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

        # Active area status in the left half of the main pane.
        vbox = gtk.VBox()
        mainpane.pack1(vbox, resize=1, shrink=0)
        aasframe = gtk.Frame("Active %s Status"%Spacestring)
        aasframe.set_shadow_type(gtk.SHADOW_IN)
        vbox.pack_start(aasframe, expand=0, fill=0, padding=2)
        self.aainfo = gtk.Label()
        gtklogger.setWidgetName(self.aainfo, "Status")
##        self.aainfo.set_alignment(0.0, 0.5)
        aasframe.add(self.aainfo)

        naaframe = gtk.Frame("Named Active %ss"%Spacestring)
        naaframe.set_shadow_type(gtk.SHADOW_IN)
        vbox.pack_start(naaframe, expand=1, fill=1)
        naabox = gtk.VBox()
        naaframe.add(naabox)
        self.aalist = chooser.ScrolledChooserListWidget(
            callback=self.aalistCB, dbcallback=self.aalistCB2,
            name="NamedAreas")
        naabox.pack_start(self.aalist.gtk, expand=1, fill=1, padding=2)
        bbox = gtk.HBox()
        naabox.pack_start(bbox, expand=0, fill=0, padding=2)
        self.storebutton = gtk.Button("Store...")
        bbox.pack_start(self.storebutton, expand=1, fill=0)
        gtklogger.setWidgetName(self.storebutton, "Store")
        gtklogger.connect(self.storebutton, 'clicked', self.storeCB)
        tooltips.set_tooltip_text(
            self.storebutton,
            "Save the current active %s for future use."%spacestring)
        self.renamebutton = gtk.Button("Rename...")
        bbox.pack_start(self.renamebutton, expand=1, fill=0)
        gtklogger.setWidgetName(self.renamebutton, "Rename")
        gtklogger.connect(self.renamebutton, 'clicked', self.renameCB)
        tooltips.set_tooltip_text(self.renamebutton,
                             "Rename the selected saved active %s."%spacestring)
        self.deletebutton = gtk.Button("Delete")
        bbox.pack_start(self.deletebutton, expand=1, fill=0)
        gtklogger.setWidgetName(self.deletebutton, "Delete")
        gtklogger.connect(self.deletebutton, 'clicked', self.deleteCB)
        tooltips.set_tooltip_text(self.deletebutton,
                             "Delete the selected saved active %s."%spacestring)
        self.restorebutton = gtk.Button("Restore")
        bbox.pack_start(self.restorebutton, expand=1, fill=0)
        gtklogger.setWidgetName(self.restorebutton, "Restore")
        gtklogger.connect(self.restorebutton, 'clicked', self.restoreCB)
        tooltips.set_tooltip_text(self.restorebutton,
                             "Use the selected saved active %s."%spacestring)
        
        # Active area modification methods in the right half of the main pane
        modframe = gtk.Frame("Active %s Modification"%Spacestring)
        gtklogger.setWidgetName(modframe, "Modify")
        modframe.set_shadow_type(gtk.SHADOW_IN)
        mainpane.pack2(modframe, resize=0, shrink=0)
        modbox = gtk.VBox()
        modframe.add(modbox)
##        scroll = gtk.ScrolledWindow()
##        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
##        modbox.pack_start(scroll, expand=1, fill=1)
        self.activeareaModFactory = regclassfactory.RegisteredClassFactory(
            activeareamod.ActiveAreaModifier.registry, title="Method:",
            scope=self, name="Method")
##        scroll.add_with_viewport(self.activeareaModFactory.gtk)
        modbox.pack_start(self.activeareaModFactory.gtk, expand=1, fill=1)
        self.historian = historian.Historian(self.activeareaModFactory.set,
                                             self.sensitizeHistory,
                                             setCBkwargs={'interactive':1})
        self.activeareaModFactory.set_callback(self.historian.stateChangeCB)

        # Prev, OK, and Next buttons
        hbox = gtk.HBox()
        modbox.pack_start(hbox, expand=0, fill=0, padding=2)
        self.prevbutton = gtkutils.prevButton()
        hbox.pack_start(self.prevbutton, expand=0, fill=0, padding=2)
        gtklogger.connect(self.prevbutton, 'clicked', self.historian.prevCB)
        tooltips.set_tooltip_text(
            self.prevbutton,
            'Recall the previous active %s modification operation.'%spacestring)
        self.okbutton = gtk.Button(stock=gtk.STOCK_OK)
        hbox.pack_start(self.okbutton, expand=1, fill=1, padding=2)
        gtklogger.setWidgetName(self.okbutton, "OK")
        gtklogger.connect(self.okbutton, 'clicked', self.okbuttonCB)
        tooltips.set_tooltip_text(
            self.okbutton,
            'Perform the active %s modification operation defined above.'
            %spacestring)
        self.nextbutton = gtkutils.nextButton()
        hbox.pack_start(self.nextbutton, expand=0, fill=0, padding=2)
        gtklogger.connect(self.nextbutton, 'clicked', self.historian.nextCB)
        tooltips.set_tooltip_text(
            self.nextbutton,
            "Recall the next active %s modification operation."%spacestring)

        # Undo, Redo, Override
        hbox = gtk.HBox()
        modbox.pack_start(hbox, expand=0, fill=0, padding=2)
        self.undobutton = gtk.Button(stock=gtk.STOCK_UNDO)
        hbox.pack_start(self.undobutton, expand=1, fill=0)
        gtklogger.setWidgetName(self.undobutton, "Undo")
        gtklogger.connect(self.undobutton, 'clicked', self.undoCB)
        tooltips.set_tooltip_text(self.undobutton,
                                  "Undo the previous operation.")

        self.redobutton = gtk.Button(stock=gtk.STOCK_REDO)
        hbox.pack_start(self.redobutton, expand=1, fill=0)
        gtklogger.setWidgetName(self.redobutton, "Redo")
        gtklogger.connect(self.redobutton, 'clicked', self.redoCB)
        tooltips.set_tooltip_text(self.redobutton, "Redo an undone operation.")

        self.overridebutton = gtk.ToggleButton('Override')
        hbox.pack_start(self.overridebutton, expand=1, fill=0)
        gtklogger.setWidgetName(self.overridebutton, "Override")
        self.overridesignal = gtklogger.connect(self.overridebutton,
                                               'clicked', self.overrideCB)
        tooltips.set_tooltip_text(self.overridebutton,
                             "Temporarily activate the entire microstructure.")

        # Switchboard signals
        self.sbcallbacks = [
            switchboard.requestCallback(self.mswidget,
                                        self.mswidgetCB),
            switchboard.requestCallback("active area modified",
                                        self.aamodified),
            switchboard.requestCallbackMain("stored active areas changed",
                                            self.storedAAChanged),
            switchboard.requestCallbackMain(('validity',
                                             self.activeareaModFactory),
                                            self.validityChangeCB)
            ]

        self.built = True

    def installed(self):
        self.sensitize()
        self.sensitizeHistory()
        
    def getCurrentMSName(self):
        return self.mswidget.get_value()
    def getCurrentMS(self):
        try:
            return microstructure.microStructures[self.getCurrentMSName()]
        except KeyError:
            pass
    def getCurrentActiveArea(self):
        return self.aalist.get_value()

    # Callback functions for active area modification

    def okbuttonCB(self, button):
        modmeth = self.activeareaModFactory.getRegistration()
        if modmeth is not None:
            self.activeareaModFactory.set_defaults()
            menuitem = getattr(mainmenu.OOF.ActiveArea,
                               utils.space2underscore(modmeth.name()))
            menuitem.callWithDefaults(microstructure=self.getCurrentMSName())

    def undoCB(self, button):
        mainmenu.OOF.ActiveArea.Undo.callWithDefaults(
            microstructure=self.getCurrentMSName())

    def redoCB(self, button):
        mainmenu.OOF.ActiveArea.Redo.callWithDefaults(
            microstructure=self.getCurrentMSName())

    def overrideCB(self, button):
        mainmenu.OOF.ActiveArea.Override(microstructure=self.getCurrentMSName(),
                                         override=button.get_active())
        
    def mswidgetCB(self, *args, **kwargs): # switchboard self.mswidget
        # called only on a subthread
        self.updateAAInfo()
        mainthread.runBlock(self.updateAAList)
        self.sensitize()
        self.setOverrideButton()

    def aalistCB(self, name, interactive): # activearealist callback
        if self.built:
            self.sensitize()

    def aalistCB2(self, name):          # activearealist double-click callback
        self.sensitize()
        self.restoreCB(None)
        
    def storeCB(self, button):
        menuitem = mainmenu.OOF.ActiveArea.Store
        if parameterwidgets.getParameters(menuitem.get_arg('name'),
                                          title="Store the active area"):
            menuitem.callWithDefaults(microstructure=self.getCurrentMSName())

    def renameCB(self, button):
        menuitem = mainmenu.OOF.ActiveArea.Rename
        namearg = menuitem.get_arg('newname')
        namearg.value = self.getCurrentActiveArea()
        oldname = self.getCurrentActiveArea()
        if parameterwidgets.getParameters(menuitem.get_arg('newname'),
                                          title="Rename active%s '%s'"
                                               % (spacestring,oldname)):
            menuitem.callWithDefaults(microstructure=self.getCurrentMSName(),
                                      oldname=oldname)

    def deleteCB(self, button):
        if reporter.query("Really delete %s?" % self.getCurrentActiveArea(),
                          "No", default="Yes") == "Yes":
            mainmenu.OOF.ActiveArea.Delete(
                microstructure=self.getCurrentMSName(),
                name=self.getCurrentActiveArea())

    def restoreCB(self, button):
        mainmenu.OOF.ActiveArea.Restore(microstructure=self.getCurrentMSName(),
                               name=self.getCurrentActiveArea())
        

    def aamodified(self, modifier):
        # callback for switchboard signal "active area modified"
        # called only on a subthread
        self.updateAAInfo()
        self.updateHistory(modifier)
        self.sensitize()
        self.setOverrideButton()

    def storedAAChanged(self, name):
        # callback for switchboard signal "stored active areas changed"
        # called only on the main thread
        debug.mainthreadTest()
        self.updateAAList()
        try:
            self.aalist.set_selection(name)
        except KeyError:
            pass
        self.sensitize()

    def updateAAList(self):             # update list of named active areas
        debug.mainthreadTest()
        ms = self.getCurrentMS()
        if ms is not None:
            self.aalist.update(ms.getObject().activeAreaNames())
        else:
            self.aalist.update([])

    def updateAAInfo(self):             # must be called on subthread
        debug.subthreadTest()
        ms = self.getCurrentMS()
        if ms is not None:
            activearea = ms.getObject().activearea
            activearea.begin_reading()
            try:
                aasize = activearea.size()
                mssize = ms.getObject().sizeInPixels()
                if config.dimension()==2:
                    mpxls = mssize[0] * mssize[1]
                    pixstring="pixels"
                elif config.dimension()==3:
                    mpxls = mssize[0] * mssize[1] * mssize[2]
                    pixstring="voxels"
                apxls = mpxls - aasize
                if ms.getObject().activearea.getOverride():
                    msg = "OVERRIDE: all %d %s are active" % (mpxls, pixstring)
                else:
                    msg = "%d of %d %s are active" % (apxls, mpxls, pixstring)
            finally:
                activearea.end_reading()
        else:
            msg = "No Microstructure selected"
        mainthread.runBlock(self.aainfo.set_text, (msg,))
        gtklogger.checkpoint("active area status updated")

    def setOverrideButton(self):
        mainthread.runBlock(self.setOverrideButton_thread)
    def setOverrideButton_thread(self):
        ms = self.getCurrentMS()
        if ms is not None:
            self.overridesignal.block()
            self.overridebutton.set_active(
                ms.getObject().activearea.getOverride())
            self.overridesignal.unblock()

    def updateHistory(self, activeareaModifier):
        if activeareaModifier is not None:
            self.historian.record(activeareaModifier)
            
    def sensitize(self):
        mainthread.runBlock(self.sensitize_thread)
    def sensitize_thread(self):
        debug.mainthreadTest()
        ms = self.getCurrentMS()
        if ms is not None:
            activearea = ms.getObject().activearea
            self.undobutton.set_sensitive(activearea.undoable())
            self.redobutton.set_sensitive(activearea.redoable())
            self.overridebutton.set_sensitive(1)
            self.okbutton.set_sensitive(self.activeareaModFactory.isValid())
            self.storebutton.set_sensitive(1)
            aachosen = self.aalist.get_value() is not None
            self.restorebutton.set_sensitive(aachosen)
            self.deletebutton.set_sensitive(aachosen)
            self.renamebutton.set_sensitive(aachosen)
        else:
            self.undobutton.set_sensitive(0)
            self.redobutton.set_sensitive(0)
            self.overridebutton.set_sensitive(0)
            self.okbutton.set_sensitive(0)
            self.storebutton.set_sensitive(0)
            self.restorebutton.set_sensitive(0)
            self.deletebutton.set_sensitive(0)
            self.renamebutton.set_sensitive(0)

    def sensitizeHistory(self):
        debug.mainthreadTest()
        self.nextbutton.set_sensitive(self.historian.nextSensitive())
        self.prevbutton.set_sensitive(self.historian.prevSensitive())

    def validityChangeCB(self, validity):
        # called only on the main thread
        self.sensitize_thread()

####################################
        
aap = ActiveAreaPage()
