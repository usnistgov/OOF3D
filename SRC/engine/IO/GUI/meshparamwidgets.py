# -*- python -*-
# $RCSfile: meshparamwidgets.py,v $
# $Revision: 1.79.4.12 $
# $Author: langer $
# $Date: 2014/07/16 21:07:18 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

# ParameterWidgets for things that depend on a Mesh, such as Fields,
# Fluxes, and Equations defined on the Mesh.

from ooflib.SWIG.common import config
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.engine import equation
from ooflib.SWIG.engine import field
from ooflib.SWIG.engine import flux
from ooflib.SWIG.engine import planarity
from ooflib.common import debug
from ooflib.common.IO.GUI import chooser
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import whowidget
from ooflib.engine import mesh
from ooflib.engine import skeletoncontext
from ooflib.engine import subproblemcontext
from ooflib.engine.IO import meshparameters
import gtk
import string
#Interface branch
from ooflib.common.IO import placeholder

class MeshParamWidgetBase(parameterwidgets.ParameterWidget):
    # Base class for a widget that displays and allows choices from a
    # list of things from a Mesh (eg, defined Fields or active
    # Equations).  The meshfunc constructor argument is a function
    # that returns the list of things to display.  It's called with
    # the mesh as its first argument, so it can be a Mesh member
    # function.  self.chooser is the ChooserWidget that displays the
    # items returned by meshfunc.

    def __init__(self, param, whoclass, meshfunc, scope, name=None,
                 separator_func=None, verbose=False):
        self.meshfunc = meshfunc
        self.whoclass = whoclass
        self.chooser = chooser.ChooserWidget([], callback=self.chooserCB,
                                             name=name,
                                             separator_func=separator_func,)
        parameterwidgets.ParameterWidget.__init__(self, self.chooser.gtk, scope,
                                                  verbose=verbose)
        self.meshwidget = scope.findWidget(
            lambda w: isinstance(w, whowidget.WhoWidget)
            and w.whoclass is whoclass)
        assert self.meshwidget is not None
        if self.meshwidget is None:
            raise ooferror.ErrPyProgrammingError("Can't find WhoWidget for %s"
                                                 % `whoclass`)
        self.sbcallbacks = [
            switchboard.requestCallbackMain(self.meshwidget, self.update),
            switchboard.requestCallbackMain("mesh changed", self.meshChangeCB),
            switchboard.requestCallbackMain("subproblem changed",
                                            self.meshChangeCB)
            ]

        self.update(interactive=0)
        self.set_value(param.value)
        
    def update(self, interactive):
        msh = self.getSource()
        self.vals = {None:None}
        if msh is not None:
            namelist = []
            for obj in self.meshfunc(msh):
                self.vals[obj.name()] = obj
                namelist.append(obj.name())
            self.chooser.update(namelist)
            self.widgetChanged(len(namelist) > 0, interactive)
        else:
            self.chooser.update([])
            self.widgetChanged(0, interactive)
    
    #def dumpCycle(self, subp):
        #msh = self.getSource()
        #self.vals = {None:None}
        #if msh is not None:
            #namelist = []
            #for obj in self.meshfunc(msh):
	        #if obj.path() != subp.path():
		    ##The current subproblem cannot depend on a possible subproblem subproblem that depend on it already: Loop deep 1
		    #if subp.path() not in obj.subptype.get_dependencies():
		       ##The current subproblem dependents cannot be in a possible selectable subproblem dependenties: Loop deep 2
		       #intersection = False
		       #for sub in obj.subptype.get_dependencies():
			   #if sub in subp.subptype.get_dependents():
			      #intersection = True
		       #if not intersection:
			  ##self.subps.append(subproblem)
                          #self.vals[obj.name()] = obj
                          #namelist.append(obj.name())
            #self.chooser.update(namelist, to_update=False)
            #self.widgetChanged(len(namelist) > 0, False)
        #else:
            #self.chooser.update([], to_update=False)
            #self.widgetChanged(0, False)
            
    def chooserCB(self, *args):
        self.widgetChanged(1, interactive=1)
    def meshChangeCB(self, meshcontext):
        if self.meshwidget:             # we haven't been cleaned up
            src = self.getSource()
            # 'meshcontext' might be a subproblem, actually.
            if meshcontext is src or meshcontext.getParent() is src:
                self.update(interactive=0)
    def getSource(self):
        if self.meshwidget is not None:
            meshname = self.meshwidget.get_value()
            try:
                return self.whoclass[meshname]
            except KeyError:
                pass
    def get_value(self):
        return self.vals[self.chooser.get_value()]
    def set_value(self, obj):
        if obj is not None and obj.name() in self.chooser.choices():
            self.chooser.set_state(obj.name())
            self.widgetChanged(1, interactive=0)
        
    def cleanUp(self):
        debug.mainthreadTest()
        self.meshwidget = None
        map(switchboard.removeCallback, self.sbcallbacks)
        parameterwidgets.ParameterWidget.cleanUp(self)

class MeshParamWidget(MeshParamWidgetBase):
    def __init__(self, param, meshfunc, scope, name=None, separator_func=None,
                 verbose=False):
        MeshParamWidgetBase.__init__(self, param,
                                     mesh.meshes,
                                     meshfunc, scope, name, separator_func,
                                     verbose=verbose)

class SubProblemParamWidget(MeshParamWidgetBase):
    def __init__(self, param, meshfunc, scope, name=None, separator_func=None,
                 verbose=False):
        MeshParamWidgetBase.__init__(self, param,
                                     subproblemcontext.subproblems,
                                     meshfunc, scope, name, separator_func,
                                     verbose=verbose)
    

# Widgets for quantities to which Invariants can be calculated should
# be subclasses of InvariandWidget.

class InvariandWidget: pass

# Widgets for quantities for which components can be extracted should
# be subclasses of IndexableWidget.

class IndexableWidget: pass

#############################

def meshfieldlister(meshctxt):          # meshfunc for FieldParameterWidgets
    # list fields and out-of-plane fields, if defined.
    try:
        compoundfields = meshctxt.all_compound_subproblem_fields()
        flds = []
        for fld in compoundfields:
            flds.append(fld)
            if config.dimension() == 2:
                if not meshctxt.getObject().in_plane(fld): 
                    flds.append(fld.out_of_plane())
        return flds
    except:
        # This might be called with an unresolvable proxy if there
        # are no meshes.
        return []


class FieldParameterWidget(MeshParamWidget, InvariandWidget, IndexableWidget):
    def __init__(self, param, scope, name=None, verbose=False):
        if param.outofplane:
            flist = meshfieldlister
        else:
            flist = mesh.Mesh.all_compound_subproblem_fields
        MeshParamWidget.__init__(self, param, flist, scope, name, verbose)
##        self.sbcallbacks.append(
##            switchboard.requestCallbackMain("field defined", self.fieldDefCB))
    def fieldDefCB(self, *args):
        self.update(interactive=False)

def _makeFieldWidget(param, scope, verbose=False):
    return FieldParameterWidget(param, scope, name=param.name, verbose=verbose)

meshparameters.FieldParameter.makeWidget = _makeFieldWidget

def subpfieldlister(subp):     # meshfunc for SubProblemFieldParameterWidgets
    # list fields and out-of-plane fields, if defined.
    try:
        compoundfields = subp.all_compound_fields()
        flds = []
        for fld in compoundfields:
            flds.append(fld)
            if (config.dimension() == 2 and
                not subp.getParent().getObject().in_plane(fld)):
                flds.append(fld.out_of_plane())
        return flds
    except:
        # This might be called with an unresolvable proxy if there
        # are no meshes.
        return []
        
class SubProblemFieldParameterWidget(SubProblemParamWidget, InvariandWidget,
                                     IndexableWidget):
    def __init__(self, param, scope, name=None, verbose=False):
        if param.outofplane:
            flist = subpfieldlister
        else:
            flist = subproblemcontext.SubProblemContext.all_compound_fields
        SubProblemParamWidget.__init__(self, param, flist, scope, name,
                                       verbose=verbose)

def _makeSubPFieldWidget(param, scope, verbose=False):
    return FieldParameterWidget(param, scope, name=param.name, verbose=verbose)

meshparameters.SubProblemFieldParameter.makeWidget = _makeSubPFieldWidget

#############################

class FluxParameterWidget(MeshParamWidget, InvariandWidget, IndexableWidget):
    def __init__(self, param, scope, name=None, verbose=False):
        MeshParamWidget.__init__(self, param,
                                 mesh.Mesh.all_subproblem_fluxes,
                                 scope,
                                 name=name,
                                 verbose=verbose)
            
def _makeFluxWidget(param, scope, verbose=False):
    return FluxParameterWidget(param, scope, name=param.name, verbose=verbose)

meshparameters.FluxParameter.makeWidget = _makeFluxWidget

class SubProblemFluxParameterWidget(SubProblemParamWidget, InvariandWidget,
                                    IndexableWidget):
    def __init__(self, param, scope, name=None, verbose=False):
        SubProblemParamWidget.__init__(
            self, param,
            subproblemcontext.SubProblemContext.all_fluxes,
            scope,
            name=name,
            verbose=verbose)
            
def _makeSubPFluxWidget(param, scope, verbose=False):
    return SubProblemParamWidget(param, scope, name=param.name, verbose=verbose)

meshparameters.SubProblemFluxParameter.makeWidget = _makeSubPFluxWidget

#############################

class EquationParameterWidget(MeshParamWidget, IndexableWidget):
    def __init__(self, param, scope, name=None, verbose=False):
        eqfunc = mesh.Mesh.all_subproblem_equations
        MeshParamWidget.__init__(self, param, eqfunc, scope, name=name,
                                 verbose=verbose)

def _makeEquationWidget(param, scope, verbose=False):
    return EquationParameterWidget(param, scope, name=param.name, 
                                   verbose=verbose)

meshparameters.EquationParameter.makeWidget = _makeEquationWidget

class SubProblemEquationParameterWidget(SubProblemParamWidget, IndexableWidget):
    def __init__(self, param, scope, name=None, verbose=False):
        eqfunc = subproblemcontext.SubProblemContext.all_equations
        SubProblemParamWidget.__init__(self, param, eqfunc, scope, name=name,
                                       verbose=verbose)

def _makeSubPEquationWidget(param, scope, verbose=False):
    return SubProblemEquationParameterWidget(param, scope, name=param.name,
                                             verbose=verbose)

meshparameters.SubProblemEquationParameter.makeWidget = _makeSubPEquationWidget

class EquationBCParameterWidget(MeshParamWidget, IndexableWidget):
    def __init__(self, param, scope, name=None, verbose=False):
        eqfunc = mesh.Mesh.all_subproblem_equations_bc
        MeshParamWidget.__init__(self, param, eqfunc, scope, name,
                                 verbose=verbose)

def _makeEquationBCWidget(param, scope, verbose=False):
    return EquationBCParameterWidget(param, scope, name=param.name,
                                     verbose=verbose)

meshparameters.EquationBCParameter.makeWidget = _makeEquationBCWidget

class SubProblemEquationBCParameterWidget(SubProblemParamWidget,
                                          IndexableWidget):
    def __init__(self, param, scope, name=None, verbose=False):
        eqfunc = subproblemcontext.SubProblemContext.all_equations_bc
        SubProblemParamWidget.__init__(self, param, eqfunc, scope, name,
                                       verbose=verbose)

def _makeSubPEquationBCWidget(param, scope, verbose=False):
    return SubProblemEquationBCParameterWidget(param, scope, name=param.name,
                                               verbose=verbose)

meshparameters.SubProblemEquationBCParameter.makeWidget = \
                                                     _makeSubPEquationBCWidget

#############################################
#############################################

class FieldIndexParameterWidget(parameterwidgets.ParameterWidget):
    def __init__(self, param, scope, name=None, verbose=False):
        debug.mainthreadTest()
        self.chooser = chooser.ChooserWidget([], callback=self.chooserCB,
                                             name=name)
        box = gtk.VBox()
        box.pack_start(self.chooser.gtk, expand=0, fill=0)
        parameterwidgets.ParameterWidget.__init__(self, box, scope, verbose)
        self.fieldwidget = scope.findWidget(
            lambda w: isinstance(w, IndexableWidget))
        self.sbcallback = switchboard.requestCallbackMain(self.fieldwidget,
                                                          self.fieldCB)
        self.notapplicable = gtk.Label('(Not Applicable)')
        self.notapplicable.set_alignment(0.0, 0.5)
        box.pack_start(self.notapplicable, expand=0, fill=0)
        self.nIndices = 0
        self.update()
        if param.value in self.chooser.choices():
            self.chooser.set_state(param.value)
        self.widgetChanged(1, interactive=0)
    def chooserCB(self, *args):
        self.widgetChanged(1, interactive=1)
    def fieldCB(self, interactive):
        self.update()
        self.widgetChanged(1, interactive)
    def update(self):                   # field has changed
        itlist = []
        self.nIndices = 0
        field = self.fieldwidget.get_value()
        if field is not None:
            iterator = field.iterator_all()
            while not iterator.end():
                self.nIndices += 1
                it = iterator.cloneIndex()
                itrepr = it.shortrepr()
                itlist.append(itrepr)
                iterator.next()
        self.chooser.update(itlist)
        self.show()
    def show(self):
        debug.mainthreadTest()
        self.gtk.show()
        if self.nIndices > 1:
            self.chooser.show()
            self.notapplicable.hide()
        else:
            self.chooser.gtk.hide()
            self.notapplicable.show()
    def get_value(self):
        val = self.chooser.get_value()
        if val is None:
            return ''
        return val
    def cleanUp(self):
        parameterwidgets.ParameterWidget.cleanUp(self)
        switchboard.removeCallback(self.sbcallback)

def _makeFieldIndexParameterWidget(param, scope, verbose=False):
    return FieldIndexParameterWidget(param, scope, name=param.name, 
                                     verbose=verbose)

meshparameters.FieldIndexParameter.makeWidget = _makeFieldIndexParameterWidget


class SubProblemExluder:
      def __init__(self, widget, base):
	  self.widget = widget
	  self.subps = []
	  self.base = base
		 
      def __call__(self, mesh):
	  if self.widget is None:
	     return mesh.subproblems()
	  else:
	     subp = self.base[self.widget.get_value()]
	     for subproblem in mesh.subproblems():
		 if (subproblem.path() != subp.path() or
                     subproblem.name() == "default"):
		    self.subps.append(subproblem)
	     return self.subps


############################################################

# Not a widget for listing things in a SubProblem, but for listing the
# SubProblems in a Mesh.  This is only a bit of a hack, since it's
# different than the other widgets in the class.  The value of a
# SubProblemParameter is the SubProblem's path (similar to a
# WhoWidget), whereas the value of the other types of MeshParamWidget
# is a real object.

class SubProblemWidget(MeshParamWidget):
    def __init__(self, param, scope, name=None, verbose=False):
        self.scope = scope
        self.targetwidget = self.scope.findWidget(
            lambda w: isinstance(w, whowidget.WhoParameterWidget))
        
        self.exclude = SubProblemExluder(
            self.targetwidget, subproblemcontext.subproblems)
        
        MeshParamWidget.__init__(self, param, self.exclude, scope, name,
                                 verbose=verbose)
        
        self.sbcallbacks.append(
            switchboard.requestCallbackMain(("new who", "SubProblem"),
                                            self.newSubProblemCB))
    def newSubProblemCB(self, subp):
        self.update(interactive=False)
    def get_value(self):
        subp = MeshParamWidget.get_value(self)
        if subp:
            return subp.path()
    def set_value(self, path):
        try:
	    subp = subproblemcontext.subproblems[path]
            MeshParamWidget.set_value(self, subp)
        except KeyError:
            pass

def _makeSubProblemWidget(param, scope, verbose=False):
    return SubProblemWidget(param, scope, name=param.name, verbose=verbose)

subproblemcontext.SubProblemParameter.makeWidget = _makeSubProblemWidget

############################################################

# Special widget for mesh boundary parameters.  As it turns out, these
# params take strings, not boundary objects, so we override a
# significant fraction of the foregoing machinery, which is really
# designed for parameters which take the actual object.

class MeshBoundaryParamWidget(MeshParamWidget):
    def __init__(self, param, scope, name=None, verbose=False):
        MeshParamWidget.__init__(self, param, _getSortedBdyNames,
                                 scope, name=name, separator_func=_bdysepfunc,
                                 verbose=verbose)
        self.sbcallbacks.append(
            switchboard.requestCallbackMain('mesh boundaries changed',
                                            self.newBdys) )
    def newBdys(self, msh):
        if msh is self.getSource():
            self.update(interactive=0)
    def update(self, interactive):
        msh = self.getSource()
        if msh is not None:
            namelist = self.meshfunc(msh)
            self.chooser.update(namelist)
##             # remove from namelist the boundaries with visible=False
##             for name in namelist:
##                 try: # ignore the separator which will cause a key error
##                     print name, msh.getObject().boundaries[name].visible
##                     if not msh.getObject().boundaries[name].visible:
##                         namelist.remove(name)
##                 except:
##                     pass
            if namelist: # If list has nonzero length, widget is valid.
                self.widgetChanged(1, interactive)
        else:
            self.chooser.update([])
            self.widgetChanged(0, interactive)
    def set_value(self, value):
        if value in self.chooser.choices():
            self.chooser.set_state(value)
            self.widgetChanged(1, interactive=0)
    def get_value(self):
        return self.chooser.get_value()

def _makeBoundaryWidget(param, scope, verbose=False):
    return MeshBoundaryParamWidget(param, scope, name=param.name, 
                                   verbose=verbose)

meshparameters.MeshBoundaryParameter.makeWidget = _makeBoundaryWidget

# The MeshBoundaryParamWidget puts _separator_proxy in the list of
# boundaries to divide the edge boundaries from the point boundaries.
# The ChooserWidget replaces it with a real separator, using
# _bdysepfunc as the predicate.

_separator_proxy = "----------"

def _getSortedBdyNames(msh):
    if config.dimension() == 2:
        return (msh.edgeBoundaryNames() + [_separator_proxy] + 
                msh.visiblePointBoundaryNames())
    return (msh.faceBoundaryNamesSorted() + [_separator_proxy] + 
            msh.edgeBoundaryNamesSorted() + [_separator_proxy] + 
            msh.visiblePointBoundaryNamesSorted())
    

def _bdysepfunc(model, iter):
    return model[iter][0] == _separator_proxy





# Special cases for nontrivial face, edge and point boundaries.

if config.dimension() == 3:

    class MeshFaceBdyParamWidget(MeshBoundaryParamWidget):
        def __init__(self, param, scope, name=None, verbose=False):
            MeshParamWidget.__init__(self, param,
                                      mesh.Mesh.faceBoundaryNamesSorted,
                                      scope, name=name, verbose=verbose)
            self.sbcallbacks.append(
                switchboard.requestCallbackMain('mesh boundaries changed',
                                                self.newBdys) )

    def _makeFaceBdyWidget(param, scope, verbose=False):
        return MeshFaceBdyParamWidget(param, scope, name=param.name,
                                      verbose=verbose)

    meshparameters.MeshFaceBdyParameter.makeWidget = _makeFaceBdyWidget



class MeshEdgeBdyParamWidget(MeshBoundaryParamWidget):
    def __init__(self, param, scope, name=None, verbose=False):
        MeshParamWidget.__init__(self, param,
                                  mesh.Mesh.edgeBoundaryNames,
                                  scope, name=name, verbose=verbose)
        self.sbcallbacks.append(
            switchboard.requestCallbackMain('mesh boundaries changed',
                                            self.newBdys) )

def _makeEdgeBdyWidget(param, scope, verbose=False):
    return MeshEdgeBdyParamWidget(param, scope, name=param.name, 
                                  verbose=verbose)

meshparameters.MeshEdgeBdyParameter.makeWidget = _makeEdgeBdyWidget


class MeshPeriodicEdgeBdyParamWidget(MeshBoundaryParamWidget):
    def __init__(self, param, scope, name=None, verbose=False):
        MeshParamWidget.__init__(self, param,
                                  mesh.Mesh.periodicEdgeBoundaryNames,
                                  scope, name=name, verbose=verbose)
        self.sbcallbacks.append(
            switchboard.requestCallbackMain('mesh boundaries changed',
                                            self.newBdys) )

def _makePeriodicEdgeBdyWidget(param, scope, verbose=False):
    return MeshPeriodicEdgeBdyParamWidget(param, scope, name=param.name,
                                          verbose=verbose)

meshparameters.MeshPeriodicEdgeBdyParameter.makeWidget = _makePeriodicEdgeBdyWidget



class MeshPointBdyParamWidget(MeshBoundaryParamWidget):
    def __init__(self, param, scope, name=None, verbose=False):
        MeshParamWidget.__init__(self, param,
                                  mesh.Mesh.visiblePointBoundaryNames,
                                  scope, name=name, verbose=verbose)
        self.sbcallbacks.append(
            switchboard.requestCallbackMain('mesh boundaries changed',
                                        self.newBdys) )


def _makePointBdyWidget(param, scope, verbose=False):
    return MeshPointBdyParamWidget(param, scope, name=param.name,
                                   verbose=verbose)

meshparameters.MeshPointBdyParameter.makeWidget = _makePointBdyWidget

#Interface branch
def _getSortedBdyInterfaceNames(msh):
    interfacemsplugin=msh.getMicrostructure().getPlugIn("Interfaces")
    if config.dimension() == 2:
        return msh.edgeBoundaryNames() + [_separator_proxy] + \
            interfacemsplugin.getInterfaceNames()
    return msh.faceBoundaryNamesSorted() + [_separator_proxy] + \
        msh.edgeBoundaryNames() + [_separator_proxy] + \
        interfacemsplugin.getInterfaceNames()

# This one includes the string "<every>"
if config.dimension() == 3:
    def _getMeshFaceBdyNamesExtra(msh):
        return [placeholder.every.IDstring] + msh.faceBoundaryNamesSorted()

def _getMeshEdgeBdyNamesExtra(msh):
    return [placeholder.every.IDstring] + msh.edgeBoundaryNames()

#This one lists mesh boundary names and interface names together.
#It is no longer used, as new mesh boundaries are also
#created from interfaces (originally, mesh boundaries are
#created only based on a skeleton boundary template).
class MeshEdgeBdyInterfaceParamWidget(MeshBoundaryParamWidget):
    def __init__(self, param, scope, name=None, verbose=False):
        MeshParamWidget.__init__(self, param, _getSortedBdyInterfaceNames,
                                 scope, name=name, separator_func=_bdysepfunc,
                                 verbose=verbose)
        self.sbcallbacks.append(
            switchboard.requestCallbackMain('mesh boundaries changed',
                                            self.newBdys) )

def _makeEdgeBdyInterfaceWidget(param, scope, verbose=False):
    return MeshEdgeBdyInterfaceParamWidget(param, scope, name=param.name,
                                           verbose=verbose)

meshparameters.MeshEdgeBdyInterfaceParameter.makeWidget = _makeEdgeBdyInterfaceWidget

class MeshEdgeBdyParamWidgetExtra(MeshBoundaryParamWidget):
    def __init__(self, param, scope, name=None, verbose=False):
        MeshParamWidget.__init__(self, param, _getMeshEdgeBdyNamesExtra,
                                 scope, name=name, separator_func=_bdysepfunc,
                                 verbose=verbose)
        self.sbcallbacks.append(
            switchboard.requestCallbackMain('mesh boundaries changed',
                                            self.newBdys) )

def _makeEdgeBdyWidgetExtra(param, scope, verbose=False):
    return MeshEdgeBdyParamWidgetExtra(param, scope, name=param.name,
                                       verbose=verbose)

meshparameters.MeshEdgeBdyParameterExtra.makeWidget = _makeEdgeBdyWidgetExtra
