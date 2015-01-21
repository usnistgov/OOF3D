# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.3 $
# $Author: langer $
# $Date: 2014/09/27 22:34:59 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from generics import *

def fieldButtonCheck(field, defined, active):
    b1=gtklogger.findWidget('OOF3D:Fields & Equations Page:HPane:Fields:'+field+' defined')
    b2=gtklogger.findWidget('OOF3D:Fields & Equations Page:HPane:Fields:'+field+' active')
    return b1.get_active()==defined and b2.get_active()==active

def eqnButtonCheck(equation, active):
    return (gtklogger.findWidget('OOF3D:Fields & Equations Page:HPane:Equations:'+equation+' active').get_active() == active)
   
def CopyFieldDialogCheck(microstructures, meshes, skeletons, subproblems):
    okbutton = gtklogger.findWidget('Dialog-Select a target Subproblem:gtk-ok')
    return ((okbutton.get_property('sensitive') == True) and
	   chooserCheck('Dialog-Select a target Subproblem:target:Microstructure', microstructures) and
           chooserCheck('Dialog-Select a target Subproblem:target:Mesh', meshes) and
           chooserCheck('Dialog-Select a target Subproblem:target:Skeleton', skeletons) and
           chooserCheck('Dialog-Select a target Subproblem:target:SubProblem', subproblems))
           
def CopyFieldDialogSelect(microstructure, mesh, skeleton, subproblem):
    okbutton = gtklogger.findWidget('Dialog-Select a target Subproblem:gtk-ok')
    return ((okbutton.get_property('sensitive') == True) and
	   chooserStateCheck('Dialog-Select a target Subproblem:target:Microstructure', microstructure) and
           chooserStateCheck('Dialog-Select a target Subproblem:target:Mesh', mesh) and
           chooserStateCheck('Dialog-Select a target Subproblem:target:Skeleton', skeleton) and
           chooserStateCheck('Dialog-Select a target Subproblem:target:SubProblem', subproblem)) 
     
def CopyEquationDialogCheck(microstructures, meshes, skeletons, subproblems):
    okbutton = gtklogger.findWidget('Dialog-Select a target subproblem:gtk-ok')
    return ((okbutton.get_property('sensitive') == True) and
	   chooserCheck('Dialog-Select a target subproblem:target:Microstructure', microstructures) and
           chooserCheck('Dialog-Select a target subproblem:target:Mesh', meshes) and
           chooserCheck('Dialog-Select a target subproblem:target:Skeleton', skeletons) and
           chooserCheck('Dialog-Select a target subproblem:target:SubProblem', subproblems))
           
def CopyEquationDialogSelect(microstructure, mesh, skeleton, subproblem):
    okbutton = gtklogger.findWidget('Dialog-Select a target subproblem:gtk-ok')
    return ((okbutton.get_property('sensitive') == True) and
	   chooserStateCheck('Dialog-Select a target subproblem:target:Microstructure', microstructure) and
           chooserStateCheck('Dialog-Select a target subproblem:target:Mesh', mesh) and
           chooserStateCheck('Dialog-Select a target subproblem:target:Skeleton', skeleton) and
           chooserStateCheck('Dialog-Select a target subproblem:target:SubProblem', subproblem)) 

def solverSubproblemsCheck(names):
    return names == [x.name() for x in treeViewColValues('OOF3D:Solver Page:VPane:Subproblems:SubproblemScroll:SubproblemList', 0)]

def solverFieldsCheck(names):
    return names == [x.name() for x in treeViewColValues('OOF3D:Solver Page:VPane:FieldInit:Scroll:Initializers', 0)]

def solverSubproblemsPageSensitivityCheck0():
    return sensitizationCheck({ 'VPane:Subproblems:Set':0,
				'VPane:Subproblems:Copy':0,
				'VPane:Subproblems:CopyAll':0,
				'VPane:Subproblems:Remove':0,
				'VPane:Subproblems:RemoveAll':0
				},
			       base='OOF3D:Solver Page')
           
def solverSubproblemsPageSensitivityCheck1():
    return sensitizationCheck({ 'VPane:Subproblems:Set':1,
				'VPane:Subproblems:Copy':0,
				'VPane:Subproblems:CopyAll':0,
				'VPane:Subproblems:Remove':0,
				'VPane:Subproblems:RemoveAll':0
				},
			       base='OOF3D:Solver Page')
			       
def solverFieldsPageSensitivityCheck0():
    return sensitizationCheck({ 'VPane:FieldInit:Set':0,
				'VPane:FieldInit:CopyInit':0,
				'VPane:FieldInit:Clear':0,
				'VPane:FieldInit:ClearAll':0,
				'VPane:FieldInit:ApplyAt':0,
				'VPane:FieldInit:Apply':0
				},
			       base='OOF3D:Solver Page')
			       
def solverFieldsPageSensitivityCheck1():
    return sensitizationCheck({ 'VPane:FieldInit:Set':1,
				'VPane:FieldInit:CopyInit':0,
				'VPane:FieldInit:Clear':0,
				'VPane:FieldInit:ClearAll':0,
				'VPane:FieldInit:ApplyAt':0,
				'VPane:FieldInit:Apply':0
				},
			       base='OOF3D:Solver Page')
