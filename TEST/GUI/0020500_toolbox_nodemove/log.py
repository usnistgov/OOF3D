checkpoint toplevel widget mapped OOF2 Activity Viewer
# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:13:00 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov.

import tests

findMenu(findWidget('OOF2:MenuBar'), 'Windows:Graphics:New').activate()
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint toplevel widget mapped OOF2 Graphics 1
findWidget('OOF2 Graphics 1:Pane0').set_position(285)
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(691)
findWidget('OOF2 Graphics 1').resize(800, 400)
checkpoint OOF.Windows.Graphics.New
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(714)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(258)
setComboBox(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBChooser'), 'Move Nodes')
checkpoint Graphics_1 Move Nodes sensitized

assert tests.sensitivityCheck0()
assert tests.textCompare('---', '---', '---', '---')
assert tests.mouseMode()

findWidget('OOF2 Graphics 1').resize(800, 400)
findMenu(findWidget('OOF2:MenuBar'), 'File:Load:Data').activate()
checkpoint toplevel widget mapped Dialog-Data
findWidget('Dialog-Data').resize(190, 71)
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
findWidget('Dialog-Data:filename').set_text('../../examples/tr')
findWidget('Dialog-Data:filename').set_text('../../examples/tri')
findWidget('Dialog-Data:filename').set_text('../../examples/tria')
findWidget('Dialog-Data:filename').set_text('../../examples/trian')
findWidget('Dialog-Data:filename').set_text('../../examples/triang')
findWidget('Dialog-Data:filename').set_text('../../examples/triangl')
findWidget('Dialog-Data:filename').set_text('../../examples/triangle')
findWidget('Dialog-Data:filename').set_text('../../examples/triangle.')
findWidget('Dialog-Data:filename').set_text('../../examples/triangle.s')
findWidget('Dialog-Data:filename').set_text('../../examples/triangle.sk')
findWidget('Dialog-Data:filename').set_text('../../examples/triangle.ske')
findWidget('Dialog-Data:filename').set_text('../../examples/triangle.skel')
findWidget('Dialog-Data:filename').set_text('../../examples/triangle.skele')
findWidget('Dialog-Data:filename').set_text('../../examples/triangle.skelet')
findWidget('Dialog-Data:filename').set_text('../../examples/triangle.skeleto')
findWidget('Dialog-Data:filename').set_text('../../examples/triangle.skeleton')
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
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
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
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint meshable button set
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
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
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint mesh bdy page updated
findWidget('OOF2 Activity Viewer').resize(400, 300)
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

assert tests.sensitivityCheck0()
assert tests.textCompare('---', '---', '---', '---')
assert tests.mouseMode()

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 8.8861003861004e+01,y=-8.9710424710425e+01,button=1,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox node changed
checkpoint Move Node toolbox down event
assert tests.floatCompare(88.86, 89.71, 0, 0)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8861003861004e+01,y=-8.9285714285714e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
assert tests.floatCompare(88.86, 89.29, 0.129, 0)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8861003861004e+01,y=-8.8861003861004e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.9285714285714e+01,y=-8.8861003861004e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.9285714285714e+01,y=-8.8436293436293e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.9710424710425e+01,y=-8.8436293436293e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.9710424710425e+01,y=-8.7586872586873e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.9710424710425e+01,y=-8.7162162162162e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.9710424710425e+01,y=-8.6737451737452e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 9.0135135135135e+01,y=-8.6737451737452e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 9.0135135135135e+01,y=-8.6312741312741e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 9.0135135135135e+01,y=-8.5888030888031e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 9.0559845559846e+01,y=-8.5463320463320e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 9.0559845559846e+01,y=-8.5038610038610e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 9.0984555984556e+01,y=-8.4613899613900e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 9.0984555984556e+01,y=-8.4189189189189e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 9.1409266409266e+01,y=-8.4189189189189e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 9.1409266409266e+01,y=-8.3339768339768e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 9.1409266409266e+01,y=-8.2915057915058e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 9.1833976833977e+01,y=-8.2490347490347e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 9.1833976833977e+01,y=-8.2490347490347e+01,button=1,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint OOF.Graphics_1.Toolbox.Move_Nodes.MoveNode
checkpoint Move Node toolbox up event

# Done with one mouse move
assert tests.floatCompare(91.83, 82.49, 1.104, 0)
assert tests.sensitivityCheck1()

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 7.6544401544402e+01,y=-8.5888030888031e+01,button=1,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox node changed
checkpoint Move Node toolbox down event
# Beginning another mouse move
assert tests.floatCompare(76.54, 85.89, 0, 0)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.6544401544402e+01,y=-8.5463320463320e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.6969111969112e+01,y=-8.5463320463320e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.6969111969112e+01,y=-8.5038610038610e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.6969111969112e+01,y=-8.4613899613900e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.7393822393822e+01,y=-8.4613899613900e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.7393822393822e+01,y=-8.3764478764479e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.7818532818533e+01,y=-8.3764478764479e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.7818532818533e+01,y=-8.3339768339768e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.7818532818533e+01,y=-8.2915057915058e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.8243243243243e+01,y=-8.2490347490347e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.8667953667954e+01,y=-8.2490347490347e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.8667953667954e+01,y=-8.1640926640927e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.9092664092664e+01,y=-8.1640926640927e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.9092664092664e+01,y=-8.1216216216216e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.9092664092664e+01,y=-8.0791505791506e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.9517374517375e+01,y=-8.0791505791506e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.9517374517375e+01,y=-8.0366795366795e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.9517374517375e+01,y=-7.9942084942085e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.9942084942085e+01,y=-7.9942084942085e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.9942084942085e+01,y=-7.9517374517375e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 7.9942084942085e+01,y=-7.9517374517375e+01,button=1,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint OOF.Graphics_1.Toolbox.Move_Nodes.MoveNode
checkpoint Move Node toolbox up event

# end of the second mouse move
assert tests.sensitivityCheck1()
assert tests.floatCompare(79.94, 79.52, 0.9468, -0.01294)

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Move Nodes:Undo').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint boundary page updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint OOF.Skeleton.Undo

assert tests.sensitivityCheck2()

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Move Nodes:Undo').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint boundary page updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint OOF.Skeleton.Undo

assert tests.sensitivityCheck3()

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Move Nodes:Redo').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint boundary page updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint OOF.Skeleton.Redo

assert tests.sensitivityCheck2()

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Move Nodes:Redo').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint boundary page updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint OOF.Skeleton.Redo

assert tests.sensitivityCheck1()

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Move Nodes:Undo').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint boundary page updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint OOF.Skeleton.Undo

assert tests.sensitivityCheck2()

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Move Nodes:Undo').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint boundary page updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint OOF.Skeleton.Undo

checkpoint_count("Graphics_1 Move Nodes sensitized")
assert tests.sensitivityCheck3()

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Move Nodes:MoveWith:Keyboard').clicked()
checkpoint Graphics_1 Move Nodes sensitized

assert tests.keyboardMode()
assert tests.sensitivityCheck3()

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.4111969111969e+01,y=-1.0714285714286e+01,button=1,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.4111969111969e+01,y=-1.0714285714286e+01,button=1,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox node changed
checkpoint Graphics_1 Move Nodes sensitized
checkpoint OOF.Graphics_1.Toolbox.Move_Nodes.SelectNode
checkpoint Move Node toolbox up event

assert tests.sensitivityCheck4()

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Move Nodes:x').set_text('1.5')
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Move Nodes:x').set_text('15.5')
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Move Nodes:Move').clicked()
checkpoint Move Node toolbox info updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint OOF.Graphics_1.Toolbox.Move_Nodes.MoveNode

assert tests.sensitivityCheck5()
assert tests.floatCompare(15.5, 12.5, 0.2238, 0)

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Move Nodes:Undo').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint boundary page updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint OOF.Skeleton.Undo

assert tests.sensitivityCheck4()

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.1988416988417e+01,y=-2.5154440154440e+01,button=1,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.1988416988417e+01,y=-2.5154440154440e+01,button=1,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox node changed
checkpoint Graphics_1 Move Nodes sensitized
checkpoint OOF.Graphics_1.Toolbox.Move_Nodes.SelectNode
checkpoint Move Node toolbox up event
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Move Nodes:y').set_text('')
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Move Nodes:y').set_text('3')
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Move Nodes:y').set_text('30')
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Move Nodes:Move').clicked()
checkpoint Move Node toolbox info updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint OOF.Graphics_1.Toolbox.Move_Nodes.MoveNode

assert tests.sensitivityCheck5()
assert tests.floatCompare(12.5, 30, 0.4065, 0.193)

# Try an illegal move
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Move Nodes:y').set_text('300')
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Move Nodes:y').set_text('3000')
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Move Nodes:Move').clicked()
checkpoint Move Node toolbox info updated

assert tests.sensitivityCheck5()
assert tests.xyshCompare(12.5, 30, '---', '---')
assert tests.nIllegalElements() == 0

# Allow an illegal move
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Move Nodes:AllowIllegal').clicked()
checkpoint OOF.Graphics_1.Toolbox.Move_Nodes.AllowIllegal
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Move Nodes:y').set_text('0')
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Move Nodes:y').set_text('60')
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Move Nodes:Move').clicked()
checkpoint Move Node toolbox info updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint OOF.Graphics_1.Toolbox.Move_Nodes.MoveNode

assert tests.sensitivityCheck5()
assert tests.xyshCompare(12.5, 60, '---', '---')
assert tests.messageCompare("2 illegal elements in the skeleton.\n")
assert tests.nIllegalElements() == 2

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Move Nodes:Undo').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint boundary page updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint OOF.Skeleton.Undo

assert tests.nIllegalElements() == 0
assert tests.sensitivityCheck6()

checkpoint_count("Graphics_1 Move Nodes sensitized")
checkpoint_count("Move Node toolbox info updated")

# Switch back to Mouse mode
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Move Nodes:MoveWith:Mouse').clicked()
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Move Nodes sensitized

assert tests.textCompare('---', '---', '---', '---')
assert tests.sensitivityCheck2()

canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.1988416988417e+01,y=-8.8011583011583e+01,button=1,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox node changed
checkpoint Move Node toolbox down event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.1988416988417e+01,y=-8.7586872586873e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.2413127413127e+01,y=-8.7586872586873e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
assert tests.floatCompare(12.41, 87.59, 0.003452, 0)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.2413127413127e+01,y=-8.6737451737452e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.3262548262548e+01,y=-8.6312741312741e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.3687258687259e+01,y=-8.5888030888031e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.4536679536680e+01,y=-8.5888030888031e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.4536679536680e+01,y=-8.5038610038610e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.4961389961390e+01,y=-8.4189189189189e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.5386100386100e+01,y=-8.2915057915058e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
# legal
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.6235521235521e+01,y=-8.1216216216216e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.7084942084942e+01,y=-8.0366795366795e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
assert tests.messageCompare("")
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.7934362934363e+01,y=-7.8667953667954e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
assert tests.xyshCompare(17.93, 78.67, '---', '---')
assert tests.messageCompare('Illegal node position!')
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.9208494208494e+01,y=-7.7393822393822e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.9633204633205e+01,y=-7.6544401544402e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.0057915057915e+01,y=-7.6119691119691e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.0482625482625e+01,y=-7.5694980694981e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.0482625482625e+01,y=-7.4845559845560e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.0482625482625e+01,y=-7.4420849420849e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.1332046332046e+01,y=-7.3996138996139e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.1332046332046e+01,y=-7.3146718146718e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.1756756756757e+01,y=-7.2722007722008e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.1756756756757e+01,y=-7.2297297297297e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.2181467181467e+01,y=-7.1872586872587e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.2181467181467e+01,y=-7.1447876447876e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.2181467181467e+01,y=-7.1023166023166e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.3030888030888e+01,y=-7.1023166023166e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.3030888030888e+01,y=-7.0598455598456e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.3030888030888e+01,y=-7.0173745173745e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.3455598455598e+01,y=-7.0173745173745e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.3455598455598e+01,y=-6.9749034749035e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.3455598455598e+01,y=-6.9324324324324e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.3880308880309e+01,y=-6.9324324324324e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.3880308880309e+01,y=-6.9324324324324e+01,button=1,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint Move Node toolbox writable changed
checkpoint OOF.Graphics_1.Toolbox.Move_Nodes.MoveNode
checkpoint Move Node toolbox up event

assert tests.xyshCompare(23.88, 69.32, '---', '---')
assert tests.messageCompare("2 illegal elements in the skeleton.\n")
assert tests.sensitivityCheck1()

findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Move Nodes:Undo').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint boundary page updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Move Nodes sensitized
checkpoint OOF.Skeleton.Undo

assert tests.xyshCompare(23.88, 69.32, '---', '---')

# Make a forbidden illegal move with the mouse.
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Move Nodes:AllowIllegal').clicked()
checkpoint OOF.Graphics_1.Toolbox.Move_Nodes.AllowIllegal
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 8.8011583011583e+01,y=-1.1988416988417e+01,button=1,state=0,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox node changed
checkpoint Move Node toolbox down event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8011583011583e+01,y=-1.2413127413127e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
assert tests.messageCompare("")
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8011583011583e+01,y=-1.3262548262548e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8011583011583e+01,y=-1.4111969111969e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
assert tests.messageCompare("")
assert tests.floatCompare(88.01, 14.11, 0.5019, -0.001353)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8011583011583e+01,y=-1.4961389961390e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
assert tests.messageCompare("Illegal node position!")
assert tests.xyshCompare(88.01, 14.96, '---', '---')
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8011583011583e+01,y=-1.5386100386100e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8011583011583e+01,y=-1.6235521235521e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8011583011583e+01,y=-1.7084942084942e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8011583011583e+01,y=-1.7934362934363e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8011583011583e+01,y=-1.8783783783784e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8011583011583e+01,y=-2.0482625482625e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8011583011583e+01,y=-2.0907335907336e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8011583011583e+01,y=-2.2181467181467e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8011583011583e+01,y=-2.2606177606178e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8011583011583e+01,y=-2.3030888030888e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8011583011583e+01,y=-2.3455598455598e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8011583011583e+01,y=-2.3880308880309e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8011583011583e+01,y=-2.4305019305019e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8011583011583e+01,y=-2.4729729729730e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8011583011583e+01,y=-2.5154440154440e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
assert tests.messageCompare("Illegal node position!")
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8011583011583e+01,y=-2.5579150579151e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8011583011583e+01,y=-2.6003861003861e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8011583011583e+01,y=-2.6853281853282e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8011583011583e+01,y=-2.7277992277992e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8011583011583e+01,y=-2.8127413127413e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8011583011583e+01,y=-2.8552123552124e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8436293436293e+01,y=-2.8552123552124e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8436293436293e+01,y=-2.9401544401544e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8436293436293e+01,y=-2.9826254826255e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8436293436293e+01,y=-3.0250965250965e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
assert tests.messageCompare("Illegal node position!")
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8436293436293e+01,y=-3.0675675675676e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8861003861004e+01,y=-3.0675675675676e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8861003861004e+01,y=-3.1525096525097e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8861003861004e+01,y=-3.1949806949807e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8861003861004e+01,y=-3.2374517374517e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8861003861004e+01,y=-3.2799227799228e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.9285714285714e+01,y=-3.2799227799228e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox info updated
checkpoint Move Node toolbox move event
assert tests.xyshCompare(89.29, 32.8, '---', '---')
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 8.9285714285714e+01,y=-3.2799227799228e+01,button=1,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Move Node toolbox up event

# Displayed x and y snap back to original values when forbidden move
# is finished.
assert tests.xyshCompare(87.5, 12.5, '---', '---')

# Delete the skeleton display layer.
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.1696070952851e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.3392141905703e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 3.5088212858554e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 4.6784283811406e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 5.8000000000000e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 4.6303929047149e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 3.4607858094297e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.2911787141446e+01)
widget_0 = findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList')
widget_0.event(event(gtk.gdk.BUTTON_PRESS,x= 1.7400000000000e+02,y= 2.6000000000000e+01,button=1,state=0,window=widget_0.window))
findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((10,))
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.3000000000000e+01)
checkpoint OOF.Graphics_1.Layer.Select
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Layer:Delete').activate()
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
checkpoint OOF.Graphics_1.Layer.Delete

assert tests.sensitivityCheck0()
assert tests.textCompare('---', '---', '---', '---')
assert tests.messageCompare("")

findMenu(findWidget('OOF2:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(190, 71)
findWidget('Dialog-Python_Log:filename').set_text('m')
findWidget('Dialog-Python_Log:filename').set_text('mo')
findWidget('Dialog-Python_Log:filename').set_text('mov')
findWidget('Dialog-Python_Log:filename').set_text('move')
findWidget('Dialog-Python_Log:filename').set_text('moven')
findWidget('Dialog-Python_Log:filename').set_text('moveno')
findWidget('Dialog-Python_Log:filename').set_text('movenod')
findWidget('Dialog-Python_Log:filename').set_text('movenode')
findWidget('Dialog-Python_Log:filename').set_text('movenode.')
findWidget('Dialog-Python_Log:filename').set_text('movenode.l')
findWidget('Dialog-Python_Log:filename').set_text('movenode.lo')
findWidget('Dialog-Python_Log:filename').set_text('movenode.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('movenode.log')
findMenu(findWidget('OOF2:MenuBar'), 'File:Quit').activate()
checkpoint OOF.ActivityViewer.File.Close
checkpoint OOF.Graphics_1.File.Close
