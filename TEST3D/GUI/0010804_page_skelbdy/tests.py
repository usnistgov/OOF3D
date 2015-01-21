# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.3 $
# $Author: langer $
# $Date: 2014/09/27 22:34:54 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from generics import *

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

def BoundaryNewDialogCheck0(constructor, *directions):
    okbutton = gtklogger.findWidget('Dialog-New Boundary:gtk-ok')
    part1 = ((okbutton.get_property('sensitive') == True) and
           chooserCheck('Dialog-New Boundary:constructor:Chooser', ('Point boundary from nodes',
                                                                   'Point boundary from segments',
                                                                   'Point boundary from faces',
                                                                   'Point boundary from elements',
                                                                   'Edge boundary from nodes',
                                                                   'Edge boundary from segments',
                                                                   'Edge boundary from faces',
                                                                   'Face boundary from faces',
                                                                   'Face boundary from elements',)) and
           chooserCheck('Dialog-New Boundary:constructor:'+constructor+':group', ('<selection>',)))
    if not directions:
       part2 = True
    else:
       part2 = chooserCheck('Dialog-New Boundary:constructor:'+constructor+':direction', directions)
    
    return part1 and part2
    
def BoundaryNewDialogCheck1(constructor, group, direction=None):
    okbutton = gtklogger.findWidget('Dialog-New Boundary:gtk-ok')
    return ((okbutton.get_property('sensitive') == True) and
           chooserStateCheck('Dialog-New Boundary:constructor:Chooser', constructor) and
           chooserStateCheck('Dialog-New Boundary:constructor:'+constructor+':group', group) and
           ((direction == None) or chooserStateCheck('Dialog-New Boundary:constructor:'+constructor+':direction', direction)))
           
def BoundaryNewDialogCheck2(constructor, *directions):
    okbutton = gtklogger.findWidget('Dialog-New Boundary:gtk-ok')
    part1 = ((okbutton.get_property('sensitive') == False) and
           chooserCheck('Dialog-New Boundary:constructor:Chooser', ('Point boundary from nodes',
                                                                   'Point boundary from segments',
                                                                   'Point boundary from faces',
                                                                   'Point boundary from elements',
                                                                   'Edge boundary from nodes',
                                                                   'Edge boundary from segments',
                                                                   'Edge boundary from faces',
                                                                   'Face boundary from faces',
                                                                   'Face boundary from elements',)) and
           chooserCheck('Dialog-New Boundary:constructor:'+constructor+':group', ('<selection>',)))
    if not directions:
       part2 = True
    else:
       part2 = chooserCheck('Dialog-New Boundary:constructor:'+constructor+':direction', directions)
    
    return part1 and part2
    
def BoundaryNewDialogCheck3(constructor, group, direction=None):
    okbutton = gtklogger.findWidget('Dialog-New Boundary:gtk-ok')
    return ((okbutton.get_property('sensitive') == False) and
           chooserStateCheck('Dialog-New Boundary:constructor:Chooser', constructor) and
           chooserStateCheck('Dialog-New Boundary:constructor:'+constructor+':group', group) and
           ((direction == None) or chooserStateCheck('Dialog-New Boundary:constructor:'+constructor+':direction', direction)))
           
