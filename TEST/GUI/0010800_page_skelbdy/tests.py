# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:11:35 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

from generics import *

def sensitization0():
    return sensitizationCheck({"New" : 0,
                               "Modify" : 0,
                               "Rename" : 0,
                               "Delete" : 0
                               },
                              base="OOF2:Skeleton Boundaries Page:Pane:Boundaries")

def sensitization1():
    return sensitizationCheck({"New" : 1,
                               "Modify" : 0,
                               "Rename" : 0,
                               "Delete" : 0
                               },
                              base="OOF2:Skeleton Boundaries Page:Pane:Boundaries")

def sensitization2():
    return sensitizationCheck({"New" : 1,
                               "Modify" : 1,
                               "Rename" : 1,
                               "Delete" : 1
                               },
                              base="OOF2:Skeleton Boundaries Page:Pane:Boundaries")



def _statusText():
    textview = gtklogger.findWidget(
        'OOF2:Skeleton Boundaries Page:Pane:InfoScroll:status')
    buffer = textview.get_buffer()
    return buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter())
    
def bdyStatusEmpty():
    return _statusText() == "No skeleton selected." and selectedBdy(None)

def bdyStatusNoBdy():
    return _statusText() == "No boundary selected." and selectedBdy(None)

def bdyStatusCheck(name, bdytype, size):
    text = _statusText()
    expected = "Boundary %s:\nType: %s\nSize: %d" % (name, bdytype, size)
    return text == expected

bdylistwidget = \
 'OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList'

def bdyNames(names):
    return chooserCheck(bdylistwidget, names)

def selectedBdy(name):
    if name is not None:
        return chooserListStateCheck(bdylistwidget, [name])
    else:
        return chooserListStateCheck(bdylistwidget, [])

def newBdyOK(sensitive):
    okbutton = gtklogger.findWidget('Dialog-New Boundary:gtk-ok')
    return okbutton.get_property('sensitive') == sensitive

directionwidget = \
                'Dialog-New Boundary:constructor:Edge boundary from %s:direction'
def directionCheck(type, choices):
##    print treeViewColValues(directionwidget%type, 0)
##    print directionwidget%type
    return chooserCheck(directionwidget % type, choices)

def modifyBdyOK(sensitive):
    okbutton = gtklogger.findWidget('Dialog-Boundary modifier:gtk-ok')
    return okbutton.get_property('sensitive') == sensitive
