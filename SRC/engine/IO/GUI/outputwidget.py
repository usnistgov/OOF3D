# -*- python -*-
# $RCSfile: outputwidget.py,v $
# $Revision: 1.2.4.6 $
# $Author: langer $
# $Date: 2014/05/14 18:48:28 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import utils
from ooflib.engine.IO import output
from ooflib.common.IO.GUI import gfxLabelTree
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import widgetscope
import gtk
import sys

class OutputParameterWidget(parameterwidgets.ParameterWidget,
                            widgetscope.WidgetScope):
    def __init__(self, value, outputtree, scope=None, name=None, verbose=False):
        debug.mainthreadTest()
        frame = gtk.Frame()
        self.vbox = gtk.VBox()
        frame.add(self.vbox)
        # top part is a bunch of chooser widgets representing the
        # LabelTree of outputs.
        self.treewidget = \
                     gfxLabelTree.LabelTreeChooserWidget(outputtree,
                                                         callback=self.treeCB,
                                                         name=name)
        self.vbox.pack_start(self.treewidget.gtk, expand=0, fill=0)
        # bottom part is a ParameterTable
        self.parambox = gtk.VBox()
        gtklogger.setWidgetName(self.parambox, "Parameters")
        self.paramtable = None
        self.params = []
        self.vbox.pack_start(self.parambox, expand=0, fill=0)
        
        parameterwidgets.ParameterWidget.__init__(self, frame, scope, name, 
                                                  verbose)
        widgetscope.WidgetScope.__init__(self, scope)
        if value is not None:
            self.set_value(value)
        else:
            self.set_value(outputtree.numberOneChild())

    def show(self):
        debug.mainthreadTest()
        self.gtk.show()                 # self.gtk is the GtkFrame
        self.vbox.show()
        self.treewidget.show()
        self.parambox.show()
        if self.paramtable:
            self.paramtable.show()
    def set_value(self, value):
        if value is not None:
            self.treewidget.set_value(value.getPrototype())
            self.makeParameterTable(value, interactive=0)
    def makeParameterTable(self, value, interactive):
        # 'value' is an Output prototype.  The parameter table is
        # rebuilt every time the Output changes.
        debug.mainthreadTest()
        self.destroyParameterTable()

        # 'value' is an Output of the requested type, but it may have
        # incorrect parameter values.  Cloning the output creates
        # clones of the parameters, each with auxData "Output" set to
        # its pipeline component.  The Parameters' widgets can use
        # this data if necessary (see invariantwidget.py).
        self.output = value.clone()

        # get the hierarchical list of the settable parameters
        paramhier = self.output.listAllParametersHierarchically(onlySettable=1)
        
        self.params = utils.flatten_all(paramhier)

        if self.params:
            for param in self.params:
                if param.value is None:
                    param.value = param.default
            self.paramtable = parameterwidgets.HierParameterTable(
                paramhier, scope=self)
            self.parambox.pack_start(self.paramtable.gtk, expand=0, fill=0)
            self.widgetChanged(self.paramtable.isValid(), interactive)
            self.paramtable.show()
            self.sbcallback = switchboard.requestCallbackMain(
                self.paramtable, self.tableChangedCB)
        else:
            self.paramtable = None
            self.widgetChanged(1, interactive)
    def get_value(self):
        if self.paramtable is not None:
            self.paramtable.get_values() # copies widget values to params
        return self.output
    def destroyParameterTable(self):
        debug.mainthreadTest()
        if self.paramtable is not None:
            table = self.paramtable
            self.paramtable = None
            table.destroy()
            switchboard.removeCallback(self.sbcallback)
    def treeCB(self):
        self.makeParameterTable(self.treewidget.get_value(), interactive=1)
    def tableChangedCB(self, *args):      # switchboard callback
        self.widgetChanged(self.paramtable.isValid(), interactive=1)


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class ValueOutputParameterWidget(OutputParameterWidget):
    def __init__(self, value, scope=None, name=None, verbose=False):
        OutputParameterWidget.__init__(self, value, output.valueOutputs,
                                       scope=scope, name=name, verbose=verbose)

def _ValueOutputParameter_makeWidget(self, scope=None, verbose=False):
    return ValueOutputParameterWidget(self.value, scope=scope, name=self.name,
                                      verbose=verbose)

output.ValueOutputParameter.makeWidget = _ValueOutputParameter_makeWidget

#=--=##=--=##=--=#
        
class ScalarOutputParameterWidget(OutputParameterWidget):
    def __init__(self, value, scope=None, name=None, verbose=False):
        OutputParameterWidget.__init__(self, value, output.scalarOutputs,
                                       scope=scope, name=name, verbose=verbose)

def _ScalarOutputParameter_makeWidget(self, scope=None, verbose=False):
    return ScalarOutputParameterWidget(self.value, scope=scope, name=self.name,
                                       verbose=verbose)

output.ScalarOutputParameter.makeWidget = _ScalarOutputParameter_makeWidget

