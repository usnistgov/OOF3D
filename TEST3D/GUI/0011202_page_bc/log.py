# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.6 $
# $Author: fyc $
# $Date: 2014/06/16 20:21:56 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

import tests

#Testing Boundary Condition creation using Dirichlet on a Displacement Field
#The field component is x here

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
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Equation.Activate
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Boundary Conditions')
checkpoint page installed Boundary Conditions
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 289)
findWidget('Dialog-New Boundary Condition:name:Auto').clicked()
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_constantXmax')
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
assert tests.boundaryConditionCheck(['dirichlet_fieldx_componentx_constantXmax'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'Xmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_constantXmin')
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
assert tests.boundaryConditionCheck(['dirichlet_fieldx_componentx_constantXmax','dirichlet_fieldx_componentx_constantXmin'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_continuumXmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'Ymax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_constantYmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_continuumYmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'Ymin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_constantYmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_continuumYmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'Zmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_constantZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_continuumZmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'Zmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_constantZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_continuumZmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XmaxYmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_constantXmaxYmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_continuumXmaxYmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XmaxYmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_constantXmaxYmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_continuumXmaxYmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XmaxZmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_constantXmaxZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_continuumXmaxZmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XmaxZmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_constantXmaxZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_continuumXmaxZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XminYmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_constantXminYmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_continuumXminYmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XminYmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_constantXminYmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_continuumXminYmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XminZmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_constantXminZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_continuumXminZmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XminZmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_constantXminZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_continuumXminZmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'YmaxZmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_constantYmaxZmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_continuumYmaxZmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'YmaxZmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_constantYmaxZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_continuumYmaxZmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'YminZmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_constantYminZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_continuumYminZmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'YminZmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_constantYminZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_continuumYminZmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XmaxYmaxZmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_constantXmaxYmaxZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_continuumXmaxYmaxZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XmaxYmaxZmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_constantXmaxYmaxZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_continuumXmaxYmaxZmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XmaxYminZmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_constantXmaxYminZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_continuumXmaxYminZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XmaxYminZmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_constantXmaxYminZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_continuumXmaxYminZmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XminYmaxZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_constantXminYmaxZmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_continuumXminYmaxZmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XminYmaxZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_constantXminYmaxZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_continuumXminYmaxZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XminYminZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_constantXminYminZmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_continuumXminYminZmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XminYminZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_constantXminYminZmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentx_continuumXminYminZmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'Xmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_constantXmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:eqn_component'), 'y')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'Xmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_constantXmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_continuumXmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'Ymax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_constantYmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_continuumYmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'Ymin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_constantYmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_continuumYmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'Zmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_constantZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_continuumZmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'Zmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_constantZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_continuumZmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XmaxYmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_constantXmaxYmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_continuumXmaxYmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XmaxYmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_constantXmaxYmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_continuumXmaxYmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XmaxZmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_constantXmaxZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_continuumXmaxZmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XmaxZmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_constantXmaxZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_continuumXmaxZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XminYmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_constantXminYmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_continuumXminYmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XminYmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_constantXminYmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_continuumXminYmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XminZmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_constantXminZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_continuumXminZmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XminZmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_constantXminZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_continuumXminZmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'YmaxZmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_constantYmaxZmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_continuumYmaxZmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'YmaxZmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_constantYmaxZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_continuumYmaxZmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'YminZmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_constantYminZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_continuumYminZmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'YminZmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_constantYminZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_continuumYminZmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XmaxYmaxZmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_constantXmaxYmaxZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_continuumXmaxYmaxZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XmaxYmaxZmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_constantXmaxYmaxZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_continuumXmaxYmaxZmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XmaxYminZmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_constantXmaxYminZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_continuumXmaxYminZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XmaxYminZmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_constantXmaxYminZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_continuumXmaxYminZmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XminYmaxZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_constantXminYmaxZmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_continuumXminYmaxZmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XminYmaxZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_constantXminYmaxZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_continuumXminYmaxZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XminYminZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_constantXminYminZmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_continuumXminYminZmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XminYminZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_constantXminYminZmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componenty_continuumXminYminZmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'Xmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:eqn_component'), 'z')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_constantXmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'Xmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_constantXmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_continuumXmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'Ymax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_constantYmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_continuumYmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'Ymin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_constantYmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_continuumYmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'Zmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_constantZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_continuumZmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'Zmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_constantZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_continuumZmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XmaxYmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_constantXmaxYmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_continuumXmaxYmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XmaxYmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_constantXmaxYmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_continuumXmaxYmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XmaxZmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_constantXmaxZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_continuumXmaxZmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XmaxZmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_constantXmaxZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_continuumXmaxZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XminYmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_constantXminYmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_continuumXminYmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XminYmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_constantXminYmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_continuumXminYmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XminZmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_constantXminZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_continuumXminZmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XminZmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_constantXminZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_continuumXminZmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'YmaxZmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_constantYmaxZmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_continuumYmaxZmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'YmaxZmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_constantYmaxZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_continuumYmaxZmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'YminZmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_constantYminZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_continuumYminZmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'YminZmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_constantYminZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_continuumYminZmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XmaxYmaxZmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_constantXmaxYmaxZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_continuumXmaxYmaxZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XmaxYmaxZmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_constantXmaxYmaxZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_continuumXmaxYmaxZmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XmaxYminZmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_constantXmaxYminZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_continuumXmaxYminZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XmaxYminZmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_constantXmaxYminZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_continuumXmaxYminZmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XminYmaxZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_constantXminYmaxZmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_continuumXminYmaxZmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XminYmaxZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_constantXminYmaxZmin')
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_continuumXminYmaxZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XminYminZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_constantXminYminZmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_continuumXminYminZmax')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XminYminZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_constantXminYminZmin')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_fieldx_componentz_continuumXminYminZmin')
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
assert tests.boundaryConditionCheck(['dirichlet_fieldx_componentx_constantXmax', 'dirichlet_fieldx_componentx_constantXmaxYmax', 'dirichlet_fieldx_componentx_constantXmaxYmaxZmax', 'dirichlet_fieldx_componentx_constantXmaxYmaxZmin', 'dirichlet_fieldx_componentx_constantXmaxYmin', 'dirichlet_fieldx_componentx_constantXmaxYminZmax', 'dirichlet_fieldx_componentx_constantXmaxYminZmin', 'dirichlet_fieldx_componentx_constantXmaxZmax', 'dirichlet_fieldx_componentx_constantXmaxZmin', 'dirichlet_fieldx_componentx_constantXmin', 'dirichlet_fieldx_componentx_constantXminYmax', 'dirichlet_fieldx_componentx_constantXminYmaxZmax', 'dirichlet_fieldx_componentx_constantXminYmaxZmin', 'dirichlet_fieldx_componentx_constantXminYmin', 'dirichlet_fieldx_componentx_constantXminYminZmax', 'dirichlet_fieldx_componentx_constantXminYminZmin', 'dirichlet_fieldx_componentx_constantXminZmax', 'dirichlet_fieldx_componentx_constantXminZmin', 'dirichlet_fieldx_componentx_constantYmax', 'dirichlet_fieldx_componentx_constantYmaxZmax', 'dirichlet_fieldx_componentx_constantYmaxZmin', 'dirichlet_fieldx_componentx_constantYmin', 'dirichlet_fieldx_componentx_constantYminZmax', 'dirichlet_fieldx_componentx_constantYminZmin', 'dirichlet_fieldx_componentx_constantZmax', 'dirichlet_fieldx_componentx_constantZmin', 'dirichlet_fieldx_componentx_continuumXmaxYmax', 'dirichlet_fieldx_componentx_continuumXmaxYmaxZmax', 'dirichlet_fieldx_componentx_continuumXmaxYmaxZmin', 'dirichlet_fieldx_componentx_continuumXmaxYmin', 'dirichlet_fieldx_componentx_continuumXmaxYminZmax', 'dirichlet_fieldx_componentx_continuumXmaxYminZmin', 'dirichlet_fieldx_componentx_continuumXmaxZmax', 'dirichlet_fieldx_componentx_continuumXmaxZmin', 'dirichlet_fieldx_componentx_continuumXmin', 'dirichlet_fieldx_componentx_continuumXminYmax', 'dirichlet_fieldx_componentx_continuumXminYmaxZmax', 'dirichlet_fieldx_componentx_continuumXminYmaxZmin', 'dirichlet_fieldx_componentx_continuumXminYmin', 'dirichlet_fieldx_componentx_continuumXminYminZmax', 'dirichlet_fieldx_componentx_continuumXminYminZmin', 'dirichlet_fieldx_componentx_continuumXminZmax', 'dirichlet_fieldx_componentx_continuumXminZmin', 'dirichlet_fieldx_componentx_continuumYmax', 'dirichlet_fieldx_componentx_continuumYmaxZmax', 'dirichlet_fieldx_componentx_continuumYmaxZmin', 'dirichlet_fieldx_componentx_continuumYmin', 'dirichlet_fieldx_componentx_continuumYminZmax', 'dirichlet_fieldx_componentx_continuumYminZmin', 'dirichlet_fieldx_componentx_continuumZmax', 'dirichlet_fieldx_componentx_continuumZmin', 'dirichlet_fieldx_componenty_constantXmax', 'dirichlet_fieldx_componenty_constantXmaxYmax', 'dirichlet_fieldx_componenty_constantXmaxYmaxZmax', 'dirichlet_fieldx_componenty_constantXmaxYmaxZmin', 'dirichlet_fieldx_componenty_constantXmaxYmin', 'dirichlet_fieldx_componenty_constantXmaxYminZmax', 'dirichlet_fieldx_componenty_constantXmaxYminZmin', 'dirichlet_fieldx_componenty_constantXmaxZmax', 'dirichlet_fieldx_componenty_constantXmaxZmin', 'dirichlet_fieldx_componenty_constantXmin', 'dirichlet_fieldx_componenty_constantXminYmax', 'dirichlet_fieldx_componenty_constantXminYmaxZmax', 'dirichlet_fieldx_componenty_constantXminYmaxZmin', 'dirichlet_fieldx_componenty_constantXminYmin', 'dirichlet_fieldx_componenty_constantXminYminZmax', 'dirichlet_fieldx_componenty_constantXminYminZmin', 'dirichlet_fieldx_componenty_constantXminZmax', 'dirichlet_fieldx_componenty_constantXminZmin', 'dirichlet_fieldx_componenty_constantYmax', 'dirichlet_fieldx_componenty_constantYmaxZmax', 'dirichlet_fieldx_componenty_constantYmaxZmin', 'dirichlet_fieldx_componenty_constantYmin', 'dirichlet_fieldx_componenty_constantYminZmax', 'dirichlet_fieldx_componenty_constantYminZmin', 'dirichlet_fieldx_componenty_constantZmax', 'dirichlet_fieldx_componenty_constantZmin', 'dirichlet_fieldx_componenty_continuumXmaxYmax', 'dirichlet_fieldx_componenty_continuumXmaxYmaxZmax', 'dirichlet_fieldx_componenty_continuumXmaxYmaxZmin', 'dirichlet_fieldx_componenty_continuumXmaxYmin', 'dirichlet_fieldx_componenty_continuumXmaxYminZmax', 'dirichlet_fieldx_componenty_continuumXmaxYminZmin', 'dirichlet_fieldx_componenty_continuumXmaxZmax', 'dirichlet_fieldx_componenty_continuumXmaxZmin', 'dirichlet_fieldx_componenty_continuumXmin', 'dirichlet_fieldx_componenty_continuumXminYmax', 'dirichlet_fieldx_componenty_continuumXminYmaxZmax', 'dirichlet_fieldx_componenty_continuumXminYmaxZmin', 'dirichlet_fieldx_componenty_continuumXminYmin', 'dirichlet_fieldx_componenty_continuumXminYminZmax', 'dirichlet_fieldx_componenty_continuumXminYminZmin', 'dirichlet_fieldx_componenty_continuumXminZmax', 'dirichlet_fieldx_componenty_continuumXminZmin', 'dirichlet_fieldx_componenty_continuumYmax', 'dirichlet_fieldx_componenty_continuumYmaxZmax', 'dirichlet_fieldx_componenty_continuumYmaxZmin', 'dirichlet_fieldx_componenty_continuumYmin', 'dirichlet_fieldx_componenty_continuumYminZmax', 'dirichlet_fieldx_componenty_continuumYminZmin', 'dirichlet_fieldx_componenty_continuumZmax', 'dirichlet_fieldx_componenty_continuumZmin', 'dirichlet_fieldx_componentz_constantXmax', 'dirichlet_fieldx_componentz_constantXmaxYmax', 'dirichlet_fieldx_componentz_constantXmaxYmaxZmax', 'dirichlet_fieldx_componentz_constantXmaxYmaxZmin', 'dirichlet_fieldx_componentz_constantXmaxYmin', 'dirichlet_fieldx_componentz_constantXmaxYminZmax', 'dirichlet_fieldx_componentz_constantXmaxYminZmin', 'dirichlet_fieldx_componentz_constantXmaxZmax', 'dirichlet_fieldx_componentz_constantXmaxZmin', 'dirichlet_fieldx_componentz_constantXmin', 'dirichlet_fieldx_componentz_constantXminYmax', 'dirichlet_fieldx_componentz_constantXminYmaxZmax', 'dirichlet_fieldx_componentz_constantXminYmaxZmin', 'dirichlet_fieldx_componentz_constantXminYmin', 'dirichlet_fieldx_componentz_constantXminYminZmax', 'dirichlet_fieldx_componentz_constantXminYminZmin', 'dirichlet_fieldx_componentz_constantXminZmax', 'dirichlet_fieldx_componentz_constantXminZmin', 'dirichlet_fieldx_componentz_constantYmax', 'dirichlet_fieldx_componentz_constantYmaxZmax', 'dirichlet_fieldx_componentz_constantYmaxZmin', 'dirichlet_fieldx_componentz_constantYmin', 'dirichlet_fieldx_componentz_constantYminZmax', 'dirichlet_fieldx_componentz_constantYminZmin', 'dirichlet_fieldx_componentz_constantZmax', 'dirichlet_fieldx_componentz_constantZmin', 'dirichlet_fieldx_componentz_continuumXmaxYmax', 'dirichlet_fieldx_componentz_continuumXmaxYmaxZmax', 'dirichlet_fieldx_componentz_continuumXmaxYmaxZmin', 'dirichlet_fieldx_componentz_continuumXmaxYmin', 'dirichlet_fieldx_componentz_continuumXmaxYminZmax', 'dirichlet_fieldx_componentz_continuumXmaxYminZmin', 'dirichlet_fieldx_componentz_continuumXmaxZmax', 'dirichlet_fieldx_componentz_continuumXmaxZmin', 'dirichlet_fieldx_componentz_continuumXmin', 'dirichlet_fieldx_componentz_continuumXminYmax', 'dirichlet_fieldx_componentz_continuumXminYmaxZmax', 'dirichlet_fieldx_componentz_continuumXminYmaxZmin', 'dirichlet_fieldx_componentz_continuumXminYmin', 'dirichlet_fieldx_componentz_continuumXminYminZmax', 'dirichlet_fieldx_componentz_continuumXminYminZmin', 'dirichlet_fieldx_componentz_continuumXminZmax', 'dirichlet_fieldx_componentz_continuumXminZmin', 'dirichlet_fieldx_componentz_continuumYmax', 'dirichlet_fieldx_componentz_continuumYmaxZmax', 'dirichlet_fieldx_componentz_continuumYmaxZmin', 'dirichlet_fieldx_componentz_continuumYmin', 'dirichlet_fieldx_componentz_continuumYminZmax', 'dirichlet_fieldx_componentz_continuumYminZmin', 'dirichlet_fieldx_componentz_continuumZmax', 'dirichlet_fieldx_componentz_continuumZmin'])
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