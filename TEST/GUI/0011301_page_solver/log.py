checkpoint toplevel widget mapped OOF2 Activity Viewer
# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:12:04 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov.

# Check that the solver page status is updated correctly when a named
# bc profile is edited.

import tests

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
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
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
findWidget('OOF2 Activity Viewer').resize(400, 300)
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
checkpoint OOF.File.Load.Data
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Solver')
assert tests.sensitive(1)
assert tests.statusTail("Stiffness Matrix: Symmetric\nUnsolved")
findWidget('OOF2').resize(550, 350)
findWidget('OOF2:Solver Page:Solve').clicked()
findWidget('OOF2 Messages 1').resize(553, 200)
checkpoint OOF.Solver.Solve
assert tests.sensitive(1)
assert tests.statusLine(2, "Solution Status: completed")
findWidget('OOF2:Navigation:Prev').clicked()
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(269)
findWidget('OOF2:Boundary Conditions Page:Pane:Profile:New').clicked()
checkpoint toplevel widget mapped New Named Profile
findWidget('New Named Profile').resize(255, 128)
findWidget('New Named Profile:gtk-ok').clicked()
findWidget('OOF2:Boundary Conditions Page:Pane:Profile:ProfileScroll:ProfileList').get_selection().select_path((0,))
checkpoint OOF.Mesh.Profiles.New
findWidget('OOF2:Boundary Conditions Page:Pane:Condition:BCScroll:BCList').get_selection().select_path((4,))
tree=findWidget('OOF2:Boundary Conditions Page:Pane:Condition:BCScroll:BCList')
column = tree.get_column(0)
tree.row_activated((4,), column)
checkpoint toplevel widget mapped Edit Boundary Condition
findWidget('Edit Boundary Condition').resize(399, 276)
setComboBox(findWidget('Edit Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Linear Profile')
findWidget('Edit Boundary Condition').resize(399, 300)
setComboBox(findWidget('Edit Boundary Condition:condition:Dirichlet:profile:Chooser'), 'Named Profile')
findWidget('Edit Boundary Condition:gtk-ok').clicked()
findWidget('OOF2 Messages 1').resize(770, 200)
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(269)
checkpoint OOF.Mesh.Boundary_Conditions.Edit
findWidget('OOF2:Navigation:Next').clicked()
assert tests.sensitive(1)
assert tests.statusTail("Stiffness Matrix: Symmetric\nUnsolved")
findWidget('OOF2:Solver Page:Solve').clicked()
checkpoint OOF.Solver.Solve
assert tests.sensitive(1)
assert tests.statusLine(2, "Solution Status: completed")
findWidget('OOF2:Navigation:Prev').clicked()
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(269)
findWidget('OOF2:Boundary Conditions Page:Pane:Profile:Edit').clicked()
checkpoint toplevel widget mapped Edit profile.
findWidget('Edit profile.').resize(246, 104)
findWidget('Edit profile.:profile:Continuum Profile:function').set_text('.0')
findWidget('Edit profile.:profile:Continuum Profile:function').set_text('2.0')
findWidget('Edit profile.:gtk-ok').clicked()
findWidget('OOF2:Boundary Conditions Page:Pane:Profile:ProfileScroll:ProfileList').get_selection().unselect_all()
findWidget('OOF2:Boundary Conditions Page:Pane:Profile:ProfileScroll:ProfileList').get_selection().select_path((0,))
checkpoint OOF.Mesh.Profiles.Edit
findWidget('OOF2:Navigation:Next').clicked()
assert tests.sensitive(1)
assert tests.statusTail("Stiffness Matrix: Symmetric\nUnsolved")
findMenu(findWidget('OOF2:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Fake FileSelector
findWidget('Fake FileSelector').resize(194, 72)
findWidget('Fake FileSelector:filename').set_text('s')
findWidget('Fake FileSelector:filename').set_text('so')
findWidget('Fake FileSelector:filename').set_text('sol')
findWidget('Fake FileSelector:filename').set_text('solv')
findWidget('Fake FileSelector:filename').set_text('solve')
findWidget('Fake FileSelector:filename').set_text('solver')
findWidget('Fake FileSelector:filename').set_text('solverp')
findWidget('Fake FileSelector:filename').set_text('solverpa')
findWidget('Fake FileSelector:filename').set_text('solverpag')
findWidget('Fake FileSelector:filename').set_text('solverpage')
findWidget('Fake FileSelector:filename').set_text('solverpage.')
findWidget('Fake FileSelector:filename').set_text('solverpage.l')
findWidget('Fake FileSelector:filename').set_text('solverpage.lo')
findWidget('Fake FileSelector:filename').set_text('solverpage.log')
findWidget('Fake FileSelector:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('solverpage.log')
findMenu(findWidget('OOF2:MenuBar'), 'File:Quit').activate()
