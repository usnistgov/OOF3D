# -*- python -*-
# $RCSfile: interfacewidget.py,v $
# $Revision: 1.3.10.2 $
# $Author: langer $
# $Date: 2014/05/15 15:06:15 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import switchboard
from ooflib.common.IO.GUI import chooser
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import whowidget
from ooflib.engine.IO import interfaceparameters
from ooflib.engine.IO.GUI import materialwidget
import ooflib.common.microstructure
from ooflib.engine import skeletoncontext

#The following widgets list interface and boundary names

#Listbox
class ListOfInterfacesWidget(parameterwidgets.ParameterWidget):
    def __init__(self, param, scope=None, name=None, verbose=False):
        self.widget = chooser.ScrolledMultiListWidget([],
                                                      callback=self.widgetCB)

        parameterwidgets.ParameterWidget.__init__(self, self.widget.gtk,
                                                  scope=scope, name=name,
                                                  expandable=True,
                                                  verbose=verbose)
        self.mswidget = self.scope.findWidget(
            lambda w: isinstance(w, whowidget.WhoWidget)
            and w.whoclass is ooflib.common.microstructure.microStructures)
        self.update()
        if param.value is not None:
            self.widget.set_selection(param.value)
        self.sbcallbacks = [
            switchboard.requestCallbackMain(self.mswidget, self.update)
            ]
    def cleanUp(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        self.mswidget = None
        parameterwidgets.ParameterWidget.cleanUp(self)
    def update(self, *args, **kwargs):
        msname = self.mswidget.get_value()
        if msname:
            ms = ooflib.common.microstructure.microStructures[msname]
            if ms:
                interfacemsplugin=ms.getObject().getPlugIn("Interfaces")
                names=interfacemsplugin.getInterfaceNames()
                names.sort()
                self.widget.update(names)
                self.widgetChanged(len(names) > 0, interactive=0)
                return
        self.widget.update([])
        self.widgetChanged(0, interactive=0)
    def get_value(self):
        return self.widget.get_value()
    def set_value(self, value):
        self.widget.set_selection(value)
    def widgetCB(self, list, interactive):
        self.widgetChanged(len(list) > 0, interactive=1)

def _makeListOfInterfacesWidget(self, scope=None, verbose=False):
    return ListOfInterfacesWidget(self, scope=scope, name=self.name, 
                                  verbose=verbose)

interfaceparameters.ListOfInterfacesParameter.makeWidget = _makeListOfInterfacesWidget

#Listbox. This widget differs from the above widget by having
#a self.interfacematwidget member
class ListOfInterfacesWithMaterialWidget(parameterwidgets.ParameterWidget):
    def __init__(self, param, scope=None, name=None, verbose=False):
        self.widget = chooser.ScrolledMultiListWidget([],
                                                      callback=self.widgetCB)

        parameterwidgets.ParameterWidget.__init__(self, self.widget.gtk,
                                                  scope=scope, name=name,
                                                  expandable=True,
                                                  verbose=verbose)
        self.mswidget = self.scope.findWidget(
            lambda w: isinstance(w, whowidget.WhoWidget)
            and w.whoclass is ooflib.common.microstructure.microStructures)
        self.interfacematwidget = self.scope.findWidget(
            lambda w: isinstance(w, materialwidget.InterfaceMaterialWidget))
        self.update()
        if param.value is not None:
            self.widget.set_selection(param.value)
        self.sbcallbacks = [
            switchboard.requestCallbackMain(self.mswidget, self.update),
            switchboard.requestCallbackMain(self.interfacematwidget, self.update)
            ]
    def cleanUp(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        self.mswidget = None
        self.interfacematwidget = None
        parameterwidgets.ParameterWidget.cleanUp(self)
    def update(self, *args, **kwargs):
        msname = self.mswidget.get_value()
        interfacematname = self.interfacematwidget.get_value()
        if msname:
            ms = ooflib.common.microstructure.microStructures[msname]
            if ms:
                interfacemsplugin=ms.getObject().getPlugIn("Interfaces")
                names=interfacemsplugin.getInterfaceNamesWithMaterial(interfacematname)
                if names:
                    names.sort()
                    self.widget.update(names)
                    self.widgetChanged(len(names) > 0, interactive=0)
                    return
        self.widget.update([])
        self.widgetChanged(0, interactive=0)
    def get_value(self):
        return self.widget.get_value()
    def set_value(self, value):
        self.widget.set_selection(value)
    def widgetCB(self, list, interactive):
        self.widgetChanged(len(list) > 0, interactive=1)

def _makeListOfInterfacesWithMaterialWidget(self, scope=None, verbose=False):
    return ListOfInterfacesWithMaterialWidget(self, scope=scope, name=self.name,
                                              verbose=verbose)

interfaceparameters.ListOfInterfacesWithMaterialParameter.makeWidget = _makeListOfInterfacesWithMaterialWidget

#Drop-down combobox
class InterfacesWidget(parameterwidgets.ParameterWidget):
    def __init__(self, param, scope=None, name=None, verbose=False):
        self.widget = chooser.ChooserWidget([],
                                            callback=self.widgetCB,
                                            name=name)
        parameterwidgets.ParameterWidget.__init__(self, self.widget.gtk,
                                                  scope=scope, name=name,
                                                  verbose=verbose)
        self.mswidget = self.scope.findWidget(
            lambda w: isinstance(w, whowidget.WhoWidget)
            and w.whoclass is skeletoncontext.skeletonContexts) #Needs an MS:Skeleton
        self.sbcallbacks = [
            switchboard.requestCallbackMain(self.mswidget, self.update),
            switchboard.requestCallbackMain("new interface created",
                                            self.update),
            switchboard.requestCallbackMain("interface removed",
                                            self.update),
            switchboard.requestCallbackMain("interface renamed",
                                            self.update),
            ]
        self.update(interactive=0)
        if param.value is not None and self.widget.nChoices()>0:
            self.set_value(param.value)
    def cleanUp(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        self.mswidget = None
        parameterwidgets.ParameterWidget.cleanUp(self)
    def update(self, *args, **kwargs):
        msname = self.mswidget.get_value(depth=1) #Get the ms path
        if msname:
            ms = ooflib.common.microstructure.microStructures[msname]
            if ms:
                interfacemsplugin=ms.getObject().getPlugIn("Interfaces")
                names=interfacemsplugin.getInterfaceNames()
                names.sort()
                self.widget.update(names)
                self.widgetChanged(len(names) > 0, interactive=0)
                return
        self.widget.update([])
        self.widgetChanged(0, interactive=0)
    def get_value(self):
        return self.widget.get_value()
    def set_value(self, value):
        self.widget.set_state(value)
    def widgetCB(self, gtkobj, name):
        self.widgetChanged(validity=self.widget.nChoices()>0, interactive=1)

def _makeInterfacesWidget(self, scope=None, verbose=False):
    return InterfacesWidget(self, scope=scope, name=self.name, verbose=verbose)

interfaceparameters.InterfacesParameter.makeWidget = _makeInterfacesWidget

#Listbox
## Includes skeleton boundary names ##
class ListOfInterfacesSkelBdyWidget(ListOfInterfacesWidget):
    def update(self, *args, **kwargs):
        msname = self.mswidget.get_value()
        if msname:
            ms = ooflib.common.microstructure.microStructures[msname]
            if ms:
                interfacemsplugin=ms.getObject().getPlugIn("Interfaces")
                inames=interfacemsplugin.getInterfaceNames()
                sbnames=interfacemsplugin.getSkelBdyNames()
                inames.sort()
                sbnames.sort()
                names=inames+sbnames
                self.widget.update(names)
                self.widgetChanged(len(names) > 0, interactive=0)
                return
        self.widget.update([])
        self.widgetChanged(0, interactive=0)

def _makeListOfInterfacesSkelBdyWidget(self, scope=None, verbose=False):
    return ListOfInterfacesSkelBdyWidget(self, scope=scope, name=self.name,
                                         verbose=verbose)

interfaceparameters.ListOfInterfacesSkelBdyParameter.makeWidget = _makeListOfInterfacesSkelBdyWidget

#Listbox. This widget differs from the above widget by having
#a self.interfacematwidget member
class ListOfInterfacesSkelBdyWithMaterialWidget(ListOfInterfacesWithMaterialWidget):
    def update(self, *args, **kwargs):
        msname = self.mswidget.get_value()
        interfacematname = self.interfacematwidget.get_value()
        if msname:
            ms = ooflib.common.microstructure.microStructures[msname]
            if ms:
                interfacemsplugin=ms.getObject().getPlugIn("Interfaces")
                inames=interfacemsplugin.getInterfaceNamesWithMaterial(interfacematname)
                sbnames=interfacemsplugin.getSkelBdyNamesWithMaterial(interfacematname)
                inames.sort()
                sbnames.sort()
                names=inames+sbnames
                self.widget.update(names)
                self.widgetChanged(len(names) > 0, interactive=0)
                return
        self.widget.update([])
        self.widgetChanged(0, interactive=0)

def _makeListOfInterfacesSkelBdyWithMaterialWidget(self, scope=None, 
                                                   verbose=False):
    return ListOfInterfacesSkelBdyWithMaterialWidget(
        self, scope=scope, name=self.name, verbose=verbose)

interfaceparameters.ListOfInterfacesSkelBdyWithMaterialParameter.makeWidget = _makeListOfInterfacesSkelBdyWithMaterialWidget

###################################################################################
#Drop-down combobox
#Lists skeleton names plus "<All>"
class SkelAllWidget(parameterwidgets.ParameterWidget):
    def __init__(self, param, scope=None, name=None, verbose=False):
        self.widget = chooser.ChooserWidget([],
                                            callback=self.widgetCB,
                                            name=name)
        parameterwidgets.ParameterWidget.__init__(self, self.widget.gtk,
                                                  scope=scope, name=name,
                                                  verbose=verbose)
        self.mswidget = self.scope.findWidget(
            lambda w: isinstance(w, whowidget.WhoWidget)
            and w.whoclass is ooflib.common.microstructure.microStructures)
        self.sbcallbacks = [
            switchboard.requestCallbackMain(self.mswidget, self.update)
            ]
        self.update(interactive=0)
        if param.value is not None and self.widget.nChoices()>0:
            self.set_value(param.value)
    def cleanUp(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        self.mswidget = None
        parameterwidgets.ParameterWidget.cleanUp(self)
    def update(self, *args, **kwargs):
        msname = self.mswidget.get_value(depth=1) #Get the ms path
        if msname:
            ms = ooflib.common.microstructure.microStructures[msname]
            if ms:
                skelclass=skeletoncontext.skeletonContexts
                names=[]
                for skelkey in skelclass.keys(base=msname):
                    names.append(skelkey[0])
                names.sort()
                names=interfaceparameters.SkelAllParameter.extranames+names
                self.widget.update(names)
                self.widgetChanged(len(names) > 0, interactive=0)
                return
        self.widget.update([])
        self.widgetChanged(0, interactive=0)
    def get_value(self):
        return self.widget.get_value()
    def set_value(self, value):
        self.widget.set_state(value)
    def widgetCB(self, gtkobj, name):
        self.widgetChanged(validity=self.widget.nChoices()>0, interactive=1)

def _makeSkelAllWidget(self, scope=None, verbose=False):
    return SkelAllWidget(self, scope=scope, name=self.name, verbose=verbose)

interfaceparameters.SkelAllParameter.makeWidget = _makeSkelAllWidget

#Listbox
#The list is modulated by a microstructure widget and another widget
#that has a chooser for the skeleton names. Includes an option
#called "<All>" that lists all interface names and all skeleton boundary names
#that are common to all skeletons in the microstructure.
class ListOfInterfacesCombinedBdysWidget(parameterwidgets.ParameterWidget):
    def __init__(self, param, scope=None, name=None, verbose=False):
        self.widget = chooser.ScrolledMultiListWidget([],
                                                      callback=self.widgetCB)

        parameterwidgets.ParameterWidget.__init__(self, self.widget.gtk,
                                                  scope=scope, name=name,
                                                  expandable=True,
                                                  verbose=verbose)
        self.mswidget = self.scope.findWidget(
            lambda w: isinstance(w, whowidget.WhoWidget)
            and w.whoclass is ooflib.common.microstructure.microStructures)
        self.skelallwidget = self.scope.findWidget(
            lambda w: isinstance(w, SkelAllWidget))
        self.update()
        if param.value is not None:
            self.widget.set_selection(param.value)
        self.sbcallbacks = [
            switchboard.requestCallbackMain(self.mswidget, self.update),
            switchboard.requestCallbackMain(self.skelallwidget, self.update)
            ]
    def cleanUp(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        self.skelallwidget = None
        self.mswidget = None
        parameterwidgets.ParameterWidget.cleanUp(self)
    def update(self, *args, **kwargs):
        msname = self.mswidget.get_value()
        if msname:
            ms = ooflib.common.microstructure.microStructures[msname]
            if ms:
                interfacemsplugin=ms.getObject().getPlugIn("Interfaces")
                names=interfacemsplugin.getInterfaceNames()
                names.sort()
                skelname=self.skelallwidget.get_value()
                if skelname:
                    if skelname==interfaceparameters.SkelAllParameter.extranames[0]:
                        commonbdynames=interfacemsplugin.getCommonSkelBdyNames()
                        commonbdynames.sort()
                        names=names+commonbdynames
                    else:
                        bdynames=interfacemsplugin.getOneSkelBdyNames(skelname)
                        bdynames.sort()
                        names=names+bdynames
                self.widget.update(names)
                self.widgetChanged(len(names) > 0, interactive=0)
                return
        self.widget.update([])
        self.widgetChanged(0, interactive=0)
    def get_value(self):
        return self.widget.get_value()
    def set_value(self, value):
        self.widget.set_selection(value)
    def widgetCB(self, list, interactive):
        self.widgetChanged(len(list) > 0, interactive=1)

def _makeListOfInterfacesCombinedBdysWidget(self, scope=None, verbose=False):
    return ListOfInterfacesCombinedBdysWidget(self, scope=scope, name=self.name,
                                              verbose=verbose)

interfaceparameters.ListOfInterfacesCombinedBdysParameter.makeWidget = _makeListOfInterfacesCombinedBdysWidget
