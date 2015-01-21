# -*- python -*-
# $RCSfile: newmeshWidget.py,v $
# $Revision: 1.12.10.4 $
# $Author: langer $
# $Date: 2014/05/08 14:39:05 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import switchboard
from ooflib.SWIG.engine import elementshape
from ooflib.SWIG.engine import masterelement
from ooflib.common import debug
from ooflib.common.IO.GUI import chooser
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import tooltips
from ooflib.engine.IO import meshmenu
import gtk
import string

# Widget for the MasterElementTypesParameter, whose value is a list of
# MasterElement enumerators, one for each MasterElement topology.  The
# widget has a ChooserWidget for each element topology, and two extra
# Choosers for specifying the mapping order and interpolation order of
# the elements.  The Choosers for the elements only list those
# elements that have the desired orders.  This ensures that the user
# doesn't try to use linear triangles with quadratic quadrilaterals,
# for example.

class MasterElementTypesWidget(parameterwidgets.ParameterWidget):
    def __init__(self, param, scope=None, name=None, verbose=False):
        frame = gtk.Frame()
        self.table = None
        parameterwidgets.ParameterWidget.__init__(self, frame, scope, name=name,
                                                  verbose=verbose)
        self.nclasses = 0    # number of enum classes (ie element topologies)
        self.classwidgets = []          # widgets for each enum class
        self.build(interactive=0)       # construct everything
        if param.value:
            self.set_value(param.value)
        self.sbcallback = switchboard.requestCallbackMain("new master element",
                                                          self.newElementCB)
    def cleanUp(self):
        debug.mainthreadTest()
        switchboard.removeCallback(self.sbcallback)
        parameterwidgets.ParameterWidget.cleanUp(self)
        del self.classwidgets
        del self.tablelabels
    def newElementCB(self):             # switchboard "new master element"
        self.build(interactive=0)
    def build(self, interactive):
        debug.mainthreadTest()
        # elclasses = masterelement.getMasterElementEnumClasses()
        nclasses = len(elementshape.enumClasses)
        # elgeometries = masterelement.getMasterElementGeometries()

        # Build the widgets
        if self.table is None or nclasses != self.nclasses:
            self.nclasses = nclasses
            if self.table:
                self.table.destroy()
            self.tablelabels = []
            self.table = gtk.Table(rows=2+nclasses, columns=2)
            self.gtk.add(self.table)

            # Choosers for mapping and interpolation order
            self.mapchooser = chooser.ChooserWidget([], callback=self.orderCB,
                                                    name="Map")
            self.funchooser = chooser.ChooserWidget([], callback=self.orderCB,
                                                    name="Func")
            label = gtk.Label('mapping order')
            tooltips.set_tooltip_text(label,'Polynomial order of the functions used to map master elements to physical space.')
            label.set_alignment(1.0, 0.5)
            self.tablelabels.append(label)
            self.table.attach(label, 0, 1, 0, 1, xpadding=5, xoptions=gtk.FILL)
            self.table.attach(self.mapchooser.gtk, 1, 2, 0, 1,
                              xpadding=5, xoptions=gtk.EXPAND|gtk.FILL)
            label = gtk.Label('interpolation order:')
            tooltips.set_tooltip_text(label,'Polynomial order of the functions used to interpolate within elements.')
            label.set_alignment(1.0, 0.5)
            self.tablelabels.append(label)
            self.table.attach(label, 0, 1, 1, 2, xpadding=5,
                              xoptions=gtk.FILL)
            self.table.attach(self.funchooser.gtk, 1, 2, 1, 2,
                              xpadding=5, xoptions=gtk.EXPAND|gtk.FILL)

            # Choosers for each element geometry
            row = 2
            self.classwidgets = []
            for geometry, elclass in elementshape.enumClasses.items():
                label = gtk.Label(geometry+' element:')
                tooltips.set_tooltip_text(
                    label,
                    'Type of finite element to use for %s elements' % geometry)
                label.set_alignment(1.0, 0.5)
                self.tablelabels.append(label)
                self.table.attach(label, 0,1, row,row+1, xoptions=gtk.FILL)
                ewidget = chooser.ChooserWidget([], name="%s element"%geometry)
                self.classwidgets.append((elclass, ewidget))
                self.table.attach(ewidget.gtk, 1,2, row,row+1,
                                  xpadding=5, xoptions=gtk.EXPAND|gtk.FILL)
                row += 1

        # Set the allowed values for each chooser.
        # Find out which mapping and interpolation orders have to be listed.
        maporderset = set()
        funorderset = set()
        for elclass in elementshape.enumClasses.values():
            for elname in elclass.names:
                el = masterelement.getMasterElementFromEnum(elclass(elname))
                maporderset.add(el.map_order())
                funorderset.add(el.fun_order())
        maporders = list(maporderset)
        maporders.sort()
        funorders = list(funorderset)
        funorders.sort()
        # List the orders in the widgets
        self.mapchooser.update([`order` for order in maporders])
        self.funchooser.update([`order` for order in funorders])
        try:
            current_map = int(self.mapchooser.get_value())
            current_fun = int(self.funchooser.get_value())
        except:
            # If the choosers don't have values, it's because there
            # aren't any elements defined. 
            self.widgetChanged(validity=0, interactive=interactive)
        else:
            # Find and list the element types for the current shape
            ok = True
            for elclass, ewidget in self.classwidgets:
                elements = masterelement.getMasterElementsFromEnumClass(elclass)
                okels = [el for el in elements
                         if el.map_order() == current_map
                         and el.fun_order() == current_fun]
                ok = ok and len(okels) > 0
                ewidget.update([el.name() for el in okels],
                               elclass.helpdict)
            self.widgetChanged(validity=ok, interactive=interactive)

    def orderCB(self, *args, **kwargs):
        # Mapping or interpolation order has been changed by the user.
        self.build(interactive=1)

    def set_value(self, value):
        # value is a list of enums.  Pick the first one, and get the
        # MasterElement that it corresponds to, and set the mapchooser
        # and funchooser accordingly.  This assumes that all enums in
        # value correspond to elements with the same orders.
        el = masterelement.getMasterElementFromEnum(value[0])
        self.mapchooser.set_state(`el.map_order()`)
        self.funchooser.set_state(`el.fun_order()`)
        self.build(interactive=0)
        for val, (elclass, ewidget) in zip(value, self.classwidgets):
            ewidget.set_state(val.name)
        self.widgetChanged(validity=1, interactive=0)

    def show(self):
        debug.mainthreadTest()
        self.gtk.show()
        self.table.show()
        self.mapchooser.show()
        self.funchooser.show()
        for labelbox in self.tablelabels:
            labelbox.show_all()
        for elclass, ewidget in self.classwidgets:
            ewidget.show()

    def get_value(self):
        return [eclass(ewidget.get_value())
                for eclass, ewidget in self.classwidgets]

def _MasterElementTypesParameter_makeWidget(self, scope=None, verbose=False):
    return MasterElementTypesWidget(self, scope, name=self.name,
                                    verbose=verbose)

meshmenu.MasterElementTypesParameter.makeWidget = \
                                   _MasterElementTypesParameter_makeWidget

