# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:12:02 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

from generics import *

def sensitive(state):
    return sensitizationCheck({"OOF2:Solver Page:Solve" : state})

def statusTail(text):
    return gtkTextviewTail("OOF2:Solver Page:StatusScroll:Status", text)

def statusHead(text):
    return gtkTextviewHead("OOF2:Solver Page:StatusScroll:Status", text)

def statusLine(line, text):
    return gtkTextviewLine("OOF2:Solver Page:StatusScroll:Status", line, text)
