# -*- python -*-
# $RCSfile: boundarycondPage.py,v $
# $Revision: 1.103.2.8 $
# $Author: langer $
# $Date: 2014/11/05 16:54:47 $

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
from ooflib.common import microstructure
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import oofGUI
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import tooltips
from ooflib.common.IO.GUI import whowidget
from ooflib.common.IO import reporter
from ooflib.engine import skeletoncontext
from ooflib.engine import subproblemcontext
from ooflib.engine.IO import boundaryconditionmenu
import ooflib.engine.mesh

import gobject
import gtk

# TODO 3.1: MAYBE Construct names automatically:
#           bdyname:fieldname:component, or bdyname:fluxname:component

class BoundaryCondPage(oofGUI.MainPage):
    def __init__(self):
        oofGUI.MainPage.__init__(
            self, name="Boundary Conditions",
            ordering=230,
            tip=
            "Set field and flux boundary conditions on the mesh's boundaries.")
        mainbox = gtk.VBox(spacing=2)
        self.gtk.add(mainbox)

        align = gtk.Alignment(xalign=0.5)
        mainbox.pack_start(align, expand=0, fill=0)
        centerbox = gtk.HBox(spacing=3)
        align.add(centerbox)
        self.meshwidget = whowidget.WhoWidget(ooflib.engine.mesh.meshes,
                                              callback=self.meshCB, scope=self)
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
        switchboard.requestCallbackMain(self.meshwidget, self.meshwidgetCB)

        bcbuildframe = gtk.Frame()
        gtklogger.setWidgetName(bcbuildframe, 'Condition')
        bcbuildframe.set_shadow_type(gtk.SHADOW_IN)
        mainbox.pack_start(bcbuildframe, expand=1, fill=1)
        bcbuildbox = gtk.VBox(spacing=2)
        bcbuildframe.add(bcbuildbox)


        # Buttons for creating, editing and removing boundary conditions

        align = gtk.Alignment(xalign=0.5)
        bcbuildbox.pack_start(align, expand=0, fill=0, padding=3)
        bcbuttons = gtk.HBox(homogeneous=1, spacing=3)
        align.add(bcbuttons)
        
        self.bcNew = gtk.Button("New...")
        gtklogger.setWidgetName(self.bcNew, 'New')
        gtklogger.connect(self.bcNew, "clicked", self.bcNew_CB)
        tooltips.set_tooltip_text(self.bcNew,"Create a new boundary condition in the current mesh.")
        bcbuttons.pack_start(self.bcNew, expand=1, fill=1)

        self.bcRename = gtk.Button("Rename...")
        gtklogger.setWidgetName(self.bcRename, 'Rename')
        gtklogger.connect(self.bcRename, 'clicked', self.bcRename_CB)
        tooltips.set_tooltip_text(self.bcRename,
                             "Rename the selected boundary condition.")
        bcbuttons.pack_start(self.bcRename, expand=1, fill=1)

        self.bcEdit = gtk.Button("Edit...")
        gtklogger.setWidgetName(self.bcEdit, 'Edit')
        gtklogger.connect(self.bcEdit, 'clicked', self.bcEdit_CB)
        tooltips.set_tooltip_text(self.bcEdit,
                             "Edit the selected boundary condition.")
        bcbuttons.pack_start(self.bcEdit, expand=1, fill=1)

        self.bcCopy = gtk.Button("Copy...")
        gtklogger.setWidgetName(self.bcCopy, 'Copy')
        gtklogger.connect(self.bcCopy, 'clicked', self.bcCopy_CB)
        tooltips.set_tooltip_text(self.bcCopy,
                       "Copy the selected boundary condition to another mesh.")
        bcbuttons.pack_start(self.bcCopy, expand=1, fill=1)

        self.bcCopyAll = gtk.Button("Copy All...")
        gtklogger.setWidgetName(self.bcCopyAll, 'CopyAll')
        gtklogger.connect(self.bcCopyAll, 'clicked', self.bcCopyAll_CB)
        tooltips.set_tooltip_text(self.bcCopyAll,
                            "Copy all the boundary conditions to another mesh.")
        bcbuttons.pack_start(self.bcCopyAll, expand=1, fill=1)
        
        self.bcDel = gtk.Button("Delete")
        gtklogger.setWidgetName(self.bcDel, 'Delete')
        gtklogger.connect(self.bcDel, "clicked", self.bcDel_CB)
        tooltips.set_tooltip_text(self.bcDel,
                             "Remove the selected boundary condition.")
        bcbuttons.pack_start(self.bcDel, expand=1, fill=1)
        
        # List of boundary conditions
        bcscroll = gtk.ScrolledWindow()
        gtklogger.logScrollBars(bcscroll, "BCScroll")
        bcbuildbox.pack_start(bcscroll, expand=1, fill=1)
        bcscroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.bclist = BCList(self) 
        bcscroll.add(self.bclist.gtk)

        self.bclist.update(None)

        switchboard.requestCallbackMain(("new who", "Microstructure"),
                                        self.newMSorSkeleton)
        switchboard.requestCallbackMain(("new who", "Skeleton"),
                                        self.newMSorSkeleton)

        # Callbacks for when the mesh changes state internally.
        switchboard.requestCallbackMain("boundary conditions changed",
                                        self.newBCs)
        switchboard.requestCallbackMain("boundary conditions toggled",
                                        self.toggleBCs)
        switchboard.requestCallbackMain("field defined",
                                        self.fieldDefined)
        switchboard.requestCallbackMain("equation activated",
                                        self.eqnActivated)
        switchboard.requestCallbackMain("made reservation",
                                        self.reservationChanged)
        switchboard.requestCallbackMain("cancelled reservation",
                                        self.reservationChanged)
        switchboard.requestCallbackMain("mesh boundaries changed",
                                        self.newMeshBoundaries)
        switchboard.requestCallbackMain("mesh status changed",
                                        self.statusChanged)
        
    def installed(self):
        self.update()

    #######################

    def currentMSName(self):
        path = labeltree.makePath(self.meshwidget.get_value(depth=1))
        if path:
            return path[0]
    def currentMS(self):
        msname = self.currentMSName()
        if msname:
            return microstructure.microStructures[msname].getObject()

    def currentSkeletonName(self):
        path = labeltree.makePath(self.meshwidget.get_value(depth=2))
        if path:
            return path[1]
    def currentSkeleton(self):
        ms = self.currentMS()
        meshname = self.currentSkeletonName()
        if meshname:
            return skeletoncontext.getSkeleton(ms, meshname)

    def currentFullMeshName(self):
        return self.meshwidget.get_value()
    def currentMeshName(self):
        path = labeltree.makePath(self.currentFullMeshName())
        if path:
            return path[2]
    def currentMesh(self):
        try:
            return ooflib.engine.mesh.meshes[self.currentFullMeshName()]
        except KeyError:
            return None
            
    def sensitize(self):
        debug.mainthreadTest()
        msok = self.currentMS() is not None
        skelok = msok and self.currentSkeleton() is not None
        meshok = (skelok and self.currentMesh() is not None
                  and not self.currentMesh().query_reservation())
        meshsync = meshok and not self.currentMesh().outOfSync()

        if meshok:
            mesh = self.currentMesh()
            neqns = len(mesh.all_subproblem_equations())
            nflds = len(mesh.all_subproblem_fields())

        bclist = self.bclist.getBCName() is not None

        self.bcNew.set_sensitive(meshsync and (neqns > 0 and nflds > 0))
        self.bcDel.set_sensitive(bclist and meshok)
        self.bcEdit.set_sensitive(bclist and meshsync)
        self.bcCopy.set_sensitive(bclist)
#         self.bcEnableDisable.set_sensitive(bclist)
        self.bcCopyAll.set_sensitive(bclist)
        self.bcRename.set_sensitive(bclist and meshok)
        
        self.bcCopyAll.set_sensitive(len(self.bclist)>0)
        
    def update(self):
        self.set_state(self.currentFullMeshName())
        
    def set_state(self, meshpath):
        path = labeltree.makePath(meshpath)
        self.meshwidget.set_value(path)
        self.bclist.update(self.currentMesh())
        
    def newMSorSkeleton(self, name):
        # switchboard ("new who", "Skeleton") or ("new who", "Microstructure")
        if not self.currentMesh():
            self.meshwidget.set_value(name)

    def meshCB(self, meshpath):         # WhoWidget callback
        self.set_state(meshpath)
        self.sensitize()

    def meshwidgetCB(self, interactive): # switchboard callback
        self.update()
        self.sensitize()

    def newMeshBoundaries(self, mesh): # switchboard "mesh boundaries changed"
        if mesh==self.currentMesh():
            self.update()
            self.sensitize()

    def statusChanged(self, mesh): # switchboard "mesh status changed"
        if mesh is self.currentMesh():
            self.sensitize()
            
    def reservationChanged(self, whoobj):
        # switchboard "made reservation", "cancelled reservation"
        if  self.currentFullMeshName() == whoobj.path():
            self.sensitize()

    def fieldDefined(self, subproblemname, fieldname, active):
        subpcontext = subproblemcontext.subproblems[subproblemname]
        meshname = subpcontext.getParent().path()
        if meshname == self.currentFullMeshName():
            self.update()
            self.sensitize()

    def eqnActivated(self, subproblemname, eqnname, active):
        subpcontext = subproblemcontext.subproblems[subproblemname]
        meshname = subpcontext.getParent().path()
        if meshname == self.currentFullMeshName():
            self.update()
            self.sensitize()

    ###############################

    def bcNew_CB(self, gtkobj):         # "New..." button callback
        menuitem = boundaryconditionmenu.bcmenu.New
        params = [p for p in menuitem.params if p.name != "mesh"]
        defaults={'mesh': self.currentFullMeshName()}
        parameterwidgets.persistentMenuitemDialog(
            menuitem, defaults, scope=self, title="New Boundary Condition",
            *params)

    def bcDel_CB(self, gtkobj):
        meshname = self.currentFullMeshName()
        bcname = self.bclist.getBCName()
        if meshname and bcname and reporter.query("Really delete?",
                          "No", default="Yes") == "Yes":
	  boundaryconditionmenu.bcmenu.Delete(mesh=meshname, name=bcname)

    # This one can also copy a BC to another mesh.
    def bcCopy_CB(self, gtkobj):
        currentmesh = self.currentFullMeshName()
        bcname = self.bclist.getBCName()
        if currentmesh and bcname:
            menuitem = boundaryconditionmenu.bcmenu.Copy
            newnameparam = menuitem.get_arg("name")
            mesh_ctxt = ooflib.engine.mesh.meshes[currentmesh]
            condition_obj = mesh_ctxt.getBdyCondition(bcname)
            # We want to list only the boundaries of the type
            # appropriate for the boundary condition type.  We
            # retrieve the subclass of boundary parameter associated
            # with the boundary condition, pass that to the widget,
            # extract the parameter value and then explicity pass that
            # value to callWithDefaults since the boundary parameter
            # type might not match.
            boundaryparam = condition_obj.getRegistration().getParameter(
                "boundary").clone()
            bc = ooflib.engine.mesh.meshes[currentmesh].getBdyCondition(bcname)
            boundaryparam.set(bc.boundary)
            meshnameparam = menuitem.get_arg("mesh")
            if parameterwidgets.getParameters(
                newnameparam, meshnameparam, boundaryparam,
                title="Choose a name and boundary.", scope=self):
                menuitem.callWithDefaults(current=currentmesh, bc=bcname, boundary=boundaryparam.value)

    # Convenience function to copy all the BCs to another mesh.  
    def bcCopyAll_CB(self, gtkobj):
        currentmesh = self.currentFullMeshName()
        if currentmesh:
            menuitem = boundaryconditionmenu.bcmenu.Copy_All
            meshnameparam = menuitem.get_arg("mesh")
            if parameterwidgets.getParameters(
                meshnameparam,
                title="Choose the target mesh.", scope=self):
                menuitem.callWithDefaults(current=currentmesh)
    
    def bcEdit_CB(self, *args):
        meshname = self.currentFullMeshName()
        bcname = self.bclist.getBCName()
        if meshname and bcname:
            menuitem = boundaryconditionmenu.bcmenu.Edit
            mesh_ctxt = ooflib.engine.mesh.meshes[meshname]

            condition_obj = mesh_ctxt.getBdyCondition(bcname)
            condition_param = menuitem.get_arg('condition')
            # Set the parameter so the dialog box starts with the right object.
            condition_param.set(condition_obj)

            if parameterwidgets.getParameters(
                condition_param, title="Edit Boundary Condition",
                scope=self):
                menuitem.callWithDefaults(name=bcname, mesh=meshname)
                
    def bcRename_CB(self, gtkobj):
        meshname = self.currentFullMeshName()
        bcname = self.bclist.getBCName()
        if meshname and bcname:
            menuitem = boundaryconditionmenu.bcmenu.Rename
            newnameparam = menuitem.get_arg('name')
            newnameparam.value = bcname
            if parameterwidgets.getParameters(newnameparam,
                                              title="Rename the boundary condition '%s'" % bcname):
                menuitem.callWithDefaults(mesh=meshname, bc=bcname)

    def newBCs(self, mesh, bc, visible): # sb "boundary conditions changed"
        if mesh==self.currentMesh() and visible:
            self.bclist.update(mesh, select=bc)

    def toggleBCs(self,  mesh, bc, visible): # sb "boundary conditions
        # toggled" This has a separate callback from "boundary
        # conditions changed" so that when the bc list is sorted by
        # 'enable' status, it somehow won't be resorted when an enable
        # button is toggled.  Resorting when the button is pressed
        # makes the clicked button move out from under the mouse,
        # which is unnerving.  However, it's not clear how to do it
        # right, so for now this doesn't do anything special.
        if mesh == self.currentMesh() and visible:
            self.bclist.update(mesh, select=bc)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Stateful widget for listing the currently-available boundary
# conditions.  This could be merged into BoundaryCondPage.  It's
# separate for historical reasons.

class BCList:
    sortByNameID = 1
    sortByBdyID = 2
#     sortByEnableID = 3

    def __init__(self, parent, mesh=None):
        debug.mainthreadTest()
        self.parent = parent # Reference to the enclosing BoundaryCondPage.
        self.current_mesh = mesh
        debug.mainthreadTest()
        self.bcliststore = gtk.ListStore(gobject.TYPE_STRING,
                                         gobject.TYPE_PYOBJECT)
        self.sortedlist = gtk.TreeModelSort(self.bcliststore)
        self.gtk = gtk.TreeView(self.sortedlist)
        gtklogger.setWidgetName(self.gtk, "BCList")

        # Enable/disable column
        enablecell = gtk.CellRendererToggle()
        enablecol = gtk.TreeViewColumn("Enable")
        enablecol.pack_start(enablecell, expand=False)
        enablecol.set_cell_data_func(enablecell, self.renderEnableCell)
        self.gtk.append_column(enablecol)
        gtklogger.adoptGObject(enablecell, self.gtk,
                               access_function=gtklogger.findCellRenderer,
                               access_kwargs={'col':0, 'rend':0})
        gtklogger.connect(enablecell, 'toggled', self.enableCellCB)
        ## Click on the column header to sort by Enabled status.
        ## Currently commented out because clicking on a toggle cell
        ## when sorting by Enable may trigger an instant re-sort,
        ## which moves the clicked cell.
#         gtklogger.adoptGObject(enablecol, self.gtk,
#                                access_method=gtk.TreeView.get_column,
#                                access_args=(0,))
#         gtklogger.connect_passive(enablecol, 'clicked')
#         enablecol.set_sort_column_id(self.sortByEnableID)
#         self.sortedlist.set_sort_func(self.sortByEnableID, self.sortByEnableFn)

        # Boundary condition name column
        bcnamecell = gtk.CellRendererText()
        bcnamecol = gtk.TreeViewColumn('Name')
        bcnamecol.pack_start(bcnamecell, expand=False)
        bcnamecol.set_attributes(bcnamecell, text=0)
        self.gtk.append_column(bcnamecol)
        gtklogger.adoptGObject(bcnamecol, self.gtk,
                               access_method=gtk.TreeView.get_column,
                               access_args=(1,))
        gtklogger.connect_passive(bcnamecol, 'clicked')
        bcnamecol.set_sort_column_id(self.sortByNameID)
        self.sortedlist.set_sort_func(self.sortByNameID, self.sortByNameFn)
        
        # Boundary name column
        bdycell = gtk.CellRendererText()
        bdycol = gtk.TreeViewColumn('Boundary')
        bdycol.pack_start(bdycell, expand=True)
        bdycol.set_cell_data_func(bdycell, self.renderBdy)
        self.gtk.append_column(bdycol)
        gtklogger.adoptGObject(bdycol, self.gtk,
                               access_method=gtk.TreeView.get_column,
                               access_args=(2,))
        gtklogger.connect_passive(bdycol, 'clicked')
        bdycol.set_sort_column_id(self.sortByBdyID)
        self.sortedlist.set_sort_func(self.sortByBdyID, self.sortByBdyFn)

        # Boundary condition column
        bccell = gtk.CellRendererText()
        bccol = gtk.TreeViewColumn('Condition')
        bccol.pack_start(bccell, expand=True)
        bccol.set_cell_data_func(bccell, self.renderBC)
        self.gtk.append_column(bccol)

        selection = self.gtk.get_selection()
        gtklogger.adoptGObject(selection, self.gtk,
                               access_method=self.gtk.get_selection)

        self.signals = (
            gtklogger.connect(selection, 'changed', self.selectCB),
            gtklogger.connect(self.gtk, 'row-activated', self.doubleClickCB)
            )

        # Set initial sorting method
        self.lastsortcol = bcnamecol
        self.sortedlist.set_sort_column_id(self.sortByNameID, 
                                           gtk.SORT_ASCENDING)

    def renderEnableCell(self, column, cell_renderer, model, iter):
        debug.mainthreadTest()
        bc = model[iter][1]
        cell_renderer.set_active(not bc.explicit_disable)

    def enableCellCB(self, cell_renderer, path):
        bc = self.sortedlist[path][1]
        meshname = self.parent.currentFullMeshName()
        if bc.is_explicitly_disabled():
            boundaryconditionmenu.bcmenu.Enable(mesh=meshname, name=bc.name())
        else:
            boundaryconditionmenu.bcmenu.Disable(mesh=meshname, name=bc.name())

    def renderBdy(self, column, cell_renderer, model, iter):
        debug.mainthreadTest()
        bc = model[iter][1]
        try:
            bdyname = bc.bdy_string()
        except:
            bdyname = '???'
        cell_renderer.set_property('text', bdyname)

    def renderBC(self, column, cell_renderer, model, iter):
        debug.mainthreadTest()
        bc = model[iter][1]
        cell_renderer.set_property('text', bc.display_string())

    def getBC(self):
        debug.mainthreadTest()
        selection = self.gtk.get_selection()
        model, iter = selection.get_selected()
        if iter:
            return model[iter][1]
    def getBCName(self):
        debug.mainthreadTest()
        selection = self.gtk.get_selection()
        model, iter = selection.get_selected()
        if iter:
            return model[iter][0]
                                   
    def __len__(self):
        return len(self.bcliststore)
    
    # Simplest to just rebuild the whole list.
    def update(self, mesh, select=None):
        debug.mainthreadTest()
        self.current_mesh = mesh
        currentBC = select or self.getBCName()
        for signal in self.signals:
            signal.block()
        try:
            self.bcliststore.clear()
            if mesh:
                items = mesh.allBoundaryConds()[:]
                for (name, bc) in items:
                    if bc.isVisible():
                        self.bcliststore.append([name, bc])
                if currentBC is not None:
                    for row in range(len(self.sortedlist)):
                        if self.sortedlist[row][0] == currentBC:
                            self.gtk.get_selection().select_path(row)
                            break
        finally:
            for signal in self.signals:
                signal.unblock()
        self.parent.sensitize()

    def selectCB(self, selection):
        self.parent.sensitize()
    def doubleClickCB(self, treeview, path, col):
        self.parent.bcEdit_CB()

    def sortByNameFn(self, model, iter1, iter2):
        return cmp(model[iter1][0], model[iter2][0])

#     def sortByEnableFn(self, model, iter1, iter2):
#         bc1 = model[iter1][1]
#         bc2 = model[iter2][1]
#         # I don't understand how bc1 or bc2 can be None, but they
#         # sometimes are, so we need to check for.  What we do when one
#         # of them is None doesn't seem to matter.
#         if bc1 is not None and bc2 is not None:
#             return cmp(bc1.is_explicitly_disabled(),
#                        bc2.is_explicitly_disabled())
#         if bc1 == bc2:          # both None
#             return 0
#         if bc1 is None:
#             return -1
#         return 1

    def sortByBdyFn(self, model, iter1, iter2):
        bc1 = model[iter1][1]
        bc2 = model[iter2][1]
        # I don't understand how bc1 or bc2 can be None, but they
        # sometimes are, so we need to check for.  What we do when one
        # of them is None doesn't seem to matter.
        if bc1 is not None and bc2 is not None:
            return cmp(bc1.bdy_string(), bc2.bdy_string())
        if bc1 == bc2:          # both None
            return 0
        if bc1 is None:
            return -1
        return 1

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

bcp = BoundaryCondPage()
