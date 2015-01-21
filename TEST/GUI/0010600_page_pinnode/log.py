checkpoint toplevel widget mapped OOF2 Activity Viewer
# -*- python -*-
# $RCSfile: log.py,v $
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

import tests
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Pin Nodes')
assert tests.sensitization0()
findWidget('OOF2:Pin Nodes Page:Pane').set_position(233)
findMenu(findWidget('OOF2:MenuBar'), 'File:Load:Data').activate()
checkpoint toplevel widget mapped Dialog-Data
findWidget('Dialog-Data').resize(194, 72)
findWidget('Dialog-Data:filename').set_text('.')
findWidget('Dialog-Data:filename').set_text('..')
findWidget('Dialog-Data:filename').set_text('../')
findWidget('Dialog-Data:filename').set_text('../.')
findWidget('Dialog-Data:filename').set_text('../..')
findWidget('Dialog-Data:filename').set_text('../../')
findWidget('Dialog-Data:filename').set_text('../../e')
findWidget('Dialog-Data:filename').set_text('../../ex')
findWidget('Dialog-Data:filename').set_text('../../exa')
findWidget('Dialog-Data:filename').set_text('../../exam')
findWidget('Dialog-Data:filename').set_text('../../examp')
findWidget('Dialog-Data:filename').set_text('../../exampl')
findWidget('Dialog-Data:filename').set_text('../../example')
findWidget('Dialog-Data:filename').set_text('../../examples')
findWidget('Dialog-Data:filename').set_text('../../examples/')
findWidget('Dialog-Data:filename').set_text('../../examples/t')
findWidget('Dialog-Data:filename').set_text('../../examples/tw')
findWidget('Dialog-Data:filename').set_text('../../examples/two')
findWidget('Dialog-Data:filename').set_text('../../examples/two_')
findWidget('Dialog-Data:filename').set_text('../../examples/two_c')
findWidget('Dialog-Data:filename').set_text('../../examples/two_ci')
findWidget('Dialog-Data:filename').set_text('../../examples/two_cir')
findWidget('Dialog-Data:filename').set_text('../../examples/two_circ')
findWidget('Dialog-Data:filename').set_text('../../examples/two_circl')
findWidget('Dialog-Data:filename').set_text('../../examples/two_circle')
findWidget('Dialog-Data:filename').set_text('../../examples/two_circles')
findWidget('Dialog-Data:filename').set_text('../../examples/two_circles.')
findWidget('Dialog-Data:filename').set_text('../../examples/two_circles.s')
findWidget('Dialog-Data:filename').set_text('../../examples/two_circles.sk')
findWidget('Dialog-Data:filename').set_text('../../examples/two_circles.ske')
findWidget('Dialog-Data:filename').set_text('../../examples/two_circles.skel')
findWidget('Dialog-Data:filename').set_text('../../examples/two_circles.skele')
findWidget('Dialog-Data:filename').set_text('../../examples/two_circles.skelet')
findWidget('Dialog-Data:filename').set_text('../../examples/two_circles.skeleto')
findWidget('Dialog-Data:filename').set_text('../../examples/two_circles.skeleton')
findWidget('Dialog-Data:gtk-ok').clicked()
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized
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
checkpoint interface page updated
findWidget('OOF2 Activity Viewer').resize(400, 300)
findWidget('OOF2:Pin Nodes Page:Pane').set_position(233)
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint meshable button set
checkpoint meshable button set
checkpoint meshable button set
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint mesh bdy page updated
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint boundary page updated
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint OOF.File.Load.Data
checkpoint_count("boundary page updated")
assert tests.sensitization1()
findMenu(findWidget('OOF2:MenuBar'), 'Windows:Graphics:New').activate()
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint toplevel widget mapped OOF2 Graphics 1
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(693)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
checkpoint OOF.Windows.Graphics.New
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(693)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1').resize(800, 400)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(693)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1').resize(800, 400)
assert tests.pinnedNodesCheck(0)
findWidget('OOF2:Pin Nodes Page:Pane:Modify:Invert').clicked()
findWidget('OOF2:Pin Nodes Page:Pane').set_position(233)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint OOF.Skeleton.PinNodes.Invert
assert tests.pinnedNodesCheck(617)
assert tests.sensitization2()
findWidget('OOF2:Pin Nodes Page:Pane:Modify:Unpin All').clicked()
findWidget('OOF2:Pin Nodes Page:Pane').set_position(233)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint OOF.Skeleton.PinNodes.UnpinAll
assert tests.pinnedNodesCheck(0)
assert tests.sensitization3()
findWidget('OOF2:Pin Nodes Page:Pane:Modify:Undo').clicked()
findWidget('OOF2:Pin Nodes Page:Pane').set_position(233)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint OOF.Skeleton.PinNodes.Undo
assert tests.pinnedNodesCheck(617)
assert tests.sensitization4()
findWidget('OOF2:Pin Nodes Page:Pane:Modify:Undo').clicked()
findWidget('OOF2:Pin Nodes Page:Pane').set_position(233)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint OOF.Skeleton.PinNodes.Undo
assert tests.pinnedNodesCheck(0)
assert tests.sensitization5()
findWidget('OOF2:Pin Nodes Page:Pane:Modify:Redo').clicked()
findWidget('OOF2:Pin Nodes Page:Pane').set_position(233)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint OOF.Skeleton.PinNodes.Redo
assert tests.pinnedNodesCheck(617)
assert tests.sensitization4()
setComboBox(findWidget('OOF2:Pin Nodes Page:Pane:Modify:Method:Chooser'), 'Pin Internal Boundary Nodes')
findWidget('OOF2:Pin Nodes Page:Pane:Modify:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint OOF.Skeleton.PinNodes.Pin_Internal_Boundary_Nodes
assert tests.pinnedNodesCheck(617)
findWidget('OOF2:Pin Nodes Page:Pane:Modify:Unpin All').clicked()
findWidget('OOF2:Pin Nodes Page:Pane').set_position(233)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint OOF.Skeleton.PinNodes.UnpinAll
assert tests.pinnedNodesCheck(0)
findWidget('OOF2:Pin Nodes Page:Pane:Modify:OK').clicked()
findWidget('OOF2:Pin Nodes Page:Pane').set_position(233)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint OOF.Skeleton.PinNodes.Pin_Internal_Boundary_Nodes
assert tests.pinnedNodesCheck(106)
findWidget('OOF2:Pin Nodes Page:Pane:Modify:Undo').clicked()
findWidget('OOF2:Pin Nodes Page:Pane').set_position(233)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint OOF.Skeleton.PinNodes.Undo
assert tests.pinnedNodesCheck(0)
findWidget('OOF2:Pin Nodes Page:Pane:Modify:Redo').clicked()
findWidget('OOF2:Pin Nodes Page:Pane').set_position(233)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint OOF.Skeleton.PinNodes.Redo
assert tests.pinnedNodesCheck(106)
setComboBox(findWidget('OOF2:Pin Nodes Page:Pane:Modify:Method:Chooser'), 'UnPin Node Selection')
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
setComboBox(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBChooser'), 'Skeleton Selection')
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
checkpoint Graphics_1 Element sensitized
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
checkpoint selection info updated
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Select:Element').clicked()
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Select:Node').clicked()
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
setComboBox(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Node:Method:Chooser'), 'Rectangle')
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.4565217391304e+01,y=-8.3260869565217e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.4565217391304e+01,y=-8.2826086956522e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.5000000000000e+01,y=-8.0652173913043e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.5434782608696e+01,y=-7.8478260869565e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.5869565217391e+01,y=-7.7608695652174e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.8043478260870e+01,y=-7.3260869565217e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.0652173913043e+01,y=-6.9347826086957e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.3695652173913e+01,y=-6.4565217391304e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.5869565217391e+01,y=-6.0652173913043e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.8478260869565e+01,y=-5.7608695652174e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.0652173913043e+01,y=-5.5434782608696e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.2391304347826e+01,y=-5.2826086956522e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.3695652173913e+01,y=-5.0652173913043e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.4130434782609e+01,y=-4.9347826086957e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.4565217391304e+01,y=-4.8043478260870e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.5869565217391e+01,y=-4.6739130434783e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.7173913043478e+01,y=-4.5869565217391e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.8478260869565e+01,y=-4.5000000000000e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.0217391304348e+01,y=-4.3695652173913e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.2391304347826e+01,y=-4.1521739130435e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.4565217391304e+01,y=-4.0217391304348e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.7608695652174e+01,y=-3.8043478260870e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.0217391304348e+01,y=-3.5434782608696e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.2826086956522e+01,y=-3.2826086956522e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.3260869565217e+01,y=-3.2391304347826e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.4565217391304e+01,y=-3.1956521739130e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.4565217391304e+01,y=-3.2391304347826e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.5000000000000e+01,y=-3.2391304347826e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.5000000000000e+01,y=-3.2826086956522e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.5434782608696e+01,y=-3.3695652173913e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.5869565217391e+01,y=-3.5000000000000e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.5869565217391e+01,y=-3.6304347826087e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.6304347826087e+01,y=-3.7173913043478e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.6739130434783e+01,y=-3.8478260869565e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.7173913043478e+01,y=-3.9347826086957e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.7608695652174e+01,y=-3.9782608695652e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8043478260870e+01,y=-4.0217391304348e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8043478260870e+01,y=-4.0652173913043e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8913043478261e+01,y=-4.0652173913043e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.9347826086957e+01,y=-4.0652173913043e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.9347826086957e+01,y=-4.1086956521739e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.9347826086957e+01,y=-4.1521739130435e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.9347826086957e+01,y=-4.1956521739130e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 8.9347826086957e+01,y=-4.1956521739130e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
checkpoint Graphics_1 Node sensitized
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Rectangle
findWidget('OOF2:Pin Nodes Page:Pane:Modify:OK').clicked()
findWidget('OOF2:Pin Nodes Page:Pane').set_position(233)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint OOF.Skeleton.PinNodes.UnPin_Node_Selection
assert tests.pinnedNodesCheck(70)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Node:Clear').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Clear
setComboBox(findWidget('OOF2:Pin Nodes Page:Pane:Modify:Method:Chooser'), 'Pin Node Selection')
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Node:Undo').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Undo
findWidget('OOF2:Pin Nodes Page:Pane:Modify:OK').clicked()
findWidget('OOF2:Pin Nodes Page:Pane').set_position(233)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint OOF.Skeleton.PinNodes.Pin_Node_Selection
assert tests.pinnedNodesCheck(211)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Node:Clear').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint selection info updated
checkpoint Graphics_1 Node sensitized
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Clear
findWidget('OOF2:Pin Nodes Page:Pane:Modify:Unpin All').clicked()
findWidget('OOF2:Pin Nodes Page:Pane').set_position(233)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint OOF.Skeleton.PinNodes.UnpinAll
assert tests.pinnedNodesCheck(0)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Select:Node').clicked()
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Select:Segment').clicked()
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
checkpoint Graphics_1 Node sensitized
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint selection info updated
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.5434782608696e+01,y=-8.8913043478261e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.5434782608696e+01,y=-8.8913043478261e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint Graphics_1 Segment sensitized
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
setComboBox(findWidget('OOF2:Pin Nodes Page:Pane:Modify:Method:Chooser'), 'Pin Selected Segments')
findWidget('OOF2:Pin Nodes Page:Pane:Modify:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint OOF.Skeleton.PinNodes.Pin_Selected_Segments
assert tests.pinnedNodesCheck(2)
setComboBox(findWidget('OOF2:Pin Nodes Page:Pane:Modify:Method:Chooser'), 'Pin Selected Elements')
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Select:Segment').clicked()
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Select:Element').clicked()
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 7.1739130434783e+00,y=-8.1956521739130e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 7.1739130434783e+00,y=-8.1956521739130e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Element sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint Graphics_1 Element sensitized
checkpoint skeleton selection page updated
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.Single_Element
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Pin Nodes Page:Pane:Modify:OK').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint OOF.Skeleton.PinNodes.Pin_Selected_Elements
assert tests.pinnedNodesCheck(6)
findWidget('OOF2:Pin Nodes Page:Pane:Modify:Invert').clicked()
findWidget('OOF2:Pin Nodes Page:Pane').set_position(233)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint OOF.Skeleton.PinNodes.Invert
assert tests.pinnedNodesCheck(611)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton')
findWidget('OOF2').resize(593, 434)
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
findWidget('OOF2:Skeleton Page:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(194, 94)
checkpoint skeleton page sensitized
findWidget('Questioner:gtk-cancel').clicked()
findWidget('OOF2:Skeleton Page:New').clicked()
checkpoint toplevel widget mapped Dialog-New skeleton
findWidget('Dialog-New skeleton').resize(334, 152)
findWidget('Dialog-New skeleton:gtk-ok').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2:Pin Nodes Page:Pane').set_position(276)
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Pin Nodes Page:Pane').set_position(276)
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint Graphics_1 Element sensitized
checkpoint skeleton selection page updated
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint mesh bdy page updated
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Skeleton.New
assert tests.chooserStateCheck('OOF2:Pin Nodes Page:Skeleton', 'skeleton')
assert tests.chooserCheck('OOF2:Pin Nodes Page:Skeleton', ['skeleton', 'skeleton<2>'])
setComboBox(findWidget('OOF2:Pin Nodes Page:Skeleton'), 'skeleton<2>')
assert tests.sensitization1()
setComboBox(findWidget('OOF2:Pin Nodes Page:Skeleton'), 'skeleton')
findWidget('OOF2:Pin Nodes Page:Pane').set_position(276)
setComboBox(findWidget('OOF2:Pin Nodes Page:Skeleton'), 'skeleton<2>')
findWidget('OOF2:Pin Nodes Page:Pane').set_position(276)
findWidget('OOF2:Navigation:Prev').clicked()
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
findWidget('OOF2:Skeleton Page:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(220, 94)
findWidget('Questioner:gtk-ok').clicked()
checkpoint skeleton page sensitized
checkpoint skeleton page sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
checkpoint Graphics_1 Element sensitized
checkpoint mesh bdy page updated
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
checkpoint skeleton page sensitized
checkpoint OOF.Skeleton.Delete
findWidget('OOF2:Navigation:Next').clicked()
assert tests.chooserCheck('OOF2:Pin Nodes Page:Skeleton', ['skeleton'])
assert tests.sensitization2()
findWidget('OOF2:Pin Nodes Page:Pane').set_position(276)
findWidget('OOF2:Navigation:Prev').clicked()
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
findWidget('OOF2:Skeleton Page:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(194, 94)
findWidget('Questioner:gtk-ok').clicked()
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox writable changed
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
checkpoint Graphics_1 Element sensitized
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
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
checkpoint skeleton page sensitized
checkpoint skeleton page sensitized
checkpoint OOF.Skeleton.Delete
findWidget('OOF2:Navigation:Next').clicked()
assert tests.chooserCheck('OOF2:Pin Nodes Page:Skeleton', [])
assert tests.sensitization0()
findWidget('OOF2:Pin Nodes Page:Pane').set_position(276)
findMenu(findWidget('OOF2:MenuBar'), 'File:Quit').activate()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(358, 94)
findWidget('Questioner:gtk-cancel').clicked()
findMenu(findWidget('OOF2:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(194, 72)
findWidget('Dialog-Python_Log:filename').set_text('p')
findWidget('Dialog-Python_Log:filename').set_text('pi')
findWidget('Dialog-Python_Log:filename').set_text('pin')
findWidget('Dialog-Python_Log:filename').set_text('pinn')
findWidget('Dialog-Python_Log:filename').set_text('pinno')
findWidget('Dialog-Python_Log:filename').set_text('pinnod')
findWidget('Dialog-Python_Log:filename').set_text('pinnode')
findWidget('Dialog-Python_Log:filename').set_text('pinnode.')
findWidget('Dialog-Python_Log:filename').set_text('pinnode.l')
findWidget('Dialog-Python_Log:filename').set_text('pinnode.lo')
findWidget('Dialog-Python_Log:filename').set_text('pinnode.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('pinnode.log')
findMenu(findWidget('OOF2:MenuBar'), 'File:Quit').activate()
