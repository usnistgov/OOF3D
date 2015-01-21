# -*- python -*-
# $RCSfile: fieldPage.py,v $
# $Revision: 1.60.2.8 $
# $Author: fyc $
# $Date: 2014/07/28 22:18:24 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.engine import equation
from ooflib.common import debug
from ooflib.common import labeltree
from ooflib.common import microstructure
from ooflib.common import utils
from ooflib.common.IO import parameter
from ooflib.common.IO import whoville
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import oofGUI
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import tooltips
from ooflib.common.IO.GUI import whowidget
from ooflib.engine import fieldinit
from ooflib.engine import skeletoncontext
from ooflib.engine.IO import subproblemmenu
import ooflib.SWIG.engine.field
import ooflib.engine.IO.meshmenu
import ooflib.engine.mesh

import gobject
import gtk
import string

allCompoundFields = ooflib.SWIG.engine.field.allCompoundFields

subpmenu = subproblemmenu.subproblemMenu
meshmenu = ooflib.engine.IO.meshmenu.meshmenu

class ButtonSignal:
    def __init__(self, button, signal):
        self.button = button
        self.signal = signal
    def set(self, active):
        debug.mainthreadTest()
        self.signal.block()
        self.button.set_active(active)
        self.signal.unblock()
    def set_sensitive(self, sensitivity):
        debug.mainthreadTest()
        self.button.set_sensitive(sensitivity)


class FieldPage(oofGUI.MainPage):
    def __init__(self):
        oofGUI.MainPage.__init__(self, name="Fields & Equations", ordering=210,
                                 tip="Define fields on a finite element mesh.")
        mainbox = gtk.VBox(spacing=2)
        self.gtk.add(mainbox)

        align = gtk.Alignment(xalign=0.5)
        mainbox.pack_start(align, expand=0, fill=0)
        centerbox = gtk.HBox(spacing=3)
        align.add(centerbox)
        self.subpwidget = whowidget.WhoWidget(
            ooflib.engine.subproblemcontext.subproblems, scope=self)
        switchboard.requestCallbackMain(self.subpwidget, self.subpwidgetCB)
        label = gtk.Label("Microstructure=")
        label.set_alignment(1.0, 0.5)
        centerbox.pack_start(label, expand=0, fill=0)
        centerbox.pack_start(self.subpwidget.gtk[0], expand=0, fill=0)
        label = gtk.Label("Skeleton=")
        label.set_alignment(1.0, 0.5)
        centerbox.pack_start(label, expand=0, fill=0)
        centerbox.pack_start(self.subpwidget.gtk[1], expand=0, fill=0)
        label = gtk.Label("Mesh=")
        label.set_alignment(1.0, 0.5)
        centerbox.pack_start(label, expand=0, fill=0)
        centerbox.pack_start(self.subpwidget.gtk[2], expand=0, fill=0)
        label = gtk.Label("SubProblem=")
        label.set_alignment(1.0, 0.5)
        centerbox.pack_start(label, expand=0, fill=0)
        centerbox.pack_start(self.subpwidget.gtk[3], expand=0, fill=0)

        hpane = gtk.HPaned()
        gtklogger.setWidgetName(hpane, 'HPane')
        mainbox.pack_start(hpane, expand=1, fill=1)
        gtklogger.connect_passive(hpane, 'notify::position')

        ## Field Pane
        fieldframe = gtk.Frame("Fields")
        fieldframe.set_shadow_type(gtk.SHADOW_IN)
        hpane.pack1(fieldframe, resize=1, shrink=0)
        vbox = gtk.VBox(spacing=2)
        fieldframe.add(vbox)
        scroll = gtk.ScrolledWindow()
        gtklogger.logScrollBars(scroll, "Fields")
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        vbox.pack_start(scroll, expand=1, fill=1)
        bbox = gtk.VBox() # extra layer keeps table from expanding inside scroll
        scroll.add_with_viewport(bbox)
        self.fieldtable = gtk.Table()
        self.fieldtable.set_border_width(3)
        bbox.pack_start(self.fieldtable, expand=0, fill=0)
        self.build_fieldTable()
        align = gtk.Alignment(xalign=0.5)
        vbox.pack_start(align, expand=0, fill=0)
        self.copyfieldbutton = gtk.Button("Copy Field State...")
        gtklogger.setWidgetName(self.copyfieldbutton, 'CopyField')
        gtklogger.connect(self.copyfieldbutton, 'clicked', self.copyfstateCB)
        tooltips.set_tooltip_text(self.copyfieldbutton,
            "Copy all field status variables from the current subproblem to another subproblem.")
        align.add(self.copyfieldbutton)

        ## Equation Pane
        eqnframe = gtk.Frame("Equations")
        eqnframe.set_shadow_type(gtk.SHADOW_IN)
        hpane.pack2(eqnframe, resize=1, shrink=0)
        vbox = gtk.VBox(spacing=2)
        eqnframe.add(vbox)
        scroll = gtk.ScrolledWindow()
        gtklogger.logScrollBars(scroll, "Equations")
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        vbox.pack_start(scroll, expand=1, fill=1)
        bbox = gtk.VBox() # extra layer keeps table from expanding inside scroll
        scroll.add_with_viewport(bbox)
        self.eqntable = gtk.Table()
        self.eqntable.set_border_width(3)
        bbox.pack_start(self.eqntable, expand=0, fill=0)
        self.eqnbuttons = {}
        self.build_eqnTable()
        align = gtk.Alignment(xalign=0.5)
        vbox.pack_start(align, expand=0, fill=0)
        self.copyeqnbutton = gtk.Button("Copy Equation State...")
        gtklogger.setWidgetName(self.copyeqnbutton, "CopyEquation")
        gtklogger.connect(self.copyeqnbutton, "clicked", self.copyeqstateCB)
        align.add(self.copyeqnbutton)
        tooltips.set_tooltip_text(self.copyeqnbutton,
            "Copy the status of all equations from the current mesh to another mesh.")

        switchboard.requestCallbackMain(("new who", "Microstructure"),
                                         self.newMSorSkeletonOrMesh)
        switchboard.requestCallbackMain(("new who", "Skeleton"),
                                        self.newMSorSkeletonOrMesh)
        switchboard.requestCallbackMain(("new who", "Mesh"),
                                        self.newMSorSkeletonOrMesh)
        switchboard.requestCallbackMain("made reservation",
                                        self.reservationChanged)
        switchboard.requestCallbackMain("cancelled reservation",
                                        self.reservationChanged)
        switchboard.requestCallbackMain("new field", self.newFieldCB)
        switchboard.requestCallbackMain("field defined", self.defineFldCB)
        switchboard.requestCallbackMain("field activated", self.activateFldCB)
        if config.dimension() == 2:
            switchboard.requestCallbackMain("field inplane", self.inplaneFldCB)
        switchboard.requestCallbackMain("new equation",self.newEquationCB)
        switchboard.requestCallbackMain("equation activated",
                                        self.activateEqnCB)
        switchboard.requestCallbackMain("mesh status changed",
                                        self.meshStatusCB)
#         switchboard.requestCallbackMain("field initialized", self.initFldCB)

    def installed(self):
        self.update()
        self.sensitize()

    def build_fieldTable(self):
        debug.mainthreadTest()
        self.fieldtable.foreach(gtk.Object.destroy) # clear the table
        self.fieldbuttons = {}
        self.fieldtable.resize(len(allCompoundFields), 6)
        self.fieldtable.attach(gtk.VSeparator(), 1,2, 0,len(allCompoundFields),
                               xoptions=0, yoptions=gtk.EXPAND|gtk.FILL)
        self.fieldtable.set_col_spacing(0, 3)
        row = 0
        for fname, fld in allCompoundFields.items():
            label = gtk.Label(fname)
            label.set_alignment(1.0, 0.5)
            self.fieldtable.attach(label, 0,1, row,row+1,
                                   xoptions=gtk.FILL, yoptions=0)
            button = gtk.CheckButton('defined')
            gtklogger.setWidgetName(button, fname+" defined")
            signal = gtklogger.connect(button, 'clicked',
                                       self.fieldDefineCB, fld)
            self.fieldbuttons[(fname, "defined")] = ButtonSignal(button, signal)
            self.fieldtable.attach(button, 2,3, row, row+1,
                                   xoptions=0, yoptions=0)
            self.setFieldDefineTip(button, fld)

            button = gtk.CheckButton('active')
            gtklogger.setWidgetName(button, fname+" active")
            signal = gtklogger.connect(button, 'clicked',
                                       self.fieldActiveCB, fld)
            self.fieldbuttons[(fname, "active")] = ButtonSignal(button, signal)
            self.fieldtable.attach(button, 3,4, row, row+1,
                                   xoptions=0, yoptions=0)
            self.setFieldActiveTip(button, fld)

            if config.dimension() == 2:
                button = gtk.CheckButton('in-plane')
                gtklogger.setWidgetName(button, fname + " in-plane")
                signal = gtklogger.connect(button, 'clicked',
                                           self.fieldInPlaneCB, fld)
                self.fieldbuttons[(fname, "inplane")] = ButtonSignal(button,
                                                                     signal)
                self.fieldtable.attach(button, 4,5, row, row+1,
                                       xoptions=0, yoptions=0)
                self.setFieldInPlaneTip(button, fld)

            row += 1

    def newFieldCB(self):               # switchboard "new field"
        self.build_fieldTable()
        self.show()

    def fieldDefineCB(self, button, field): # gtk callback
        if button.get_active():
            subpmenu.Field.Define(subproblem=self.currentFullSubProblemName(),
                                  field=field)
        else:
            subpmenu.Field.Undefine(subproblem=self.currentFullSubProblemName(),
                                    field=field)
        self.setFieldDefineTip(button, field)

    def setFieldDefineTip(self, button, field):
        if button.get_active():
            verb = "Undefine"
        else:
            verb = "Define"
        tooltips.set_tooltip_text(button,
            "%s the %s field on the mesh.  Only defined fields have values."
            % (verb, field.name()))

    def fieldActiveCB(self, button, field): # gtk callback
        if button.get_active():
            subpmenu.Field.Activate(
                subproblem=self.currentFullSubProblemName(), field=field)
        else:
            subpmenu.Field.Deactivate(
                subproblem=self.currentFullSubProblemName(), field=field)
        self.setFieldActiveTip(button, field)
        
    def setFieldActiveTip(self, button, field):
        if button.get_active():
            verb = "Deactivate"
        else:
            verb = "Activate"
        tooltips.set_tooltip_text(button,
            "%s the %s field on the subproblem. The solver finds the values of the active fields by solving the active equations."
            % (verb, field.name()))

    if config.dimension() == 2:
        def fieldInPlaneCB(self, button, field): # gtk callback
            debug.mainthreadTest()
            if button.get_active():
                meshmenu.Field.In_Plane(
                    mesh=self.currentFullMeshName(),
                    field = field)
            else:
                meshmenu.Field.Out_of_Plane(
                    mesh=self.currentFullMeshName(),
                    field = field)
            self.setFieldInPlaneTip(button, field)

        def setFieldInPlaneTip(self, button, field):
            debug.mainthreadTest()
            if button.get_active():
                verb = "Do not constrain"
            else:
                verb = "Constrain"
            tooltips.set_tooltip_text(button,
                "%s the derivatives of the %s field to lie in the x-y plane."
                % (verb, field.name()))

    def defineFldCB(self, subpname, fieldname, defined): # sb "field defined"
        if subpname == self.currentFullSubProblemName():
            # TODO 3.1: PLASTICITY For testing purposes, we sometimes
            # define fields for which there are no widgets -- these
            # cause a key error here.  Ignore it.
            try:
                self.fieldbuttons[(fieldname, "defined")].set(defined)
            except KeyError:
                pass
            self.update()

    def activateFldCB(self, subpname, fieldname, active): # sb "field activated"
        if subpname == self.currentFullSubProblemName():
            self.fieldbuttons[(fieldname, "active")].set(active)

    if config.dimension() == 2:
        def inplaneFldCB(self, meshname, fieldname, inplane): # sb "field inplane"
            if meshname == self.currentFullMeshName():
                self.fieldbuttons[(fieldname, "inplane")].set(inplane)

    def activateEqnCB(self, subpname, eqname, active): # "equation activated"
        if subpname == self.currentFullSubProblemName():
            self.eqnbuttons[(eqname, "active")].set(active)
            

    ########################


    def build_eqnTable(self):
        debug.mainthreadTest()
        self.eqntable.foreach(gtk.Object.destroy) # clear the table
        self.eqnbuttons = {}
        eqlist = equation.allEquations
        self.eqntable.resize(len(eqlist), 3)
        row=0
        for eqn in eqlist:
            label = gtk.Label(utils.underscore2space(eqn.name()))
            label.set_alignment(1.0, 0.5)
            self.eqntable.attach(label, 0,1, row, row+1,
                                 xoptions=gtk.FILL, yoptions=0)
            button = gtk.CheckButton('active')
            gtklogger.setWidgetName(button, eqn.name() + " active")
            signal = gtklogger.connect(button, 'clicked', self.eqnButtonCB, eqn)
            self.eqnbuttons[(eqn.name(), "active")] = ButtonSignal(button,
                                                                   signal)
            tooltips.set_tooltip_text(button,'Active equations will be solved.')
            self.eqntable.attach(button, 2,3, row,row+1, xoptions=0,
                                 yoptions=0)
            row += 1
        self.eqntable.attach(gtk.VSeparator(), 1,2, 0,len(eqlist),
                             xoptions=0, yoptions=gtk.EXPAND|gtk.FILL)
        self.eqntable.set_col_spacing(0, 3)

    def newEquationCB(self):  # Switchboard, "new equation".
        self.build_eqnTable()
        self.show()

    def activateEqnCB(self, subproblem, eqn, active): # sb "equation activated"
         if subproblem == self.currentFullSubProblemName():
             self.eqnbuttons[(eqn, "active")].set(active)

    def eqnButtonCB(self, button, eqn): # gtk callback
        if button.get_active():
            subpmenu.Equation.Activate(
                subproblem=self.currentFullSubProblemName(), equation=eqn)
        else:
            subpmenu.Equation.Deactivate(
                subproblem=self.currentFullSubProblemName(), equation=eqn)


    ########################

    def currentFullMeshName(self):
        return self.subpwidget.get_value(depth=3)
    def currentMeshContext(self):
        try:
            return ooflib.engine.mesh.meshes[self.currentFullMeshName()]
        except KeyError:
            return None
    def currentMesh(self):
        meshctxt = self.currentMeshContext()
        if meshctxt:
            return meshctxt.getObject()
            
    def currentFullSubProblemName(self):
        return self.subpwidget.get_value()
    def currentSubProblemContext(self):
        try:
            return ooflib.engine.subproblemcontext.subproblems[
                self.currentFullSubProblemName()]
        except KeyError:
            return None
    def currentSubProblem(self):
        subpc = self.currentSubProblemContext()
        if subpc:
            return subpc.getObject()
	

    def sensitize(self):
        debug.mainthreadTest()
        meshctxt = self.currentMeshContext()
        subpctxt = self.currentSubProblemContext()
        subpok = subpctxt is not None and not subpctxt.query_reservation()
        meshok = meshctxt and not meshctxt.outOfSync()
        self.fieldtable.set_sensitive(subpok and meshok)
        self.eqntable.set_sensitive(subpok and meshok)
        self.copyfieldbutton.set_sensitive(subpok and meshok)
        self.copyeqnbutton.set_sensitive(subpok and meshok)
        gtklogger.checkpoint("Field page sensitized")
        
    def update(self):
        self.set_state(self.currentFullSubProblemName())

    def set_state(self, subppath):
        debug.mainthreadTest()
        path = labeltree.makePath(subppath)
        self.subpwidget.set_value(path)
        # Retrieve the subproblem from the widget, just in case
        # subppath wasn't a complete subproblem path.
        subpctxt = self.currentSubProblemContext()
        if subpctxt:           # ie, path was complete
            subp = subpctxt.getObject() # CSubProblem object
            mesh = self.currentMesh()
            for fname,fld in allCompoundFields.items():
                fdef = subp.is_defined_field(fld)
                self.fieldbuttons[(fname, "defined")].set(fdef)
                self.fieldbuttons[(fname, "active")].set_sensitive(fdef)
                if config.dimension() == 2:
                    self.fieldbuttons[(fname, "inplane")].set_sensitive(fdef)
                if fdef:
                    self.fieldbuttons[(fname, "active")].set(
                        subp.is_active_field(fld))
                    if config.dimension() == 2:
                        self.fieldbuttons[(fname, "inplane")].set(
                            mesh.in_plane(fld))
                else:                   # field not defined
                    self.fieldbuttons[(fname, "active")].set(0)
                    if config.dimension() == 2:
                        self.fieldbuttons[(fname, "inplane")].set(0)
            for eqn in equation.allEquations:
                active = subp.is_active_equation(eqn)
                self.eqnbuttons[(eqn.name(),"active")].set(active)
        else:                           # no current subproblem
            for button in self.fieldbuttons.values():
                button.set(0)
            for button in self.eqnbuttons.values():
                button.set(0)
        self.sensitize()

    def copyfstateCB(self, gtkobj):     # Button callback.
        menuitem = subpmenu.Copy_Field_State
        targetparam = menuitem.get_arg("target")
        
        targetparam.set(self.currentFullSubProblemName())
        if parameterwidgets.getParameters(targetparam,
                                          title="Select a target Subproblem"):
            menuitem.callWithDefaults(source=self.currentFullSubProblemName())

    def copyeqstateCB(self, gtkobj): # Button callback
        menuitem = subpmenu.Copy_Equation_State
        targetparam = menuitem.get_arg("target")
        targetparam.set(self.currentFullSubProblemName())
        if parameterwidgets.getParameters(targetparam,
                                          title="Select a target subproblem"):
            menuitem.callWithDefaults(source=self.currentFullSubProblemName())

    # switchboard ("new who", "Skeleton") or ("new who", "Mesh")
    def newMSorSkeletonOrMesh(self, skeletonname):
        if not self.currentSubProblemContext():
            self.subpwidget.set_value(skeletonname)

    def subpwidgetCB(self, interactive):      # switchboard callback
        self.update()

    def reservationChanged(self, whoobj):
        # switchboard "made reservation", "cancelled reservation"
        if self.currentFullSubProblemName() == whoobj.path():
            self.sensitize()

    def meshStatusCB(self, meshctxt):
        if meshctxt is self.currentMeshContext():
            self.sensitize()

#############

fp = FieldPage()
