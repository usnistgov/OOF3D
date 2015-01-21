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

#Testing FE Mesh subproblem consistency based on dependencies

findWidget('OOF3D').resize(550, 350)
findMenu(findWidget('OOF3D:MenuBar'), 'File:Load:Data').activate()
checkpoint toplevel widget mapped Dialog-Data
findWidget('Dialog-Data').resize(190, 65)
findWidget('Dialog-Data:filename').set_text('TEST_DATA/triangle.skeleton')
findWidget('Dialog-Data:gtk-ok').clicked()
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint active area status updated
checkpoint named analysis chooser set
checkpoint pixel page updated
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
findWidget('OOF3D').resize(550, 350)
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
findWidget('OOF3D').resize(553, 358)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(307)
findWidget('OOF3D').resize(554, 361)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(308)
findWidget('OOF3D').resize(560, 365)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(314)
findWidget('OOF3D').resize(565, 371)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(319)
findWidget('OOF3D').resize(579, 384)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(333)
findWidget('OOF3D').resize(596, 400)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(350)
findWidget('OOF3D').resize(613, 412)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(367)
findWidget('OOF3D').resize(631, 425)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(385)
findWidget('OOF3D').resize(644, 437)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(398)
findWidget('OOF3D').resize(652, 443)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(406)
findWidget('OOF3D').resize(660, 448)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(414)
findWidget('OOF3D').resize(674, 455)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(428)
findWidget('OOF3D').resize(682, 459)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(436)
findWidget('OOF3D').resize(691, 462)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(445)
findWidget('OOF3D').resize(705, 471)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(459)
findWidget('OOF3D').resize(714, 478)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(468)
findWidget('OOF3D').resize(730, 488)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(484)
findWidget('OOF3D').resize(741, 495)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(495)
findWidget('OOF3D').resize(749, 498)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(503)
findWidget('OOF3D').resize(761, 503)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(515)
findWidget('OOF3D').resize(768, 505)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(522)
findWidget('OOF3D').resize(775, 509)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(529)
findWidget('OOF3D').resize(778, 511)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(532)
findWidget('OOF3D').resize(782, 512)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(536)
findWidget('OOF3D').resize(783, 512)
findWidget('OOF3D:FE Mesh Page:Pane').set_position(537)
findWidget('OOF3D').resize(783, 512)
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
findWidget('OOF3D Messages 1').resize(543, 200)
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.New
assert tests.subproblemsCheck(['default','subproblem','subproblem<2>'])
assert tests.subproblemsConsistencies([True, True, True])
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:SubproblemScroll:SubproblemList').get_selection().select_path((1,))
checkpoint mesh page subproblems sensitized
assert tests.subproblemsCheck(['default','subproblem','subproblem<2>'])
assert tests.subproblemsSelectedCheck('subproblem')
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
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:New').clicked()
checkpoint toplevel widget mapped Dialog-Create a new subproblem
findWidget('Dialog-Create a new subproblem').resize(389, 121)
findWidget('Dialog-Create a new subproblem:gtk-ok').clicked()
checkpoint mesh page subproblems sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.New
assert tests.subproblemsCheck(['default','subproblem<2>','subproblem','subproblem<3>'])
assert tests.subproblemsConsistencies([True, False, False, False])
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:SubproblemScroll:SubproblemList').get_selection().select_path((2,))
checkpoint mesh page subproblems sensitized
assert tests.subproblemsCheck(['default','subproblem<2>','subproblem','subproblem<3>'])
assert tests.subproblemsSelectedCheck('subproblem')
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
findWidget('OOF3D:FE Mesh Page:Pane:Subproblems:SubproblemScroll:SubproblemList').get_selection().select_path((3,))
checkpoint mesh page subproblems sensitized
assert tests.subproblemsCheck(['default','subproblem<2>','subproblem<3>','subproblem'])
assert tests.subproblemsSelectedCheck('subproblem')
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
assert tests.subproblemsConsistencies([True])
findMenu(findWidget('OOF3D:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(190, 92)
findWidget('Dialog-Python_Log:filename').set_text('meshpage.log')
findWidget('Dialog-Python_Log').resize(198, 92)
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('meshpage.log')
widget_1=findWidget('OOF3D')
handled_1=widget_1.event(event(gtk.gdk.DELETE,window=widget_1.window))
