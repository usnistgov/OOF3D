# -*- python -*-
# $RCSfile: pinnodesPage.py,v $
# $Revision: 1.20.10.9 $
# $Author: langer $
# $Date: 2013/11/08 22:06:53 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import utils
from ooflib.common.IO import mainmenu
from ooflib.common.IO import whoville
from ooflib.common.IO.GUI import fixedwidthtext
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import oofGUI
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import regclassfactory
from ooflib.common.IO.GUI import tooltips
from ooflib.common.IO.GUI import whowidget
from ooflib.engine import pinnodesmodifier
from ooflib.engine import skeletoncontext
import gtk

class PinNodesPage(oofGUI.MainPage):
    def __init__(self):
        oofGUI.MainPage.__init__(self, name="Pin Nodes", ordering=120.1,
                                 tip='Pin and unpin nodes')

        mainbox = gtk.VBox(spacing=2)
        self.gtk.add(mainbox)

        align = gtk.Alignment(xalign=0.5)
        mainbox.pack_start(align, expand=0, fill=0)
        centerbox = gtk.HBox(spacing=3)
        align.add(centerbox)
        self.skelwidget = whowidget.WhoWidget(whoville.getClass('Skeleton'),
                                              callback=self.select_skeletonCB)
        label = gtk.Label('Microstructure=')
        label.set_alignment(1.0, 0.5)
        centerbox.pack_start(label, expand=0, fill=0)
        centerbox.pack_start(self.skelwidget.gtk[0], expand=0, fill=0)
        label = gtk.Label('Skeleton=')
        label.set_alignment(1.0, 0.5)
        centerbox.pack_start(label, expand=0, fill=0)
        centerbox.pack_start(self.skelwidget.gtk[1], expand=0, fill=0)

        mainpane = gtk.HPaned()
        gtklogger.setWidgetName(mainpane, 'Pane')
        mainbox.pack_start(mainpane, expand=1, fill=1)
        gtklogger.connect_passive(mainpane, 'notify::position')

        # Pinned nodes status in the left half of the main pane
        pnsframe = gtk.Frame("Pinned Nodes Status")
        pnsframe.set_shadow_type(gtk.SHADOW_IN)
        self.datascroll = gtk.ScrolledWindow()
        gtklogger.logScrollBars(self.datascroll, "StatusScroll")
        pnsframe.add(self.datascroll)
        self.datascroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.psdata = fixedwidthtext.FixedWidthTextView()
        self.psdata.set_editable(False)
        self.psdata.set_wrap_mode(gtk.WRAP_WORD)
        self.psdata.set_cursor_visible(False)
        self.datascroll.add_with_viewport(self.psdata)
        mainpane.pack1(pnsframe, resize=1, shrink=0)
        
        # Pin nodes method
        modframe = gtk.Frame("Pin Nodes Methods")
        gtklogger.setWidgetName(modframe, 'Modify')
        modframe.set_shadow_type(gtk.SHADOW_IN)
        modbox = gtk.VBox()  # will have "methods" and "buttons"
        modframe.add(modbox)
        self.pinModFactory = regclassfactory.RegisteredClassFactory(
            pinnodesmodifier.PinNodesModifier.registry,
            title="Method:", scope=self, name="Method")
        modbox.pack_start(self.pinModFactory.gtk, expand=1, fill=1, padding=2)

        # buttons
        hbox1 = gtk.HBox()
        modbox.pack_start(hbox1, expand=0, fill=0, padding=2)
        self.okbutton = gtk.Button(stock=gtk.STOCK_OK)
        gtklogger.setWidgetName(self.okbutton, 'OK')
        gtklogger.connect(self.okbutton, "clicked", self.okCB)
        tooltips.set_tooltip_text(self.okbutton,"Pin nodes with the selected method.")
        self.undobutton = gtk.Button(stock=gtk.STOCK_UNDO)
        gtklogger.setWidgetName(self.undobutton, 'Undo')
        gtklogger.connect(self.undobutton, "clicked", self.undoCB)
        tooltips.set_tooltip_text(self.undobutton,"Undo the latest action.")
        self.redobutton = gtk.Button(stock=gtk.STOCK_REDO)
        gtklogger.setWidgetName(self.redobutton, 'Redo')
        gtklogger.connect(self.redobutton, "clicked", self.redoCB)
        tooltips.set_tooltip_text(self.redobutton,"Redo the latest undone action.")
        hbox1.pack_start(self.undobutton, expand=0, fill=1, padding=2)
        hbox1.pack_start(self.okbutton, expand=1, fill=1, padding=2)
        hbox1.pack_end(self.redobutton, expand=0, fill=1, padding=2)

        hbox2 = gtk.HBox(homogeneous=1)
        modbox.pack_start(hbox2, expand=0, fill=0, padding=2)
        self.unpinallbutton = gtk.Button("Unpin All")
        gtklogger.setWidgetName(self.unpinallbutton, 'Unpin All')
        gtklogger.connect(self.unpinallbutton, "clicked", self.unpinallCB)
        tooltips.set_tooltip_text(self.unpinallbutton,"Unpin all the pinned nodes.")
        self.invertbutton = gtk.Button("Invert")
        gtklogger.setWidgetName(self.invertbutton, 'Invert')
        gtklogger.connect(self.invertbutton, "clicked", self.invertCB)
        tooltips.set_tooltip_text(self.invertbutton,"Invert - pin the unpinned and unpin the pinned.")
        hbox2.pack_start(self.unpinallbutton, expand=1, fill=1, padding=2)
        hbox2.pack_start(self.invertbutton, expand=1, fill=1, padding=2)
        
        mainpane.pack2(modframe, resize=0, shrink=0)

        # Switchboard callbacks
        switchboard.requestCallbackMain(('who changed', 'Skeleton'),
                                        self.changeSkeleton)
        switchboard.requestCallbackMain(('new who', 'Microstructure'),
                                        self.newMS)
        switchboard.requestCallbackMain("new pinned nodes",
                                        self.newNodesPinned)
        switchboard.requestCallbackMain(self.skelwidget,
                                        self.skel_update)
        switchboard.requestCallbackMain("made reservation",
                                        self.reservationChanged)
        switchboard.requestCallbackMain("cancelled reservation",
                                        self.reservationChanged)

    def installed(self):
        self.sensitize()

    # Switchboard callbacks
    def changeSkeleton(self, skelcontext):
        if skelcontext is self.currentSkelContext():
            self.update()

    def newMS(self, msname):
        if not self.currentSkelName():
            self.skelwidget.set_value(msname)

    def newNodesPinned(self, skelcontext):
        if self.currentSkelContext() is skelcontext:
            self.update()

    def skel_update(self, *args, **kwargs):  # Switchboard "self.skelwidget"
        skeleton = self.currentSkelName()
        self.update()

    def reservationChanged(self, who):
        if self.currentSkelContext() is who:
            self.sensitize()

    def update(self):
        debug.mainthreadTest()
        skelctxt = self.currentSkelContext()
        if skelctxt is not None:
            nnodes = skelctxt.getObject().nnodes()
            npinned = skelctxt.pinnednodes.npinned()
            self.psdata.get_buffer().set_text(
                "Total No. of Nodes: %d\nNo. of Pinned Nodes: %d\n" %
                (nnodes, npinned))
        else:
            self.psdata.get_buffer().set_text("")
        self.sensitize()

    def select_skeletonCB(self, *args):
        self.update()

    def currentSkelName(self):
        return self.skelwidget.get_value()
    
    def currentSkelContext(self):
        try:
            if self.skelwidget.get_value() is None:
                return None
            return skeletoncontext.skeletonContexts[self.currentSkelName()]
        except KeyError:
            return None

    def getSkeletonAvailability(self):
        ctxt = self.currentSkelContext()
        return ctxt is not None and not ctxt.query_reservation()

    def sensitize(self):
        debug.mainthreadTest()
        skelcontext = self.currentSkelContext()
        skelok = (skelcontext is not None 
                  and not skelcontext.query_reservation())
        self.okbutton.set_sensitive(skelok)
        self.undobutton.set_sensitive(skelok and
                                      skelcontext.pinnednodes.undoable())
        self.redobutton.set_sensitive(skelok and
                                      skelcontext.pinnednodes.redoable())
        self.unpinallbutton.set_sensitive(skelok and
                                          skelcontext.pinnednodes.npinned() > 0)
        self.invertbutton.set_sensitive(skelok)
        gtklogger.checkpoint("pinnodes page sensitized")


    def okCB(self, *args):
        modmethod = self.pinModFactory.getRegistration()
        if modmethod is not None:
            self.pinModFactory.set_defaults()
            menuitem = getattr(mainmenu.OOF.Skeleton.PinNodes,
                               utils.space2underscore(modmethod.name()))
            menuitem.callWithDefaults(skeleton=self.currentSkelName())

    def undoCB(self, *args):
        mainmenu.OOF.Skeleton.PinNodes.Undo(skeleton=self.currentSkelName())
    
    def redoCB(self, *args):
        mainmenu.OOF.Skeleton.PinNodes.Redo(skeleton=self.currentSkelName())

    def unpinallCB(self, *args):
        mainmenu.OOF.Skeleton.PinNodes.UnPinAll(skeleton=self.currentSkelName())

    def invertCB(self, *args):
        mainmenu.OOF.Skeleton.PinNodes.Invert(skeleton=self.currentSkelName())


# Create the page.
pinnodesPage = PinNodesPage()
