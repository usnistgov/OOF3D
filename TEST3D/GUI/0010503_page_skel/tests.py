# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.3 $
# $Author: fyc $
# $Date: 2014/02/12 21:13:48 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from generics import *

def skeletonMethodListCheck(*names):
    return chooserCheck('OOF3D:Skeleton Page:Pane:Modification:Method:Chooser', names)

def currentSkeletonMethodCheck(name):
    return chooserStateCheck('OOF3D:Skeleton Page:Pane:Modification:Method:Chooser', name)
    
def skeletonMethodTargetsListCheck(method, *names):
    return chooserCheck('OOF3D:Skeleton Page:Pane:Modification:Method:'+method+':targets:Chooser', names)

def currentSkeletonMethodTargetsCheck(method, name):
    return chooserStateCheck('OOF3D:Skeleton Page:Pane:Modification:Method:'+method+':targets:Chooser', name)
    
def skeletonMethodTargetsListChooseFromCheck(method, target, *names):
    return chooserCheck('OOF3D:Skeleton Page:Pane:Modification:Method:'+method+':targets:'+target+':choose_from:Chooser', names)

def currentSkeletonMethodTargetsChooseFromCheck(method, target, name):
    return chooserStateCheck('OOF3D:Skeleton Page:Pane:Modification:Method:'+method+':targets:'+target+':choose_from:Chooser', name)

def skeletonMethodCriterionListCheck(method, *names):
    return chooserCheck('OOF3D:Skeleton Page:Pane:Modification:Method:'+method+':criterion:Chooser', names)
    
def currentSkeletonMethodCriterionCheck(method, name):
    return chooserStateCheck('OOF3D:Skeleton Page:Pane:Modification:Method:'+method+':criterion:Chooser', name)

def skeletonMethodCriterionUnitListCheck(method, criterion, *names):
    return chooserCheck('OOF3D:Skeleton Page:Pane:Modification:Method:'+method+':criterion:'+criterion+':units', names)

def currentSkeletonMethodCriterionUnitCheck(method, criterion, name):
    return chooserStateCheck('OOF3D:Skeleton Page:Pane:Modification:Method:'+method+':criterion:'+criterion+':units', name)

def skeletonMethodIterationListCheck(method, *names):
    return chooserCheck('OOF3D:Skeleton Page:Pane:Modification:Method:'+method+':iteration:Chooser', names)

def currentSkeletonMethodIterationCheck(method, name):
    return chooserStateCheck('OOF3D:Skeleton Page:Pane:Modification:Method:'+method+':iteration:Chooser', name)
    
def skeletonMethodIterationConditionListCheck(method, iteration, *names):
    return chooserCheck('OOF3D:Skeleton Page:Pane:Modification:Method:'+method+':iteration:'+iteration+':condition:Chooser', names)

def currentSkeletonMethodIterationConditionCheck(method, iteration, name):
    return chooserStateCheck('OOF3D:Skeleton Page:Pane:Modification:Method:'+method+':iteration:'+iteration+':condition:Chooser', name)

def skeletonPageModificationSensitivityCheck0():
    return sensitizationCheck({ 'Pane:Modification:Method':1,
				'Pane:Modification:Prev':0,
				'Pane:Modification:OK':0,
				'Pane:Modification:Next':0,
				'Pane:Modification:Undo':0,
				'Pane:Modification:Redo':0
				},
			       base='OOF3D:Skeleton Page')
       
def skeletonPageModificationSensitivityCheck1():
    return sensitizationCheck({ 'Pane:Modification:Method':1,
				'Pane:Modification:Prev':0,
				'Pane:Modification:OK':1,
				'Pane:Modification:Next':0,
				'Pane:Modification:Undo':0,
				'Pane:Modification:Redo':0
				},
			       base='OOF3D:Skeleton Page')

def skeletonPageModificationSensitivityCheck2():
    return sensitizationCheck({ 'Pane:Modification:Method':1,
				'Pane:Modification:Prev':1,
				'Pane:Modification:OK':1,
				'Pane:Modification:Next':0,
				'Pane:Modification:Undo':1,
				'Pane:Modification:Redo':0
				},
			       base='OOF3D:Skeleton Page')
			       
def skeletonPageModificationSensitivityCheck3():
    return sensitizationCheck({ 'Pane:Modification:Method':1,
				'Pane:Modification:Prev':1,
				'Pane:Modification:OK':1,
				'Pane:Modification:Next':0,
				'Pane:Modification:Undo':0,
				'Pane:Modification:Redo':1
				},
			       base='OOF3D:Skeleton Page')

def skeletonPageModificationSensitivityCheck4():
    return sensitizationCheck({ 'Pane:Modification:Method':1,
				'Pane:Modification:Prev':0,
				'Pane:Modification:OK':1,
				'Pane:Modification:Next':1,
				'Pane:Modification:Undo':0,
				'Pane:Modification:Redo':1
				},
			       base='OOF3D:Skeleton Page')
			      
def skeletonPageModificationSensitivityCheck5():
    return sensitizationCheck({ 'Pane:Modification:Method':1,
				'Pane:Modification:Prev':0,
				'Pane:Modification:OK':1,
				'Pane:Modification:Next':1,
				'Pane:Modification:Undo':1,
				'Pane:Modification:Redo':0
				},
			       base='OOF3D:Skeleton Page')

def skeletonPageModificationSensitivityCheck6():
    return sensitizationCheck({ 'Pane:Modification:Method':1,
				'Pane:Modification:Prev':0,
				'Pane:Modification:OK':1,
				'Pane:Modification:Next':0,
				'Pane:Modification:Undo':1,
				'Pane:Modification:Redo':0
				},
			       base='OOF3D:Skeleton Page')

def skeletonPageModificationSensitivityCheck7():
    return sensitizationCheck({ 'Pane:Modification:Method':1,
				'Pane:Modification:Prev':0,
				'Pane:Modification:OK':1,
				'Pane:Modification:Next':0,
				'Pane:Modification:Undo':0,
				'Pane:Modification:Redo':1
				},
			       base='OOF3D:Skeleton Page')

def skeletonPageModificationSensitivityCheck8():
    return sensitizationCheck({ 'Pane:Modification:Method':1,
				'Pane:Modification:Prev':1,
				'Pane:Modification:OK':1,
				'Pane:Modification:Next':1,
				'Pane:Modification:Undo':1,
				'Pane:Modification:Redo':0
				},
			       base='OOF3D:Skeleton Page')

def skeletonPageModificationSensitivityCheck9():
    return sensitizationCheck({ 'Pane:Modification:Method':1,
				'Pane:Modification:Prev':1,
				'Pane:Modification:OK':1,
				'Pane:Modification:Next':1,
				'Pane:Modification:Undo':0,
				'Pane:Modification:Redo':1
				},
			       base='OOF3D:Skeleton Page')

def skeletonPageModificationSensitivityCheck9b():
    return sensitizationCheck({ 'Pane:Modification:Method':1,
				'Pane:Modification:Prev':1,
				'Pane:Modification:OK':0,
				'Pane:Modification:Next':1,
				'Pane:Modification:Undo':0,
				'Pane:Modification:Redo':1
				},
			       base='OOF3D:Skeleton Page')

def skeletonPageModificationSensitivityCheck10():
    return sensitizationCheck({ 'Pane:Modification:Method':1,
				'Pane:Modification:Prev':0,
				'Pane:Modification:OK':1,
				'Pane:Modification:Next':1,
				'Pane:Modification:Undo':1,
				'Pane:Modification:Redo':1
				},
			       base='OOF3D:Skeleton Page')
			       
def skeletonPageModificationSensitivityCheck11():
    return sensitizationCheck({ 'Pane:Modification:Method':1,
				'Pane:Modification:Prev':1,
				'Pane:Modification:OK':1,
				'Pane:Modification:Next':0,
				'Pane:Modification:Undo':1,
				'Pane:Modification:Redo':1
				},
			       base='OOF3D:Skeleton Page')
			       
def skeletonPageModificationSensitivityCheck12():
    return sensitizationCheck({ 'Pane:Modification:Method':1,
				'Pane:Modification:Prev':1,
				'Pane:Modification:OK':1,
				'Pane:Modification:Next':1,
				'Pane:Modification:Undo':1,
				'Pane:Modification:Redo':1
				},
			       base='OOF3D:Skeleton Page')