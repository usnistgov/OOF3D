# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:13:19 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

from generics import *
import sys

def peekedNode():
    from ooflib.common.IO import gfxmanager
    window = gfxmanager.gfxManager.getWindow("Graphics_1")
    toolbox = window.getToolboxByName('Mesh_Info')
    if toolbox.peeker:
        return toolbox.peeker.objects["Node"]


nodelistwidget = "OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Mesh Info:ElementInfo:NodeList"

def nodeListCheck(nodes):
    return chooserCheck(nodelistwidget, nodes)

def peekNodeCheck(nodenumber):
    treeview = gtklogger.findWidget(nodelistwidget)
    selection = treeview.get_selection()
    model, iter = selection.get_selected()
    if iter is None:
        return nodenumber is None and peekedNode() is None
    selectedtext = model[iter][0]
    return (peekedNode().index() == nodenumber and
            int(selectedtext.split()[1]) == nodenumber)

clickwidgets = "OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Mesh Info:Click:"

def nodeMode():
    return (gtklogger.findWidget(clickwidgets+"Node").get_active() and
            not gtklogger.findWidget(clickwidgets+"Element").get_active())

def elementMode():
    return (not gtklogger.findWidget(clickwidgets+"Node").get_active() and
            gtklogger.findWidget(clickwidgets+"Element").get_active())
