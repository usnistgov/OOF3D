checkpoint toplevel widget mapped OOF2 Activity Viewer
# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:11:58 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov.

checkpoint meshable button set
## Test that the On/Off (EnableDisable) button on the boundary
checkpoint microstructure page sensitized
## condition page works properly.

import tests
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
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint mesh bdy page updated
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint boundary page updated
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint mesh bdy page updated
checkpoint boundary page updated
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
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.File.LoadStartUp.Data
findWidget('OOF2 Activity Viewer').resize(400, 300)
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint meshable button set
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
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
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.File.LoadStartUp.Data
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Boundary Conditions')
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(230)
findWidget('OOF2:Boundary Conditions Page:Pane:Condition:BCScroll:BCList').get_selection().select_path((2,))
assert not tests.bcDisabled(0)
assert not tests.bcDisabled(2)
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(230)
findWidget('OOF2:Boundary Conditions Page:Pane:Condition:EnableDisable').clicked()
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(230)
findWidget('OOF2 Messages 1').resize(553, 200)
checkpoint OOF.Mesh.Boundary_Conditions.Disable
assert not tests.bcDisabled(0)
assert tests.bcDisabled(2)
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(230)
setComboBox(findWidget('OOF2:Boundary Conditions Page:Microstructure'), 'el_shape.png')
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(230)
findWidget('OOF2:Boundary Conditions Page:Pane:Condition:BCScroll:BCList').get_selection().select_path((0,))
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(230)
findWidget('OOF2:Boundary Conditions Page:Pane:Condition:EnableDisable').clicked()
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(230)
findWidget('OOF2 Messages 1').resize(561, 200)
checkpoint OOF.Mesh.Boundary_Conditions.Disable
assert tests.bcDisabled(0)
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(230)
setComboBox(findWidget('OOF2:Boundary Conditions Page:Microstructure'), 'cyallow.png')
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(230)
findWidget('OOF2:Boundary Conditions Page:Pane:Condition:BCScroll:BCList').get_selection().select_path((2,))
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(230)
findWidget('OOF2:Boundary Conditions Page:Pane:Condition:EnableDisable').clicked()
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(230)
checkpoint OOF.Mesh.Boundary_Conditions.Enable
assert not tests.bcDisabled(0)
assert not tests.bcDisabled(2)
findWidget('OOF2:Navigation:Prev').clicked()
findWidget('OOF2').resize(676, 350)
findWidget('OOF2:Fields & Equations Page:HPane:Equations:Force_Balance active').clicked()
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Subproblem.Equation.Deactivate
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Boundary Conditions')
assert not tests.bcDisabled(0)
assert not tests.bcDisabled(1)
assert not tests.bcDisabled(2)
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(285)
findWidget('OOF2:Boundary Conditions Page:Pane:Condition:EnableDisable').clicked()
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(285)
checkpoint OOF.Mesh.Boundary_Conditions.Disable
assert not tests.bcDisabled(0)
assert not tests.bcDisabled(1)
assert tests.bcDisabled(2)
findWidget('OOF2:Boundary Conditions Page:Pane:Condition:EnableDisable').clicked()
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(285)
checkpoint OOF.Mesh.Boundary_Conditions.Enable
assert not tests.bcDisabled(0)
assert not tests.bcDisabled(1)
assert not tests.bcDisabled(2)
findMenu(findWidget('OOF2:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(194, 72)
findWidget('Dialog-Python_Log:filename').set_text('b')
findWidget('Dialog-Python_Log:filename').set_text('bc')
findWidget('Dialog-Python_Log:filename').set_text('bco')
findWidget('Dialog-Python_Log:filename').set_text('bcon')
findWidget('Dialog-Python_Log:filename').set_text('bcono')
findWidget('Dialog-Python_Log:filename').set_text('bconof')
findWidget('Dialog-Python_Log:filename').set_text('bconoff')
findWidget('Dialog-Python_Log:filename').set_text('bconoff.')
findWidget('Dialog-Python_Log:filename').set_text('bconoff.p')
findWidget('Dialog-Python_Log:filename').set_text('bconoff.py')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
findMenu(findWidget('OOF2:MenuBar'), 'File:Quit').activate()
checkpoint OOF.ActivityViewer.File.Close
