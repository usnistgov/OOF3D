# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.6 $
# $Author: fyc $
# $Date: 2014/06/19 15:33:58 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

import tests

#Testing Basic Solver Mode

findWidget('OOF3D').resize(550, 350)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Microstructure')
checkpoint page installed Microstructure
findWidget('OOF3D:Microstructure Page:Pane').set_position(225)
findWidget('OOF3D:Microstructure Page:Pane').set_position(156)
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint microstructure page sensitized
findMenu(findWidget('OOF3D:MenuBar'), 'File:Load:Data').activate()
checkpoint toplevel widget mapped Dialog-Data
findWidget('Dialog-Data').resize(190, 67)
findWidget('Dialog-Data:filename').set_text('TEST_DATA/two_walls.mesh')
findWidget('Dialog-Data:gtk-ok').clicked()
findWidget('OOF3D:Microstructure Page:Pane').set_position(159)
checkpoint meshable button set
checkpoint meshable button set
checkpoint microstructure page sensitized
checkpoint named analysis chooser set
checkpoint named analysis chooser set
checkpoint pixel page updated
checkpoint active area status updated
checkpoint microstructure page sensitized
checkpoint meshable button set
checkpoint Field page sensitized
checkpoint Materials page updated
checkpoint mesh page subproblems sensitized
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
findWidget('OOF3D:Microstructure Page:Pane').set_position(225)
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
checkpoint Field page sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page subproblems sensitized
checkpoint mesh page sensitized
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
checkpoint toplevel widget mapped OOF3D Activity Viewer
checkpoint boundary page updated
findWidget('OOF3D Activity Viewer').resize(400, 300)
checkpoint boundary page updated
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
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Solver')
checkpoint Solver page sensitized
checkpoint page installed Solver
assert tests.solverSubproblemsPageSensitivityCheck0()
assert tests.solverFieldsPageSensitivityCheck0()
findWidget('OOF3D').resize(552, 427)
findWidget('OOF3D:Solver Page:VPane').set_position(130)
findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList').get_selection().select_path((0,))
findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll').get_vadjustment().set_value( 3.0000000000000e+00)
findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll').get_vadjustment().set_value( 0.0000000000000e+00)
findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll').get_vadjustment().set_value( 3.0000000000000e+00)
findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll').get_vadjustment().set_value( 0.0000000000000e+00)
tree=findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList')
column = tree.get_column(2)
tree.row_activated((0,), column)
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(475, 179)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
assert tests.solverSubproblemsPageSensitivityCheck2()
assert tests.solverFieldsPageSensitivityCheck0()
findWidget('OOF3D').resize(554, 428)
findWidget('OOF3D:Solver Page:VPane').set_position(131)
findWidget('OOF3D').resize(556, 430)
findWidget('OOF3D:Solver Page:VPane').set_position(132)
findWidget('OOF3D').resize(569, 439)
findWidget('OOF3D:Solver Page:VPane').set_position(136)
findWidget('OOF3D').resize(584, 450)
findWidget('OOF3D:Solver Page:VPane').set_position(142)
findWidget('OOF3D').resize(592, 456)
findWidget('OOF3D:Solver Page:VPane').set_position(145)
findWidget('OOF3D').resize(612, 468)
findWidget('OOF3D:Solver Page:VPane').set_position(151)
findWidget('OOF3D').resize(623, 474)
findWidget('OOF3D:Solver Page:VPane').set_position(154)
findWidget('OOF3D').resize(647, 483)
findWidget('OOF3D:Solver Page:VPane').set_position(158)
findWidget('OOF3D').resize(661, 489)
findWidget('OOF3D:Solver Page:VPane').set_position(161)
findWidget('OOF3D').resize(696, 499)
findWidget('OOF3D:Solver Page:VPane').set_position(166)
findWidget('OOF3D').resize(713, 505)
findWidget('OOF3D:Solver Page:VPane').set_position(169)
findWidget('OOF3D').resize(746, 512)
findWidget('OOF3D:Solver Page:VPane').set_position(173)
findWidget('OOF3D').resize(764, 515)
findWidget('OOF3D:Solver Page:VPane').set_position(174)
findWidget('OOF3D').resize(799, 529)
findWidget('OOF3D:Solver Page:VPane').set_position(181)
findWidget('OOF3D').resize(818, 536)
findWidget('OOF3D:Solver Page:VPane').set_position(185)
findWidget('OOF3D').resize(850, 550)
findWidget('OOF3D:Solver Page:VPane').set_position(192)
findWidget('OOF3D').resize(878, 564)
findWidget('OOF3D:Solver Page:VPane').set_position(199)
findWidget('OOF3D').resize(892, 571)
findWidget('OOF3D:Solver Page:VPane').set_position(203)
findWidget('OOF3D').resize(918, 587)
findWidget('OOF3D:Solver Page:VPane').set_position(211)
findWidget('OOF3D').resize(931, 596)
findWidget('OOF3D:Solver Page:VPane').set_position(215)
findWidget('OOF3D').resize(955, 610)
findWidget('OOF3D:Solver Page:VPane').set_position(222)
findWidget('OOF3D').resize(965, 617)
findWidget('OOF3D:Solver Page:VPane').set_position(226)
findWidget('OOF3D').resize(985, 629)
findWidget('OOF3D:Solver Page:VPane').set_position(232)
findWidget('OOF3D').resize(995, 635)
findWidget('OOF3D:Solver Page:VPane').set_position(235)
findWidget('OOF3D').resize(1014, 647)
findWidget('OOF3D:Solver Page:VPane').set_position(241)
findWidget('OOF3D').resize(1025, 652)
findWidget('OOF3D:Solver Page:VPane').set_position(243)
findWidget('OOF3D').resize(1042, 661)
findWidget('OOF3D:Solver Page:VPane').set_position(248)
findWidget('OOF3D').resize(1059, 666)
findWidget('OOF3D:Solver Page:VPane').set_position(250)
findWidget('OOF3D').resize(1068, 670)
findWidget('OOF3D:Solver Page:VPane').set_position(252)
findWidget('OOF3D').resize(1081, 678)
findWidget('OOF3D:Solver Page:VPane').set_position(256)
findWidget('OOF3D').resize(1092, 685)
findWidget('OOF3D:Solver Page:VPane').set_position(260)
findWidget('OOF3D').resize(1096, 685)
findWidget('OOF3D').resize(1098, 686)
findWidget('OOF3D:Solver Page:VPane').set_position(261)
findWidget('OOF3D').resize(1099, 686)
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(475, 179)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Basic:matrix_method:Chooser'), 'Direct')
assert tests.SetSolverDialogCheck(('Static','Adaptive','Uniform'), ('Iterative', 'Direct'))
assert tests.SetSolverDialogSelect('Static', 'Direct')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
assert tests.solverSubproblemsPageSensitivityCheck2()
assert tests.solverFieldsPageSensitivityCheck0()
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(364, 135)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Basic:time_stepper:Chooser'), 'Adaptive')
findWidget('Dialog-Specify Solver').resize(438, 179)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Basic:matrix_method:Chooser'), 'Iterative')
findWidget('Dialog-Specify Solver').resize(475, 223)
assert tests.SetSolverDialogCheck(('Static','Adaptive','Uniform'), ('Iterative', 'Direct'))
assert tests.SetSolverDialogSelect('Adaptive', 'Iterative')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
findWidget('OOF3D Messages 1').resize(803, 200)
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
assert tests.solverSubproblemsPageSensitivityCheck2()
assert tests.solverFieldsPageSensitivityCheck0()
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(475, 223)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Basic:matrix_method:Chooser'), 'Direct')
assert tests.SetSolverDialogCheck(('Static','Adaptive','Uniform'), ('Iterative', 'Direct'))
assert tests.SetSolverDialogSelect('Adaptive', 'Direct')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
assert tests.solverSubproblemsPageSensitivityCheck2()
assert tests.solverFieldsPageSensitivityCheck0()
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(438, 179)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Basic:time_stepper:Chooser'), 'Uniform')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Basic:matrix_method:Chooser'), 'Iterative')
findWidget('Dialog-Specify Solver').resize(475, 201)
assert tests.SetSolverDialogCheck(('Static','Adaptive','Uniform'), ('Iterative', 'Direct'))
assert tests.SetSolverDialogSelect('Uniform', 'Iterative')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
assert tests.solverSubproblemsPageSensitivityCheck2()
assert tests.solverFieldsPageSensitivityCheck0()
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(475, 201)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Basic:matrix_method:Chooser'), 'Direct')
assert tests.SetSolverDialogCheck(('Static','Adaptive','Uniform'), ('Iterative', 'Direct'))
assert tests.SetSolverDialogSelect('Uniform', 'Direct')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
assert tests.solverSubproblemsPageSensitivityCheck2()
assert tests.solverFieldsPageSensitivityCheck0()
findMenu(findWidget('OOF3D:MenuBar'), 'File:Save:Python_Log').activate()
checkpoint toplevel widget mapped Dialog-Python_Log
findWidget('Dialog-Python_Log').resize(190, 92)
findWidget('Dialog-Python_Log:filename').set_text('solverpage.log')
findWidget('Dialog-Python_Log:gtk-ok').clicked()
checkpoint OOF.File.Save.Python_Log
assert tests.filediff('solverpage.log')
widget_2=findWidget('OOF3D')
handled_2=widget_2.event(event(gtk.gdk.DELETE,window=widget_2.window))
postpone if not handled_2: widget_2.destroy()
checkpoint OOF.Graphics_1.File.Close
