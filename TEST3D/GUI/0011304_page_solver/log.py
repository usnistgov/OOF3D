# -*- python -*-
# $RCSfile: log.py,v $
# $Revision: 1.1.2.6 $
# $Author: fyc $
# $Date: 2014/07/07 17:26:17 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

import tests

#Testing Advanced Solver Mode with a Uniform time stepper

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
findWidget('OOF3D').resize(550, 350)
setComboBox(findWidget('OOF3D:Navigation:PageMenu'), 'Solver')
checkpoint Solver page sensitized
checkpoint page installed Solver
findWidget('OOF3D').resize(552, 427)
findWidget('OOF3D:Solver Page:VPane').set_position(130)
findCellRenderer(findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList'), col=1, rend=0).emit('toggled', '0')
findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList').get_selection().select_path((0,))
checkpoint Solver page sensitized
findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll').get_vadjustment().set_value( 3.0000000000000e+00)
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Disable_Solution
findCellRenderer(findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList'), col=1, rend=0).emit('toggled', '0')
findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll').get_vadjustment().set_value( 0.0000000000000e+00)
tree=findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList')
column = tree.get_column(1)
tree.row_activated((0,), column)
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(475, 179)
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Enable_Solution
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Chooser'), 'Advanced')
findWidget('Dialog-Specify Solver').resize(500, 343)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:time_stepper:Chooser'), 'Uniform')
assert tests.SetTimeStepperDialogCheck(('Static','Adaptive','Uniform'), ('Forward Euler','Backward Euler','Crank-Nicolson','Liniger','Galerkin','2nd order Runge-Kutta','4th order Runge-Kutta','SS22'))
assert tests.SetTimeStepperDialogSelect('Uniform', 'Forward Euler')
findWidget('Dialog-Specify Solver').resize(576, 395)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
findWidget('OOF3D Messages 1').resize(793, 200)
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(576, 395)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:time_stepper:Uniform:stepper:Chooser'), 'Backward Euler')
assert tests.SetTimeStepperDialogCheck(('Static','Adaptive','Uniform'), ('Forward Euler','Backward Euler','Crank-Nicolson','Liniger','Galerkin','2nd order Runge-Kutta','4th order Runge-Kutta','SS22'))
assert tests.SetTimeStepperDialogSelect('Uniform', 'Backward Euler')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(576, 395)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:time_stepper:Uniform:stepper:Chooser'), 'Crank-Nicolson')
assert tests.SetTimeStepperDialogCheck(('Static','Adaptive','Uniform'), ('Forward Euler','Backward Euler','Crank-Nicolson','Liniger','Galerkin','2nd order Runge-Kutta','4th order Runge-Kutta','SS22'))
assert tests.SetTimeStepperDialogSelect('Uniform', 'Crank-Nicolson')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(576, 395)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:time_stepper:Uniform:stepper:Chooser'), 'Liniger')
assert tests.SetTimeStepperDialogCheck(('Static','Adaptive','Uniform'), ('Forward Euler','Backward Euler','Crank-Nicolson','Liniger','Galerkin','2nd order Runge-Kutta','4th order Runge-Kutta','SS22'))
assert tests.SetTimeStepperDialogSelect('Uniform', 'Liniger')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(576, 395)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:time_stepper:Uniform:stepper:Chooser'), 'Galerkin')
assert tests.SetTimeStepperDialogCheck(('Static','Adaptive','Uniform'), ('Forward Euler','Backward Euler','Crank-Nicolson','Liniger','Galerkin','2nd order Runge-Kutta','4th order Runge-Kutta','SS22'))
assert tests.SetTimeStepperDialogSelect('Uniform', 'Galerkin')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(576, 395)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:time_stepper:Uniform:stepper:Chooser'), '2nd order Runge-Kutta')
assert tests.SetTimeStepperDialogCheck(('Static','Adaptive','Uniform'), ('Forward Euler','Backward Euler','Crank-Nicolson','Liniger','Galerkin','2nd order Runge-Kutta','4th order Runge-Kutta','SS22'))
assert tests.SetTimeStepperDialogSelect('Uniform', '2nd order Runge-Kutta')
findWidget('Dialog-Specify Solver').resize(576, 395)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(576, 395)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:time_stepper:Uniform:stepper:Chooser'), '4th order Runge-Kutta')
assert tests.SetTimeStepperDialogCheck(('Static','Adaptive','Uniform'), ('Forward Euler','Backward Euler','Crank-Nicolson','Liniger','Galerkin','2nd order Runge-Kutta','4th order Runge-Kutta','SS22'))
assert tests.SetTimeStepperDialogSelect('Uniform', '4th order Runge-Kutta')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(576, 395)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:time_stepper:Uniform:stepper:Chooser'), 'SS22')
assert tests.SetTimeStepperDialogCheck(('Static','Adaptive','Uniform'), ('Forward Euler','Backward Euler','Crank-Nicolson','Liniger','Galerkin','2nd order Runge-Kutta','4th order Runge-Kutta','SS22'))
assert tests.SetTimeStepperDialogSelect('Uniform', 'SS22')
findWidget('Dialog-Specify Solver').resize(607, 439)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(607, 439)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:time_stepper:Uniform:stepper:Chooser'), 'Forward Euler')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:nonlinear_solver:Chooser'), 'Newton')
assert tests.SetTimeStepperDialogCheck(('Static','Adaptive','Uniform'), ('Forward Euler','Backward Euler','Crank-Nicolson','Liniger','Galerkin','2nd order Runge-Kutta','4th order Runge-Kutta','SS22'))
assert tests.SetTimeStepperDialogSelect('Uniform', 'Forward Euler')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='CG', precondsym='ILU', asymetric='BiCG', precondasym='ILU')
findWidget('Dialog-Specify Solver').resize(607, 461)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
findWidget('OOF3D Messages 1').resize(1113, 200)
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(576, 461)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:time_stepper:Uniform:stepper:Chooser'), 'Backward Euler')
assert tests.SetTimeStepperDialogCheck(('Static','Adaptive','Uniform'), ('Forward Euler','Backward Euler','Crank-Nicolson','Liniger','Galerkin','2nd order Runge-Kutta','4th order Runge-Kutta','SS22'))
assert tests.SetTimeStepperDialogSelect('Uniform', 'Backward Euler')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(576, 461)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:time_stepper:Uniform:stepper:Chooser'), 'Crank-Nicolson')
assert tests.SetTimeStepperDialogCheck(('Static','Adaptive','Uniform'), ('Forward Euler','Backward Euler','Crank-Nicolson','Liniger','Galerkin','2nd order Runge-Kutta','4th order Runge-Kutta','SS22'))
assert tests.SetTimeStepperDialogSelect('Uniform', 'Crank-Nicolson')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(576, 461)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:time_stepper:Uniform:stepper:Chooser'), 'Liniger')
assert tests.SetTimeStepperDialogCheck(('Static','Adaptive','Uniform'), ('Forward Euler','Backward Euler','Crank-Nicolson','Liniger','Galerkin','2nd order Runge-Kutta','4th order Runge-Kutta','SS22'))
assert tests.SetTimeStepperDialogSelect('Uniform', 'Liniger')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(576, 461)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:time_stepper:Uniform:stepper:Chooser'), 'Galerkin')
assert tests.SetTimeStepperDialogCheck(('Static','Adaptive','Uniform'), ('Forward Euler','Backward Euler','Crank-Nicolson','Liniger','Galerkin','2nd order Runge-Kutta','4th order Runge-Kutta','SS22'))
assert tests.SetTimeStepperDialogSelect('Uniform', 'Galerkin')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(576, 461)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:time_stepper:Uniform:stepper:Chooser'), '2nd order Runge-Kutta')
assert tests.SetTimeStepperDialogCheck(('Static','Adaptive','Uniform'), ('Forward Euler','Backward Euler','Crank-Nicolson','Liniger','Galerkin','2nd order Runge-Kutta','4th order Runge-Kutta','SS22'))
assert tests.SetTimeStepperDialogSelect('Uniform', '2nd order Runge-Kutta')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(576, 461)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:time_stepper:Uniform:stepper:Chooser'), '4th order Runge-Kutta')
assert tests.SetTimeStepperDialogCheck(('Static','Adaptive','Uniform'), ('Forward Euler','Backward Euler','Crank-Nicolson','Liniger','Galerkin','2nd order Runge-Kutta','4th order Runge-Kutta','SS22'))
assert tests.SetTimeStepperDialogSelect('Uniform', '4th order Runge-Kutta')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(576, 461)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:time_stepper:Uniform:stepper:Chooser'), 'SS22')
assert tests.SetTimeStepperDialogCheck(('Static','Adaptive','Uniform'), ('Forward Euler','Backward Euler','Crank-Nicolson','Liniger','Galerkin','2nd order Runge-Kutta','4th order Runge-Kutta','SS22'))
assert tests.SetTimeStepperDialogSelect('Uniform', 'SS22')
findWidget('Dialog-Specify Solver').resize(607, 505)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(607, 505)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:time_stepper:Uniform:stepper:Chooser'), 'Forward Euler')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:nonlinear_solver:Chooser'), 'Picard')
assert tests.SetTimeStepperDialogCheck(('Static','Adaptive','Uniform'), ('Forward Euler','Backward Euler','Crank-Nicolson','Liniger','Galerkin','2nd order Runge-Kutta','4th order Runge-Kutta','SS22'))
assert tests.SetTimeStepperDialogSelect('Uniform', 'Forward Euler')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='CG', precondsym='ILU', asymetric='BiCG', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(576, 461)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:time_stepper:Uniform:stepper:Chooser'), 'Backward Euler')
assert tests.SetTimeStepperDialogCheck(('Static','Adaptive','Uniform'), ('Forward Euler','Backward Euler','Crank-Nicolson','Liniger','Galerkin','2nd order Runge-Kutta','4th order Runge-Kutta','SS22'))
assert tests.SetTimeStepperDialogSelect('Uniform', 'Backward Euler')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(576, 461)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:time_stepper:Uniform:stepper:Chooser'), 'Crank-Nicolson')
assert tests.SetTimeStepperDialogCheck(('Static','Adaptive','Uniform'), ('Forward Euler','Backward Euler','Crank-Nicolson','Liniger','Galerkin','2nd order Runge-Kutta','4th order Runge-Kutta','SS22'))
assert tests.SetTimeStepperDialogSelect('Uniform', 'Crank-Nicolson')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(576, 461)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:time_stepper:Uniform:stepper:Chooser'), 'Liniger')
assert tests.SetTimeStepperDialogCheck(('Static','Adaptive','Uniform'), ('Forward Euler','Backward Euler','Crank-Nicolson','Liniger','Galerkin','2nd order Runge-Kutta','4th order Runge-Kutta','SS22'))
assert tests.SetTimeStepperDialogSelect('Uniform', 'Liniger')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(576, 461)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:time_stepper:Uniform:stepper:Chooser'), 'Galerkin')
assert tests.SetTimeStepperDialogCheck(('Static','Adaptive','Uniform'), ('Forward Euler','Backward Euler','Crank-Nicolson','Liniger','Galerkin','2nd order Runge-Kutta','4th order Runge-Kutta','SS22'))
assert tests.SetTimeStepperDialogSelect('Uniform', 'Galerkin')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(576, 461)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:time_stepper:Uniform:stepper:Chooser'), '2nd order Runge-Kutta')
assert tests.SetTimeStepperDialogCheck(('Static','Adaptive','Uniform'), ('Forward Euler','Backward Euler','Crank-Nicolson','Liniger','Galerkin','2nd order Runge-Kutta','4th order Runge-Kutta','SS22'))
assert tests.SetTimeStepperDialogSelect('Uniform', '2nd order Runge-Kutta')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(576, 461)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:time_stepper:Uniform:stepper:Chooser'), '4th order Runge-Kutta')
assert tests.SetTimeStepperDialogCheck(('Static','Adaptive','Uniform'), ('Forward Euler','Backward Euler','Crank-Nicolson','Liniger','Galerkin','2nd order Runge-Kutta','4th order Runge-Kutta','SS22'))
assert tests.SetTimeStepperDialogSelect('Uniform', '4th order Runge-Kutta')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(576, 461)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:time_stepper:Uniform:stepper:Chooser'), 'SS22')
assert tests.SetTimeStepperDialogCheck(('Static','Adaptive','Uniform'), ('Forward Euler','Backward Euler','Crank-Nicolson','Liniger','Galerkin','2nd order Runge-Kutta','4th order Runge-Kutta','SS22'))
assert tests.SetTimeStepperDialogSelect('Uniform', 'SS22')
findWidget('Dialog-Specify Solver').resize(607, 505)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(607, 505)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'BiCGStab')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:nonlinear_solver:Chooser'), 'None')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='BiCGStab', precondsym='ILU', asymetric='BiCG', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D').resize(554, 427)
findWidget('OOF3D').resize(555, 427)
findWidget('OOF3D').resize(557, 427)
findWidget('OOF3D').resize(562, 429)
findWidget('OOF3D:Solver Page:VPane').set_position(131)
findWidget('OOF3D').resize(565, 431)
findWidget('OOF3D:Solver Page:VPane').set_position(132)
findWidget('OOF3D').resize(573, 434)
findWidget('OOF3D:Solver Page:VPane').set_position(134)
findWidget('OOF3D').resize(591, 438)
findWidget('OOF3D:Solver Page:VPane').set_position(136)
findWidget('OOF3D').resize(600, 442)
findWidget('OOF3D:Solver Page:VPane').set_position(138)
findWidget('OOF3D').resize(617, 449)
findWidget('OOF3D:Solver Page:VPane').set_position(141)
findWidget('OOF3D').resize(623, 449)
findWidget('OOF3D').resize(634, 452)
findWidget('OOF3D:Solver Page:VPane').set_position(143)
findWidget('OOF3D').resize(639, 452)
findWidget('OOF3D').resize(649, 456)
findWidget('OOF3D:Solver Page:VPane').set_position(145)
findWidget('OOF3D').resize(655, 457)
findWidget('OOF3D').resize(660, 459)
findWidget('OOF3D:Solver Page:VPane').set_position(146)
findWidget('OOF3D').resize(672, 463)
findWidget('OOF3D:Solver Page:VPane').set_position(148)
findWidget('OOF3D').resize(678, 465)
findWidget('OOF3D:Solver Page:VPane').set_position(149)
findWidget('OOF3D').resize(693, 467)
findWidget('OOF3D:Solver Page:VPane').set_position(150)
findWidget('OOF3D').resize(699, 468)
findWidget('OOF3D:Solver Page:VPane').set_position(151)
findWidget('OOF3D').resize(706, 470)
findWidget('OOF3D:Solver Page:VPane').set_position(152)
findWidget('OOF3D').resize(718, 473)
findWidget('OOF3D:Solver Page:VPane').set_position(153)
findWidget('OOF3D').resize(724, 473)
findWidget('OOF3D').resize(737, 475)
findWidget('OOF3D:Solver Page:VPane').set_position(154)
findWidget('OOF3D').resize(741, 475)
findWidget('OOF3D').resize(750, 476)
findWidget('OOF3D:Solver Page:VPane').set_position(155)
findWidget('OOF3D').resize(754, 478)
findWidget('OOF3D:Solver Page:VPane').set_position(156)
findWidget('OOF3D').resize(762, 478)
findWidget('OOF3D').resize(766, 478)
findWidget('OOF3D').resize(769, 480)
findWidget('OOF3D:Solver Page:VPane').set_position(157)
findWidget('OOF3D').resize(773, 481)
findWidget('OOF3D').resize(780, 484)
findWidget('OOF3D:Solver Page:VPane').set_position(159)
findWidget('OOF3D').resize(783, 486)
findWidget('OOF3D:Solver Page:VPane').set_position(160)
findWidget('OOF3D').resize(788, 489)
findWidget('OOF3D:Solver Page:VPane').set_position(161)
findWidget('OOF3D').resize(792, 492)
findWidget('OOF3D:Solver Page:VPane').set_position(163)
findWidget('OOF3D').resize(794, 494)
findWidget('OOF3D:Solver Page:VPane').set_position(164)
findWidget('OOF3D').resize(798, 496)
findWidget('OOF3D:Solver Page:VPane').set_position(165)
findWidget('OOF3D').resize(800, 499)
findWidget('OOF3D:Solver Page:VPane').set_position(166)
findWidget('OOF3D').resize(805, 504)
findWidget('OOF3D:Solver Page:VPane').set_position(169)
findWidget('OOF3D').resize(808, 506)
findWidget('OOF3D:Solver Page:VPane').set_position(170)
findWidget('OOF3D').resize(816, 514)
findWidget('OOF3D:Solver Page:VPane').set_position(174)
findWidget('OOF3D').resize(827, 524)
findWidget('OOF3D:Solver Page:VPane').set_position(179)
findWidget('OOF3D').resize(839, 532)
findWidget('OOF3D:Solver Page:VPane').set_position(183)
findWidget('OOF3D').resize(849, 539)
findWidget('OOF3D:Solver Page:VPane').set_position(186)
findWidget('OOF3D').resize(853, 540)
findWidget('OOF3D:Solver Page:VPane').set_position(187)
findWidget('OOF3D').resize(858, 544)
findWidget('OOF3D:Solver Page:VPane').set_position(189)
findWidget('OOF3D').resize(860, 544)
findWidget('OOF3D').resize(863, 546)
findWidget('OOF3D:Solver Page:VPane').set_position(190)
findWidget('OOF3D').resize(864, 548)
findWidget('OOF3D:Solver Page:VPane').set_position(191)
findWidget('OOF3D').resize(868, 552)
findWidget('OOF3D:Solver Page:VPane').set_position(193)
findWidget('OOF3D').resize(871, 555)
findWidget('OOF3D:Solver Page:VPane').set_position(194)
findWidget('OOF3D').resize(874, 557)
findWidget('OOF3D:Solver Page:VPane').set_position(196)
findWidget('OOF3D').resize(877, 561)
findWidget('OOF3D:Solver Page:VPane').set_position(198)
findWidget('OOF3D').resize(880, 562)
findWidget('OOF3D').resize(885, 565)
findWidget('OOF3D:Solver Page:VPane').set_position(200)
findWidget('OOF3D').resize(888, 567)
findWidget('OOF3D:Solver Page:VPane').set_position(201)
findWidget('OOF3D').resize(889, 567)
findWidget('OOF3D').resize(889, 568)
findWidget('OOF3D').resize(891, 568)
findWidget('OOF3D').resize(891, 569)
findWidget('OOF3D:Solver Page:VPane').set_position(202)
findWidget('OOF3D').resize(892, 569)
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(500, 343)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'GMRES')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='GMRES', precondsym='ILU', asymetric='BiCG', precondasym='ILU')
findWidget('Dialog-Specify Solver').resize(518, 365)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
findWidget('OOF3D Messages 1').resize(1003, 200)
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(518, 365)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'Direct')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='Direct', precondsym=None, asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='Direct', precondsym=None, asymetric='BiCG', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(500, 269)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'CG')
findWidget('Dialog-Specify Solver').resize(500, 343)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:nonlinear_solver:Chooser'), 'Newton')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='CG', precondsym='ILU', asymetric='BiCG', precondasym='ILU')
findWidget('Dialog-Specify Solver').resize(538, 409)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
findWidget('OOF3D Messages 1').resize(1113, 200)
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'BiCG')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='BiCG', precondsym='ILU', asymetric='BiCG', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
findWidget('OOF3D Messages 1').resize(1133, 200)
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'BiCGStab')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='BiCGStab', precondsym='ILU', asymetric='BiCG', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
findWidget('OOF3D Messages 1').resize(1233, 200)
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'GMRES')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='GMRES', precondsym='ILU', asymetric='BiCG', precondasym='ILU')
findWidget('Dialog-Specify Solver').resize(538, 431)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'Direct')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='Direct', precondsym=None, asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='Direct', precondsym=None, asymetric='BiCG', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 335)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'CG')
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:nonlinear_solver:Chooser'), 'Picard')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='CG', precondsym='ILU', asymetric='BiCG', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'BiCG')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='BiCG', precondsym='ILU', asymetric='BiCG', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'BiCGStab')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='BiCGStab', precondsym='ILU', asymetric='BiCG', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'GMRES')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='ILU', asymetric='BiCG', precondasym='ILU')
findWidget('Dialog-Specify Solver').resize(538, 431)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'Direct')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='Direct', precondsym=None, asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='Direct', precondsym=None, asymetric='BiCG', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 335)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'CG')
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:nonlinear_solver:Chooser'), 'None')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'BiCGStab')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='CG', precondsym='ILU', asymetric='BiCGStab', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(500, 343)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'GMRES')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='CG', precondsym='ILU', asymetric='GMRES', precondasym='ILU')
findWidget('Dialog-Specify Solver').resize(518, 365)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(518, 365)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'Direct')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='Direct', precondasym=None)
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='CG', precondsym='ILU', asymetric='Direct', precondasym=None)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(500, 269)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'GMRES')
findWidget('Dialog-Specify Solver').resize(518, 365)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'BiCG')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'BiCG')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'BiCGStab')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='BiCG', precondsym='ILU', asymetric='BiCGStab', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(500, 343)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'GMRES')###
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='BiCG', precondsym='ILU', asymetric='GMRES', precondasym='ILU')
findWidget('Dialog-Specify Solver').resize(518, 365)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(518, 365)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'Direct')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='Direct', precondasym=None)
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='BiCG', precondsym='ILU', asymetric='Direct', precondasym=None)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(500, 269)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'BiCG')
findWidget('Dialog-Specify Solver').resize(500, 343)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'BiCGStab')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'BiCGStab')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='BiCGStab', precondsym='ILU', asymetric='BiCGStab', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(500, 343)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'GMRES')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='BiCGStab', precondsym='ILU', asymetric='GMRES', precondasym='ILU')
findWidget('Dialog-Specify Solver').resize(518, 365)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(518, 365)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'Direct')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='Direct', precondasym=None)
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='BiCGStab', precondsym='ILU', asymetric='Direct', precondasym=None)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(500, 269)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'BiCG')
findWidget('Dialog-Specify Solver').resize(500, 343)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'GMRES')
findWidget('Dialog-Specify Solver').resize(518, 365)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'BiCGStab')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='GMRES', precondsym='ILU', asymetric='BiCGStab', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(518, 365)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'GMRES')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='GMRES', precondsym='ILU', asymetric='GMRES', precondasym='ILU')
findWidget('Dialog-Specify Solver').resize(518, 387)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(518, 387)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'Direct')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='Direct', precondasym=None)
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='GMRES', precondsym='ILU', asymetric='Direct', precondasym=None)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(518, 291)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'BiCG')
findWidget('Dialog-Specify Solver').resize(518, 365)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'Direct')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'BiCGStab')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='Direct', precondsym=None, asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='Direct', precondsym=None, asymetric='BiCGStab', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(500, 269)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'GMRES')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='Direct', precondsym=None, asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='Direct', precondsym=None, asymetric='GMRES', precondasym='ILU')
findWidget('Dialog-Specify Solver').resize(518, 291)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(518, 291)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'Direct')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='Direct', precondsym=None, asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='Direct', precondasym=None)
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='Direct', precondsym=None, asymetric='Direct', precondasym=None)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(381, 195)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'BiCG')
findWidget('Dialog-Specify Solver').resize(500, 269)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'CG')
findWidget('Dialog-Specify Solver').resize(500, 343)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:nonlinear_solver:Chooser'), 'Newton')
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'BiCGStab')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='CG', precondsym='ILU', asymetric='BiCGStab', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'GMRES')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='CG', precondsym='ILU', asymetric='GMRES', precondasym='ILU')
findWidget('Dialog-Specify Solver').resize(538, 431)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'Direct')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='Direct', precondasym=None)
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='CG', precondsym='ILU', asymetric='Direct', precondasym=None)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 335)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'BiCG')
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'BiCG')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'BiCGStab')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='BiCG', precondsym='ILU', asymetric='BiCGStab', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'GMRES')
findWidget('Dialog-Specify Solver').resize(538, 431)
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='BiCG', precondsym='ILU', asymetric='GMRES', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'Direct')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='Direct', precondasym=None)
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='BiCG', precondsym='ILU', asymetric='Direct', precondasym=None)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 335)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'BiCGStab')
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'BiCGStab')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='BiCGStab', precondsym='ILU', asymetric='BiCGStab', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'GMRES')
findWidget('Dialog-Specify Solver').resize(538, 431)
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='BiCGStab', precondsym='ILU', asymetric='GMRES', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'Direct')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='Direct', precondasym=None)
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='BiCGStab', precondsym='ILU', asymetric='Direct', precondasym=None)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 335)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'BiCGStab')
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'GMRES')
findWidget('Dialog-Specify Solver').resize(538, 431)
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='GMRES', precondsym='ILU', asymetric='BiCGStab', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'GMRES')
findWidget('Dialog-Specify Solver').resize(538, 453)
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='GMRES', precondsym='ILU', asymetric='GMRES', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 453)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'Direct')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='Direct', precondasym=None)
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='GMRES', precondsym='ILU', asymetric='Direct', precondasym=None)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 357)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'BiCGStab')
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'Direct')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='Direct', precondsym=None, asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='Direct', precondsym=None, asymetric='BiCGStab', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 335)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'GMRES')
findWidget('Dialog-Specify Solver').resize(538, 357)
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='Direct', precondsym=None, asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='Direct', precondsym=None, asymetric='GMRES', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 357)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'Direct')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='Direct', precondsym=None, asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='Direct', precondasym=None)
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='Direct', precondsym=None, asymetric='Direct', precondasym=None)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 261)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'BiCGStab')
findWidget('Dialog-Specify Solver').resize(538, 335)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'CG')
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:nonlinear_solver:Chooser'), 'Picard')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='CG', precondsym='ILU', asymetric='BiCGStab', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'GMRES')
findWidget('Dialog-Specify Solver').resize(538, 431)
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='CG', precondsym='ILU', asymetric='GMRES', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'Direct')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='Direct', precondasym=None)
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='CG', precondsym='ILU', asymetric='Direct', precondasym=None)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 335)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'BiCGStab')
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'BiCG')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='BiCG', precondsym='ILU', asymetric='BiCGStab', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'GMRES')
findWidget('Dialog-Specify Solver').resize(538, 431)
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='BiCG', precondsym='ILU', asymetric='GMRES', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'Direct')
findWidget('Dialog-Specify Solver').resize(538, 431)
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='Direct', precondasym=None)
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='BiCG', precondsym='ILU', asymetric='Direct', precondasym=None)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 335)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'BiCGStab')
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'BiCGStab')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='BiCGStab', precondsym='ILU', asymetric='BiCGStab', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'GMRES')
findWidget('Dialog-Specify Solver').resize(538, 431)
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='BiCGStab', precondsym='ILU', asymetric='GMRES', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'Direct')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='Direct', precondasym=None)
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='BiCGStab', precondsym='ILU', asymetric='Direct', precondasym=None)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 335)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'BiCGStab')
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'GMRES')
findWidget('Dialog-Specify Solver').resize(538, 431)
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='ILU', asymetric='BiCGStab', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'GMRES')
findWidget('Dialog-Specify Solver').resize(538, 453)
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='ILU', asymetric='GMRES', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 453)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'Direct')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=None)
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='ILU', asymetric='Direct', precondasym=None)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 357)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'BiCGStab')
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'Direct')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='Direct', precondsym=None, asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='Direct', precondsym=None, asymetric='BiCGStab', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 335)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'GMRES')
findWidget('Dialog-Specify Solver').resize(538, 357)
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='Direct', precondsym=None, asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='Direct', precondsym=None, asymetric='GMRES', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 357)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'Direct')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='Direct', precondsym=None, asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='Direct', precondasym=None)
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='Direct', precondsym=None, asymetric='Direct', precondasym=None)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 261)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'BiCGStab')
findWidget('Dialog-Specify Solver').resize(538, 335)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'CG')
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:nonlinear_solver:Chooser'), 'None')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'IC')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='CG', precondsym='ILU', asymetric='BiCGStab', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(500, 343)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='CG', precondsym='ILU', asymetric='BiCGStab', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(500, 343)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='CG', precondsym='ILU', asymetric='BiCGStab', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(500, 343)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'ILU')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:CG:preconditioner:Chooser'), 'IC')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='CG', precondsym='IC', asymetric='BiCGStab', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(500, 343)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:CG:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='CG', precondsym='Jacobi', asymetric='BiCGStab', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(500, 343)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:CG:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='CG', precondsym='Null', asymetric='BiCGStab', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(500, 343)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:CG:preconditioner:Chooser'), 'ILU')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'BiCG')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'IC')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='CG', precondsym='ILU', asymetric='BiCG', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(500, 343)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='CG', precondsym='ILU', asymetric='BiCG', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(500, 343)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='CG', precondsym='ILU', asymetric='BiCG', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(500, 343)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'ILU')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:CG:preconditioner:Chooser'), 'IC')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='CG', precondsym='IC', asymetric='BiCG', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(500, 343)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:CG:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='CG', precondsym='Jacobi', asymetric='BiCG', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(500, 343)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:CG:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='CG', precondsym='Jacobi', asymetric='BiCG', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(500, 343)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:CG:preconditioner:Chooser'), 'ILU')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'BiCGStab')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'BiCG')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'BiCGStab')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'IC')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='BiCGStab', precondsym='ILU', asymetric='BiCG', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
tree=findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList')
column = tree.get_column(3)
tree.row_activated((0,), column)
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(500, 343)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='BiCGStab', precondsym='ILU', asymetric='BiCG', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
tree=findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList')
column = tree.get_column(3)
tree.row_activated((0,), column)
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(500, 343)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='BiCGStab', precondsym='ILU', asymetric='BiCG', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
tree=findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList')
column = tree.get_column(3)
tree.row_activated((0,), column)
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(500, 343)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'ILU')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:BiCGStab:preconditioner:Chooser'), 'IC')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='BiCGStab', precondsym='IC', asymetric='BiCG', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
tree=findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList')
column = tree.get_column(2)
tree.row_activated((0,), column)
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(500, 343)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:BiCGStab:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='BiCGStab', precondsym='Jacobi', asymetric='BiCG', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
tree=findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList')
column = tree.get_column(3)
tree.row_activated((0,), column)
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(500, 343)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:BiCGStab:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='BiCGStab', precondsym='Null', asymetric='BiCG', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
tree=findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList')
column = tree.get_column(3)
tree.row_activated((0,), column)
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(500, 343)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:BiCGStab:preconditioner:Chooser'), 'ILU')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'GMRES')
findWidget('Dialog-Specify Solver').resize(518, 365)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'IC')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='GMRES', precondsym='ILU', asymetric='BiCG', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
tree=findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList')
column = tree.get_column(2)
tree.row_activated((0,), column)
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(518, 365)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='GMRES', precondsym='ILU', asymetric='BiCG', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
tree=findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList')
column = tree.get_column(3)
tree.row_activated((0,), column)
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(518, 365)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='GMRES', precondsym='ILU', asymetric='BiCG', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
tree=findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList')
column = tree.get_column(2)
tree.row_activated((0,), column)
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(518, 365)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'ILU')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:GMRES:preconditioner:Chooser'), 'IC')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='GMRES', precondsym='IC', asymetric='BiCG', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
tree=findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList')
column = tree.get_column(3)
tree.row_activated((0,), column)
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(518, 365)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:GMRES:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='GMRES', precondsym='Jacobi', asymetric='BiCG', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
tree=findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList')
column = tree.get_column(3)
tree.row_activated((0,), column)
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(518, 365)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:GMRES:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='GMRES', precondsym='Null', asymetric='BiCG', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
tree=findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList')
column = tree.get_column(3)
tree.row_activated((0,), column)
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(518, 365)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:GMRES:preconditioner:Chooser'), 'ILU')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'Direct')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'IC')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='Direct', precondsym=None, asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='Direct', precondsym=None, asymetric='BiCG', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(500, 269)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='Direct', precondsym=None, asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='Direct', precondsym=None, asymetric='BiCG', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(500, 269)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='Direct', precondsym=None, asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='None', symetric='Direct', precondsym=None, asymetric='BiCG', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
tree=findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList')
column = tree.get_column(2)
tree.row_activated((0,), column)
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(500, 269)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'CG')
findWidget('Dialog-Specify Solver').resize(500, 343)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:nonlinear_solver:Chooser'), 'Newton')
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'IC')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='CG', precondsym='ILU', asymetric='BiCG', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
tree=findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList')
column = tree.get_column(2)
tree.row_activated((0,), column)
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='CG', precondsym='ILU', asymetric='BiCG', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
tree=findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList')
column = tree.get_column(2)
tree.row_activated((0,), column)
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='CG', precondsym='ILU', asymetric='BiCG', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
tree=findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList')
column = tree.get_column(2)
tree.row_activated((0,), column)
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'ILU')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:CG:preconditioner:Chooser'), 'IC')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='CG', precondsym='IC', asymetric='BiCG', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
tree=findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList')
column = tree.get_column(3)
tree.row_activated((0,), column)
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:CG:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='CG', precondsym='Jacobi', asymetric='BiCG', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
tree=findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList')
column = tree.get_column(3)
tree.row_activated((0,), column)
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:CG:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='CG', precondsym='Null', asymetric='BiCG', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
tree=findWidget('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList')
column = tree.get_column(3)
tree.row_activated((0,), column)
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:CG:preconditioner:Chooser'), 'ILU')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'BiCGStab')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'IC')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='CG', precondsym='ILU', asymetric='BiCGStab', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='CG', precondsym='ILU', asymetric='BiCGStab', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='CG', precondsym='ILU', asymetric='BiCGStab', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'ILU')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'GMRES')
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'IC')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='CG', precondsym='ILU', asymetric='GMRES', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='CG', precondsym='ILU', asymetric='GMRES', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='CG', precondsym='ILU', asymetric='GMRES', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:CG:preconditioner:Chooser'), 'IC')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='CG', precondsym='IC', asymetric='GMRES', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='CG', precondsym='ILU', asymetric='GMRES', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='CG', precondsym='ILU', asymetric='GMRES', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:CG:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='CG', precondsym='Jacobi', asymetric='GMRES', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='CG', precondsym='Jacobi', asymetric='GMRES', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='CG', precondsym='Jacobi', asymetric='GMRES', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:CG:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='CG', precondsym='Null', asymetric='GMRES', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='CG', precondsym='Null', asymetric='GMRES', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='CG', precondsym='Null', asymetric='GMRES', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:CG:preconditioner:Chooser'), 'ILU')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'BiCG')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='BiCG', precondsym='ILU', asymetric='GMRES', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='BiCG', precondsym='ILU', asymetric='GMRES', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='BiCG', precondsym='ILU', asymetric='GMRES', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:BiCG:preconditioner:Chooser'), 'IC')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='BiCG', precondsym='IC', asymetric='GMRES', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='BiCG', precondsym='IC', asymetric='GMRES', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='BiCG', precondsym='IC', asymetric='GMRES', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:BiCG:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='BiCG', precondsym='Jacobi', asymetric='GMRES', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='BiCG', precondsym='Jacobi', asymetric='GMRES', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='BiCG', precondsym='Jacobi', asymetric='GMRES', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:BiCG:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='BiCG', precondsym='Null', asymetric='GMRES', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='BiCG', precondsym='Null', asymetric='GMRES', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='BiCG', precondsym='Null', asymetric='GMRES', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:BiCG:preconditioner:Chooser'), 'ILU')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'BiCGStab')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='BiCGStab', precondsym='ILU', asymetric='GMRES', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='BiCGStab', precondsym='ILU', asymetric='GMRES', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='BiCGStab', precondsym='ILU', asymetric='GMRES', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:BiCGStab:preconditioner:Chooser'), 'IC')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='BiCGStab', precondsym='IC', asymetric='GMRES', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='BiCGStab', precondsym='IC', asymetric='GMRES', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='BiCGStab', precondsym='IC', asymetric='GMRES', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:BiCGStab:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='BiCGStab', precondsym='Jacobi', asymetric='GMRES', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='BiCGStab', precondsym='Jacobi', asymetric='GMRES', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='BiCGStab', precondsym='Jacobi', asymetric='GMRES', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:BiCGStab:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='BiCGStab', precondsym='Null', asymetric='GMRES', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='BiCGStab', precondsym='Null', asymetric='GMRES', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='BiCGStab', precondsym='Null', asymetric='GMRES', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:BiCGStab:preconditioner:Chooser'), 'ILU')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'GMRES')
findWidget('Dialog-Specify Solver').resize(538, 453)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:GMRES:preconditioner:Chooser'), 'ILU')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='GMRES', precondsym='ILU', asymetric='GMRES', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 453)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='GMRES', precondsym='ILU', asymetric='GMRES', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 453)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='GMRES', precondsym='ILU', asymetric='GMRES', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 453)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:GMRES:preconditioner:Chooser'), 'IC')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='GMRES', precondsym='IC', asymetric='GMRES', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 453)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='GMRES', precondsym='IC', asymetric='GMRES', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 453)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='GMRES', precondsym='IC', asymetric='GMRES', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 453)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:GMRES:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='GMRES', precondsym='Jacobi', asymetric='GMRES', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 453)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='GMRES', precondsym='Jacobi', asymetric='GMRES', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 453)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='GMRES', precondsym='Jacobi', asymetric='GMRES', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 453)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:GMRES:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='GMRES', precondsym='Null', asymetric='GMRES', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 453)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='GMRES', precondsym='Null', asymetric='GMRES', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 453)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='GMRES', precondsym='ILU', asymetric='GMRES', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 453)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:GMRES:preconditioner:Chooser'), 'ILU')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'Direct')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='Direct', precondsym=None, asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='Direct', precondsym=None, asymetric='GMRES', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 357)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='Direct', precondsym=None, asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='Direct', precondsym=None, asymetric='GMRES', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 357)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='Direct', precondsym=None, asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Newton', symetric='Direct', precondsym=None, asymetric='GMRES', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 357)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'CG')
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'BiCG')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:nonlinear_solver:Chooser'), 'Picard')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'IC')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='CG', precondsym='ILU', asymetric='BiCG', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='CG', precondsym='ILU', asymetric='BiCG', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='CG', precondsym='ILU', asymetric='BiCG', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:CG:preconditioner:Chooser'), 'IC')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='CG', precondsym='IC', asymetric='BiCG', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='CG', precondsym='IC', asymetric='BiCG', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='CG', precondsym='IC', asymetric='BiCG', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:CG:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='CG', precondsym='Jacobi', asymetric='BiCG', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='CG', precondsym='Jacobi', asymetric='BiCG', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='CG', precondsym='Jacobi', asymetric='BiCG', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:CG:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='CG', precondsym='Null', asymetric='BiCG', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='CG', precondsym='Null', asymetric='BiCG', precondasym='ILU')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='CG', precondsym='Null', asymetric='BiCG', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'BiCGStab')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:CG:preconditioner:Chooser'), 'ILU')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='CG', precondsym='ILU', asymetric='BiCGStab', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='CG', precondsym='ILU', asymetric='BiCGStab', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='CG', precondsym='ILU', asymetric='BiCGStab', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:CG:preconditioner:Chooser'), 'IC')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='CG', precondsym='IC', asymetric='BiCGStab', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='CG', precondsym='IC', asymetric='BiCGStab', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='CG', precondsym='IC', asymetric='BiCGStab', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:CG:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='CG', precondsym='Jacobi', asymetric='BiCGStab', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='CG', precondsym='Jacobi', asymetric='BiCGStab', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Null')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:CG:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='CG', precondsym='Null', asymetric='BiCGStab', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='CG', precondsym='Null', asymetric='BiCGStab', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='CG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='CG', precondsym='Null', asymetric='BiCGStab', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:CG:preconditioner:Chooser'), 'ILU')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'BiCG')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='BiCG', precondsym='ILU', asymetric='BiCGStab', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='BiCG', precondsym='ILU', asymetric='BiCGStab', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='BiCG', precondsym='ILU', asymetric='BiCGStab', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:BiCG:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='BiCG', precondsym='Jacobi', asymetric='BiCGStab', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='BiCG', precondsym='Jacobi', asymetric='BiCGStab', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='BiCG', precondsym='Jacobi', asymetric='BiCGStab', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:BiCG:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='BiCG', precondsym='Null', asymetric='BiCGStab', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='BiCG', precondsym='Null', asymetric='BiCGStab', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCG', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='BiCG', precondsym='Null', asymetric='BiCGStab', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:BiCG:preconditioner:Chooser'), 'ILU')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'BiCGStab')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:BiCGStab:preconditioner:Chooser'), 'ILU')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='BiCGStab', precondsym='ILU', asymetric='BiCGStab', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='BiCGStab', precondsym='ILU', asymetric='BiCGStab', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='BiCGStab', precondsym='ILU', asymetric='BiCGStab', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:BiCGStab:preconditioner:Chooser'), 'IC')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='BiCGStab', precondsym='IC', asymetric='BiCGStab', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='BiCGStab', precondsym='IC', asymetric='BiCGStab', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='BiCGStab', precondsym='IC', asymetric='BiCGStab', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:BiCGStab:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='BiCGStab', precondsym='Jacobi', asymetric='BiCGStab', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='BiCGStab', precondsym='Jacobi', asymetric='BiCGStab', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='BiCGStab', precondsym='Jacobi', asymetric='BiCGStab', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:BiCGStab:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='BiCGStab', precondsym='Null', asymetric='BiCGStab', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='BiCGStab', precondsym='Null', asymetric='BiCGStab', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='BiCGStab', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='BiCGStab', precondsym='Null', asymetric='BiCGStab', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 409)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:BiCGStab:preconditioner:Chooser'), 'ILU')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'GMRES')
findWidget('Dialog-Specify Solver').resize(538, 431)
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='ILU', asymetric='BiCGStab', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='ILU', asymetric='BiCGStab', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='ILU', asymetric='BiCGStab', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:GMRES:preconditioner:Chooser'), 'ILU')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='ILU', asymetric='BiCGStab', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='ILU', asymetric='BiCGStab', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='ILU', asymetric='BiCGStab', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:GMRES:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='Jacobi', asymetric='BiCGStab', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='Jacobi', asymetric='BiCGStab', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='Jacobi', asymetric='BiCGStab', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:GMRES:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='Null', asymetric='BiCGStab', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='Null', asymetric='BiCGStab', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='Null', asymetric='BiCGStab', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'Direct')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='Direct', precondsym=None, asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='Direct', precondsym=None, asymetric='BiCGStab', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 335)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='Direct', precondsym=None, asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='Direct', precondsym=None, asymetric='BiCGStab', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 335)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='Direct', precondsym=None, asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='Direct', precondsym=None, asymetric='BiCGStab', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 335)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'GMRES')
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:GMRES:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:GMRES:preconditioner:Chooser'), 'ILU')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'BiCG')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'IC')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='ILU', asymetric='BiCG', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='ILU', asymetric='BiCG', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCG', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='ILU', asymetric='BiCG', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCG:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'BiCGStab')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='ILU', asymetric='BiCGStab', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='ILU', asymetric='BiCGStab', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='ILU', asymetric='BiCGStab', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:GMRES:preconditioner:Chooser'), 'IC')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='IC', asymetric='BiCGStab', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='IC', asymetric='BiCGStab', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='IC', asymetric='BiCGStab', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:GMRES:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='Jacobi', asymetric='BiCGStab', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='Jacobi', asymetric='BiCGStab', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='Jacobi', asymetric='BiCGStab', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:GMRES:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='Null', asymetric='BiCGStab', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='Null', asymetric='BiCGStab', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='BiCGStab', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='Null', asymetric='BiCGStab', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 431)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:BiCGStab:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:GMRES:preconditioner:Chooser'), 'ILU')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'GMRES')
findWidget('Dialog-Specify Solver').resize(538, 453)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'IC')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='ILU', asymetric='GMRES', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 453)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='ILU', asymetric='GMRES', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 453)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='ILU', asymetric='GMRES', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 453)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:GMRES:preconditioner:Chooser'), 'IC')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='IC', asymetric='GMRES', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 453)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='IC', asymetric='GMRES', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 453)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='IC', asymetric='GMRES', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 453)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:GMRES:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='Jacobi', asymetric='GMRES', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 453)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='Jacobi', asymetric='GMRES', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 453)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='Jacobi', asymetric='GMRES', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 453)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:GMRES:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='Null', asymetric='GMRES', precondasym='IC')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 453)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='Null', asymetric='GMRES', precondasym='Jacobi')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 453)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='GMRES', precondasym=('ILU','IC','Jacobi','Null'))
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='Null', asymetric='GMRES', precondasym='Null')
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 453)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:GMRES:preconditioner:Chooser'), 'IC')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:GMRES:preconditioner:Chooser'), 'ILU')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser'), 'Direct')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:GMRES:preconditioner:Chooser'), 'IC')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='Direct', precondasym=None)
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='IC', asymetric='Direct', precondasym=None)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 357)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:GMRES:preconditioner:Chooser'), 'Jacobi')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='Direct', precondasym=None)
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='Jacobi', asymetric='Direct', precondasym=None)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 357)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:GMRES:preconditioner:Chooser'), 'Null')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='GMRES', precondsym=('ILU','IC','Jacobi','Null'), asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='Direct', precondasym=None)
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='GMRES', precondsym='Null', asymetric='Direct', precondasym=None)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
findWidget('OOF3D:Solver Page:VPane:Subproblems:Set').clicked()
checkpoint toplevel widget mapped Dialog-Specify Solver
findWidget('Dialog-Specify Solver').resize(538, 357)
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:GMRES:preconditioner:Chooser'), 'ILU')
setComboBox(findWidget('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser'), 'Direct')
assert tests.SetSolverDialogCheck(mode=('Basic','Advanced'), stepper=('Static','Adaptive','Uniform'), method=('None','Newton','Picard'), symetric=('CG','BiCG','BiCGStab','GMRES','Direct'), selectedsym='Direct', precondsym=None, asymetric=('BiCG','BiCGStab','GMRES','Direct'), selectedasym='Direct', precondasym=None)
assert tests.SetSolverDialogSelect(mode='Advanced', stepper='Uniform', method='Picard', symetric='Direct', precondsym=None, asymetric='Direct', precondasym=None)
findWidget('Dialog-Specify Solver:gtk-ok').clicked()
checkpoint Solver page sensitized
checkpoint Field page sensitized
checkpoint Solver page sensitized
checkpoint OOF.Subproblem.Set_Solver
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