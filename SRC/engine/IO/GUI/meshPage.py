# -*- python -*-
# $RCSfile: meshPage.py,v $
# $Revision: 1.105.2.14 $
# $Author: langer $
# $Date: 2014/11/05 16:54:53 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import switchboard
from ooflib.SWIG.engine import elementshape
from ooflib.SWIG.engine import meshdatacache
from ooflib.common import debug
from ooflib.common import labeltree
from ooflib.common import microstructure
from ooflib.common.IO import mainmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import whoville
from ooflib.common.IO import reporter
from ooflib.common.IO.GUI import chooser
from ooflib.common.IO.GUI import fixedwidthtext
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import gtkutils
from ooflib.common.IO.GUI import historian
from ooflib.common.IO.GUI import oofGUI
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import regclassfactory
from ooflib.common.IO.GUI import tooltips
from ooflib.common.IO.GUI import whowidget
from ooflib.engine import meshmod
from ooflib.engine import meshstatus
from ooflib.engine import skeletoncontext
import ooflib.engine.mesh

import gobject
import gtk
import string

meshmenu = mainmenu.OOF.Mesh

class MeshPage(oofGUI.MainPage):
    def __init__(self):
        self.built = False
        oofGUI.MainPage.__init__(
            self, name="FE Mesh", ordering=200,
            tip="Create a Finite Element Mesh from a Skeleton.")
        mainbox = gtk.VBox(spacing=2)
        self.gtk.add(mainbox)

        align = gtk.Alignment(xalign=0.5)
        mainbox.pack_start(align, expand=0, fill=0)
        centerbox = gtk.HBox(spacing=3)
        align.add(centerbox)
        self.meshwidget = whowidget.WhoWidget(ooflib.engine.mesh.meshes,
                                              scope=self)
        label = gtk.Label("Microstructure=")
        label.set_alignment(1.0, 0.5)
        centerbox.pack_start(label, expand=0, fill=0)
        centerbox.pack_start(self.meshwidget.gtk[0], expand=0, fill=0)

        label = gtk.Label("Skeleton=")
        label.set_alignment(1.0, 0.5)
        centerbox.pack_start(label, expand=0, fill=0)
        centerbox.pack_start(self.meshwidget.gtk[1], expand=0, fill=0)

        label = gtk.Label("Mesh=")
        label.set_alignment(1.0, 0.5)
        centerbox.pack_start(label, expand=0, fill=0)
        centerbox.pack_start(self.meshwidget.gtk[2], expand=0, fill=0)

        # Centered box of buttons
        align = gtk.Alignment(xalign=0.5)
        mainbox.pack_start(align, expand=0, fill=0)
        bbox = gtk.HBox(homogeneous=1, spacing=3)
        align.add(bbox)
        self.newbutton = gtkutils.StockButton(gtk.STOCK_NEW, "New...")
        gtklogger.setWidgetName(self.newbutton, 'New')
        gtklogger.connect(self.newbutton, 'clicked', self.newCB)
        tooltips.set_tooltip_text(
            self.newbutton, "Create a new mesh from the current skeleton.")
        bbox.pack_start(self.newbutton, expand=0, fill=1)
        
        self.renamebutton = gtkutils.StockButton(gtk.STOCK_EDIT, "Rename...")
        gtklogger.setWidgetName(self.renamebutton, 'Rename')
        gtklogger.connect(self.renamebutton, 'clicked', self.renameCB)
        tooltips.set_tooltip_text(self.renamebutton,"Rename the current mesh.")
        bbox.pack_start(self.renamebutton, expand=0, fill=1)
        
        self.copybutton = gtkutils.StockButton(gtk.STOCK_COPY, "Copy...")
        gtklogger.setWidgetName(self.copybutton, 'Copy')
        gtklogger.connect(self.copybutton, 'clicked', self.copyCB)
        tooltips.set_tooltip_text(self.copybutton,"Copy the current mesh.")
        bbox.pack_start(self.copybutton, expand=0, fill=1)
        
        self.deletebutton = gtkutils.StockButton(gtk.STOCK_DELETE, "Delete")
        gtklogger.setWidgetName(self.deletebutton, 'Delete')
        gtklogger.connect(self.deletebutton, 'clicked', self.deleteCB)
        tooltips.set_tooltip_text(self.deletebutton,"Delete the current mesh.")
        bbox.pack_start(self.deletebutton, expand=0, fill=1)
        
        self.savebutton = gtkutils.StockButton(gtk.STOCK_SAVE, "Save...")
        gtklogger.setWidgetName(self.savebutton, 'Save')
        gtklogger.connect(self.savebutton, 'clicked', self.saveCB)
        tooltips.set_tooltip_text(self.savebutton,
                             "Save the current mesh to a file.")
        bbox.pack_start(self.savebutton, expand=0, fill=1)

        mainpane = gtk.HPaned()
        gtklogger.setWidgetName(mainpane, 'Pane')
        mainbox.pack_start(mainpane, expand=1, fill=1)
        gtklogger.connect_passive(mainpane, 'notify::position')
        leftbox = gtk.VPaned()
        mainpane.pack1(leftbox, resize=1, shrink=0)
        
        infoframe = gtk.Frame('Mesh Information')
        infoframe.set_shadow_type(gtk.SHADOW_IN)
        leftbox.pack1(infoframe, resize=1, shrink=1)
        scroll = gtk.ScrolledWindow()
        gtklogger.logScrollBars(scroll, "MeshInfo")
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scroll.set_shadow_type(gtk.SHADOW_IN)
        infoframe.add(scroll)
        self.infoarea = fixedwidthtext.FixedWidthTextView()
        gtklogger.setWidgetName(self.infoarea, 'info')
        self.infoarea.set_cursor_visible(False)
        self.infoarea.set_editable(False)
        scroll.add(self.infoarea)

###
        ## Subproblem creation, deletion, etc.
        #subprobframe = gtk.Frame('Subproblems')
        #gtklogger.setWidgetName(subprobframe, 'Subproblems')
        #subprobframe.set_shadow_type(gtk.SHADOW_IN)
        #leftbox.pack2(subprobframe, resize=1, shrink=1)
        #subpbox = gtk.VBox()
        #subprobframe.add(subpbox)
        #self.subpchooser = chooser.ScrolledChooserListWidget(
            #callback=self.subpchooserCB,
            #dbcallback=self.subprobEditCB,
            #name="subprobChooser")
        #subpbox.pack_start(self.subpchooser.gtk, expand=1, fill=1)

        #subpbuttons1 = gtk.HBox(homogeneous=True, spacing=2)
        #subpbuttons2 = gtk.HBox(homogeneous=True, spacing=2)
        #subpbox.pack_start(subpbuttons1, expand=0, fill=0)
        #subpbox.pack_start(subpbuttons2, expand=0, fill=0)
        
        # Subproblem creation, deletion, etc.
	subprobframe = gtk.Frame('Subproblems')
	gtklogger.setWidgetName(subprobframe, 'Subproblems')
	subprobframe.set_shadow_type(gtk.SHADOW_IN)
	leftbox.pack2(subprobframe, resize=1, shrink=1)
	subpbox = gtk.VBox()
	subprobframe.add(subpbox)
	innerframe = gtk.Frame()
	innerframe.set_shadow_type(gtk.SHADOW_IN)
	subpbox.pack_start(innerframe, expand=1, fill=1)
	self.subpScroll = gtk.ScrolledWindow()
	gtklogger.logScrollBars(self.subpScroll, "SubproblemScroll")
	self.subpScroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
	innerframe.add(self.subpScroll)

	self.subprobList = gtk.ListStore(gobject.TYPE_PYOBJECT)
	self.subpListView = gtk.TreeView(self.subprobList)
	gtklogger.setWidgetName(self.subpListView, "SubproblemList")
	self.subpScroll.add(self.subpListView)
	gtklogger.adoptGObject(self.subprobList, self.subpListView,
				access_method=self.subpListView.get_model)
	# Catch selection changes
	gtklogger.adoptGObject(self.subpListView.get_selection(),
				self.subpListView,
				access_method=self.subpListView.get_selection)
	self.subpselsig = gtklogger.connect(self.subpListView.get_selection(),
					    'changed', self.subpSelectCB)
	# Catch double clicks or returns
	gtklogger.connect(self.subpListView, 'row-activated',
			  self.subprobEditCB)

	# Subproblem name in the column 1
	namecell = gtk.CellRendererText()
	namecol = gtk.TreeViewColumn("Subproblem")
	namecol.set_resizable(True)
	namecol.pack_start(namecell, expand=True)
	namecol.set_cell_data_func(namecell, self.renderSubproblemName)
	self.subpListView.append_column(namecol)

	# Subproblem consistency in the column 2
	consistencycell = gtk.CellRendererText()
	consistencycol = gtk.TreeViewColumn("Consistent?")
	consistencycol.set_resizable(True)
	consistencycol.pack_start(consistencycell, expand=True)
	consistencycol.set_cell_data_func(consistencycell, self.renderSubproblemConsistency)
	self.subpListView.append_column(consistencycol)
	
	# Subproblem type in the column 3
	typecell = gtk.CellRendererText()
	typecol = gtk.TreeViewColumn("Type")
	typecol.set_resizable(True)
	typecol.pack_start(typecell, expand=True)
	typecol.set_cell_data_func(typecell, self.renderSubproblemType)
	self.subpListView.append_column(typecol)

	# Buttons at the bottom of the subproblem pane
	subpbuttons1 = gtk.HBox(homogeneous=True, spacing=2)
	subpbuttons2 = gtk.HBox(homogeneous=True, spacing=2)
	subpbox.pack_start(subpbuttons1, expand=0, fill=0)
	subpbox.pack_start(subpbuttons2, expand=0, fill=0)
###

        self.subprobNew = gtkutils.StockButton(gtk.STOCK_NEW, "New...")
        gtklogger.setWidgetName(self.subprobNew, "New")
        gtklogger.connect(self.subprobNew, "clicked", self.subprobNewCB)
        tooltips.set_tooltip_text(self.subprobNew,"Create a new subproblem.")
        subpbuttons1.pack_start(self.subprobNew, expand=1, fill=1)

        self.subprobRename = gtk.Button("Rename...")
        gtklogger.setWidgetName(self.subprobRename, "Rename")
        gtklogger.connect(self.subprobRename, "clicked", self.subprobRenameCB)
        tooltips.set_tooltip_text(self.subprobRename,
                             "Rename the selected subproblem")
        subpbuttons1.pack_start(self.subprobRename, expand=1, fill=1)

        self.subprobEdit = gtkutils.StockButton(gtk.STOCK_EDIT, "Edit...")
        gtklogger.setWidgetName(self.subprobEdit, "Edit")
        gtklogger.connect(self.subprobEdit, 'clicked', self.subprobEditCB)
        tooltips.set_tooltip_text(self.subprobEdit,
                                  "Edit the selected subproblem.")
        subpbuttons1.pack_start(self.subprobEdit, expand=1, fill=1)

        self.subprobCopy = gtkutils.StockButton(gtk.STOCK_COPY, "Copy...")
        gtklogger.setWidgetName(self.subprobCopy, "Copy")
        gtklogger.connect(self.subprobCopy, "clicked", self.subprobCopyCB)
        tooltips.set_tooltip_text(self.subprobCopy,
                                  "Copy the selected subproblem.")
        subpbuttons2.pack_start(self.subprobCopy, expand=1, fill=1)

##        subpbuttons2.pack_start(gtk.HBox(), expand=1, fill=1) # filler
        self.subprobInfo = gtk.Button("Info")
        gtklogger.setWidgetName(self.subprobInfo, "Info")
        gtklogger.connect(self.subprobInfo, 'clicked', self.subprobInfoCB)
        tooltips.set_tooltip_text(self.subprobInfo,
                             "Print information about the selected subproblem")
        subpbuttons2.pack_start(self.subprobInfo, expand=1, fill=1)
        
        self.subprobDelete = gtkutils.StockButton(gtk.STOCK_DELETE, "Delete")
        gtklogger.setWidgetName(self.subprobDelete, "Delete")
        gtklogger.connect(self.subprobDelete, "clicked", self.subprobDeleteCB)
        tooltips.set_tooltip_text(self.subprobDelete,
                             "Delete the selected subproblem.")
        subpbuttons2.pack_start(self.subprobDelete, expand=1, fill=1)
        
        # Right hand side for element operations
        
        elementopsframe = gtk.Frame(label="Mesh Operations")
        gtklogger.setWidgetName(elementopsframe, 'ElementOps')
        elementopsframe.set_shadow_type(gtk.SHADOW_IN)
        mainpane.pack2(elementopsframe, resize=0, shrink=0)
        elementopsbox = gtk.VBox(spacing=3)
        elementopsframe.add(elementopsbox)
        self.elementops = regclassfactory.RegisteredClassFactory(
            meshmod.MeshModification.registry,
            title="Method:",
            callback=self.elementopsCB,
            expand=0, fill=0, scope=self, name="Method")
        elementopsbox.pack_start(self.elementops.gtk, expand=1, fill=1)

        self.historian = historian.Historian(self.elementops.set,
                                             self.sensitizeHistory,
                                             setCBkwargs={'interactive':1})
        # Prev, OK, Next
        hbox = gtk.HBox()
        elementopsbox.pack_start(hbox, expand=0, fill=0, padding=2)
        self.prevbutton = gtkutils.prevButton()
        gtklogger.connect(self.prevbutton, 'clicked', self.prevCB)
        tooltips.set_tooltip_text(self.prevbutton,
                             "Recall the previous mesh element operation.")
        hbox.pack_start(self.prevbutton, expand=0, fill=0, padding=2)

        self.okbutton = gtk.Button(stock=gtk.STOCK_OK)
        gtklogger.setWidgetName(self.okbutton, 'OK')
        gtklogger.connect(self.okbutton, 'clicked', self.okCB)
        tooltips.set_tooltip_text(self.okbutton,
                          'Perform the mesh operation defined above.')
        hbox.pack_start(self.okbutton, expand=1, fill=1, padding=5)

        self.nextbutton = gtkutils.nextButton()
        gtklogger.connect(self.nextbutton, 'clicked', self.nextCB)
        tooltips.set_tooltip_text(self.nextbutton,
                             'Recall the next mesh element operation.')
        hbox.pack_start(self.nextbutton, expand=0, fill=0, padding=2)

        self.built = True

        # lastStatus is used to prevent update_info() from being
        # called when a nominal status change hasn't really changed
        # anything.
        self.lastStatus = None

        switchboard.requestCallbackMain("Mesh modified",
                                        self.recordModifier)
        switchboard.requestCallbackMain("mesh changed", self.meshchangeCB)
        switchboard.requestCallbackMain(("new who", "Microstructure"),
                                        self.newMSorSkeleton)
        switchboard.requestCallbackMain(("new who", "Skeleton"),
                                        self.newMSorSkeleton)
        switchboard.requestCallbackMain(("new who", "Mesh"),
                                        self.newMesh)
        switchboard.requestCallbackMain(("new who", "SubProblem"),
                                        self.newSubProblem)
        switchboard.requestCallbackMain(("rename who", "SubProblem"),
                                        self.renamedSubProblem)
        switchboard.requestCallbackMain(("remove who", "SubProblem"),
                                         self.removeSubProblem)
        switchboard.requestCallbackMain(self.meshwidget, self.meshwidgetCB)
        switchboard.requestCallbackMain("equation activated",
                                        self.equationCB)
        switchboard.requestCallbackMain("mesh status changed",
                                        self.statusChanged)
#         switchboard.requestCallbackMain("mesh boundaries changed",
#                                         self.newMeshBoundaries)

        switchboard.requestCallbackMain(('validity', self.elementops),
                                        self.validityChangeCB)
        

    def installed(self):
        self.sensitize()
        self.sensitizeHistory()
        self.update()

##     This doesn't seem to be necessary...
#     def newMeshBoundaries(self, mesh):
#         if mesh==self.currentMesh():
#             self.update()
#             self.sensitize()
            
    #######################

    def currentSkeletonFullName(self):
        return self.meshwidget.get_value(depth=2)
    def currentSkeletonContext(self):
        try:
            return skeletoncontext.skeletonContexts[
                self.currentSkeletonFullName()]
        except KeyError:
            return None

    def currentFullMeshName(self):
        return self.meshwidget.get_value()
    def currentMeshName(self):
        path = labeltree.makePath(self.currentFullMeshName())
        if path:
            return path[2]
    def currentMeshContext(self):
        try:
            return ooflib.engine.mesh.meshes[self.currentFullMeshName()]
        except KeyError:
            return None
    def currentMesh(self):
        ctxt = self.currentMeshContext()
        if ctxt:
            return ctxt.getObject()

    def currentSubProblemName(self):
        #return self.subpchooser.get_value()
        ctxt = self.currentSubProblemContext()
        if ctxt:
            return ctxt.name()
    def currentSubProblemConsistency(self):
        ctxt = self.currentSubProblemContext()
        if ctxt:
            return ctxt.consistency()
    def currentSubProblemContext(self):
        debug.mainthreadTest()
        selection = self.subpListView.get_selection()
        model, iter = selection.get_selected()
        if iter:
            return model[iter][0]
      
        #meshctxt = self.currentMeshContext()
        #if meshctxt is not None:
            #try:
                #return meshctxt.get_subproblem(self.currentSubProblemName())
            #except KeyError:
                #return None
    def currentFullSubProblemName(self):
        ctxt = self.currentSubProblemContext()
        if ctxt:
            return ctxt.path()
            
    def renderSubproblemName(self, column, cell_renderer, model, iter):
        debug.mainthreadTest()
        subpctxt = model[iter][0]
        cell_renderer.set_property('text', subpctxt.name())
    
    def renderSubproblemConsistency(self, column, cell_renderer, model, iter):
        debug.mainthreadTest()
        subpctxt = model[iter][0]
        if subpctxt.consistency():
	   consis = "True"
	else:
	   consis = "False"
        cell_renderer.set_property('text', consis)
        
    def renderSubproblemType(self, column, cell_renderer, model, iter):
        debug.mainthreadTest()
        subpctxt = model[iter][0]
        cell_renderer.set_property('text', subpctxt.subptype.__class__.__name__)
            
    def sensitize(self):
        debug.mainthreadTest()
        skelok = self.currentSkeletonContext() is not None
        meshctxt = self.currentMeshContext()
        meshok = meshctxt is not None
        meshsync = meshok and not isinstance(meshctxt.status,
                                             meshstatus.OutOfSync)
        self.newbutton.set_sensitive(skelok)
        self.deletebutton.set_sensitive(meshok)
        self.renamebutton.set_sensitive(meshok)
        self.copybutton.set_sensitive(meshok and meshsync)
        self.savebutton.set_sensitive(meshok and meshsync)
        self.okbutton.set_sensitive(meshok and self.elementops.isValid())
        self.sensitizeSubProblems()
        gtklogger.checkpoint("mesh page sensitized")

    def sensitizeHistory(self):
        debug.mainthreadTest()
        self.nextbutton.set_sensitive(self.historian.nextSensitive())
        self.prevbutton.set_sensitive(self.historian.prevSensitive())
        
    def update(self):
        self.set_state(self.currentFullMeshName())

    def recordModifier(self, path, modifier):  # callback for "Mesh modified"
        if modifier:
            self.historian.record(modifier)
        # might as well do the update for Mesh Information pane.
        self.set_state(path)

    def meshchangeCB(self, meshctxt): # switchboard "mesh changed"
        self.update_info()

    def update_info(self):
        themesh = self.currentMeshContext()
        textlines = []
        if themesh is not None:
            skel = themesh.getSkeleton()
            self.lastStatus = themesh.status.tag
            textlines.append("Status: %s" % self.lastStatus)
            if themesh.outOfSync():
                textlines.append("*** Mesh must be rebuilt! ***")
            textlines.append("No. of Nodes:\t%d" % themesh.nnodes())
            textlines.append("No. of Elements:\t%d" % (themesh.nelements() +
                                                       themesh.nedgements()))
            # Get the number of each type of element in the mesh, in a
            # dictionary keyed by ElementShape names.  Since the order
            # of the items in the dictionary isn't necessarily the
            # order in which we want to display them, keying the
            # dictionary by the ElementShapes themselves wouldn't save
            # much work.
            counts = themesh.getObject().getElementShapeCounts()
            for geom in elementshape.shapeNames():
                textlines.append("%s element:\t%s (%d)"
                                 % (geom, 
                                    themesh.getMasterElementType(geom),
                                    counts[geom]))
            textlines.append("Time:\t%s" % themesh.getCurrentTime())
            textlines.append(
                "Data Cache Type: %s" %
                themesh.getDataCacheType())
            n = themesh.dataCacheSize()
            textlines.append("Data Cache Size: %d time step%s" 
                             % (n, "s"*(n!=1)))
        else:                           # no current mesh
            textlines.append("No mesh!")
        buffer = self.infoarea.get_buffer()
        buffer.set_text('\n'.join(textlines))

    def statusChanged(self, meshctxt): # switchboard "mesh status changed"
        if meshctxt is self.currentMeshContext():
            if meshctxt.status.tag != self.lastStatus:
                self.update_info()
                self.sensitize()
            
    def set_state(self, meshpath):  # widget update & information update
        debug.mainthreadTest()
        path = labeltree.makePath(meshpath)
        self.meshwidget.set_value(path)
        self.update_info()
        self.set_subproblem_state()
        self.sensitize()
        self.sensitizeHistory()

    def newMSorSkeleton(self, path):
        # switchboard ("new who", "Microstructure") or ("new who", "Skeleton")
        if not self.currentMesh():
            self.meshwidget.set_value(path)

    def newMesh(self, meshname):        # switchboard ("new who", "Mesh")
        self.set_state(meshname)
        self.sensitize()
    
    def meshwidgetCB(self, interactive): # switchboard widget callback
        self.update()
        self.sensitize()

    def equationCB(self, *args):  # switchboard "equation activated"
        switchboard.notify(self.meshwidget, interactive=1)

    def newCB(self, *args):             # gtk button callback
        menuitem = mainmenu.OOF.Mesh.New
        params = filter(lambda x: x.name !='skeleton', menuitem.params)
        if parameterwidgets.getParameters(title='Create a new mesh',
                                          scope=self, *params):
            menuitem.callWithDefaults(skeleton=self.currentSkeletonFullName())

    def deleteCB(self, *args):          # gtk button callback
        if reporter.query(
            "Really delete %s?"%self.currentFullMeshName(),
            "No", default="Yes") == "Yes":
            meshmenu.Delete(mesh=self.currentFullMeshName())

    def copyCB(self, *args):            # gtk button callback
        menuitem = mainmenu.OOF.Mesh.Copy
        nameparam = menuitem.get_arg("name")
        fieldparam = menuitem.get_arg("copy_field")
        eqnparam = menuitem.get_arg("copy_equation")
        bcparam = menuitem.get_arg("copy_bc")
        if parameterwidgets.getParameters(nameparam, fieldparam, eqnparam,
                                          bcparam, title='Copy a mesh'):
            menuitem.callWithDefaults(mesh=self.currentFullMeshName())
        
    def renameCB(self, *args):          # gtk button callback
        menuitem = meshmenu.Rename
        namearg = menuitem.get_arg('name')
        curmeshpath = self.currentFullMeshName()
        namearg.value = labeltree.makePath(curmeshpath)[-1]
        if parameterwidgets.getParameters(namearg,
                                          title='Rename mesh '+namearg.value):
            menuitem.callWithDefaults(mesh=curmeshpath)

    def saveCB(self, *args):
        menuitem = mainmenu.OOF.File.Save.Mesh
        meshname = self.meshwidget.get_value()
        params = filter(lambda x: x.name!="mesh", menuitem.params)
        if parameterwidgets.getParameters(ident='SaveMeshFromPage',
                                          title='Save Mesh "%s"' % meshname,
                                          *params):
            menuitem.callWithDefaults(mesh=meshname)

    def prevCB(self, gtkobj):
        self.historian.prevCB()

    def nextCB(self, gtkobj):
        self.historian.nextCB()

    def elementopsCB(self, reg):
        self.historian.stateChangeCB(reg)
        self.sensitize()

    def okCB(self, gtkobj):
        path = self.meshwidget.get_value()
        modifier = self.elementops.get_value()
        if path and modifier:
            mainmenu.OOF.Mesh.Modify(mesh=path, modifier=modifier)

    def validityChangeCB(self, validity):
        self.sensitize()

    ######################

    # subproblem callbacks and sensitization

    def set_subproblem_state(self, subprobname=None):
        debug.mainthreadTest()
        currentSub = self.currentSubProblemContext()
        self.subpselsig.block()
        try:
            self.subprobList.clear()
            meshctxt = self.currentMeshContext()
            if meshctxt is None:
                return
            subprobs = [s for s in meshctxt.subproblems()]
            #subprobs.sort()
            for subprob in subprobs:
                it = self.subprobList.append([subprob])
                if subprob is currentSub:
                    # Reselect previous selection
                    self.subpListView.get_selection().select_iter(it)
        finally:
            self.subpselsig.unblock()
            self.sensitizeSubProblems()
        
        #meshctxt = self.currentMeshContext()
        #if meshctxt is not None:
            #self.subpchooser.update(meshctxt.subproblemNames())
            #if subprobname is not None:
                #self.subpchooser.set_selection(subprobname)
        #else:
            #self.subpchooser.update([])

    def subprobNewCB(self, gtkobj):
        menuitem = mainmenu.OOF.Subproblem.New
        params = filter(lambda x: x.name != 'mesh', menuitem.params)
        if parameterwidgets.getParameters(title='Create a new subproblem',
                                          scope=self, *params):
            menuitem.callWithDefaults(mesh=self.currentFullMeshName())
    def subprobCopyCB(self, gtkobj):
        menuitem = mainmenu.OOF.Subproblem.Copy
        # Initialize the 'mesh' parameter to the current mesh, but
        # allow the user to change it.  Usually the subproblem will be
        # copied to the current mesh, but not always.
        meshparam = menuitem.get_arg('mesh')
        meshparam.value = self.currentFullMeshName()
        params = filter(lambda x: x.name != 'subproblem', menuitem.params)
        if parameterwidgets.getParameters(title='Copy a subproblem',
                                          scope=self, *params):
            menuitem.callWithDefaults(
                subproblem=self.currentFullSubProblemName())
    def subprobRenameCB(self, gtkobj):
        menuitem = mainmenu.OOF.Subproblem.Rename
        namearg = menuitem.get_arg('name')
        cursubprob = self.currentFullSubProblemName()
        namearg.value = labeltree.makePath(cursubprob)[-1]
        if parameterwidgets.getParameters(
            namearg, title="Rename subproblem " + namearg.value):
            menuitem.callWithDefaults(subproblem=cursubprob)

    def subprobInfoCB(self, gtkobj):
        mainmenu.OOF.Subproblem.Info(
            subproblem=self.currentFullSubProblemName())

    def subprobDeleteCB(self, gtkobj):
        if reporter.query(
            "Really delete %s" % self.currentFullSubProblemName(),
            "No", default="Yes") == "Yes":
            mainmenu.OOF.Subproblem.Delete(
                subproblem=self.currentFullSubProblemName())

###
    def subprobEditCB(self, gtkobj, path=None, col=None):
        subproblemname = self.currentFullSubProblemName()
        if subproblemname:
            menuitem = mainmenu.OOF.Subproblem.Edit
            subpctxt = ooflib.engine.subproblemcontext.subproblems[
                subproblemname]
            subpparam = menuitem.get_arg('subproblem')
            subpparam.set(subpctxt.subptype)
            extra_params = []
            extra_params.append(whoville.WhoParameter(subpctxt.name(), subpctxt, subpctxt.path()))
            if parameterwidgets.getParameters(
                subpparam, title="Edit Subproblem definition", scope=self, hidden_params=extra_params):
                menuitem.callWithDefaults(name=subproblemname)
        
    ###
    def subpSelectCB(self, selection):
        if self.built:
            self.sensitizeSubProblems()

    def sensitizeSubProblems(self):
        debug.mainthreadTest()
        subpok = self.currentSubProblemName() is not None
        defaultsubp = (self.currentSubProblemName() ==
                       ooflib.engine.mesh.defaultSubProblemName)
        meshctxt = self.currentMeshContext()
        meshok = meshctxt is not None and not meshctxt.outOfSync()
        self.subprobNew.set_sensitive(meshok)
        self.subprobRename.set_sensitive(subpok and not defaultsubp)
        self.subprobCopy.set_sensitive(subpok and self.currentSubProblemContext().consistency())
        self.subprobDelete.set_sensitive(subpok and not defaultsubp)
        self.subprobEdit.set_sensitive(meshok and subpok and not defaultsubp)
        self.subprobInfo.set_sensitive(subpok)
        gtklogger.checkpoint("mesh page subproblems sensitized")

    def newSubProblem(self, subproblempath): # sb ("new who", "SubProblem")
        path = labeltree.makePath(subproblempath)
        if labeltree.makePath(self.currentFullMeshName()) == path[:-1]:
            self.set_subproblem_state(path[-1])
    def renamedSubProblem(self, oldpath, newname):
        # switchboard ("rename who", "SubProblem")
        path = labeltree.makePath(oldpath)
        if labeltree.makePath(self.currentFullMeshName()) == path[:-1]:
            self.set_subproblem_state(newname)
    def removeSubProblem(self, path):
        if labeltree.makePath(self.currentFullMeshName()) == path[:-1]:
            self.set_subproblem_state()
        

#############
        
mp = MeshPage()
