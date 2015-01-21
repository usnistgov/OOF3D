# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/23 14:35:11 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from generics import *

def _getStatusText():
    textviewer = gtklogger.findWidget('OOF3D:Voxel Selection Page:Pane:DataScroll:DataView')
    buffer = textviewer.get_buffer()
    return buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter())
    
def voxelSelectionPageStatusCheck(nvox, total):
    return _getStatusText() == "%d of %d voxels selected" % (nvox, total)

def voxelSelectionPageNoMSCheck():
    return _getStatusText() == "No Microstructure selected."

def sensitization0():
    return (sensitizationCheck(
        {'OOF3D:Voxel Selection Page:Microstructure' : 0})
            and
            sensitizationCheck(
        {'Prev' : 0,
         'OK' : 0,
         'Next' : 0,
         'Undo' : 0,
         'Redo' : 0,
         'Clear' : 0
        },
        base="OOF3D:Voxel Selection Page:Pane:SelectionModification"))

def sensitization1():
    return (sensitizationCheck(
        {'OOF3D:Voxel Selection Page:Microstructure' : 1})
            and
            sensitizationCheck(
        {'Prev' : 0,
         'OK' : 1,
         'Next' : 0,
         'Undo' : 0,
         'Redo' : 0,
         'Clear' : 0
        },
        base="OOF3D:Voxel Selection Page:Pane:SelectionModification"))

def sensitization2():
    return (sensitizationCheck(
        {'OOF3D:Voxel Selection Page:Microstructure' : 1})
            and
            sensitizationCheck(
        {'Prev' : 0,
         'OK' : 1,
         'Next' : 0,
         'Undo' : 1,
         'Redo' : 0,
         'Clear' : 1
        },
        base="OOF3D:Voxel Selection Page:Pane:SelectionModification"))

def sensitization3():
    return (sensitizationCheck(
        {'OOF3D:Voxel Selection Page:Microstructure' : 1})
            and
            sensitizationCheck(
        {'Prev' : 0,
         'OK' : 1,
         'Next' : 0,
         'Undo' : 1,
         'Redo' : 1,
         'Clear' : 1
        },
        base="OOF3D:Voxel Selection Page:Pane:SelectionModification"))

def sensitization4():
    return (sensitizationCheck(
        {'OOF3D:Voxel Selection Page:Microstructure' : 1})
            and
            sensitizationCheck(
        {'Prev' : 0,
         'OK' : 1,
         'Next' : 0,
         'Undo' : 1,
         'Redo' : 0,
         'Clear' : 0
        },
        base="OOF3D:Voxel Selection Page:Pane:SelectionModification"))

def sensitization5():
    return (sensitizationCheck(
        {'OOF3D:Voxel Selection Page:Microstructure' : 1})
            and
            sensitizationCheck(
        {'Prev' : 1,
         'OK' : 1,
         'Next' : 0,
         'Undo' : 1,
         'Redo' : 0,
         'Clear' : 0
        },
        base="OOF3D:Voxel Selection Page:Pane:SelectionModification"))

def sensitization6():
    return (sensitizationCheck(
        {'OOF3D:Voxel Selection Page:Microstructure' : 1})
            and
            sensitizationCheck(
        {'Prev' : 1,
         'OK' : 1,
         'Next' : 0,
         'Undo' : 1,
         'Redo' : 0,
         'Clear' : 1
        },
        base="OOF3D:Voxel Selection Page:Pane:SelectionModification"))
