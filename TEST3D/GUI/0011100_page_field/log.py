# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.2 $
# $Author: fyc $
# $Date: 2014/06/19 15:25:48 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

import tests

#Testing the Fields & Equations sections and their dependencies handling

findWidget('OOF3D').resize(550, 350)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Microstructure')
checkpoint page installed Microstructure
findWidget('OOF3D:Microstructure Page:Pane').set_position(225)
findWidget('OOF3D:Microstructure Page:Pane').set_position(156)
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized
findMenu(findWidget('OOF3D:MenuBar'), 'File:Load:Data').activate()
checkpoint toplevel widget mapped Dialog-Data
findWidget('Dialog-Data').resize(190, 67)
findWidget('Dialog-Data:filename').set_text('TEST_DATA/two_walls.skeleton')
findWidget('Dialog-Data:gtk-ok').clicked()
findWidget('OOF3D:Microstructure Page:Pane').set_position(159)
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint named analysis chooser set
checkpoint named analysis chooser set
checkpoint pixel page updated
checkpoint active area status updated
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint Field page sensitized
checkpoint Materials page updated
checkpoint mesh page subproblems sensitized
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
findWidget('OOF3D:Microstructure Page:Pane').set_position(225)
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
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page sensitized
checkpoint pinnodes page sensitized
checkpoint boundary page updated
checkpoint skeleton selection page selection sensitized
checkpoint Solver page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint pinnodes page sensitized
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
checkpoint toplevel widget mapped OOF3D Activity Viewer
checkpoint boundary page updated
findWidget('OOF3D Activity Viewer').resize(400, 300)
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
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'FE Mesh')
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint page installed FE Mesh
findWidget('OOF3D:FE Mesh Page:Pane').set_position(304)
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
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'FE Mesh')
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint page installed FE Mesh
findWidget('OOF3D:FE Mesh Page:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new mesh
findWidget('Dialog-Create a new mesh').resize(345, 153)
findWidget('Dialog-Create a new mesh:gtk-ok').clicked()
checkpoint named analysis chooser set
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
checkpoint OOF.Mesh.New
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new subproblem
findWidget('Dialog-Create a new subproblem').resize(286, 97)
findWidget('Dialog-Create a new subproblem:gtk-ok').clicked()
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.New
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
findWidget('OOF3D').resize(699, 350)
findWidget('OOF3D:Fields & Equations Page:HPane').set_position(312)
findWidget('OOF3D:Fields & Equations Page:HPane:Fields:Temperature defined').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Field.Define
findWidget('OOF3D:Fields & Equations Page:HPane:Fields:Displacement defined').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Field.Define
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
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Equation.Activate
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
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Equation.Activate
assert tests.fieldButtonCheck('Temperature',True,False)
assert tests.fieldButtonCheck('Displacement',True,False)
assert tests.fieldButtonCheck('Voltage',False,False)
assert tests.eqnButtonCheck('Heat_Eqn',True)
assert tests.eqnButtonCheck('Force_Balance',True)
assert tests.eqnButtonCheck('Coulomb_Eqn',False)
setComboBox(findWidget('OOF3D:Fields & Equations Page:Mesh'), 'mesh<2>')
checkpoint Field page sensitized
assert tests.fieldButtonCheck('Temperature',False,False)
assert tests.fieldButtonCheck('Displacement',False,False)
assert tests.fieldButtonCheck('Voltage',False,False)
assert tests.eqnButtonCheck('Heat_Eqn',False)
assert tests.eqnButtonCheck('Force_Balance',False)
assert tests.eqnButtonCheck('Coulomb_Eqn',False)
findWidget('OOF3D').resize(723, 350)
findWidget('OOF3D:Fields & Equations Page:HPane').set_position(323)
findWidget('OOF3D:Fields & Equations Page:HPane:Fields:Voltage defined').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint OOF.Subproblem.Field.Define
findWidget('OOF3D:Fields & Equations Page:HPane:Equations:Coulomb_Eqn active').clicked()
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
checkpoint OOF.Subproblem.Equation.Activate
assert tests.fieldButtonCheck('Temperature',False,False)
assert tests.fieldButtonCheck('Displacement',False,False)
assert tests.fieldButtonCheck('Voltage',True,False)
assert tests.eqnButtonCheck('Heat_Eqn',False)
assert tests.eqnButtonCheck('Force_Balance',False)
assert tests.eqnButtonCheck('Coulomb_Eqn',True)
setComboBox(findWidget('OOF3D:Fields & Equations Page:SubProblem'), 'subproblem')
checkpoint Field page sensitized
findWidget('OOF3D:Fields & Equations Page:HPane:Fields:Temperature defined').clicked()
findWidget('OOF3D Messages 1').resize(543, 200)
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint OOF.Subproblem.Field.Define
findWidget('OOF3D:Fields & Equations Page:HPane:Fields:Temperature active').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint OOF.Subproblem.Field.Activate
findWidget('OOF3D:Fields & Equations Page:HPane:Fields:Displacement defined').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
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
checkpoint OOF.Subproblem.Field.Activate
findWidget('OOF3D:Fields & Equations Page:HPane:Fields:Voltage defined').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint OOF.Subproblem.Field.Define
findWidget('OOF3D:Fields & Equations Page:HPane:Fields:Voltage active').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint OOF.Subproblem.Field.Activate
assert tests.fieldButtonCheck('Temperature',True,True)
assert tests.fieldButtonCheck('Displacement',True,True)
assert tests.fieldButtonCheck('Voltage',True,True)
assert tests.eqnButtonCheck('Heat_Eqn',False)
assert tests.eqnButtonCheck('Force_Balance',False)
assert tests.eqnButtonCheck('Coulomb_Eqn',False)
setComboBox(findWidget('OOF3D:Fields & Equations Page:SubProblem'), 'default')
checkpoint Field page sensitized
setComboBox(findWidget('OOF3D:Fields & Equations Page:Mesh'), 'mesh')
checkpoint Field page sensitized
setComboBox(findWidget('OOF3D:Fields & Equations Page:Mesh'), 'mesh<2>')
checkpoint Field page sensitized
setComboBox(findWidget('OOF3D:Fields & Equations Page:SubProblem'), 'subproblem')
checkpoint Field page sensitized
setComboBox(findWidget('OOF3D:Fields & Equations Page:Mesh'), 'mesh')
checkpoint Field page sensitized
findWidget('OOF3D:Fields & Equations Page:HPane:CopyField').clicked()
checkpoint toplevel widget mapped Dialog-Select a target Subproblem
findWidget('Dialog-Select a target Subproblem').resize(190, 159)
setComboBox(findWidget('Dialog-Select a target Subproblem:target:Mesh'), 'mesh<2>')
assert tests.CopyFieldDialogCheck(microstructures=['two_walls'],skeletons=['skeleton'],meshes=['mesh', 'mesh<2>'],subproblems=['default', 'subproblem'])
assert tests.CopyFieldDialogSelect(microstructure='two_walls',skeleton='skeleton',mesh='mesh<2>',subproblem='default')
findWidget('Dialog-Select a target Subproblem:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Copy_Field_State
setComboBox(findWidget('OOF3D:Fields & Equations Page:Mesh'), 'mesh<2>')
checkpoint Field page sensitized
setComboBox(findWidget('OOF3D:Fields & Equations Page:SubProblem'), 'subproblem')
checkpoint Field page sensitized
setComboBox(findWidget('OOF3D:Fields & Equations Page:Mesh'), 'mesh')
checkpoint Field page sensitized
findWidget('OOF3D:Fields & Equations Page:HPane:CopyEquation').clicked()
checkpoint toplevel widget mapped Dialog-Select a target subproblem
findWidget('Dialog-Select a target subproblem').resize(190, 159)
setComboBox(findWidget('Dialog-Select a target subproblem:target:Mesh'), 'mesh<2>')
assert tests.CopyEquationDialogCheck(microstructures=['two_walls'],skeletons=['skeleton'],meshes=['mesh', 'mesh<2>'],subproblems=['default','subproblem'])
assert tests.CopyEquationDialogSelect(microstructure='two_walls',skeleton='skeleton',mesh='mesh<2>',subproblem='default')
findWidget('Dialog-Select a target subproblem:gtk-ok').clicked()
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
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Copy_Equation_State
setComboBox(findWidget('OOF3D:Fields & Equations Page:Mesh'), 'mesh<2>')
checkpoint Field page sensitized
setComboBox(findWidget('OOF3D:Fields & Equations Page:SubProblem'), 'subproblem')
checkpoint Field page sensitized
findWidget('OOF3D:Fields & Equations Page:HPane:CopyEquation').clicked()
checkpoint toplevel widget mapped Dialog-Select a target subproblem
findWidget('Dialog-Select a target subproblem').resize(190, 159)
setComboBox(findWidget('Dialog-Select a target subproblem:target:Mesh'), 'mesh')
assert tests.CopyEquationDialogCheck(microstructures=['two_walls'],skeletons=['skeleton'],meshes=['mesh', 'mesh<2>'],subproblems=['default'])
assert tests.CopyEquationDialogSelect(microstructure='two_walls',skeleton='skeleton',mesh='mesh',subproblem='default')
findWidget('Dialog-Select a target subproblem:gtk-ok').clicked()
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
checkpoint OOF.Subproblem.Copy_Equation_State
setComboBox(findWidget('OOF3D:Fields & Equations Page:Mesh'), 'mesh')
checkpoint Field page sensitized
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'FE Mesh')
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint page installed FE Mesh
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:SubproblemScroll:SubproblemList').get_selection().select_path((1,))
checkpoint mesh page subproblems sensitized
findWidget('OOF3D:FE Mesh Page:Pane').set_position(477)
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(399, 89)
findWidget('Questioner:gtk-yes').clicked()
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Delete
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Fields & Equations')
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint page installed Fields & Equations
setComboBox(findWidget('OOF3D:Fields & Equations Page:Mesh'), 'mesh<2>')
checkpoint Field page sensitized
setComboBox(findWidget('OOF3D:Fields & Equations Page:Mesh'), 'mesh')
checkpoint Field page sensitized
setComboBox(findWidget('OOF3D:Fields & Equations Page:Mesh'), 'mesh<2>')
checkpoint Field page sensitized
findWidget('OOF3D:Fields & Equations Page:HPane:CopyEquation').clicked()
checkpoint toplevel widget mapped Dialog-Select a target subproblem
findWidget('Dialog-Select a target subproblem').resize(190, 159)
setComboBox(findWidget('Dialog-Select a target subproblem:target:Mesh'), 'mesh')
assert tests.CopyEquationDialogCheck(microstructures=['two_walls'],skeletons=['skeleton'],meshes=['mesh', 'mesh<2>'],subproblems=['default'])
assert tests.CopyEquationDialogSelect(microstructure='two_walls',skeleton='skeleton',mesh='mesh',subproblem='default')
findWidget('Dialog-Select a target subproblem:gtk-ok').clicked()
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
checkpoint OOF.Subproblem.Copy_Equation_State
setComboBox(findWidget('OOF3D:Fields & Equations Page:Mesh'), 'mesh')
checkpoint Field page sensitized
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'FE Mesh')
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint page installed FE Mesh
findWidget('OOF3D:FE Mesh Page:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(325, 89)
findWidget('Questioner:gtk-yes').clicked()
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page sensitized
checkpoint OOF.Mesh.Delete
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Fields & Equations')
checkpoint Field page sensitized
checkpoint page installed Fields & Equations
assert tests.fieldButtonCheck('Temperature',True,False)
assert tests.fieldButtonCheck('Displacement',True,False)
assert tests.fieldButtonCheck('Voltage',False,False)
assert tests.eqnButtonCheck('Heat_Eqn',True)
assert tests.eqnButtonCheck('Force_Balance',True)
assert tests.eqnButtonCheck('Coulomb_Eqn',False)
findMenu(findWidget('OOF3D:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(190, 92)
findWidget('Dialog-Python_Log:filename').set_text('fieldeqn.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('fieldeqn.log')
widget_2=findWidget('OOF3D')
handled_2=widget_2.event(event(gtk.gdk.DELETE,window=widget_2.window))
postpone if not handled_2: widget_2.destroy()
checkpoint OOF.Graphics_1.File.Close
