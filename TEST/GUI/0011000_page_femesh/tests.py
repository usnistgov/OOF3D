# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:11:38 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

from generics import *

def sensitization0():
    return (sensitizationCheck({"New" : 0,
                                "Rename" : 0,
                                "Copy" : 0,
                                "Delete" : 0,
                                "Save" : 0,
                                "Pane:ElementOps:OK" : 0},
                               base="OOF2:FE Mesh Page")
            and
            sensitizationCheck({"New" : 0,
                                "Rename" : 0,
                                "Edit" : 0,
                                "Copy" : 0,
                                "Info" : 0,
                                "Delete" : 0},
                               base="OOF2:FE Mesh Page:Pane:Subproblems"))

def sensitization1():
    return (sensitizationCheck({"New" : 1,
                               "Rename" : 0,
                               "Copy" : 0,
                               "Delete" : 0,
                               "Save" : 0,
                               "Pane:ElementOps:OK" : 0},
                              base="OOF2:FE Mesh Page")
            and
            sensitizationCheck({"New" : 0,
                                "Rename" : 0,
                                "Edit" : 0,
                                "Copy" : 0,
                                "Info" : 0,
                                "Delete" : 0},
                               base="OOF2:FE Mesh Page:Pane:Subproblems"))

def sensitization2():
    return (sensitizationCheck({"New" : 1,
                               "Rename" : 1,
                               "Copy" : 1,
                               "Delete" : 1,
                               "Save" : 1,
                               "Pane:ElementOps:OK" : 0},
                              base="OOF2:FE Mesh Page")
            and
            sensitizationCheck({"New" : 1,
                                "Rename" : 0,
                                "Edit" : 0,
                                "Copy" : 1,
                                "Info" : 1,
                                "Delete" : 0},
                               base="OOF2:FE Mesh Page:Pane:Subproblems"))

def sensitization3():
    return (sensitizationCheck({"New" : 1,
                               "Rename" : 1,
                               "Copy" : 1,
                               "Delete" : 1,
                               "Save" : 1,
                               "Pane:ElementOps:OK" : 1},
                              base="OOF2:FE Mesh Page")
            and
            sensitizationCheck({"New" : 1,
                                "Rename" : 0,
                                "Edit" : 0,
                                "Copy" : 1,
                                "Info" : 1,
                                "Delete" : 0},
                               base="OOF2:FE Mesh Page:Pane:Subproblems"))

def sensitization4():
    return (sensitizationCheck({"New" : 1,
                               "Rename" : 1,
                               "Copy" : 1,
                               "Delete" : 1,
                               "Save" : 1,
                               "Pane:ElementOps:OK" : 1},
                              base="OOF2:FE Mesh Page")
            and
            sensitizationCheck({"New" : 1,
                                "Rename" : 1,
                                "Edit" : 1,
                                "Copy" : 1,
                                "Info" : 1,
                                "Delete" : 1},
                               base="OOF2:FE Mesh Page:Pane:Subproblems"))

def sensitization5():
    return (sensitizationCheck({"New" : 1,
                               "Rename" : 1,
                               "Copy" : 1,
                               "Delete" : 1,
                               "Save" : 1,
                               "Pane:ElementOps:OK" : 0},
                              base="OOF2:FE Mesh Page")
            and
            sensitizationCheck({"New" : 1,
                                "Rename" : 1,
                                "Edit" : 1,
                                "Copy" : 1,
                                "Info" : 1,
                                "Delete" : 1},
                               base="OOF2:FE Mesh Page:Pane:Subproblems"))

def sensitization6():
    return (sensitizationCheck({"New" : 1,
                               "Rename" : 1,
                               "Copy" : 1,
                               "Delete" : 1,
                               "Save" : 1,
                               "Pane:ElementOps:OK" : 0},
                              base="OOF2:FE Mesh Page")
            and
            sensitizationCheck({"New" : 1,
                                "Rename" : 0,
                                "Edit" : 0,
                                "Copy" : 0,
                                "Info" : 0,
                                "Delete" : 0},
                               base="OOF2:FE Mesh Page:Pane:Subproblems"))

def sensitization7():
    return (sensitizationCheck({"New" : 1,
                               "Rename" : 1,
                               "Copy" : 1,
                               "Delete" : 1,
                               "Save" : 1,
                               "Pane:ElementOps:OK" : 1},
                              base="OOF2:FE Mesh Page")
            and
            sensitizationCheck({"New" : 1,
                                "Rename" : 0,
                                "Edit" : 0,
                                "Copy" : 0,
                                "Info" : 0,
                                "Delete" : 0},
                               base="OOF2:FE Mesh Page:Pane:Subproblems"))

def groupChooserCheck(*names):
    return chooserCheck(
        'OOF2:FE Mesh Page:Pane:ElementOps:Method:Assign Material:target:Element Group:group',
        names)

def subproblemNameCheck(*names):
    return chooserCheck(
       'OOF2:FE Mesh Page:Pane:Subproblems:subprobChooserScroll:subprobChooser',
       names)

def selectedSubproblem(name):
    if name:
        return chooserListStateCheck(
      'OOF2:FE Mesh Page:Pane:Subproblems:subprobChooserScroll:subprobChooser',
      [name])
    else:
        return chooserListStateCheck(
      'OOF2:FE Mesh Page:Pane:Subproblems:subprobChooserScroll:subprobChooser',
      [])
def newSubproblemOK():
    return is_sensitive("Create a new subproblem:gtk-ok")
