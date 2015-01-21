checkpoint toplevel widget mapped OOF2 Activity Viewer
# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:10:33 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov.

import tests
findMenu(findWidget('OOF2:MenuBar'), 'Help:Tutorials').activate()
findMenu(findWidget('OOF2:MenuBar'), 'Help:Tutorials:Postprocessing').activate()
checkpoint toplevel widget mapped Postprocessing
findWidget('Postprocessing').resize(500, 300)
findWidget('Postprocessing:Next').clicked()
findWidget('Postprocessing').resize(500, 300)
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
findWidget('Dialog-Data:filename').set_text('../../examples/c')
findWidget('Dialog-Data:filename').set_text('../../examples/cy')
findWidget('Dialog-Data:filename').set_text('../../examples/cya')
findWidget('Dialog-Data:filename').set_text('../../examples/cyal')
findWidget('Dialog-Data:filename').set_text('../../examples/cyall')
findWidget('Dialog-Data:filename').set_text('../../examples/cyallo')
findWidget('Dialog-Data:filename').set_text('../../examples/cyallow')
findWidget('Dialog-Data:filename').set_text('../../examples/cyallow.')
findWidget('Dialog-Data:filename').set_text('../../examples/cyallow.m')
findWidget('Dialog-Data:filename').set_text('../../examples/cyallow.me')
findWidget('Dialog-Data:filename').set_text('../../examples/cyallow.mes')
findWidget('Dialog-Data:filename').set_text('../../examples/cyallow.mesh')
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
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint meshable button set
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
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
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.File.Load.Data
findWidget('Postprocessing:Next').clicked()
findMenu(findWidget('Postprocessing:MenuBar'), 'Windows:Graphics:New').activate()
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint toplevel widget mapped OOF2 Graphics 1
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint OOF.Windows.Graphics.New
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
findWidget('OOF2 Graphics 1').resize(800, 400)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 3.6842105263158e+00)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 7.3684210526316e+00)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.1052631578947e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.4736842105263e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.8421052631579e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.2105263157895e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.5789473684211e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.9473684210526e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 3.3157894736842e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 3.6842105263158e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 4.4210526315789e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 5.1578947368421e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 5.5263157894737e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 5.8947368421053e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 6.2631578947368e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 6.6315789473684e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 7.0000000000000e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 6.6315789473684e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 6.2631578947368e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 5.8947368421053e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 5.5263157894737e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 5.1578947368421e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 4.7894736842105e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 4.4210526315789e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 4.0526315789474e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 3.6842105263158e+01)
findCellRenderer(findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList'), col=0, rend=0).emit('toggled', '10')
findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((10,))
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 3.6000000000000e+01)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint OOF.Graphics_1.Layer.Select
checkpoint selection info updated
checkpoint OOF.Graphics_1.Layer.Hide
findWidget('Postprocessing:Next').clicked()
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Layer:New').activate()
checkpoint layereditor layerset changed
checkpoint toplevel widget mapped OOF2 Graphics Layer Editor
checkpoint layer editor updated
checkpoint layereditor layerset changed
checkpoint layer editor updated
checkpoint OOF.LayerEditor.LayerSet.New
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
setComboBox(findWidget('OOF2 Graphics Layer Editor:ObjectScroll:category'), 'Mesh')
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
checkpoint layer editor updated
checkpoint OOF.LayerEditor.LayerSet.DisplayedObject
findWidget('Postprocessing:Next').clicked()
findWidget('OOF2 Graphics Layer Editor:DisplayMethods:New').clicked()
checkpoint toplevel widget mapped Dialog-New Display Method for Mesh mesh
findWidget('Dialog-New Display Method for Mesh mesh').resize(339, 232)
setComboBox(findWidget('Dialog-New Display Method for Mesh mesh:method:Chooser'), 'Filled Contour')
findWidget('Dialog-New Display Method for Mesh mesh').resize(406, 356)
findWidget('Dialog-New Display Method for Mesh mesh:gtk-ok').clicked()
findWidget('OOF2 Messages 1').resize(598, 200)
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
checkpoint layer editor updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint OOF.LayerEditor.LayerSet.Send
checkpoint layereditor layerset changed
checkpoint OOF.LayerEditor.LayerSet.Add_Method
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('Postprocessing:Next').clicked()
findWidget('OOF2 Graphics Layer Editor:DisplayMethods:Edit').clicked()
checkpoint toplevel widget mapped Dialog-New Display Method for Mesh mesh
findWidget('Dialog-New Display Method for Mesh mesh').resize(406, 356)
findWidget('Dialog-New Display Method for Mesh mesh:method:Filled Contour:levels').set_text('1')
findWidget('Dialog-New Display Method for Mesh mesh:method:Filled Contour:levels').set_text('21')
findWidget('Dialog-New Display Method for Mesh mesh:gtk-ok').clicked()
findWidget('OOF2 Graphics Layer Editor').resize(600, 250)
checkpoint layer editor updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint OOF.LayerEditor.LayerSet.Send
checkpoint layereditor layerset changed
checkpoint OOF.LayerEditor.LayerSet.Replace_Method
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('Postprocessing:Next').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(241)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(668)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('Postprocessing:Next').clicked()
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(241)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(668)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
setComboBox(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBChooser'), 'Mesh Info')
checkpoint Graphics_1 Mesh Info sensitized
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(241)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(668)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('Postprocessing').resize(500, 300)
findWidget('Postprocessing:Next').clicked()
findWidget('Postprocessing').resize(500, 300)
findWidget('Postprocessing').resize(501, 305)
findWidget('Postprocessing').resize(501, 310)
findWidget('Postprocessing').resize(501, 319)
findWidget('Postprocessing').resize(501, 320)
findWidget('Postprocessing').resize(501, 322)
findWidget('Postprocessing').resize(501, 325)
findWidget('Postprocessing').resize(501, 327)
findWidget('Postprocessing').resize(501, 328)
findWidget('Postprocessing').resize(501, 330)
findWidget('Postprocessing').resize(501, 331)
findWidget('Postprocessing').resize(500, 334)
findWidget('Postprocessing').resize(500, 340)
findWidget('Postprocessing').resize(500, 347)
findWidget('Postprocessing').resize(500, 350)
findWidget('Postprocessing').resize(500, 351)
findWidget('Postprocessing').resize(499, 354)
findWidget('Postprocessing').resize(499, 357)
findWidget('Postprocessing').resize(499, 358)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Mesh Info:Click:Element').clicked()
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Mesh Info:Click:Node').clicked()
findWidget('OOF2 Graphics 1').resize(800, 400)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.6326086956522e+01,y=-4.3956521739130e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.6326086956522e+01,y=-4.3956521739130e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint Graphics_1 Mesh Info sensitized
checkpoint OOF.Graphics_1.Toolbox.Mesh_Info.QueryNode
assert tests.meshInfoNodeTBCheck('OOF2 Graphics 1', 16, 'FuncNode', (15, 45))
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Mesh Info:NewDataViewer').clicked()
checkpoint Mesh_Data_1 position updated
checkpoint Mesh_Data_1 mesh updated
checkpoint toplevel widget mapped Mesh Data 1
checkpoint Mesh_Data_1 data updated
assert tests.meshDataViewerCheck('Mesh Data 1', 'Graphics_1', 'cyallow.png:skeleton:mesh', 16.3261, 43.9565, x=2.72101, y=-3.13975)
findWidget('Mesh Data 1').resize(301, 326)
findWidget('Postprocessing:Next').clicked()
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Mesh Info:Click:Node').clicked()
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Mesh Info:Click:Element').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Mesh_Data_1 position updated
checkpoint OOF.Graphics_1.Toolbox.Mesh_Info.QueryElement
assert tests.meshInfoElementTBCheck('OOF2 Graphics 1', 9, 'Q4_4', ['FuncNode 11 at (15, 24)', 'FuncNode 12 at (30, 24)', 'FuncNode 17 at (30, 45)', 'FuncNode 16 at (15, 45)'], 'cyan-material')
findWidget('OOF2 Graphics 1').resize(797, 410)
findWidget('OOF2 Graphics 1').resize(796, 447)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(240)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(664)
findWidget('OOF2 Graphics 1:Pane0').set_position(325)
findWidget('OOF2 Graphics 1').resize(799, 526)
findWidget('OOF2 Graphics 1').resize(800, 551)
findWidget('OOF2 Graphics 1').resize(800, 558)
findWidget('OOF2 Graphics 1').resize(800, 560)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(241)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(668)
findWidget('OOF2 Graphics 1:Pane0').set_position(438)
findWidget('OOF2 Graphics 1').resize(800, 561)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(241)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(668)
findWidget('OOF2 Graphics 1:Pane0').set_position(439)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(242)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(668)
findWidget('OOF2 Graphics 1:Pane0').set_position(439)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(269)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(668)
findWidget('OOF2 Graphics 1:Pane0').set_position(439)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(272)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(668)
findWidget('OOF2 Graphics 1:Pane0').set_position(439)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(277)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(668)
findWidget('OOF2 Graphics 1:Pane0').set_position(439)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(668)
findWidget('OOF2 Graphics 1:Pane0').set_position(439)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 2.0760869565217e+01,y=-3.4565217391304e+01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 2.0760869565217e+01,y=-3.4565217391304e+01,state=256,window=findCanvasGdkWindow('Graphics_1')))
findWidget('OOF2 Graphics 1:Pane0').set_position(439)
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Mesh_Data_1 position updated
checkpoint Mesh_Data_1 data updated
checkpoint OOF.Graphics_1.Toolbox.Mesh_Info.QueryElement
assert tests.meshDataViewerCheck('Mesh Data 1', 'Graphics_1', 'cyallow.png:skeleton:mesh', 20.7609, 34.5652, x=3.46014, y=-2.46894)
findWidget('Postprocessing:Next').clicked()
findWidget('Postprocessing:Close').clicked()
findMenu(findWidget('OOF2:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(194, 72)
findWidget('Dialog-Python_Log:filename').set_text('p')
findWidget('Dialog-Python_Log:filename').set_text('po')
findWidget('Dialog-Python_Log:filename').set_text('pos')
findWidget('Dialog-Python_Log:filename').set_text('po')
findWidget('Dialog-Python_Log:filename').set_text('p')
findWidget('Dialog-Python_Log:filename').set_text('pp')
findWidget('Dialog-Python_Log:filename').set_text('pp.')
findWidget('Dialog-Python_Log:filename').set_text('pp.l')
findWidget('Dialog-Python_Log:filename').set_text('pp.lo')
findWidget('Dialog-Python_Log:filename').set_text('pp.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('pp.log')
findMenu(findWidget('OOF2:MenuBar'), 'File:Quit').activate()
