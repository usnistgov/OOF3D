# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:11:21 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

from generics import *

def sensitization0():
    return sensitizationCheck({'Undo' : 0,
                               'OK' : 0,
                               'Redo' : 0,
                               'Unpin All' : 0,
                               'Invert' : 0
                               },
                              base="OOF2:Pin Nodes Page:Pane:Modify")

def sensitization1():
    return sensitizationCheck({'Undo' : 0,
                               'OK' : 1,
                               'Redo' : 0,
                               'Unpin All' : 0,
                               'Invert' : 1
                               },
                              base="OOF2:Pin Nodes Page:Pane:Modify")

def sensitization2():
    return sensitizationCheck({'Undo' : 1,
                               'OK' : 1,
                               'Redo' : 0,
                               'Unpin All' : 1,
                               'Invert' : 1
                               },
                              base="OOF2:Pin Nodes Page:Pane:Modify")

def sensitization3():
    return sensitizationCheck({'Undo' : 1,
                               'OK' : 1,
                               'Redo' : 0,
                               'Unpin All' : 0,
                               'Invert' : 1
                               },
                              base="OOF2:Pin Nodes Page:Pane:Modify")

def sensitization4():
    return sensitizationCheck({'Undo' : 1,
                               'OK' : 1,
                               'Redo' : 1,
                               'Unpin All' : 1,
                               'Invert' : 1
                               },
                              base="OOF2:Pin Nodes Page:Pane:Modify")

def sensitization5():
    return sensitizationCheck({'Undo' : 0,
                               'OK' : 1,
                               'Redo' : 1,
                               'Unpin All' : 0,
                               'Invert' : 1
                               },
                              base="OOF2:Pin Nodes Page:Pane:Modify")

def pinnedNodesSkelCheck(skelname, n):
    from ooflib.common.IO import whoville
    skelctxt = whoville.getClass('Skeleton')[skelname]
    return skelctxt.pinnednodes.npinned() == n

def pinnedNodesCheck(n):
    return pinnedNodesSkelCheck('two_circles.png:skeleton', n)
