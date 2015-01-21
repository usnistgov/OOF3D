checkpoint toplevel widget mapped OOF2 Activity Viewer
# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:14:14 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov.

import tests

# This script checks for errors that occurred when solving adjacent
# subproblems and with creating new subproblems when a graphics window
# was open.  There are almost no explicit tests in the script.  If it
# finishes without hanging or crashing, it passes.

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
checkpoint OOF.Microstructure.Create_From_ImageFile
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Image')
findWidget('OOF2').resize(593, 350)
findWidget('OOF2:Image Page:Pane').set_position(380)
findWidget('OOF2:Image Page:Group').clicked()
checkpoint toplevel widget mapped Dialog-AutoGroup
findWidget('Dialog-AutoGroup').resize(211, 72)
findWidget('Dialog-AutoGroup:gtk-ok').clicked()
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint OOF.Image.AutoGroup
findWidget('OOF2').resize(593, 350)
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
findWidget('Dialog-Assign material material to pixels').resize(440, 108)
setComboBox(findWidget('Dialog-Assign material material to pixels:pixels'), '<all>')
findWidget('Dialog-Assign material material to pixels:gtk-ok').clicked()
checkpoint OOF.Material.Assign
findMenu(findWidget('OOF2:MenuBar'), 'Windows:Graphics:New').activate()
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint toplevel widget mapped OOF2 Graphics 1
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
checkpoint selection info updated
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(693)
findWidget('OOF2 Graphics 1:Pane0').set_position(283)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(693)
findWidget('OOF2 Graphics 1:Pane0').set_position(283)
findWidget('OOF2 Graphics 1').resize(800, 400)
checkpoint OOF.Windows.Graphics.New
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(250)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(693)
findWidget('OOF2 Graphics 1:Pane0').set_position(283)
findWidget('OOF2 Graphics 1:Pane0:Pane1:Pane2').set_position(259)
findWidget('OOF2 Graphics 1:Pane0:Pane1').set_position(717)
findWidget('OOF2 Graphics 1:Pane0').set_position(283)
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton')
findWidget('OOF2').resize(684, 434)
findWidget('OOF2:Skeleton Page:Pane').set_position(340)
checkpoint skeleton page sensitized
findWidget('OOF2:Skeleton Page:New').clicked()
checkpoint toplevel widget mapped Dialog-New skeleton
findWidget('Dialog-New skeleton').resize(334, 152)
findWidget('Dialog-New skeleton:gtk-ok').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
findWidget('OOF2 Graphics 1:Pane0').set_position(283)
checkpoint skeleton page sensitized
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Move Node toolbox writable changed
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint Graphics_1 Move Nodes sensitized
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
findWidget('OOF2:Skeleton Page:Pane').set_position(340)
checkpoint skeleton page sensitized
checkpoint skeleton page sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Skeleton.New
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'FE Mesh')
findWidget('OOF2:FE Mesh Page:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new mesh
findWidget('Dialog-Create a new mesh').resize(331, 188)
findWidget('Dialog-Create a new mesh:gtk-ok').clicked()
checkpoint Graphics_1 Skeleton Info sensitized
checkpoint Graphics_1 Mesh Info sensitized
checkpoint Graphics_1 Pixel Info updated
checkpoint selection info updated
checkpoint Graphics_1 Pixel Selection sensitized
checkpoint selection info updated
checkpoint selection info updated
checkpoint selection info updated
checkpoint mesh bdy page updated
checkpoint mesh bdy page updated
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
findWidget('OOF2 Graphics 1:Pane0').set_position(283)
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Mesh.New
findWidget('OOF2:FE Mesh Page:Pane:Subproblems:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new subproblem
findWidget('Dialog-Create a new subproblem').resize(288, 104)
setComboBox(findWidget('Dialog-Create a new subproblem:subproblem:Chooser'), 'PixelGroup')
findWidget('Dialog-Create a new subproblem').resize(500, 132)
findWidget('Dialog-Create a new subproblem:gtk-ok').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(283)
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Subproblem.New
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2').resize(692, 434)
findWidget('OOF2:Fields & Equations Page:HPane').set_position(132)
setComboBox(findWidget('OOF2:Fields & Equations Page:SubProblem'), 'subproblem')
findWidget('OOF2:Fields & Equations Page:HPane:Fields:Displacement defined').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(283)
checkpoint OOF.Subproblem.Field.Define
findWidget('OOF2:Fields & Equations Page:HPane:Fields:Displacement active').clicked()
checkpoint OOF.Subproblem.Field.Activate
# findWidget('OOF2:Navigation:Next').clicked()
# setComboBox(findWidget('OOF2:Equations Page:SubProblem'), 'subproblem')
findWidget('OOF2:Fields & Equations Page:HPane:Equations:Force_Balance active').clicked()
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Subproblem.Equation.Activate
findWidget('OOF2:Fields & Equations Page:HPane:Equations:Plane_Stress active').clicked()
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Subproblem.Equation.Activate
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Boundary Conditions')
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(340)
findWidget('OOF2:Boundary Conditions Page:Pane:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(399, 300)
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(340)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Continuum Profile:function').set_text('.0')
findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Continuum Profile:function').set_text('0.0')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'left')
findWidget('Dialog-New Boundary Condition:gtk-apply').clicked()
findWidget('OOF2 Messages 1').resize(798, 200)
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(340)
checkpoint OOF.Mesh.Boundary_Conditions.New
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'right')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(340)
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2:Navigation:Next').clicked()
# setComboBox(findWidget('OOF2:Solver Page:SubProblem'), 'subproblem')
# findWidget('OOF2:Solver Page:Solve').clicked()
# findWidget('OOF2 Graphics 1:Pane0').set_position(283)
# checkpoint OOF.Solver.Solve
findCellRenderer(findWidget('OOF2:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList'), col=1, rend=0).emit('toggled', '0')
findWidget('OOF2:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList').get_selection().select_path((0,))
checkpoint OOF.Subproblem.Scrub_Solution
findWidget('OOF2:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList').get_selection().select_path((1,))
findWidget('OOF2:Solver Page:VPane:Subproblems:SubproblemScroll').get_vadjustment().set_value( 3.0000000000000e+00)
tree=findWidget('OOF2:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList')
column = tree.get_column(2)
tree.row_activated((1,), column)
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(398, 212)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF2:Solver Page:end').set_text('0')
# solve 1 subproblem with trivial bcs
findWidget('OOF2:Solver Page:solve').clicked()
checkpoint contourmap info updated for Graphics_1
checkpoint OOF.Mesh.Solve

findWidget('OOF2:Navigation:Prev').clicked()
findWidget('OOF2:Navigation:Prev').clicked()
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(340)
findWidget('OOF2:Boundary Conditions Page:Pane:Condition:Edit').clicked()
checkpoint toplevel widget mapped Dialog-Edit Boundary Condition
findWidget('Dialog-Edit Boundary Condition').resize(399, 276)
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(340)
findWidget('Dialog-Edit Boundary Condition:condition:Dirichlet:profile:Continuum Profile:function').set_text('10.0')
findWidget('Dialog-Edit Boundary Condition:gtk-ok').clicked()
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(340)
checkpoint OOF.Mesh.Boundary_Conditions.Edit
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'FE Mesh')
findWidget('OOF2:FE Mesh Page:Pane:Subproblems:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new subproblem
findWidget('Dialog-Create a new subproblem').resize(500, 132)
setComboBox(findWidget('Dialog-Create a new subproblem:subproblem:PixelGroup:group'), 'RGBColor(red=0.00000,green=1.00000,blue=1.00000)')
findWidget('Dialog-Create a new subproblem:gtk-ok').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(283)
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Subproblem.New
findWidget('OOF2:FE Mesh Page:Pane:Subproblems:subprobChooserScroll').get_vadjustment().set_value( 9.0000000000000e+00)
findWidget('OOF2:FE Mesh Page:Pane:Subproblems:subprobChooserScroll').get_vadjustment().set_value( 0.0000000000000e+00)
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2').resize(716, 434)
findWidget('OOF2:Fields & Equations Page:HPane').set_position(132)
findWidget('OOF2').resize(716, 434)
findWidget('OOF2:Fields & Equations Page:HPane:CopyField').clicked()
checkpoint toplevel widget mapped Dialog-Select a target Subproblem
findWidget('Dialog-Select a target Subproblem').resize(211, 164)
setComboBox(findWidget('Dialog-Select a target Subproblem:target:SubProblem'), 'subproblem<2>')
findWidget('Dialog-Select a target Subproblem:gtk-ok').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(283)
checkpoint OOF.Subproblem.Copy_Field_State
#setComboBox(findWidget('OOF2:Fields & Equations Page:SubProblem'), 'subproblem<2>')
findWidget('OOF2:Fields & Equations Page:HPane:CopyEquation').clicked()
checkpoint toplevel widget mapped Dialog-Select a target subproblem
findWidget('Dialog-Select a target subproblem').resize(211, 164)
setComboBox(findWidget('Dialog-Select a target subproblem:target:SubProblem'), 'subproblem<2>')
findWidget('Dialog-Select a target subproblem:gtk-ok').clicked()
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Subproblem.Copy_Equation_State
setComboBox(findWidget('OOF2:Fields & Equations Page:SubProblem'), 'subproblem<2>')
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(352)
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2:Navigation:Next').clicked()

findCellRenderer(findWidget('OOF2:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList'), col=1, rend=0).emit('toggled', '1')
checkpoint OOF.Subproblem.Scrub_Solution
findWidget('OOF2:Solver Page:VPane:Subproblems:SubproblemScroll').get_vadjustment().set_value( 1.4890202136873e+01)
findWidget('OOF2:Solver Page:VPane:Subproblems:SubproblemScroll').get_vadjustment().set_value( 2.5000000000000e+01)
findWidget('OOF2:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList').get_selection().select_path((2,))
tree=findWidget('OOF2:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList')
column = tree.get_column(2)
tree.row_activated((2,), column)
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(398, 212)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF2:Solver Page:end').set_text('0')
# solve second subproblem with nontrivial bcs
findWidget('OOF2:Solver Page:solve').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(283)
checkpoint OOF.Mesh.Solve
findWidget('OOF2').resize(716, 434)

findCellRenderer(findWidget('OOF2:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList'), col=1, rend=0).emit('toggled', '1')
findWidget('OOF2:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList').get_selection().select_path((1,))
checkpoint OOF.Subproblem.Schedule_Solution
findCellRenderer(findWidget('OOF2:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList'), col=1, rend=0).emit('toggled', '2')
findWidget('OOF2:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList').get_selection().select_path((2,))
checkpoint OOF.Subproblem.Scrub_Solution
findWidget('OOF2:Solver Page:end').set_text('0')
# solve first subproblem again, with nontrivial bcs
findWidget('OOF2:Solver Page:solve').clicked()
findWidget('OOF2 Graphics 1:Pane0').set_position(283)
checkpoint OOF.Mesh.Solve
findMenu(findWidget('OOF2:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(194, 72)
findWidget('Dialog-Python_Log:filename').set_text('s')
findWidget('Dialog-Python_Log:filename').set_text('st')
findWidget('Dialog-Python_Log:filename').set_text('str')
findWidget('Dialog-Python_Log:filename').set_text('stre')
findWidget('Dialog-Python_Log:filename').set_text('stret')
findWidget('Dialog-Python_Log:filename').set_text('stretc')
findWidget('Dialog-Python_Log:filename').set_text('stretch')
findWidget('Dialog-Python_Log:filename').set_text('stretchb')
findWidget('Dialog-Python_Log:filename').set_text('stretchbu')
findWidget('Dialog-Python_Log:filename').set_text('stretchbug')
findWidget('Dialog-Python_Log:filename').set_text('stretchbug.')
findWidget('Dialog-Python_Log:filename').set_text('stretchbug.l')
findWidget('Dialog-Python_Log:filename').set_text('stretchbug.lo')
findWidget('Dialog-Python_Log:filename').set_text('stretchbug.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('stretchbug.log')
findMenu(findWidget('OOF2:MenuBar'), 'File:Quit').activate()
checkpoint OOF.ActivityViewer.File.Close
checkpoint OOF.Graphics_1.File.Close
