# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:10:34 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

from generics import *
import sys

def meshInfoNodeTBCheck(winname, index, nodetype, pos):
    indexwidget = gtklogger.findWidget(
        '%s:Pane0:Pane1:Pane2:TBScroll:Mesh Info:NodeInfo:index' % winname)
    typewidget = gtklogger.findWidget(
        '%s:Pane0:Pane1:Pane2:TBScroll:Mesh Info:NodeInfo:type' % winname)
    poswidget = gtklogger.findWidget(
        '%s:Pane0:Pane1:Pane2:TBScroll:Mesh Info:NodeInfo:position' % winname)
    return (index == int(indexwidget.get_text()) and
            nodetype == typewidget.get_text() and
            pos == eval(poswidget.get_text()))

def meshInfoElementTBCheck(winname, index, elemtype, nodelist, material):
    indexwidget = gtklogger.findWidget(
        '%s:Pane0:Pane1:Pane2:TBScroll:Mesh Info:ElementInfo:index' % winname)
    etypewidget = gtklogger.findWidget(
        '%s:Pane0:Pane1:Pane2:TBScroll:Mesh Info:ElementInfo:type' % winname)
    matlwidget = gtklogger.findWidget(
        '%s:Pane0:Pane1:Pane2:TBScroll:Mesh Info:ElementInfo:material'%winname)
    return (index == int(indexwidget.get_text()) and
            elemtype == etypewidget.get_text() and
            material == matlwidget.get_text() and
            chooserCheck(
        '%s:Pane0:Pane1:Pane2:TBScroll:Mesh Info:ElementInfo:NodeList'%winname,
        nodelist))
            
def meshDataViewerCheck(winname, source, mesh, mousex, mousey, **kwargs):
    meshwidget = gtklogger.findWidget('%s:ViewSource:meshname' % winname)
    xwidget = gtklogger.findWidget('%s:ViewSource:x' % winname)
    ywidget = gtklogger.findWidget('%s:ViewSource:y' % winname)
    ok = (chooserStateCheck('%s:ViewSource:GfxWindow' % winname, source)
          and mesh == meshwidget.get_text()
          and mousex == eval(xwidget.get_text())
          and mousey == eval(ywidget.get_text()))
    if not ok:
        return False
    for argname, value in kwargs.items():
        widget = gtklogger.findWidget('%s:Data:%s' % (winname, argname))
        if eval(widget.get_text()) != value:
            return False
    return True
