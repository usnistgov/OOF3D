# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.7 $
# $Author: fyc $
# $Date: 2014/06/13 21:42:47 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

import tests

#Testing the dependency betweenn the Boundary Condtitions Page and
#the Fields & Equations Page
#Testing the basic handling actions on a Boundary Condition

findWidget('OOF3D').resize(550, 350)
findMenu(findWidget('OOF3D:MenuBar'), 'File:Load:Data').activate()
checkpoint toplevel widget mapped Dialog-Data
findWidget('Dialog-Data').resize(190, 65)
findWidget('Dialog-Data:filename').set_text('TEST_DATA/two_walls.skeleton')
findWidget('Dialog-Data:gtk-ok').clicked()
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint named analysis chooser set
checkpoint active area status updated
checkpoint microstructure page sensitized
checkpoint Field page sensitized
checkpoint meshable button set
checkpoint Materials page updated
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint pinnodes page sensitized
checkpoint boundary page updated
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint Solver page sensitized
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint named analysis chooser set
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint toplevel widget mapped OOF3D Activity Viewer
findWidget('OOF3D Activity Viewer').resize(400, 300)
checkpoint pinnodes page sensitized
checkpoint boundary page updated
checkpoint skeleton selection page selection sensitized
checkpoint Solver page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint pinnodes page sensitized
checkpoint skeleton selection page updated
checkpoint pinnodes page sensitized
checkpoint pinnodes page sensitized
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint boundary page updated
checkpoint OOF.File.Load.Data
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton')
checkpoint page installed Skeleton
findWidget('OOF3D').resize(601, 350)
findWidget('OOF3D:Skeleton Page:Pane').set_position(250)
checkpoint skeleton page sensitized
checkpoint skeleton page info updated
checkpoint skeleton page info updated
checkpoint skeleton page sensitized
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Boundary Conditions')
checkpoint page installed Boundary Conditions
assert tests.sensitization0()
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Fields & Equations')
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint page installed Fields & Equations
findWidget('OOF3D:Fields & Equations Page:HPane').set_position(268)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Skeleton')
checkpoint page installed Skeleton
checkpoint skeleton page sensitized
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'FE Mesh')
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint page installed FE Mesh
findWidget('OOF3D:FE Mesh Page:Pane').set_position(355)
findWidget('OOF3D:FE Mesh Page:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new mesh
findWidget('Dialog-Create a new mesh').resize(373, 229)
findWidget('Dialog-Create a new mesh:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Mesh.New
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new subproblem
findWidget('Dialog-Create a new subproblem').resize(286, 94)
findWidget('Dialog-Create a new subproblem:gtk-ok').clicked()
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.New
findWidget('OOF3D:FE Mesh Page:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new mesh
findWidget('Dialog-Create a new mesh').resize(373, 229)
findWidget('Dialog-Create a new mesh:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint mesh page subproblems sensitized
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
checkpoint Solver page sensitized
checkpoint OOF.Mesh.New
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new subproblem
findWidget('Dialog-Create a new subproblem').resize(286, 94)
findWidget('Dialog-Create a new subproblem:gtk-ok').clicked()
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.New
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Boundary Conditions')
checkpoint page installed Boundary Conditions
assert tests.sensitization0()
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Fields & Equations')
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint page installed Fields & Equations
findWidget('OOF3D').resize(723, 350)
findWidget('OOF3D:Fields & Equations Page:HPane').set_position(323)
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
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Equation.Activate
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Boundary Conditions')
checkpoint page installed Boundary Conditions
assert tests.sensitization0()
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Fields & Equations')
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint page installed Fields & Equations
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
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Boundary Conditions')
checkpoint page installed Boundary Conditions
assert tests.sensitization1()
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Fields & Equations')
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint page installed Fields & Equations
findWidget('OOF3D:Fields & Equations Page:HPane:Fields:Temperature active').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Field.Activate
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'FE Mesh')
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint page installed FE Mesh
findWidget('OOF3D:FE Mesh Page:Pane').set_position(477)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Boundary Conditions')
checkpoint page installed Boundary Conditions
assert tests.sensitization1()
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Fields & Equations')
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint page installed Fields & Equations
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Boundary Conditions')
checkpoint page installed Boundary Conditions
assert tests.sensitization1()
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Fields & Equations')
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint page installed Fields & Equations
setComboBox(findWidget('OOF3D:Fields & Equations Page:Mesh'), 'mesh<2>')
checkpoint Field page sensitized
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Boundary Conditions')
checkpoint page installed Boundary Conditions
assert tests.sensitization1()
setComboBox(findWidget('OOF3D:Boundary Conditions Page:Mesh'), 'mesh<2>')
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Fields & Equations')
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint page installed Fields & Equations
setComboBox(findWidget('OOF3D:Fields & Equations Page:Mesh'), 'mesh')
checkpoint Field page sensitized
setComboBox(findWidget('OOF3D:Fields & Equations Page:SubProblem'), 'subproblem')
checkpoint Field page sensitized
setComboBox(findWidget('OOF3D:Fields & Equations Page:Mesh'), 'mesh<2>')
checkpoint Field page sensitized
findWidget('OOF3D:Fields & Equations Page:HPane:Fields:Displacement defined').clicked()
checkpoint Field page sensitized
findWidget('OOF3D Messages 1').resize(543, 200)
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint OOF.Subproblem.Field.Define
findWidget('OOF3D:Fields & Equations Page:HPane:Fields:Displacement active').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
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
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint OOF.Subproblem.Equation.Activate
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Boundary Conditions')
checkpoint page installed Boundary Conditions
assert tests.sensitization1()
setComboBox(findWidget('OOF3D:Boundary Conditions Page:Mesh'), 'mesh')
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Fields & Equations')
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint page installed Fields & Equations
findWidget('OOF3D:Fields & Equations Page:HPane:Fields:Displacement defined').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint OOF.Subproblem.Field.Undefine
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Boundary Conditions')
checkpoint page installed Boundary Conditions
assert tests.sensitization1()
setComboBox(findWidget('OOF3D:Boundary Conditions Page:Mesh'), 'mesh<2>')
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
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint OOF.Subproblem.Field.Define
findWidget('OOF3D:Fields & Equations Page:HPane:Fields:Temperature defined').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint OOF.Subproblem.Field.Undefine
findWidget('OOF3D:Fields & Equations Page:HPane:Fields:Displacement defined').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint OOF.Subproblem.Field.Define
findWidget('OOF3D:Fields & Equations Page:HPane:Fields:Displacement active').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint OOF.Subproblem.Field.Activate
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Boundary Conditions')
checkpoint page installed Boundary Conditions
assert tests.sensitization1()
setComboBox(findWidget('OOF3D:Boundary Conditions Page:Mesh'), 'mesh')
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
assert tests.ConditionNewDialogCheck0()
findWidget('Dialog-New Boundary Condition').resize(412, 255)
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint Solver page sensitized
findWidget('OOF3D Messages 1').resize(983, 200)
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.sensitization2()
findWidget('OOF3D:Boundary Conditions Page:Condition:Rename').clicked()
checkpoint toplevel widget mapped Dialog-Rename the boundary condition "bc"
findWidget('Dialog-Rename the boundary condition "bc"').resize(190, 65)
findWidget('Dialog-Rename the boundary condition "bc":name').set_text('condition1')
findWidget('Dialog-Rename the boundary condition "bc":gtk-ok').clicked()
checkpoint OOF.Mesh.Boundary_Conditions.Rename
assert tests.sensitization2()
findWidget('OOF3D:Boundary Conditions Page:Condition:Edit').clicked()
checkpoint toplevel widget mapped Dialog-Edit Boundary Condition
assert tests.ConditionEditDialogCheck0()
findWidget('Dialog-Edit Boundary Condition').resize(412, 234)
setComboBox(findWidget('Dialog-Edit Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-Edit Boundary Condition').resize(467, 276)
setComboBox(findWidget('Dialog-Edit Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
setComboBox(findWidget('Dialog-Edit Boundary Condition:condition:Dirichlet:boundary'), 'Xmin')
findWidget('Dialog-Edit Boundary Condition:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.Edit
assert tests.sensitization2()
findWidget('OOF3D:Boundary Conditions Page:Condition:Copy').clicked()
checkpoint toplevel widget mapped Dialog-Choose a name and boundary.
assert tests.ConditionCopyDialogCheck0()
findWidget('Dialog-Choose a name and boundary.').resize(270, 175)
setComboBox(findWidget('Dialog-Choose a name and boundary.:mesh:Mesh'), 'mesh<2>')
findWidget('Dialog-Choose a name and boundary.').resize(270, 175)
findWidget('Dialog-Choose a name and boundary.:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.Copy
assert tests.sensitization2()
setComboBox(findWidget('OOF3D:Boundary Conditions Page:Mesh'), 'mesh<2>')
setComboBox(findWidget('OOF3D:Boundary Conditions Page:Mesh'), 'mesh')
setComboBox(findWidget('OOF3D:Boundary Conditions Page:Mesh'), 'mesh<2>')
setComboBox(findWidget('OOF3D:Boundary Conditions Page:Mesh'), 'mesh')
findWidget('OOF3D:Boundary Conditions Page:Condition:BCScroll:BCList').get_selection().select_path((0,))
setComboBox(findWidget('OOF3D:Boundary Conditions Page:Mesh'), 'mesh<2>')
findWidget('OOF3D:Boundary Conditions Page:Condition:BCScroll:BCList').get_selection().select_path((0,))
findWidget('OOF3D:Boundary Conditions Page:Condition:CopyAll').clicked()
checkpoint toplevel widget mapped Dialog-Choose the target mesh.
assert tests.ConditionCopyAllDialogCheck0()
findWidget('Dialog-Choose the target mesh.').resize(190, 127)
findWidget('Dialog-Choose the target mesh.:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.Copy_All
assert tests.sensitization2()
setComboBox(findWidget('OOF3D:Boundary Conditions Page:Mesh'), 'mesh')
setComboBox(findWidget('OOF3D:Boundary Conditions Page:Mesh'), 'mesh<2>')
setComboBox(findWidget('OOF3D:Boundary Conditions Page:Mesh'), 'mesh')
findWidget('OOF3D:Boundary Conditions Page:Condition:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(190, 87)
findWidget('Questioner:gtk-yes').clicked()
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.Delete
assert tests.sensitization3()
setComboBox(findWidget('OOF3D:Boundary Conditions Page:Mesh'), 'mesh<2>')
setComboBox(findWidget('OOF3D:Boundary Conditions Page:Mesh'), 'mesh')
findWidget('OOF3D:Boundary Conditions Page:Condition:BCScroll:BCList').get_selection().select_path((0,))
assert tests.sensitization2()
findWidget('OOF3D:Boundary Conditions Page:Condition:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(190, 87)
findWidget('Questioner:gtk-yes').clicked()
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.Delete
assert tests.sensitization1()
setComboBox(findWidget('OOF3D:Boundary Conditions Page:Mesh'), 'mesh<2>')
setComboBox(findWidget('OOF3D:Boundary Conditions Page:Mesh'), 'mesh')
setComboBox(findWidget('OOF3D:Boundary Conditions Page:Mesh'), 'mesh<2>')
findWidget('OOF3D:Boundary Conditions Page:Condition:BCScroll:BCList').get_selection().select_path((0,))
assert tests.sensitization2()
findWidget('OOF3D:Boundary Conditions Page:Condition:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(190, 87)
findWidget('Questioner:gtk-yes').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.Delete
assert tests.sensitization1()
findMenu(findWidget('OOF3D:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(190, 92)
findWidget('Dialog-Python_Log:filename').set_text('bcpage.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('bcpage.log')
widget_2=findWidget('OOF3D')
handled_2=widget_2.event(event(gtk.gdk.DELETE,window=widget_2.window))
postpone if not handled_2: widget_2.destroy()
checkpoint OOF.Graphics_1.File.Close
