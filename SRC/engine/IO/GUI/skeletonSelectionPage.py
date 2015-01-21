# -*- python -*-
# $RCSfile: skeletonSelectionPage.py,v $
# $Revision: 1.70.2.23 $
# $Author: langer $
# $Date: 2014/11/05 16:54:55 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import labeltree
from ooflib.common import mainthread
from ooflib.common import microstructure
from ooflib.common import subthread
from ooflib.common import utils
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
from ooflib.engine import skeletoncontext
from ooflib.engine import skeletonselmodebase
import gtk
import sys


# Main GUI page for selecting Skeleton objects.

# Each type of selectable Skeleton object has an associate
# SkeletonSelectionMode subclass, of which there is one instance.  For
# each of these modes, the SkeletonSelectionPage creates a radio
# button to switch between modes, a list of groups, and a
# RegisteredClassFactory and Historian to modify the selection.  For
# each mode, all of this mode specific data is stored in a ModeData
# object.

## TODO 3.1: Clear out the forest of switchboard signals used by this
## page.

class ModeData:
    def __init__(self, page, mode):
        self.page = page                # SkeletonSelectionPage
        self.mode = mode                # SkeletonSelectionMode object
        self.factory = None             # RCF of SelectionModifiers
        self.historybox = None          # HistoryBox obj, contains Historian
        self.button = None              # Radio button for selecting this mode
    def name(self):
        return self.mode.name
    def getSkeletonContext(self):
        return self.page.getCurrentSkeleton()
    def getSelectionContext(self, skelcontext):
        return self.mode.getSelectionContext(skelcontext)
    def getSelectionMenu(self):
        return self.mode.getSelectionMenu()
    def getGroupMenu(self):
        return self.mode.getGroupMenu()
    def getGroups(self, skeletoncontext):
        return self.mode.getGroups(skeletoncontext)
    def modifierApplied(self, modifier): # sb: mode.modifierappliedsignal
        if self.historybox is not None:
            if modifier is not None:
                self.historybox.historian.record(modifier)
                self.historybox.sensitize()
    def validityChangeCB(self, validity): # sb: ('validity', factory)
        self.ok_sensitize()
    def ok_sensitize(self):
        debug.mainthreadTest()
        skelcontext = self.getSkeletonContext()
        self.historybox.okbutton.set_sensitive(
            skelcontext is not None
            and not skelcontext.query_reservation()
            and self.factory.isValid())
        
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SkeletonSelectionPage(oofGUI.MainPage):
    def __init__(self):
        self.built = False # TODO: Obsolete?
        # The installed_flag is used to set the pane state the first
        # time it's displayed, and more importantly not to set it on
        # subsequent displays.
        self.installed_flag = False 
        oofGUI.MainPage.__init__(
            self, name="Skeleton Selection",
            ordering = 135,
            tip = "Manipulate selectable skeleton objects.")

        self.mainbox = gtk.VBox(spacing=2)
        self.gtk.add(self.mainbox)

        self.skelwidgetbox = gtk.Alignment(xalign=0.5)
        self.mainbox.pack_start(self.skelwidgetbox, expand=0, fill=0)
        centerbox = gtk.HBox(spacing=3)
        self.skelwidgetbox.add(centerbox)
        self.skelwidget = whowidget.WhoWidget(skeletoncontext.skeletonContexts,
                                              scope=self)
        self.skelwidget.verbose = True
        label = gtk.Label('Microstructure=')
        label.set_alignment(1.0, 0.5)
        centerbox.pack_start(label, expand=0, fill=0)
        centerbox.pack_start(self.skelwidget.gtk[0], expand=0, fill=0)
        label = gtk.Label('Skeleton=')
        label.set_alignment(1.0, 0.5)
        centerbox.pack_start(label, expand=0, fill=0)
        centerbox.pack_start(self.skelwidget.gtk[1], expand=0, fill=0)

        self.modebox = gtk.Alignment(xalign=0.5)
        gtklogger.setWidgetName(self.modebox, 'Mode')
        self.mainbox.pack_start(self.modebox, expand=0, fill=0)
        centerbox = gtk.HBox(spacing=3)
        self.modebox.add(centerbox)
        label = gtk.Label("Selection Mode:")
        label.set_alignment(1.0, 0.5)
        centerbox.pack_start(label, expand=0, fill=0)

        # Construct buttons for switching between selection modes, and
        # the ModeData objects that contain the mode-specific data and
        # widgets.
        self.modedict = {}
        firstbutton = None
        for mode in skeletonselmodebase.SkeletonSelectionMode.modes:
            name = mode.name
            modedata = self.modedict[name] = ModeData(self, mode)
            if firstbutton:
                button = gtk.RadioButton(label=name+'s', group=firstbutton)
            else:
                button = gtk.RadioButton(label=name+'s')
                firstbutton = button
                self.activemode = modedata
            gtklogger.setWidgetName(button, name)
            modedata.button = button
            tooltips.set_tooltip_text(button, "Select " + name + "s")
            centerbox.pack_start(button, expand=0, fill=0)
            gtklogger.connect(button, 'clicked', self.pickerCB, modedata)
            switchboard.requestCallbackMain(
                modedata.mode.changedselectionsignal,
                self.newSelection, mode=modedata)
            switchboard.requestCallbackMain(
                modedata.mode.modifierappliedsignal,
                self.modifiedSelection, mode=modedata)
        firstbutton.set_active(1)

        self.mainpane = gtk.HPaned()
        gtklogger.setWidgetName(self.mainpane, 'Pane')
        self.mainbox.pack_start(self.mainpane, expand=1, fill=1)
        gtklogger.connect_passive(self.mainpane, 'notify::position')
        
        # Status and Group are on the left side of the page.
        self.leftbox = gtk.VBox(spacing=3)
        self.mainpane.pack1(self.leftbox, resize=1, shrink=0)

        # Status box.
        self.statusframe = gtk.Frame()
        self.leftbox.pack_start(self.statusframe, expand=0, fill=0)
        self.statusframe.set_shadow_type(gtk.SHADOW_IN)
        self.status = gtk.Label()
        gtklogger.setWidgetName(self.status, 'status')
        self.status.set_alignment(0.0, 0.5)
        self.statusframe.add(self.status)

        # Group operations.
        self.groupgui = GroupGUI(self)
        self.leftbox.pack_start(self.groupgui.gtk, expand=1, fill=1)

        # Selection operations on the right side of the page.
        self.selectiongui = SelectionGUI(self)
        self.mainpane.pack2(self.selectiongui.gtk, resize=0, shrink=0)

        self.built = True

        switchboard.requestCallbackMain(("new who", "Microstructure"),
                                        self.new_microstructure)
        switchboard.requestCallbackMain(self.skelwidget, self.skelwidgetCB)
        switchboard.requestCallbackMain("materials changed in skeleton",
                                        self.matchangedCB)

        switchboard.requestCallbackMain("made reservation",
                                        self.reservationChanged)
        switchboard.requestCallbackMain("cancelled reservation",
                                        self.reservationChanged)

    def installed(self):
        if not self.installed_flag:
            # initialize, arbitrarily, to the first mode listed
            self.pickerCB(None,
                          self.modedict[skeletonselmodebase.firstMode().name])
            self.installed_flag = True

    def getCurrentSkeletonName(self):
        return self.skelwidget.get_value()
    def getCurrentSkeleton(self):
        name = self.getCurrentSkeletonName()
        path = labeltree.makePath(name)
        try:
            return skeletoncontext.skeletonContexts[name]
        except KeyError:
            return None

    def getCurrentMicrostructureName(self):
        return self.skelwidget.get_value(depth=1)
    def getCurrentMicrostructureContext(self):
        try:
            return microstructure.microStructures[
                self.getCurrentMicrostructureName()]
        except KeyError:
            return None

    # Must run on a subthread, because of the lock.
    def selectionSize(self):
        debug.subthreadTest()
        skelctxt = mainthread.runBlock(self.getCurrentSkeleton)
        if skelctxt is not None:
            skelctxt.begin_reading()
            try:
                if not skelctxt.defunct():
                    return self.activemode.getSelectionContext(skelctxt).size()
            finally:
                skelctxt.end_reading()
        return 0


    def update(self):
        skelctxt = self.getCurrentSkeleton()
        subthread.execute(self.update_subthread, (skelctxt,))

    def update_subthread(self, skelcontext):
        # Get the selection from the skeleton context
        if skelcontext:
            n = self.selectionSize()    # requires subthread
            status_text = " %d %s%s selected." % (n,
                                                  self.activemode.name(),
                                                  's'*(n!=1))
        else:
            status_text = "No Skeleton selected."

        mainthread.runBlock(self.status.set_text, (status_text,))
        gtklogger.checkpoint("skeleton selection page updated")

        
    def pickerCB(self, gtk, modedata):  # new selection mode chosen
        self.statusframe.set_label(modedata.name() + ' Selection Status')
        self.activemode = modedata
        self.groupgui.pickerCB(modedata)
        self.selectiongui.pickerCB(modedata)
        self.update()                   # doesn't set self.activemode anymore

    def skelwidgetCB(self, interactive): # skeleton widget sb callback
        debug.mainthreadTest()
        skelcontext = self.getCurrentSkeleton()
        self.groupgui.new_skeleton(skelcontext)
        self.selectiongui.new_skeleton(skelcontext)
        self.update()

    def new_microstructure(self, msname): # sb ("new who", "Microstructure")
        # Switch to a new Microstructure only if there is no current Skeleton
        if not self.getCurrentSkeletonName():
            self.skelwidget.set_value(msname)
    
    def show(self):
        debug.mainthreadTest()
        self.gtk.show()
        self.mainbox.show()
        self.skelwidgetbox.show_all()
        self.modebox.show_all()
        self.mainpane.show()
        self.leftbox.show_all()
        self.groupgui.show()
        self.selectiongui.show()

    # switchboard callback for mode.modifierappliedsignal
    def modifiedSelection(self, modifier, mode):
        if mode is self.activemode:
            self.groupgui.sensitize()
            self.selectiongui.sensitize()
            # self.update must come last, so that the checkpoint is
            # issued after everything has changed.
            self.update()

    # switchboard callback for mode.changedselectionsignal
    def newSelection(self, mode, selection):
        if mode is self.activemode:
            self.groupgui.sensitize()
            self.selectiongui.sensitize()
            # self.update must come last, so that the checkpoint is
            # issued after everything has changed.
            self.update()

    def matchangedCB(self, skelctxt):
        if skelctxt is self.getCurrentSkeleton():
            self.groupgui.draw_grouplist()

    # switchboard callback for "made reservation" or "cancelled reservation"
    def reservationChanged(self, who):
        if self.getCurrentSkeleton() is who:
            self.groupgui.sensitize()
            self.selectiongui.sensitize()

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# GroupGUI contains the big list of groups, which changes when a new
# category is picked by the picker, or when a new skeletoncontext is
# selected by the mesh widget.  The GroupGUI has a local selection
# state.

class GroupGUI:
    def __init__(self, parent):
        debug.mainthreadTest()
        self.parent = parent
        self.gtk = gtk.Frame()
        gtklogger.setWidgetName(self.gtk, 'Groups')
        self.gtk.set_shadow_type(gtk.SHADOW_IN)
        box = gtk.HBox(spacing=2)
        self.gtk.add(box)
        # Set in chooserCB, the widget callback for the chooser list.
        self.current_group_name = None
        # List of buttons which are sensitive only when a group is selected.
        self.groupbuttons = []
        # List of buttons which are sensitive when there is a group
        # and a selection.
        self.groupandselectionbuttons = []

        # Left-hand button box.  New/Auto/Rename/Copy/Delete/DeleteAll
        lbuttons = gtk.VBox(spacing=2)
        box.pack_start(lbuttons, fill=0, expand=0)

        self.new_button = gtk.Button("New...")
        gtklogger.setWidgetName(self.new_button, 'New')
        lbuttons.pack_start(self.new_button, fill=0, expand=0)
        gtklogger.connect(self.new_button, "clicked", self.newGroupCB)
        tooltips.set_tooltip_text(self.new_button,
                             "Create a new empty group.")

        self.auto_button = gtk.Button("Auto")
        gtklogger.setWidgetName(self.auto_button, 'Auto')
        lbuttons.pack_start(self.auto_button, fill=0, expand=0)
        gtklogger.connect(self.auto_button, 'clicked', self.autoGroupCB)
        tooltips.set_tooltip_text(
            self.auto_button,
            "Automatically create groups from the current pixel groups.")
        
        self.rename_button = gtk.Button("Rename...")
        gtklogger.setWidgetName(self.rename_button, 'Rename')
        lbuttons.pack_start(self.rename_button, fill=0, expand=0)
        self.groupbuttons.append(self.rename_button)
        gtklogger.connect(self.rename_button, "clicked", self.renameGroupCB)
        tooltips.set_tooltip_text(self.rename_button,
                             "Rename the selected group.")

        self.copy_button = gtk.Button("Copy...")
        gtklogger.setWidgetName(self.copy_button, 'Copy')
        lbuttons.pack_start(self.copy_button, fill=0, expand=0)
        self.groupbuttons.append(self.copy_button)
        gtklogger.connect(self.copy_button, "clicked", self.copyGroupCB)
        tooltips.set_tooltip_text(self.copy_button,
                             "Copy the selected group.")

        self.delete_button = gtk.Button("Delete")
        gtklogger.setWidgetName(self.delete_button, 'Delete')
        lbuttons.pack_start(self.delete_button, fill=0, expand=0)
        self.groupbuttons.append(self.delete_button)
        gtklogger.connect(self.delete_button, "clicked", self.deleteGroupCB)
        tooltips.set_tooltip_text(self.delete_button,
                             "Deleted the selected group.")

        self.deleteAll_button = gtk.Button("Delete All")
        gtklogger.setWidgetName(self.deleteAll_button, 'DeleteAll')
        lbuttons.pack_start(self.deleteAll_button, fill=0, expand=0)
        gtklogger.connect(self.deleteAll_button, 'clicked', self.deleteAllCB)
        tooltips.set_tooltip_text(self.deleteAll_button, "Delete all groups.")
        
        # Groups list.
        self.grouplist = chooser.ScrolledChooserListWidget(
            callback=self.chooserCB, name="GroupList")
        box.pack_start(self.grouplist.gtk, fill=1, expand=1)
        
        # Right-hand button box.  Add/Remove/Clear/ClearAll/Info
        rbuttons = gtk.VBox(spacing=2)
        box.pack_start(rbuttons, fill=0, expand=0)

        self.add_button = gtk.Button("Add")
        gtklogger.setWidgetName(self.add_button, 'Add')
        rbuttons.pack_start(self.add_button, fill=0, expand=0)
        self.groupandselectionbuttons.append(self.add_button)
        gtklogger.connect(self.add_button, "clicked", self.addToGroupCB)
        tooltips.set_tooltip_text(self.add_button,
                             "Add the currently selected pixels"
                             " to the selected group.")

        self.remove_button = gtk.Button("Remove")
        gtklogger.setWidgetName(self.remove_button, 'Remove')
        rbuttons.pack_start(self.remove_button, fill=0, expand=0)
        self.groupandselectionbuttons.append(self.remove_button)
        gtklogger.connect(self.remove_button, "clicked", self.removeFromGroupCB)
        tooltips.set_tooltip_text(self.remove_button,
              "Remove the currently selected pixels from the selected group.")
        
        self.clear_button = gtk.Button("Clear")
        gtklogger.setWidgetName(self.clear_button, 'Clear')
        rbuttons.pack_start(self.clear_button, fill=0, expand=0)
        gtklogger.connect(self.clear_button, "clicked", self.clearGroupCB)
        tooltips.set_tooltip_text(self.clear_button,
                             "Remove all pixels from the selected group.")

        self.clearAll_button = gtk.Button("Clear All")
        gtklogger.setWidgetName(self.clearAll_button, 'ClearAll')
        rbuttons.pack_start(self.clearAll_button, fill=0, expand=0)
        gtklogger.connect(self.clearAll_button, "clicked", self.clearAllCB)
        tooltips.set_tooltip_text(self.clearAll_button,
                             "Remove all pixels from all groups.")

        self.info_button = gtk.Button("Info")
        gtklogger.setWidgetName(self.info_button, 'Info')
        rbuttons.pack_start(self.info_button, fill=0, expand=0)
        self.groupbuttons.append(self.info_button)
        gtklogger.connect(self.info_button, "clicked", self.queryGroupCB)
        tooltips.set_tooltip_text(self.info_button,
                             "Display information about the selected group"
                             " in the OOF Messages window.")
        
        ## TODO 3.1: Deactivate this frame when mode.materialsallowed
        ## is False, once Assign_Material has been restored to the
        ## elementgroupmenu.
        matframe = gtk.Frame("Material")
#        matframe.set_shadow_type(gtk.SHADOW_IN)
        rbuttons.pack_start(matframe, expand=0, fill=0, padding=3)
        matbox = gtk.VBox(spacing=2)
        matframe.add(matbox)

        ## TODO 3.1: Remove this line when Assign_Material and
        ## Remove_Material have been restored to the elementgroupmenu.
        ## See TODO in skeletongroupmenu.py.
        matframe.set_sensitive(False)

        self.addmaterial_button = gtk.Button("Assign")
        gtklogger.setWidgetName(self.addmaterial_button, 'AddMaterial')
        matbox.pack_start(self.addmaterial_button, fill=0, expand=0)
        gtklogger.connect(self.addmaterial_button, "clicked",
                          self.addMaterialCB)
        ## TODO 3.1: Fix tooltip when Assign_Material and Remove_Material
        ## have been rsetored to the elementgroupmenu.
        tooltips.set_tooltip_text(self.addmaterial_button,
                             "Assign a material to the members of the selected"
                             " group. (NOT IMPLEMENTED YET)")

        self.removematerial_button = gtk.Button("Remove")
        matbox.pack_start(self.removematerial_button, fill=0, expand=0)
        gtklogger.connect(self.removematerial_button, "clicked",
                          self.removeMaterialCB)
        ## TODO 3.1: Fix tooltip when Assign_Material and Remove_Material
        ## have been restored to the elementgroupmenu.
        tooltips.set_tooltip_text(self.removematerial_button,
                             "Remove an explicitly assigned material"
                             " from the members of the selected group."
                             " (NOT IMPLEMENTED YET)")
        
        # Need to be notified when groupset memberships change.
        switchboard.requestCallback("groupset member added", self.group_added),
        switchboard.requestCallback("groupset member renamed",
                                    self.group_added),
        switchboard.requestCallback("groupset changed", self.groupset_changed),
        switchboard.requestCallback("groupset member resized",
                                    self.group_resized)
        switchboard.requestCallback("new pixel group", self.pxlgroup_added)
        switchboard.requestCallback("destroy pixel group", self.pxlgroup_added)
      

    def show(self):
        debug.mainthreadTest()
        self.gtk.show_all()

    def activemode(self):
        return self.parent.activemode

    def getGroupSet(self):
        skelcontext = self.parent.getCurrentSkeleton()
        if skelcontext:
            return self.activemode().getGroups(skelcontext)

        
    # Called from the ChooserListWidget when a new selection is
    # made, including "None" for a deselection.
    def chooserCB(self, name, interactive):
        if self.parent.built:
            self.sensitize()


    # For the following three callbacks, it's tempting to just have
    # them be requested on subthreads, but there's actually no
    # guarantee that the notifying thread will not be the main thread,
    # and the locks *must* be on a subthread.  So we do it this way.

    # Utility function, conditional for the callbacks.
    def check_skel_and_gset(self, skelctxt, gset):
        page_skel = self.parent.getCurrentSkeleton()
        if skelctxt is page_skel:
            gst = self.getGroupSet()
            if gset is None or gset is gst:
                return gst
        return False

    # Switchboard callback, called when member groups are added to or removed
    # from a groupset.  Arguments are the host skeletonContext
    # and the groupset.
    def group_added(self, skelcontext, gset, name):
        debug.subthreadTest()
        gset = mainthread.runBlock(self.check_skel_and_gset, (skelcontext,gset))
        if gset:
            skelcontext.begin_reading()
            try:
                names = gset.allGroups()
            finally:
                skelcontext.end_reading()
            self.update_grouplist(names, map(gset.displayString, names))
            mainthread.runBlock(self.grouplist.set_selection,
                                    (name,) )
        self.sensitize_subthread()

    def groupset_changed(self, skelcontext, gset):
        debug.subthreadTest()
        gset = mainthread.runBlock(self.check_skel_and_gset, (skelcontext,gset))
        if gset:
            skelcontext.begin_reading()
            try:
                names = gset.allGroups()
            finally:
                skelcontext.end_reading()
            self.update_grouplist(names, map(gset.displayString, names))
        # Must sensitize -- if the current group has become empty, the
        # "clear" button's sensitivity will have changed.
        self.sensitize_subthread()

    def group_resized(self, skelcontext, gset):
        debug.subthreadTest()
        gset = mainthread.runBlock(self.check_skel_and_gset, (skelcontext,gset))
        if gset:
            skelcontext.begin_reading()
            try:
                names = gset.allGroups()
            finally:
                skelcontext.end_reading()
            self.update_grouplist(names, map(gset.displayString, names))

        # Must sensitize -- if the resize was to or away from size 0,
        # the clear button needs updating.
        #  mainthread.runBlock(self.sensitize)
        self.sensitize_subthread()

    def pxlgroup_added(self, group, *args):
        # switchboard callback when pixel groups are added or
        # removed. The auto button has to be sensitized.
        self.sensitize_subthread()
    
    # Button callback for the "new group" button.
    def newGroupCB(self, gtkobj):
        skelpath = self.parent.getCurrentSkeletonName()
        menuitem = self.activemode().getGroupMenu().New_Group
        group_param = menuitem.get_arg('name')
        if parameterwidgets.getParameters(
            group_param,
            title='Create a new %s group' % self.activemode().name()):
            menuitem.callWithDefaults(skeleton=skelpath)

    def autoGroupCB(self, gtkobj): # "auto group" button callback
        skelpath = self.parent.getCurrentSkeletonName()
        menuitem = self.activemode().getGroupMenu().Auto_Group
        menuitem.callWithDefaults(skeleton=skelpath)

    # Button callback for the "rename group" button.
    def renameGroupCB(self, gtkobj):
        skelpath = self.parent.getCurrentSkeletonName()
        current_group = self.grouplist.get_value()
        menuitem = self.activemode().getGroupMenu().Rename_Group
        new_group_param = menuitem.get_arg('new_name')
        new_group_param.value = current_group
        if parameterwidgets.getParameters(
            new_group_param, title='Rename group %s' % current_group):
            menuitem.callWithDefaults(skeleton=skelpath,
                                      group=current_group)

    # Button callback for the "copy group" button.
    def copyGroupCB(self, gtkobj):
        skelpath = self.parent.getCurrentSkeletonName()
        current_group = self.grouplist.get_value()
        menuitem = self.activemode().getGroupMenu().Copy_Group
        new_group_param = menuitem.get_arg('new_name')
        if parameterwidgets.getParameters(
            new_group_param,
            title='Copy group %s' % current_group):
            menuitem.callWithDefaults(skeleton=skelpath,
                                      group=current_group)

    # Button callback for the "delete group" button.
    def deleteGroupCB(self, gtkobj):
        skelpath = self.parent.getCurrentSkeletonName()
        current_group = self.grouplist.get_value()
        if reporter.query("Really delete %s?" % current_group,
                          "No", default="Yes") == "Yes":
	  menuitem = self.activemode().getGroupMenu().Delete_Group
	  menuitem(skeleton=skelpath, group=current_group)

    def deleteAllCB(self, gtkobj):
        skelpath = self.parent.getCurrentSkeletonName()
        if reporter.query("Really delete all?",
                          "No", default="Yes") == "Yes":
	  menuitem = self.activemode().getGroupMenu().Delete_All
	  menuitem(skeleton=skelpath)

    # Button callback for the "add" button, adds selection to group.
    def addToGroupCB(self, gtkobj):
        skelpath = self.parent.getCurrentSkeletonName()
        current_group = self.grouplist.get_value()
        menuitem = self.activemode().getGroupMenu().Add_to_Group
        menuitem(skeleton=skelpath, group=current_group)

    # Button callback for the "remove" button, removes the current
    # selection from the current group.
    def removeFromGroupCB(self, gtkobj):
        skelpath = self.parent.getCurrentSkeletonName()
        current_group = self.grouplist.get_value()
        if reporter.query("Really remove %s selections?" % current_group,
                          "No", default="Yes") == "Yes":
	  menuitem = self.activemode().getGroupMenu().Remove_from_Group
	  menuitem(skeleton=skelpath, group=current_group)

    # Button callback for the "clear" button, removes all members
    # from the current group.
    def clearGroupCB(self, gtkobj):
        skelpath = self.parent.getCurrentSkeletonName()
        current_group = self.grouplist.get_value()
        if reporter.query("Really clear %s?" % current_group,
                          "No", default="Yes") == "Yes":
	  menuitem = self.activemode().getGroupMenu().Clear_Group
	  menuitem(skeleton=skelpath, group=current_group)

    def clearAllCB(self, gtkobj):
        skelpath = self.parent.getCurrentSkeletonName()      
        if reporter.query("Really clear all?",
                          "No", default="Yes") == "Yes":
	  menuitem = self.activemode().getGroupMenu().Clear_All
	  menuitem(skeleton=skelpath)
        
    def queryGroupCB(self, gtkobj):
        skelpath = self.parent.getCurrentSkeletonName()
        current_group = self.grouplist.get_value()
        menuitem = self.activemode().getGroupMenu().Query_Group
        menuitem(skeleton=skelpath, group=current_group)

    def addMaterialCB(self, gtkobj):
        skelpath = self.parent.getCurrentSkeletonName()
        current_group = self.grouplist.get_value()
        menuitem = self.activemode().getGroupMenu().Assign_Material
        if parameterwidgets.getParameters(
            menuitem.get_arg('material'),
            title="Assign a material to a %s group" % self.activemode().name()):
            menuitem.callWithDefaults(skeleton=skelpath, group=current_group)

    def removeMaterialCB(self, gtkobj):
        skelpath = self.parent.getCurrentSkeletonName()
        current_group = self.grouplist.get_value()
        if reporter.query("Really remove %s material?" % current_group,
                          "No", default="Yes") == "Yes":
	  menuitem = self.activemode().getGroupMenu().Remove_Material
	  menuitem(skeleton=skelpath, group=current_group)
    
    # Called from the parent when the skeleton widget has a new
    # skeletoncontext, including "None".
    def new_skeleton(self, skelcontext):
        self.draw_grouplist()
        self.sensitize()

    # Called from the parent when the "picker" chooses a new selection mode.
    def pickerCB(self, mode):
        self.gtk.set_label(mode.name() + " group operations")
        self.draw_grouplist()
        self.sensitize()

    def draw_grouplist(self):
        groupset = self.getGroupSet()
        if groupset:
            namelist = groupset.allGroups()
            self.update_grouplist(namelist,
                                  map(groupset.displayString, namelist))
        else:
            self.update_grouplist([], [])

    def update_grouplist(self, names, objs):
        mainthread.runBlock(self.update_grouplist_thread, (names, objs))
    def update_grouplist_thread(self, names, objs):
        self.grouplist.update(names, objs)
        #gtklogger.checkpoint("skeleton selection page grouplist")
            

    # This little two-step is required because the selectionSize()
    # query locks the selection object, and so can't be on the main
    # thread, but all the other sensitize operations are GUI
    # operations and must be on the main thread.
    def sensitize(self):
        subthread.execute(self.sensitize_subthread)

    def sensitize_subthread(self):
        debug.subthreadTest()
        ssize = self.parent.selectionSize() # requires subthread
        mainthread.runBlock(self.sensitize_mainagain, (ssize,))

    def sensitize_mainagain(self, ssize):
        debug.mainthreadTest()
        skelctxt = self.parent.getCurrentSkeleton()
        curskel = skelctxt is not None and not skelctxt.query_reservation()
        groupset = self.getGroupSet()

        self.new_button.set_sensitive(curskel)

        # The Auto button is sensitive if the microstructure has any
        # pixel groups.
        ms = self.parent.getCurrentMicrostructureContext()
        self.auto_button.set_sensitive(
            ms is not None and curskel and ms.getObject().nGroups() > 0
            ## TODO 3.1: When autogrouping of faces is implemented, delete
            ## the next line.
            and self.parent.activemode.name() != "Face"
            )

        # The Delete All button is sensitive if the Skeleton has any
        # Element/Node/Segment groups.
        self.deleteAll_button.set_sensitive(curskel and
                                            groupset is not None and 
                                            groupset.nGroups() > 0)

        # The Clear All button is sensitive if at least one group is
        # non-empty.
        if groupset is not None:
            for group in groupset.allGroups():
                if groupset.sizeOfGroup(group) > 0:
                    self.clearAll_button.set_sensitive(True)
                    break
            else:
                self.clearAll_button.set_sensitive(False)
        else:
            self.clearAll_button.set_sensitive(False)
        
        # Set the buttons in the groupbuttons list, if there is a group.
        groupstate = self.grouplist.get_value() is not None
        for b in self.groupbuttons:
            b.set_sensitive(groupstate)

        # Set the groupandselectionbuttons if there's a group selected,
        # and the skeletoncontext has a selection of the appropriate type
        # which is of nonzero size.
        g = self.grouplist.get_value()
        groupselectstate = g is not None and ssize > 0
        for b in self.groupandselectionbuttons:
            b.set_sensitive(groupselectstate)

        groupset = self.getGroupSet()
        self.clear_button.set_sensitive(groupset is not None and g is not None
                                        and groupset.sizeOfGroup(g) > 0)

        matok = (g is not None and
                 self.activemode().mode.materialsallowed is not None)

        ## TODO 3.1: Uncomment these lines when Assign_Material and
        ## Remove_Material have been restored to the elementgroupmenu.
        # self.addmaterial_button.set_sensitive(matok)
        # self.removematerial_button.set_sensitive(matok)
        
        gtklogger.checkpoint("skeleton selection page groups sensitized")
            
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SelectionGUI:
    def __init__(self, parent):
        debug.mainthreadTest()
        self.parent = parent
        self.gtk = gtk.Frame()
        gtklogger.setWidgetName(self.gtk, 'Selection')
        self.gtk.set_shadow_type(gtk.SHADOW_IN)
        self.vbox = gtk.VBox()
        self.gtk.add(self.vbox)

        self.actionbox = gtk.VBox()
        self.vbox.pack_start(self.actionbox, expand=1, fill=1)

        self.historyline = gtk.VBox()
        self.vbox.pack_start(self.historyline, expand=0, fill=0, padding=4)

        for modeobj in parent.modedict.values():
            modeobj.factory = regclassfactory.RegisteredClassFactory(
                modeobj.mode.modifierclass.registry,
                title="Action: ",
                scope=parent, name=modeobj.name()+"Action")
            modeobj.historybox = HistoryBox(self.setCB, self.okCB)
            gtklogger.setWidgetName(modeobj.historybox.gtk,
                                    modeobj.name()+"History")
            modeobj.factory.set_callback(
                modeobj.historybox.historian.stateChangeCB)
            # Sensitize the history stuff when the selections are modified.
            switchboard.requestCallbackMain(modeobj.mode.modifierappliedsignal,
                                            modeobj.modifierApplied)
            switchboard.requestCallbackMain(('validity', modeobj.factory),
                                            modeobj.validityChangeCB)

        # Slightly misleading name, includes undo, redo and clear.
        self.undoredoline = gtk.HBox()
        
        self.undo_button = gtk.Button(stock=gtk.STOCK_UNDO)
        gtklogger.setWidgetName(self.undo_button, 'Undo')
        gtklogger.connect(self.undo_button, "clicked", self.undoCB)
        tooltips.set_tooltip_text(self.undo_button,
                             "Undo the latest selection operation.")
        self.undoredoline.pack_start(self.undo_button, expand=1, fill=0)

        self.redo_button = gtk.Button(stock=gtk.STOCK_REDO)
        gtklogger.setWidgetName(self.redo_button, 'Redo')
        gtklogger.connect(self.redo_button, "clicked", self.redoCB)
        tooltips.set_tooltip_text(self.redo_button,
                             'Redo the latest undone selection operation.')
        self.undoredoline.pack_start(self.redo_button, expand=1, fill=0)

        self.clear_button = gtk.Button(stock=gtk.STOCK_CLEAR)
        gtklogger.setWidgetName(self.clear_button, 'Clear')
        gtklogger.connect(self.clear_button, "clicked", self.clearCB)
        tooltips.set_tooltip_text(self.clear_button,
                             'Reset selection by clearing'
                             ' the current selection.')        
        self.undoredoline.pack_start(self.clear_button, expand=1, fill=0)

        self.invert_button = gtk.Button("Invert")
        gtklogger.setWidgetName(self.invert_button, 'Invert')
        gtklogger.connect(self.invert_button, "clicked", self.invertCB)
        tooltips.set_tooltip_text(self.invert_button,
                             'Toggle the current selection.')
        self.undoredoline.pack_start(self.invert_button, expand=1, fill=0)
        
        self.vbox.pack_start(self.undoredoline, expand=0, fill=0, padding=2)

        # Add all the action and history widgets.  They do not
        # all get shown, see this class's "show" routine for the drill.
        for modeobj in parent.modedict.values():
            self.actionbox.pack_start(modeobj.factory.gtk, expand=1, fill=1)
            self.historyline.pack_start(modeobj.historybox.gtk,
                                        expand=0, fill=0)

        self.sensitize()

    def activemode(self):
        return self.parent.activemode
    
    # Check the current index, and show the appropriate factory
    # and historybox.
    def show(self):
        debug.mainthreadTest()
        self.gtk.show()
        self.vbox.show()
        self.actionbox.show()
        self.historyline.show()
        for mode in self.parent.modedict.values():
            mode.historybox.gtk.hide()
            mode.factory.gtk.hide()
        self.activemode().historybox.gtk.show_all()
        self.activemode().factory.gtk.show_all()
        self.undoredoline.show_all()
        

    # Show the correct factory in the actionbox, put the right
    # historybox up, and sensitize everything.
    def pickerCB(self, mode):
        debug.mainthreadTest()
        for v in self.parent.modedict.values():
            v.historybox.gtk.hide()
            v.factory.gtk.hide()
        mode.factory.gtk.show_all()
        mode.historybox.gtk.show_all()
        mode.historybox.sensitize()
        self.gtk.set_label(mode.name() + ' Selection Operations')
        self.new_skeleton(self.parent.getCurrentSkeleton())
        

    # Called from the parent when the mesh widget state changes,
    # and also from pickerCB when the picker changes the mode.
    def new_skeleton(self, skelcontext):
        self.sensitize()
        for v in self.parent.modedict.values():
            v.ok_sensitize()

    def currentSelection(self):
        skelcontext = self.parent.getCurrentSkeleton()
        if skelcontext is not None:
            return self.activemode().getSelectionContext(skelcontext)

    # Callback from the current HistoryBox's OK button.  All the
    # historyboxes are connected to this, but only the current one can
    # have sent the signal, so it's the only one operated on.
    def okCB(self, gtkobj):
        mod = self.activemode().factory.getRegistration()
        if mod is not None:
            self.activemode().factory.set_defaults()
            menuitem = getattr(self.activemode().getSelectionMenu(),
                               utils.space2underscore(mod.name()) )
            skelpath = self.parent.getCurrentSkeletonName()

            # Set the skeleton parameter and call the registered class.
            menuitem.callWithDefaults(skeleton=skelpath)
            
    # Called when the historian switches to a new object. 
    def setCB(self, object):
        self.activemode().factory.set(object,interactive=True)
        self.activemode().historybox.sensitize()

    def undoCB(self, gtkobj):
        skelpath = self.parent.getCurrentSkeletonName()
        self.activemode().getSelectionMenu().Undo(skeleton=skelpath)

    def redoCB(self, gtkobj):
        skelpath = self.parent.getCurrentSkeletonName()
        self.activemode().getSelectionMenu().Redo(skeleton=skelpath)

    def clearCB(self, gtkobj):
        skelpath = self.parent.getCurrentSkeletonName()
        self.activemode().getSelectionMenu().Clear(skeleton=skelpath)

    def invertCB(self, gtkobj):
        skelpath = self.parent.getCurrentSkeletonName()
        self.activemode().getSelectionMenu().Invert(skeleton=skelpath)

    # Check the current selection object, and sensitize the selection
    # buttons accordingly.
    def sensitize(self):
        current_selection = self.currentSelection()
        skelcontext = self.parent.getCurrentSkeleton()
        subthread.execute(self.sensitize_subthread, (skelcontext,
                                                     current_selection) )

    def sensitize_subthread(self, skelcontext, current_selection):
        debug.subthreadTest()
        # Locks are only allowed on the subthread, but GUI updates
        # must be on the main thread.
        (c, u, i, r) = (0, 0, 0, 0)
        if skelcontext is not None and current_selection is not None:
            current_selection.begin_reading()
            if not skelcontext.defunct():
                try:
                    c = current_selection.clearable()
                    u = current_selection.undoable()
                    i = current_selection.invertable()
                    r = current_selection.redoable()
                finally:
                    current_selection.end_reading()

        mainthread.runBlock(self._set_buttons, (skelcontext, c,u,i,r))
            
    def _set_buttons(self, skelcontext, c,u,i,r):
        skelok = (skelcontext is not None and not skelcontext.query_reservation()
                  and not skelcontext.defunct())
        self.clear_button.set_sensitive(c and skelok)
        self.undo_button.set_sensitive(u and skelok)
        self.invert_button.set_sensitive(i and skelok)
        self.redo_button.set_sensitive(r and skelok)
        self.activemode().historybox.sensitize()
        self.activemode().ok_sensitize()
        gtklogger.checkpoint("skeleton selection page selection sensitized")
        
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class HistoryBox:
    def __init__(self, set_callback, ok_callback):
        debug.mainthreadTest()
        self.gtk = gtk.HBox()
        self.set_callback = set_callback
        self.historian = historian.Historian(self.setCB, self.sensitize)

        # Buttons:  Previous, OK, and next.
        self.prevbutton = gtkutils.prevButton()
        gtklogger.connect(self.prevbutton, "clicked", self.historian.prevCB)
        tooltips.set_tooltip_text(self.prevbutton,
                  "Recall the previous selection modification operation.")
        self.gtk.pack_start(self.prevbutton, expand=0, fill=0, padding=2)

        self.okbutton = gtk.Button(stock=gtk.STOCK_OK)
        gtklogger.setWidgetName(self.okbutton, 'OK')
        gtklogger.connect(self.okbutton, "clicked", ok_callback)
        self.gtk.pack_start(self.okbutton, expand=1, fill=1, padding=2)
        tooltips.set_tooltip_text(self.okbutton,
                             "Perform the selection modification operation.")
        self.okbutton.set_sensitive(0)
        
        self.nextbutton = gtkutils.nextButton()
        gtklogger.connect(self.nextbutton, "clicked", self.historian.nextCB)
        tooltips.set_tooltip_text(self.nextbutton,
                  "Recall the next selection modification operation.")
        self.gtk.pack_start(self.nextbutton, expand=0, fill=0, padding=2)
        
        
    def setCB(self, object):
        if self.set_callback:
            self.set_callback(object)

            
    def sensitize(self):
        debug.mainthreadTest()
        self.nextbutton.set_sensitive(self.historian.nextSensitive())
        self.prevbutton.set_sensitive(self.historian.prevSensitive())
            
########

ssp = SkeletonSelectionPage()
