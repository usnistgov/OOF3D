checkpoint toplevel widget mapped OOF2 Activity Viewer
# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:13:20 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov.

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
checkpoint active area status updated
checkpoint pixel page updated
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
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton')
findWidget('OOF2').resize(593, 434)
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
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
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
findWidget('OOF2:Navigation:Prev').clicked()
findWidget('OOF2:Navigation:Prev').clicked()
findWidget('OOF2').resize(684, 434)
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Material:New').clicked()
checkpoint toplevel widget mapped Dialog-New material
findWidget('Dialog-New material').resize(249, 72)
findWidget('Dialog-New material:gtk-ok').clicked()
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Material.New
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((0,))
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').expand_row((1,), open_all=False)
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').expand_row((1, 0), open_all=False)
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((1, 0, 0))
widget_0=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_0.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_0.window))
widget_1=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_1.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_1.window))
tree=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
column = tree.get_column(0)
tree.row_activated((1, 0, 0), column)
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Isotropic
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic').resize(372, 244)
setComboBox(findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic:cijkl:Chooser'), 'E and nu')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic:cijkl:E and nu:young').set_text('')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic:cijkl:E and nu:young').set_text('1')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic:cijkl:E and nu:young').set_text('10')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic:gtk-ok').clicked()
checkpoint OOF.Property.Parametrize.Mechanical.Elasticity.Isotropic
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:Add').clicked()
findWidget('OOF2:Materials Page:Pane').set_position(272)
checkpoint OOF.Material.Add_property
findWidget('OOF2:Materials Page:Pane:Material:Assign').clicked()
checkpoint toplevel widget mapped Dialog-Assign material material to pixels
findWidget('Dialog-Assign material material to pixels').resize(268, 108)
setComboBox(findWidget('Dialog-Assign material material to pixels:pixels'), '<all>')
findWidget('Dialog-Assign material material to pixels:gtk-ok').clicked()
checkpoint OOF.Material.Assign
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'FE Mesh')
findWidget('OOF2').resize(684, 482)
findWidget('OOF2:FE Mesh Page:Pane').set_position(265)
findWidget('OOF2:FE Mesh Page:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new mesh
findWidget('Dialog-Create a new mesh').resize(331, 188)
findWidget('Dialog-Create a new mesh:gtk-ok').clicked()
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
findWidget('OOF2:FE Mesh Page:Pane').set_position(265)
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2:Fields & Equations Page:HPane').set_position(153)
findWidget('OOF2:Fields & Equations Page:HPane:Fields:Displacement defined').clicked()
checkpoint OOF.Subproblem.Field.Define
findWidget('OOF2:Fields & Equations Page:HPane:Fields:Displacement active').clicked()
checkpoint OOF.Subproblem.Field.Activate
findWidget('OOF2:Fields & Equations Page:HPane:Fields:Displacement in-plane').clicked()
checkpoint OOF.Mesh.Field.In_Plane
findWidget('OOF2:Fields & Equations Page:HPane:Equations:Force_Balance active').clicked()
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Subproblem.Equation.Activate
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(336)
findWidget('OOF2:Boundary Conditions Page:Pane:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(399, 300)
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(336)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'bottomleft')
findWidget('Dialog-New Boundary Condition:gtk-apply').clicked()
findWidget('OOF2 Messages 1').resize(792, 200)
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(336)
checkpoint OOF.Mesh.Boundary_Conditions.New
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:eqn_component'), 'y')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:field_component'), 'y')
findWidget('Dialog-New Boundary Condition:gtk-apply').clicked()
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(336)
checkpoint OOF.Mesh.Boundary_Conditions.New
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'topright')
findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Constant Profile:value').set_text('0.')
findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Constant Profile:value').set_text('0.1')
findWidget('Dialog-New Boundary Condition:gtk-apply').clicked()
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(336)
checkpoint OOF.Mesh.Boundary_Conditions.New
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:eqn_component'), 'x')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:field_component'), 'x')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(336)
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2:Navigation:Next').clicked()
#findWidget('OOF2:Solver Page:Solve').clicked()

findWidget('OOF2:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList').get_selection().select_path((0,))
findWidget('OOF2:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(423, 212)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF2:Solver Page:end').set_text('0')
findWidget('OOF2:Solver Page:solve').clicked()
checkpoint OOF.Mesh.Solve

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
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
setComboBox(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBChooser'), 'Mesh Info')
checkpoint Graphics_1 Mesh Info sensitized
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:TBScroll:Mesh Info:NewDataViewer').clicked()
checkpoint Mesh_Data_1 mesh updated
checkpoint toplevel widget mapped Mesh Data 1
checkpoint Mesh_Data_1 data updated
findWidget('Mesh Data 1').resize(301, 278)
assert tests.dataWidgets()
setComboBox(findWidget('Mesh Data 1:ViewSource:output:output_0'), 'Strain')
checkpoint Mesh_Data_1 data updated
assert tests.dataWidgets()
findWidget('Mesh Data 1').resize(370, 282)
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 1.0450000000000e+00,y=-1.0450000000000e+00,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.0450000000000e+00,y=-1.0450000000000e+00,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Mesh_Data_1 position updated
checkpoint Mesh_Data_1 data updated
assert tests.dataWidgets('xy', 'xz', 'yz', 'zz', 'yy', 'xx')
checkpoint OOF.Graphics_1.Toolbox.Mesh_Info.QueryElement
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('Mesh Data 1').resize(510, 370)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('Mesh Data 1').resize(510, 370)
setComboBox(findWidget('Mesh Data 1:ViewSource:output:output_1'), 'Invariant')
findWidget('Mesh Data 1').resize(510, 402)
checkpoint Mesh_Data_1 data updated
assert tests.dataWidgets('generic')
setComboBox(findWidget('Mesh Data 1:ViewSource:output:Parameters:type:Chooser'), 'Elastic Strain')
checkpoint Mesh_Data_1 data updated
checkpoint Mesh_Data_1 data updated
assert tests.dataWidgets('generic')
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 6.2413043478261e-01,y=-9.2543478260870e-01,state=0,window=findCanvasGdkWindow('Graphics_1')))
canvasobj = findCanvasRoot(findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 6.2413043478261e-01,y=-9.2543478260870e-01,state=256,window=findCanvasGdkWindow('Graphics_1')))
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Mesh_Data_1 position updated
checkpoint Mesh_Data_1 data updated
checkpoint OOF.Graphics_1.Toolbox.Mesh_Info.QueryElement
assert tests.dataWidgets('generic')
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.5263157894737e+00)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 7.5789473684211e+00)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.2631578947368e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 1.7684210526316e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.7789473684211e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 3.0315789473684e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 3.5368421052632e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 3.7894736842105e+01)
findWidget('OOF2 Graphics 1:Pane0:LayerScroll:LayerList').get_selection().select_path((10,))
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 3.7000000000000e+01)
checkpoint OOF.Graphics_1.Layer.Select
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'Layer:Delete').activate()
findWidget('OOF2 Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.6000000000000e+01)
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint Mesh_Data_1 mesh updated
checkpoint Mesh_Data_1 data updated
checkpoint Mesh_Data_1 data updated
checkpoint OOF.Graphics_1.Layer.Delete
assert tests.dataWidgets()
findMenu(findWidget('OOF2 Graphics 1:MenuBar'), 'File:Quit').activate()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(358, 94)
findWidget('Questioner:gtk-delete').clicked()
