# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.2 $
# $Author: fyc $
# $Date: 2013/07/19 17:23:49 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

from generics import *

def activeVolumeStatusCheck(nactive, ntotal, override=False):
    status = gtklogger.findWidget('OOF3D:Active Volume Page:Pane:Status')
    if override:
        return status.get_text()=="OVERRIDE: all %d voxels are active" % ntotal
    return status.get_text() == '%d of %d voxels are active' % (nactive, ntotal)

def voxelSelectionCheck(n):
    return pixelSelectionSizeCheck('5color', n)

def activeVolumeMSCheck(msname, n):
    from ooflib.common.IO import whoville
    ms = whoville.getClass('Microstructure')[msname].getObject()
    npix = ms.size()[0]*ms.size()[1]
    return npix - ms.activearea.size()  # aa.size() is no. of inactive voxels

def activeVolumeCheck(n):
    return activeVolumeMSCheck('5color', n)

def activeVolumeOverrideCheck(o):
    from ooflib.common.IO import whoville
    ms = whoville.getClass('Microstructure')['5color'].getObject()
    return ms.activearea.getOverride() == o

def activeVolumePageSensitivityCheck0():
    return (sensitizationCheck({'OOF3D:Active Volume Page:Microstructure' : 1})
            and
            sensitizationCheck({"Store" : 1,
                                "Rename" : 0,
                                "Delete" : 0,
                                "Restore" : 0,
                                "Modify:Method" : 1,
                                "Modify:Prev" : 1,
                                "Modify:OK" : 1,
                                "Modify:Next" : 1,
                                "Modify:Undo" : 0,
                                "Modify:Redo" : 0,
                                "Modify:Override" : 1
                                },
                               base="OOF3D:Active Volume Page:Pane"))

def activeVolumePageSensitivityCheck1():
    return (sensitizationCheck({'OOF3D:Active Volume Page:Microstructure' : 1})
            and
            sensitizationCheck({"Store" : 1,
                                "Rename" : 1,
                                "Delete" : 1,
                                "Restore" : 1,
                                "Modify:Method" : 1,
                                "Modify:Prev" : 0,
                                "Modify:OK" : 1,
                                "Modify:Next" : 0,
                                "Modify:Undo" : 1,
                                "Modify:Redo" : 0,
                                "Modify:Override" : 1
                                },
                               base="OOF3D:Active Volume Page:Pane"))
            

