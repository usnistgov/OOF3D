# -*- python -*-
# $RCSfile: solverPage.py,v $
# $Revision: 1.87.10.11 $
# $Author: langer $
# $Date: 2014/11/07 20:31:09 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.SWIG.common import config
from ooflib.SWIG.common import guitop
from ooflib.SWIG.common import lock
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.engine import field
from ooflib.common import debug
from ooflib.common import labeltree
from ooflib.common import mainthread
from ooflib.common import utils
from ooflib.common.IO import parameter
from ooflib.common.IO import reporter
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import gtkutils
from ooflib.common.IO.GUI import oofGUI
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import reporter_GUI
from ooflib.common.IO.GUI import tooltips
from ooflib.common.IO.GUI import whowidget
from ooflib.engine import fieldinit
from ooflib.engine import meshstatus
from ooflib.engine import subproblemcontext
import ooflib.engine.IO.meshmenu
import ooflib.engine.IO.subproblemmenu
import ooflib.engine.mesh

import gobject
import gtk

meshmenu = ooflib.engine.IO.meshmenu.meshmenu
subpmenu = ooflib.engine.IO.subproblemmenu.subproblemMenu

class SolverPage(oofGUI.MainPage):
    def __init__(self):
        oofGUI.MainPage.__init__(
            self, name="Solver",
            ordering=240,
            tip="Find solutions for static and time-dependent problems.")
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

        mainvpane = gtk.VPaned()
        gtklogger.setWidgetName(mainvpane, 'VPane')
        mainbox.pack_start(mainvpane, expand=1, fill=1)
        gtklogger.connect_passive(mainvpane, 'notify::position')

        # Subproblem pane

        ## TODO 3.1: Make it possible to reorder the subproblems by
        ## drag and drop.

        subprobframe = gtk.Frame('Solvers')
        gtklogger.setWidgetName(subprobframe, "Subproblems")
        subprobframe.set_shadow_type(gtk.SHADOW_IN)
        mainvpane.pack1(subprobframe, resize=1, shrink=0)
        subpvbox = gtk.VBox()   # contains scrolled list and buttons
        subpvbox.set_border_width(3)
        subprobframe.add(subpvbox)
        innerframe = gtk.Frame()
        innerframe.set_shadow_type(gtk.SHADOW_IN)
        subpvbox.pack_start(innerframe, expand=1, fill=1)
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
                          self.subpActivateRowCB)

        # Order number in the first column
        ordercell = gtk.CellRendererText()
        ordercol = gtk.TreeViewColumn("Order")
        ordercol.set_resizable(False)
        ordercol.pack_start(ordercell, expand=False)
        ordercol.set_cell_data_func(ordercell, self.renderSubproblemOrder)
        self.subpListView.append_column(ordercol)
        # Checkbox in the second column
        solvecell = gtk.CellRendererToggle()
        solvecol = gtk.TreeViewColumn("Solve?")
        solvecol.pack_start(solvecell, expand=False)
        solvecol.set_cell_data_func(solvecell, self.renderSolveCell)
        self.subpListView.append_column(solvecol)
        gtklogger.adoptGObject(solvecell, self.subpListView,
                               access_function=gtklogger.findCellRenderer,
                               access_kwargs={'col':1, 'rend':0})
        gtklogger.connect(solvecell, 'toggled', self.solvecellCB)
        # Subproblem name in the third column
        namecell = gtk.CellRendererText()
        namecol = gtk.TreeViewColumn("Subproblem")
        namecol.set_resizable(True)
        namecol.pack_start(namecell, expand=True)
        namecol.set_cell_data_func(namecell, self.renderSubproblemName)
        self.subpListView.append_column(namecol)
        # Solver in the fourth column
        solvercell = gtk.CellRendererText()
        solvercol = gtk.TreeViewColumn("Solver")
        solvercol.set_resizable(True)
        solvercol.pack_start(solvercell, expand=True)
        solvercol.set_cell_data_func(solvercell, self.renderSubproblemSolver)
        self.subpListView.append_column(solvercol)

        # Buttons at the bottom of the subproblem pane
        subpbbox = gtk.HBox(homogeneous=True)
        subpvbox.pack_start(subpbbox, expand=0, fill=0)
        # Set Solver
        self.setSolverButton = gtkutils.StockButton(gtk.STOCK_ADD, "Set...")
        gtklogger.setWidgetName(self.setSolverButton, "Set")
        gtklogger.connect(self.setSolverButton, 'clicked', self.setSolverCB)
        subpbbox.pack_start(self.setSolverButton, expand=0, fill=1)
        tooltips.set_tooltip_text(self.setSolverButton,
            "Assign a solver to the selected subproblem.")
        # Copy Solver
        self.copySolverButton = gtkutils.StockButton(gtk.STOCK_COPY, "Copy...")
        gtklogger.setWidgetName(self.copySolverButton, "Copy")
        gtklogger.connect(self.copySolverButton, 'clicked', self.copySolverCB)
        subpbbox.pack_start(self.copySolverButton, expand=0, fill=1)
        tooltips.set_tooltip_text(
            self.copySolverButton,
            "Copy the selected solver to another subproblem,"
            " possibly in another mesh.")
        # Copy All Solvers
        self.copyAllSolversButton = gtkutils.StockButton(gtk.STOCK_COPY,
                                                         "Copy All...")
        gtklogger.setWidgetName(self.copyAllSolversButton, "CopyAll")
        gtklogger.connect(self.copyAllSolversButton, 'clicked',
                          self.copyAllSolversCB)
        subpbbox.pack_start(self.copyAllSolversButton, expand=0, fill=1)
        tooltips.set_tooltip_text(
            self.copyAllSolversButton,
            "Copy all solvers to identically named subproblems in another mesh.")
        # Remove Solver
        self.removeSolverButton = gtkutils.StockButton(gtk.STOCK_REMOVE,
                                                       "Remove")
        gtklogger.setWidgetName(self.removeSolverButton, "Remove")
        gtklogger.connect(self.removeSolverButton, 'clicked',
                          self.removeSolverCB)
        subpbbox.pack_start(self.removeSolverButton, expand=0, fill=1)
        tooltips.set_tooltip_text(self.removeSolverButton,
            "Delete the solver from the selected subproblem.")
        # Remove all solvers
        self.removeAllSolversButton = gtkutils.StockButton(gtk.STOCK_CLEAR,
                                                           "Remove All")
        gtklogger.setWidgetName(self.removeAllSolversButton, "RemoveAll")
        gtklogger.connect(self.removeAllSolversButton, 'clicked',
                          self.removeAllSolversCB)
        subpbbox.pack_start(self.removeAllSolversButton, expand=0, fill=1)
        tooltips.set_tooltip_text(self.removeAllSolversButton,
            "Remove the solver from all subproblems.")
        # Second row of buttons at the bottom of the subproblem pane
        subpbbox = gtk.HBox(homogeneous=True)
        subpvbox.pack_start(subpbbox, expand=0, fill=0)
        # Solve this subproblem first
        self.firstButton = gtkutils.StockButton(gtk.STOCK_GOTO_FIRST, "First",
                                                align=0.0)
        gtklogger.setWidgetName(self.firstButton, "First")
        gtklogger.connect(self.firstButton, 'clicked', self.firstButtonCB)
        subpbbox.pack_start(self.firstButton, expand=0, fill=1)
        tooltips.set_tooltip_text(
            self.firstButton,
            "Solve the selected subproblem first when iterating"
            " over subproblems.")
        # Solve this subproblem earlier
        self.earlierButton = gtkutils.StockButton(gtk.STOCK_GO_BACK, "Earlier",
                                                  align=0.0)
        gtklogger.setWidgetName(self.earlierButton, "Earlier")
        gtklogger.connect(self.earlierButton, 'clicked', self.earlierButtonCB)
        subpbbox.pack_start(self.earlierButton, expand=0, fill=1)
        tooltips.set_tooltip_text(
            self.earlierButton,
            "Solve the selected subproblem before the one above it"
            " in the list when iterating over subproblems.")
        # Solve this subproblem later
        self.laterButton = gtkutils.StockButton(gtk.STOCK_GO_FORWARD, "Later",
                                                reverse=True, align=1.0)
        gtklogger.setWidgetName(self.laterButton, "Later")
        gtklogger.connect(self.laterButton, 'clicked', self.laterButtonCB)
        subpbbox.pack_start(self.laterButton, expand=0, fill=1)
        tooltips.set_tooltip_text(
            self.laterButton,
            "Solve the selected subproblem after the next one in the"
            " list when iterating over subproblems.")
        # Solve this subproblem last
        self.lastButton = gtkutils.StockButton(gtk.STOCK_GOTO_LAST, "Last",
                                               reverse=True, align=1.0)
        gtklogger.setWidgetName(self.lastButton, "Last")
        gtklogger.connect(self.lastButton, 'clicked', self.lastButtonCB)
        subpbbox.pack_start(self.lastButton, expand=0, fill=1)
        tooltips.set_tooltip_text(
            self.lastButton,
            "Solve the selected subproblem last when iterating"
            " over subproblems.")

        # Field Initializers
        initframe = gtk.Frame('Initialization')
        gtklogger.setWidgetName(initframe, "FieldInit")
        initframe.set_shadow_type(gtk.SHADOW_IN)
        mainvpane.pack2(initframe, resize=1, shrink=0)
        ivbox = gtk.VBox()
        ivbox.set_border_width(3)
        initframe.add(ivbox)
        self.initscroll = gtk.ScrolledWindow()
        gtklogger.logScrollBars(self.initscroll, "Scroll")
        self.initscroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.initscroll.set_shadow_type(gtk.SHADOW_IN)
        ivbox.pack_start(self.initscroll, expand=1, fill=1)
        # The ListStore just contains the defined Fields.  The
        # TreeView displays their names and initializers.
        self.initlist = gtk.ListStore(gobject.TYPE_PYOBJECT)
        self.initview = gtk.TreeView(self.initlist)
        gtklogger.setWidgetName(self.initview, 'Initializers')
        self.initscroll.add(self.initview)
        self.initview.set_headers_clickable(False)
        fieldnamecell = gtk.CellRendererText()
        fieldnamecol = gtk.TreeViewColumn('Field or BC')
        self.initview.append_column(fieldnamecol)
        fieldnamecol.pack_start(fieldnamecell, expand=False)
        fieldnamecol.set_cell_data_func(fieldnamecell, self.renderFieldName)

        fieldinitcell = gtk.CellRendererText()
        fieldinitcol = gtk.TreeViewColumn('Initializer')
        self.initview.append_column(fieldinitcol)
        fieldinitcol.pack_start(fieldinitcell, expand=True)
        fieldinitcol.set_cell_data_func(fieldinitcell, self.renderFieldInit)

        selection = self.initview.get_selection()
        gtklogger.adoptGObject(selection, self.initview,
                               access_method=self.initview.get_selection)
        self.initselsignal = gtklogger.connect(selection, 'changed',
                                               self.initSelectCB)
        gtklogger.connect(self.initview, 'row-activated',
                          self.initActivateRowCB)

        bbox = gtk.HBox(homogeneous=True)
        ivbox.pack_start(bbox, expand=0, fill=0)
        # Set button
        self.fieldinitbutton=gtkutils.StockButton(gtk.STOCK_ADD, 'Set...')
        gtklogger.setWidgetName(self.fieldinitbutton, "Set")
        gtklogger.connect(self.fieldinitbutton, 'clicked',
                          self.fieldinitbuttonCB)
        tooltips.set_tooltip_text(
            self.fieldinitbutton,'Initialized the selected field.')
        bbox.pack_start(self.fieldinitbutton, expand=0, fill=1)
        # Copy button
        self.copyinitbutton = gtkutils.StockButton(gtk.STOCK_COPY,
                                                   "Copy All...")
        gtklogger.setWidgetName(self.copyinitbutton, 'CopyInit')
        gtklogger.connect(self.copyinitbutton, 'clicked', self.copyinitCB)
        bbox.pack_start(self.copyinitbutton, expand=0, fill=1)
        tooltips.set_tooltip_text(self.copyinitbutton,
            "Copy field initializers from the current mesh to another mesh.")
        # Clear Initializer button
        self.clearinitbutton = gtkutils.StockButton(gtk.STOCK_REMOVE, "Clear")
        gtklogger.setWidgetName(self.clearinitbutton, "Clear")
        gtklogger.connect(self.clearinitbutton, 'clicked', self.clearinitCB)
        bbox.pack_start(self.clearinitbutton, expand=0, fill=1)
        tooltips.set_tooltip_text(self.clearinitbutton,
            "Remove the selected field initializer from the current mesh.")
        # Clear All Initializers button
        self.clearallinitsbutton = gtkutils.StockButton(gtk.STOCK_CLEAR,
                                                        "Clear All")
        gtklogger.setWidgetName(self.clearallinitsbutton, 'ClearAll')
        gtklogger.connect(self.clearallinitsbutton, 'clicked',
                          self.clearallinitsCB)
        bbox.pack_start(self.clearallinitsbutton, expand=0, fill=1)
        tooltips.set_tooltip_text(self.clearallinitsbutton,
            "Remove the field initializers from the current mesh.")

        # Second row of buttons in the Field Initialization pane
        bbox = gtk.HBox(homogeneous=True)
        ivbox.pack_start(bbox, expand=0, fill=1)
        # Apply button
        self.applyinitbutton = gtkutils.StockButton(gtk.STOCK_APPLY, "Apply")
        gtklogger.setWidgetName(self.applyinitbutton, "Apply")
        gtklogger.connect(self.applyinitbutton, 'clicked', self.applyinitCB)
        tooltips.set_tooltip_text(self.applyinitbutton,
            "Apply initializers to all fields at the current time.")
        bbox.pack_start(self.applyinitbutton, expand=0, fill=1)
        # Apply At button
        self.applyinitattimebutton = gtkutils.StockButton(gtk.STOCK_APPLY,
                                                          "Apply at time...")
        gtklogger.setWidgetName(self.applyinitattimebutton, "ApplyAt")
        gtklogger.connect(self.applyinitattimebutton, 'clicked',
                          self.applyinitatCB)
        tooltips.set_tooltip_text(self.applyinitattimebutton,
            "Reset the current time and apply all field initializers.")
        bbox.pack_start(self.applyinitattimebutton, expand=0, fill=1)

        # Table containing status, time entries and Solve button
        table = gtk.Table(rows=2, columns=4)
        mainbox.pack_start(table, expand=0, fill=1)

        # The start time isn't set directly by the user, except by
        # applying field initializers at a given time.  It's displayed
        # in a desensitized gtk.Entry.
        label = gtk.Label('current time=')
        label.set_alignment(1.0, 0.5)
        table.attach(label, 0,1, 0,1, xpadding=3, xoptions=~gtk.EXPAND)
        self.currentTimeEntry = gtk.Entry()
        self.currentTimeEntry.set_sensitive(False) # never sensitive
        table.attach(self.currentTimeEntry, 1,2, 0,1, xpadding=3)
        
        # End time is set by the user.
        label = gtk.Label('end time=')
        label.set_alignment(1.0, 0.5)
        table.attach(label, 0,1, 1,2, xpadding=3, xoptions=~gtk.EXPAND)
        self.endtimeEntry = gtk.Entry()
        gtklogger.setWidgetName(self.endtimeEntry, 'end')
        gtklogger.connect(self.endtimeEntry, 'changed', self.timeChangeCB)
        table.attach(self.endtimeEntry, 1,2, 1,2, xpadding=3)

        statusFrame = gtk.Frame("Status")
        statusFrame.set_shadow_type(gtk.SHADOW_IN)
        vbox = gtk.VBox()
        statusFrame.add(vbox)
        self.statusLabel = gtk.Label()
        self.statusLabel.set_alignment(0.5, 0.5)
        table.attach(statusFrame, 2,3, 0,3, xpadding=3)
        vbox.pack_start(self.statusLabel, expand=0, fill=0)
        align = gtk.Alignment(xalign=0.5)
        vbox.pack_start(align, expand=0, fill=0, padding=3)
        self.statusDetailButton = gtk.Button("Details...")
        gtklogger.setWidgetName(self.statusDetailButton, 'status')
        gtklogger.connect(self.statusDetailButton, 'clicked', self.statusCB)
        align.add(self.statusDetailButton)

        solveFrame0 = gtk.Frame()
        solveFrame0.set_shadow_type(gtk.SHADOW_OUT)
        solveFrame1 = gtk.Frame()
        solveFrame1.set_shadow_type(gtk.SHADOW_IN)
        solveFrame0.add(solveFrame1)
        table.attach(solveFrame0, 3,4, 0,3, xpadding=3,
                     xoptions=~gtk.EXPAND)
        self.solveButton = gtkutils.StockButton(gtk.STOCK_EXECUTE,
                                                '<b>Solve</b>', markup=True)
        self.solveButton.set_border_width(4)
        gtklogger.setWidgetName(self.solveButton, 'solve')
        gtklogger.connect(self.solveButton, 'clicked', self.solveCB)
        solveFrame1.add(self.solveButton)

        switchboard.requestCallbackMain("field defined", self.defineFldCB)
        switchboard.requestCallbackMain("field initializer set", self.initFldCB)
        switchboard.requestCallbackMain("subproblem changed",
                                        self.subproblemsChangedCB)
        switchboard.requestCallbackMain("mesh changed",
                                        self.subproblemsChangedCB)
        switchboard.requestCallbackMain("subproblem solvability changed",
                                        self.subpSolverChangedCB)
        switchboard.requestCallbackMain("subproblem solver changed",
                                        self.subpSolverChangedCB)
        switchboard.requestCallbackMain("subproblem solvers changed",
                                        self.subpSolversChangedCB),
        switchboard.requestCallbackMain("subproblems reordered",
                                        self.subproblemsChangedCB),
        switchboard.requestCallbackMain(("new who", "SubProblem"),
                                        self.subproblemsChangedCB)
        switchboard.requestCallbackMain(("rename who", "SubProblem"),
                                        self.subproblemsChangedCB)
        switchboard.requestCallbackMain(("remove who", "SubProblem"),
                                        self.subproblemsChangedCB)
        switchboard.requestCallbackMain("time changed",
                                        self.meshTimeChangedCB)
        switchboard.requestCallbackMain("mesh solved", self.meshSolvedCB)
        switchboard.requestCallbackMain("mesh status changed",
                                        self.statusChangedCB)
        switchboard.requestCallbackMain("made reservation",
                                        self.reservationCB)
        switchboard.requestCallbackMain("cancelled reservation",
                                        self.reservationCB)

    def installed(self):
        self.update()

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

    def update(self):
        self.updateSubproblems()
        self.updateInitializers()
        self.updateTime()
        self.updateStatus()
        self.sensitize()

    def reservationCB(self, who): # sb "made/cancelled reservation"
        if self.currentFullMeshName() == who.path():
            self.sensitize()

    def meshCB(self, *args, **kwargs): # mesh widget changed state
        self.update()

    def sensitize(self):
        ## TODO OPT: This is called an awful lot. Can it be reduced?
        ## Does it matter?
        debug.mainthreadTest()
        meshctxt = self.currentMeshContext()
        meshok = (meshctxt is not None and not meshctxt.query_reservation()
                  and not meshctxt.outOfSync())
        timedependent = meshctxt and meshctxt.timeDependent()
        if meshok:
            ninit = len(meshctxt.initializers) + meshctxt.n_initialized_bcs()
            anyinits = ninit > 0
            endtime = self.endTime(meshctxt)
        else:
            ninit = 0
            anyinits = False
            endtime = None

        subpctxt = self.currentSubProblemContext() # currently selected subProb
        subpok = subpctxt is not None and not subpctxt.query_reservation()
        fld, bc = self.selectedFieldOrBC()
        fieldok = fld is not None
        bcok = bc is not None

        # list of all subproblems to be solved
        if meshok:
            subprobs = [s for s in meshctxt.subproblems()
                        if (s.solver_mode and s.solveFlag)]
        else:
            subprobs = []

        solversok = len(subprobs) > 0 # can subproblems be solved?
        nsolvers = 0
        for subp in subprobs:
            subpobj = subp.getObject()
            solversok = (solversok and
                         subp.materialsConsistent() and
                         not subp.query_reservation() and
                         subpobj.n_active_eqns() > 0 and
                         subpobj.n_active_fields() > 0)
            if subp.solver_mode:
                nsolvers += 1

        self.setSolverButton.set_sensitive(subpok)
        self.copySolverButton.set_sensitive(subpok and
                                            subpctxt.solver_mode is not None)
        self.copyAllSolversButton.set_sensitive(meshok and nsolvers > 0)
        self.removeSolverButton.set_sensitive(subpok and
                                              subpctxt.solver_mode is not None)
        self.removeAllSolversButton.set_sensitive(meshok and nsolvers > 0)

        if subpok:
            suborder = subpctxt.solveOrder
            nsubs = meshctxt.nSubproblems()
        self.firstButton.set_sensitive(subpok and suborder > 0)
        self.earlierButton.set_sensitive(subpok and suborder > 0)
        self.laterButton.set_sensitive(subpok and suborder < nsubs-1)
        self.lastButton.set_sensitive(subpok and suborder < nsubs-1)
        
        ### Initialization Pane sensitization

        self.initview.set_sensitive(meshok)
        self.fieldinitbutton.set_sensitive(meshok and (fieldok or bcok))
        self.copyinitbutton.set_sensitive(meshok and ninit > 0)
        self.clearinitbutton.set_sensitive(
            meshok and (
                (fieldok and meshctxt.get_initializer(fld) is not None)
                or (bcok and bc.get_initializer() is not None)))
        self.clearallinitsbutton.set_sensitive(meshok and ninit > 0)
        self.applyinitbutton.set_sensitive(anyinits)
        self.applyinitattimebutton.set_sensitive(anyinits)

        ## Time pane sensitization

        self.endtimeEntry.set_sensitive(meshok)
        # self.stepsizeEntry.set_sensitive(meshok)

        timesok = (meshok and
                   ((endtime is not None and
                     meshctxt.getCurrentTime() <= endtime)
                    or not timedependent))
        self.solveButton.set_sensitive(timesok and solversok and
                                       meshctxt.status.solvable)

        if (meshctxt is not None
            and isinstance(meshctxt.status, (meshstatus.Solving,
                                             meshstatus.Solved))
            and timedependent):
            self.solveButton.relabel("Continue")
        else:
            self.solveButton.relabel("Solve")
        self.statusDetailButton.set_sensitive(meshctxt is not None)

        gtklogger.checkpoint("Solver page sensitized")

    ####################

    # Support functions for the SubProblem pane

    def currentSubProblemContext(self):
        debug.mainthreadTest()
        selection = self.subpListView.get_selection()
        model, iter = selection.get_selected()
        if iter:
            return model[iter][0]
    def currentFullSubProblemName(self):
        ctxt = self.currentSubProblemContext()
        if ctxt:
            return ctxt.path()
    def currentSubProblemName(self):
        ctxt = self.currentSubProblemContext()
        if ctxt:
            return ctxt.name()
    def orderedSubProblemNames(self):
        return [s[0].name() for s in self.subprobList]

    # TreeView callback for displaying the subproblem order.
    def renderSubproblemOrder(self, column, cell_renderer, model, iter):
        debug.mainthreadTest()
        rowno = model.get_path(iter)[0]
        cell_renderer.set_property('text', `rowno`)

    # TreeView callback for setting the state of the 'Solve' button
    # for each SubProblem
    def renderSolveCell(self, column, cell_renderer, model, iter):
        debug.mainthreadTest()
        subproblemctxt = model[iter][0]
        cell_renderer.set_active(subproblemctxt.solveFlag)

    def renderSubproblemName(self, column, cell_renderer, model, iter):
        debug.mainthreadTest()
        subpctxt = model[iter][0]
        cell_renderer.set_property('text', subpctxt.name())

    def renderSubproblemSolver(self, column, cell_renderer, model, iter):
        debug.mainthreadTest()
        subpctxt = model[iter][0]
        if subpctxt.solver_mode:
            cell_renderer.set_property(
                'text',
                subpctxt.solver_string() )
        else:
            cell_renderer.set_property('text', '<none>')

    # gtk callback for clicks on a subproblem's 'Solve' button.  This
    # just toggles whether or not the subproblem is being solved.
    def solvecellCB(self, cell_renderer, path):
        debug.mainthreadTest()
        subproblemctxt = self.subprobList[path][0]
        solvable = not subproblemctxt.solveFlag
        if solvable:
            subpmenu.Enable_Solution(subproblem=subproblemctxt.path())
        else:
            subpmenu.Disable_Solution(subproblem=subproblemctxt.path())

    def setSolverCB(self, *args): # gtk callback
        menuitem = subpmenu.Set_Solver
        subp = self.currentSubProblemContext()
        mode_arg = menuitem.get_arg('solver_mode')
        mode_arg.set(subp.solver_mode)
        if parameterwidgets.getParameters(mode_arg,
                                          title='Specify Solver',
                                          parentwindow=guitop.top().gtk,
                                          scope=self):
            menuitem.callWithDefaults(
                subproblem=self.currentFullSubProblemName())

    def copySolverCB(self, *args): # gtk callback
        menuitem = subpmenu.Copy_Solver
        targetparam = menuitem.get_arg("target")
        targetparam.set(self.currentFullSubProblemName())
        if parameterwidgets.getParameters(
            targetparam,
            title="Copy a Solver to a Subproblem"):
            menuitem.callWithDefaults(source=self.currentFullSubProblemName())

    def copyAllSolversCB(self, *args):
        menuitem = meshmenu.Copy_All_Solvers
        targetparam = menuitem.get_arg("target")
        targetparam.set(self.currentFullMeshName())
        if parameterwidgets.getParameters(
            targetparam,
            title="Copy all Solvers to a Mesh"):
            menuitem.callWithDefaults(source=self.currentFullMeshName())

    def removeSolverCB(self, button): # gtk callback
        subpmenu.Remove_Solver(subproblem=self.currentFullSubProblemName())

    def removeAllSolversCB(self, button): # gtk callback
        meshmenu.Remove_All_Solvers(mesh=self.currentFullMeshName())

    # Button callbacks for reordering subproblems
    def firstButtonCB(self, *args):
        subp = self.currentSubProblemName()
        names = self.orderedSubProblemNames()
        names.remove(subp)
        meshmenu.ReorderSubproblems(mesh=self.currentFullMeshName(),
                                    subproblems=[subp]+names)
    def earlierButtonCB(self, *args):
        subp = self.currentSubProblemName()
        names = self.orderedSubProblemNames()
        which = names.index(subp)
        names[which-1:which+1] = [subp, names[which-1]]
        meshmenu.ReorderSubproblems(mesh=self.currentFullMeshName(),
                                    subproblems=names)
    def laterButtonCB(self, *args):
        subp = self.currentSubProblemName()
        names = self.orderedSubProblemNames()
        which = names.index(subp)
        names[which:which+2] = [names[which+1], subp]
        meshmenu.ReorderSubproblems(mesh=self.currentFullMeshName(),
                                    subproblems=names)
    def lastButtonCB(self, *args):
        subp = self.currentSubProblemName()
        names = self.orderedSubProblemNames()
        names.remove(subp)
        meshmenu.ReorderSubproblems(mesh=self.currentFullMeshName(),
                                    subproblems=names+[subp])

    # gtk callback, subproblem selection changed
    def subpSelectCB(self, selection):
        self.sensitize()

    # gtk callback, double click or <return> on subproblem list
    def subpActivateRowCB(self, treeview, path, col):
        self.setSolverCB()

    def updateSubproblems(self):
        debug.mainthreadTest()
        currentSub = self.currentSubProblemContext()
        self.subpselsig.block()
        try:
            self.subprobList.clear()
            meshctxt = self.currentMeshContext()
            if meshctxt is None:
                return
            subprobs = [(s.solveOrder,s) for s in meshctxt.subproblems()]
            subprobs.sort()
            for order, subprob in subprobs:
	        if subprob.consistency():#Check the subproblem consistency. Before even rendering it here.
		    it = self.subprobList.append([subprob])
		    if subprob is currentSub:
			# Reselect previous selection
			self.subpListView.get_selection().select_iter(it)
        finally:
            self.subpselsig.unblock()

    def subpSolverChangedCB(self, subpname):
        # switchboard "subproblem solvability changed" or "subproblem
        # solver changed".
        # Find which subproblem it is in the list, and tell the
        # TreeView that one of its rows has changed.
        debug.mainthreadTest()
        subpctxt = subproblemcontext.subproblems[subpname]
        rowno = 0
        for row in self.subprobList:
            if row[0] is subpctxt:
                self.subprobList.row_changed(rowno,
                                             self.subprobList.get_iter(rowno))
                self.sensitize()
                # Changing solvers can change which fields can be
                # initialized.
                self.updateInitializers()
                return
            rowno += 1

    def subpSolversChangedCB(self, *args):
        # switchboard "subproblem solvers changed".  Note the plural...
        # Called by OOF.Mesh.Remove_All_Solvers.
        self.updateSubproblems()
        self.updateInitializers()
        self.sensitize()

    def subproblemsChangedCB(self, *args):
        # switchboard "new who", "rename who", etc.
        self.updateSubproblems()
        self.updateInitializers()
        self.updateStatus()
        self.sensitize()

    ####################

    # Support functions for the Initialization pane

    def fieldinitbuttonCB(self, *args): # gtk callback, initialize field
        fld, bc = self.selectedFieldOrBC()
        if fld is not None:
            menuitem = meshmenu.Set_Field_Initializer
            # We can't simply use
            # parameter.getParameters(menuitem.get_arg('initializer'))
            # here, because the menu item's parameter accepts members
            # of the FieldInit base class, but we need to create a
            # widget for the appropriate derived class
            # (ScalarFieldInit, et al).  It's the derived classes that
            # are the registered classes.
            param = parameter.RegisteredParameter(
                'initializer', fieldinit.fieldInitDict[fld.classname()])

            # Set the parameter value to the current initializer of
            # the appropriate field in the current mesh (context) --
            # this is the value that the initializer widget will start
            # with.  If it doesn't get set here, it will just have the
            # most recently-set one, which may be for a different
            # mesh.
            param.value = self.currentMeshContext().get_initializer(fld)

            init = parameterwidgets.getParameterValues(
                param, title = 'Initialize field ' + fld.name(), scope=self)

            if init is not None:
                menuitem.callWithDefaults(mesh=self.currentFullMeshName(),
                                          field=fld,
                                          initializer=init[0])
        if bc is not None:
            menuitem = meshmenu.Boundary_Conditions.Set_BC_Initializer
            iparam = menuitem.get_arg('initializer')
            iparam.set(bc.get_initializer())
            bcparam = menuitem.get_arg('bc')
            bcparam.set(bc.name())
            # Make a bc parameter widget and put it in the local
            # widgetscope so that the initializer RCF can find it.
            bcwidget = bcparam.makeWidget()
            self.addWidget(bcwidget)
            if parameterwidgets.getParameters(
                iparam,
                scope=self,
                title='Initialize BC ' + bc.name()):
                menuitem.callWithDefaults(mesh=self.currentFullMeshName())
            self.removeWidget(bcwidget)
            bcwidget.destroy()

    def initFldCB(self):                # sb "field initializer set"
        # This function really should just emit the ListStore signal
        # that causes its TreeView to update.  Presumably that's easy
        # to do, but I don't know how at the moment, so I'll just
        # rebuild the list entirely.
        self.updateInitializers()

    def defineFldCB(self, subpname, fieldname, defined): # sb "field defined"
        subppath = labeltree.makePath(subpname)
        if subppath[:-1] == labeltree.makePath(self.currentFullMeshName()):
            self.updateInitializers()
            self.sensitize()

    def copyinitCB(self, button): # gtk callback, copy field initializers
        menuitem = meshmenu.Copy_Field_Initializers
        targetparam = menuitem.get_arg("target")
        targetparam.set(self.currentFullMeshName())
        if parameterwidgets.getParameters(targetparam,
                                          parentwindow=guitop.top().gtk,
                                          title="Select a target Mesh"):
            menuitem.callWithDefaults(source=self.currentFullMeshName())

    def clearinitCB(self, button): # clear field initializer button callback
        fld, bc = self.selectedFieldOrBC()
        if fld is not None:
            menuitem = meshmenu.Clear_Field_Initializer
            menuitem.callWithDefaults(mesh=self.currentFullMeshName(),
                                      field=fld)
        if bc is not None:
            menuitem = meshmenu.Boundary_Conditions.Clear_BC_Initializer
            menuitem.callWithDefaults(mesh=self.currentFullMeshName(),
                                      bc=bc.name())

    def clearallinitsCB(self, button): # clear all field initializers button
        menuitem = meshmenu.Clear_Field_Initializers # clears BCs as well
        menuitem.callWithDefaults(mesh=self.currentFullMeshName())

    def applyinitCB(self, button): # apply all field initializers button
        menuitem = meshmenu.Apply_Field_Initializers
        menuitem.callWithDefaults(mesh=self.currentFullMeshName())

    def applyinitatCB(self, button): # apply all initializers and set time
        menuitem = meshmenu.Apply_Field_Initializers_at_Time
        if parameterwidgets.getParameters(
            menuitem.get_arg('time'), title="Initialize Fields at Time"):
            menuitem.callWithDefaults(mesh=self.currentFullMeshName())

    # Functions that the TreeView machinery calls to fill in the
    # cells.  These will never be called for undefined fields, so
    # there's no need to check that the mesh or field exists.
    def renderFieldName(self, column, cell_renderer, model, iter):
        debug.mainthreadTest()
        obj = model[iter][0]    # Either a Field or a BC
        cell_renderer.set_property('text', obj.name())

    def renderFieldInit(self, column, cell_renderer, model, iter):
        debug.mainthreadTest()
        obj = model[iter][0]    # Either a Field or a BC
        mesh = self.currentMeshContext()
        if mesh:
            if isinstance(obj, field.FieldPtr):
                init = mesh.get_initializer(obj)
            else:               # it's a BC
                init = obj.get_initializer()
            if init is not None:
                cell_renderer.set_property('text', init.shortrepr())
            else:
                cell_renderer.set_property('text', '---')
        else:                   # No mesh?  Is this possible?
            cell_renderer.set_property('text', '')

    def updateInitializers(self):
        debug.mainthreadTest()
        currentObj = self.selectedObj()
        self.initlist.clear()
        mesh = self.currentMeshContext()
        if mesh:
            for field in mesh.all_initializable_fields():
                # debug.fmsg("field", field, field.classname())
                self.initlist.append([field])
            for name, bc in mesh.allBoundaryConds():
                if bc.initializable(mesh):
                    self.initlist.append([bc])
            if currentObj is not None:
                for row in range(len(self.initlist)):
                    if self.initlist[row][0] == currentObj:
                        self.initview.get_selection().select_path(row)
                        break

    def initSelectCB(self, selection):
        # gtk callback. Field init selection changed
        self.sensitize()

    def initActivateRowCB(self, treeview, path, col):
        # gtk callback. Field init row activated (double click or return)
        self.fieldinitbuttonCB()

    # Get the Field or BC currently selected in the initializer TreeView
    def selectedObj(self):
        debug.mainthreadTest()
        selection = self.initview.get_selection() # TreeSelection object
        model, iter = selection.get_selected()
        if iter:
            return model[iter][0]

    def selectedFieldOrBC(self):
        obj = self.selectedObj()
        if obj is None:
            return (None, None)
        if isinstance(obj, field.FieldPtr):
            return (obj, None)
        return (None, obj)

    ####################

    # Support functions for the time entries and the Solve button

    def updateTime(self):
        debug.mainthreadTest()
        meshctxt = self.currentMeshContext()
        if meshctxt:
            time = meshctxt.getObject().latestTime()
            self.currentTimeEntry.set_text(`time`)
        else:
            self.currentTimeEntry.set_text("")

    def updateEndTime(self):
        debug.mainthreadTest()
        meshctxt = self.currentMeshContext()
        if meshctxt and meshctxt.timeDiff is not None:
            time = meshctxt.getObject().getCurrentTime()
            self.endtimeEntry.set_text(`time + meshctxt.timeDiff`)
        else:
            self.endtimeEntry.set_text("")

    def updateStatus(self):
        debug.mainthreadTest()
        meshctxt = self.currentMeshContext()
        if meshctxt:
            self.statusLabel.set_text(meshctxt.status.tag)
        else:
            self.statusLabel.set_text("No mesh!")

    def endTime(self, meshctxt):
        txt = mainthread.runBlock(self.getEndTimeText)
        if not txt:
            # If the problem isn't time dependent and endtime isn't
            # set explicitly, just set it to the current time. 
            if meshctxt and not meshctxt.timeDependent():
                return meshctxt.getObject().getCurrentTime()
        try:
            return float(utils.OOFeval(txt))
        except:
            pass
    def getEndTimeText(self):
        return self.endtimeEntry.get_text().rstrip()

    def timeChangeCB(self, entry): # gtk callback
        self.sensitize()

    def solveCB(self, button):
        meshctxt = self.currentMeshContext()
        endtime = self.endTime(meshctxt)
        meshmenu.Solve(mesh=self.currentFullMeshName(),
                       endtime=endtime)

    def meshSolvedCB(self, mesh):     # sb "mesh solved"
        debug.mainthreadTest()
        if mesh is self.currentMeshContext():
            self.updateEndTime()
            self.sensitize()

    def meshTimeChangedCB(self, mesh): # sb "time changed"
        debug.mainthreadTest()
        if mesh is self.currentMeshContext():
            self.currentTimeEntry.set_text(`mesh.getObject().latestTime()`)

    def statusChangedCB(self, mesh): # sb "mesh status changed"
        if mesh is self.currentMeshContext():
            self.update()

    def statusCB(self, button): # status details button callback
        meshctxt = self.currentMeshContext()
        details = meshctxt.status.getDetails()
        if details:
            reporter.report("\n*** Mesh Status for %s ***\n%s: %s" %
                            (meshctxt.path(), meshctxt.status.tag, details))
        else:
            reporter.report("\n*** Mesh Status for %s ***\n%s" %
                          (meshctxt.path(), meshctxt.status.tag))
        # TODO 3.1: Give more details here about why the Solve button
        # isn't sensitive, if it isn't sensitive.  sensitize() and
        # statusCB() should use the same code somehow.
        reporter_GUI.raiseMessageWindows()

    def getStatus(self):
        # TODO 3.1: Finish this and use it in sensitize() and statusCB().
        # It should return meshok, timesok, solversok and msgs.
        meshctxt = self.currentMeshContext()
        msgs = []
        if not meshctxt:
            msgs.append("There is no mesh.")
            return msgs
        if meshctxt.query_reservation():
            msgs.append("Mesh is busy.")
        if meshctxt.outOfSync():
            msgs.append("Mesh needs to be rebuilt.")

################

SolverPage()

