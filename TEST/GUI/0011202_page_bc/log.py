checkpoint toplevel widget mapped OOF2 Activity Viewer
# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:11:52 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov.

# Test to see if the correct target boundaries are listed when copying
# boundary conditions from one mesh to another.

import tests

setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Microstructure')
findWidget('OOF2:Microstructure Page:Pane').set_position(150)
findWidget('OOF2:Microstructure Page:New').clicked()
checkpoint toplevel widget mapped Dialog-Create Microstructure
findWidget('Dialog-Create Microstructure').resize(314, 168)
findWidget('Dialog-Create Microstructure:gtk-ok').clicked()
findWidget('OOF2:Microstructure Page:Pane').set_position(153)
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint meshable button set
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
checkpoint OOF.Microstructure.New
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton')
findWidget('OOF2').resize(593, 434)
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
checkpoint skeleton page sensitized
findWidget('OOF2:Skeleton Page:New').clicked()
checkpoint toplevel widget mapped Dialog-New skeleton
findWidget('Dialog-New skeleton').resize(334, 152)
findWidget('Dialog-New skeleton:gtk-ok').clicked()
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page updated
checkpoint skeleton selection page groups sensitized
checkpoint skeleton page sensitized
checkpoint mesh bdy page updated
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint boundary page updated
checkpoint skeleton page sensitized
checkpoint skeleton page sensitized
checkpoint skeleton selection page grouplist
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint OOF.Skeleton.New
findWidget('OOF2:Skeleton Page:Pane').set_position(249)
findWidget('OOF2:Skeleton Page:New').clicked()
checkpoint toplevel widget mapped Dialog-New skeleton
findWidget('Dialog-New skeleton').resize(334, 152)
findWidget('Dialog-New skeleton:gtk-ok').clicked()
findWidget('OOF2 Messages 1').resize(544, 200)
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
checkpoint mesh bdy page updated
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Skeleton.New
checkpoint skeleton page sensitized
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Skeleton Boundaries')
setComboBox(findWidget('OOF2:Skeleton Boundaries Page:Skeleton'), 'skeleton<2>')
checkpoint boundary page updated
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:BoundaryListScroll:BoundaryList').get_selection().select_path((0,))
checkpoint boundary page updated
checkpoint boundary page updated
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
findWidget('OOF2:Skeleton Boundaries Page:Pane:Boundaries:Delete').clicked()
findWidget('OOF2:Skeleton Boundaries Page:Pane').set_position(294)
checkpoint boundary page updated
checkpoint mesh bdy page updated
checkpoint boundary page updated
checkpoint OOF.Skeleton.Boundary.Delete
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'FE Mesh')
findWidget('OOF2').resize(593, 482)
findWidget('OOF2:FE Mesh Page:Pane').set_position(174)
setComboBox(findWidget('OOF2:FE Mesh Page:Skeleton'), 'skeleton<2>')
findWidget('OOF2:FE Mesh Page:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new mesh
findWidget('Dialog-Create a new mesh').resize(331, 188)
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
findWidget('OOF2:FE Mesh Page:Pane').set_position(174)
setComboBox(findWidget('OOF2:FE Mesh Page:Skeleton'), 'skeleton')
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
findWidget('OOF2:FE Mesh Page:Pane').set_position(174)
findWidget('OOF2:FE Mesh Page:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new mesh
findWidget('Dialog-Create a new mesh').resize(331, 188)
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
findWidget('OOF2:FE Mesh Page:Pane').set_position(174)
findWidget('OOF2:Navigation:Next').clicked()
setComboBox(findWidget('OOF2:Fields & Equations Page:Skeleton'), 'skeleton')
#findWidget('OOF2:Fields & Equations Page:HPane').set_position(153)
findWidget('OOF2:Fields & Equations Page:HPane:Fields:Temperature defined').clicked()
checkpoint OOF.Subproblem.Field.Define
findWidget('OOF2:Fields & Equations Page:HPane:Fields:Temperature active').clicked()
checkpoint OOF.Subproblem.Field.Activate
findWidget('OOF2:Fields & Equations Page:HPane:Equations:Heat_Eqn active').clicked()
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Subproblem.Equation.Activate
setComboBox(findWidget('OOF2:Fields & Equations Page:Skeleton'), 'skeleton<2>')
findWidget('OOF2:Fields & Equations Page:HPane:Fields:Temperature defined').clicked()
checkpoint OOF.Subproblem.Field.Define
findWidget('OOF2:Fields & Equations Page:HPane:Fields:Temperature active').clicked()
checkpoint OOF.Subproblem.Field.Activate
findWidget('OOF2:Fields & Equations Page:HPane:Equations:Heat_Eqn active').clicked()
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint OOF.Subproblem.Equation.Activate
setComboBox(findWidget('OOF2:Navigation:PageMenu'), 'Boundary Conditions')
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(290)
setComboBox(findWidget('OOF2:Boundary Conditions Page:Skeleton'), 'skeleton')
findWidget('OOF2:Boundary Conditions Page:Pane:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(399, 276)
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(290)
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
findWidget('OOF2 Messages 1').resize(742, 200)
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(290)
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF2:Boundary Conditions Page:Pane:Condition:Copy').clicked()
checkpoint toplevel widget mapped Dialog-Choose a name and boundary.
findWidget('Dialog-Choose a name and boundary.').resize(273, 188)
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(290)
assert tests.bdyNameCheck('top', 'bottom', 'right', 'left', None,                           'topleft', 'bottomleft', 'topright', 'bottomright')
setComboBox(findWidget('Dialog-Choose a name and boundary.:mesh:Skeleton'), 'skeleton<2>')
assert tests.bdyNameCheck('bottom', 'right', 'left', None,                           'topleft', 'bottomleft', 'topright', 'bottomright')
findWidget('Dialog-Choose a name and boundary.:gtk-cancel').clicked()
setComboBox(findWidget('OOF2:Boundary Conditions Page:Skeleton'), 'skeleton<2>')
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(290)
findWidget('OOF2:Boundary Conditions Page:Pane:Condition:New').clicked()
checkpoint toplevel widget mapped Dialog-New Boundary Condition
findWidget('Dialog-New Boundary Condition').resize(399, 276)
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(290)
findWidget('Dialog-New Boundary Condition:gtk-ok').clicked()
# New boundary condition created.
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(290)
checkpoint OOF.Mesh.Boundary_Conditions.New
findWidget('OOF2:Boundary Conditions Page:Pane:Condition:Copy').clicked()
checkpoint toplevel widget mapped Dialog-Choose a name and boundary.
findWidget('Dialog-Choose a name and boundary.').resize(273, 188)
findWidget('OOF2:Boundary Conditions Page:Pane').set_position(290)
assert tests.bdyNameCheck('top', 'bottom', 'right', 'left', None,                           'topleft', 'bottomleft', 'topright', 'bottomright')
setComboBox(findWidget('Dialog-Choose a name and boundary.:mesh:Skeleton'), 'skeleton<2>')
assert tests.bdyNameCheck('bottom', 'right', 'left', None,                           'topleft', 'bottomleft', 'topright', 'bottomright')
setComboBox(findWidget('Dialog-Choose a name and boundary.:mesh:Skeleton'), 'skeleton')
assert tests.bdyNameCheck('top', 'bottom', 'right', 'left', None,                           'topleft', 'bottomleft', 'topright', 'bottomright')
findWidget('Dialog-Choose a name and boundary.:gtk-cancel').clicked()
findMenu(findWidget('OOF2:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(194, 72)
findWidget('Dialog-Python_Log:filename').set_text('b')
findWidget('Dialog-Python_Log:filename').set_text('bd')
findWidget('Dialog-Python_Log:filename').set_text('bdy')
findWidget('Dialog-Python_Log:filename').set_text('bdyt')
findWidget('Dialog-Python_Log:filename').set_text('bdyte')
findWidget('Dialog-Python_Log:filename').set_text('bdytet')
findWidget('Dialog-Python_Log:filename').set_text('bdytets')
findWidget('Dialog-Python_Log:filename').set_text('bdytet')
findWidget('Dialog-Python_Log:filename').set_text('bdyte')
findWidget('Dialog-Python_Log:filename').set_text('bdytes')
findWidget('Dialog-Python_Log:filename').set_text('bdytest')
findWidget('Dialog-Python_Log:filename').set_text('bdytest.')
findWidget('Dialog-Python_Log:filename').set_text('bdytest.l')
findWidget('Dialog-Python_Log:filename').set_text('bdytest.lo')
findWidget('Dialog-Python_Log:filename').set_text('bdytest.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('bdytest.log')
findMenu(findWidget('OOF2:MenuBar'), 'File:Quit').activate()
