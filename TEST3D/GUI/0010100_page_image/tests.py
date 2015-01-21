# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/23 14:35:07 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

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
        base='OOF3D:Image Page')
            and
            sensitizationCheck(
        {'Prev' : 0,
         'OK' : 1,
         'Next' : 0,
         'Undo' : 0,
         'Redo' : 0
        },
        base='OOF3D:Image Page:Pane'
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
        base='OOF3D:Image Page')
            and
            sensitizationCheck(
        {'Prev' : 0,
         'OK' : 1,
         'Next' : 0,
         'Undo' : 1,
         'Redo' : 0
        },
        base='OOF3D:Image Page:Pane'
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
        base='OOF3D:Image Page')
            and
            sensitizationCheck(
        {'Prev' : 0,
         'OK' : 1,
         'Next' : 0,
         'Undo' : 0,
         'Redo' : 1
        },
        base='OOF3D:Image Page:Pane'
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
        base='OOF3D:Image Page')
            and
            sensitizationCheck(
        {'Prev' : 1,
         'OK' : 1,
         'Next' : 0,
         'Undo' : 1,
         'Redo' : 0
        },
        base='OOF3D:Image Page:Pane'
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
        base='OOF3D:Image Page')
            and
            sensitizationCheck(
        {'Prev' : 1,
         'OK' : 1,
         'Next' : 0,
         'Undo' : 1,
         'Redo' : 1
        },
        base='OOF3D:Image Page:Pane'
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
        base='OOF3D:Image Page')
            and
            sensitizationCheck(
        {'Prev' : 1,
         'OK' : 1,
         'Next' : 0,
         'Undo' : 0,
         'Redo' : 1
        },
        base='OOF3D:Image Page:Pane'
        ))

def micro_sensitization():
    return sensitizationCheck(
        {'Microstructure' : 1,
         'New' : 1,
         'NewFromFile' : 1,
         'Rename' : 1,
         'Copy' : 1,
         'Delete' : 1,
         'Save' : 1,
         'Pane:VoxelGroups:New' : 1,
         'Pane:VoxelGroups:Rename' : 1,
         'Pane:VoxelGroups:Copy' : 1,
         'Pane:VoxelGroups:Delete' : 1,
         'Pane:VoxelGroups:Meshable' : 1,
         'Pane:VoxelGroups:Add' : 0,
         'Pane:VoxelGroups:Remove' : 0,
         'Pane:VoxelGroups:Clear' : 1,
         'Pane:VoxelGroups:Info' : 1
         },
        base='OOF3D:Microstructure Page')

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
        base='OOF3D:Image Page')
            and
            sensitizationCheck(
        {'Prev' : 1,
         'OK' : 0,
         'Next' : 0,
         'Undo' : 0,
         'Redo' : 0
        },
        base='OOF3D:Image Page:Pane'
        ))

