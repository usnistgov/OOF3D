# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.2 $
# $Author: fyc $
# $Date: 2014/06/19 15:29:44 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

import tests

#Check that the field is propagated when created.
#Is it usable?

findWidget('OOF3D').resize(550, 350)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Microstructure')
checkpoint page installed Microstructure
findWidget('OOF3D:Microstructure Page:Pane').set_position(225)
findWidget('OOF3D:Microstructure Page:Pane').set_position(156)
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized
findWidget('OOF3D:Microstructure Page:New').clicked()
checkpoint toplevel widget mapped Dialog-Create Microstructure
findWidget('Dialog-Create Microstructure').resize(315, 199)
findWidget('Dialog-Create Microstructure:gtk-ok').clicked()
findWidget('OOF3D:Microstructure Page:Pane').set_position(159)
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint active area status updated
checkpoint named analysis chooser set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint Field page sensitized
checkpoint Materials page updated
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page sensitized
checkpoint pinnodes page sensitized
checkpoint boundary page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint Solver page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint OOF.Microstructure.New
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Materials')
checkpoint Materials page updated
checkpoint page installed Materials
findWidget('OOF3D').resize(691, 350)
findWidget('OOF3D:Materials Page:Pane').set_position(278)
findWidget('OOF3D:Materials Page:Pane:Material:New').clicked()
checkpoint toplevel widget mapped Dialog-New material
findWidget('Dialog-New material').resize(300, 95)
findWidget('Dialog-New material:gtk-ok').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint OOF.Material.New
findWidget('OOF3D:Materials Page:Pane:Material:Assign').clicked()
checkpoint toplevel widget mapped Dialog-Assign material material to voxels
findWidget('Dialog-Assign material material to voxels').resize(278, 103)
setComboBox(findWidget('Dialog-Assign material material to voxels:pixels'), '<every>')
findWidget('Dialog-Assign material material to voxels:gtk-ok').clicked()
checkpoint OOF.Material.Assign
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton')
checkpoint page installed Skeleton
checkpoint skeleton page sensitized
findWidget('OOF3D').resize(691, 357)
findWidget('OOF3D:Skeleton Page:Pane').set_position(340)
checkpoint skeleton page sensitized
findWidget('OOF3D:Skeleton Page:New').clicked()
checkpoint toplevel widget mapped Dialog-New skeleton
findWidget('Dialog-New skeleton').resize(380, 191)
findWidget('Dialog-New skeleton:gtk-ok').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton page sensitized
checkpoint named analysis chooser set
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page sensitized
checkpoint pinnodes page sensitized
checkpoint boundary page updated
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
checkpoint skeleton page sensitized
checkpoint skeleton selection page selection sensitized
checkpoint Solver page sensitized
checkpoint OOF.Skeleton.New
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'FE Mesh')
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint page installed FE Mesh
findWidget('OOF3D:FE Mesh Page:Pane').set_position(445)
findWidget('OOF3D:FE Mesh Page:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new mesh
findWidget('Dialog-Create a new mesh').resize(345, 153)
findWidget('Dialog-Create a new mesh:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Mesh.New
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Fields & Equations')
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint page installed Fields & Equations
assert tests.fieldButtonCheck('Temperature',False,False)
assert tests.fieldButtonCheck('Displacement',False,False)
assert tests.fieldButtonCheck('Voltage',False,False)
assert tests.eqnButtonCheck('Heat_Eqn',False)
assert tests.eqnButtonCheck('Force_Balance',False)
assert tests.eqnButtonCheck('Coulomb_Eqn',False)
findWidget('OOF3D').resize(715, 357)
findWidget('OOF3D:Fields & Equations Page:HPane').set_position(320)
findWidget('OOF3D:Fields & Equations Page:HPane:Fields:Temperature defined').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Field.Define
assert tests.fieldButtonCheck('Temperature',True,False)
assert tests.fieldButtonCheck('Displacement',False,False)
assert tests.fieldButtonCheck('Voltage',False,False)
assert tests.eqnButtonCheck('Heat_Eqn',False)
assert tests.eqnButtonCheck('Force_Balance',False)
assert tests.eqnButtonCheck('Coulomb_Eqn',False)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Solver')
checkpoint Solver page sensitized
checkpoint page installed Solver
assert tests.solverSubproblemsPageSensitivityCheck0()
assert tests.solverFieldsPageSensitivityCheck0()
assert tests.solverSubproblemsCheck(['default'])
assert tests.solverFieldsCheck(['Temperature'])
findWidget('OOF3D').resize(715, 427)
findWidget('OOF3D:Solver Page:VPane').set_position(130)
findWidget('OOF3D:Solver Page:VPane:FieldInit:Scroll:Initializers').get_selection().select_path((0,))
checkpoint Solver page sensitized
assert tests.solverFieldsPageSensitivityCheck1()
findWidget('OOF3D:Solver Page:VPane:FieldInit:Scroll').get_vadjustment().set_value( 3.0000000000000e+00)
findWidget('OOF3D:Solver Page:VPane:FieldInit:Scroll').get_vadjustment().set_value( 0.0000000000000e+00)
findWidget('OOF3D:Solver Page:VPane:FieldInit:Scroll').get_vadjustment().set_value( 3.0000000000000e+00)
tree=findWidget('OOF3D:Solver Page:VPane:FieldInit:Scroll:Initializers')
column = tree.get_column(1)
tree.row_activated((0,), column)
checkpoint toplevel widget mapped Dialog-Initialize field Temperature
findWidget('Dialog-Initialize field Temperature').resize(253, 97)
findWidget('Dialog-Initialize field Temperature:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Solver page sensitized
findWidget('OOF3D:Solver Page:VPane:FieldInit:Scroll:Initializers').get_selection().unselect_all()
checkpoint Solver page sensitized
findWidget('OOF3D:Solver Page:VPane:FieldInit:Scroll:Initializers').get_selection().select_path((0,))
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Set_Field_Initializer
findWidget('OOF3D:Solver Page:VPane:FieldInit:Apply').clicked()
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
findWidget('OOF3D:Solver Page:VPane:FieldInit:Scroll:Initializers').get_selection().unselect_all()
checkpoint Solver page sensitized
findWidget('OOF3D:Solver Page:VPane:FieldInit:Scroll:Initializers').get_selection().select_path((0,))
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Apply_Field_Initializers
findMenu(findWidget('OOF3D:MenuBar'), 'Windows:Graphics:New').activate()
checkpoint Move Node toolbox info updated
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint toplevel widget mapped OOF3D Graphics 1
findWidget('OOF3D Graphics 1').resize(1000, 800)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 705))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
checkpoint OOF.Windows.Graphics.New
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 705))
findWidget('OOF3D Graphics 1').resize(1000, 800)
findWidget('OOF3D').resize(715, 427)
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 703))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 703))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 683))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 683))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 662))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 662))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 639))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 639))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 626))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 626))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 621))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 621))
findWidget('OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame').size_allocate(gtk.gdk.Rectangle(0, 29, 380, 608))
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 608))
findMenu(findWidget('OOF3D Graphics 1:MenuBar'), 'Layer:New').activate()
checkpoint toplevel widget mapped Dialog-New
findWidget('Dialog-New').resize(291, 191)
setComboBox(findWidget('Dialog-New:category'), 'Microstructure')
findWidget('Dialog-New').resize(404, 391)
setComboBox(findWidget('Dialog-New:how:Material:no_material:Chooser'), 'RGBColor')
findWidget('Dialog-New').resize(404, 435)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Red:slider').get_adjustment().set_value( 1.5384615384615e-02)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Red:slider').get_adjustment().set_value( 3.0769230769231e-02)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Red:slider').get_adjustment().set_value( 4.6153846153846e-02)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Red:slider').get_adjustment().set_value( 7.6923076923077e-02)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Red:slider').get_adjustment().set_value( 9.2307692307692e-02)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Red:slider').get_adjustment().set_value( 1.0769230769231e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Red:slider').get_adjustment().set_value( 1.2307692307692e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Red:slider').get_adjustment().set_value( 1.3846153846154e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Red:slider').get_adjustment().set_value( 1.6923076923077e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Red:slider').get_adjustment().set_value( 1.8461538461538e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Red:slider').get_adjustment().set_value( 2.0000000000000e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Red:slider').get_adjustment().set_value( 2.1538461538462e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Green:slider').get_adjustment().set_value( 1.5384615384615e-02)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Green:slider').get_adjustment().set_value( 3.0769230769231e-02)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Green:slider').get_adjustment().set_value( 4.6153846153846e-02)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Green:slider').get_adjustment().set_value( 6.1538461538462e-02)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Green:slider').get_adjustment().set_value( 7.6923076923077e-02)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Green:slider').get_adjustment().set_value( 9.2307692307692e-02)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Green:slider').get_adjustment().set_value( 1.0769230769231e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Green:slider').get_adjustment().set_value( 1.2307692307692e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Green:slider').get_adjustment().set_value( 1.3846153846154e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Green:slider').get_adjustment().set_value( 1.5384615384615e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Green:slider').get_adjustment().set_value( 1.6923076923077e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Green:slider').get_adjustment().set_value( 1.8461538461538e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Green:slider').get_adjustment().set_value( 2.0000000000000e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Green:slider').get_adjustment().set_value( 2.1538461538462e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Green:slider').get_adjustment().set_value( 2.3076923076923e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Green:slider').get_adjustment().set_value( 2.4615384615385e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Green:slider').get_adjustment().set_value( 2.6153846153846e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Blue:slider').get_adjustment().set_value( 1.5384615384615e-02)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Blue:slider').get_adjustment().set_value( 3.0769230769231e-02)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Blue:slider').get_adjustment().set_value( 4.6153846153846e-02)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Blue:slider').get_adjustment().set_value( 6.1538461538462e-02)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Blue:slider').get_adjustment().set_value( 7.6923076923077e-02)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Blue:slider').get_adjustment().set_value( 9.2307692307692e-02)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Blue:slider').get_adjustment().set_value( 1.0769230769231e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Blue:slider').get_adjustment().set_value( 1.2307692307692e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Blue:slider').get_adjustment().set_value( 1.3846153846154e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Blue:slider').get_adjustment().set_value( 1.5384615384615e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Blue:slider').get_adjustment().set_value( 1.6923076923077e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Blue:slider').get_adjustment().set_value( 1.8461538461538e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Blue:slider').get_adjustment().set_value( 2.0000000000000e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Blue:slider').get_adjustment().set_value( 2.1538461538462e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Blue:slider').get_adjustment().set_value( 2.3076923076923e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Blue:slider').get_adjustment().set_value( 2.4615384615385e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Blue:slider').get_adjustment().set_value( 2.6153846153846e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Blue:slider').get_adjustment().set_value( 2.7692307692308e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Blue:slider').get_adjustment().set_value( 2.9230769230769e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Blue:slider').get_adjustment().set_value( 3.0769230769231e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Blue:slider').get_adjustment().set_value( 3.2307692307692e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Blue:slider').get_adjustment().set_value( 3.3846153846154e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Blue:slider').get_adjustment().set_value( 3.5384615384615e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Blue:slider').get_adjustment().set_value( 3.6923076923077e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Blue:slider').get_adjustment().set_value( 3.8461538461538e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Blue:slider').get_adjustment().set_value( 4.0000000000000e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Green:slider').get_adjustment().set_value( 2.7692307692308e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Green:slider').get_adjustment().set_value( 2.9230769230769e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Green:slider').get_adjustment().set_value( 3.0769230769231e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Green:slider').get_adjustment().set_value( 3.2307692307692e-01)
findWidget('Dialog-New:how:Material:no_material:RGBColor:Green:slider').get_adjustment().set_value( 3.3846153846154e-01)
findWidget('Dialog-New:gtk-ok').clicked()
findWidget('OOF3D Messages 1').resize(603, 200)
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.New
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 608))
findWidget('OOF3D Graphics 1:Pane0:Pane2:tumble').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 608))
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 574)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 8.6000000000000e+01,y= 9.4000000000000e+01,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 574)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 1.1200000000000e+02,y= 1.1700000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 608))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D Graphics 1:Pane0:LayerScroll').get_vadjustment().set_value( 2.0000000000000e+00)
tree=findWidget('OOF3D Graphics 1:Pane0:LayerScroll:LayerList')
column = tree.get_column(2)
tree.row_activated((14,), column)
checkpoint toplevel widget mapped Dialog-Edit Graphics Layer
findWidget('Dialog-Edit Graphics Layer').resize(404, 435)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Red:slider').get_adjustment().set_value( 1.5384615384615e-02)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Red:slider').get_adjustment().set_value( 3.0769230769231e-02)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Red:slider').get_adjustment().set_value( 4.6153846153846e-02)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Red:slider').get_adjustment().set_value( 6.1538461538462e-02)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Red:slider').get_adjustment().set_value( 7.6923076923077e-02)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Red:slider').get_adjustment().set_value( 9.2307692307692e-02)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Red:slider').get_adjustment().set_value( 1.0769230769231e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Red:slider').get_adjustment().set_value( 1.2307692307692e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Red:slider').get_adjustment().set_value( 1.3846153846154e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Red:slider').get_adjustment().set_value( 1.5384615384615e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Red:slider').get_adjustment().set_value( 1.6923076923077e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Red:slider').get_adjustment().set_value( 1.8461538461538e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Green:slider').get_adjustment().set_value( 1.5384615384615e-02)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Green:slider').get_adjustment().set_value( 3.0769230769231e-02)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Green:slider').get_adjustment().set_value( 4.6153846153846e-02)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Green:slider').get_adjustment().set_value( 6.1538461538462e-02)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Green:slider').get_adjustment().set_value( 7.6923076923077e-02)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Green:slider').get_adjustment().set_value( 9.2307692307692e-02)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Green:slider').get_adjustment().set_value( 1.0769230769231e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Green:slider').get_adjustment().set_value( 1.2307692307692e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 9.8461538461538e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 9.6923076923077e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 9.3846153846154e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 9.2307692307692e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 8.9230769230769e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 8.7692307692308e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 8.4615384615385e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 8.3076923076923e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 8.0000000000000e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 7.8461538461538e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 7.5384615384615e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 7.3846153846154e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 7.2307692307692e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 7.0769230769231e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 6.9230769230769e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 6.7692307692308e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 6.6153846153846e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 6.4615384615385e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 6.3076923076923e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 6.1538461538462e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 6.0000000000000e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 5.8461538461538e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 5.6923076923077e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 5.5384615384615e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 5.3846153846154e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 5.2307692307692e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 5.0769230769231e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 4.9230769230769e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 4.7692307692308e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 4.6153846153846e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 4.4615384615385e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 4.3076923076923e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 4.1538461538462e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 4.0000000000000e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 3.8461538461538e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 3.6923076923077e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 3.5384615384615e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 3.3846153846154e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 3.2307692307692e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 3.0769230769231e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 2.9230769230769e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 2.7692307692308e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 2.6153846153846e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 2.4615384615385e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 2.3076923076923e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 2.1538461538462e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Blue:slider').get_adjustment().set_value( 2.0000000000000e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Green:slider').get_adjustment().set_value( 1.3846153846154e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Green:slider').get_adjustment().set_value( 1.5384615384615e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Green:slider').get_adjustment().set_value( 1.6923076923077e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Green:slider').get_adjustment().set_value( 1.8461538461538e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Green:slider').get_adjustment().set_value( 2.0000000000000e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Green:slider').get_adjustment().set_value( 2.1538461538462e-01)
findWidget('Dialog-Edit Graphics Layer:how:Material:no_color:RGBColor:Green:slider').get_adjustment().set_value( 2.3076923076923e-01)
findWidget('Dialog-Edit Graphics Layer:gtk-ok').clicked()
checkpoint Graphics_1 Voxel Info updated
checkpoint Graphics_1 Pin Nodes updated
checkpoint OOF.Graphics_1.Layer.Edit
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 574)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_PRESS,x= 3.5800000000000e+02,y= 2.4000000000000e+02,button=1,state=16,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
window = findOOFWindow('Graphics_1')
oldsize = window.setCanvasSize(614, 574)
canvasobj = findCanvasDrawingArea(findWidget('OOF3D Graphics 1:Pane0:Pane2:Canvas'), windowname='Graphics_1')
canvasobj.emit('event', event(gtk.gdk.BUTTON_RELEASE,x= 3.9500000000000e+02,y= 3.3600000000000e+02,button=1,state=272,window=findCanvasGdkWindow('Graphics_1')))
window.setCanvasSize(oldsize[0], oldsize[1])
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 608))
checkpoint OOF.Graphics_1.Settings.Camera.View
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 608))
findWidget('OOF3D Graphics 1:Pane0:Pane2:fill').clicked()
findWidget('OOF3D Graphics 1:Pane0:Pane2').size_allocate(gtk.gdk.Rectangle(0, 29, 1000, 608))
findMenu(findWidget('OOF3D:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(190, 92)
findWidget('Dialog-Python_Log:filename').set_text('ftest.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('ftest.log')
widget_2=findWidget('OOF3D')
handled_2=widget_2.event(event(gtk.gdk.DELETE,window=widget_2.window))
postpone if not handled_2: widget_2.destroy()
checkpoint OOF.Graphics_1.File.Close
