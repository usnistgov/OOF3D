# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.6 $
# $Author: fyc $
# $Date: 2014/06/19 15:33:05 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

import tests

#Testing the Solver Page Basic Operation in relation to the Fields & Equations Page

findWidget('OOF3D').resize(550, 350)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Microstructure')
checkpoint page installed Microstructure
findWidget('OOF3D:Microstructure Page:Pane').set_position(225)
findWidget('OOF3D:Microstructure Page:Pane').set_position(156)
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Solver')
checkpoint Solver page sensitized
checkpoint page installed Solver
assert tests.solverSubproblemsPageSensitivityCheck0()
assert tests.solverFieldsPageSensitivityCheck0()
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
checkpoint skeleton selection page groups sensitized
checkpoint Solver page sensitized
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
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((0,))
checkpoint Materials page updated
checkpoint property selected
widget_0=findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_0.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_0.window))
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').expand_row((1,), open_all=False)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').expand_row((1, 0), open_all=False)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((1, 0, 0))
checkpoint Materials page updated
checkpoint property deselected
checkpoint Materials page updated
checkpoint property selected
widget_1=findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_1.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_1.window))
findWidget('OOF3D:Materials Page:Pane:Property:Add').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint property selected
checkpoint Materials page updated
checkpoint OOF.Material.Add_property
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').expand_row((1, 0, 2), open_all=False)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').collapse_row((1, 0, 2))
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 3.1167322789559e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 6.2334645579118e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 9.3501968368677e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').expand_row((1, 2), open_all=False)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 9.3000000000000e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').collapse_row((1, 2))
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').expand_row((1, 3), open_all=False)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((1, 3, 0))
checkpoint Materials page updated
checkpoint property deselected
checkpoint Materials page updated
checkpoint property selected
widget_2=findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_2.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_2.window))
findWidget('OOF3D:Materials Page:Pane:Property:Add').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint property selected
checkpoint Materials page updated
checkpoint OOF.Material.Add_property
findWidget('OOF3D Messages 1').resize(563, 200)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 6.1832677210441e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 3.0665354420882e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 0.0000000000000e+00)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().unselect_all()
checkpoint Materials page updated
checkpoint property deselected
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').collapse_row((1,))
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').expand_row((2,), open_all=False)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').expand_row((2, 0), open_all=False)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((2, 0, 0))
checkpoint Materials page updated
checkpoint property selected
widget_3=findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_3.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_3.window))
findWidget('OOF3D:Materials Page:Pane:Property:Add').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint property selected
checkpoint Materials page updated
checkpoint OOF.Material.Add_property
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 3.1167322789559e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').expand_row((2, 1), open_all=False)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 3.1000000000000e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 6.2167322789559e+01)
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree').get_selection().select_path((2, 1, 0))
checkpoint Materials page updated
checkpoint property deselected
findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll').get_vadjustment().set_value( 6.2000000000000e+01)
checkpoint Materials page updated
checkpoint property selected
widget_4=findWidget('OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
widget_4.event(event(gtk.gdk.BUTTON_RELEASE,button=1,window=widget_4.window))
findWidget('OOF3D:Materials Page:Pane:Property:Add').clicked()
checkpoint Materials page updated
checkpoint Materials page updated
checkpoint property selected
checkpoint Materials page updated
checkpoint OOF.Material.Add_property
findWidget('OOF3D:Materials Page:Pane:Material:PropertyListScroll').get_vadjustment().set_value( 9.0000000000000e+00)
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
checkpoint Solver page sensitized
checkpoint skeleton selection page selection sensitized
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
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Mesh.New
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Solver')
checkpoint Solver page sensitized
checkpoint page installed Solver
findWidget('OOF3D').resize(691, 427)
assert tests.solverSubproblemsPageSensitivityCheck0()
assert tests.solverFieldsPageSensitivityCheck0()
assert tests.solverSubproblemsCheck(['default'])
findWidget('OOF3D:Solver Page:VPane').set_position(130)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Fields & Equations')
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint page installed Fields & Equations
findWidget('OOF3D').resize(715, 427)
findWidget('OOF3D:Fields & Equations Page:HPane').set_position(320)
findWidget('OOF3D:Fields & Equations Page:HPane:Fields:Displacement defined').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Field.Define
findWidget('OOF3D:Fields & Equations Page:HPane:Fields:Displacement active').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Field.Activate
findWidget('OOF3D:Fields & Equations Page:HPane:Equations:Force_Balance active').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Equation.Activate
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Solver')
checkpoint Solver page sensitized
checkpoint page installed Solver
assert tests.solverSubproblemsPageSensitivityCheck0()
assert tests.solverFieldsPageSensitivityCheck0()
assert tests.solverSubproblemsCheck(['default'])
assert tests.solverFieldsCheck(['Displacement'])
findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList').get_selection().select_path((0,))
checkpoint Solver page sensitized
assert tests.solverSubproblemsPageSensitivityCheck1()
assert tests.solverFieldsPageSensitivityCheck0()
assert tests.solverSubproblemsCheck(['default'])
assert tests.solverFieldsCheck(['Displacement'])
findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll').get_vadjustment().set_value( 3.0000000000000e+00)
findCellRenderer(findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList'), col=1, rend=0).emit('toggled', '0')
findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll').get_vadjustment().set_value( 0.0000000000000e+00)
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Disable_Solution
assert tests.solverSubproblemsPageSensitivityCheck1()
assert tests.solverFieldsPageSensitivityCheck0()
assert tests.solverSubproblemsCheck(['default'])
assert tests.solverFieldsCheck(['Displacement'])
findCellRenderer(findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList'), col=1, rend=0).emit('toggled', '0')
findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll').get_vadjustment().set_value( 3.0000000000000e+00)
tree=findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList')
column = tree.get_column(1)
tree.row_activated((0,), column)
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(475, 179)
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Enable_Solution
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
assert tests.solverSubproblemsPageSensitivityCheck2()
assert tests.solverFieldsPageSensitivityCheck0()
assert tests.solverSubproblemsCheck(['default'])
assert tests.solverFieldsCheck(['Displacement'])
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Fields & Equations')
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint page installed Fields & Equations
findWidget('OOF3D:Fields & Equations Page:HPane:Fields:Displacement active').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Field.Deactivate
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Solver')
checkpoint Solver page sensitized
checkpoint page installed Solver
assert tests.solverSubproblemsPageSensitivityCheck2()
assert tests.solverFieldsPageSensitivityCheck0()
assert tests.solverSubproblemsCheck(['default'])
assert tests.solverFieldsCheck(['Displacement'])
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Fields & Equations')
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint page installed Fields & Equations
findWidget('OOF3D:Fields & Equations Page:HPane:Fields:Displacement active').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Field.Activate
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Solver')
checkpoint Solver page sensitized
checkpoint page installed Solver
assert tests.solverSubproblemsPageSensitivityCheck2()
assert tests.solverFieldsPageSensitivityCheck0()
assert tests.solverSubproblemsCheck(['default'])
assert tests.solverFieldsCheck(['Displacement'])
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Fields & Equations')
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint page installed Fields & Equations
findWidget('OOF3D:Fields & Equations Page:HPane:Equations:Force_Balance active').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Equation.Deactivate
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Solver')
checkpoint Solver page sensitized
checkpoint page installed Solver
assert tests.solverSubproblemsPageSensitivityCheck2()
assert tests.solverFieldsPageSensitivityCheck0()
assert tests.solverSubproblemsCheck(['default'])
assert tests.solverFieldsCheck(['Displacement'])
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Fields & Equations')
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint page installed Fields & Equations
findWidget('OOF3D:Fields & Equations Page:HPane:Equations:Force_Balance active').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Equation.Activate
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Solver')
checkpoint Solver page sensitized
checkpoint page installed Solver
assert tests.solverSubproblemsPageSensitivityCheck2()
assert tests.solverFieldsPageSensitivityCheck0()
assert tests.solverSubproblemsCheck(['default'])
assert tests.solverFieldsCheck(['Displacement'])
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Fields & Equations')
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint page installed Fields & Equations
findWidget('OOF3D:Fields & Equations Page:HPane:Equations:Force_Balance active').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Equation.Deactivate
findWidget('OOF3D:Fields & Equations Page:HPane:Equations:Heat_Eqn active').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Equation.Activate
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Solver')
checkpoint Solver page sensitized
checkpoint page installed Solver
assert tests.solverSubproblemsPageSensitivityCheck2()
assert tests.solverFieldsPageSensitivityCheck0()
assert tests.solverSubproblemsCheck(['default'])
assert tests.solverFieldsCheck(['Displacement'])
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Fields & Equations')
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint page installed Fields & Equations
findWidget('OOF3D:Fields & Equations Page:HPane:Fields:Temperature defined').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Field.Define
findWidget('OOF3D:Fields & Equations Page:HPane:Fields:Temperature active').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Field.Activate
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Solver')
checkpoint Solver page sensitized
checkpoint page installed Solver
assert tests.solverSubproblemsPageSensitivityCheck2()
assert tests.solverFieldsPageSensitivityCheck0()
assert tests.solverSubproblemsCheck(['default'])
assert tests.solverFieldsCheck(['Temperature', 'Displacement'])
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Fields & Equations')
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint page installed Fields & Equations
findWidget('OOF3D:Fields & Equations Page:HPane:Equations:Force_Balance active').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Equation.Activate
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Solver')
checkpoint Solver page sensitized
checkpoint page installed Solver
assert tests.solverSubproblemsPageSensitivityCheck2()
assert tests.solverFieldsPageSensitivityCheck0()
assert tests.solverSubproblemsCheck(['default'])
assert tests.solverFieldsCheck(['Temperature', 'Displacement'])
findWidget('OOF3D:Solver Page:VPane:FieldInit:Scroll').get_vadjustment().set_value( 1.8900000000000e+01)
findWidget('OOF3D:Solver Page:VPane:FieldInit:Scroll').get_vadjustment().set_value( 2.7000000000000e+01)
findWidget('OOF3D:Solver Page:VPane:FieldInit:Scroll').get_vadjustment().set_value( 2.5312500000000e+01)
findWidget('OOF3D:Solver Page:VPane:FieldInit:Scroll').get_vadjustment().set_value( 2.3625000000000e+01)
findWidget('OOF3D:Solver Page:VPane:FieldInit:Scroll').get_vadjustment().set_value( 2.1937500000000e+01)
findWidget('OOF3D:Solver Page:VPane:FieldInit:Scroll').get_vadjustment().set_value( 2.0250000000000e+01)
findWidget('OOF3D:Solver Page:VPane:FieldInit:Scroll').get_vadjustment().set_value( 1.8562500000000e+01)
findWidget('OOF3D:Solver Page:VPane:FieldInit:Scroll').get_vadjustment().set_value( 1.6875000000000e+01)
findWidget('OOF3D:Solver Page:VPane:FieldInit:Scroll').get_vadjustment().set_value( 1.5187500000000e+01)
findWidget('OOF3D:Solver Page:VPane:FieldInit:Scroll').get_vadjustment().set_value( 1.3500000000000e+01)
findWidget('OOF3D:Solver Page:VPane:FieldInit:Scroll').get_vadjustment().set_value( 1.1812500000000e+01)
findWidget('OOF3D:Solver Page:VPane:FieldInit:Scroll').get_vadjustment().set_value( 1.0125000000000e+01)
findWidget('OOF3D:Solver Page:VPane:FieldInit:Scroll').get_vadjustment().set_value( 8.4375000000000e+00)
findWidget('OOF3D:Solver Page:VPane:FieldInit:Scroll').get_vadjustment().set_value( 6.7500000000000e+00)
findWidget('OOF3D:Solver Page:VPane:FieldInit:Scroll').get_vadjustment().set_value( 5.0625000000000e+00)
findWidget('OOF3D:Solver Page:VPane:FieldInit:Scroll').get_vadjustment().set_value( 3.3750000000000e+00)
findWidget('OOF3D:Solver Page:VPane:FieldInit:Scroll').get_vadjustment().set_value( 1.6875000000000e+00)
findWidget('OOF3D:Solver Page:VPane:FieldInit:Scroll').get_vadjustment().set_value( 0.0000000000000e+00)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Fields & Equations')
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint page installed Fields & Equations
findWidget('OOF3D:Fields & Equations Page:HPane:Equations:Heat_Eqn active').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Equation.Deactivate
findWidget('OOF3D:Fields & Equations Page:HPane:Fields:Temperature active').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Field.Deactivate
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Solver')
checkpoint Solver page sensitized
checkpoint page installed Solver
assert tests.solverSubproblemsPageSensitivityCheck2()
assert tests.solverFieldsPageSensitivityCheck0()
assert tests.solverSubproblemsCheck(['default'])
assert tests.solverFieldsCheck(['Temperature', 'Displacement'])
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Fields & Equations')
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint page installed Fields & Equations
findWidget('OOF3D:Fields & Equations Page:HPane:Fields:Temperature defined').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Field.Undefine
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Solver')
checkpoint Solver page sensitized
checkpoint page installed Solver
assert tests.solverSubproblemsPageSensitivityCheck2()
assert tests.solverFieldsPageSensitivityCheck0()
assert tests.solverSubproblemsCheck(['default'])
assert tests.solverFieldsCheck(['Displacement'])
findWidget('OOF3D:Solver Page:VPane:FieldInit:Scroll').get_vadjustment().set_value( 7.5000000000000e-01)
findWidget('OOF3D:Solver Page:VPane:FieldInit:Scroll').get_vadjustment().set_value( 1.5000000000000e+00)
findWidget('OOF3D:Solver Page:VPane:FieldInit:Scroll').get_vadjustment().set_value( 2.2500000000000e+00)
findWidget('OOF3D:Solver Page:VPane:FieldInit:Scroll').get_vadjustment().set_value( 3.0000000000000e+00)
findMenu(findWidget('OOF3D:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(190, 92)
findWidget('Dialog-Python_Log:filename').set_text('solverpage.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('solverpage.log')
widget_2=findWidget('OOF3D')
handled_2=widget_2.event(event(gtk.gdk.DELETE,window=widget_2.window))
postpone if not handled_2: widget_2.destroy()
checkpoint OOF.Graphics_1.File.Close