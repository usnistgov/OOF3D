# -*- python -*-
# $RCSfile: outputPage.py,v $
# $Revision: 1.4.4.7 $
# $Author: langer $
# $Date: 2014/11/05 16:54:54 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import guitop
from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common.IO import parameter
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import gtkutils
from ooflib.common.IO.GUI import oofGUI
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import regclassfactory
from ooflib.common.IO.GUI import tooltips
from ooflib.common.IO.GUI import whowidget
from ooflib.engine.IO import scheduledoutput
from ooflib.engine.IO import scheduledoutputmenu
import ooflib.engine.mesh

import gobject
import gtk

outputmenu = scheduledoutputmenu.outputmenu

## TODO 3.1: Create an output using an OutputStream.  Clear the
## destination list on the Analysis or Bdy Analysis pages.  What
## should happen to the OutputStream on this page?  Probably we should
## raise a warning and offer to delete the scheduled output.

class OutputPage(oofGUI.MainPage):
    def __init__(self):
        oofGUI.MainPage.__init__(
            self, name="Scheduled Output", ordering=235,
            tip="Set output quantities to be computed during time evolution.")
        mainbox = gtk.VBox(spacing=2)
        self.gtk.add(mainbox)

        align = gtk.Alignment(xalign=0.5)
        mainbox.pack_start(align, expand=0, fill=0)
        centerbox = gtk.HBox(spacing=3)
        align.add(centerbox)
        self.meshwidget = whowidget.WhoWidget(ooflib.engine.mesh.meshes,
                                              scope=self)
        switchboard.requestCallbackMain(self.meshwidget, self.meshCB)
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

        align = gtk.Alignment(xalign=0.5)
        mainbox.pack_start(align, expand=0, fill=0, padding=3)
        align.add(gtk.Label(
                "Skip this page if you're only solving static problems."))

        outputFrame = gtk.Frame()
        gtklogger.setWidgetName(outputFrame, 'Output')
        outputFrame.set_shadow_type(gtk.SHADOW_IN)
        mainbox.pack_start(outputFrame, expand=1, fill=1)
        outputBox = gtk.VBox(spacing=2)
        outputFrame.add(outputBox)

        # Buttons for creating, editing, and removing Outputs

        bbox = gtk.HBox(homogeneous=True, spacing=2)
        outputBox.pack_start(bbox, expand=False, fill=False)
        # New Output
        self.newOutputButton = gtkutils.StockButton(gtk.STOCK_NEW, "New")
        gtklogger.setWidgetName(self.newOutputButton, "New")
        gtklogger.connect(self.newOutputButton, 'clicked', self.newOutputCB)
        bbox.pack_start(self.newOutputButton, expand=True, fill=True)
        tooltips.set_tooltip_text(self.newOutputButton,
                                  "Define a new output operation.")
        # Rename Output
        self.renameOutputButton = gtkutils.StockButton(gtk.STOCK_EDIT, "Rename")
        gtklogger.setWidgetName(self.renameOutputButton, "Rename")
        gtklogger.connect(self.renameOutputButton, 'clicked', self.renameCB)
        bbox.pack_start(self.renameOutputButton, expand=True, fill=True)
        tooltips.set_tooltip_text(self.renameOutputButton,
                             "Rename the selected output operation.")
        # Edit Output
        self.editOutputButton = gtkutils.StockButton(gtk.STOCK_EDIT, "Edit")
        gtklogger.setWidgetName(self.editOutputButton, "Edit")
        gtklogger.connect(self.editOutputButton, 'clicked', self.editOutputCB)
        bbox.pack_start(self.editOutputButton, expand=True, fill=True)
        tooltips.set_tooltip_text(self.editOutputButton,
                             "Redefine the selected output operation.")
        # Copy Output
        self.copyOutputButton = gtkutils.StockButton(gtk.STOCK_COPY, "Copy")
        gtklogger.setWidgetName(self.copyOutputButton, "Copy")
        gtklogger.connect(self.copyOutputButton, 'clicked', self.copyOutputCB)
        bbox.pack_start(self.copyOutputButton, expand=True, fill=True)
        tooltips.set_tooltip_text(self.copyOutputButton,
                                  "Copy the selected output.")
        # Second row of buttons
        bbox = gtk.HBox(homogeneous=True, spacing=2)
        outputBox.pack_start(bbox, expand=False, fill=False)
        # Delete Output
        self.deleteOutputButton = gtkutils.StockButton(gtk.STOCK_DELETE, 
                                                       "Delete")
        gtklogger.setWidgetName(self.deleteOutputButton, "Delete")
        gtklogger.connect(self.deleteOutputButton, 'clicked',
                          self.deleteOutputCB)
        tooltips.set_tooltip_text(self.deleteOutputButton,
                             "Delete the selected output operation.")
        bbox.pack_start(self.deleteOutputButton, expand=True, fill=True)
        # Delete all outputs
        self.deleteAllButton = gtkutils.StockButton(gtk.STOCK_DELETE,
                                                    "Delete All")
        gtklogger.setWidgetName(self.deleteAllButton, "DeleteAll")
        gtklogger.connect(self.deleteAllButton, 'clicked', self.deleteAllCB)
        bbox.pack_start(self.deleteAllButton, expand=True, fill=True)
        tooltips.set_tooltip_text(self.deleteAllButton,
                             "Delete all output operations")
        # Rewind
        self.rewindDestButton = gtkutils.StockButton(gtk.STOCK_MEDIA_REWIND,
                                                     "Rewind")
        gtklogger.setWidgetName(self.rewindDestButton, "Rewind")
        gtklogger.connect(self.rewindDestButton, 'clicked',
                          self.rewindDestinationCB)
        bbox.pack_start(self.rewindDestButton, expand=True, fill=True)
        tooltips.set_tooltip_text(self.rewindDestButton,
                             "Go back to the start of the output file.")
        # Rewind All
        self.rewindAllDestsButton = gtkutils.StockButton(gtk.STOCK_MEDIA_REWIND,
                                                         "Rewind All")
        gtklogger.setWidgetName(self.rewindAllDestsButton, "RewindAll")
        gtklogger.connect(self.rewindAllDestsButton, 'clicked',
                          self.rewindAllDestinationsCB)
        bbox.pack_start(self.rewindAllDestsButton, expand=True, fill=True)
        tooltips.set_tooltip_text(self.rewindAllDestsButton,
                             "Go back to the start of all output files.")

        # List of Outputs
        outputScroll = gtk.ScrolledWindow()
        gtklogger.logScrollBars(outputScroll, "OutputScroll")
        outputBox.pack_start(outputScroll, expand=True, fill=True)
        outputScroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)

        self.outputList = gtk.ListStore(gobject.TYPE_PYOBJECT)
        self.outputView = gtk.TreeView(self.outputList)
        outputScroll.add(self.outputView)
        gtklogger.setWidgetName(self.outputView, "OutputList")
        # Catch double clicks
        gtklogger.connect(self.outputView, 'row-activated',
                          self.outputDoubleClickCB)
        # Catch selection changes
        gtklogger.adoptGObject(self.outputView.get_selection(),
                               self.outputView,
                               access_method=self.outputView.get_selection)
        self.selectionSignal = gtklogger.connect(
            self.outputView.get_selection(), 'changed',
            self.selectionCB)

        # Enable/disable column
        enableCell = gtk.CellRendererToggle()
        enableCol = gtk.TreeViewColumn("Enable")
        enableCol.pack_start(enableCell, expand=False)
        enableCol.set_resizable(False)
        enableCol.set_cell_data_func(enableCell, self.renderEnableCell)
        self.outputView.append_column(enableCol)
        gtklogger.adoptGObject(enableCell, self.outputView,
                               access_function=gtklogger.findCellRenderer,
                               access_kwargs={'col':0, 'rend':0})
        gtklogger.connect(enableCell, 'toggled', self.enableCellCB)

        # Output name column
        self.outputCell = gtk.CellRendererText()
        outputCol = gtk.TreeViewColumn("Output")
        outputCol.pack_start(self.outputCell, expand=True)
        outputCol.set_cell_data_func(self.outputCell, self.renderOutputCell)
        self.outputView.append_column(outputCol)

        # Output schedule column
        self.schedCell = gtk.CellRendererText()
        schedCol = gtk.TreeViewColumn("Schedule")
        schedCol.pack_start(self.schedCell, expand=True)
        schedCol.set_cell_data_func(self.schedCell, self.renderScheduleCB)
        self.outputView.append_column(schedCol)

        # Output destination column
        self.destCell = gtk.CellRendererText()
        destCol = gtk.TreeViewColumn("Destination")
        destCol.pack_start(self.destCell, expand=True)
        destCol.set_cell_data_func(self.destCell, self.renderDestinationCB)
        self.outputView.append_column(destCol)

        switchboard.requestCallbackMain("scheduled outputs changed",
                                        self.outputsChangedCB)
        switchboard.requestCallbackMain("new scheduled output",
                                        self.newOutputSBCB)

    def installed(self):
        self.update()
        self.sensitize()

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

    def currentOutput(self):
        debug.mainthreadTest()
        selection = self.outputView.get_selection()
        model, iter = selection.get_selected()
        if iter:
            return model[iter][0]

    def currentOutputName(self):
        o = self.currentOutput()
        if o:
            return o.name()

    def update(self):
        # update() does *not* call sensitize(), because there are some
        # cases in which other things need to be done first.  Any
        # function that calls update() should probably call
        # sensitize() too.
        debug.mainthreadTest()
        meshctxt = self.currentMeshContext()
        current = self.currentOutputName()
        # It's important to block the selection signal while clearing
        # the list, or else gtklogger will log the deselection of the
        # current selection.  Since selectOutput() blocks the signals,
        # the reselection won't be logged, and the next operation on
        # the selection will fail when a log script is replayed.
        self.selectionSignal.block()
        self.outputList.clear()
        self.selectionSignal.unblock()
        if meshctxt is not None:
            for output in meshctxt.outputSchedule.outputs:
                it = self.outputList.append([output])
            self.selectOutput(current)

    def selectOutput(self, name):
        for rowno, row in enumerate(self.outputList):
            # row is a TreeModelRow object. row[0] is a ScheduledOutput
            if row[0].name() == name:
                selection = self.outputView.get_selection()
                self.selectionSignal.block()
                try:
                    selection.select_path(rowno)
                finally:
                    self.selectionSignal.unblock()
                self.outputView.scroll_to_cell(rowno)

    def sensitize(self):
        debug.mainthreadTest()
        meshok = self.currentMeshContext() is not None
        output = self.currentOutput()
        outputok = output is not None
        outputsExist = (meshok and 
                        self.currentMeshContext().outputSchedule.nOutputs() > 0)

        self.newOutputButton.set_sensitive(meshok)
        self.editOutputButton.set_sensitive(outputok)
        self.copyOutputButton.set_sensitive(outputok)
        self.renameOutputButton.set_sensitive(outputok)
        self.deleteOutputButton.set_sensitive(outputok)
        self.deleteAllButton.set_sensitive(outputsExist)

        destinationok = (outputok and output.settableDestination and
                         output.destination is not None)
        self.rewindDestButton.set_sensitive(
            destinationok and output.destination.getRegistration().rewindable)
        self.rewindAllDestsButton.set_sensitive(outputsExist)

    def outputsChangedCB(self, meshctxt):
        # switchboard "scheduled outputs changed"
        if meshctxt is self.currentMeshContext():
            self.update()
            self.sensitize()

    def newOutputSBCB(self, meshctxt, outputname):
        # switchboard "new scheduled output"
        if meshctxt is self.currentMeshContext():
            self.update()
            self.selectOutput(outputname)
            self.sensitize()

    def meshCB(self, *args, **kwargs): # mesh widget changed state
        # debug.fmsg("updating")
        self.update()
        # debug.fmsg("sensitizing")
        self.sensitize()
        # debug.fmsg("done")

    ##############

    # TreeView selection and double click callbacks.

    def selectionCB(self, treeselection):
        debug.mainthreadTest()
        model, iter = treeselection.get_selected()
        if self.outputView.get_selection() is not treeselection:
            self.selectionSignal.block()
            try:
                if iter:
                    self.outputView.get_selection().select_iter(iter)
                else:
                    self.outputView.get_selection().unselect_all()
            finally:
                self.selectionSignal.unblock()
        self.sensitize()

    def outputDoubleClickCB(self, treeview, path, col):
        self.editOutputCB()
            
    ##############

    def renderEnableCell(self, column, cell_renderer, model, iter):
        debug.mainthreadTest()
        output = model[iter][0]
        cell_renderer.set_active(output.active)

    def enableCellCB(self, cell_renderer, path):
        debug.mainthreadTest()
        output = self.outputList[path][0]
        outputmenu.Enable(mesh=self.currentFullMeshName(),
                          output=output.name(),
                          enable=(not output.active))

    def renderOutputCell(self, column, cell_renderer, model, iter):
        debug.mainthreadTest()
        output = model[iter][0]
        cell_renderer.set_property('text', output.name())

        
    def renderScheduleCB(self, column, cell_renderer, model, iter):
        debug.mainthreadTest()
        output = model[iter][0]
        if output.schedule is not None:
            cell_renderer.set_property('text', output.schedule.shortrepr())
        else:
            cell_renderer.set_property('text', '---')

    def renderDestinationCB(self, column, cell_renderer, model, iter):
        debug.mainthreadTest()
        output = model[iter][0]
        if output.destination is not None:
            cell_renderer.set_property('text', output.destination.shortrepr())
        else:
            cell_renderer.set_property('text', '---')

    ############

    # Output button callbacks

    def newOutputCB(self, gtkbutton):
        # Create a new scheduled output
        menuitem = outputmenu.New
        params = filter(lambda a: a.name != 'mesh', menuitem.params)

        if parameterwidgets.getParameters(title='Define a new Output',
                                          scope=self,
                                          parentwindow=guitop.top().gtk,
                                          *params):
            menuitem.callWithDefaults(mesh=self.currentFullMeshName())

    def editOutputCB(self, *args):
        menuitem = outputmenu.Edit
        output = self.currentOutput()
        newoutputparam = menuitem.get_arg('new_output')
        newoutputparam.set(output)
        newschedtypeparam = menuitem.get_arg('new_scheduletype')
        newschedtypeparam.set(output.scheduleType)
        newscheduleparam = menuitem.get_arg('new_schedule')
        newscheduleparam.set(output.schedule)
        destparam = menuitem.get_arg('new_destination')
        destparam.set(output.destination)
        params = filter(lambda a: a.name not in ('mesh', 'output'), 
                        menuitem.params)
        if parameterwidgets.getParameters(title='Redefine an Output',
                                          scope=self,
                                          parentwindow=guitop.top().gtk,
                                          *params):
            menuitem.callWithDefaults(mesh=self.currentFullMeshName(),
                                      output=self.currentOutputName())

    def copyOutputCB(self, gtkbutton):
        menuitem = outputmenu.Copy
        output = self.currentOutput()
        targetmeshparam = menuitem.get_arg('targetmesh')
        targetmeshparam.set(self.currentFullMeshName())
        if parameterwidgets.getParameters(targetmeshparam,
                                          menuitem.get_arg('copy'),
                                          scope=self,
                                          title="Copy an Output",
                                          parentwindow=guitop.top().gtk):
            menuitem.callWithDefaults(mesh=self.currentFullMeshName(),
                                      source=self.currentOutputName())

    def renameCB(self, gtkbutton):
        menuitem = outputmenu.Rename
        nameparam = menuitem.get_arg('name')
        name = self.currentOutputName()
        nameparam.set(name)
        if parameterwidgets.getParameters(nameparam,
                                          title='Rename output "%s"'%name,
                                          scope=self,
                                          parentwindow=guitop.top().gtk):
            menuitem.callWithDefaults(mesh=self.currentFullMeshName(),
                                      output=self.currentOutputName())

    def deleteOutputCB(self, gtkbutton):
        outputmenu.Delete.callWithDefaults(mesh=self.currentFullMeshName(),
                                           output=self.currentOutputName())
    def deleteAllCB(self, gtkbutton):
        outputmenu.DeleteAll.callWithDefaults(mesh=self.currentFullMeshName())

    ##############

    def rewindDestinationCB(self, gtkbutton):
        menuitem = outputmenu.Rewind
        menuitem.callWithDefaults(mesh=self.currentFullMeshName(),
                                  output=self.currentOutputName())

    def rewindAllDestinationsCB(self, gtkbutton):
        menuitem = outputmenu.RewindAll
        menuitem.callWithDefaults(mesh=self.currentFullMeshName())

op = OutputPage()
