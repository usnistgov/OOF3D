# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.2 $
# $Author: langer $
# $Date: 2014/09/27 22:34:49 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from generics import *

def sensitization0():
    return sensitizationCheck({'Undo' : 0,
                               'OK' : 0,
                               'Redo' : 0,
                               'Unpin All' : 0,
                               'Invert' : 0
                               },
                              base="OOF3D:Pin Nodes Page:Pane:Modify")

def sensitization1():
    return sensitizationCheck({'Undo' : 0,
                               'OK' : 1,
                               'Redo' : 0,
                               'Unpin All' : 0,
                               'Invert' : 1
                               },
                              base="OOF3D:Pin Nodes Page:Pane:Modify")

def sensitization2():
    return sensitizationCheck({'Undo' : 1,
                               'OK' : 1,
                               'Redo' : 0,
                               'Unpin All' : 1,
                               'Invert' : 1
                               },
                              base="OOF3D:Pin Nodes Page:Pane:Modify")

def sensitization3():
    return sensitizationCheck({'Undo' : 1,
                               'OK' : 1,
                               'Redo' : 0,
                               'Unpin All' : 0,
                               'Invert' : 1
                               },
                              base="OOF3D:Pin Nodes Page:Pane:Modify")

def sensitization4():
    return sensitizationCheck({'Undo' : 1,
                               'OK' : 1,
                               'Redo' : 1,
                               'Unpin All' : 0,
                               'Invert' : 1
                               },
                              base="OOF3D:Pin Nodes Page:Pane:Modify")

def sensitization5():
    return sensitizationCheck({'Undo' : 1,
                               'OK' : 1,
                               'Redo' : 0,
                               'Unpin All' : 0,
                               'Invert' : 1
                               },
                              base="OOF3D:Pin Nodes Page:Pane:Modify")

def pinnedNodesSkelCheck(skelname, n):
    from ooflib.common.IO import whoville
    skelctxt = whoville.getClass('Skeleton')[skelname]
    return skelctxt.pinnednodes.npinned() == n

def pinnedNodesCheck(n):
    return pinnedNodesSkelCheck('5color:skeleton', n)
