# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:10:56 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

from generics import *

def sensitization0():
    return (sensitizationCheck(
        {'Microstructure' : 1,
         'Image' : 1,
         'Load' : 1,
         'Copy' : 1,
         'Rename' : 1,
         'Delete' : 1,
         'Save' : 1,
         'Group' : 1
        },
        base='OOF2:Image Page')
            and
            sensitizationCheck(
        {'Prev' : 0,
         'OK' : 1,
         'Next' : 0,
         'Undo' : 0,
         'Redo' : 0
        },
        base='OOF2:Image Page:Pane'
        ))

def sensitization1():
    return (sensitizationCheck(
        {'Microstructure' : 1,
         'Image' : 1,
         'Load' : 1,
         'Copy' : 1,
         'Rename' : 1,
         'Delete' : 1,
         'Save' : 1,
         'Group' : 1
        },
        base='OOF2:Image Page')
            and
            sensitizationCheck(
        {'Prev' : 0,
         'OK' : 1,
         'Next' : 0,
         'Undo' : 1,
         'Redo' : 0
        },
        base='OOF2:Image Page:Pane'
        ))

def sensitization2():
    return (sensitizationCheck(
        {'Microstructure' : 1,
         'Image' : 1,
         'Load' : 1,
         'Copy' : 1,
         'Rename' : 1,
         'Delete' : 1,
         'Save' : 1,
         'Group' : 1
        },
        base='OOF2:Image Page')
            and
            sensitizationCheck(
        {'Prev' : 0,
         'OK' : 1,
         'Next' : 0,
         'Undo' : 0,
         'Redo' : 1
        },
        base='OOF2:Image Page:Pane'
        ))

def sensitization3():
    return (sensitizationCheck(
        {'Microstructure' : 1,
         'Image' : 1,
         'Load' : 1,
         'Copy' : 1,
         'Rename' : 1,
         'Delete' : 1,
         'Save' : 1,
         'Group' : 1
        },
        base='OOF2:Image Page')
            and
            sensitizationCheck(
        {'Prev' : 1,
         'OK' : 1,
         'Next' : 0,
         'Undo' : 1,
         'Redo' : 0
        },
        base='OOF2:Image Page:Pane'
        ))

def sensitization4():
    return (sensitizationCheck(
        {'Microstructure' : 1,
         'Image' : 1,
         'Load' : 1,
         'Copy' : 1,
         'Rename' : 1,
         'Delete' : 1,
         'Save' : 1,
         'Group' : 1
        },
        base='OOF2:Image Page')
            and
            sensitizationCheck(
        {'Prev' : 1,
         'OK' : 1,
         'Next' : 0,
         'Undo' : 1,
         'Redo' : 1
        },
        base='OOF2:Image Page:Pane'
        ))

def sensitization5():
    return (sensitizationCheck(
        {'Microstructure' : 1,
         'Image' : 1,
         'Load' : 1,
         'Copy' : 1,
         'Rename' : 1,
         'Delete' : 1,
         'Save' : 1,
         'Group' : 1
        },
        base='OOF2:Image Page')
            and
            sensitizationCheck(
        {'Prev' : 1,
         'OK' : 1,
         'Next' : 0,
         'Undo' : 0,
         'Redo' : 1
        },
        base='OOF2:Image Page:Pane'
        ))

def micro_sensitization():
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

def sensitization6():
    return (sensitizationCheck(
        {'Microstructure' : 1,
         'Image' : 0,
         'Load' : 1,
         'Copy' : 0,
         'Rename' : 0,
         'Delete' : 0,
         'Save' : 0,
         'Group' : 0
        },
        base='OOF2:Image Page')
            and
            sensitizationCheck(
        {'Prev' : 1,
         'OK' : 0,
         'Next' : 0,
         'Undo' : 0,
         'Redo' : 0
        },
        base='OOF2:Image Page:Pane'
        ))

