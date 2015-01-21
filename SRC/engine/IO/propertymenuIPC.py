# -*- python -*-
# $RCSfile: propertymenuIPC.py,v $
# $Revision: 1.3.18.1 $
# $Author: langer $
# $Date: 2014/09/27 22:34:20 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.common.IO import oofmenu
from ooflib.common.IO import parallelmainmenu
from ooflib.common.IO import parameter
from ooflib.engine import propertyregistration

AllProperties = propertyregistration.AllProperties
StringParameter = parameter.StringParameter

## OOF.LoadData.IPC.Property
ipcpropmenu = parallelmainmenu.ipcmenu.addItem(
    oofmenu.OOFMenuItem('Property', secret=1, no_log=1)
    )

def parallel_copywrapper(menuitem, property, new_name):
    try:
        AllProperties.new_prop(property, new_name)
    except ErrUserError, e:
        print e

ipcpropmenu.addItem(oofmenu.OOFMenuItem(
    'Copy',
    callback=parallel_copywrapper,
    threadable=oofmenu.PARALLEL_THREADABLE,
    params=
    [
    StringParameter('property'),
    StringParameter('new_name')
    ]
    ))

def parallel_deletewrapper(menuitem, property):
    try:
        AllProperties.delete(property)
    except ErrUserError, e:
        print e

ipcpropmenu.addItem(oofmenu.OOFMenuItem(
    'Delete',
    callback=parallel_deletewrapper,
    params=
    [
    StringParameter('property')
    ]
    ))

AllProperties.set_parallel_parametrizercallback()
