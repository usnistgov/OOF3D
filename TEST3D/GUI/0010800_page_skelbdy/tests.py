# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.3 $
# $Author: langer $
# $Date: 2014/09/27 22:34:52 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from generics import *

def boundariesCheck(*names):
    return chooserCheck(
        'OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList',
        names)

def _getStatusText():
    textviewer = gtklogger.findWidget('OOF3D:Skeleton Boundaries Page:Pane:Boundary data:InfoScroll:status')
    buffer = textviewer.get_buffer()
    return buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter())
    
def voxelSelectionPageStatusCheck(name, bdytype, size):
    if name is '':
      return _getStatusText() == "No boundary selected."
    else:
      return _getStatusText() == "Boundary %s:\nType: %s\nSize: %d" % (name, bdytype, size)
      
def boundariesSelectedCheck(name):
    return name == treeViewSelectCheck('OOF3D:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList', 0)

def sensitization0():
    return (sensitizationCheck(
        {'New' : 0,
         'Modify' : 0,
         'Rename' : 0,
         'Delete' : 0
        },
        base="OOF3D:Skeleton Boundaries Page:Pane:Boundaries"))

def sensitization1():
    return (sensitizationCheck(
        {'New' : 1,
         'Modify' : 0,
         'Rename' : 0,
         'Delete' : 0
        },
        base="OOF3D:Skeleton Boundaries Page:Pane:Boundaries"))

def sensitization2():
    return (sensitizationCheck(
        {'New' : 1,
         'Modify' : 1,
         'Rename' : 1,
         'Delete' : 1
        },
        base="OOF3D:Skeleton Boundaries Page:Pane:Boundaries"))
        
        
