# -*- python -*-
# $RCSfile: materialwidget.py,v $
# $Revision: 1.24.2.2 $
# $Author: langer $
# $Date: 2014/05/08 14:39:04 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import switchboard
from ooflib.SWIG.engine import material
from ooflib.common import debug
from ooflib.common.IO.GUI import chooser
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import whowidget
from ooflib.engine import materialmanager
from ooflib.engine import mesh
from ooflib.engine import subproblemcontext
from ooflib.engine.IO import materialmenu
from ooflib.engine.IO import materialparameter

class MaterialWidget(parameterwidgets.ParameterWidget):
    def __init__(self, param, scope=None, name=None, verbose=False):
        self.chooser = chooser.ChooserWidget([], callback=self.chooserCB,
                                             name=name)
        parameterwidgets.ParameterWidget.__init__(self, self.chooser.gtk, scope,
                                                  verbose=verbose)
        self.sbcallbacks = [
            switchboard.requestCallbackMain("new_material", self.update),
            switchboard.requestCallbackMain("remove_material", self.update)
            ]
        self.update()
        if param.value is not None:
            self.set_value(param.value)
    def chooserCB(self, gtkobj, name):
        self.widgetChanged(validity=self.chooser.nChoices()>0, interactive=1)
    def cleanUp(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        parameterwidgets.ParameterWidget.cleanUp(self)
    def update(self, *args):
        names = materialmanager.getMaterialNames()
        names.sort()
        self.chooser.update(names)
        self.widgetChanged(len(names) > 0, interactive=0)
    def get_value(self):
        return self.chooser.get_value()
    def set_value(self, material):
        self.chooser.set_state(material)
        self.widgetChanged(validity=(material is not None), interactive=0)

def _MaterialParameter_makeWidget(self, scope=None, verbose=False):
    return MaterialWidget(self, scope, name=self.name, verbose=verbose)
materialparameter.MaterialParameter.makeWidget = _MaterialParameter_makeWidget

#Interface branch
class InterfaceMaterialWidget(MaterialWidget):
    def update(self, *args):
        names = materialmanager.getInterfaceMaterialNames()
        names.sort()
        self.chooser.update(names)
        self.widgetChanged(len(names) > 0, interactive=0)

def _InterfaceMaterialParameter_makeWidget(self, scope=None, verbose=False):
    return InterfaceMaterialWidget(self, scope, name=self.name, verbose=verbose)

materialparameter.InterfaceMaterialParameter.makeWidget = \
    _InterfaceMaterialParameter_makeWidget

#Interface branch
class BulkMaterialWidgetExtra(MaterialWidget):
    def update(self, *args):
        names = materialmanager.getBulkMaterialNames()
        names.sort()
        self.chooser.update(
            materialparameter.BulkMaterialParameterExtra.extranames + names)
        self.widgetChanged(len(names) > 0, interactive=0)

def _BulkMaterialParameterExtra_makeWidget(self, scope=None, verbose=False):
    return BulkMaterialWidgetExtra(self, scope, name=self.name, verbose=verbose)
materialparameter.BulkMaterialParameterExtra.makeWidget = \
    _BulkMaterialParameterExtra_makeWidget

#Interface branch
class BulkMaterialWidget(MaterialWidget):
    def update(self, *args):
        names = materialmanager.getBulkMaterialNames()
        names.sort()
        self.chooser.update(names)
        self.widgetChanged(len(names) > 0, interactive=0)

def _BulkMaterialParameter_makeWidget(self, scope=None, verbose=False):
    return BulkMaterialWidget(self, scope, name=self.name, verbose=verbose)
materialparameter.BulkMaterialParameter.makeWidget = \
    _BulkMaterialParameter_makeWidget

class MeshMaterialWidget(MaterialWidget):
    def __init__(self, param, scope=None, name=None, verbose=False):
        self.meshwidget = scope.findWidget(
            lambda w: isinstance(w, whowidget.WhoWidget)
            and w.whoclass in (mesh.meshes, subproblemcontext.subproblems))
        MaterialWidget.__init__(self, param, scope, name, verbose=verbose)
        self.sbcallbacks.append(
            switchboard.requestCallbackMain(self.meshwidget, self.update))
    def update(self, *args):
        meshname = self.meshwidget.get_value(depth=3)
        meshctxt = mesh.meshes[meshname]
        matls = meshctxt.getObject().getAllMaterials()
        names = [m.name() for m in matls]
        names.sort()
        self.chooser.update(names)
        self.widgetChanged(len(names) > 0, interactive=0)

def _MeshMatParam_makeWidget(self, scope=None, verbose=False):
    return MeshMaterialWidget(self, scope, name=self.name, verbose=verbose)
materialparameter.MeshMaterialParameter.makeWidget = _MeshMatParam_makeWidget
        
########################

class AnyMaterialWidget(MaterialWidget):
    def update(self, *args):
        names = materialmanager.getMaterialNames()
        names.sort()
        self.chooser.update(materialparameter.AnyMaterialParameter.extranames
                            + names)
        self.widgetChanged(validity=1, interactive=0)

def _AnyMaterialParameter_makeWidget(self, scope=None, verbose=False):
    return AnyMaterialWidget(self, scope, name=self.name, verbose=verbose)

materialparameter.AnyMaterialParameter.makeWidget = \
    _AnyMaterialParameter_makeWidget

#Interface branch
class InterfaceAnyMaterialWidget(MaterialWidget):
    def update(self, *args):
        names = materialmanager.getInterfaceMaterialNames()
        names.sort()
        self.chooser.update(
            materialparameter.InterfaceAnyMaterialParameter.extranames + names)
        self.widgetChanged(validity=1, interactive=0)

def _InterfaceAnyMaterialParameter_makeWidget(self, scope=None, verbose=False):
    return InterfaceAnyMaterialWidget(self, scope, name=self.name, 
                                      verbose=verbose)

materialparameter.InterfaceAnyMaterialParameter.makeWidget = \
    _InterfaceAnyMaterialParameter_makeWidget

########################
        
class MaterialsWidget(parameterwidgets.ParameterWidget):
    def __init__(self, param, scope=None, name=None, verbose=False):
        names = materialmanager.getMaterialNames()
        names.sort()
        self.widget = chooser.ScrolledMultiListWidget(names,
                                                      callback=self.widgetCB,
                                                      name=name)
        parameterwidgets.ParameterWidget.__init__(
            self, self.widget.gtk, scope, expandable=True, verbose=verbose)
        self.widget.set_selection(param.value)
        self.sbcallbacks = [
            switchboard.requestCallbackMain('new_material', self.newMaterial),
            switchboard.requestCallbackMain('remove_material',
                                            self.newMaterial)
            ]
        self.widgetChanged((param.value is not None), interactive=0) 
    def cleanUp(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        parameterwidgets.ParameterWidget.cleanUp(self)
    def newMaterial(self, *args):
        names = materialmanager.getMaterialNames()
        names.sort()
        self.widget.update(names)
    def get_value(self):
        return self.widget.get_value()
    def set_value(self, value):
        self.widget.set_selection(value)
    def widgetCB(self, list, interactive):
        self.widgetChanged(len(list) > 0, interactive=1)

def _MaterialsWidget_makeWidget(self, scope=None, verbose=False):
    return MaterialsWidget(self, scope, name=self.name, verbose=verbose)

materialparameter.ListOfMaterialsParameter.makeWidget = \
    _MaterialsWidget_makeWidget
