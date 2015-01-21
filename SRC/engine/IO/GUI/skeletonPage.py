# -*- python -*-
# $RCSfile: skeletonPage.py,v $
# $Revision: 1.119.2.17 $
# $Author: langer $
# $Date: 2014/11/05 16:54:55 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import labeltree
from ooflib.common import mainthread
from ooflib.common import subthread
from ooflib.common.IO import mainmenu
from ooflib.common.IO import parameter, reporter
from ooflib.common.IO import whoville
from ooflib.common.IO.GUI import fixedwidthtext
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import gtkutils
from ooflib.common.IO.GUI import historian
from ooflib.common.IO.GUI import oofGUI
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import regclassfactory
from ooflib.common.IO.GUI import tooltips
from ooflib.common.IO.GUI import whowidget
from ooflib.engine import skeletoncontext
from ooflib.SWIG.engine import cskeletonmodifier
import gtk
import pango

## TODO: Display average shape energy for skeleton.  Allow user to
## choose if shape energy should be weighted by volume or not?  Same
## for homogeneity?

# Define some convenience variables.
OOF = mainmenu.OOF
skeletonmenu = mainmenu.OOF.Skeleton
SkeletonModifier = cskeletonmodifier.CSkeletonModifier
itORthem = ["it", "them"]

class SkeletonPage(oofGUI.MainPage):
    def __init__(self):
        self.postponed_update = False
        oofGUI.MainPage.__init__(self, name="Skeleton", ordering=120,
                                 tip='Construct and modify mesh skeletons')

        mainbox = gtk.VBox(spacing=2)
        self.gtk.add(mainbox)

        align = gtk.Alignment(xalign=0.5)
        mainbox.pack_start(align, expand=0, fill=0)
        centerbox = gtk.HBox(spacing=3)
        align.add(centerbox)
        self.skelwidget = whowidget.WhoWidget(whoville.getClass('Skeleton'),
                                              scope=self)
        label = gtk.Label('Microstructure=')
        label.set_alignment(1.0, 0.5)
        centerbox.pack_start(label, expand=0, fill=0)
        centerbox.pack_start(self.skelwidget.gtk[0], expand=1, fill=1)
        label = gtk.Label('Skeleton=')
        label.set_alignment(1.0, 0.5)
        centerbox.pack_start(label, expand=0, fill=0)
        centerbox.pack_start(self.skelwidget.gtk[1], expand=1, fill=1)

        # Centered box of buttons
        align = gtk.Alignment(xalign=0.5)
        mainbox.pack_start(align, expand=0, fill=0)
        bbox = gtk.HBox(homogeneous=1, spacing=3)
        align.add(bbox)

        self.newbutton = gtkutils.StockButton(gtk.STOCK_NEW, 'New...')
        gtklogger.setWidgetName(self.newbutton, "New")
        gtklogger.connect(self.newbutton, 'clicked', self.new_skeleton_CB)
        tooltips.set_tooltip_text(self.newbutton, "Create a new skeleton from the current microstructure.")
        bbox.pack_start(self.newbutton, expand=1, fill=1)
        
        self.simplebutton = gtk.Button('Simple...')
        gtklogger.setWidgetName(self.simplebutton, "Simple")
        gtklogger.connect(self.simplebutton, 'clicked', self.simple_skeleton_CB)
        tooltips.set_tooltip_text(self.simplebutton, "Create a new skeleton from the current microstructure in a naive fashion, by creating one quadrilateral or two triangular elements per pixel.  Material boundaries will be inherently jagged, which may cause errors in finite element solutions.")
        bbox.pack_start(self.simplebutton, expand=1, fill=1)

        ## TODO 3.1: Implement AutoSkeleton and uncomment this.
        # self.autobutton = gtk.Button('Auto...')
        # gtklogger.setWidgetName(self.autobutton, 'Auto')
        # gtklogger.connect(self.autobutton, 'clicked', self.autoCB)
        # tooltips.set_tooltip_text(self.autobutton, "Create and automatically refine a Skeleton.")
        # bbox.pack_start(self.autobutton, expand=1, fill=1)
        
        self.renamebutton = gtkutils.StockButton(gtk.STOCK_EDIT, 'Rename...')
        gtklogger.setWidgetName(self.renamebutton, "Rename")
        gtklogger.connect(self.renamebutton, 'clicked', self.rename_skeleton_CB)
        tooltips.set_tooltip_text(self.renamebutton, "Rename the current skeleton.")
        bbox.pack_start(self.renamebutton, expand=1, fill=1)

        self.copybutton = gtkutils.StockButton(gtk.STOCK_COPY, 'Copy...')
        gtklogger.setWidgetName(self.copybutton, 'Copy')
        gtklogger.connect(self.copybutton, 'clicked', self.copy_skeleton_CB)
        tooltips.set_tooltip_text(self.copybutton, "Copy the current skeleton.")
        bbox.pack_start(self.copybutton, expand=1, fill=1)

        self.deletebutton = gtkutils.StockButton(gtk.STOCK_DELETE, 'Delete')
        gtklogger.setWidgetName(self.deletebutton, 'Delete')
        gtklogger.connect(self.deletebutton, 'clicked', self.delete_skeletonCB)
        tooltips.set_tooltip_text(self.deletebutton, "Delete the current skeleton.")
        bbox.pack_start(self.deletebutton, expand=1, fill=1)

        self.savebutton = gtkutils.StockButton(gtk.STOCK_SAVE, 'Save...')
        gtklogger.setWidgetName(self.savebutton, "Save")
        gtklogger.connect(self.savebutton, 'clicked', self.save_skeletonCB)
        tooltips.set_tooltip_text(self.savebutton,
                             "Save the current skeleton to a file.")
        bbox.pack_start(self.savebutton, expand=1, fill=1)
        
        mainpane = gtk.HPaned()
        gtklogger.setWidgetName(mainpane, 'Pane')
        mainbox.pack_start(mainpane, expand=1, fill=1)
        gtklogger.connect_passive(mainpane, 'notify::position')

        self.skelframe = gtk.Frame(label="Skeleton Status")
        self.skelframe.set_shadow_type(gtk.SHADOW_IN)
        mainpane.pack1(self.skelframe, resize=1, shrink=0)
        scroll = gtk.ScrolledWindow()
        gtklogger.logScrollBars(scroll, "StatusScroll")
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scroll.set_shadow_type(gtk.SHADOW_IN)
        self.skelframe.add(scroll)
        self.skelinfo = fixedwidthtext.FixedWidthTextView()
        gtklogger.setWidgetName(self.skelinfo, "SkeletonText")
        self.skelinfo.set_wrap_mode(gtk.WRAP_WORD)
        self.skelinfo.set_editable(False)
        self.skelinfo.set_cursor_visible(False)
        self.boldTag = self.skelinfo.get_buffer().create_tag(
            "bold", weight=pango.WEIGHT_BOLD)
        scroll.add(self.skelinfo)

        # End of left-side of skeleton info frame.

        # Start of right-side

        skelmodframe = gtk.Frame(label="Skeleton Modification")
        gtklogger.setWidgetName(skelmodframe, 'Modification')
        skelmodframe.set_shadow_type(gtk.SHADOW_IN)
        skelmodbox = gtk.VBox(spacing=3)
        skelmodframe.add(skelmodbox)

        self.skelmod = regclassfactory.RegisteredClassFactory(
                       SkeletonModifier.registry,
                       title="method: ",
                       callback=self.skelmodCB,
                       expand=0, fill=0, scope=self, name="Method")
        self.historian = historian.Historian(self.skelmod.set,
                                             self.sensitizeHistory,
                                             compareCB=lambda x,y: x==y,
                                             setCBkwargs={'interactive':1})

        skelmodbox.pack_start(self.skelmod.gtk,expand=1,fill=1)

        # Buttons for "Previous", "OK", and "Next"
        hbox = gtk.HBox()
        self.prevskelmodbutton = gtkutils.prevButton()
        gtklogger.connect(self.prevskelmodbutton, 'clicked', self.prevskelmod)
        tooltips.set_tooltip_text(self.prevskelmodbutton,
                      'Recall the previous skeleton modification operation.')
        hbox.pack_start(self.prevskelmodbutton, expand=0, fill=0, padding=2)

        self.okbutton = gtk.Button(stock=gtk.STOCK_OK)
        gtklogger.setWidgetName(self.okbutton, 'OK')
        gtklogger.connect(self.okbutton, 'clicked', self.okskelmod)
        tooltips.set_tooltip_text(self.okbutton,
                  'Perform the skeleton modification operation defined above.')
        hbox.pack_start(self.okbutton, expand=1, fill=1, padding=5)

        self.nextskelmodbutton = gtkutils.nextButton()
        gtklogger.connect(self.nextskelmodbutton, 'clicked', self.nextskelmod)
        tooltips.set_tooltip_text(self.nextskelmodbutton,
                             'Recall the next skeleton modification operation.')
        hbox.pack_start(self.nextskelmodbutton, expand=0, fill=0, padding=2)

        skelmodbox.pack_start(hbox, expand=0, fill=0, padding=2) 

        # Buttons for "Undo", "Redo"
        hbox = gtk.HBox()
        self.undobutton = gtk.Button(stock=gtk.STOCK_UNDO)
        gtklogger.setWidgetName(self.undobutton, 'Undo')
        gtklogger.connect(self.undobutton, 'clicked', self.undoskelmod)
        tooltips.set_tooltip_text(self.undobutton,
                             'Undo the latest skeleton modification.')
        hbox.pack_start(self.undobutton, expand=1, fill=0, padding=10)

        self.redobutton = gtk.Button(stock=gtk.STOCK_REDO)
        gtklogger.setWidgetName(self.redobutton, 'Redo')
        gtklogger.connect(self.redobutton, 'clicked', self.redoskelmod)
        tooltips.set_tooltip_text(self.redobutton,
                             'Redo the latest undone skeleton modification.')
        hbox.pack_start(self.redobutton, expand=1, fill=0, padding=10)

        skelmodbox.pack_start(hbox, expand=0, fill=0, padding=2)

        mainpane.pack2(skelmodframe, resize=0, shrink=0)
        # End of right-side

        self.sbcallbacks = [
            switchboard.requestCallback("made reservation",
                                        self.update_ok_button),
            switchboard.requestCallback("cancelled reservation",
                                        self.update_ok_button),
            # "Skeleton modified" indicates that a specific modifier
            # has been applied.  "Skeleton changed" indicates that
            # something has changed, which might or might not have
            # involved a SkeletonModifier.
            switchboard.requestCallbackMain("Skeleton modified",
                                            self.recordModifier),
            switchboard.requestCallback("Skeleton changed",
                                        self.skelChangeCB),
            switchboard.requestCallback(('who changed', 'Skeleton'),
                                        self.changeSkeleton),
            switchboard.requestCallbackMain(SkeletonModifier,
                                            self.updateskelmod),
            switchboard.requestCallbackMain(("new who", "Microstructure"),
                                            self.newMicrostructure),
            switchboard.requestCallback(("new who", 'Skeleton'),
                                        self.newSkeleton),
            # Pages should catch the signal from updates to the widget
            # which don't originate on this page, e.g. deletions via
            # menu command.
            switchboard.requestCallback(self.skelwidget, self.skel_update),

            switchboard.requestCallback(('validity', self.skelmod),
                                        self.validityChangeCB)
            ]

    def installed(self):       # called by oofGUI when switching pages
        subthread.execute(self.installed_subth)
    def installed_subth(self):
        self.sensitize()
        if self.postponed_update:
            self.postponed_update = False
            self.update(self.skelwidget.get_value(), locked=False)


    def skelmodCB(self, reg):
        subthread.execute(self.skelmodCB_subthread, (reg,))

    def skelmodCB_subthread(self, reg):
        self.historian.stateChangeCB(reg)
        self.sensitize()

    def legalityCheck(self):
        reg = self.skelmod.getRegistration()
        if hasattr(reg, "ok_illegal"):
            return 1
        return not self.currentSkeleton().illegal()

    def currentMSName(self):
        path = labeltree.makePath(mainthread.runBlock(self.skelwidget.get_value,
                                                      (), {'depth':1}))
        if path:
            return path[0]

    def currentSkeletonName(self):
        path = labeltree.makePath(
            mainthread.runBlock(self.skelwidget.get_value))
        if path:
            return path[-1]

    def currentSkeletonFullName(self):
        return mainthread.runBlock(self.skelwidget.get_value)

    def currentSkeletonContext(self):
        try:
            return skeletoncontext.skeletonContexts[self.currentSkeletonFullName()]
        except KeyError:
            return None
    def currentSkeleton(self):
        ctxt = self.currentSkeletonContext()
        if ctxt:
            return ctxt.getObject()

    # def nodesMoved(self, context):      # switchboard "skeleton nodes moved"
    #     debug.fmsg("got 'skeleton nodes moved'", context.path(),
    #                self.currentSkeletonFullName())
    #     cname = context.path()
    #     if self.currentSkeletonFullName() == cname:
    #         self.update(cname, locked=False)

    # switchboard callback for "Skeleton changed", sent when pixel
    # groups or materials have changed in the microstructure, or the
    # Skeleton geometry has changed.
    def skelChangeCB(self, skel_name):
        if self.currentSkeletonFullName()==skel_name:
            self.update(skel_name, locked=False)
        
    def newSkeleton(self, whoname):     # switchboard ("new who", "Skeleton")
        self.update(whoname, locked=False)

    def skel_update(self, *args, **kwargs):  # Switchboard "self.skelwidget"
        skelname = self.currentSkeletonFullName()
        self.update(skelname, locked=False)
        
    def changeSkeleton(self, skelcontext): # sb ('who changed', "Skeleton")
        try:
            path = skelcontext.path()
        except KeyError:
            return
        if self.currentSkeletonFullName() == path:
            self.update(path, locked=True)

    def newMicrostructure(self, msname): # sb ("new who", "Microstructure")
        # Switch to a new Microstructure only if there isn't a
        # currently selected Skeleton.
        if not self.currentSkeletonFullName():
            self.skelwidget.set_value(msname)

    def recordModifier(self, path, modifier):
        if modifier:
            self.historian.record(modifier)

    def update(self, skelname, locked):
        ## TODO OPT: Is this being called too often?  If the number of
        ## calls can't be reduced, can it use timestamps to reduce the
        ## amount of work it does?  In particular, the illegalCount
        ## calculation may be expensive, and has no timestamps at the
        ## moment.
        debug.subthreadTest()
        # Most pages are updated when their info changes even if
        # they're not currently visible.  Because the Skeleton Page
        # displays the homogeneity which may be slow to compute, it's
        # not updated unless it's currently visible.
        if not self.is_current():       # not displayed in the GUI
            self.postponed_update = True
            return
        self.postponed_update = False
        skelpath = labeltree.makePath(skelname)
        if skelpath:
            skelctxt = skeletoncontext.skeletonContexts[skelpath]
            skel = skelctxt.getObject()
            ## Updating the state info is done in two stages, because
            ## the homogeneity index can take a while to compute.  In
            ## the first stage, the quick stuff is computed, and the
            ## homogeneity index is displayed as '????'. 
            if not locked:
                skelctxt.begin_reading()
            try:
                ms_name = skel.getMicrostructure().name()
                nNodes = skel.nnodes()#len(skel.nodes)
                nElements = skel.nelements() #len(skel.elements)
                nFaces = skel.nfaces()
                nSegments = skel.nsegments()
                illegalcount = skel.getIllegalCount()
                suspectcount = skel.getSuspectCount()
                shapecounts = None #skel.countShapes()
                x_periodicity = bool(skel.getPeriodicity(0)) # left right
                y_periodicity = bool(skel.getPeriodicity(1)) # top bottom
                z_periodicity = (config.dimension()==3 and
                                  bool(skel.getPeriodicity(2))) # front back
            finally:
                if not locked:
                    skelctxt.end_reading()
            mainthread.runBlock(self.writeInfoBuffer,
                                (nNodes, nElements, nFaces, nSegments, 
                                 illegalcount, suspectcount, shapecounts,
                                 None, x_periodicity, y_periodicity,
                                 z_periodicity))
            # Homogeneity Index stuff.  
            if not locked:
                skelctxt.begin_writing()
            try:
                homogIndex = skel.getHomogeneityIndex()
            finally:
                if not locked:
                    skelctxt.end_writing()
            mainthread.runBlock(self.writeInfoBuffer,
                                (nNodes, nElements, nFaces, nSegments,
                                 illegalcount, suspectcount, shapecounts,
                                 homogIndex, x_periodicity, y_periodicity,
                                 z_periodicity))
        else:
            mainthread.runBlock(self.deleteInfoBuffer)
        self.sensitize()
            
    def deleteInfoBuffer(self):
        buffer = self.skelinfo.get_buffer()
        buffer.delete(buffer.get_start_iter(), buffer.get_end_iter())
        buffer.insert(buffer.get_end_iter(),
                      "No skeleton selected.\n")

    def writeInfoBuffer(self, nNodes, nElements, nFaces, nSegments, 
                        illegalcount, suspectcount, shapecounts, homogIndex,
                        x_periodicity, y_periodicity, z_periodicity):
        # Called by update() to actually fill in the data on the
        # main thread.
        debug.mainthreadTest()
        buffer = self.skelinfo.get_buffer()
        buffer.delete(buffer.get_start_iter(), buffer.get_end_iter())
        if illegalcount > 0 :
            buffer.insert_with_tags(buffer.get_end_iter(),
                                    "WARNING: %d ILLEGAL ELEMENT%s.\n" %
                                    (illegalcount, "S"*(illegalcount!=1)),
                                    self.boldTag)
            buffer.insert(buffer.get_end_iter(),
                          "Element data is unreliable.\n")

            buffer.insert(buffer.get_end_iter(),
                          "Remove %s before proceeding.\n\n"
                          % itORthem[illegalcount!=1])
        if suspectcount > 0 :
            buffer.insert_with_tags(buffer.get_end_iter(),
                                    "WARNING: %d SUSPECT ELEMENT%s.\n" %
                                    (suspectcount, "S"*(suspectcount!=1)),
                                    self.boldTag)
            buffer.insert(buffer.get_end_iter(),
                          "Refinement cannot be performed reliably.\n")

            buffer.insert(buffer.get_end_iter(),
                          "Remove %s before proceeding.\n\n"
                          % itORthem[suspectcount!=1])

        buffer.insert(buffer.get_end_iter(),
                      "No. of Elements: %d\n" % nElements)
        buffer.insert(buffer.get_end_iter(),
                      "No. of Faces: %d\n" % nFaces)
        buffer.insert(buffer.get_end_iter(),
                      "No. of Segments: %d\n" % nSegments)
        buffer.insert(buffer.get_end_iter(), "No. of Nodes: %d\n" % nNodes)

        #for name in skeletonelement.ElementShapeType.names:
        #    buffer.insert(buffer.get_end_iter(),
        #                  "No. of %ss: %d\n" % (name, shapecounts[name]))

        # buffer.insert(buffer.get_end_iter(),
        #                   "Z Periodicity: %s\n" % x_periodicity)
        # buffer.insert(buffer.get_end_iter(),
        #                   "Y Periodicity: %s\n" % y_periodicity)
        # if config.dimension() == 3:
        #     buffer.insert(buffer.get_end_iter(),
        #                   "Z Periodicity: %s\n" % z_periodicity)
            

        if homogIndex is not None:
           buffer.insert(buffer.get_end_iter(),
                         "Homogeneity Index: %s\n" % homogIndex)
        else:
           buffer.insert(buffer.get_end_iter(),
                         "Homogeneity Index: ????\n")
        gtklogger.checkpoint("skeleton page info updated")

    def new_skeleton_CB(self, gtkobj): # gtk callback for "New..." button
        paramset = filter(lambda x: x.name!='microstructure',
                          skeletonmenu.New.params)
        if parameterwidgets.getParameters(title='New skeleton', *paramset):
            skeletonmenu.New.callWithDefaults(
                microstructure=self.currentMSName())

    def simple_skeleton_CB(self, gtkobj): # gtk callback for "Simple..." button
        paramset = filter(lambda x: x.name!='microstructure',
                          skeletonmenu.Simple.params)
        if parameterwidgets.getParameters(title='Simple skeleton', *paramset):
            skeletonmenu.Simple.callWithDefaults(
                microstructure=self.currentMSName())
    def autoCB(self, gtkobj):           # gtk callback for "Auto..." button
        paramset = filter(lambda x: x.name!='microstructure',
                          skeletonmenu.Auto.params)
        if parameterwidgets.getParameters(title='Automatic skeleton',
                                          *paramset):
            skeletonmenu.Auto.callWithDefaults(
                microstructure=self.currentMSName())

    def copy_skeleton_CB(self, gtkobj): # gtk callback for "Copy..." button
        menuitem = skeletonmenu.Copy
        namearg = menuitem.get_arg('name')
        if parameterwidgets.getParameters(namearg, title='Copy skeleton'):
            menuitem.callWithDefaults(skeleton=self.skelwidget.get_value())

    def rename_skeleton_CB(self, gtkobj): # gtk callback for "Rename..." button
        menuitem = skeletonmenu.Rename
        namearg = menuitem.get_arg('name')
        namearg.value = labeltree.makePath(self.skelwidget.get_value())[-1]
        if parameterwidgets.getParameters(namearg, title='Rename skeleton'):
            menuitem.callWithDefaults(skeleton=self.skelwidget.get_value())

    def delete_skeletonCB(self, gtkobj): # gtk callback for Delete button.
        skelname = self.currentSkeletonName()
        if reporter.query("Delete skeleton %s?" % skelname,
                          "OK", "Cancel", default="OK")=="OK":
            menuitem = skeletonmenu.Delete
            menuitem.callWithDefaults(skeleton=self.skelwidget.get_value())

    def getSkeletonAvailability(self):
        try:
            currentSkel = self.skelwidget.get_value() # colon separated string
            ctxt = skeletoncontext.skeletonContexts[currentSkel]
            return not ctxt.query_reservation()
        except KeyError:
            return 1
        
    def sensitize(self):
        debug.subthreadTest()
        context = self.currentSkeletonContext()
        if context is not None:
            skelselected = True
            context.begin_reading()
            try:
                undoable = context.undoable()
                redoable = context.redoable()
                not_illegal = self.legalityCheck()
            finally:
                context.end_reading()
        else:
            skelselected = False
            undoable = redoable = False
            not_illegal = False
        mainthread.runBlock(self.sensitize_thread,
                            (skelselected, undoable, redoable, not_illegal))

    def sensitize_thread(self, skelselected, undoable, redoable, not_illegal):
        debug.mainthreadTest()
        self.okbutton.set_sensitive(skelselected and self.skelmod.isValid()
                                    and not_illegal)
        self.undobutton.set_sensitive(undoable)
        self.redobutton.set_sensitive(redoable)
        
        msclass = whoville.getClass('Microstructure')
        havems = msclass is not None and msclass.nActual() > 0
        self.newbutton.set_sensitive(havems)
        self.simplebutton.set_sensitive(havems)
        ## TODO 3.1: uncomment this when AutoSkeleton is restored.
        # self.autobutton.set_sensitive(havems)
        self.deletebutton.set_sensitive(skelselected)
        self.renamebutton.set_sensitive(skelselected)
        self.copybutton.set_sensitive(skelselected)
        self.savebutton.set_sensitive(skelselected)

        if not self.getSkeletonAvailability():
            self.okbutton.set_sensitive(0)
            self.undobutton.set_sensitive(0)
            self.redobutton.set_sensitive(0)
        self.sensitizeHistory_thread()
        gtklogger.checkpoint("skeleton page sensitized")
        
    def sensitizeHistory(self):
        mainthread.runBlock(self.sensitizeHistory_thread)
    def sensitizeHistory_thread(self):
        debug.mainthreadTest()
        self.nextskelmodbutton.set_sensitive(self.historian.nextSensitive())
        self.prevskelmodbutton.set_sensitive(self.historian.prevSensitive())

    def validityChangeCB(self, validity):
        self.sensitize()

    def updateskelmod(self):    # a new modifier was added
        self.skelmod.update(SkeletonModifier.registry)

    def currentFullSkeletonName(self):
        return self.skelwidget.get_value()
    
    def update_ok_button(self, who):
        if  self.currentSkeletonContext() is who:
            self.sensitize()
            
    def okskelmod(self,gtkobj):
        path = self.skelwidget.get_value()
        modifier = self.skelmod.get_value()
        if path and modifier:
            OOF.Skeleton.Modify(skeleton=path, modifier=modifier)
        else:
            reporter.report("Can't modify!!!!")

    def prevskelmod(self,gtkobj):
        self.historian.prevCB()

    def nextskelmod(self,gtkobj):
        self.historian.nextCB()

    def undoskelmod(self,gtkobj):
        path = self.skelwidget.get_value()
        OOF.Skeleton.Undo(skeleton = path)

    def redoskelmod(self,gtkobj):
        path = self.skelwidget.get_value()
        OOF.Skeleton.Redo(skeleton = path)

    def save_skeletonCB(self, button):
        menuitem = mainmenu.OOF.File.Save.Skeleton
        skelname = self.skelwidget.get_value()
        params = filter(lambda x: x.name!="skeleton", menuitem.params)
        if parameterwidgets.getParameters(title='Save Skeleton "%s"' % skelname,
                                          *params):
            menuitem.callWithDefaults(skeleton=skelname)

# Create the page.
skeletonpage = SkeletonPage()

