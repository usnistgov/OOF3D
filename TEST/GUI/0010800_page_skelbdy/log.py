checkpoint toplevel widget mapped OOF2 Activity Viewer
# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:11:32 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov.

import tests
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton Boundaries')
assert tests.sensitization0()
assert tests.bdyStatusEmpty()
assert tests.bdyNames([])
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
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
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
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
assert tests.bdyNames(['top', 'right', 'bottom', 'left', None, 'topleft',                        'bottomleft', 'topright', 'bottomright'])
assert tests.selectedBdy(None)
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
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(693)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1').resize(800, 400)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
checkpoint OOF.Windows.Graphics.New
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(693)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1').resize(800, 400)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((0,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.bdyStatusCheck('top', 'Edge', 10)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((1,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.bdyStatusCheck('right', 'Edge', 14)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((2,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.bdyStatusCheck('bottom', 'Edge', 12)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((3,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.bdyStatusCheck('left', 'Edge', 12)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((5,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.bdyStatusCheck('topleft', 'Point', 1)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((7,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.bdyStatusCheck('topright', 'Point', 1)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((6,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.bdyStatusCheck('bottomleft', 'Point', 1)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((8,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.bdyStatusCheck('bottomright', 'Point', 1)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
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
setComboBox(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Element:Method:Chooser'), 'ByDominantPixel')
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.1956521739130e+01,y=-3.5000000000000e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.1956521739130e+01,y=-3.5000000000000e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Element sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.ByDominantPixel
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
assert tests.newBdyOK(False)
assert tests.directionCheck('segments', ['No edge sequence'])
findWidget('Dialog-New Boundary').resize(361, 160)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Edge boundary from elements')
assert tests.newBdyOK(True)
assert tests.directionCheck('elements', ['Clockwise', 'Counterclockwise'])
findWidget('Dialog-New Boundary:gtk-ok').clicked()
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF2 Messages 1').resize(541, 200)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 9.8000000000000e+01)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 6.0000000000000e+00)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
assert tests.bdyNames(['top', 'right', 'bottom', 'left', 'boundary', None,                       'topleft', 'bottomleft', 'topright', 'bottomright'])
findWidget('OOF2:Navigation:Prev').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(222)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.8043478260870e+01,y=-7.2826086956522e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.8043478260870e+01,y=-7.2826086956522e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(222)
checkpoint Graphics_1 Element sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.ByDominantPixel
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(222)
findWidget('OOF2:Skeleton Selection Page:Pane:Groups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new Element group
findWidget('Dialog-Create a new Element group').resize(249, 72)
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(222)
findWidget('Dialog-Create a new Element group:name:Auto').clicked()
findWidget('Dialog-Create a new Element group:name:Text').set_text('r')
findWidget('Dialog-Create a new Element group:name:Text').set_text('re')
findWidget('Dialog-Create a new Element group:name:Text').set_text('red')
findWidget('Dialog-Create a new Element group:name:Text').set_text('red ')
findWidget('Dialog-Create a new Element group:name:Text').set_text('red s')
findWidget('Dialog-Create a new Element group:name:Text').set_text('red sp')
findWidget('Dialog-Create a new Element group:name:Text').set_text('red spo')
findWidget('Dialog-Create a new Element group:name:Text').set_text('red spot')
findWidget('Dialog-Create a new Element group:gtk-ok').clicked()
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.ElementGroup.New_Group
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(222)
findWidget('OOF2:Skeleton Selection Page:Pane:Groups:Add').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(222)
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint OOF.ElementGroup.Add_to_Group
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(361, 160)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('Dialog-New Boundary:gtk-ok').clicked()
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 8.8000000000000e+01)
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.8000000000000e+01)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint OOF.Skeleton.Boundary.Construct
assert tests.bdyStatusCheck('boundary<2>', 'Edge', 38)
assert tests.bdyNames(['top', 'right', 'bottom', 'left', 'boundary',                       'boundary<2>', None, 'topleft', 'bottomleft',                       'topright', 'bottomright'])
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Select:Segment').clicked()
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint Graphics_1 Segment sensitized
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Settings:Zoom:In').activate()
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 6.3000000000000e+01)
checkpoint OOF.Graphics_1.Settings.Zoom.In
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Settings:Zoom:In').activate()
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:hscroll').get_adjustment().set_value( 1.4000000000000e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 1.5800000000000e+02)
checkpoint OOF.Graphics_1.Settings.Zoom.In
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.0024154589372e+01,y=-4.9347826086957e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.0024154589372e+01,y=-4.9347826086957e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Segment sensitized
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((4,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(278, 108)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
setComboBox(findWidget('Dialog-Boundary modifier:modifier:Chooser'), 'Remove segments')
findWidget('Dialog-Boundary modifier:gtk-ok').clicked()
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 8.8000000000000e+01)
checkpoint boundary page updated
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.8000000000000e+01)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint OOF.Skeleton.Boundary.Modify
assert tests.bdyStatusCheck('boundary', 'Edge', 30)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.8864734299517e+01,y=-5.1086956521739e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.8864734299517e+01,y=-5.1086956521739e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Segment sensitized
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.0603864734300e+01,y=-5.2439613526570e+01,state=1,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.0603864734300e+01,y=-5.2439613526570e+01,state=257,window=findCanvasGdkWindow('Graphics_1')))
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint Graphics_1 Segment sensitized
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.2729468599034e+01,y=-5.4371980676328e+01,state=1,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.2729468599034e+01,y=-5.4371980676328e+01,state=257,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Segment sensitized
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.4082125603865e+01,y=-5.5917874396135e+01,state=1,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.4082125603865e+01,y=-5.6497584541063e+01,state=257,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.4082125603865e+01,y=-5.6497584541063e+01,state=257,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Segment sensitized
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(278, 108)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
setComboBox(findWidget('Dialog-Boundary modifier:modifier:Chooser'), 'Add segments')
findWidget('Dialog-Boundary modifier:gtk-ok').clicked()
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 8.8000000000000e+01)
checkpoint boundary page updated
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.8000000000000e+01)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint OOF.Skeleton.Boundary.Modify
findWidget('OOF2:Navigation:Prev').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(222)
findWidget('OOF2:Skeleton Selection Page:Mode:Segment').clicked()
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
findWidget('OOF2').resize(554, 350)
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(194)
setComboBox(findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentAction:Chooser'), 'Select Named Boundary')
setComboBox(findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentAction:Select Named Boundary:boundary'), 'boundary<2>')
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:SegmentHistory:OK').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(194)
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint selection info updated
checkpoint skeleton selection page updated
checkpoint Graphics_1 Segment sensitized
checkpoint OOF.SegmentSelection.Select_Named_Boundary
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Navigation:Next').clicked()
assert tests.sensitization2()
assert tests.bdyStatusCheck('boundary', 'Edge', 34)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(278, 108)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
assert tests.modifyBdyOK(False)
findWidget('Dialog-Boundary modifier:gtk-cancel').clicked()
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.7367149758454e+01,y=-5.5144927536232e+01,state=4,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.7367149758454e+01,y=-5.5144927536232e+01,state=260,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Segment sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(278, 108)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
assert tests.modifyBdyOK(True)
findWidget('Dialog-Boundary modifier:gtk-ok').clicked()
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 8.8000000000000e+01)
checkpoint boundary page updated
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.8000000000000e+01)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint OOF.Skeleton.Boundary.Modify
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((5,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.bdyStatusCheck('boundary<2>', 'Edge', 38)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:Delete').clicked()
checkpoint boundary page updated
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Delete
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 6.0000000000000e+00)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
assert tests.bdyNames(['top', 'right', 'bottom', 'left', 'boundary', None,                       'topleft', 'bottomleft', 'topright', 'bottomright'])
assert tests.selectedBdy(None)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((4,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.bdyStatusCheck("boundary", "Edge", 71)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.8140096618357e+01,y=-5.1280193236715e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.8140096618357e+01,y=-5.1280193236715e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Segment sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.6207729468599e+01,y=-5.0120772946860e+01,state=1,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.6207729468599e+01,y=-5.0120772946860e+01,state=257,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Segment sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.4468599033816e+01,y=-4.8574879227053e+01,state=1,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.4468599033816e+01,y=-4.8574879227053e+01,state=257,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Segment sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.3309178743961e+01,y=-4.7222222222222e+01,state=1,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.3115942028986e+01,y=-4.7222222222222e+01,state=257,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 4.3115942028986e+01,y=-4.7222222222222e+01,state=257,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Segment sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(278, 108)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
assert tests.modifyBdyOK(True)
findWidget('Dialog-Boundary modifier:gtk-ok').clicked()
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 8.8000000000000e+01)
checkpoint boundary page updated
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 6.0000000000000e+00)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint OOF.Skeleton.Boundary.Modify
assert tests.bdyStatusCheck('boundary', 'Edge', 75)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:Modify').clicked()
checkpoint toplevel widget mapped Dialog-Boundary modifier
findWidget('Dialog-Boundary modifier').resize(278, 108)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
setComboBox(findWidget('Dialog-Boundary modifier:modifier:Chooser'), 'Reverse direction')
assert tests.modifyBdyOK(True)
findWidget('Dialog-Boundary modifier:gtk-ok').clicked()
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 8.8000000000000e+01)
checkpoint boundary page updated
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 6.0000000000000e+00)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint OOF.Skeleton.Boundary.Modify
assert tests.bdyStatusCheck('boundary', 'Edge', 75)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 1.5874015748031e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 1.8850393700787e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 2.1826771653543e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 2.3562992125984e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 2.4307086614173e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 2.4803149606299e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 2.5051181102362e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 2.5547244094488e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 2.5795275590551e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 2.6043307086614e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 2.6291338582677e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 2.6539370078740e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 2.6787401574803e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 2.7035433070866e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 2.7283464566929e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 2.7779527559055e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 2.8027559055118e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 2.8275590551181e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 2.8523622047244e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 2.8771653543307e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 2.9019685039370e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 2.9267716535433e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 2.9515748031496e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 2.9763779527559e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 3.0011811023622e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 3.0259842519685e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 3.1003937007874e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 3.1500000000000e+02)
widget = findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll')
widget.event(event(gtk.gdk.BUTTON_RELEASE,x= 1.4000000000000e+01,y= 2.2700000000000e+02,state=256,window=widget.window))
checkpoint OOF.Graphics_1.Settings.Scroll.Vertical
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Select:Node').clicked()
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
setComboBox(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Node:Method:Chooser'), 'Rectangle')
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.2342995169082e+01,y=-1.6304347826087e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.2536231884058e+01,y=-1.6111111111111e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.3115942028986e+01,y=-1.5724637681159e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.3695652173913e+01,y=-1.5531400966184e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.5628019323672e+01,y=-1.5144927536232e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.8333333333333e+01,y=-1.4565217391304e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.1811594202899e+01,y=-1.3985507246377e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.5483091787440e+01,y=-1.3792270531401e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.8961352657005e+01,y=-1.3599033816425e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.2826086956522e+01,y=-1.3599033816425e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.5531400966184e+01,y=-1.3599033816425e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.8236714975845e+01,y=-1.3599033816425e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.1328502415459e+01,y=-1.3792270531401e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.3647342995169e+01,y=-1.3792270531401e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.6159420289855e+01,y=-1.3985507246377e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.7898550724638e+01,y=-1.3985507246377e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.0024154589372e+01,y=-1.3985507246377e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.1376811594203e+01,y=-1.3985507246377e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.2149758454106e+01,y=-1.3985507246377e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.3309178743961e+01,y=-1.3985507246377e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.4082125603865e+01,y=-1.3792270531401e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.4275362318841e+01,y=-1.3792270531401e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.4468599033816e+01,y=-1.3792270531401e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.4661835748792e+01,y=-1.3792270531401e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.4855072463768e+01,y=-1.3792270531401e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.5048309178744e+01,y=-1.3792270531401e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.5241545893720e+01,y=-1.3792270531401e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 8.5241545893720e+01,y=-1.3792270531401e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Node sensitized
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Rectangle
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(361, 160)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Edge boundary from nodes')
findWidget('Dialog-New Boundary:name:Auto').clicked()
findWidget('Dialog-New Boundary:name:Text').set_text('i')
findWidget('Dialog-New Boundary:name:Text').set_text('in')
findWidget('Dialog-New Boundary:name:Text').set_text('int')
findWidget('Dialog-New Boundary:name:Text').set_text('inte')
findWidget('Dialog-New Boundary:name:Text').set_text('inter')
findWidget('Dialog-New Boundary:name:Text').set_text('interi')
findWidget('Dialog-New Boundary:name:Text').set_text('interio')
findWidget('Dialog-New Boundary:name:Text').set_text('interior')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 8.8000000000000e+01)
checkpoint mesh bdy page updated
checkpoint boundary page updated
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.8000000000000e+01)
checkpoint boundary page updated
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
assert tests.bdyNames(['top', 'right', 'bottom', 'left', 'boundary',                       'interior', None, 'topleft', 'bottomleft', 'topright',                       'bottomright'])
assert tests.bdyStatusCheck('interior', 'Edge', 14)
setComboBox(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Node:Method:Chooser'), 'Single_Node')
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.6062801932367e+01,y=-1.7077294685990e+01,state=1,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.6062801932367e+01,y=-1.7077294685990e+01,state=257,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
checkpoint Graphics_1 Node sensitized
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.6642512077295e+01,y=-2.0362318840580e+01,state=1,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.6642512077295e+01,y=-2.0362318840580e+01,state=257,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Node sensitized
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.8768115942029e+01,y=-2.4806763285024e+01,state=1,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.8768115942029e+01,y=-2.4806763285024e+01,state=257,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Node sensitized
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(361, 160)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
assert tests.newBdyOK(False)
assert tests.directionCheck('nodes', ['No edge sequence'])
findWidget('Dialog-New Boundary:gtk-cancel').clicked()
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 6.1086956521739e+01,y=-2.0942028985507e+01,state=1,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 6.1086956521739e+01,y=-2.0942028985507e+01,state=257,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Node sensitized
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 5.8961352657005e+01,y=-2.0362318840580e+01,state=1,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.8961352657005e+01,y=-2.0362318840580e+01,state=257,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Node sensitized
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(361, 160)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
assert tests.newBdyOK(False)
assert tests.directionCheck('nodes', ['No edge sequence'])
findWidget('Dialog-New Boundary:gtk-cancel').clicked()
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 8.3695652173913e+01,y=-1.7850241545894e+01,state=1,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 8.3695652173913e+01,y=-1.7850241545894e+01,state=257,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Node sensitized
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 8.0990338164251e+01,y=-1.7850241545894e+01,state=1,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 8.0990338164251e+01,y=-1.7850241545894e+01,state=257,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Node sensitized
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(361, 160)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
assert tests.newBdyOK(False)
assert tests.directionCheck('nodes', ['No edge sequence'])
findWidget('Dialog-New Boundary:gtk-cancel').clicked()
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Node:Undo').clicked()
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Undo
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Node:Undo').clicked()
checkpoint selection info updated
checkpoint Graphics_1 Node sensitized
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Undo
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Node:Undo').clicked()
checkpoint selection info updated
checkpoint Graphics_1 Node sensitized
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Undo
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Node:Undo').clicked()
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Undo
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Node:Undo').clicked()
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Undo
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Node:Undo').clicked()
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Undo
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Node:Undo').clicked()
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Undo
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 8.0603864734300e+01,y=-1.8043478260870e+01,state=1,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 8.0603864734300e+01,y=-1.8043478260870e+01,state=257,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Node sensitized
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 8.3115942028986e+01,y=-1.7463768115942e+01,state=1,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 8.3115942028986e+01,y=-1.7463768115942e+01,state=257,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Node sensitized
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(361, 160)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
assert tests.newBdyOK(False)
assert tests.directionCheck('nodes', ['No edge sequence'])
findWidget('Dialog-New Boundary:gtk-cancel').clicked()
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 8.0410628019324e+01,y=-1.7657004830918e+01,state=4,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 8.0410628019324e+01,y=-1.7657004830918e+01,state=260,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Node sensitized
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 8.2922705314010e+01,y=-1.7657004830918e+01,state=4,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.2922705314010e+01,y=-1.7463768115942e+01,state=260,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 8.2922705314010e+01,y=-1.7463768115942e+01,state=260,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Node sensitized
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 9.0652173913043e+01,y=-2.5772946859903e+01,state=1,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 9.0652173913043e+01,y=-2.5772946859903e+01,state=257,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Node sensitized
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(361, 160)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
assert tests.newBdyOK(False)
assert tests.directionCheck('nodes', ['No edge sequence'])
findWidget('Dialog-New Boundary:gtk-cancel').clicked()
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 8.2922705314010e+01,y=-2.5386473429952e+01,state=1,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 8.2922705314010e+01,y=-2.5386473429952e+01,state=257,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Node sensitized
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 8.5434782608696e+01,y=-2.0555555555556e+01,state=1,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 8.5434782608696e+01,y=-2.0555555555556e+01,state=257,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Node sensitized
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 8.3115942028986e+01,y=-1.9589371980676e+01,state=1,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 8.3115942028986e+01,y=-1.9589371980676e+01,state=257,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
checkpoint Graphics_1 Node sensitized
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(361, 160)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
assert tests.newBdyOK(False)
assert tests.directionCheck('nodes', ['No edge sequence'])
findWidget('Dialog-New Boundary:gtk-cancel').clicked()
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 8.3115942028986e+01,y=-1.7077294685990e+01,state=1,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.2922705314010e+01,y=-1.7463768115942e+01,state=257,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 8.2922705314010e+01,y=-1.7463768115942e+01,state=257,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
checkpoint Graphics_1 Node sensitized
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(361, 160)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
setComboBox(findWidget('Dialog-New Boundary:constructor:Edge boundary from nodes:direction'), 'Right to left')
assert tests.newBdyOK(True)
assert tests.directionCheck('nodes', ['Left to right', 'Right to left', 'Top to bottom', 'Bottom to top'])
findWidget('Dialog-New Boundary:gtk-ok').clicked()
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.1000000000000e+02)
checkpoint mesh bdy page updated
checkpoint boundary page updated
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 5.0000000000000e+01)
checkpoint boundary page updated
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint OOF.Skeleton.Boundary.Construct
assert tests.bdyNames(['top', 'right', 'bottom', 'left', 'boundary',                       'interior', 'interior<2>', None, 'topleft',                       'bottomleft', 'topright', 'bottomright'])
assert tests.selectedBdy('interior<2>')
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:Delete').clicked()
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
checkpoint boundary page updated
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.8000000000000e+01)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Delete
assert tests.bdyNames(['top', 'right', 'bottom', 'left', 'boundary',                       'interior', None, 'topleft', 'bottomleft', 'topright',                       'bottomright'])
assert tests.selectedBdy(None)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(361, 160)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Point boundary from nodes')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
checkpoint mesh bdy page updated
checkpoint boundary page updated
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.9000000000000e+01)
checkpoint boundary page updated
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint OOF.Skeleton.Boundary.Construct
assert tests.bdyNames(['top', 'right', 'bottom', 'left', 'boundary',                       'interior', None, 'topleft', 'bottomleft', 'topright',                       'bottomright', 'interior<2>'])
assert tests.selectedBdy('interior<2>')
assert tests.bdyStatusCheck('interior<2>', 'Point', 20)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:Delete').clicked()
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
checkpoint boundary page updated
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.8000000000000e+01)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Delete
assert tests.bdyNames(['top', 'right', 'bottom', 'left', 'boundary',                       'interior', None, 'topleft', 'bottomleft', 'topright',                       'bottomright'])
assert tests.selectedBdy(None)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 8.3888888888889e+01,y=-1.5338164251208e+01,state=4,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.3695652173913e+01,y=-1.5338164251208e+01,state=260,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 8.3695652173913e+01,y=-1.5338164251208e+01,state=260,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Node sensitized
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 8.3309178743961e+01,y=-1.7270531400966e+01,state=4,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 8.3309178743961e+01,y=-1.7270531400966e+01,state=260,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Node sensitized
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Node.Single_Node
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(361, 132)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('Dialog-New Boundary:gtk-ok').clicked()
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
checkpoint mesh bdy page updated
checkpoint boundary page updated
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.9000000000000e+01)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
assert tests.bdyStatusCheck('interior<2>', 'Point', 18)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:Delete').clicked()
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
checkpoint boundary page updated
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.8000000000000e+01)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Delete
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Select:Segment').clicked()
checkpoint Graphics_1 Node sensitized
checkpoint selection info updated
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
setComboBox(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Segment:Method:Chooser'), 'Circle')
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 4.9879227053140e+01,y=-2.7318840579710e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.0072463768116e+01,y=-2.7125603864734e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.1038647342995e+01,y=-2.6352657004831e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.1618357487923e+01,y=-2.5772946859903e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.2391304347826e+01,y=-2.4420289855072e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.3357487922705e+01,y=-2.3454106280193e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.4130434782609e+01,y=-2.2487922705314e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.5096618357488e+01,y=-2.1714975845411e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.5676328502415e+01,y=-2.1135265700483e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.5869565217391e+01,y=-2.0555555555556e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.6256038647343e+01,y=-2.0169082125604e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.6835748792271e+01,y=-1.9202898550725e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.7415458937198e+01,y=-1.8623188405797e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.7995169082126e+01,y=-1.8429951690821e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.8574879227053e+01,y=-1.8236714975845e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.8768115942029e+01,y=-1.8236714975845e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.8961352657005e+01,y=-1.8236714975845e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.9154589371981e+01,y=-1.8236714975845e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.9347826086957e+01,y=-1.8236714975845e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 5.9347826086957e+01,y=-1.8236714975845e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Segment sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint Graphics_1 Segment sensitized
checkpoint skeleton selection page updated
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Segment.Circle
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(361, 132)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Edge boundary from segments')
findWidget('Dialog-New Boundary').resize(361, 160)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Edge boundary from elements')
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Point boundary from segments')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
checkpoint mesh bdy page updated
checkpoint boundary page updated
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.9000000000000e+01)
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
assert tests.bdyStatusCheck('interior<2>', 'Point', 44)
assert tests.bdyNames(['top', 'right', 'bottom', 'left', 'boundary',                       'interior', None, 'topleft', 'bottomleft', 'topright',                       'bottomright', 'interior<2>'])
assert tests.selectedBdy('interior<2>')
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:Delete').clicked()
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
checkpoint boundary page updated
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.8000000000000e+01)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Delete
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(361, 132)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Point boundary from elements')
findWidget('Dialog-New Boundary:gtk-cancel').clicked()
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Skeleton Selection:Select:Element').clicked()
checkpoint Graphics_1 Segment sensitized
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.5917874396135e+01,y=-2.9057971014493e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.6111111111111e+01,y=-2.9057971014493e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.6111111111111e+01,y=-2.9057971014493e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Element sensitized
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
checkpoint Graphics_1 Element sensitized
checkpoint selection info updated
checkpoint OOF.Graphics_1.Toolbox.Select_Element.ByDominantPixel
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:hscroll').get_adjustment().set_value( 1.3860000000000e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:hscroll').get_adjustment().set_value( 1.3440000000000e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:hscroll').get_adjustment().set_value( 1.0360000000000e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:hscroll').get_adjustment().set_value( 1.9600000000000e+01)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:hscroll').get_adjustment().set_value( 0.0000000000000e+00)
widget = findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:hscroll')
widget.event(event(gtk.gdk.BUTTON_RELEASE,x= 1.0000000000000e+00,y=-5.0000000000000e+00,state=256,window=widget.window))
checkpoint OOF.Graphics_1.Settings.Scroll.Horizontal
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(361, 132)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
setComboBox(findWidget('Dialog-New Boundary:constructor:Chooser'), 'Point boundary from elements')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
checkpoint mesh bdy page updated
checkpoint boundary page updated
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.9000000000000e+01)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
assert tests.bdyStatusCheck('interior<2>', 'Point', 31)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:Delete').clicked()
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
checkpoint boundary page updated
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 2.8000000000000e+01)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Delete
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary
findWidget('Dialog-New Boundary').resize(361, 132)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
setComboBox(findWidget('Dialog-New Boundary:constructor:Point boundary from elements:group'), 'red spot')
findWidget('Dialog-New Boundary:gtk-ok').clicked()
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
checkpoint mesh bdy page updated
checkpoint boundary page updated
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 4.9000000000000e+01)
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Construct
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
assert tests.bdyStatusCheck('interior<2>', 'Point', 38)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 3.1251968503937e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 3.0507874015748e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 2.8771653543307e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 2.6787401574803e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 1.7362204724409e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 1.3145669291339e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 1.1161417322835e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 3.9685039370079e+01)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 3.4724409448819e+01)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 3.7204724409449e+01)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 3.9685039370079e+01)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 4.4645669291339e+01)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 4.7125984251969e+01)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 5.2086614173228e+01)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 5.4566929133858e+01)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 5.7047244094488e+01)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 5.9527559055118e+01)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 6.2007874015748e+01)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll').get_adjustment().set_value( 6.6968503937008e+01)
widget = findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas:vscroll')
widget.event(event(gtk.gdk.BUTTON_RELEASE,x= 1.0000000000000e+01,y= 5.3000000000000e+01,state=256,window=widget.window))
checkpoint OOF.Graphics_1.Settings.Scroll.Vertical
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:Rename').clicked()
checkpoint toplevel widget mapped Dialog-New name for this boundary
findWidget('Dialog-New name for this boundary').resize(194, 72)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('Dialog-New name for this boundary:name').set_text('')
findWidget('Dialog-New name for this boundary:name').set_text('r')
findWidget('Dialog-New name for this boundary:name').set_text('re')
findWidget('Dialog-New name for this boundary:name').set_text('red')
findWidget('Dialog-New name for this boundary:name').set_text('bred')
findWidget('Dialog-New name for this boundary:name').set_text('bired')
findWidget('Dialog-New name for this boundary:name').set_text('bigred')
findWidget('Dialog-New name for this boundary:name').set_text('big red')
findWidget('Dialog-New name for this boundary:gtk-ok').clicked()
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
checkpoint mesh bdy page updated
checkpoint boundary page updated
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Rename
assert tests.bdyNames(['top', 'right', 'bottom', 'left', 'boundary',                       'interior', None, 'topleft', 'bottomleft', 'topright',                       'bottomright', 'big red'])
assert tests.selectedBdy('big red')
assert tests.bdyStatusCheck('big red', 'Point', 38)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton')
findWidget('OOF2').resize(593, 434)
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
findWidget('OOF2:Skeleton Page:New').clicked()
checkpoint toplevel widget mapped Dialog-New skeleton
checkpoint skeleton page sensitized
findWidget('Dialog-New skeleton').resize(334, 152)
findWidget('Dialog-New skeleton:gtk-ok').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Element sensitized
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
checkpoint skeleton page sensitized
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton Boundaries')
assert tests.bdyNames(['top', 'right', 'bottom', 'left', 'boundary',                        'interior', None, 'topleft', 'bottomleft', 'topright',                       'bottomright', 'big red'])
assert tests.selectedBdy('big red')
setComboBox(findWidget('OOF2:Skeleton Boundaries Page:Skeleton'), 'skeleton<2>')
checkpoint boundary page updated
assert tests.bdyNames(['top', 'bottom', 'right', 'left', None, 'topleft',                       'bottomleft', 'topright', 'bottomright'])
assert tests.selectedBdy(None)
assert tests.bdyStatusNoBdy()
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
setComboBox(findWidget('OOF2:Skeleton Boundaries Page:Skeleton'), 'skeleton')
checkpoint boundary page updated
assert tests.bdyNames(['top', 'right', 'bottom', 'left', 'boundary',                       'interior', None, 'topleft', 'bottomleft', 'topright',                       'bottomright', 'big red'])
assert tests.selectedBdy('big red')
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.0200000000000e+02)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 0.0000000000000e+00)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
setComboBox(findWidget('OOF2:Skeleton Boundaries Page:Skeleton'), 'skeleton<2>')
checkpoint boundary page updated
assert tests.bdyStatusNoBdy()
assert tests.bdyNames(['top', 'bottom', 'right', 'left', None, 'topleft',                       'bottomleft', 'topright', 'bottomright'])
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((5,))
checkpoint boundary page updated
checkpoint boundary page updated
assert tests.bdyStatusCheck('topleft', 'Point', 1)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:Delete').clicked()
checkpoint boundary page updated
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Delete
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
assert tests.bdyStatusNoBdy()
assert tests.bdyNames(['top', 'bottom', 'right', 'left', None, 'bottomleft', 'topright', 'bottomright'])
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton')
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
findWidget('OOF2:Skeleton Page:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(220, 94)
findWidget('Questioner:gtk-ok').clicked()
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
checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint OOF.Skeleton.Delete
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton Boundaries')
assert tests.bdyStatusCheck('big red', 'Point', 38)
assert tests.selectedBdy('big red')
assert tests.bdyNames(['top', 'right', 'bottom', 'left', 'boundary',                       'interior', None, 'topleft', 'bottomleft', 'topright',                       'bottomright', 'big red'])
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 1.0200000000000e+02)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll').get_vadjustment().set_value( 0.0000000000000e+00)
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton')
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
findWidget('OOF2:Skeleton Page:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(194, 94)
findWidget('Questioner:gtk-ok').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
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
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton Boundaries')
assert tests.bdyNames([])
assert tests.bdyStatusEmpty()
assert tests.sensitization0()
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findMenu(findWidget('OOF2:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(194, 72)
findWidget('Dialog-Python_Log:filename').set_text('skelbdy.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('skelbdy.log')
findMenu(findWidget('OOF2:MenuBar'), 'File:Quit').activate()
