# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:11:27 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

from generics import *
from skelseltests import *

def nodeSelectionCheck(nodes):
    return skeletonNodeSelectionCheck('microstructure:skeleton', nodes)

def nodeSelectionCheck2(nodes):
    return skeletonNodeSelectionCheck('microstructure:skeleton<2>', nodes)

def sensitization0():
    return (sensitizationCheck({'New': 1,
                                'Rename': 0,
                                'Copy': 0,
                                'Delete' : 0,
                                'Add': 0,
                                'Remove': 0,
                                'Clear': 0,
                                'Info': 0
                                },
                               base="OOF2:Skeleton Selection Page:Pane:Groups")
            and
            historySensitizationCheck('Element', prev=0, ok=1, next=0)
            and
            sensitizationCheck({'Undo' : 0,
                                'Redo' : 0,
                                'Clear': 0,
                                'Invert' : 1
                                },
                               base="OOF2:Skeleton Selection Page:Pane:Selection")
            )

def sensitization1():
    return (sensitizationCheck({'New': 1,
                                'Rename': 0,
                                'Copy': 0,
                                'Delete' : 0,
                                'Add': 0,
                                'Remove': 0,
                                'Clear': 0,
                                'Info': 0
                                },
                               base="OOF2:Skeleton Selection Page:Pane:Groups")
            and
            historySensitizationCheck('Element', prev=0, ok=1, next=0)
            and
            sensitizationCheck({'Undo' : 1,
                                'Redo' : 0,
                                'Clear': 1,
                                'Invert' : 1
                                },
                               base="OOF2:Skeleton Selection Page:Pane:Selection")
            )

def sensitization2():
    return (sensitizationCheck({'New': 1,
                                'Rename': 1,
                                'Copy': 1,
                                'Delete' : 1,
                                'Add': 1,
                                'Remove': 1,
                                'Clear': 0,
                                'Info': 1
                                },
                               base="OOF2:Skeleton Selection Page:Pane:Groups")
            and
            historySensitizationCheck('Node', prev=0, ok=1, next=0)
            and
            sensitizationCheck({'Undo' : 1,
                                'Redo' : 0,
                                'Clear': 1,
                                'Invert' : 1
                                },
                               base="OOF2:Skeleton Selection Page:Pane:Selection")
            )

def sensitization3():
    return (sensitizationCheck({'New': 1,
                                'Rename': 1,
                                'Copy': 1,
                                'Delete' : 1,
                                'Add': 1,
                                'Remove': 1,
                                'Clear': 1,
                                'Info': 1
                                },
                               base="OOF2:Skeleton Selection Page:Pane:Groups")
            and
            historySensitizationCheck('Node', prev=1, ok=1, next=0)
            and
            sensitizationCheck({'Undo' : 1,
                                'Redo' : 1,
                                'Clear': 1,
                                'Invert' : 1
                                },
                               base="OOF2:Skeleton Selection Page:Pane:Selection")
            )


def sensitization4():
    return (sensitizationCheck({'New': 1,
                                'Rename': 1,
                                'Copy': 1,
                                'Delete' : 1,
                                'Add': 0,
                                'Remove': 0,
                                'Clear': 1,
                                'Info': 1
                                },
                               base="OOF2:Skeleton Selection Page:Pane:Groups")
            and
            historySensitizationCheck('Node', prev=1, ok=1, next=0)
            and
            sensitizationCheck({'Undo' : 0,
                                'Redo' : 1,
                                'Clear': 0,
                                'Invert' : 1
                                },
                               base="OOF2:Skeleton Selection Page:Pane:Selection")
            )

def sensitization5():
    return (sensitizationCheck({'New': 0,
                                'Rename': 0,
                                'Copy': 0,
                                'Delete' : 0,
                                'Add': 0,
                                'Remove': 0,
                                'Clear': 0,
                                'Info': 0
                                },
                               base="OOF2:Skeleton Selection Page:Pane:Groups")
            and
            historySensitizationCheck('Node', prev=1, ok=0, next=0)
            and
            sensitizationCheck({'Undo' : 0,
                                'Redo' : 0,
                                'Clear': 0,
                                'Invert' : 0
                                },
                               base="OOF2:Skeleton Selection Page:Pane:Selection")
            )

