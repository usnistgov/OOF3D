# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.7 $
# $Author: fyc $
# $Date: 2014/06/16 20:23:03 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

import tests

#Testing Boundary Condition creation using Floating on Displacement Field
#The equation here is Force_Balance
#The field component is y

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
findWidget('OOF3D').resize(675, 350)
findWidget('OOF3D:Fields & Equations Page:HPane').set_position(301)
findWidget('OOF3D:Fields & Equations Page:HPane:Fields:Displacement defined').clicked()
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
findWidget('OOF3D:Fields & Equations Page:HPane:Fields:Displacement active').clicked()
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
findWidget('OOF3D:Fields & Equations Page:HPane:Equations:Force_Balance active').clicked()
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
findWidget('Dialog-New Boundary Condition').resize(412, 289)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Chooser'), 'Floating')
findWidget('Dialog-New Boundary Condition:name:Auto').clicked()
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:field_component'), 'y')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:boundary'), 'Xmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_constantXmax')
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
assert tests.boundaryConditionCheck(['floating_fieldy_componentx_constantXmax'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:boundary'), 'Xmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_constantXmin')
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
assert tests.boundaryConditionCheck(['floating_fieldy_componentx_constantXmax','floating_fieldy_componentx_constantXmin'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_continuumXmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_constantYmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_continuumYmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_constantYmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_continuumYmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_constantZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_continuumZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_constantZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_continuumZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_constantXmaxYmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_continuumXmaxYmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_constantXmaxYmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_continuumXmaxYmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_constantXmaxZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_continuumXmaxZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_constantXmaxZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_continuumXmaxZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_constantXminYmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_continuumXminYmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_constantXminYmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_continuumXminYmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_constantXminZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_continuumXminZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_constantXminZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_continuumXminZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_constantYmaxZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_continuumYmaxZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_constantYmaxZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_continuumYmaxZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_constantYminZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_continuumYminZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_constantYminZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_continuumYminZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_constantXmaxYmaxZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_continuumXmaxYmaxZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_constantXmaxYmaxZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_continuumXmaxYmaxZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_constantXmaxYminZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_continuumXmaxYminZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_constantXmaxYminZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_continuumXmaxYminZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_constantXminYmaxZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_continuumXminYmaxZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_constantXminYmaxZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_continuumXminYmaxZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_constantXminYminZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_continuumXminYminZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_constantXminYminZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentx_continuumXminYminZmin')
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
findWidget('Dialog-New Boundary Condition').resize(412, 289)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:boundary'), 'Xmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_constantXmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:eqn_component'), 'y')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:boundary'), 'Xmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_constantXmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_continuumXmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_constantYmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_continuumYmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_constantYmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_continuumYmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_constantZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_continuumZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_constantZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_continuumZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_constantXmaxYmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_continuumXmaxYmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_constantXmaxYmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_continuumXmaxYmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_constantXmaxZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_continuumXmaxZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_constantXmaxZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_continuumXmaxZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_constantXminYmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_continuumXminYmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_constantXminYmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_continuumXminYmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_constantXminZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_continuumXminZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_constantXminZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_continuumXminZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_constantYmaxZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_continuumYmaxZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_constantYmaxZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_continuumYmaxZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_constantYminZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_continuumYminZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_constantYminZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_continuumYminZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_constantXmaxYmaxZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_continuumXmaxYmaxZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_constantXmaxYmaxZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_continuumXmaxYmaxZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_constantXmaxYminZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_continuumXmaxYminZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_constantXmaxYminZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_continuumXmaxYminZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_constantXminYmaxZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_continuumXminYmaxZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_constantXminYmaxZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_continuumXminYmaxZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_constantXminYminZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_continuumXminYminZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_constantXminYminZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componenty_continuumXminYminZmin')
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
findWidget('Dialog-New Boundary Condition').resize(412, 289)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:eqn_component'), 'z')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:boundary'), 'Xmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_constantXmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:boundary'), 'Xmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Floating:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_constantXmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_continuumXmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_constantYmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_continuumYmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_constantYmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_continuumYmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_constantZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_continuumZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_constantZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_continuumZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_constantXmaxYmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_continuumXmaxYmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_constantXmaxYmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_continuumXmaxYmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_constantXmaxZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_continuumXmaxZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_constantXmaxZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_continuumXmaxZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_constantXminYmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_continuumXminYmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_constantXminYmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_continuumXminYmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_constantXminZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_continuumXminZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_constantXminZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_continuumXminZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_constantYmaxZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_continuumYmaxZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_constantYmaxZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_continuumYmaxZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_constantYminZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_continuumYminZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_constantYminZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_continuumYminZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_constantXmaxYmaxZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_continuumXmaxYmaxZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_constantXmaxYmaxZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_continuumXmaxYmaxZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_constantXmaxYminZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_continuumXmaxYminZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_constantXmaxYminZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_continuumXmaxYminZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_constantXminYmaxZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_continuumXminYmaxZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_constantXminYmaxZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_continuumXminYmaxZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_constantXminYminZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_continuumXminYminZmax')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_constantXminYminZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('floating_fieldy_componentz_continuumXminYminZmin')
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
assert tests.boundaryConditionCheck(['floating_fieldy_componentx_constantXmax', 'floating_fieldy_componentx_constantXmaxYmax', 'floating_fieldy_componentx_constantXmaxYmaxZmax', 'floating_fieldy_componentx_constantXmaxYmaxZmin', 'floating_fieldy_componentx_constantXmaxYmin', 'floating_fieldy_componentx_constantXmaxYminZmax', 'floating_fieldy_componentx_constantXmaxYminZmin', 'floating_fieldy_componentx_constantXmaxZmax', 'floating_fieldy_componentx_constantXmaxZmin', 'floating_fieldy_componentx_constantXmin', 'floating_fieldy_componentx_constantXminYmax', 'floating_fieldy_componentx_constantXminYmaxZmax', 'floating_fieldy_componentx_constantXminYmaxZmin', 'floating_fieldy_componentx_constantXminYmin', 'floating_fieldy_componentx_constantXminYminZmax', 'floating_fieldy_componentx_constantXminYminZmin', 'floating_fieldy_componentx_constantXminZmax', 'floating_fieldy_componentx_constantXminZmin', 'floating_fieldy_componentx_constantYmax', 'floating_fieldy_componentx_constantYmaxZmax', 'floating_fieldy_componentx_constantYmaxZmin', 'floating_fieldy_componentx_constantYmin', 'floating_fieldy_componentx_constantYminZmax', 'floating_fieldy_componentx_constantYminZmin', 'floating_fieldy_componentx_constantZmax', 'floating_fieldy_componentx_constantZmin', 'floating_fieldy_componentx_continuumXmaxYmax', 'floating_fieldy_componentx_continuumXmaxYmaxZmax', 'floating_fieldy_componentx_continuumXmaxYmaxZmin', 'floating_fieldy_componentx_continuumXmaxYmin', 'floating_fieldy_componentx_continuumXmaxYminZmax', 'floating_fieldy_componentx_continuumXmaxYminZmin', 'floating_fieldy_componentx_continuumXmaxZmax', 'floating_fieldy_componentx_continuumXmaxZmin', 'floating_fieldy_componentx_continuumXmin', 'floating_fieldy_componentx_continuumXminYmax', 'floating_fieldy_componentx_continuumXminYmaxZmax', 'floating_fieldy_componentx_continuumXminYmaxZmin', 'floating_fieldy_componentx_continuumXminYmin', 'floating_fieldy_componentx_continuumXminYminZmax', 'floating_fieldy_componentx_continuumXminYminZmin', 'floating_fieldy_componentx_continuumXminZmax', 'floating_fieldy_componentx_continuumXminZmin', 'floating_fieldy_componentx_continuumYmax', 'floating_fieldy_componentx_continuumYmaxZmax', 'floating_fieldy_componentx_continuumYmaxZmin', 'floating_fieldy_componentx_continuumYmin', 'floating_fieldy_componentx_continuumYminZmax', 'floating_fieldy_componentx_continuumYminZmin', 'floating_fieldy_componentx_continuumZmax', 'floating_fieldy_componentx_continuumZmin', 'floating_fieldy_componenty_constantXmax', 'floating_fieldy_componenty_constantXmaxYmax', 'floating_fieldy_componenty_constantXmaxYmaxZmax', 'floating_fieldy_componenty_constantXmaxYmaxZmin', 'floating_fieldy_componenty_constantXmaxYmin', 'floating_fieldy_componenty_constantXmaxYminZmax', 'floating_fieldy_componenty_constantXmaxYminZmin', 'floating_fieldy_componenty_constantXmaxZmax', 'floating_fieldy_componenty_constantXmaxZmin', 'floating_fieldy_componenty_constantXmin', 'floating_fieldy_componenty_constantXminYmax', 'floating_fieldy_componenty_constantXminYmaxZmax', 'floating_fieldy_componenty_constantXminYmaxZmin', 'floating_fieldy_componenty_constantXminYmin', 'floating_fieldy_componenty_constantXminYminZmax', 'floating_fieldy_componenty_constantXminYminZmin', 'floating_fieldy_componenty_constantXminZmax', 'floating_fieldy_componenty_constantXminZmin', 'floating_fieldy_componenty_constantYmax', 'floating_fieldy_componenty_constantYmaxZmax', 'floating_fieldy_componenty_constantYmaxZmin', 'floating_fieldy_componenty_constantYmin', 'floating_fieldy_componenty_constantYminZmax', 'floating_fieldy_componenty_constantYminZmin', 'floating_fieldy_componenty_constantZmax', 'floating_fieldy_componenty_constantZmin', 'floating_fieldy_componenty_continuumXmaxYmax', 'floating_fieldy_componenty_continuumXmaxYmaxZmax', 'floating_fieldy_componenty_continuumXmaxYmaxZmin', 'floating_fieldy_componenty_continuumXmaxYmin', 'floating_fieldy_componenty_continuumXmaxYminZmax', 'floating_fieldy_componenty_continuumXmaxYminZmin', 'floating_fieldy_componenty_continuumXmaxZmax', 'floating_fieldy_componenty_continuumXmaxZmin', 'floating_fieldy_componenty_continuumXmin', 'floating_fieldy_componenty_continuumXminYmax', 'floating_fieldy_componenty_continuumXminYmaxZmax', 'floating_fieldy_componenty_continuumXminYmaxZmin', 'floating_fieldy_componenty_continuumXminYmin', 'floating_fieldy_componenty_continuumXminYminZmax', 'floating_fieldy_componenty_continuumXminYminZmin', 'floating_fieldy_componenty_continuumXminZmax', 'floating_fieldy_componenty_continuumXminZmin', 'floating_fieldy_componenty_continuumYmax', 'floating_fieldy_componenty_continuumYmaxZmax', 'floating_fieldy_componenty_continuumYmaxZmin', 'floating_fieldy_componenty_continuumYmin', 'floating_fieldy_componenty_continuumYminZmax', 'floating_fieldy_componenty_continuumYminZmin', 'floating_fieldy_componenty_continuumZmax', 'floating_fieldy_componenty_continuumZmin', 'floating_fieldy_componentz_constantXmax', 'floating_fieldy_componentz_constantXmaxYmax', 'floating_fieldy_componentz_constantXmaxYmaxZmax', 'floating_fieldy_componentz_constantXmaxYmaxZmin', 'floating_fieldy_componentz_constantXmaxYmin', 'floating_fieldy_componentz_constantXmaxYminZmax', 'floating_fieldy_componentz_constantXmaxYminZmin', 'floating_fieldy_componentz_constantXmaxZmax', 'floating_fieldy_componentz_constantXmaxZmin', 'floating_fieldy_componentz_constantXmin', 'floating_fieldy_componentz_constantXminYmax', 'floating_fieldy_componentz_constantXminYmaxZmax', 'floating_fieldy_componentz_constantXminYmaxZmin', 'floating_fieldy_componentz_constantXminYmin', 'floating_fieldy_componentz_constantXminYminZmax', 'floating_fieldy_componentz_constantXminYminZmin', 'floating_fieldy_componentz_constantXminZmax', 'floating_fieldy_componentz_constantXminZmin', 'floating_fieldy_componentz_constantYmax', 'floating_fieldy_componentz_constantYmaxZmax', 'floating_fieldy_componentz_constantYmaxZmin', 'floating_fieldy_componentz_constantYmin', 'floating_fieldy_componentz_constantYminZmax', 'floating_fieldy_componentz_constantYminZmin', 'floating_fieldy_componentz_constantZmax', 'floating_fieldy_componentz_constantZmin', 'floating_fieldy_componentz_continuumXmaxYmax', 'floating_fieldy_componentz_continuumXmaxYmaxZmax', 'floating_fieldy_componentz_continuumXmaxYmaxZmin', 'floating_fieldy_componentz_continuumXmaxYmin', 'floating_fieldy_componentz_continuumXmaxYminZmax', 'floating_fieldy_componentz_continuumXmaxYminZmin', 'floating_fieldy_componentz_continuumXmaxZmax', 'floating_fieldy_componentz_continuumXmaxZmin', 'floating_fieldy_componentz_continuumXmin', 'floating_fieldy_componentz_continuumXminYmax', 'floating_fieldy_componentz_continuumXminYmaxZmax', 'floating_fieldy_componentz_continuumXminYmaxZmin', 'floating_fieldy_componentz_continuumXminYmin', 'floating_fieldy_componentz_continuumXminYminZmax', 'floating_fieldy_componentz_continuumXminYminZmin', 'floating_fieldy_componentz_continuumXminZmax', 'floating_fieldy_componentz_continuumXminZmin', 'floating_fieldy_componentz_continuumYmax', 'floating_fieldy_componentz_continuumYmaxZmax', 'floating_fieldy_componentz_continuumYmaxZmin', 'floating_fieldy_componentz_continuumYmin', 'floating_fieldy_componentz_continuumYminZmax', 'floating_fieldy_componentz_continuumYminZmin', 'floating_fieldy_componentz_continuumZmax', 'floating_fieldy_componentz_continuumZmin'])
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