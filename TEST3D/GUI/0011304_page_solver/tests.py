# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.3 $
# $Author: langer $
# $Date: 2014/09/27 22:35:12 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from generics import *

def solverSubproblemsCheck(names):
    return names == [x.name() for x in treeViewColValues('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList', 0)]

def solverFieldsCheck(names):
    return names == [x.name() for x in treeViewColValues('OOF3D:Solver Page:VPane:FieldInit:Scroll:Initializers', 0)]
			       
def SetSolverDialogCheck(mode=None, stepper=None, method=None, symetric=None, selectedsym=None, precondsym=None, asymetric=None, selectedasym=None, precondasym=None):
    okbutton = gtklogger.findWidget('Dialog-Specify Solver:gtk-ok')
    return ((okbutton.get_property('sensitive') == True) and
	   chooserCheck('Dialog-Specify Solver:solver_mode:Chooser', mode) and
           chooserCheck('Dialog-Specify Solver:solver_mode:Advanced:nonlinear_solver:Chooser', method) and
           chooserCheck('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser', symetric) and
           (True if precondsym == None else chooserCheck('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:'+selectedsym+':preconditioner:Chooser', precondsym)) and
           chooserCheck('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser', asymetric) and
           (True if precondasym == None else chooserCheck('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:'+selectedasym+':preconditioner:Chooser', precondasym)))
           
def SetSolverDialogSelect(mode=None, stepper=None, method=None, symetric=None, precondsym=None, asymetric=None, precondasym=None):
    okbutton = gtklogger.findWidget('Dialog-Specify Solver:gtk-ok')
    return ((okbutton.get_property('sensitive') == True) and
           chooserStateCheck('Dialog-Specify Solver:solver_mode:Chooser', mode) and
           chooserStateCheck('Dialog-Specify Solver:solver_mode:Advanced:nonlinear_solver:Chooser', method) and
           chooserStateCheck('Dialog-Specify Solver:solver_mode:Advanced:symmetric_solver:Chooser', symetric) and
           chooserStateCheck('Dialog-Specify Solver:solver_mode:Advanced:asymmetric_solver:Chooser', asymetric))
           
def SetTimeStepperDialogCheck(methods=None, stepper=None):
    okbutton = gtklogger.findWidget('Dialog-Specify Solver:gtk-ok')
    return ((okbutton.get_property('sensitive') == True) and
	   chooserCheck('Dialog-Specify Solver:solver_mode:Advanced:time_stepper:Chooser', methods) and
           chooserCheck('Dialog-Specify Solver:solver_mode:Advanced:time_stepper:Uniform:stepper:Chooser', stepper))
           
           
def SetTimeStepperDialogSelect(method=None, stepper=None):
    okbutton = gtklogger.findWidget('Dialog-Specify Solver:gtk-ok')
    return ((okbutton.get_property('sensitive') == True) and
	   chooserStateCheck('Dialog-Specify Solver:solver_mode:Advanced:time_stepper:Chooser', method) and
           chooserStateCheck('Dialog-Specify Solver:solver_mode:Advanced:time_stepper:Uniform:stepper:Chooser', stepper))
