# -*- python -*-
# $RCSfile: skeletonBoundaryPage.py,v $
# $Revision: 1.67.2.11 $
# $Author: fyc $
# $Date: 2014/07/28 22:18:49 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common import config
from ooflib.common import debug
from ooflib.common import labeltree
from ooflib.common import utils
from ooflib.common.IO import whoville
from ooflib.common.IO.GUI import chooser
from ooflib.common.IO.GUI import fixedwidthtext
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import oofGUI
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import tooltips
from ooflib.common.IO.GUI import whowidget
from ooflib.engine import boundarybuilder
from ooflib.engine import skeletoncontext
from ooflib.engine.IO import boundarymenu
import gtk

# TODO 3.1: Display interface material, if any.

class SkeletonBoundaryPage(oofGUI.MainPage):
    def __init__(self):
        self.built = False
        oofGUI.MainPage.__init__(self, name="Skeleton Boundaries",
                                 ordering = 150,
                                 tip = "Create and orient boundaries.")

        mainbox = gtk.VBox(spacing=2)
        self.gtk.add(mainbox)

        align = gtk.Alignment(xalign=0.5)
        mainbox.pack_start(align, expand=0, fill=0)
        centerbox = gtk.HBox(spacing=3)
        align.add(centerbox)
        
        self.skelwidget = whowidget.WhoWidget(whoville.getClass('Skeleton'),
                                              scope=self)
        switchboard.requestCallbackMain(self.skelwidget,
                                        self.widgetChanged)
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

        boundarylistframe = gtk.Frame("Boundaries")
        gtklogger.setWidgetName(boundarylistframe, 'Boundaries')
        boundarylistframe.set_shadow_type(gtk.SHADOW_IN)
        mainpane.pack1(boundarylistframe, resize=0, shrink=0)

        boundarylistbox = gtk.VBox()
        boundarylistframe.add(boundarylistbox)

        # List of all the boundaries.
        self.boundarylist = chooser.ScrolledChooserListWidget(
            callback=self.boundarylistCB,
            dbcallback=self.modifyBoundaryCB,
            autoselect=0,
            name="BoundaryList",
            separator_func=self.chooserSepFunc)
        boundarylistbox.pack_start(self.boundarylist.gtk, expand=1, fill=1)

        boundarybuttonbox = gtk.HBox(homogeneous=1, spacing=2)
        boundarylistbox.pack_start(boundarybuttonbox, expand=0, fill=0)

        # Buttons that actually do stuff.
        self.newbutton = gtk.Button("New...")
        gtklogger.setWidgetName(self.newbutton, 'New')
        gtklogger.connect(self.newbutton, "clicked", self.newBoundaryCB)
        tooltips.set_tooltip_text(self.newbutton,
                             "Construct a new boundary in the skeleton and associated meshes.")
        boundarybuttonbox.pack_start(self.newbutton, expand=1, fill=1)

        self.editbutton = gtk.Button("Modify...")
        gtklogger.setWidgetName(self.editbutton, 'Modify')
        gtklogger.connect(self.editbutton, "clicked", self.modifyBoundaryCB)
        tooltips.set_tooltip_text(self.editbutton,
                             "Modify the attributes of the selected boundary.")
        boundarybuttonbox.pack_start(self.editbutton, expand=1, fill=1)
        
        self.renamebutton = gtk.Button("Rename...")
        gtklogger.setWidgetName(self.renamebutton, 'Rename')
        gtklogger.connect(self.renamebutton, "clicked", self.renameBoundaryCB)
        tooltips.set_tooltip_text(self.renamebutton,
                             "Rename the selected boundary.")
        boundarybuttonbox.pack_start(self.renamebutton, expand=1, fill=1)

        self.deletebutton = gtk.Button("Delete")
        gtklogger.setWidgetName(self.deletebutton, 'Delete')
        gtklogger.connect(self.deletebutton, "clicked", self.deleteBoundaryCB)
        tooltips.set_tooltip_text(self.deletebutton,
                             "Delete the selected boundary from the skeleton and associated meshes.")
        boundarybuttonbox.pack_start(self.deletebutton, expand=1, fill=1)
        
        # TODO 3.1: Copying could be added here -- the scenario is
        # that a user may want to make a copy of a boundary, and then
        # edit one of the copies.  Currently boundary editing is
        # primitive (one can only add/remove components), but when
        # visual pointy-clicky boundary editing is added, copying will
        # make sense.

        infoframe = gtk.Frame("Boundary data")
        gtklogger.setWidgetName(infoframe, 'Boundary data')
        infoframe.set_shadow_type(gtk.SHADOW_IN)
        mainpane.pack2(infoframe, resize=1, shrink=1)

        infowindow = gtk.ScrolledWindow()
        gtklogger.logScrollBars(infowindow, "InfoScroll")
        infowindow.set_shadow_type(gtk.SHADOW_IN)
        infoframe.add(infowindow)
        infowindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        
        self.infotext = fixedwidthtext.FixedWidthTextView()
        self.infotext.set_wrap_mode(gtk.WRAP_WORD)
        gtklogger.setWidgetName(self.infotext, 'status')
        self.infotext.set_editable(False)
        infowindow.add(self.infotext)

        self.built = True
        
        # Catches push events *after* the boundaries have been
        # propagated, and also undo/redo events.  "who changed" is
        # too early.
        switchboard.requestCallbackMain("new boundary configuration",
                                        self.newBdyConfigCB)
        switchboard.requestCallbackMain("new boundary created",
                                        self.newBdyCB)
        switchboard.requestCallbackMain("boundary removed",
                                        self.newBdyCB)
        switchboard.requestCallbackMain("boundary renamed",
                                        self.newBdyCB),
        switchboard.requestCallbackMain(("new who", "Microstructure"),
                                        self.newMicrostructureCB)
        self.selectsignals = [
            switchboard.requestCallbackMain("boundary selected",
                                            self.bdySelectedCB),
            switchboard.requestCallbackMain("boundary unselected",
                                            self.bdyUnselectedCB)
            ]
            
    def installed(self):
	self.updateInfo()
	self.sensitize()
        
    def currentSkeletonContext(self):
        try:
            return skeletoncontext.skeletonContexts[self.skelwidget.get_value()]
        except KeyError:
            return None

    def widgetChanged(self, interactive): # sb callback from skelwidget
        self.updateBdyList()
        self.updateInfo()
        self.sensitize()
        gtklogger.checkpoint("boundary page updated")

    # A separator is inserted in the list of boundary names between
    # the edge boundaries and the point boundaries.  (The separator is
    # a meta-boundary!)  This is done by including a string unlikely
    # to be a boundary name in the list of names sent to the
    # ChooserListWidget, and giving the widget a separator_func that
    # looks for the string.
    
    separator_proxy = "a string unlikely to be a boundary name"

    def updateBdyList(self):
        skelctxt = self.currentSkeletonContext()
        if skelctxt:
            edgebdynames = skelctxt.edgeboundaries.keys()
            edgebdynames.sort()
            ptbdynames = skelctxt.pointboundaries.keys()
            ptbdynames.sort()
            names = edgebdynames + [self.separator_proxy] + ptbdynames
            if config.dimension() == 3:
                facebdynames = skelctxt.faceboundaries.keys()
                facebdynames.sort()
                names = facebdynames + [self.separator_proxy] + names
            self.boundarylist.update(names)
            # If we've just switched Skeletons, we need make sure that
            # the selected bdy in our list is the same as the one
            # selected in the Skeleton. This is important because it's
            # also displayed on the canvas.
            selbdyname = skelctxt.getSelectedBoundaryName()
            if selbdyname:
                self.boundarylist.set_selection(selbdyname)
        else:
            self.boundarylist.update([])

    def chooserSepFunc(self, model, iter):
        # See comment about separators above.
        return model[iter][0] == self.separator_proxy
        
    def sensitize(self):
        debug.mainthreadTest()
        buttons_alive = self.boundarylist.has_selection()
        self.editbutton.set_sensitive(buttons_alive)
        self.renamebutton.set_sensitive(buttons_alive)
        self.deletebutton.set_sensitive(buttons_alive)
        self.newbutton.set_sensitive(self.currentSkeletonContext() is not None)

    def updateInfo(self):
        debug.mainthreadTest()
        skelctxt = self.currentSkeletonContext()
        if skelctxt is not None:
            bdyname = self.boundarylist.get_value()
            if bdyname is not None:
                bdytext = skelctxt.boundaryInfo(bdyname)
                self.infotext.get_buffer().set_text(
                    "Boundary %s:\n%s" % (bdyname, bdytext))
            else:
                self.infotext.get_buffer().set_text("No boundary selected.")
        else:
            self.infotext.get_buffer().set_text("No skeleton selected.")

    def newMicrostructureCB(self, msname): # sb ("new who", "Microstructure")
        if not self.currentSkeletonContext():
            self.skelwidget.set_value(msname)
            
    def newBdyConfigCB(self, skelctxt): # sb "new boundary configuration"
        if skelctxt is self.currentSkeletonContext():
            self.sensitize()
            self.updateBdyList()
            self.updateInfo()
            gtklogger.checkpoint("boundary page updated")
                    

    def newBdyCB(self, skelctxt):       # sb bdy creation, removal, or renaming
        if skelctxt is self.currentSkeletonContext():
            self.updateBdyList()
            self.updateInfo()
            self.sensitize()
            gtklogger.checkpoint("boundary page updated")

    def bdySelectedCB(self, skelctxt, name): # sb "boundary selected"
        if skelctxt is self.currentSkeletonContext():
            self.inhibitSignals()
            self.boundarylist.set_selection(name)
            self.uninhibitSignals()
            self.updateInfo()
            self.sensitize()
            gtklogger.checkpoint("boundary page updated")
    def bdyUnselectedCB(self, skelctxt): # sb "boundary unselected"
        if skelctxt is self.currentSkeletonContext():
            self.inhibitSignals()
            self.boundarylist.set_selection(None)
            self.uninhibitSignals()
            self.updateInfo()
            self.sensitize()
            gtklogger.checkpoint("boundary page updated")
    def inhibitSignals(self):
        debug.mainthreadTest()
        for sig in self.selectsignals:
            sig.block()
    def uninhibitSignals(self):
        debug.mainthreadTest()
        for sig in self.selectsignals:
            sig.unblock()

    def boundarylistCB(self, bdyobj, interactive): # ChooserListWidget callback
        if self.built and interactive:
            skelctxt = self.currentSkeletonContext()
            if skelctxt:
                bdyname = self.boundarylist.get_value()
                if bdyname:
                    skelctxt.selectBoundary(bdyname)
                else:
                    skelctxt.unselectBoundary()
            self.sensitize()
            self.updateInfo()
            gtklogger.checkpoint("boundary page updated")

    # Context-sensitivity is built in to the DirectorWidget.
    def newBoundaryCB(self, gtkobj):    # button callback
        menuitem = boundarymenu.boundarymenu.Construct
        nameparam =  menuitem.get_arg('name')
        builderparam = menuitem.get_arg('constructor')
        if parameterwidgets.getParameters(
            nameparam, builderparam, title="New Boundary",scope=self):
            menuitem.callWithDefaults(skeleton=self.skelwidget.get_value())
    
    def modifyBoundaryCB(self, *args): # button callback
        # The parameter widget needs to know what types of modifiers
        # to present, so we need to let it know what kind of boundary
        # it's operating on.  We just pass the boundary through to the
        # parameter via the dialog box.  The box is a widgetscope, so
        # the enclosed widgets can navigate to it easily, and it has
        # the same lifetime as the data in question.

        menuitem = boundarymenu.boundarymenu.Modify
        modparam = menuitem.get_arg('modifier')

        skelctxt = skeletoncontext.skeletonContexts[
            self.skelwidget.get_value()]
        bdyobj = skelctxt.getBoundary(self.boundarylist.get_value())

        dialog_extra = {'boundary' : bdyobj}
        
        if parameterwidgets.getParameters(
            modparam, title="Boundary modifier", scope=self,
            dialog_data=dialog_extra):
            menuitem.callWithDefaults(skeleton=self.skelwidget.get_value(),
                                      boundary=self.boundarylist.get_value())

    def renameBoundaryCB(self, gtkobj): # button callback
        menuitem = boundarymenu.boundarymenu.Rename
        newname = menuitem.get_arg('name')
        oldname = self.boundarylist.get_value()
        newname.set(oldname)
        if parameterwidgets.getParameters(
            newname, title="New name for this boundary"):
            menuitem.callWithDefaults(
                skeleton=self.skelwidget.get_value(),
                boundary=self.boundarylist.get_value())

    def deleteBoundaryCB(self, gtkobj): # button callback
        menuitem = boundarymenu.boundarymenu.Delete
        menuitem(skeleton=self.skelwidget.get_value(),
                 boundary=self.boundarylist.get_value())

        
    
sbp = SkeletonBoundaryPage()
