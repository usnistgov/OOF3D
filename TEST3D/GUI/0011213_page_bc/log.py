# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.7 $
# $Author: fyc $
# $Date: 2014/06/16 20:23:16 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

import tests

#Testing Boundary Condition creation using Floating on Voltage Field
#The equation here is Coulomb_Eqn

findWidget('OOF3D').resize(550, 350)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Microstructure')
checkpoint page installed Microstructure
findWidget('OOF3D:Microstructure Page:Pane').set_position(225)
findWidget('OOF3D:Microstructure Page:Pane').set_position(156)
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint microstructure page sensitized
checkpoint meshable button set
findMenu(findWidget('OOF3D:MenuBar'), 'File:Load:Data').activate()
checkpoint toplevel widget mapped Dialog-Data
findWidget('Dialog-Data').resize(190, 67)
findWidget('Dialog-Data:filename').set_text('TEST_DATA/two_walls.skeleton')
findWidget('Dialog-Data:gtk-ok').clicked()
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint named analysis chooser set
checkpoint active area status updated
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint Field page sensitized
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
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint named analysis chooser set
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint pinnodes page sensitized
checkpoint boundary page updated
checkpoint skeleton selection page selection sensitized
checkpoint Solver page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint pinnodes page sensitized
findWidget('OOF3D Activity Viewer').resize(400, 300)
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
findWidget('OOF3D Messages 1').resize(553, 200)
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
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Fields & Equations')
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint page installed Fields & Equations
findWidget('OOF3D').resize(667, 350)
findWidget('OOF3D:Fields & Equations Page:HPane').set_position(298)
findWidget('OOF3D:Fields & Equations Page:HPane:Fields:Voltage defined').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Field.Define
findWidget('OOF3D:Fields & Equations Page:HPane:Fields:Voltage active').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Field.Activate
findWidget('OOF3D:Fields & Equations Page:HPane:Equations:Coulomb_Eqn active').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Equation.Activate
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Boundary Conditions')
checkpoint page installed Boundary Conditions
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Chooser'), 'Floating')
findWidget('Dialog-New Boundary Condition:name:Auto').clicked()
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_constantXmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
findWidget('OOF3D Messages 1').resize(983, 200)
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['floating_constantXmax'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_continiumXmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
findWidget('OOF3D Messages 1').resize(1023, 200)
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['floating_constantXmax','floating_continiumXmax'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:boundary'), 'Xmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_constantXmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_continuumXmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:boundary'), 'Ymax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_constantYmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_continuumYmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:boundary'), 'Ymin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_constantYmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_continuumYmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:boundary'), 'Zmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_constantZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_continuumZmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:boundary'), 'Zmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_constantZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_continuumZmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:boundary'), 'XmaxYmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_constantXmaxYmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_continuumXmaxYmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:boundary'), 'XmaxYmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_constantXmaxYmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_continuumXmaxYmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:boundary'), 'XmaxZmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_constantXmaxZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_continuumXmaxZmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Constant Profile')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:boundary'), 'XmaxZmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_constantXmaxZmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_continuumXmaxZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:boundary'), 'XminYmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_constantXminYmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_continuumXminYmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Constant Profile')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:boundary'), 'XminYmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_constantXminYmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_continuumXminYmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:boundary'), 'XminZmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_constantXminZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_continuumXminZmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:boundary'), 'XminZmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_constantXminZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_continuumXminZmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Constant Profile')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:boundary'), 'YmaxZmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_constantYmaxZmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_continuumYmaxZmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:boundary'), 'YmaxZmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_constantYmaxZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_continuumYmaxZmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:boundary'), 'YminZmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_constantYminZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_continuumYminZmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:boundary'), 'YminZmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_constantYminZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_continuumYminZmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:boundary'), 'XmaxYmaxZmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_constantXmaxYmaxZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_continuumXmaxYmaxZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:boundary'), 'XmaxYmaxZmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_constantXmaxYmaxZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_continuumXmaxYmaxZmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:boundary'), 'XmaxYminZmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_constantXmaxYminZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_continuumXmaxYminZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:boundary'), 'XmaxYminZmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_constantXmaxYminZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_continuumXmaxYminZmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:boundary'), 'XminYmaxZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_constantXminYmaxZmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_continuumXminYmaxZmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:boundary'), 'XminYmaxZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_constantXminYmaxZmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_continuumXminYmaxZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:boundary'), 'XminYminZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_constantXminYminZmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_continuumXminYminZmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:boundary'), 'XminYminZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_constantXminYminZmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_continuumXminYminZmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['floating_constantXmax', 'floating_constantXmaxYmax', 'floating_constantXmaxYmaxZmax', 'floating_constantXmaxYmaxZmin', 'floating_constantXmaxYmin', 'floating_constantXmaxYminZmax', 'floating_constantXmaxYminZmin', 'floating_constantXmaxZmax', 'floating_constantXmaxZmin', 'floating_constantXmin', 'floating_constantXminYmax', 'floating_constantXminYmaxZmax', 'floating_constantXminYmaxZmin', 'floating_constantXminYmin', 'floating_constantXminYminZmax', 'floating_constantXminYminZmin', 'floating_constantXminZmax', 'floating_constantXminZmin', 'floating_constantYmax', 'floating_constantYmaxZmax', 'floating_constantYmaxZmin', 'floating_constantYmin', 'floating_constantYminZmax', 'floating_constantYminZmin', 'floating_constantZmax', 'floating_constantZmin', 'floating_continiumXmax', 'floating_continuumXmaxYmax', 'floating_continuumXmaxYmaxZmax', 'floating_continuumXmaxYmaxZmin', 'floating_continuumXmaxYmin', 'floating_continuumXmaxYminZmax', 'floating_continuumXmaxYminZmin', 'floating_continuumXmaxZmax', 'floating_continuumXmaxZmin', 'floating_continuumXmin', 'floating_continuumXminYmax', 'floating_continuumXminYmaxZmax', 'floating_continuumXminYmaxZmin', 'floating_continuumXminYmin', 'floating_continuumXminYminZmax', 'floating_continuumXminYminZmin', 'floating_continuumXminZmax', 'floating_continuumXminZmin', 'floating_continuumYmax', 'floating_continuumYmaxZmax', 'floating_continuumYmaxZmin', 'floating_continuumYmin', 'floating_continuumYminZmax', 'floating_continuumYminZmin', 'floating_continuumZmax', 'floating_continuumZmin'])
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
