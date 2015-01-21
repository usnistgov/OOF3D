checkpoint toplevel widget mapped OOF2 Activity Viewer
# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:12:17 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov.

# Some "checkpoint Graphics_1 Mesh Info sensitized" lines were
# inserted by hand to get some "checkpoint_count" calls to pass.  This
# test should probably be re-recorded.

import tests

setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Boundary Analysis')
findWidget('OOF2:Boundary Analysis Page:Pane:frame').size_allocate(gtk.gdk.Rectangle(4, 102, 181, 164))
findWidget('OOF2:Boundary Analysis Page:Pane:frame').size_allocate(gtk.gdk.Rectangle(4, 102, 181, 164))
assert tests.goSensitive(0)
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
checkpoint interface page updated
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
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((0,))
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').expand_row((1,), open_all=False)
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').expand_row((1, 0), open_all=False)
findWidget('OOF2:Materials Page:Pane').set_position(272)
findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((1, 0, 0))
widget_0=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_0.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_0.window))
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
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton')
findWidget('OOF2').resize(684, 434)
findWidget('OOF2:Skeleton Page:Pane').set_position(340)
findWidget('OOF2:Skeleton Page:New').clicked()
checkpoint toplevel widget mapped Dialog-New skeleton
checkpoint skeleton page sensitized
findWidget('Dialog-New skeleton').resize(334, 152)
findWidget('Dialog-New skeleton:x_elements').set_text('')
findWidget('Dialog-New skeleton:x_elements').set_text('1')
findWidget('Dialog-New skeleton:x_elements').set_text('10')
findWidget('Dialog-New skeleton:y_elements').set_text('')
findWidget('Dialog-New skeleton:y_elements').set_text('1')
findWidget('Dialog-New skeleton:y_elements').set_text('10')
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
findWidget('OOF2:Skeleton Page:Pane').set_position(340)
checkpoint skeleton selection page updated
checkpoint OOF.Skeleton.New
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'FE Mesh')
findWidget('OOF2').resize(684, 482)
findWidget('OOF2:FE Mesh Page:Pane').set_position(265)
findWidget('OOF2:FE Mesh Page:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new mesh
findWidget('Dialog-Create a new mesh').resize(331, 188)
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
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Boundary Analysis')
findWidget('OOF2:Boundary Analysis Page:Pane:frame').size_allocate(gtk.gdk.Rectangle(4, 102, 226, 296))
assert tests.goSensitive(0)
assert tests.bdyList("top", "bottom", "right", "left")
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Fields & Equations')
findWidget('OOF2:Fields & Equations Page:HPane').set_position(153)
findWidget('OOF2:Fields & Equations Page:HPane:Fields:Temperature defined').clicked()
checkpoint OOF.Subproblem.Field.Define
findWidget('OOF2:Fields & Equations Page:HPane:Fields:Displacement defined').clicked()
checkpoint OOF.Subproblem.Field.Define
# findWidget('OOF2:Fields & Equations Page:HPane:InitScroll:Initializers').get_selection().select_path((0,))
# tree=findWidget('OOF2:Fields & Equations Page:HPane:InitScroll:Initializers')
# column = tree.get_column(1)
# tree.row_activated((0,), column)
# checkpoint toplevel widget mapped Dialog-Initialize field Temperature
# findWidget('Dialog-Initialize field Temperature').resize(239, 104)
# setComboBox(findWidget('Dialog-Initialize field Temperature:initializer:Chooser'), 'XYFunction')
# findWidget('Dialog-Initialize field Temperature').resize(253, 104)
# findWidget('Dialog-Initialize field Temperature:initializer:XYFunction:function').set_text('x')
# findWidget('Dialog-Initialize field Temperature:initializer:XYFunction:function').set_text('x*')
# findWidget('Dialog-Initialize field Temperature:initializer:XYFunction:function').set_text('x*y')
# findWidget('Dialog-Initialize field Temperature:initializer:XYFunction:function').set_text('x*y*')
# findWidget('Dialog-Initialize field Temperature:initializer:XYFunction:function').set_text('x*y*y')
# findWidget('Dialog-Initialize field Temperature:gtk-ok').clicked()
# findWidget('OOF2:Fields & Equations Page:HPane:InitScroll:Initializers').get_selection().unselect_all()
# findWidget('OOF2:Fields & Equations Page:HPane:InitScroll:Initializers').get_selection().select_path((0,))
# checkpoint OOF.Mesh.Set_Field_Initializer
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Solver')
findWidget('OOF2').resize(705, 477)
findWidget('OOF2:Solver Page:VPane').set_position(151)
findWidget('OOF2:Solver Page:VPane').set_position(326)
findWidget('OOF2:Solver Page:VPane:FieldInit:Scroll:Initializers').get_selection().select_path((0,))
tree=findWidget('OOF2:Solver Page:VPane:FieldInit:Scroll:Initializers')
column = tree.get_column(1)
tree.row_activated((0,), column)
checkpoint toplevel widget mapped Dialog-Initialize field Temperature
findWidget('Dialog-Initialize field Temperature').resize(232, 100)
setComboBox(findWidget('Dialog-Initialize field Temperature:initializer:Chooser'), 'XYFunction')
findWidget('Dialog-Initialize field Temperature').resize(247, 100)
findWidget('Dialog-Initialize field Temperature:initializer:XYFunction:function').set_text('x')
findWidget('Dialog-Initialize field Temperature:initializer:XYFunction:function').set_text('x*')
findWidget('Dialog-Initialize field Temperature:initializer:XYFunction:function').set_text('x*y')
findWidget('Dialog-Initialize field Temperature:initializer:XYFunction:function').set_text('x*y*')
findWidget('Dialog-Initialize field Temperature:initializer:XYFunction:function').set_text('x*y*y')
findWidget('Dialog-Initialize field Temperature:gtk-ok').clicked()
findWidget('OOF2:Solver Page:VPane:FieldInit:Scroll:Initializers').get_selection().unselect_all()
findWidget('OOF2:Solver Page:VPane:FieldInit:Scroll:Initializers').get_selection().select_path((0,))
checkpoint OOF.Mesh.Set_Field_Initializer
findWidget('OOF2:Solver Page:VPane:FieldInit:Apply').clicked()
checkpoint OOF.Mesh.Apply_Field_Initializers

setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Boundary Analysis')
assert tests.goSensitive(0)
findWidget('OOF2:Boundary Analysis Page:Pane:frame').size_allocate(gtk.gdk.Rectangle(4, 102, 190, 296))
findWidget('OOF2:Boundary Analysis Page:Pane:frame:BoundaryListScroll:BoundaryList').get_selection().select_path((0,))
assert tests.goSensitive(1)
findWidget('OOF2:Boundary Analysis Page:Go').clicked()
checkpoint OOF.Mesh.Boundary_Analysis.Analyze
# Analysis on top boundary completed.
assert tests.msgFloat(0.0, 0.5)
findWidget('OOF2:Boundary Analysis Page:Pane:frame:BoundaryListScroll:BoundaryList').get_selection().select_path((1,))
tree=findWidget('OOF2:Boundary Analysis Page:Pane:frame:BoundaryListScroll:BoundaryList')
column = tree.get_column(0)
tree.row_activated((3,), column)
checkpoint OOF.Mesh.Boundary_Analysis.Analyze
# Analysis on bottom boundary completed.
assert tests.msgFloat(0.0, 0.0)
findWidget('OOF2').resize(684, 482)
findWidget('OOF2:Boundary Analysis Page:Pane:frame:BoundaryListScroll:BoundaryList').get_selection().select_path((3,))
tree=findWidget('OOF2:Boundary Analysis Page:Pane:frame:BoundaryListScroll:BoundaryList')
column = tree.get_column(0)
tree.row_activated((2,), column)
checkpoint OOF.Mesh.Boundary_Analysis.Analyze
# Analysis on left boundary completed.
assert tests.msgFloat(0.0, 0.0)
findWidget('OOF2:Boundary Analysis Page:Pane:frame:BoundaryListScroll:BoundaryList').get_selection().select_path((2,))
tree=findWidget('OOF2:Boundary Analysis Page:Pane:frame:BoundaryListScroll:BoundaryList')
column = tree.get_column(0)
tree.row_activated((1,), column)
checkpoint OOF.Mesh.Boundary_Analysis.Analyze
# Analysis on right boundary completed.
assert tests.msgFloat(0.0, 0.335)
setComboBox(findWidget('OOF2:Boundary Analysis Page:Pane:BdyAnalyzerRCF:Average Field:field'), 'Displacement')
findWidget('OOF2:Boundary Analysis Page:Pane:frame:BoundaryListScroll:BoundaryList').get_selection().select_path((0,))
tree=findWidget('OOF2:Boundary Analysis Page:Pane:frame:BoundaryListScroll:BoundaryList')
column = tree.get_column(0)
tree.row_activated((0,), column)
checkpoint OOF.Mesh.Boundary_Analysis.Analyze
# Analysis on top boundary completed.
assert tests.msgFloat(0, 0, 0)
findWidget('OOF2:Boundary Analysis Page:Pane:frame:BoundaryListScroll:BoundaryList').get_selection().select_path((2,))
findWidget('OOF2:Boundary Analysis Page:Go').clicked()
checkpoint OOF.Mesh.Boundary_Analysis.Analyze
# Analysis on right boundary completed.
assert tests.msgFloat(0, 0, 0)
findWidget('OOF2:Boundary Analysis Page:Pane:frame:BoundaryListScroll:BoundaryList').get_selection().select_path((3,))
findWidget('OOF2:Boundary Analysis Page:Go').clicked()
checkpoint OOF.Mesh.Boundary_Analysis.Analyze
# Analysis on left boundary completed.
assert tests.msgFloat(0, 0, 0)
findWidget('OOF2:Boundary Analysis Page:Pane:frame:BoundaryListScroll:BoundaryList').get_selection().select_path((1,))
findWidget('OOF2:Boundary Analysis Page:Go').clicked()
checkpoint OOF.Mesh.Boundary_Analysis.Analyze
# Analysis on bottom boundary completed.
assert tests.msgFloat(0, 0, 0)
setComboBox(findWidget('OOF2:Boundary Analysis Page:Pane:BdyAnalyzerRCF:Chooser'), 'Integrate Flux')
findWidget('OOF2:Boundary Analysis Page:Pane:frame').size_allocate(gtk.gdk.Rectangle(4, 102, 226, 296))
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Fields & Equations')
findWidget('OOF2:Fields & Equations Page:HPane:Equations:Force_Balance active').clicked()
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Subproblem.Equation.Activate
findWidget('OOF2:Fields & Equations Page:HPane:Fields:Displacement active').clicked()
checkpoint OOF.Subproblem.Field.Activate
findWidget('OOF2:Fields & Equations Page:HPane:Fields:Displacement in-plane').clicked()
checkpoint OOF.Mesh.Field.In_Plane
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Boundary Analysis')
findWidget('OOF2:Boundary Analysis Page:Pane:frame').size_allocate(gtk.gdk.Rectangle(4, 102, 226, 296))
assert tests.goSensitive(1)
findWidget('OOF2:Boundary Analysis Page:Pane:frame:BoundaryListScroll:BoundaryList').get_selection().select_path((1,))
findWidget('OOF2:Boundary Analysis Page:Go').clicked()
checkpoint OOF.Mesh.Boundary_Analysis.Analyze
findWidget('OOF2:Boundary Analysis Page:Pane:frame:BoundaryListScroll:BoundaryList').get_selection().select_path((3,))
findWidget('OOF2:Boundary Analysis Page:Go').clicked()
checkpoint OOF.Mesh.Boundary_Analysis.Analyze
findWidget('OOF2:Boundary Analysis Page:Pane:frame:BoundaryListScroll:BoundaryList').get_selection().select_path((2,))
findWidget('OOF2:Boundary Analysis Page:Go').clicked()
checkpoint OOF.Mesh.Boundary_Analysis.Analyze
findWidget('OOF2:Boundary Analysis Page:Pane:frame:BoundaryListScroll:BoundaryList').get_selection().select_path((0,))
findWidget('OOF2:Boundary Analysis Page:Go').clicked()
checkpoint OOF.Mesh.Boundary_Analysis.Analyze
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Boundary Conditions')
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(336)
findWidget('OOF2:Boundary Conditions Page:Pane:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(399, 288)
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(336)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:field'), 'Displacement')
findWidget('Dialog-New Boundary Condition').resize(399, 300)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'left')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Continuum Profile:function').set_text('1.0')
findWidget('Dialog-New Boundary Condition:gtk-apply').clicked()
checkpoint OOF.Mesh.Boundary_Conditions.New
# Boundary condition set.
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:field_component'), 'y')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:eqn_component'), 'y')
findWidget('Dialog-New Boundary Condition:gtk-apply').clicked()
checkpoint OOF.Mesh.Boundary_Conditions.New
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'right')
findWidget('Dialog-New Boundary Condition:gtk-apply').clicked()
checkpoint OOF.Mesh.Boundary_Conditions.New
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:field_component'), 'x')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:eqn_component'), 'x')
findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Continuum Profile:function').set_text('')
findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Continuum Profile:function').set_text('0')
findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Continuum Profile:function').set_text('0.')
findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Continuum Profile:function').set_text('0.1')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint OOF.Mesh.Boundary_Conditions.New
checkpoint_count("OOF.Mesh.Boundary_Conditions.New")

# Boundary condition set.
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Solver')
# findWidget('OOF2:Solver Page:Solve').clicked()
# checkpoint OOF.Solver.Solve
findWidget('OOF2:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList').get_selection().select_path((0,))
findWidget('OOF2:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(398, 212)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF2:Solver Page:end').set_text('0')
findWidget('OOF2:Solver Page:solve').clicked()
checkpoint OOF.Mesh.Solve

findMenu(findWidget('OOF2:MenuBar'), 'Windows:Graphics:New').activate()
checkpoint Move Node toolbox info updated
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
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Boundary Conditions')
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(336)
findWidget('OOF2:Boundary Conditions Page:Pane:Condition:BCScroll').get_hadjustment().set_value( 2.8285714285714e+00)
findWidget('OOF2:Boundary Conditions Page:Pane:Condition:BCScroll').get_hadjustment().set_value( 3.6771428571429e+01)
findWidget('OOF2:Boundary Conditions Page:Pane:Condition:BCScroll').get_hadjustment().set_value( 5.9400000000000e+01)
findWidget('OOF2:Boundary Conditions Page:Pane:Condition:BCScroll').get_hadjustment().set_value( 9.9000000000000e+01)
findWidget('OOF2:Boundary Conditions Page:Pane:Condition:BCScroll:BCList').get_selection().select_path((0,))
tree=findWidget('OOF2:Boundary Conditions Page:Pane:Condition:BCScroll:BCList')
column = tree.get_column(1)
tree.row_activated((0,), column)
checkpoint toplevel widget mapped Dialog-Edit Boundary Condition
findWidget('Dialog-Edit Boundary Condition').resize(399, 276)
setComboBox(findWidget('Dialog-Edit Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-Edit Boundary Condition:condition:Dirichlet:profile:Continuum Profile:function').set_text('')
findWidget('Dialog-Edit Boundary Condition:condition:Dirichlet:profile:Continuum Profile:function').set_text('0')
findWidget('Dialog-Edit Boundary Condition:gtk-ok').clicked()
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(336)
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint_count("Graphics_1 Mesh Info sensitized")
checkpoint OOF.Mesh.Boundary_Conditions.Edit
findWidget('OOF2:Boundary Conditions Page:Pane:Condition:BCScroll:BCList').get_selection().select_path((1,))
tree=findWidget('OOF2:Boundary Conditions Page:Pane:Condition:BCScroll:BCList')
column = tree.get_column(1)
tree.row_activated((1,), column)
checkpoint toplevel widget mapped Dialog-Edit Boundary Condition
findWidget('Dialog-Edit Boundary Condition').resize(399, 276)
setComboBox(findWidget('Dialog-Edit Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-Edit Boundary Condition:condition:Dirichlet:profile:Continuum Profile:function').set_text('')
findWidget('Dialog-Edit Boundary Condition:condition:Dirichlet:profile:Continuum Profile:function').set_text('0')
findWidget('Dialog-Edit Boundary Condition:gtk-ok').clicked()
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(336)
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint OOF.Mesh.Boundary_Conditions.Edit
findWidget('OOF2:Boundary Conditions Page:Pane:Condition:BCScroll:BCList').get_selection().select_path((2,))
tree=findWidget('OOF2:Boundary Conditions Page:Pane:Condition:BCScroll:BCList')
column = tree.get_column(1)
tree.row_activated((2,), column)
checkpoint toplevel widget mapped Dialog-Edit Boundary Condition
findWidget('Dialog-Edit Boundary Condition').resize(399, 276)
setComboBox(findWidget('Dialog-Edit Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-Edit Boundary Condition:condition:Dirichlet:profile:Continuum Profile:function').set_text('')
findWidget('Dialog-Edit Boundary Condition:condition:Dirichlet:profile:Continuum Profile:function').set_text('0')
findWidget('Dialog-Edit Boundary Condition:gtk-ok').clicked()
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(336)
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint OOF.Mesh.Boundary_Conditions.Edit
checkpoint_count("Graphics_1 Mesh Info sensitized")
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Solver')
findWidget('OOF2:Solver Page:end').set_text('0')
findWidget('OOF2:Solver Page:solve').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint_count("Graphics_1 Mesh Info sensitized")
checkpoint OOF.Mesh.Solve
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint_count("Graphics_1 Mesh Info sensitized")
findWidget('OOF2 Graphics 1').resize(800, 400)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Boundary Analysis')
findWidget('OOF2:Boundary Analysis Page:Pane:frame').size_allocate(gtk.gdk.Rectangle(4, 102, 226, 296))
findWidget('OOF2:Boundary Analysis Page:Go').clicked()
checkpoint OOF.Mesh.Boundary_Analysis.Analyze
checkpoint_count("Graphics_1 Mesh Info sensitized")
assert tests.msgFloat(0, 0, 0.0062016590418835175)
# Analysis complete on top boundary.
findWidget('OOF2:Boundary Analysis Page:Pane:frame:BoundaryListScroll:BoundaryList').get_selection().select_path((2,))
findWidget('OOF2:Boundary Analysis Page:Go').clicked()
checkpoint OOF.Mesh.Boundary_Analysis.Analyze
# Analysis complete on right boundary.
assert tests.msgFloat(0, 0.087825528898592839, 0)
findWidget('OOF2:Boundary Analysis Page:Pane:frame:BoundaryListScroll:BoundaryList').get_selection().select_path((3,))
tree=findWidget('OOF2:Boundary Analysis Page:Pane:frame:BoundaryListScroll:BoundaryList')
column = tree.get_column(0)
tree.row_activated((2,), column)
checkpoint OOF.Mesh.Boundary_Analysis.Analyze
# Analysis complete on left boundary.
assert tests.msgFloat(0, -0.087825528898597807, 0)
findWidget('OOF2:Boundary Analysis Page:Pane:frame:BoundaryListScroll:BoundaryList').get_selection().select_path((1,))
tree=findWidget('OOF2:Boundary Analysis Page:Pane:frame:BoundaryListScroll:BoundaryList')
column = tree.get_column(0)
tree.row_activated((3,), column)
checkpoint OOF.Mesh.Boundary_Analysis.Analyze
# Analysis complete on bottom boundary.
assert tests.msgFloat(0, 0, -0.0062016590418854916)
findWidget('OOF2').resize(684, 482)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Materials')
findWidget('OOF2:Materials Page:Pane').set_position(272)
widget_1=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_1.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_1.window))
tree=findWidget('OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
column = tree.get_column(0)
tree.row_activated((1, 0, 0), column)
checkpoint toplevel widget mapped Dialog-Parametrize Mechanical;Elasticity;Isotropic
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic').resize(372, 244)
setComboBox(findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic:cijkl:Chooser'), 'E and nu')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic:cijkl:E and nu:poisson').set_text('0.')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic:cijkl:E and nu:poisson').set_text('0.0')
findWidget('Dialog-Parametrize Mechanical;Elasticity;Isotropic:gtk-ok').clicked()
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint OOF.Property.Parametrize.Mechanical.Elasticity.Isotropic
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Solver')
findWidget('OOF2:Solver Page:end').set_text('0')
findWidget('OOF2:Solver Page:solve').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
checkpoint Graphics_1 Mesh Info sensitized
#checkpoint Graphics_1 Mesh Info sensitized
checkpoint OOF.Mesh.Solve
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Boundary Analysis')
findWidget('OOF2:Boundary Analysis Page:Pane:frame').size_allocate(gtk.gdk.Rectangle(4, 102, 226, 296))
findWidget('OOF2:Boundary Analysis Page:Pane:frame:BoundaryListScroll:BoundaryList').get_selection().select_path((2,))
tree=findWidget('OOF2:Boundary Analysis Page:Pane:frame:BoundaryListScroll:BoundaryList')
column = tree.get_column(0)
tree.row_activated((1,), column)
checkpoint OOF.Mesh.Boundary_Analysis.Analyze
# Analysis complete on right boundary.
assert tests.msgFloat(0, 0.066666666666669996, 0)
findWidget('OOF2:Boundary Analysis Page:Pane:frame:BoundaryListScroll:BoundaryList').get_selection().select_path((3,))
tree=findWidget('OOF2:Boundary Analysis Page:Pane:frame:BoundaryListScroll:BoundaryList')
column = tree.get_column(0)
tree.row_activated((2,), column)
checkpoint OOF.Mesh.Boundary_Analysis.Analyze
# Analysis complete on left boundary.
assert tests.msgFloat(0, -0.06666666666666736, 0)
findWidget('OOF2:Boundary Analysis Page:Pane:frame:BoundaryListScroll:BoundaryList').get_selection().select_path((1,))
tree=findWidget('OOF2:Boundary Analysis Page:Pane:frame:BoundaryListScroll:BoundaryList')
column = tree.get_column(0)
tree.row_activated((3,), column)
checkpoint OOF.Mesh.Boundary_Analysis.Analyze
# Analysis completed on bottom boundary.
assert tests.msgFloat(0, 0, 0)
findWidget('OOF2:Boundary Analysis Page:Pane:frame:BoundaryListScroll:BoundaryList').get_selection().select_path((0,))
tree=findWidget('OOF2:Boundary Analysis Page:Pane:frame:BoundaryListScroll:BoundaryList')
column = tree.get_column(0)
tree.row_activated((0,), column)
checkpoint OOF.Mesh.Boundary_Analysis.Analyze
# Analysis completed on top boundary.
assert tests.msgFloat(0, 0, 0)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Fields & Equations')
findWidget('OOF2:Fields & Equations Page:HPane:Fields:Displacement defined').clicked()
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
##checkpoint Graphics_1 Mesh Info sensitized
##checkpoint Graphics_1 Mesh Info sensitized
checkpoint OOF.Subproblem.Field.Undefine
findWidget('OOF2:Fields & Equations Page:HPane:Fields:Temperature defined').clicked()
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint OOF.Subproblem.Field.Undefine
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Boundary Analysis')
assert tests.goSensitive(1)
findWidget('OOF2:Boundary Analysis Page:Pane:frame').size_allocate(gtk.gdk.Rectangle(4, 102, 226, 296))
setComboBox(findWidget('OOF2:Boundary Analysis Page:Pane:BdyAnalyzerRCF:Chooser'), 'Average Field')
setComboBox(findWidget('OOF2:Boundary Analysis Page:Pane:BdyAnalyzerRCF:Chooser'), 'Integrate Flux')
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Fields & Equations')
findWidget('OOF2:Fields & Equations Page:HPane:Equations:Force_Balance active').clicked()
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint OOF.Subproblem.Equation.Deactivate
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Boundary Analysis')
assert tests.goSensitive(0)
findWidget('OOF2:Boundary Analysis Page:Pane:frame').size_allocate(gtk.gdk.Rectangle(4, 102, 226, 296))
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'FE Mesh')
findWidget('OOF2:FE Mesh Page:Pane').set_position(265)
findWidget('OOF2:FE Mesh Page:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(302, 94)
findWidget('Questioner:gtk-yes').clicked()
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint mesh page subproblems sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
findWidget('OOF2 Graphics 1:Pane0').set_position(278)
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
checkpoint OOF.Mesh.Delete
findWidget('OOF2:FE Mesh Page:Pane').set_position(265)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Boundary Analysis')
assert tests.bdyList()
assert tests.goSensitive(0)
findWidget('OOF2:Boundary Analysis Page:Pane:frame').size_allocate(gtk.gdk.Rectangle(4, 102, 226, 296))
findMenu(findWidget('OOF2:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(194, 72)
findWidget('Dialog-Python_Log:filename').set_text('b')
findWidget('Dialog-Python_Log:filename').set_text('bd')
findWidget('Dialog-Python_Log:filename').set_text('bdy')
findWidget('Dialog-Python_Log:filename').set_text('bdya')
findWidget('Dialog-Python_Log:filename').set_text('bdyan')
findWidget('Dialog-Python_Log:filename').set_text('bdyana')
findWidget('Dialog-Python_Log:filename').set_text('bdyanal')
findWidget('Dialog-Python_Log:filename').set_text('bdyanal.')
findWidget('Dialog-Python_Log:filename').set_text('bdyanal.l')
findWidget('Dialog-Python_Log:filename').set_text('bdyanal.lo')
findWidget('Dialog-Python_Log:filename').set_text('bdyanal.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff("bdyanal.log")
findMenu(findWidget('OOF2:MenuBar'), 'File:Quit').activate()
