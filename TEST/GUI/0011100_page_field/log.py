checkpoint toplevel widget mapped OOF2 Activity Viewer
# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:11:39 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov.

import tests

setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Fields & Equations')
findWidget('OOF2:Fields & Equations Page:HPane').set_position(243)
assert tests.sensitization0()
findMenu(findWidget('OOF2:MenuBar'), 'File:Load:Data').activate()
checkpoint toplevel widget mapped Dialog-Data
findWidget('Dialog-Data').resize(190, 70)
findWidget('Dialog-Data:filename').set_text('.')
findWidget('Dialog-Data:filename').set_text('..')
findWidget('Dialog-Data:filename').set_text('../')
findWidget('Dialog-Data:filename').set_text('../.')
findWidget('Dialog-Data:filename').set_text('../..')
findWidget('Dialog-Data:filename').set_text('../../')
findWidget('Dialog-Data:filename').set_text('../../e')
findWidget('Dialog-Data:filename').set_text('../../ex')
findWidget('Dialog-Data:filename').set_text('../../exa')
findWidget('Dialog-Data:filename').set_text('../../exam')
findWidget('Dialog-Data:filename').set_text('../../examp')
findWidget('Dialog-Data:filename').set_text('../../exampl')
findWidget('Dialog-Data:filename').set_text('../../example')
findWidget('Dialog-Data:filename').set_text('../../examples')
findWidget('Dialog-Data:filename').set_text('../../examples/')
findWidget('Dialog-Data:filename').set_text('../../examples/t')
findWidget('Dialog-Data:filename').set_text('../../examples/tw')
findWidget('Dialog-Data:filename').set_text('../../examples/two')
findWidget('Dialog-Data:filename').set_text('../../examples/two_')
findWidget('Dialog-Data:filename').set_text('../../examples/two_c')
findWidget('Dialog-Data:filename').set_text('../../examples/two_ci')
findWidget('Dialog-Data:filename').set_text('../../examples/two_cir')
findWidget('Dialog-Data:filename').set_text('../../examples/two_circ')
findWidget('Dialog-Data:filename').set_text('../../examples/two_circl')
findWidget('Dialog-Data:filename').set_text('../../examples/two_circle')
findWidget('Dialog-Data:filename').set_text('../../examples/two_circles')
findWidget('Dialog-Data:filename').set_text('../../examples/two_circles.')
findWidget('Dialog-Data:filename').set_text('../../examples/two_circles.s')
findWidget('Dialog-Data:filename').set_text('../../examples/two_circles.sk')
findWidget('Dialog-Data:filename').set_text('../../examples/two_circles.ske')
findWidget('Dialog-Data:filename').set_text('../../examples/two_circles.skel')
findWidget('Dialog-Data:filename').set_text('../../examples/two_circles.skele')
findWidget('Dialog-Data:filename').set_text('../../examples/two_circles.skelet')
findWidget('Dialog-Data:filename').set_text('../../examples/two_circles.skeleto')
findWidget('Dialog-Data:filename').set_text('../../examples/two_circles.skeleton')
findWidget('Dialog-Data:gtk-ok').clicked()
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint active area status updated
checkpoint mesh bdy page updated
checkpoint Field page sensitized
checkpoint Materials page updated
findWidget('OOF2').resize(560, 350)
findWidget('OOF2:Fields & Equations Page:HPane').set_position(247)
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
checkpoint interface page updated
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint microstructure page sensitized
checkpoint meshable button set
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
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint meshable button set
checkpoint meshable button set
checkpoint meshable button set
checkpoint meshable button set
checkpoint meshable button set
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint mesh bdy page updated
checkpoint Field page sensitized
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
findWidget('OOF2').resize(625, 350)
findWidget('OOF2:Fields & Equations Page:HPane').set_position(277)
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
checkpoint OOF.File.Load.Data
assert tests.sensitization0()

# Create a mesh and check field page sensitization

findWidget('OOF2:Navigation:Prev').clicked()
findWidget('OOF2').resize(625, 369)
findWidget('OOF2:FE Mesh Page:Pane').set_position(331)
findWidget('OOF2:FE Mesh Page:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new mesh
findWidget('Dialog-Create a new mesh').resize(337, 204)
findWidget('Dialog-Create a new mesh:gtk-ok').clicked()
checkpoint mesh bdy page updated
checkpoint mesh bdy page updated
checkpoint Field page sensitized
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
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Mesh.New
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2').resize(715, 369)
findWidget('OOF2:Fields & Equations Page:HPane').set_position(317)
assert tests.sensitization1()
findWidget('OOF2:Fields & Equations Page:HPane:Fields:Temperature defined').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint OOF.Subproblem.Field.Define
assert tests.sensitization2()
findWidget('OOF2:Fields & Equations Page:HPane:Fields:Displacement defined').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint OOF.Subproblem.Field.Define
assert tests.sensitization3()
findWidget('OOF2:Fields & Equations Page:HPane:Fields:Temperature defined').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint OOF.Subproblem.Field.Undefine
assert tests.sensitization4()
findWidget('OOF2:Fields & Equations Page:HPane:Fields:Displacement defined').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint OOF.Subproblem.Field.Undefine
assert tests.sensitization1()
findWidget('OOF2:Fields & Equations Page:HPane:Fields:Temperature defined').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint OOF.Subproblem.Field.Define
assert tests.sensitization2()

# Create a new subproblem, switch between subproblems, and copy field
# and equation state between subproblems.

findWidget('OOF2:Navigation:Prev').clicked()
findWidget('OOF2:FE Mesh Page:Pane').set_position(421)
findWidget('OOF2:FE Mesh Page:Pane:Subproblems:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new subproblem
findWidget('Dialog-Create a new subproblem').resize(291, 100)
findWidget('Dialog-Create a new subproblem:gtk-ok').clicked()
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Subproblem.New
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2').resize(739, 369)
findWidget('OOF2:Fields & Equations Page:HPane').set_position(328)
assert tests.fieldButtonCheck(1, 0, 0)
assert tests.sensitization2()
setComboBox(findWidget('OOF2:Fields & Equations Page:SubProblem'), 'subproblem')
checkpoint Field page sensitized
assert tests.sensitization1()
assert tests.fieldButtonCheck(0, 0, 0)
setComboBox(findWidget('OOF2:Fields & Equations Page:SubProblem'), 'default')
checkpoint Field page sensitized
assert tests.sensitization2()
assert tests.fieldButtonCheck(1, 0, 0)
findWidget('OOF2:Fields & Equations Page:HPane:CopyField').clicked()
checkpoint toplevel widget mapped Dialog-Select a target Subproblem
findWidget('Dialog-Select a target Subproblem').resize(231, 156)
setComboBox(findWidget('Dialog-Select a target Subproblem:target:SubProblem'), 'subproblem')
findWidget('Dialog-Select a target Subproblem:gtk-ok').clicked()
checkpoint OOF.Subproblem.Copy_Field_State
assert tests.sensitization2()
assert tests.fieldButtonCheck(1, 0, 0)
setComboBox(findWidget('OOF2:Fields & Equations Page:SubProblem'), 'subproblem')
checkpoint Field page sensitized
assert tests.sensitization2()
assert tests.fieldButtonCheck(1, 0, 0)
assert tests.eqnButtonCheck(0)
findWidget('OOF2:Fields & Equations Page:HPane:Equations:Heat_Eqn active').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Subproblem.Equation.Activate
assert tests.eqnButtonCheck(1)
setComboBox(findWidget('OOF2:Fields & Equations Page:SubProblem'), 'default')
checkpoint Field page sensitized
assert tests.eqnButtonCheck(0)
setComboBox(findWidget('OOF2:Fields & Equations Page:SubProblem'), 'subproblem')
checkpoint Field page sensitized
assert tests.eqnButtonCheck(1)
findWidget('OOF2:Fields & Equations Page:HPane:CopyEquation').clicked()
checkpoint toplevel widget mapped Dialog-Select a target subproblem
findWidget('Dialog-Select a target subproblem').resize(231, 156)
setComboBox(findWidget('Dialog-Select a target subproblem:target:SubProblem'), 'default')
findWidget('Dialog-Select a target subproblem:gtk-ok').clicked()
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Subproblem.Copy_Equation_State
assert tests.eqnButtonCheck(1)
setComboBox(findWidget('OOF2:Fields & Equations Page:SubProblem'), 'default')
checkpoint Field page sensitized
assert tests.eqnButtonCheck(1)

# Create a new Mesh, and switch back and forth between meshes checking
# that the page updates properly.
findWidget('OOF2:Navigation:Prev').clicked()
findWidget('OOF2:FE Mesh Page:Pane').set_position(445)
findWidget('OOF2:FE Mesh Page:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new mesh
findWidget('Dialog-Create a new mesh').resize(337, 204)
findWidget('Dialog-Create a new mesh:gtk-ok').clicked()
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
checkpoint OOF.Mesh.New
findWidget('OOF2:Navigation:Next').clicked()
findWidget('OOF2').resize(763, 369)
findWidget('OOF2:Fields & Equations Page:HPane').set_position(339)
assert tests.sensitization2()
assert tests.fieldButtonCheck(1, 0, 0)
assert tests.eqnButtonCheck(1)
setComboBox(findWidget('OOF2:Fields & Equations Page:Mesh'), 'mesh<2>')
checkpoint Field page sensitized
assert tests.sensitization1()
assert tests.fieldButtonCheck(0, 0, 0)
assert tests.eqnButtonCheck(0)
setComboBox(findWidget('OOF2:Fields & Equations Page:Mesh'), 'mesh')
checkpoint Field page sensitized
assert tests.sensitization2()
assert tests.fieldButtonCheck(1, 0, 0)
assert tests.eqnButtonCheck(1)
findWidget('OOF2:Fields & Equations Page:HPane:CopyField').clicked()
checkpoint toplevel widget mapped Dialog-Select a target Subproblem
findWidget('Dialog-Select a target Subproblem').resize(231, 156)
setComboBox(findWidget('Dialog-Select a target Subproblem:target:Mesh'), 'mesh<2>')
findWidget('Dialog-Select a target Subproblem:gtk-ok').clicked()
checkpoint OOF.Subproblem.Copy_Field_State
assert tests.sensitization2()
assert tests.fieldButtonCheck(1, 0, 0)
assert tests.eqnButtonCheck(1)
setComboBox(findWidget('OOF2:Fields & Equations Page:Mesh'), 'mesh<2>')
checkpoint Field page sensitized
assert tests.sensitization2()
assert tests.fieldButtonCheck(1, 0, 0)
assert tests.eqnButtonCheck(0)
setComboBox(findWidget('OOF2:Fields & Equations Page:Mesh'), 'mesh')
checkpoint Field page sensitized
assert tests.sensitization2()
assert tests.fieldButtonCheck(1, 0, 0)
assert tests.eqnButtonCheck(1)
findWidget('OOF2:Fields & Equations Page:HPane:CopyEquation').clicked()
checkpoint toplevel widget mapped Dialog-Select a target subproblem
findWidget('Dialog-Select a target subproblem').resize(231, 156)
setComboBox(findWidget('Dialog-Select a target subproblem:target:Mesh'), 'mesh<2>')
findWidget('Dialog-Select a target subproblem:gtk-ok').clicked()
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Subproblem.Copy_Equation_State
assert tests.sensitization2()
assert tests.fieldButtonCheck(1, 0, 0)
assert tests.eqnButtonCheck(1)
setComboBox(findWidget('OOF2:Fields & Equations Page:Mesh'), 'mesh<2>')
checkpoint Field page sensitized
assert tests.sensitization2()
assert tests.fieldButtonCheck(1, 0, 0)
assert tests.eqnButtonCheck(1)
findWidget('OOF2:Navigation:Prev').clicked()
findWidget('OOF2:FE Mesh Page:Pane').set_position(469)
findWidget('OOF2:FE Mesh Page:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(344, 92)
findWidget('Questioner:gtk-yes').clicked()
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh bdy page updated
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Mesh.Delete
findWidget('OOF2:Navigation:Next').clicked()
assert tests.sensitization2()
assert tests.fieldButtonCheck(1, 0, 0)
assert tests.eqnButtonCheck(1)
setComboBox(findWidget('OOF2:Fields & Equations Page:SubProblem'), 'subproblem')
checkpoint Field page sensitized
findWidget('OOF2:Navigation:Prev').clicked()
findWidget('OOF2:FE Mesh Page:Pane:Subproblems:subprobChooserScroll:subprobChooser').get_selection().select_path((1,))
checkpoint mesh page subproblems sensitized
findWidget('OOF2:FE Mesh Page:Pane:Subproblems:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(388, 92)
findWidget('Questioner:gtk-yes').clicked()
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Subproblem.Delete
findWidget('OOF2:Navigation:Next').clicked()
assert tests.sensitization2()
assert tests.fieldButtonCheck(1, 0, 0)
assert tests.eqnButtonCheck(1)
findWidget('OOF2:Navigation:Prev').clicked()
findWidget('OOF2:FE Mesh Page:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(316, 92)
findWidget('Questioner:gtk-yes').clicked()
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh bdy page updated
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint Field page sensitized
checkpoint OOF.Mesh.Delete
findWidget('OOF2:Navigation:Next').clicked()
assert tests.sensitization0()
findMenu(findWidget('OOF2:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(190, 96)
findWidget('Dialog-Python_Log:filename').set_text('f')
findWidget('Dialog-Python_Log:filename').set_text('fi')
findWidget('Dialog-Python_Log:filename').set_text('fie')
findWidget('Dialog-Python_Log:filename').set_text('fiel')
findWidget('Dialog-Python_Log:filename').set_text('field')
findWidget('Dialog-Python_Log:filename').set_text('fielde')
findWidget('Dialog-Python_Log:filename').set_text('fieldeq')
findWidget('Dialog-Python_Log:filename').set_text('fieldeqn')
findWidget('Dialog-Python_Log:filename').set_text('fieldeqn.')
findWidget('Dialog-Python_Log:filename').set_text('fieldeqn.l')
findWidget('Dialog-Python_Log:filename').set_text('fieldeqn.lo')
findWidget('Dialog-Python_Log:filename').set_text('fieldeqn.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('fieldeqn.log')
findMenu(findWidget('OOF2:MenuBar'), 'File:Quit').activate()
