# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.7 $
# $Author: fyc $
# $Date: 2014/06/13 21:45:15 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

import tests

#Testing Boundary Condition creation using Dirichlet on a Temperature Field
#The field component is not applicable here

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
findWidget('OOF3D:Fields & Equations Page:HPane:Fields:Temperature defined').clicked()
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
findWidget('OOF3D:Fields & Equations Page:HPane:Fields:Temperature active').clicked()
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
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Equation.Activate
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Boundary Conditions')
checkpoint page installed Boundary Conditions
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_constantXmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['bc'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_continiumXmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['bc','bc<2>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'Xmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_constantXmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['bc','bc<2>','bc<3>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_continuumXmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['bc','bc<2>','bc<3>','bc<4>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'Ymax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_constantYmax')
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
assert tests.boundaryConditionCheck(['bc','bc<2>','bc<3>','bc<4>','bc<5>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_continuumYmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['bc','bc<2>','bc<3>','bc<4>','bc<5>','bc<6>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'Ymin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_constantYmin')
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
assert tests.boundaryConditionCheck(['bc','bc<2>','bc<3>','bc<4>','bc<5>','bc<6>','bc<7>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_continuumYmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['bc','bc<2>','bc<3>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'Zmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_constantZmax')
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
assert tests.boundaryConditionCheck(['bc','bc<2>','bc<3>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_continuumZmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<2>','bc<3>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'Zmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_constantZmin')
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
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<2>','bc<3>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_continuumZmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<2>','bc<3>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XmaxYmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_constantXmaxYmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<2>','bc<3>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_continuumXmaxYmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<2>','bc<3>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XmaxYmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_constantXmaxYmin')
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
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<2>','bc<3>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_continuumXmaxYmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<2>','bc<3>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XmaxZmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_constantXmaxZmax')
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
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<2>','bc<3>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_continuumXmaxZmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<2>','bc<3>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XmaxZmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_constantXmaxZmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<19>','bc<2>','bc<3>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_continuumXmaxZmin')
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
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<19>','bc<20>','bc<2>','bc<3>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XminYmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_constantXminYmax')
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
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<19>','bc<20>','bc<21>','bc<2>','bc<3>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_continuumXminYmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<19>','bc<20>','bc<21>','bc<22>','bc<2>','bc<3>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XminYmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_constantXminYmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<19>','bc<20>','bc<21>','bc<22>','bc<23>','bc<2>','bc<3>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_continuumXminYmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<19>','bc<20>','bc<21>','bc<22>','bc<23>','bc<24>','bc<2>','bc<3>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XminZmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_constantXminZmax')
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
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<19>','bc<20>','bc<21>','bc<22>','bc<23>','bc<24>','bc<25>','bc<2>','bc<3>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_continuumXminZmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<19>','bc<20>','bc<21>','bc<22>','bc<23>','bc<24>','bc<25>','bc<26>','bc<2>','bc<3>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XminZmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_constantXminZmin')
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
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<19>','bc<20>','bc<21>','bc<22>','bc<23>','bc<24>','bc<25>','bc<26>','bc<27>','bc<2>','bc<3>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_continuumXminZmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<19>','bc<20>','bc<21>','bc<22>','bc<23>','bc<24>','bc<25>','bc<26>','bc<27>','bc<28>','bc<2>','bc<3>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'YmaxZmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_constantYmaxZmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<19>','bc<20>','bc<21>','bc<22>','bc<23>','bc<24>','bc<25>','bc<26>','bc<27>','bc<28>','bc<29>','bc<2>','bc<3>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_continuumYmaxZmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<19>','bc<20>','bc<21>','bc<22>','bc<23>','bc<24>','bc<25>','bc<26>','bc<27>','bc<28>','bc<29>','bc<2>','bc<30>','bc<3>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'YmaxZmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_constantYmaxZmin')
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
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<19>','bc<20>','bc<21>','bc<22>','bc<23>','bc<24>','bc<25>','bc<26>','bc<27>','bc<28>','bc<29>','bc<2>','bc<30>','bc<31>','bc<3>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_continuumYmaxZmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<19>','bc<20>','bc<21>','bc<22>','bc<23>','bc<24>','bc<25>','bc<26>','bc<27>','bc<28>','bc<29>','bc<2>','bc<30>','bc<31>','bc<32>','bc<3>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'YminZmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_constantYminZmax')
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
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<19>','bc<20>','bc<21>','bc<22>','bc<23>','bc<24>','bc<25>','bc<26>','bc<27>','bc<28>','bc<29>','bc<2>','bc<30>','bc<31>','bc<32>','bc<33>','bc<3>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_continuumYminZmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<19>','bc<20>','bc<21>','bc<22>','bc<23>','bc<24>','bc<25>','bc<26>','bc<27>','bc<28>','bc<29>','bc<2>','bc<30>','bc<31>','bc<32>','bc<33>','bc<34>','bc<3>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'YminZmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_constantYminZmin')
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
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<19>','bc<20>','bc<21>','bc<22>','bc<23>','bc<24>','bc<25>','bc<26>','bc<27>','bc<28>','bc<29>','bc<2>','bc<30>','bc<31>','bc<32>','bc<33>','bc<34>','bc<35>','bc<3>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_continuumYminZmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<19>','bc<20>','bc<21>','bc<22>','bc<23>','bc<24>','bc<25>','bc<26>','bc<27>','bc<28>','bc<29>','bc<2>','bc<30>','bc<31>','bc<32>','bc<33>','bc<34>','bc<35>','bc<36>','bc<3>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XmaxYmaxZmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_constantXmaxYmaxZmax')
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
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<19>','bc<20>','bc<21>','bc<22>','bc<23>','bc<24>','bc<25>','bc<26>','bc<27>','bc<28>','bc<29>','bc<2>','bc<30>','bc<31>','bc<32>','bc<33>','bc<34>','bc<35>','bc<36>','bc<37>','bc<3>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_continuumXmaxYmaxZmax')
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
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<19>','bc<20>','bc<21>','bc<22>','bc<23>','bc<24>','bc<25>','bc<26>','bc<27>','bc<28>','bc<29>','bc<2>','bc<30>','bc<31>','bc<32>','bc<33>','bc<34>','bc<35>','bc<36>','bc<37>','bc<38>','bc<3>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XmaxYmaxZmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_constantXmaxYmaxZmin')
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
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<19>','bc<20>','bc<21>','bc<22>','bc<23>','bc<24>','bc<25>','bc<26>','bc<27>','bc<28>','bc<29>','bc<2>','bc<30>','bc<31>','bc<32>','bc<33>','bc<34>','bc<35>','bc<36>','bc<37>','bc<38>','bc<39>','bc<3>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_continuumXmaxYmaxZmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<19>','bc<20>','bc<21>','bc<22>','bc<23>','bc<24>','bc<25>','bc<26>','bc<27>','bc<28>','bc<29>','bc<2>','bc<30>','bc<31>','bc<32>','bc<33>','bc<34>','bc<35>','bc<36>','bc<37>','bc<38>','bc<39>','bc<3>','bc<40>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XmaxYminZmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_constantXmaxYminZmax')
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
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<19>','bc<20>','bc<21>','bc<22>','bc<23>','bc<24>','bc<25>','bc<26>','bc<27>','bc<28>','bc<29>','bc<2>','bc<30>','bc<31>','bc<32>','bc<33>','bc<34>','bc<35>','bc<36>','bc<37>','bc<38>','bc<39>','bc<3>','bc<40>','bc<41>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_continuumXmaxYminZmax')
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
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<19>','bc<20>','bc<21>','bc<22>','bc<23>','bc<24>','bc<25>','bc<26>','bc<27>','bc<28>','bc<29>','bc<2>','bc<30>','bc<31>','bc<32>','bc<33>','bc<34>','bc<35>','bc<36>','bc<37>','bc<38>','bc<39>','bc<3>','bc<40>','bc<41>','bc<42>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XmaxYminZmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_constantXmaxYminZmin')
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
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<19>','bc<20>','bc<21>','bc<22>','bc<23>','bc<24>','bc<25>','bc<26>','bc<27>','bc<28>','bc<29>','bc<2>','bc<30>','bc<31>','bc<32>','bc<33>','bc<34>','bc<35>','bc<36>','bc<37>','bc<38>','bc<39>','bc<3>','bc<40>','bc<41>','bc<42>','bc<43>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_continuumXmaxYminZmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<19>','bc<20>','bc<21>','bc<22>','bc<23>','bc<24>','bc<25>','bc<26>','bc<27>','bc<28>','bc<29>','bc<2>','bc<30>','bc<31>','bc<32>','bc<33>','bc<34>','bc<35>','bc<36>','bc<37>','bc<38>','bc<39>','bc<3>','bc<40>','bc<41>','bc<42>','bc<43>','bc<44>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XminYmaxZmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_continuumXminYmaxZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_constantXminYmaxZmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<19>','bc<20>','bc<21>','bc<22>','bc<23>','bc<24>','bc<25>','bc<26>','bc<27>','bc<28>','bc<29>','bc<2>','bc<30>','bc<31>','bc<32>','bc<33>','bc<34>','bc<35>','bc<36>','bc<37>','bc<38>','bc<39>','bc<3>','bc<40>','bc<41>','bc<42>','bc<43>','bc<44>','bc<45>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_continuumXminYmaxZmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<19>','bc<20>','bc<21>','bc<22>','bc<23>','bc<24>','bc<25>','bc<26>','bc<27>','bc<28>','bc<29>','bc<2>','bc<30>','bc<31>','bc<32>','bc<33>','bc<34>','bc<35>','bc<36>','bc<37>','bc<38>','bc<39>','bc<3>','bc<40>','bc<41>','bc<42>','bc<43>','bc<44>','bc<45>','bc<46>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XminYmaxZmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_continuumXminYmaxZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_constantXminYmaxZmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<19>','bc<20>','bc<21>','bc<22>','bc<23>','bc<24>','bc<25>','bc<26>','bc<27>','bc<28>','bc<29>','bc<2>','bc<30>','bc<31>','bc<32>','bc<33>','bc<34>','bc<35>','bc<36>','bc<37>','bc<38>','bc<39>','bc<3>','bc<40>','bc<41>','bc<42>','bc<43>','bc<44>','bc<45>','bc<46>','bc<47>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_continuumXminYmaxZmin')
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
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<19>','bc<20>','bc<21>','bc<22>','bc<23>','bc<24>','bc<25>','bc<26>','bc<27>','bc<28>','bc<29>','bc<2>','bc<30>','bc<31>','bc<32>','bc<33>','bc<34>','bc<35>','bc<36>','bc<37>','bc<38>','bc<39>','bc<3>','bc<40>','bc<41>','bc<42>','bc<43>','bc<44>','bc<45>','bc<46>','bc<47>','bc<48>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XminYminZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_constantXminYminZmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<19>','bc<20>','bc<21>','bc<22>','bc<23>','bc<24>','bc<25>','bc<26>','bc<27>','bc<28>','bc<29>','bc<2>','bc<30>','bc<31>','bc<32>','bc<33>','bc<34>','bc<35>','bc<36>','bc<37>','bc<38>','bc<39>','bc<3>','bc<40>','bc<41>','bc<42>','bc<43>','bc<44>','bc<45>','bc<46>','bc<47>','bc<48>','bc<49>','bc<4>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_continuumXminYminZmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<19>','bc<20>','bc<21>','bc<22>','bc<23>','bc<24>','bc<25>','bc<26>','bc<27>','bc<28>','bc<29>','bc<2>','bc<30>','bc<31>','bc<32>','bc<33>','bc<34>','bc<35>','bc<36>','bc<37>','bc<38>','bc<39>','bc<3>','bc<40>','bc<41>','bc<42>','bc<43>','bc<44>','bc<45>','bc<46>','bc<47>','bc<48>','bc<49>','bc<4>','bc<50>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:boundary'), 'XminYminZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_constantXminYminZmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<19>','bc<20>','bc<21>','bc<22>','bc<23>','bc<24>','bc<25>','bc<26>','bc<27>','bc<28>','bc<29>','bc<2>','bc<30>','bc<31>','bc<32>','bc<33>','bc<34>','bc<35>','bc<36>','bc<37>','bc<38>','bc<39>','bc<3>','bc<40>','bc<41>','bc<42>','bc<43>','bc<44>','bc<45>','bc<46>','bc<47>','bc<48>','bc<49>','bc<4>','bc<50>','bc<51>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(412, 265)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('dirichlet_continuumXminYminZmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['bc','bc<10>','bc<11>','bc<12>','bc<13>','bc<14>','bc<15>','bc<16>','bc<17>','bc<18>','bc<19>','bc<20>','bc<21>','bc<22>','bc<23>','bc<24>','bc<25>','bc<26>','bc<27>','bc<28>','bc<29>','bc<2>','bc<30>','bc<31>','bc<32>','bc<33>','bc<34>','bc<35>','bc<36>','bc<37>','bc<38>','bc<39>','bc<3>','bc<40>','bc<41>','bc<42>','bc<43>','bc<44>','bc<45>','bc<46>','bc<47>','bc<48>','bc<49>','bc<4>','bc<50>','bc<51>','bc<52>','bc<5>','bc<6>','bc<7>','bc<8>','bc<9>'])
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