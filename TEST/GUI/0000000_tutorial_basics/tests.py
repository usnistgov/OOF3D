# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:10:10 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

# Test functions called by python lines embedded in the gui log file.

# Most import statements are within the test functions so that
# importing this file doesn't affect the import order.

from ooflib.common.IO.GUI import gtklogger
from generics import *

def existence():
    # If this test fails, we're in big trouble.
    return True

def gui_open():
    from ooflib.common import guitop
    return guitop.top() != None
    
def tutorialPageCheck(pageno):
    from ooflib.common.IO.GUI import tutorialsGUI
    return tutorialsGUI.tutorialInProgress.index == pageno

def countMSGroups(msname):
    from ooflib.common.IO import whoville
    ms = whoville.getClass('Microstructure')[msname].getObject()
    return len(ms.groupNames())


def msPageSensitizationCheck0():
    # Check initial sensitization of the MS page
    return sensitizationCheck(
        {'Microstructure' : 0,
         'New' : 1,
         'NewFromImage' : 0,
         'NewFromFile' : 1,
         'Rename' : 0,
         'Copy' : 0,
         'Delete' : 0,
         'Save' : 0,
         'Pane:PixelGroups:New' : 0,
         'Pane:PixelGroups:Rename' : 0,
         'Pane:PixelGroups:Copy' : 0,
         'Pane:PixelGroups:Delete' : 0,
         'Pane:PixelGroups:Meshable' : 0,
         'Pane:PixelGroups:Add' : 0,
         'Pane:PixelGroups:Remove' : 0,
         'Pane:PixelGroups:Clear' : 0,
         'Pane:PixelGroups:Info' : 0
         },
        base='OOF2:Microstructure Page')

def msPageSensitizationCheck1():
    # Check sensitization of the MS page after a Microstructure has
    # been created.
    return sensitizationCheck(
        {'Microstructure' : 1,
         'New' : 1,
         'NewFromImage' : 1,
         'NewFromFile' : 1,
         'Rename' : 1,
         'Copy' : 1,
         'Delete' : 1,
         'Save' : 1,
         'Pane:PixelGroups:New' : 1,
         'Pane:PixelGroups:Rename' : 0,
         'Pane:PixelGroups:Copy' : 0,
         'Pane:PixelGroups:Delete' : 0,
         'Pane:PixelGroups:Meshable' : 0,
         'Pane:PixelGroups:Add' : 0,
         'Pane:PixelGroups:Remove' : 0,
         'Pane:PixelGroups:Clear' : 0,
         'Pane:PixelGroups:Info' : 0
         },
        base='OOF2:Microstructure Page')

def msPageSensitizationCheck2():
    # Check sensitization of the MS page after a Microstructure has
    # been created and groups have been defined.
    return sensitizationCheck(
        {'Microstructure' : 1,
         'New' : 1,
         'NewFromImage' : 1,
         'NewFromFile' : 1,
         'Rename' : 1,
         'Copy' : 1,
         'Delete' : 1,
         'Save' : 1,
         'Pane:PixelGroups:New' : 1,
         'Pane:PixelGroups:Rename' : 1,
         'Pane:PixelGroups:Copy' : 1,
         'Pane:PixelGroups:Delete' : 1,
         'Pane:PixelGroups:Meshable' : 1,
         'Pane:PixelGroups:Add' : 0,
         'Pane:PixelGroups:Remove' : 0,
         'Pane:PixelGroups:Clear' : 1,
         'Pane:PixelGroups:Info' : 1
         },
        base='OOF2:Microstructure Page')
