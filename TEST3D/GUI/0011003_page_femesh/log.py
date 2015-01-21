# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.2 $
# $Author: langer $
# $Date: 2014/09/27 22:34:57 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

import tests

#Testing FE Mesh page dependencies with the Field&Equations Page and the Solver Page. 
#Testing also the impact of the subproblem consistency and the fact that it is shown in the other pages.

findWidget('OOF3D').resize(550, 350)
findMenu(findWidget('OOF3D:MenuBar'), 'File:Load:Data').activate()
checkpoint toplevel widget mapped Dialog-Data
findWidget('Dialog-Data').resize(190, 65)
findWidget('Dialog-Data:filename').set_text('TEST_DATA/triangle.skeleton')
findWidget('Dialog-Data:gtk-ok').clicked()
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint pixel page updated
checkpoint active area status updated
checkpoint named analysis chooser set
checkpoint microstructure page sensitized
checkpoint Field page sensitized
checkpoint meshable button set
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
checkpoint toplevel widget mapped OOF3D Activity Viewer
findWidget('OOF3D Activity Viewer').resize(400, 300)
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
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page selection sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page updated
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
checkpoint pinnodes page sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
checkpoint skeleton selection page groups sensitized
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
widget_0=findWidget('OOF3D Activity Viewer')
handled_0=widget_0.event(event(gtk.gdk.DELETE,window=widget_0.window))
postpone if not handled_0: widget_0.destroy()
checkpoint OOF.ActivityViewer.File.Close
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'FE Mesh')
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint page installed FE Mesh
assert tests.FEMeshPageInfoCheck()
assert tests.FEMeshPageCheck1()
assert tests.FEMeshPageSubproblemsCheck0()
assert tests.FEMeshPageOperationsCheck0()
assert tests.chooserCheck('OOF3D:FE Mesh Page:Microstructure', ['triangle'])
assert tests.chooserStateCheck('OOF3D:FE Mesh Page:Microstructure', 'triangle')
assert tests.chooserCheck('OOF3D:FE Mesh Page:Skeleton', ['skeleton'])
assert tests.chooserStateCheck('OOF3D:FE Mesh Page:Skeleton', 'skeleton')
findWidget('OOF3D:FE Mesh Page:Pane').set_position(304)
findWidget('OOF3D').resize(559, 364)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(313)
findWidget('OOF3D').resize(566, 371)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(320)
findWidget('OOF3D').resize(580, 383)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(334)
findWidget('OOF3D').resize(600, 400)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(354)
findWidget('OOF3D').resize(611, 409)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(365)
findWidget('OOF3D').resize(623, 417)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(377)
findWidget('OOF3D').resize(635, 426)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(389)
findWidget('OOF3D').resize(650, 441)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(404)
findWidget('OOF3D').resize(664, 457)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(418)
findWidget('OOF3D').resize(688, 478)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(442)
findWidget('OOF3D').resize(701, 488)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(455)
findWidget('OOF3D').resize(718, 501)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(472)
findWidget('OOF3D').resize(727, 511)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(481)
findWidget('OOF3D').resize(734, 516)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(488)
findWidget('OOF3D').resize(740, 521)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(494)
findWidget('OOF3D').resize(747, 522)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(501)
findWidget('OOF3D').resize(752, 524)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(506)
findWidget('OOF3D').resize(756, 526)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(510)
findWidget('OOF3D').resize(761, 527)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(515)
findWidget('OOF3D').resize(764, 527)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(518)
findWidget('OOF3D').resize(766, 527)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(520)
findWidget('OOF3D').resize(767, 527)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(521)
findWidget('OOF3D').resize(770, 529)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(524)
findWidget('OOF3D').resize(773, 530)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(527)
findWidget('OOF3D').resize(778, 530)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(532)
findWidget('OOF3D').resize(779, 531)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(533)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Fields & Equations')
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint page installed Fields & Equations
assert tests.chooserCheck('OOF3D:Fields & Equations Page:Microstructure', ['triangle'])
assert tests.chooserStateCheck('OOF3D:Fields & Equations Page:Microstructure', 'triangle')
assert tests.chooserCheck('OOF3D:Fields & Equations Page:Skeleton', ['skeleton'])
assert tests.chooserStateCheck('OOF3D:Fields & Equations Page:Skeleton', 'skeleton')
assert tests.sensitizationCheck({"Mesh" : 0,"SubProblem" : 0},base="OOF3D:Fields & Equations Page")
findWidget('OOF3D:Fields & Equations Page:HPane').set_position(348)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Solver')
checkpoint Solver page sensitized
checkpoint page installed Solver
assert tests.chooserCheck('OOF3D:Solver Page:Microstructure', ['triangle'])
assert tests.chooserStateCheck('OOF3D:Solver Page:Microstructure', 'triangle')
assert tests.chooserCheck('OOF3D:Solver Page:Skeleton', ['skeleton'])
assert tests.chooserStateCheck('OOF3D:Solver Page:Skeleton', 'skeleton')
assert tests.sensitizationCheck({"Mesh" : 0},base="OOF3D:Solver Page")
findWidget('OOF3D:Solver Page:VPane').set_position(185)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'FE Mesh')
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint page installed FE Mesh
assert tests.FEMeshPageInfoCheck()
assert tests.FEMeshPageCheck1()
assert tests.FEMeshPageSubproblemsCheck0()
assert tests.FEMeshPageOperationsCheck0()
assert tests.chooserCheck('OOF3D:FE Mesh Page:Microstructure', ['triangle'])
assert tests.chooserStateCheck('OOF3D:FE Mesh Page:Microstructure', 'triangle')
assert tests.chooserCheck('OOF3D:FE Mesh Page:Skeleton', ['skeleton'])
assert tests.chooserStateCheck('OOF3D:FE Mesh Page:Skeleton', 'skeleton')
findWidget('OOF3D:FE Mesh Page:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new mesh
findWidget('Dialog-Create a new mesh').resize(373, 229)
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
assert tests.FEMeshPageCheck2()
assert tests.FEMeshPageSubproblemsCheck1()
assert tests.FEMeshPageOperationsCheck1()
assert tests.chooserCheck('OOF3D:FE Mesh Page:Mesh', ['mesh'])
assert tests.chooserStateCheck('OOF3D:FE Mesh Page:Mesh', 'mesh')
assert tests.subproblemsCheck(['default'])
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Fields & Equations')
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint page installed Fields & Equations
assert tests.chooserCheck('OOF3D:Fields & Equations Page:Microstructure', ['triangle'])
assert tests.chooserStateCheck('OOF3D:Fields & Equations Page:Microstructure', 'triangle')
assert tests.chooserCheck('OOF3D:Fields & Equations Page:Skeleton', ['skeleton'])
assert tests.chooserStateCheck('OOF3D:Fields & Equations Page:Skeleton', 'skeleton')
assert tests.chooserCheck('OOF3D:Fields & Equations Page:Mesh', ['mesh'])
assert tests.chooserStateCheck('OOF3D:Fields & Equations Page:Mesh', 'mesh')
assert tests.chooserCheck('OOF3D:Fields & Equations Page:SubProblem', ['default'])
assert tests.chooserStateCheck('OOF3D:Fields & Equations Page:SubProblem', 'default')
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Solver')
checkpoint Solver page sensitized
checkpoint page installed Solver
assert tests.chooserCheck('OOF3D:Solver Page:Microstructure', ['triangle'])
assert tests.chooserStateCheck('OOF3D:Solver Page:Microstructure', 'triangle')
assert tests.chooserCheck('OOF3D:Solver Page:Skeleton', ['skeleton'])
assert tests.chooserStateCheck('OOF3D:Solver Page:Skeleton', 'skeleton')
assert tests.chooserCheck('OOF3D:Solver Page:Mesh', ['mesh'])
assert tests.chooserStateCheck('OOF3D:Solver Page:Mesh', 'mesh')
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'FE Mesh')
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint page installed FE Mesh
assert tests.FEMeshPageCheck2()
assert tests.FEMeshPageSubproblemsCheck1()
assert tests.FEMeshPageOperationsCheck1()
assert tests.chooserCheck('OOF3D:FE Mesh Page:Mesh', ['mesh'])
assert tests.chooserStateCheck('OOF3D:FE Mesh Page:Mesh', 'mesh')
assert tests.subproblemsCheck(['default'])
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new subproblem
findWidget('Dialog-Create a new subproblem').resize(286, 94)
findWidget('Dialog-Create a new subproblem:gtk-ok').clicked()
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.New
assert tests.subproblemsCheck(['default','subproblem'])
assert tests.subproblemsConsistencies([True, True])
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new subproblem
findWidget('Dialog-Create a new subproblem').resize(286, 94)
setComboBox(findWidget('Dialog-Create a new subproblem:subproblem:Chooser'), 'Complement')
findWidget('Dialog-Create a new subproblem').resize(365, 121)
setComboBox(findWidget('Dialog-Create a new subproblem:subproblem:Complement:complement_of'), 'subproblem')
findWidget('Dialog-Create a new subproblem:gtk-ok').clicked()
checkpoint mesh page subproblems sensitized
findWidget('OOF3D Messages 1').resize(543, 200)
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.New
assert tests.subproblemsCheck(['default','subproblem','subproblem<2>'])
assert tests.subproblemsConsistencies([True, True, True])
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Fields & Equations')
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint page installed Fields & Equations
assert tests.chooserCheck('OOF3D:Fields & Equations Page:Microstructure', ['triangle'])
assert tests.chooserStateCheck('OOF3D:Fields & Equations Page:Microstructure', 'triangle')
assert tests.chooserCheck('OOF3D:Fields & Equations Page:Skeleton', ['skeleton'])
assert tests.chooserStateCheck('OOF3D:Fields & Equations Page:Skeleton', 'skeleton')
assert tests.chooserCheck('OOF3D:Fields & Equations Page:Mesh', ['mesh'])
assert tests.chooserStateCheck('OOF3D:Fields & Equations Page:Mesh', 'mesh')
assert tests.chooserCheck('OOF3D:Fields & Equations Page:SubProblem', ['default','subproblem','subproblem<2>'])
assert tests.chooserStateCheck('OOF3D:Fields & Equations Page:SubProblem', 'default')
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Solver')
checkpoint Solver page sensitized
checkpoint page installed Solver
assert tests.chooserCheck('OOF3D:Solver Page:Microstructure', ['triangle'])
assert tests.chooserStateCheck('OOF3D:Solver Page:Microstructure', 'triangle')
assert tests.chooserCheck('OOF3D:Solver Page:Skeleton', ['skeleton'])
assert tests.chooserStateCheck('OOF3D:Solver Page:Skeleton', 'skeleton')
assert tests.chooserCheck('OOF3D:Solver Page:Mesh', ['mesh'])
assert tests.chooserStateCheck('OOF3D:Solver Page:Mesh', 'mesh')
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'FE Mesh')
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint page installed FE Mesh
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:SubproblemScroll:SubproblemList').get_selection().select_path((1,))
checkpoint mesh page subproblems sensitized
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:Edit').clicked()
checkpoint toplevel widget mapped Dialog-Edit Subproblem definition
findWidget('Dialog-Edit Subproblem definition').resize(244, 73)
setComboBox(findWidget('Dialog-Edit Subproblem definition:subproblem:Chooser'), 'Complement')
findWidget('Dialog-Edit Subproblem definition').resize(389, 100)
setComboBox(findWidget('Dialog-Edit Subproblem definition:subproblem:Complement:complement_of'), 'subproblem<2>')
findWidget('Dialog-Edit Subproblem definition:gtk-ok').clicked()
findWidget('OOF3D Messages 1').resize(573, 200)
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Edit
assert tests.subproblemsCheck(['default','subproblem<2>','subproblem'])
assert tests.subproblemsConsistencies([True, False, False])
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Fields & Equations')
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint page installed Fields & Equations
assert tests.chooserCheck('OOF3D:Fields & Equations Page:Microstructure', ['triangle'])
assert tests.chooserStateCheck('OOF3D:Fields & Equations Page:Microstructure', 'triangle')
assert tests.chooserCheck('OOF3D:Fields & Equations Page:Skeleton', ['skeleton'])
assert tests.chooserStateCheck('OOF3D:Fields & Equations Page:Skeleton', 'skeleton')
assert tests.chooserCheck('OOF3D:Fields & Equations Page:Mesh', ['mesh'])
assert tests.chooserStateCheck('OOF3D:Fields & Equations Page:Mesh', 'mesh')
assert tests.chooserCheck('OOF3D:Fields & Equations Page:SubProblem', ['default'])
assert tests.chooserStateCheck('OOF3D:Fields & Equations Page:SubProblem', 'default')
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Solver')
checkpoint Solver page sensitized
checkpoint page installed Solver
assert tests.chooserCheck('OOF3D:Solver Page:Microstructure', ['triangle'])
assert tests.chooserStateCheck('OOF3D:Solver Page:Microstructure', 'triangle')
assert tests.chooserCheck('OOF3D:Solver Page:Skeleton', ['skeleton'])
assert tests.chooserStateCheck('OOF3D:Solver Page:Skeleton', 'skeleton')
assert tests.chooserCheck('OOF3D:Solver Page:Mesh', ['mesh'])
assert tests.chooserStateCheck('OOF3D:Solver Page:Mesh', 'mesh')
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'FE Mesh')
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint page installed FE Mesh
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new subproblem
findWidget('Dialog-Create a new subproblem').resize(389, 121)
setComboBox(findWidget('Dialog-Create a new subproblem:subproblem:Chooser'), 'EntireMesh')
findWidget('Dialog-Create a new subproblem:gtk-ok').clicked()
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.New
assert tests.subproblemsCheck(['default','subproblem<2>','subproblem','subproblem<3>'])
assert tests.subproblemsConsistencies([True, False, False, True])
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Fields & Equations')
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint page installed Fields & Equations
assert tests.chooserCheck('OOF3D:Fields & Equations Page:Microstructure', ['triangle'])
assert tests.chooserStateCheck('OOF3D:Fields & Equations Page:Microstructure', 'triangle')
assert tests.chooserCheck('OOF3D:Fields & Equations Page:Skeleton', ['skeleton'])
assert tests.chooserStateCheck('OOF3D:Fields & Equations Page:Skeleton', 'skeleton')
assert tests.chooserCheck('OOF3D:Fields & Equations Page:Mesh', ['mesh'])
assert tests.chooserStateCheck('OOF3D:Fields & Equations Page:Mesh', 'mesh')
assert tests.chooserCheck('OOF3D:Fields & Equations Page:SubProblem', ['default','subproblem<3>'])
assert tests.chooserStateCheck('OOF3D:Fields & Equations Page:SubProblem', 'default')
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Solver')
checkpoint Solver page sensitized
checkpoint page installed Solver
assert tests.chooserCheck('OOF3D:Solver Page:Microstructure', ['triangle'])
assert tests.chooserStateCheck('OOF3D:Solver Page:Microstructure', 'triangle')
assert tests.chooserCheck('OOF3D:Solver Page:Skeleton', ['skeleton'])
assert tests.chooserStateCheck('OOF3D:Solver Page:Skeleton', 'skeleton')
assert tests.chooserCheck('OOF3D:Solver Page:Mesh', ['mesh'])
assert tests.chooserStateCheck('OOF3D:Solver Page:Mesh', 'mesh')
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'FE Mesh')
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint page installed FE Mesh
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:SubproblemScroll:SubproblemList').get_selection().select_path((3,))
checkpoint mesh page subproblems sensitized
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:Edit').clicked()
checkpoint toplevel widget mapped Dialog-Edit Subproblem definition
findWidget('Dialog-Edit Subproblem definition').resize(244, 73)
setComboBox(findWidget('Dialog-Edit Subproblem definition:subproblem:Chooser'), 'Complement')
findWidget('Dialog-Edit Subproblem definition').resize(389, 100)
findWidget('Dialog-Edit Subproblem definition:gtk-ok').clicked()
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Edit
assert tests.subproblemsCheck(['default','subproblem<2>','subproblem','subproblem<3>'])
assert tests.subproblemsConsistencies([True, False, False, False])
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Fields & Equations')
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint page installed Fields & Equations
assert tests.chooserCheck('OOF3D:Fields & Equations Page:Microstructure', ['triangle'])
assert tests.chooserStateCheck('OOF3D:Fields & Equations Page:Microstructure', 'triangle')
assert tests.chooserCheck('OOF3D:Fields & Equations Page:Skeleton', ['skeleton'])
assert tests.chooserStateCheck('OOF3D:Fields & Equations Page:Skeleton', 'skeleton')
assert tests.chooserCheck('OOF3D:Fields & Equations Page:Mesh', ['mesh'])
assert tests.chooserStateCheck('OOF3D:Fields & Equations Page:Mesh', 'mesh')
assert tests.chooserCheck('OOF3D:Fields & Equations Page:SubProblem', ['default'])
assert tests.chooserStateCheck('OOF3D:Fields & Equations Page:SubProblem', 'default')
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Solver')
checkpoint Solver page sensitized
checkpoint page installed Solver
assert tests.chooserCheck('OOF3D:Solver Page:Microstructure', ['triangle'])
assert tests.chooserStateCheck('OOF3D:Solver Page:Microstructure', 'triangle')
assert tests.chooserCheck('OOF3D:Solver Page:Skeleton', ['skeleton'])
assert tests.chooserStateCheck('OOF3D:Solver Page:Skeleton', 'skeleton')
assert tests.chooserCheck('OOF3D:Solver Page:Mesh', ['mesh'])
assert tests.chooserStateCheck('OOF3D:Solver Page:Mesh', 'mesh')
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'FE Mesh')
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint page installed FE Mesh
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:SubproblemScroll:SubproblemList').get_selection().select_path((2,))
checkpoint mesh page subproblems sensitized
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:Edit').clicked()
checkpoint toplevel widget mapped Dialog-Edit Subproblem definition
findWidget('Dialog-Edit Subproblem definition').resize(389, 100)
setComboBox(findWidget('Dialog-Edit Subproblem definition:subproblem:Chooser'), 'EntireMesh')
findWidget('Dialog-Edit Subproblem definition:gtk-ok').clicked()
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint Solver page sensitized
checkpoint named analysis chooser set
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Edit
assert tests.subproblemsCheck(['default','subproblem<2>','subproblem<3>','subproblem'])
assert tests.subproblemsConsistencies([True, True, True, True])
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Fields & Equations')
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint page installed Fields & Equations
assert tests.chooserCheck('OOF3D:Fields & Equations Page:Microstructure', ['triangle'])
assert tests.chooserStateCheck('OOF3D:Fields & Equations Page:Microstructure', 'triangle')
assert tests.chooserCheck('OOF3D:Fields & Equations Page:Skeleton', ['skeleton'])
assert tests.chooserStateCheck('OOF3D:Fields & Equations Page:Skeleton', 'skeleton')
assert tests.chooserCheck('OOF3D:Fields & Equations Page:Mesh', ['mesh'])
assert tests.chooserStateCheck('OOF3D:Fields & Equations Page:Mesh', 'mesh')
assert tests.chooserCheck('OOF3D:Fields & Equations Page:SubProblem', ['default','subproblem<2>','subproblem<3>','subproblem'])
assert tests.chooserStateCheck('OOF3D:Fields & Equations Page:SubProblem', 'default')
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Solver')
checkpoint Solver page sensitized
checkpoint page installed Solver
assert tests.chooserCheck('OOF3D:Solver Page:Microstructure', ['triangle'])
assert tests.chooserStateCheck('OOF3D:Solver Page:Microstructure', 'triangle')
assert tests.chooserCheck('OOF3D:Solver Page:Skeleton', ['skeleton'])
assert tests.chooserStateCheck('OOF3D:Solver Page:Skeleton', 'skeleton')
assert tests.chooserCheck('OOF3D:Solver Page:Mesh', ['mesh'])
assert tests.chooserStateCheck('OOF3D:Solver Page:Mesh', 'mesh')
findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll').get_vadjustment().set_value( 1.4000000000000e+01)
findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll').get_vadjustment().set_value( 0.0000000000000e+00)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'FE Mesh')
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint page installed FE Mesh
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:SubproblemScroll:SubproblemList').get_selection().select_path((3,))
checkpoint mesh page subproblems sensitized
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:Delete').clicked()
checkpoint toplevel widget mapped Questioner
findWidget('Questioner').resize(354, 87)
findWidget('Questioner:gtk-yes').clicked()
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Delete
assert tests.subproblemsCheck(['default'])
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Fields & Equations')
checkpoint Field page sensitized
checkpoint Field page sensitized
checkpoint page installed Fields & Equations
assert tests.chooserCheck('OOF3D:Fields & Equations Page:Microstructure', ['triangle'])
assert tests.chooserStateCheck('OOF3D:Fields & Equations Page:Microstructure', 'triangle')
assert tests.chooserCheck('OOF3D:Fields & Equations Page:Skeleton', ['skeleton'])
assert tests.chooserStateCheck('OOF3D:Fields & Equations Page:Skeleton', 'skeleton')
assert tests.chooserCheck('OOF3D:Fields & Equations Page:Mesh', ['mesh'])
assert tests.chooserStateCheck('OOF3D:Fields & Equations Page:Mesh', 'mesh')
assert tests.chooserCheck('OOF3D:Fields & Equations Page:SubProblem', ['default'])
assert tests.chooserStateCheck('OOF3D:Fields & Equations Page:SubProblem', 'default')
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Solver')
checkpoint Solver page sensitized
checkpoint page installed Solver
assert tests.chooserCheck('OOF3D:Solver Page:Microstructure', ['triangle'])
assert tests.chooserStateCheck('OOF3D:Solver Page:Microstructure', 'triangle')
assert tests.chooserCheck('OOF3D:Solver Page:Skeleton', ['skeleton'])
assert tests.chooserStateCheck('OOF3D:Solver Page:Skeleton', 'skeleton')
assert tests.chooserCheck('OOF3D:Solver Page:Mesh', ['mesh'])
assert tests.chooserStateCheck('OOF3D:Solver Page:Mesh', 'mesh')
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'FE Mesh')
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
checkpoint page installed FE Mesh
findMenu(findWidget('OOF3D:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(190, 92)
findWidget('Dialog-Python_Log:filename').set_text('meshpage.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('meshpage.log')
widget_1=findWidget('OOF3D')
handled_1=widget_1.event(event(gtk.gdk.DELETE,window=widget_1.window))
