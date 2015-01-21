# -*- python -*-
# $RCSfile: microstructurePage.py,v $
# $Revision: 1.98.2.9 $
# $Author: langer $
# $Date: 2013/11/15 22:03:17 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.SWIG.common import lock
from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import mainthread
from ooflib.common import microstructure
from ooflib.common import subthread
from ooflib.common.IO import mainmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import reporter
from ooflib.common.IO import whoville
from ooflib.common.IO.GUI import chooser
from ooflib.common.IO.GUI import fixedwidthtext
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import gtkutils
from ooflib.common.IO.GUI import mainmenuGUI
from ooflib.common.IO.GUI import oofGUI
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import whowidget
from ooflib.common.IO.GUI import tooltips
import gtk
import pango
from types import *
import sys

if config.dimension()==2:
    pixstring = "pixel"
    Pixstring = "Pixel"
elif config.dimension()==3:
    pixstring = "voxel"
    Pixstring = "Voxel"

class MicrostructurePage(oofGUI.MainPage):
    def __init__(self):
        debug.mainthreadTest()
        self.built = False

        oofGUI.MainPage.__init__(
            self, name="Microstructure", ordering=10,
            tip="Define Microstructure and %s Group objects."%Pixstring)

        vbox = gtk.VBox(spacing=2)
        self.gtk.add(vbox)

        align = gtk.Alignment(xalign=0.5)
        vbox.pack_start(align, expand=0, fill=0)
        centerbox = gtk.HBox()
        align.add(centerbox)
        label=gtk.Label('Microstructure=')
        label.set_alignment(1.0, 0.5)
        centerbox.pack_start(label, expand=0, fill=0)
        self.mswidget = whowidget.WhoWidget(microstructure.microStructures,
                                            callback=self.msCB)
        centerbox.pack_start(self.mswidget.gtk[0], expand=0, fill=0)
        
        align = gtk.Alignment(xalign=0.5) # first row of ms buttons
        vbox.pack_start(align, expand=0, fill=0)
        self.newbuttonbox = gtk.HBox(homogeneous=0, spacing=3)
        align.add(self.newbuttonbox)

        self.newbutton = gtkutils.StockButton(gtk.STOCK_NEW, 'New...')
        gtklogger.setWidgetName(self.newbutton, "New")
        gtklogger.connect(self.newbutton,'clicked', self.newEmptyCB)
        tooltips.set_tooltip_text(
            self.newbutton,
            "Create a new microstructure that is NOT associated with images.")
        self.newbuttonbox.pack_start(self.newbutton, expand=1, fill=1)
        
        # Other buttons can be added to the row of "New" buttons by
        # other modules.  When they're added, by addNewButton(), a
        # function can be specified for sensitizing the button.  This
        # is the list of those functions:
        self.sensitizeFns = []

        # Other modules can contribute strings to be displayed on the
        # info page.  This is the list of
        # MicrostructurePageInfoPlugIns that retrieve those strings.
        self.infoplugins = []

        align = gtk.Alignment(xalign=0.5) # second row of ms buttons
        vbox.pack_start(align, expand=0, fill=0)
        centerbox = gtk.HBox(homogeneous=1, spacing=3)
        align.add(centerbox)

        self.renamebutton = gtkutils.StockButton(gtk.STOCK_EDIT, 'Rename...')
        gtklogger.setWidgetName(self.renamebutton, "Rename")
        gtklogger.connect(self.renamebutton, 'clicked', self.renameMSCB)
        self.renamebutton.set_sensitive(0)
        tooltips.set_tooltip_text(self.renamebutton,
                             "Rename the current microstructure.")
        centerbox.pack_start(self.renamebutton, expand=1, fill=1)

        self.copybutton = gtkutils.StockButton(gtk.STOCK_COPY, 'Copy...')
        gtklogger.setWidgetName(self.copybutton, "Copy")
        gtklogger.connect(self.copybutton, 'clicked', self.copyMSCB)
        self.copybutton.set_sensitive(0)
        tooltips.set_tooltip_text(self.copybutton,
                             "Copy the current microstructure.")        
        centerbox.pack_start(self.copybutton, expand=1, fill=1)

        self.deletebutton = gtkutils.StockButton(gtk.STOCK_DELETE, 'Delete')
        gtklogger.setWidgetName(self.deletebutton, "Delete")
        gtklogger.connect(self.deletebutton, 'clicked', self.deleteMSCB)
        self.deletebutton.set_sensitive(0)
        tooltips.set_tooltip_text(self.deletebutton,
                             "Delete the current microstructure.")
        centerbox.pack_start(self.deletebutton, expand=1, fill=1)

        self.savebutton = gtkutils.StockButton(gtk.STOCK_SAVE, 'Save...')
        gtklogger.setWidgetName(self.savebutton, "Save")
        gtklogger.connect(self.savebutton, 'clicked', self.saveMSCB)
        self.savebutton.set_sensitive(0)
        tooltips.set_tooltip_text(self.savebutton,
                             "Save the current microstructure to a file.")
        centerbox.pack_start(self.savebutton, expand=1, fill=1)

        pane = gtk.HPaned()
        gtklogger.setWidgetName(pane, "Pane")
        vbox.pack_start(pane, expand=1, fill=1, padding=2)
        gtklogger.connect_passive(pane, 'notify::position')

        #######
        
        infoframe = gtk.Frame('Microstructure Info')
        infoframe.set_shadow_type(gtk.SHADOW_IN)
        pane.pack1(infoframe, resize=True, shrink=False)
        scroll = gtk.ScrolledWindow()
        gtklogger.logScrollBars(scroll, "InfoFrameScroll")
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scroll.set_shadow_type(gtk.SHADOW_IN)
        infoframe.add(scroll)
        self.infoarea = fixedwidthtext.FixedWidthTextView()
        self.infoarea.set_editable(0)
        self.infoarea.set_cursor_visible(False)
        self.infoarea.set_wrap_mode(gtk.WRAP_WORD)
        scroll.add(self.infoarea)
        
        ########

        self.grouplock = lock.Lock()
        groupframe = gtk.Frame('%s Groups'%Pixstring)
        gtklogger.setWidgetName(groupframe, "%sGroups"%Pixstring)
        groupframe.set_shadow_type(gtk.SHADOW_IN)
        pane.pack2(groupframe, resize=True, shrink=False)
        hbox = gtk.HBox()
        groupframe.add(hbox)
        vbox = gtk.VBox(spacing=2)      # buttons on L side of pixel group list
        hbox.pack_start(vbox, expand=0, fill=0, padding=2)
        frame = gtk.Frame()              # frame for the list of groups
        frame.set_shadow_type(gtk.SHADOW_IN)
        hbox.pack_start(frame)
        grparea = gtk.VBox()
        frame.add(grparea)
        # only one of grplist and grpmsg is visible at a time
        self.grplist = chooser.ScrolledChooserListWidget( # list of pixel groups
            callback=self.listItemChosen, name="GroupList")
        grparea.add(self.grplist.gtk)
        self.grpmsg = gtk.Label()       # helpful message when there are no grps
        grparea.add(self.grpmsg)

        self.newgroupbutton = gtk.Button('New...')
        gtklogger.setWidgetName(self.newgroupbutton, "New")
        vbox.pack_start(self.newgroupbutton, expand=0, fill=0)
        gtklogger.connect(self.newgroupbutton, 'clicked', self.newGroupButtonCB)
        self.newgroupbutton.set_sensitive(0)
        tooltips.set_tooltip_text(
            self.newgroupbutton,
            "Create a new empty %s group in the current microstructure."
            % pixstring)

        self.renamegroupbutton = gtk.Button('Rename...')
        gtklogger.setWidgetName(self.renamegroupbutton, "Rename")
        vbox.pack_start(self.renamegroupbutton, expand=0, fill=0)
        gtklogger.connect(self.renamegroupbutton, 'clicked',
                         self.renameGroupButtonCB)
        self.renamegroupbutton.set_sensitive(0)
        tooltips.set_tooltip_text(self.renamegroupbutton,
                             "Rename the selected %s group." % pixstring)

        self.copygroupbutton = gtk.Button('Copy...')
        gtklogger.setWidgetName(self.copygroupbutton, "Copy")
        vbox.pack_start(self.copygroupbutton, expand=0, fill=0)
        gtklogger.connect(self.copygroupbutton, 'clicked',
                         self.copyGroupButtonCB)
        self.copygroupbutton.set_sensitive(0)
        tooltips.set_tooltip_text(
            self.copygroupbutton,
            "Create a new group containing the same %ss as the selected group."
            % pixstring)

        self.delgroupbutton = gtk.Button('Delete')
        gtklogger.setWidgetName(self.delgroupbutton, "Delete")
        vbox.pack_start(self.delgroupbutton, expand=0, fill=0)
        gtklogger.connect(self.delgroupbutton, 'clicked',
                         self.deleteGroupButtonCB)
        self.delgroupbutton.set_sensitive(0)
        tooltips.set_tooltip_text(
            self.delgroupbutton,
            "Delete the selected %s group from the microstructure." % pixstring)

        self.meshablebutton = gtk.CheckButton('Meshable')
        gtklogger.setWidgetName(self.meshablebutton, "Meshable")
        vbox.pack_start(self.meshablebutton, expand=0, fill=0)
        self.meshablesignal = gtklogger.connect(self.meshablebutton, 'clicked',
                                                self.meshableGroupCB)
        self.meshablebutton.set_sensitive(0)
        tooltips.set_tooltip_text(
            self.meshablebutton,
            "Should adaptive meshes follow the boundaries of the selected %s group?" % pixstring)


        # buttons on rhs of pixelgroup list
        vbox = gtk.VBox(spacing=2)
        hbox.pack_start(vbox, expand=0, fill=0, padding=2)

        self.addbutton = gtk.Button('Add')
        gtklogger.setWidgetName(self.addbutton, "Add")
        vbox.pack_start(self.addbutton, expand=0, fill=0)
        gtklogger.connect(self.addbutton, 'clicked', self.addPixelsCB)
        self.addbutton.set_sensitive(0)
        tooltips.set_tooltip_text(
            self.addbutton,
            "Add the currently selected %ss to the selected group." % pixstring)

        self.removebutton = gtk.Button('Remove')
        gtklogger.setWidgetName(self.removebutton, "Remove")
        vbox.pack_start(self.removebutton, expand=0, fill=0)
        gtklogger.connect(self.removebutton, 'clicked', self.removePixelsCB)
        self.removebutton.set_sensitive(0)
        tooltips.set_tooltip_text(
            self.removebutton,
            "Remove the currently selected %ss from the selected group."
            % pixstring)

        self.clearbutton = gtk.Button('Clear')
        gtklogger.setWidgetName(self.clearbutton, "Clear")
        vbox.pack_start(self.clearbutton, expand=0, fill=0)
        gtklogger.connect(self.clearbutton, 'clicked', self.clearPixelsCB)
        self.clearbutton.set_sensitive(0)
        tooltips.set_tooltip_text(
            self.clearbutton,
            "Reset the selected group by removing all the %ss from the group."
            % pixstring)
        
        self.infobutton = gtk.Button('Info')
        gtklogger.setWidgetName(self.infobutton, "Info")
        vbox.pack_start(self.infobutton, expand=0, fill=0)
        gtklogger.connect(self.infobutton, 'clicked', self.queryPixelsCB)
        self.infobutton.set_sensitive(0)
        tooltips.set_tooltip_text(
            self.infobutton,
            "Display information about the selected group in the Messages window.")        

        self.built = True

        self.sbcallbacks = [
            switchboard.requestCallback('new pixel group', self.newpixgrp),
            switchboard.requestCallback('destroy pixel group', self.destpixgrp),
            #
            switchboard.requestCallback('changed pixel group', self.destpixgrp),
            switchboard.requestCallback('changed pixel groups', self.chngdgrps),
            switchboard.requestCallback(('new who', 'Microstructure'),
                                        self.newwhoMS),
            switchboard.requestCallback(('new who', 'Image'), self.newwhoImage),
            switchboard.requestCallback(('rename who', 'Image'),
                                        self.displayMSInfo),
            switchboard.requestCallback('remove who', self.removewho),
            switchboard.requestCallback('renamed pixel group',
                                        self.renamepixgrp),
            switchboard.requestCallback('pixel selection changed',
                                        self.selectionchanged),
            switchboard.requestCallback(
            'images changed in microstructure', self.displayMSInfo)
            ]
        # Don't call redisplay_all here!  It would be called before
        # the main gtk loop starts, so the mainthread/subthread
        # mechanism won't be in place, and the grouplock will complain
        # about potential deadlocking.

    def redisplay_all(self):
        self.rebuild_grouplist()        # hides either grplist or grpmsg.
        self.displayMSInfo()
        self.sensitize()

    def installed(self):
        ## Obsolete comment that may still be relevant... The old
        ## "shown" routine is now called "installed".  The default
        ## "show" method just calls self.gtk.show_all().
        # If redisplay_all is called by show() rather than by shown()
        # it can be called by gui start up code, which may be running
        # concurrently with other start up operations, including
        # gtklogging initialization.  If that happens, the recording
        # of checkpoints reached by redisplay_all will depend on race
        # conditions.  So redisplay_all must be called by shown(),
        # which is guaranteed (more likely?) to be called after gui
        # initialization is complete.
        subthread.execute(self.redisplay_all)
        
    def currentMSName(self):
        return mainthread.runBlock(self.mswidget.get_value)

    def currentMScontext(self):
        msname = self.currentMSName()
        if msname:
            try:
                return microstructure.microStructures[msname]
            except KeyError:
                return None

    def currentMS(self):
        ctxt = self.currentMScontext()
        if ctxt:
            return ctxt.getObject()
        
    def currentGroupName(self):
        return mainthread.runBlock(self.grplist.get_value)

    def currentGroup(self):
        name = self.currentGroupName()
        if name:
            ms = self.currentMS()
            if ms is not None:
                return ms.findGroup(name)

    def rebuild_grouplist(self):
        debug.subthreadTest()
        mscontext = self.currentMScontext()
        msg = None
        if mscontext is not None:
            mscontext.begin_reading()
            ms = mscontext.getObject()
            try:
                if ms.nGroups() > 0:
                    grpnames = ms.groupNames()
                    dispnames = grpnames[:]
                    for i in range(len(grpnames)):
                        grpname = grpnames[i]
                        grp = ms.findGroup(grpname)
                        dispnames[i] += " (%d %s%s" % (len(grp), pixstring,
                                                          "s"*(len(grp)!=1))
                        if grp.is_meshable():
                            dispnames[i] += ", meshable)"
                        else:
                            dispnames[i] += ")"
                else:
                    msg = 'No %s groups defined!'%pixstring
            finally:
                mscontext.end_reading()
        else:                           # ms is None
            msg = 'No Microstructure defined!'
        if msg:
            mainthread.runBlock(self.set_group_message, (msg,))
        else:
            mainthread.runBlock(self.set_group_list, (grpnames, dispnames))
        self.setMeshableButton()

    def set_group_message(self, msg):
        debug.mainthreadTest()
        self.grpmsg.set_text(msg)
        self.grplist.update([])
        self.grplist.hide()
        self.grpmsg.show()
    def set_group_list(self, grpnames, dispnames=[]):
        debug.mainthreadTest()
        self.grplist.update(grpnames, dispnames)
        self.grplist.show()
        self.grpmsg.hide()

    def addNewButton(self, gtkobj, sensitizefn):
        debug.mainthreadTest()
        self.newbuttonbox.pack_start(gtkobj, expand=1, fill=1)
        gtkobj.show()
        if sensitizefn is not None:
            self.sensitizeFns.append(sensitizefn)

    def addMicrostructureInfo(self, msinfoplugin):
        self.infoplugins.append(msinfoplugin)
        self.infoplugins.sort()
        return msinfoplugin

    def displayMSInfo(self, *args):
        # *args is given because this is used as a switchboard
        # callback for ('rename who', 'Image') as well as being called
        # directly.  This indicates either slovenliness or efficiency
        # on the part of the programmer.
        debug.subthreadTest()
        mscontext = self.currentMScontext()
        text = ""
        if mscontext is not None:
            mscontext.begin_reading()
            try:
                ms = mscontext.getObject()
                size = ms.sizeInPixels()
                if config.dimension() == 2:
                    text += 'Pixel size: %dx%d\n' % (size.x, size.y)
                    size = ms.size()
                    text += 'Physical size: %gx%g\n' % (size.x, size.y)
                elif config.dimension() == 3:
                    text += 'Voxel size: %dx%dx%d\n' % (size.x, size.y, size.z)
                    size = ms.size()
                    text += 'Physical size: %gx%gx%g\n' % (size.x, size.y, size.z)
                imagenames = ms.imageNames()
                if imagenames:
                    text += 'Images:\n'
                    for name in imagenames:
                        text += '  ' + name + '\n'
                for infoplugin in self.infoplugins:
                    plugintext = infoplugin(mscontext)
                    if plugintext:
                        text += plugintext + '\n'
            finally:
                mscontext.end_reading()
        mainthread.runBlock(self.infoarea.get_buffer().set_text, (text,))

    def setMeshableButton(self):
        debug.subthreadTest()
        mscontext = self.currentMScontext()
        if mscontext:
            mscontext.begin_reading()
            try:
                grp = self.currentGroup()
                meshable = grp is not None and grp.is_meshable()
            finally:
                mscontext.end_reading()
        else:
            meshable = False
        mainthread.runBlock(self.setMeshableButton_thread, (meshable,))
    def setMeshableButton_thread(self, meshable):
        debug.mainthreadTest()
        self.meshablesignal.block()
        self.meshablebutton.set_active(meshable)
        self.meshablesignal.unblock()
        gtklogger.checkpoint("meshable button set")

    def sensitize(self):
        debug.subthreadTest()
        ms = self.currentMS()
        msctxt = self.currentMScontext()
        ms_available = (ms is not None)
        grp = self.currentGroup()
        grp_selected = (grp is not None) and ms_available
        nonemptygrp = False
        pixelsselected = False
        if msctxt:
            msctxt.begin_reading() # Length of group; uses shared data.
            try:
                nonemptygrp = grp_selected and len(grp) > 0
                pixelsselected = ms_available and not ms.pixelselection.empty()
            finally:
                msctxt.end_reading()
        mainthread.runBlock(self.sensitize_thread,
                            (ms_available, grp_selected, pixelsselected,
                             nonemptygrp))
    def sensitize_thread(self, ms_available, grp_selected, pixelsselected,
                         nonemptygrp):
        debug.mainthreadTest()
        self.renamebutton.set_sensitive(ms_available)
        self.copybutton.set_sensitive(ms_available)
        self.deletebutton.set_sensitive(ms_available)
        self.savebutton.set_sensitive(ms_available)

        self.newgroupbutton.set_sensitive(ms_available)
        self.renamegroupbutton.set_sensitive(grp_selected)
        self.copygroupbutton.set_sensitive(grp_selected)
        self.delgroupbutton.set_sensitive(grp_selected)
        self.meshablebutton.set_sensitive(grp_selected)
        self.infobutton.set_sensitive(grp_selected)

        self.addbutton.set_sensitive(grp_selected and pixelsselected)
        self.removebutton.set_sensitive(grp_selected and pixelsselected)
        self.clearbutton.set_sensitive(nonemptygrp)

        for fn in self.sensitizeFns:
            fn()
        gtklogger.checkpoint("microstructure page sensitized")

    def selectionchanged(self, who): # switchboard 'pixel selection changed'
        self.sensitize()

    ###############################

    def renameMSCB(self, button):
        menuitem = mainmenu.OOF.Microstructure.Rename
        namearg = menuitem.get_arg('name')
        namearg.value = self.currentMSName()
        if parameterwidgets.getParameters(
            namearg,
            title='Rename Microstructure '+self.currentMSName()):
            menuitem.callWithDefaults(microstructure=self.currentMSName())

    def copyMSCB(self, button):
        menuitem = mainmenu.OOF.Microstructure.Copy
        namearg = menuitem.get_arg('name')
        if parameterwidgets.getParameters(namearg, title='Copy microstructure'):
            menuitem.callWithDefaults(microstructure=self.currentMSName())

    def deleteMSCB(self, button):
        if reporter.query("Really delete %s?" % self.currentMSName(),
                          "No", default="Yes") == "Yes":
            mainmenu.OOF.Microstructure.Delete(
                microstructure=self.currentMSName())

    def listItemChosen(self, name, interactive): # Chooser callback
        if self.built:
            subthread.execute(self.listItemChosen_thread, (name,))
    def listItemChosen_thread(self, name):
        self.grouplock.acquire()
        try:
            self.sensitize()
            self.setMeshableButton()
        finally:
            self.grouplock.release()
        
    def newpixgrp(self, group):  # switchboard callback 'new pixel group'
        self.grouplock.acquire()
        try:
            self.rebuild_grouplist()
            # This makes the newly added pixel group automatically selected.
            mainthread.runBlock(self.grplist.set_selection, (group.name(),))
            self.setMeshableButton()
            self.sensitize()
        finally:
            self.grouplock.release()

    def destpixgrp(self, group, ms_name):
        # switchboard 'destroy pixel group' or 'changed pixel group'
        self.grouplock.acquire()
        try:
            if ms_name==self.currentMSName():
                self.rebuild_grouplist()
                self.setMeshableButton()
                self.sensitize()
        finally:
            self.grouplock.release()
    def chngdgrps(self, ms_name):       # 'changed pixel groups'
        self.grouplock.acquire()
        try:
            if ms_name == self.currentMSName():
                self.rebuild_grouplist()
                self.setMeshableButton()
                self.sensitize()
        finally:
            self.grouplock.release()
    
    def newwhoMS(self, whoname): # switchboard ('new who', 'Microstructure')
        # whoname is a list of strings
        self.grouplock.acquire()
        try:
            mainthread.runBlock(self.mswidget.set_value, (whoname,))
            self.rebuild_grouplist()
            self.setMeshableButton()
            self.displayMSInfo()
            self.sensitize()
        finally:
            self.grouplock.release()

    def newwhoImage(self, whoname):     # switchboard ('new who', 'Image')
        self.displayMSInfo()            # displays image name
        self.sensitize()

    def removewho(self, whoclassname, whoname): # switchboard 'remove who'
        if whoclassname == 'Microstructure':
            self.grouplock.acquire()
            try:
                self.rebuild_grouplist()
                self.setMeshableButton()
                self.displayMSInfo()
                self.sensitize()
            finally:
                self.grouplock.release()
        elif whoclassname == 'Image':
            self.sensitize()

    def msCB(self, *args):              # whowidget callback
        subthread.execute(self.redisplay_all)

    def newEmptyCB(self, *args):
        menuitem = mainmenu.OOF.Microstructure.New
        if parameterwidgets.getParameters(title='Create Microstructure',
                                          *menuitem.params):
            menuitem.callWithDefaults()

    def newGroupButtonCB(self, button):
        menuitem = mainmenu.OOF.PixelGroup.New
        nameparam = menuitem.get_arg('name')
        if parameterwidgets.getParameters(nameparam,
                                          title='Create new %s group'%pixstring):
            menuitem.callWithDefaults(microstructure=self.currentMSName())

    def renameGroupButtonCB(self, button):
        menuitem = mainmenu.OOF.PixelGroup.Rename
        nameparam = menuitem.get_arg('new_name')
        nameparam.value = self.currentGroupName()
        if parameterwidgets.getParameters(
            nameparam,
            title = 'Rename %sgroup '%pixstring + self.currentGroupName()):
            menuitem.callWithDefaults(
                microstructure=self.currentMSName(),
                group=self.currentGroupName())

    def renamepixgrp(self, group, oldname, newname):
        # switchboard 'rename pixel group'
        debug.subthreadTest()
        self.grouplock.acquire()
        try:
            mscontext = self.currentMScontext()
            if mscontext:
                mscontext.begin_reading()
                try:
                    ms = mscontext.getObject()
                    ok = group.name() in ms.groupNames()
                finally:
                    mscontext.end_reading()
                if ok:
                    # Ensure that the new pixel group is selected.
                    self.rebuild_grouplist()
                    mainthread.runBlock(self.grplist.set_selection, (newname,))
                    self.sensitize()
        finally:
            self.grouplock.release()

    def deleteGroupButtonCB(self, button):
        if reporter.query("Really delete %s?" % self.currentGroupName(),
                          "No", default="Yes") == "Yes":
            mainmenu.OOF.PixelGroup.Delete(microstructure=self.currentMSName(),
                                           group=self.currentGroupName())

    def copyGroupButtonCB(self, button):
        menuitem = mainmenu.OOF.PixelGroup.Copy
        nameparam = menuitem.get_arg('name')
        if parameterwidgets.getParameters(
            nameparam,
            title='Copy group '+self.currentGroup().name()):
            menuitem.callWithDefaults(microstructure=self.currentMSName(),
                                      group=self.currentGroupName())

    def meshableGroupCB(self, button):
        self.meshablesignal.block()
        mainmenu.OOF.PixelGroup.Meshable(microstructure=self.currentMSName(),
                                group=self.currentGroupName(),
                                meshable=self.meshablebutton.get_active())
        self.meshablesignal.unblock()

    def addPixelsCB(self, button):
        mainmenu.OOF.PixelGroup.AddSelection(microstructure=self.currentMSName(),
                                    group=self.currentGroupName())

    def removePixelsCB(self, button):
        mainmenu.OOF.PixelGroup.RemoveSelection(microstructure=self.currentMSName(),
                                       group=self.currentGroupName())

    def clearPixelsCB(self, button):
        mainmenu.OOF.PixelGroup.Clear(microstructure=self.currentMSName(),
                             group=self.currentGroupName())

    def queryPixelsCB(self, button):
        mainmenu.OOF.PixelGroup.Query(microstructure=self.currentMSName(),
                             group=self.currentGroupName())

    def saveMSCB(self, button):
        menuitem = mainmenu.OOF.File.Save.Microstructure
        msname = self.currentMSName()
        if parameterwidgets.getParameters(
            menuitem.get_arg('filename'),
            menuitem.get_arg('mode'),
            menuitem.get_arg('format'),
            title="Save Microstructure '%s'" % msname):
            menuitem.callWithDefaults(microstructure=msname)

mp = MicrostructurePage()

#######################################

## Extension mechanisms

# Add a button (or any other gtk widget) to the row of "New..."
# buttons.  sensitizefn will be called when the page's components are
# sensitized, and should do whatever's appropriate to the new widget.

def addNewButton(gtkobj, sensitizefn=None):
    mp.addNewButton(gtkobj, sensitizefn)

# Add more info to the info pane.  The callback will be called with
# the Microstructure context as an argument, and should return a
# string, or None.  addMicrostructureInfo returns a
# MicrostructurePageInfoPlugIn object whose update() method can be
# called to force the info pane to redraw.

def addMicrostructureInfo(callback, ordering):
    return mp.addMicrostructureInfo(MicrostructurePageInfoPlugIn(callback,
                                                                 ordering))
class MicrostructurePageInfoPlugIn:
    def __init__(self, callback, ordering):
        self.ordering = ordering
        self.callback = callback
    def __call__(self, ms):
        return self.callback(ms)
    def __cmp__(self, other):
        return cmp(self.ordering, other.ordering)
    def update(self):
        mp.displayMSInfo()

    
