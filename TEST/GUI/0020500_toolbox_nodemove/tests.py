# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:13:01 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

from generics import *

tbox = "OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Move Nodes"

def sensitivityCheck0():
    return sensitizationCheck(
        {"MoveWith:Keyboard" : 1,
         "MoveWith:Mouse" : 1,
         "AllowIllegal" : 1,
         "Undo" : 0,
         "Move" : 0,
         "Redo": 0},
        base=tbox)

def sensitivityCheck1():
    return sensitizationCheck(
        {"MoveWith:Keyboard" : 1,
         "MoveWith:Mouse" : 1,
         "AllowIllegal" : 1,
         "Undo" : 1,
         "Move" : 0,
         "Redo": 0},
        base=tbox)

def sensitivityCheck2():
    return sensitizationCheck(
        {"MoveWith:Keyboard" : 1,
         "MoveWith:Mouse" : 1,
         "AllowIllegal" : 1,
         "Undo" : 1,
         "Move" : 0,
         "Redo": 1},
        base=tbox)

def sensitivityCheck3():
    return sensitizationCheck(
        {"MoveWith:Keyboard" : 1,
         "MoveWith:Mouse" : 1,
         "AllowIllegal" : 1,
         "Undo" : 0,
         "Move" : 0,
         "Redo": 1},
        base=tbox)

def sensitivityCheck4():
    return sensitizationCheck(
        {"MoveWith:Keyboard" : 1,
         "MoveWith:Mouse" : 1,
         "AllowIllegal" : 1,
         "Undo" : 0,
         "Move" : 1,
         "Redo": 1},
        base=tbox)

def sensitivityCheck5():
    return sensitizationCheck(
        {"MoveWith:Keyboard" : 1,
         "MoveWith:Mouse" : 1,
         "AllowIllegal" : 1,
         "Undo" : 1,
         "Move" : 1,
         "Redo": 0},
        base=tbox)

def sensitivityCheck6():
    return sensitizationCheck(
        {"MoveWith:Keyboard" : 1,
         "MoveWith:Mouse" : 1,
         "AllowIllegal" : 1,
         "Undo" : 1,
         "Move" : 1,
         "Redo": 1},
        base=tbox)


# Check the x, y, shape, and homogeneity values as strings.
def textCompare(x, y, shape, homog):
    return gtkMultiTextCompare({'x':x, 'y':y, 'shape':shape, 'homog':homog},
                               tbox)

# Check the values as floats.
def floatCompare(x, y, shape, homog):
    return gtkMultiFloatCompare({'x':x, 'y':y, 'shape':shape, 'homog':homog},
                               tbox)

# Check x and y as floats, but shape and homogeneity as strings.
def xyshCompare(x, y, shape, homog):
    return (gtkMultiFloatCompare({'x':x, 'y':y}, tbox) and
            gtkMultiTextCompare({'shape':shape, 'homog':homog}, tbox))

def messageCompare(msg):
    text = gtklogger.findWidget(tbox+":Status").get_text()
    ok = text == msg
    if not ok:
        print >> sys.stderr, "Expected:", msg
        print >> sys.stderr, "     Got:", text
    return ok

def mouseMode():
    return (gtklogger.findWidget(tbox+":MoveWith:Mouse").get_active() and not
            gtklogger.findWidget(tbox+":MoveWith:Keyboard").get_active())

def keyboardMode():
    return not mouseMode()

#############

def nIllegalElements():
    from ooflib.common.IO import whoville
    sc = whoville.getClass('Skeleton')['triangle.png:skeleton']
    return sc.getObject().getIllegalCount()

