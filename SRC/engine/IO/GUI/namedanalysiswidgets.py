# -*- python -*-
# $RCSfile: namedanalysiswidgets.py,v $
# $Revision: 1.5.10.4 $
# $Author: fyc $
# $Date: 2014/07/07 22:09:02 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common.IO.GUI import chooser
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.engine import namedanalysis

class AllAnalyses(object):
    def getNames(self):
        return (namedanalysis.analysisNames())
    def signals(self):
        return [
            switchboard.requestCallbackMain("named analyses changed",
                                            self.update)
            ]

class AnalysisNamesWidgetBase(parameterwidgets.ParameterWidget):
    def __init__(self, param, scope=None, name=None, verbose=False):
        names = self.getNames()
        names.sort()
        self.widget = chooser.ScrolledMultiListWidget(names,
                                                      callback=self.widgetCB)
        parameterwidgets.ParameterWidget.__init__(self, self.widget.gtk,
                                                  scope, name=name,
                                                  expandable=True,
                                                  verbose=verbose)
        self.widget.set_selection(param.value)
        self.widgetChanged(param.value is not None, interactive=False)
        self.sbcallbacks = self.signals()
        self.widgetChanged(len(self.get_value()) > 0, interactive=False)
    def cleanUp(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        parameterwidgets.ParameterWidget.cleanUp(self)
    def get_value(self):
        return self.widget.get_value()
    def set_value(self, value):
        self.widget.set_selection(value)
    def widgetCB(self, list, interactive):
        self.widgetChanged(len(list) > 0, interactive=True)
    def update(self, *args):
        names = self.getNames()
        names.sort()
        self.widget.update(names)
        self.widgetChanged(len(self.get_value()) > 0, interactive=False)


class AnalysisNamesWidget(AnalysisNamesWidgetBase, AllAnalyses):
    pass

def _AnalysisNamesParam_makeWidget(self, scope=None, verbose=False):
    return AnalysisNamesWidget(self, scope, name=self.name, verbose=verbose)

namedanalysis.AnalysisNamesParameter.makeWidget = _AnalysisNamesParam_makeWidget

################

class AnalysisNameWidgetBase(parameterwidgets.ParameterWidget):
    def __init__(self, param, scope=None, name=None, verbose=False):
        self.chooser = chooser.ChooserWidget([], name=name)
        parameterwidgets.ParameterWidget.__init__(self, self.chooser.gtk, scope, verbose=verbose)
        self.update()
        if param.value is not None:
            self.set_value(param.value)
        self.sbcallbacks = [
            switchboard.requestCallbackMain("named analyses changed",
                                            self.update)
            ]
    def cleanUp(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        parameterwidgets.ParameterWidget.cleanUp(self)
    def set_value(self, name):
        self.chooser.set_state(name)
        self.widgetChanged(name is not None, interactive=False)
    def get_value(self):
        return self.chooser.get_value()
    def update(self, *args):
        names = self.getNames()
        names.sort()
        self.chooser.update(names)
        self.widgetChanged(len(names) > 0, interactive=False)


class AnalysisNameWidget(AnalysisNameWidgetBase, AllAnalyses):
    pass

def _AnalysisNameParam_makeWidget(self, scope=None, verbose=False):
    return AnalysisNameWidget(self, scope, name=self.name, verbose=verbose)

namedanalysis.AnalysisNameParameter.makeWidget = _AnalysisNameParam_makeWidget
