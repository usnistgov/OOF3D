checkpoint toplevel widget mapped OOF2 Activity Viewer
# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:13:18 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov.

## Check that the "peeked" node is drawn correctly, and is consistent
## with the selection in the toolbox's node list.

import tests

setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Microstructure')
findWidget('OOF2:Microstructure Page:Pane').set_position(150)
findWidget('OOF2:Microstructure Page:New').clicked()
checkpoint toplevel widget mapped Dialog-Create Microstructure
findWidget('Dialog-Create Microstructure').resize(314, 168)
findWidget('Dialog-Create Microstructure:gtk-ok').clicked()
findWidget('OOF2:Microstructure Page:Pane').set_position(153)
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint pixel page updated
checkpoint active area status updated
checkpoint mesh bdy page updated
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint boundary page updated
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.Microstructure.New
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Materials')
findWidget('OOF2').resize(684, 350)
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Material:New').clicked()
checkpoint toplevel widget mapped Dialog-New material
findWidget('Dialog-New material').resize(249, 72)
findWidget('Dialog-New material:gtk-ok').clicked()
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Material.New
findWidget('OOF2:Materials Page:Pane:Material:Assign').clicked()
checkpoint toplevel widget mapped Dialog-Assign material material to pixels
findWidget('Dialog-Assign material material to pixels').resize(268, 108)
setComboBox(findWidget('Dialog-Assign material material to pixels:pixels'), '<all>')
findWidget('Dialog-Assign material material to pixels:gtk-ok').clicked()
checkpoint OOF.Material.Assign
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton')
findWidget('OOF2').resize(684, 434)
findWidget('OOF2:Skeleton Page:Pane').set_position(340)
findWidget('OOF2:Skeleton Page:New').clicked()
checkpoint toplevel widget mapped Dialog-New skeleton
checkpoint skeleton page sensitized
findWidget('Dialog-New skeleton').resize(334, 152)
findWidget('Dialog-New skeleton:gtk-ok').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton page sensitized
checkpoint mesh bdy page updated
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint skeleton page sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Skeleton.New
findWidget('OOF2:Skeleton Page:Pane').set_position(340)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'FE Mesh')
findWidget('OOF2').resize(684, 482)
findWidget('OOF2:FE Mesh Page:Pane').set_position(265)
findWidget('OOF2:FE Mesh Page:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new mesh
findWidget('Dialog-Create a new mesh').resize(331, 188)
setComboBox(findWidget('Dialog-Create a new mesh:element_types:Func'), '2')
findWidget('Dialog-Create a new mesh:gtk-ok').clicked()
findWidget('OOF2:FE Mesh Page:Pane').set_position(265)
checkpoint mesh bdy page updated
checkpoint mesh bdy page updated
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Mesh.New
findMenu(findWidget('OOF2:MenuBar'), 'Windows:Graphics:New').activate()
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint toplevel widget mapped OOF2 Graphics 1
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint OOF.Windows.Graphics.New
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(693)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(693)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1').resize(800, 400)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(693)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1').resize(800, 405)
findWidget('OOF2 Graphics 1').resize(797, 439)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(714)
findWidget('OOF2 Graphics 1:Pane0').set_position(317)
findWidget('OOF2 Graphics 1').resize(796, 519)
findWidget('OOF2 Graphics 1').resize(796, 540)
findWidget('OOF2 Graphics 1').resize(797, 543)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(714)
findWidget('OOF2 Graphics 1:Pane0').set_position(421)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(714)
findWidget('OOF2 Graphics 1:Pane0').set_position(421)
setComboBox(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBChooser'), 'Mesh Info')
checkpoint Graphics_1 Mesh Info sensitized
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(714)
findWidget('OOF2 Graphics 1:Pane0').set_position(421)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.9782608695652e-01,y=-1.5869565217391e-01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.9782608695652e-01,y=-1.5869565217391e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Mesh Info sensitized
checkpoint OOF.Graphics_1.Toolbox.Mesh_Info.QueryElement
findWidget('OOF2 Graphics 1:Pane0').set_position(421)
assert tests.elementMode()
assert tests.nodeListCheck(['FuncNode 0 at (0, 0)',                             'FuncNode 25 at (0.125, 0)',                             'FuncNode 1 at (0.25, 0)',                             'FuncNode 26 at (0.25, 0.125)',                             'FuncNode 6 at (0.25, 0.25)',                             'FuncNode 27 at (0.125, 0.25)',                             'FuncNode 5 at (0, 0.25)',                             'FuncNode 28 at (0, 0.125)'])
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.4130434782609e-01,y=-1.5869565217391e-01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.4130434782609e-01,y=-1.5869565217391e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Mesh Info sensitized
checkpoint OOF.Graphics_1.Toolbox.Mesh_Info.QueryElement
findWidget('OOF2 Graphics 1:Pane0').set_position(421)
assert tests.nodeListCheck(['FuncNode 1 at (0.25, 0)',                             'FuncNode 29 at (0.375, 0)',                             'FuncNode 2 at (0.5, 0)',                             'FuncNode 30 at (0.5, 0.125)',                             'FuncNode 7 at (0.5, 0.25)',                             'FuncNode 31 at (0.375, 0.25)',                             'FuncNode 6 at (0.25, 0.25)',                             'FuncNode 26 at (0.25, 0.125)'])
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 6.8913043478261e-01,y=-1.9347826086957e-01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 6.8913043478261e-01,y=-1.9347826086957e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Mesh Info sensitized
checkpoint OOF.Graphics_1.Toolbox.Mesh_Info.QueryElement
findWidget('OOF2 Graphics 1:Pane0').set_position(421)
assert tests.nodeListCheck(['FuncNode 2 at (0.5, 0)',                             'FuncNode 32 at (0.625, 0)',                             'FuncNode 3 at (0.75, 0)',                             'FuncNode 33 at (0.75, 0.125)',                             'FuncNode 8 at (0.75, 0.25)',                             'FuncNode 34 at (0.625, 0.25)',                             'FuncNode 7 at (0.5, 0.25)',                             'FuncNode 30 at (0.5, 0.125)'])
assert tests.peekNodeCheck(None)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Mesh Info:ElementInfo:NodeList').get_selection().select_path((1,))
assert tests.peekNodeCheck(32)
findWidget('OOF2 Graphics 1:Pane0').set_position(421)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Mesh Info:ElementInfo:NodeList').get_selection().select_path((0,))
assert tests.peekNodeCheck(2)
findWidget('OOF2 Graphics 1:Pane0').set_position(421)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Mesh Info:ElementInfo:NodeList').get_selection().select_path((4,))
assert tests.peekNodeCheck(8)
findWidget('OOF2 Graphics 1:Pane0').set_position(421)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 6.8478260869565e-01,y=-3.2826086956522e-01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 6.8478260869565e-01,y=-3.2826086956522e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Mesh Info sensitized
checkpoint OOF.Graphics_1.Toolbox.Mesh_Info.QueryElement
findWidget('OOF2 Graphics 1:Pane0').set_position(421)
assert tests.nodeListCheck(['FuncNode 7 at (0.5, 0.25)',                             'FuncNode 34 at (0.625, 0.25)',                             'FuncNode 8 at (0.75, 0.25)',                             'FuncNode 43 at (0.75, 0.375)',                             'FuncNode 13 at (0.75, 0.5)',                             'FuncNode 44 at (0.625, 0.5)',                             'FuncNode 12 at (0.5, 0.5)',                             'FuncNode 41 at (0.5, 0.375)'])
assert tests.peekNodeCheck(8)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Mesh Info:ElementInfo:NodeList').get_selection().select_path((3,))
assert tests.peekNodeCheck(43)
findWidget('OOF2 Graphics 1:Pane0').set_position(421)
tree=findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Mesh Info:ElementInfo:NodeList')
column = tree.get_column(0)
tree.row_activated((3,), column)
checkpoint Graphics_1 Mesh Info sensitized
checkpoint OOF.Graphics_1.Toolbox.Mesh_Info.QueryNode
findWidget('OOF2 Graphics 1:Pane0').set_position(421)
assert tests.nodeMode()
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 7.1956521739130e-01,y=-6.4130434782609e-01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.2391304347826e-01,y=-6.3695652173913e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 7.2391304347826e-01,y=-6.3695652173913e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Mesh Info sensitized
checkpoint OOF.Graphics_1.Toolbox.Mesh_Info.QueryNode
findWidget('OOF2 Graphics 1:Pane0').set_position(421)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.8478260869565e-01,y=-6.2826086956522e-01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.8478260869565e-01,y=-6.2826086956522e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Mesh Info sensitized
checkpoint OOF.Graphics_1.Toolbox.Mesh_Info.QueryNode
findWidget('OOF2 Graphics 1:Pane0').set_position(421)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Mesh Info:Prev').clicked()
checkpoint Graphics_1 Mesh Info sensitized
assert tests.nodeMode()
findWidget('OOF2 Graphics 1:Pane0').set_position(421)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Mesh Info:Prev').clicked()
checkpoint Graphics_1 Mesh Info sensitized
assert tests.nodeMode()
findWidget('OOF2 Graphics 1:Pane0').set_position(421)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Mesh Info:Prev').clicked()
checkpoint Graphics_1 Mesh Info sensitized
assert tests.elementMode()
assert tests.nodeListCheck(['FuncNode 7 at (0.5, 0.25)',                             'FuncNode 34 at (0.625, 0.25)',                             'FuncNode 8 at (0.75, 0.25)',                             'FuncNode 43 at (0.75, 0.375)',                             'FuncNode 13 at (0.75, 0.5)',                             'FuncNode 44 at (0.625, 0.5)',                             'FuncNode 12 at (0.5, 0.5)',                             'FuncNode 41 at (0.5, 0.375)'])
assert tests.peekNodeCheck(43)
findWidget('OOF2 Graphics 1:Pane0').set_position(421)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Mesh Info:Prev').clicked()
checkpoint Graphics_1 Mesh Info sensitized
assert tests.elementMode()
assert tests.nodeListCheck(['FuncNode 2 at (0.5, 0)',                             'FuncNode 32 at (0.625, 0)',                             'FuncNode 3 at (0.75, 0)',                             'FuncNode 33 at (0.75, 0.125)',                             'FuncNode 8 at (0.75, 0.25)',                             'FuncNode 34 at (0.625, 0.25)',                             'FuncNode 7 at (0.5, 0.25)',                             'FuncNode 30 at (0.5, 0.125)'])
assert tests.peekNodeCheck(None)
findWidget('OOF2 Graphics 1:Pane0').set_position(421)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Mesh Info:Prev').clicked()
checkpoint Graphics_1 Mesh Info sensitized
assert tests.elementMode()
assert tests.nodeListCheck(['FuncNode 1 at (0.25, 0)',                             'FuncNode 29 at (0.375, 0)',                             'FuncNode 2 at (0.5, 0)',                             'FuncNode 30 at (0.5, 0.125)',                             'FuncNode 7 at (0.5, 0.25)',                             'FuncNode 31 at (0.375, 0.25)',                             'FuncNode 6 at (0.25, 0.25)',                             'FuncNode 26 at (0.25, 0.125)'])
assert tests.peekNodeCheck(None)
findWidget('OOF2 Graphics 1:Pane0').set_position(421)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Mesh Info:Next').clicked()
checkpoint Graphics_1 Mesh Info sensitized
assert tests.elementMode()
assert tests.nodeListCheck(['FuncNode 2 at (0.5, 0)',                             'FuncNode 32 at (0.625, 0)',                             'FuncNode 3 at (0.75, 0)',                             'FuncNode 33 at (0.75, 0.125)',                             'FuncNode 8 at (0.75, 0.25)',                             'FuncNode 34 at (0.625, 0.25)',                             'FuncNode 7 at (0.5, 0.25)',                             'FuncNode 30 at (0.5, 0.125)'])
assert tests.peekNodeCheck(None)
findWidget('OOF2 Graphics 1:Pane0').set_position(421)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Mesh Info:Next').clicked()
checkpoint Graphics_1 Mesh Info sensitized
assert tests.elementMode()
assert tests.nodeListCheck(['FuncNode 7 at (0.5, 0.25)',                             'FuncNode 34 at (0.625, 0.25)',                             'FuncNode 8 at (0.75, 0.25)',                             'FuncNode 43 at (0.75, 0.375)',                             'FuncNode 13 at (0.75, 0.5)',                             'FuncNode 44 at (0.625, 0.5)',                             'FuncNode 12 at (0.5, 0.5)',                             'FuncNode 41 at (0.5, 0.375)'])
assert tests.peekNodeCheck(None)
findWidget('OOF2 Graphics 1:Pane0').set_position(421)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Mesh Info:Next').clicked()
checkpoint Graphics_1 Mesh Info sensitized
assert tests.nodeMode()
findWidget('OOF2 Graphics 1:Pane0').set_position(421)
findMenu(findWidget('OOF2:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(194, 72)
findWidget('Dialog-Python_Log:filename').set_text('m')
findWidget('Dialog-Python_Log:filename').set_text('me')
findWidget('Dialog-Python_Log:filename').set_text('mes')
findWidget('Dialog-Python_Log:filename').set_text('mesh')
findWidget('Dialog-Python_Log:filename').set_text('meshi')
findWidget('Dialog-Python_Log:filename').set_text('meshin')
findWidget('Dialog-Python_Log:filename').set_text('meshinf')
findWidget('Dialog-Python_Log:filename').set_text('meshinfo')
findWidget('Dialog-Python_Log:filename').set_text('meshinfo.')
findWidget('Dialog-Python_Log:filename').set_text('meshinfo.l')
findWidget('Dialog-Python_Log:filename').set_text('meshinfo.lo')
findWidget('Dialog-Python_Log:filename').set_text('meshinfo.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('meshinfo.log')
findMenu(findWidget('OOF2:MenuBar'), 'File:Quit').activate()
