# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.7 $
# $Author: fyc $
# $Date: 2014/06/16 20:22:37 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

import tests

#Testing Boundary Condition creation using Generalized Force on Temperature Field
#The equation here is Heat_Eqn

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
findWidget('OOF3D:Fields & Equations Page:HPane:Equations:Heat_Eqn active').clicked()
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Chooser'), 'Generalized Force')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Generalized Force:boundary'), 'XmaxYmaxZmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('generalized_force_constantXmaxYmaxZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Generalized Force:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('generalized_force_continuumXmaxYmaxZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Generalized Force:profile:Chooser'), 'Continuum Profile')
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
assert tests.boundaryConditionCheck(['bc','bc<2>'])
findWidget('OOF3D Messages 1').resize(983, 200)
findWidget('OOF3D:Boundary Conditions Page:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(467, 309)
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Generalized Force:boundary'), 'XmaxYmaxZmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('generalized_force_constantXmaxYmaxZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Generalized Force:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Generalized Force:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('generalized_force_continuumXmaxYmaxZmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Generalized Force:boundary'), 'XmaxYminZmax')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('generalized_force_constantXmaxYminZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Generalized Force:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('generalized_force_continuumXmaxYminZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Generalized Force:profile:Chooser'), 'Continuum Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Generalized Force:boundary'), 'XmaxYminZmin')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('generalized_force_constantXmaxYminZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Generalized Force:profile:Chooser'), 'Constant Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Generalized Force:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('generalized_force_continuumXmaxYminZmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Generalized Force:boundary'), 'XminYmaxZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Generalized Force:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('generalized_force_constantXminYmaxZmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Generalized Force:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('generalized_force_continuumXminYmaxZmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Generalized Force:boundary'), 'XminYmaxZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Generalized Force:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('generalized_force_constantXminYmaxZmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
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
findWidget('Dialog-New Boundary Condition:name:Text').set_text('generalized_force_continuumXminYmaxZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Generalized Force:profile:Chooser'), 'Continuum Profile')
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Generalized Force:boundary'), 'XminYminZmax')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Generalized Force:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('generalized_force_constantXminYminZmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Generalized Force:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('generalized_force_continuumXminYminZmax')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Generalized Force:boundary'), 'XminYminZmin')
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Generalized Force:profile:Chooser'), 'Constant Profile')
findWidget('Dialog-New Boundary Condition:name:Text').set_text('generalized_force_constantXminYminZmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
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
setComboBox(findWidget('Dialog-New Boundary Condition:condition:Generalized Force:profile:Chooser'), 'Continuum Profile')
findWidget('Dialog-New Boundary Condition').resize(467, 309)
findWidget('Dialog-New Boundary Condition:name:Text').set_text('generalized_force_continuumXminYminZmin')
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint OOF.Mesh.Boundary_Conditions.New
assert tests.boundaryConditionCheck(['bc', 'bc<10>', 'bc<11>', 'bc<12>', 'bc<13>', 'bc<14>', 'bc<15>', 'bc<16>', 'bc<2>', 'bc<3>', 'bc<4>', 'bc<5>', 'bc<6>', 'bc<7>', 'bc<8>', 'bc<9>'])
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
