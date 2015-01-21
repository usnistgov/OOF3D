# -*- python -*-
# $RCSfile: orientmapwhowidget.py,v $
# $Revision: 1.2.18.2 $
# $Author: langer $
# $Date: 2014/09/27 22:34:43 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 


# Widgets for listing Microstructures with or without Orientation Map data.

from ooflib.SWIG.orientationmap import orientmapdata
from ooflib.common import debug
from ooflib.common.IO import whoville
from ooflib.common.IO.GUI import whowidget
from ooflib.orientationmap import orientmapmenu

def _withOrientationMap(who):
    return (whoville.excludeProxies(who) and
            orientmapdata.getOrientationMap(who.getObject()) is not None)

class MicrostructureWithOrientationMapWidget(whowidget.WhoParameterWidget):
    def __init__(self, value=None, scope=None, name=None, verbose=False):
        whowidget.WhoParameterWidget.__init__(
            self, whoclass=whoville.getClass('Microstructure'),
            value=value, scope=scope, name=name,
            condition=_withOrientationMap,
            verbose=verbose)

def _MicrostructureWithOrientMapParameter_makeWidget(self, scope=None, 
                                                     verbose=False):
    return MicrostructureWithOrientationMapWidget(
        self.value, scope=scope, name=self.name, verbose=verbose)

orientmapmenu.MicrostructureWithOrientMapParameter.makeWidget = \
                              _MicrostructureWithOrientMapParameter_makeWidget

##########

def _withoutOrientationMap(who):
    result = (whoville.excludeProxies(who) and
            orientmapdata.getOrientationMap(who.getObject()) is None)
    return result

class MicrostructureWithoutOrientationMapWidget(whowidget.WhoParameterWidget):
    def __init__(self, value=None, scope=None, name=None, verbose=False):
        whowidget.WhoParameterWidget.__init__(
            self, whoclass=whoville.getClass('Microstructure'),
            value=value, scope=scope, name=name,
            condition=_withoutOrientationMap, verbose=verbose)

def _MicrostructureWithoutOrientMapParameter_makeWidget(self, scope=None,
                                                        verbose=False):
    return MicrostructureWithoutOrientationMapWidget(
        self.value, scope=scope, name=self.name, verbose=verbose)

orientmapmenu.MicrostructureWithoutOrientMapParameter.makeWidget = \
                            _MicrostructureWithoutOrientMapParameter_makeWidget
