checkpoint toplevel widget mapped OOF2 Activity Viewer
# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:12:12 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
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
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov.

import tests

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
findWidget('OOF2 Activity Viewer').resize(400, 300)
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
checkpoint OOF.File.LoadStartUp.Data
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Analysis')
assert tests.goSensitive(1)
assert tests.samplingOptions('Grid Points', 'Spaced Grid Points', 'Pixels')
assert tests.samplingParams('Grid Points',                            ['x_points', 'y_points', 'show_x', 'show_y'])
findWidget('OOF2').resize(550, 354)
findWidget('OOF2').resize(550, 423)
findWidget('OOF2').resize(552, 474)
findWidget('OOF2').resize(553, 500)
findWidget('OOF2').resize(554, 518)
findWidget('OOF2').resize(559, 538)
findWidget('OOF2').resize(559, 539)
findWidget('OOF2').resize(560, 542)
findWidget('OOF2').resize(560, 543)
findWidget('OOF2').resize(561, 543)
findWidget('OOF2:Analysis Page:bottom:Sampling:Sampling:Grid Points:x_points').set_text('')
findWidget('OOF2:Analysis Page:bottom:Sampling:Sampling:Grid Points:x_points').set_text('3')
findWidget('OOF2:Analysis Page:bottom:Sampling:Sampling:Grid Points:y_points').set_text('')
findWidget('OOF2:Analysis Page:bottom:Sampling:Sampling:Grid Points:y_points').set_text('3')
findWidget('OOF2:Analysis Page:Go').clicked()
findWidget('OOF2 Messages 1').resize(545, 200)
checkpoint OOF.Mesh.Analyze.Direct_Output
assert tests.msgTextTail('10.0, 10.0, 0.0')
setComboBox(findWidget('OOF2:Analysis Page:top:Domain:DomainRCF:Chooser'), 'Pixel Group')
assert tests.goSensitive(1)
assert tests.samplingOptions('Grid Points', 'Spaced Grid Points', 'Pixels')
assert tests.samplingParams('Grid Points',                             ['x_points', 'y_points', 'show_x', 'show_y'])
setComboBox(findWidget('OOF2:Analysis Page:top:Domain:DomainRCF:Pixel Group:pixels'), 'green')
assert tests.goSensitive(1)
assert tests.samplingOptions('Grid Points', 'Spaced Grid Points', 'Pixels')
assert tests.samplingParams('Grid Points',                             ['x_points', 'y_points', 'show_x', 'show_y'])
findWidget('OOF2:Analysis Page:Go').clicked()
checkpoint OOF.Mesh.Analyze.Direct_Output
assert tests.msgTextTail('10.0, 10.0, 0.0')
setComboBox(findWidget('OOF2:Analysis Page:top:Domain:DomainRCF:Chooser'), 'Entire Mesh')
assert tests.goSensitive(1)
assert tests.samplingOptions('Grid Points', 'Spaced Grid Points', 'Pixels')
assert tests.samplingParams('Grid Points',                             ['x_points', 'y_points', 'show_x', 'show_y'])
setComboBox(findWidget('OOF2:Analysis Page:top:Domain:DomainRCF:Chooser'), 'Cross Section')
assert tests.goSensitive(0)
assert tests.samplingOptions('Line Points', 'Element Segments')
assert tests.samplingParams('Line Points', ['n_points', 'show_distance',                             'show_fraction', 'show_x', 'show_y'])
assert tests.csWidgetCheck0()
setComboBox(findWidget('OOF2:Analysis Page:bottom:Sampling:Sampling:Chooser'), 'Element Segments')
assert tests.goSensitive(0)
assert tests.samplingOptions('Line Points', 'Element Segments')
assert tests.samplingParams('Element Segments', ['n_points', 'show_segment',                           'show_distance', 'show_fraction', 'show_x', 'show_y'])
setComboBox(findWidget('OOF2:Analysis Page:top:Domain:DomainRCF:Chooser'), 'Element Group')
assert tests.goSensitive(1)
assert tests.samplingOptions('Grid Points', 'Spaced Grid Points')
assert tests.samplingParams('Grid Points',                             ['x_points', 'y_points', 'show_x', 'show_y'])
findWidget('OOF2:Analysis Page:Go').clicked()
checkpoint OOF.Mesh.Analyze.Direct_Output
assert tests.msgTextTail("OOF.Mesh.Analyze.Direct_Output(mesh='el_shape.png:skeleton:mesh', time=latest, data=getOutput('Field:Component',component='x',field=Displacement), domain=ElementGroup(elements=selection), sampling=GridSampleSet(x_points=3,y_points=3,show_x=True,show_y=True), destination=MessageWindowStream())")
setComboBox(findWidget('OOF2:Analysis Page:top:Domain:DomainRCF:Chooser'), 'Entire Mesh')
setComboBox(findWidget('OOF2:Analysis Page:bottom:Operation:OperationRCF:Chooser'), 'Average')
assert tests.goSensitive(1)
assert tests.samplingOptions('Element Set', 'Grid Points',                              'Spaced Grid Points', 'Pixels')
assert tests.samplingParams('Grid Points', ['x_points', 'y_points'])
setComboBox(findWidget('OOF2:Analysis Page:bottom:Operation:OperationRCF:Chooser'), 'Direct Output')
assert tests.goSensitive(1)
assert tests.samplingOptions('Grid Points', 'Spaced Grid Points', 'Pixels')
assert tests.samplingParams('Grid Points',                             ['x_points', 'y_points', 'show_x', 'show_y'])
setComboBox(findWidget('OOF2:Analysis Page:bottom:Operation:OperationRCF:Chooser'), 'Standard Deviation')
assert tests.goSensitive(1)
assert tests.samplingOptions('Element Set', 'Grid Points',                              'Spaced Grid Points', 'Pixels')
assert tests.samplingParams('Grid Points', ['x_points', 'y_points'])
setComboBox(findWidget('OOF2:Analysis Page:bottom:Sampling:Sampling:Chooser'), 'Spaced Grid Points')
assert tests.goSensitive(1)
assert tests.samplingParams('Spaced Grid Points', ['delta_x', 'delta_y'])
setComboBox(findWidget('OOF2:Analysis Page:bottom:Operation:OperationRCF:Chooser'), 'Direct Output')
assert tests.goSensitive(1)
assert tests.samplingParams('Spaced Grid Points', ['delta_x', 'delta_y',                             'show_x', 'show_y'])
setComboBox(findWidget('OOF2:Analysis Page:bottom:Sampling:Sampling:Chooser'), 'Grid Points')
setComboBox(findWidget('OOF2:Analysis Page:bottom:Operation:OperationRCF:Chooser'), 'Standard Deviation')
assert tests.goSensitive(1)
assert tests.samplingParams('Grid Points', ['x_points', 'y_points'])
setComboBox(findWidget('OOF2:Analysis Page:bottom:Sampling:Sampling:Chooser'), 'Pixels')
assert tests.goSensitive(1)
assert tests.samplingParams('Pixels', [])
findWidget('OOF2:Analysis Page:Destination:New').clicked()
checkpoint toplevel widget mapped Dialog-Add a data destination
findWidget('Dialog-Add a data destination').resize(194, 72)
findWidget('Dialog-Add a data destination:filename').set_text('m')
findWidget('Dialog-Add a data destination:filename').set_text('ms')
findWidget('Dialog-Add a data destination:filename').set_text('msg')
findWidget('Dialog-Add a data destination:filename').set_text('msg.')
findWidget('Dialog-Add a data destination:filename').set_text('msg.d')
findWidget('Dialog-Add a data destination:filename').set_text('msg.da')
findWidget('Dialog-Add a data destination:filename').set_text('msg.dat')
findWidget('Dialog-Add a data destination:filename').set_text('msg.data')
findWidget('Dialog-Add a data destination:gtk-ok').clicked()
assert tests.chooserCheck('OOF2:Analysis Page:Destination:Chooser', ['<Message Window>', 'msg.data'])
setComboBox(findWidget('OOF2:Analysis Page:bottom:Operation:OperationRCF:Chooser'), 'Direct Output')
findWidget('OOF2:Analysis Page:Go').clicked()
checkpoint OOF.Mesh.Analyze.Direct_Output
assert tests.filediff('msg.data')
findWidget('OOF2:Analysis Page:Destination:Clear').clicked()
assert tests.chooserCheck('OOF2:Analysis Page:Destination:Chooser', ['<Message Window>'])
setComboBox(findWidget('OOF2:Analysis Page:bottom:Operation:OperationRCF:Chooser'), 'Average')
assert tests.samplingParams('Pixels', [])
findWidget('OOF2:Analysis Page:Go').clicked()
checkpoint OOF.Mesh.Analyze.Average
assert tests.msgTextTail('# 1. time\n# 2. average of Displacement[x]\n0.0, 0.0')
findWidget('OOF2').resize(561, 543)
findWidget('OOF2:Navigation:Prev').clicked()
#findWidget('OOF2:Solver Page:Solve').clicked()
findWidget('OOF2:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList').get_selection().select_path((0,))
findWidget('OOF2:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(423, 212)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF2:Solver Page:end').set_text('0')
findWidget('OOF2:Solver Page:solve').clicked()
findWidget('OOF2:Solver Page:end').set_text('')
checkpoint OOF.Mesh.Solve

findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2:Analysis Page:Go').clicked()
checkpoint OOF.Mesh.Analyze.Average
assert tests.msgTextValue(0.0, -0.008531216, tolerance=1.e-9)
findMenu(findWidget('OOF2:MenuBar'), 'Windows:Graphics:New').activate()
checkpoint Move Node toolbox info updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint toplevel widget mapped OOF2 Graphics 1
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(693)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(693)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint OOF.Windows.Graphics.New
findWidget('OOF2 Graphics 1').resize(800, 400)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(693)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
setComboBox(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBChooser'), 'Mesh Cross Section')
checkpoint Graphics_1 Mesh Cross Section sensitized
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.5573194051951e-01,y=-1.4173913043478e+00,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.5573194051951e-01,y=-1.4173913043478e+00,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Mesh Cross Section sensitized
checkpoint OOF.Mesh.Cross_Section.New
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.5573194051951e-01,y=-1.4173913043478e+00,state=0,window=findCanvasGdkWindow('Graphics_1')))
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.5573194051951e-01,y=-1.4695652173913e+00,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.1660150573690e-01,y=-1.4695652173913e+00,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.8616672312821e-01,y=-1.4695652173913e+00,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 1.3557319405195e+00,y=-1.5217391304348e+00,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 2.2426884622586e+00,y=-1.5217391304348e+00,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 3.2861667231282e+00,y=-1.5739130434783e+00,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 4.2252971579108e+00,y=-1.5739130434783e+00,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 5.4252971579108e+00,y=-1.6782608695652e+00,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.1557319405195e+00,y=-1.6782608695652e+00,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 6.8339928100847e+00,y=-1.6782608695652e+00,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.4600797666065e+00,y=-1.6782608695652e+00,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 7.9296449839978e+00,y=-1.6782608695652e+00,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.1383406361717e+00,y=-1.6782608695652e+00,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.5035580274760e+00,y=-1.6782608695652e+00,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 8.7644275926934e+00,y=-1.6782608695652e+00,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 9.0252971579108e+00,y=-1.6782608695652e+00,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 9.1296449839978e+00,y=-1.6782608695652e+00,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 9.1818188970412e+00,y=-1.6782608695652e+00,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 9.2339928100847e+00,y=-1.6782608695652e+00,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x= 9.2861667231282e+00,y=-1.6782608695652e+00,state=256,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 9.2861667231282e+00,y=-1.6782608695652e+00,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Mesh Cross Section sensitized
checkpoint OOF.Mesh.Cross_Section.New
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
assert tests.goSensitive(1)
assert tests.samplingParams('Pixels', [])
setComboBox(findWidget('OOF2:Analysis Page:top:Domain:DomainRCF:Chooser'), 'Cross Section')
assert tests.goSensitive(1)
assert tests.samplingParams('Line Points', ['n_points'])
assert tests.samplingOptions('Line Points', 'Element Segments')
setComboBox(findWidget('OOF2:Analysis Page:bottom:Sampling:Sampling:Chooser'), 'Element Segments')
setComboBox(findWidget('OOF2:Analysis Page:bottom:Operation:OperationRCF:Chooser'), 'Direct Output')
assert tests.goSensitive(1)
assert tests.samplingOptions('Line Points', 'Element Segments')
assert tests.samplingParams('Element Segments', ['n_points', 'show_segment', 'show_distance', 'show_fraction', 'show_x', 'show_y'])
findWidget('OOF2').resize(617, 543)
findWidget('OOF2:Analysis Page:bottom:Sampling').get_vadjustment().set_value( 2.7000000000000e+00)
findWidget('OOF2:Analysis Page:bottom:Sampling').get_vadjustment().set_value( 4.0500000000000e+00)
findWidget('OOF2:Analysis Page:bottom:Sampling').get_vadjustment().set_value( 5.4000000000000e+00)
findWidget('OOF2:Analysis Page:bottom:Sampling').get_vadjustment().set_value( 8.1000000000000e+00)
findWidget('OOF2:Analysis Page:bottom:Sampling').get_vadjustment().set_value( 9.4500000000000e+00)
findWidget('OOF2:Analysis Page:bottom:Sampling').get_vadjustment().set_value( 1.2150000000000e+01)
findWidget('OOF2:Analysis Page:bottom:Sampling').get_vadjustment().set_value( 1.4850000000000e+01)
findWidget('OOF2:Analysis Page:bottom:Sampling').get_vadjustment().set_value( 1.6200000000000e+01)
findWidget('OOF2:Analysis Page:bottom:Sampling').get_vadjustment().set_value( 1.7550000000000e+01)
findWidget('OOF2:Analysis Page:bottom:Sampling').get_vadjustment().set_value( 2.0250000000000e+01)
findWidget('OOF2:Analysis Page:bottom:Sampling').get_vadjustment().set_value( 2.7000000000000e+01)
findWidget('OOF2:Analysis Page:bottom:Sampling').get_vadjustment().set_value( 2.5650000000000e+01)
findWidget('OOF2:Analysis Page:bottom:Sampling').get_vadjustment().set_value( 2.1600000000000e+01)
findWidget('OOF2:Analysis Page:bottom:Sampling').get_vadjustment().set_value( 1.7550000000000e+01)
findWidget('OOF2:Analysis Page:bottom:Sampling').get_vadjustment().set_value( 1.6200000000000e+01)
findWidget('OOF2:Analysis Page:bottom:Sampling').get_vadjustment().set_value( 1.4850000000000e+01)
findWidget('OOF2:Analysis Page:bottom:Sampling').get_vadjustment().set_value( 1.2150000000000e+01)
findWidget('OOF2:Analysis Page:bottom:Sampling').get_vadjustment().set_value( 5.4000000000000e+00)
findWidget('OOF2:Analysis Page:bottom:Sampling').get_vadjustment().set_value( 1.3500000000000e+00)
findWidget('OOF2:Analysis Page:bottom:Sampling').get_vadjustment().set_value( 0.0000000000000e+00)
setComboBox(findWidget('OOF2:Analysis Page:bottom:Sampling:Sampling:Chooser'), 'Line Points')
findWidget('OOF2:Analysis Page:Destination:New').clicked()
checkpoint toplevel widget mapped Dialog-Add a data destination
findWidget('Dialog-Add a data destination').resize(194, 72)
findWidget('Dialog-Add a data destination:filename').set_text('c')
findWidget('Dialog-Add a data destination:filename').set_text('cs')
findWidget('Dialog-Add a data destination:filename').set_text('cs.')
findWidget('Dialog-Add a data destination:filename').set_text('cs.d')
findWidget('Dialog-Add a data destination:filename').set_text('cs.da')
findWidget('Dialog-Add a data destination:filename').set_text('cs.dat')
findWidget('Dialog-Add a data destination:filename').set_text('cs.data')
findWidget('Dialog-Add a data destination:gtk-ok').clicked()
assert tests.goSensitive(1)
assert tests.csWidgetCheck1()
findWidget('OOF2:Analysis Page:Go').clicked()
checkpoint OOF.Mesh.Analyze.Direct_Output
findWidget('OOF2 Messages 1').resize(579, 200)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll').get_vadjustment().set_value( 2.3762376237624e+00)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll').get_vadjustment().set_value( 1.1881188118812e+01)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll').get_vadjustment().set_value( 3.0891089108911e+01)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll').get_vadjustment().set_value( 4.2772277227723e+01)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll').get_vadjustment().set_value( 5.9405940594059e+01)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll').get_vadjustment().set_value( 9.0297029702970e+01)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll').get_vadjustment().set_value( 1.9960396039604e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll').get_vadjustment().set_value( 2.4000000000000e+02)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll').get_hadjustment().set_value( 1.4489795918367e+00)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll').get_hadjustment().set_value( 4.3469387755102e+00)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll').get_hadjustment().set_value( 5.7959183673469e+00)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll').get_hadjustment().set_value( 1.0142857142857e+01)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll').get_hadjustment().set_value( 1.5938775510204e+01)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll').get_hadjustment().set_value( 2.1734693877551e+01)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll').get_hadjustment().set_value( 2.8979591836735e+01)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll').get_hadjustment().set_value( 5.3612244897959e+01)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll').get_hadjustment().set_value( 6.5204081632653e+01)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll').get_hadjustment().set_value( 7.1000000000000e+01)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Mesh Cross Section:Remove').clicked()
checkpoint Graphics_1 Mesh Cross Section sensitized
checkpoint OOF.Mesh.Cross_Section.Remove
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
assert tests.goSensitive(1)
assert tests.csWidgetCheck2()
findWidget('OOF2 Graphics 1').resize(800, 400)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Mesh Cross Section:Remove').clicked()
checkpoint Graphics_1 Mesh Cross Section sensitized
checkpoint OOF.Mesh.Cross_Section.Remove
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
assert tests.goSensitive(0)
assert tests.csWidgetCheck0()
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton Selection')
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(289)
findWidget('OOF2:Skeleton Selection Page:Pane:Groups:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new Element group
findWidget('Dialog-Create a new Element group').resize(249, 72)
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(289)
findWidget('Dialog-Create a new Element group:name:Auto').clicked()
findWidget('Dialog-Create a new Element group:name:Text').set_text('g')
findWidget('Dialog-Create a new Element group:name:Text').set_text('gr')
findWidget('Dialog-Create a new Element group:name:Text').set_text('gre')
findWidget('Dialog-Create a new Element group:name:Text').set_text('gree')
findWidget('Dialog-Create a new Element group:name:Text').set_text('green')
findWidget('Dialog-Create a new Element group:name:Text').set_text('green ')
findWidget('Dialog-Create a new Element group:name:Text').set_text('green e')
findWidget('Dialog-Create a new Element group:name:Text').set_text('green el')
findWidget('Dialog-Create a new Element group:name:Text').set_text('green ele')
findWidget('Dialog-Create a new Element group:name:Text').set_text('green elem')
findWidget('Dialog-Create a new Element group:name:Text').set_text('green eleme')
findWidget('Dialog-Create a new Element group:name:Text').set_text('green elemen')
findWidget('Dialog-Create a new Element group:name:Text').set_text('green element')
findWidget('Dialog-Create a new Element group:name:Text').set_text('green elements')
findWidget('Dialog-Create a new Element group:gtk-ok').clicked()
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.ElementGroup.New_Group
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(289)
setComboBox(findWidget('OOF2:Skeleton Selection Page:Pane:Selection:ElementAction:Chooser'), 'Select by Material')
setComboBox(findWidget('OOF2:Skeleton Selection Page:Pane:Selection:ElementAction:Select by Material:material'), 'green-material')
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:ElementHistory:OK').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(289)
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.ElementSelection.Select_by_Material
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(289)
findWidget('OOF2:Skeleton Selection Page:Pane:Groups:Add').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(289)
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint OOF.ElementGroup.Add_to_Group
findWidget('OOF2:Skeleton Selection Page:Pane:Selection:Clear').clicked()
findWidget('OOF2:Skeleton Selection Page:Pane').set_position(289)
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.ElementSelection.Clear
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Analysis')
setComboBox(findWidget('OOF2:Analysis Page:top:Domain:DomainRCF:Chooser'), 'Element Group')
setComboBox(findWidget('OOF2:Analysis Page:top:Domain:DomainRCF:Element Group:elements'), 'green elements')
assert tests.goSensitive(1)
assert tests.samplingOptions('Grid Points', 'Spaced Grid Points')
assert tests.samplingParams('Grid Points',                             ['x_points', 'y_points', 'show_x', 'show_y'])
setComboBox(findWidget('OOF2:Analysis Page:bottom:Operation:OperationRCF:Chooser'), 'Average')
assert tests.goSensitive(1)
assert tests.samplingOptions('Element Set', 'Grid Points', 'Spaced Grid Points')
assert tests.samplingParams('Grid Points', ['x_points', 'y_points'])
findWidget('OOF2:Analysis Page:bottom:Sampling:Sampling:Grid Points:x_points').set_text('')
findWidget('OOF2:Analysis Page:bottom:Sampling:Sampling:Grid Points:x_points').set_text('1')
findWidget('OOF2:Analysis Page:bottom:Sampling:Sampling:Grid Points:x_points').set_text('10')
findWidget('OOF2:Analysis Page:bottom:Sampling:Sampling:Grid Points:y_points').set_text('')
findWidget('OOF2:Analysis Page:bottom:Sampling:Sampling:Grid Points:y_points').set_text('1')
findWidget('OOF2:Analysis Page:bottom:Sampling:Sampling:Grid Points:y_points').set_text('10')
findWidget('OOF2:Analysis Page:Go').clicked()
checkpoint OOF.Mesh.Analyze.Average
assert tests.datacheck0()
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'FE Mesh')
findWidget('OOF2:FE Mesh Page:Pane').set_position(198)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton')
findWidget('OOF2:Skeleton Page:Pane').set_position(273)
findWidget('OOF2:Skeleton Page:New').clicked()
checkpoint toplevel widget mapped Dialog-New skeleton
findWidget('Dialog-New skeleton').resize(334, 152)
findWidget('Dialog-New skeleton:gtk-ok').clicked()
checkpoint skeleton page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint OOF.Skeleton.New
checkpoint skeleton page sensitized
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:Skeleton Page:Pane').set_position(273)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'FE Mesh')
findWidget('OOF2:FE Mesh Page:Pane').set_position(198)
setComboBox(findWidget('OOF2:FE Mesh Page:Skeleton'), 'skeleton<2>')
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
findWidget('OOF2:FE Mesh Page:Pane').set_position(198)
findWidget('OOF2:FE Mesh Page:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new mesh
findWidget('Dialog-Create a new mesh').resize(331, 188)
findWidget('Dialog-Create a new mesh:gtk-ok').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2:FE Mesh Page:Pane').set_position(198)
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
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Analysis')
assert tests.goSensitive(0)
assert tests.samplingParams('Grid Points', ['x_points', 'y_points']) ## ???
setComboBox(findWidget('OOF2:Analysis Page:Skeleton'), 'skeleton')
assert tests.goSensitive(1)
setComboBox(findWidget('OOF2:Analysis Page:top:Domain:DomainRCF:Element Group:elements'), 'green elements')
setComboBox(findWidget('OOF2:Analysis Page:Skeleton'), 'skeleton<2>')
assert tests.goSensitive(0)
setComboBox(findWidget('OOF2:Analysis Page:Skeleton'), 'skeleton')
setComboBox(findWidget('OOF2:Analysis Page:top:Domain:DomainRCF:Element Group:elements'), 'green elements')
findMenu(findWidget('OOF2:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(194, 72)
findWidget('Dialog-Python_Log:filename').set_text('a')
findWidget('Dialog-Python_Log:filename').set_text('an')
findWidget('Dialog-Python_Log:filename').set_text('ana')
findWidget('Dialog-Python_Log:filename').set_text('anal')
findWidget('Dialog-Python_Log:filename').set_text('analy')
findWidget('Dialog-Python_Log:filename').set_text('analyz')
findWidget('Dialog-Python_Log:filename').set_text('analyze')
findWidget('Dialog-Python_Log:filename').set_text('analyze.')
findWidget('Dialog-Python_Log:filename').set_text('analyze.l')
findWidget('Dialog-Python_Log:filename').set_text('analyze.lo')
findWidget('Dialog-Python_Log:filename').set_text('analyze.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('analyze.log')
findMenu(findWidget('OOF2:MenuBar'), 'File:Quit').activate()
