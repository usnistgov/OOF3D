# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.2 $
# $Author: fyc $
# $Date: 2013/08/27 17:36:30 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from generics import *

removefile('material.dat')

def sensitization2():
    return sensitizationCheck(
        {'Property:Copy' : 0,
         'Property:Parametrize' : 0,
         'Property:Delete': 0,
         'Property:Add' : 0,
         'Material:New' : 1,
         'Material:Rename' : 0,
         'Material:Copy' : 0,
         'Material:Delete' : 0,
         'Material:Save' : 0,
         'Material:RemoveProperty' : 0,
         'Material:Assign' : 0,
         'Material:RemoveMaterial' : 1,
         'Material:MaterialList' : 0
        },
        base='OOF3D:Materials Page:Pane')

def sensitization3():
    return sensitizationCheck(
        {'Property:Copy' : 0,
         'Property:Parametrize' : 0,
         'Property:Delete': 0,
         'Property:Add' : 0,
         'Material:New' : 1,
         'Material:Rename' : 1,
         'Material:Copy' : 1,
         'Material:Delete' : 1,
         'Material:Save' : 1,
         'Material:RemoveProperty' : 0,
         'Material:Assign' : 1,
         'Material:RemoveMaterial' : 1,
         'Material:MaterialList' : 1
        },
        base='OOF3D:Materials Page:Pane')

def sensitization4():
    return sensitizationCheck(
        {'Property:Copy' : 1,
         'Property:Parametrize' : 1,
         'Property:Delete': 1,
         'Property:Add' : 1,
         'Material:New' : 1,
         'Material:Rename' : 1,
         'Material:Copy' : 1,
         'Material:Delete' : 1,
         'Material:Save' : 1,
         'Material:RemoveProperty' : 1,
         'Material:Assign' : 1,
         'Material:RemoveMaterial' : 1,
         'Material:MaterialList' : 1
        },
        base='OOF3D:Materials Page:Pane')

def sensitization5():
    return sensitizationCheck(
        {'Property:Copy' : 1,
         'Property:Parametrize' : 1,
         'Property:Delete': 0,
         'Property:Add' : 1,
         'Material:New' : 1,
         'Material:Rename' : 1,
         'Material:Copy' : 1,
         'Material:Delete' : 1,
         'Material:Save' : 1,
         'Material:RemoveProperty' : 1,
         'Material:Assign' : 1,
         'Material:RemoveMaterial' : 1,
         'Material:MaterialList' : 1
        },
        base='OOF3D:Materials Page:Pane')

def sensitization6():
    return sensitizationCheck(
        {'Property:Copy' : 1,
         'Property:Parametrize' : 1,
         'Property:Delete': 0,
         'Property:Add' : 1,
         'Material:New' : 1,
         'Material:Rename' : 1,
         'Material:Copy' : 1,
         'Material:Delete' : 1,
         'Material:Save' : 1,
         'Material:RemoveProperty' : 0,
         'Material:Assign' : 1,
         'Material:RemoveMaterial' : 1,
         'Material:MaterialList' : 1
        },
        base='OOF3D:Materials Page:Pane')

def sensitization0():
    return sensitizationCheck(
        {'Property:Copy' : 1,
         'Property:Parametrize' : 1,
         'Property:Delete': 1,
         'Property:Add' : 1,
         'Material:New' : 1,
         'Material:Rename' : 1,
         'Material:Copy' : 1,
         'Material:Delete' : 1,
         'Material:Save' : 1,
         'Material:RemoveProperty' : 0,
         'Material:Assign' : 1,
         'Material:RemoveMaterial' : 1,
         'Material:MaterialList' : 1
        },
        base='OOF3D:Materials Page:Pane')

def sensitization1():
    return sensitizationCheck(
        {'Property:Copy' : 1,
         'Property:Parametrize' : 1,
         'Property:Delete': 1,
         'Property:Add' : 0,
         'Material:New' : 1,
         'Material:Rename' : 0,
         'Material:Copy' : 0,
         'Material:Delete' : 0,
         'Material:Save' : 0,
         'Material:RemoveProperty' : 0,
         'Material:Assign' : 0,
         'Material:RemoveMaterial' : 1,
         'Material:MaterialList' : 0
        },
        base='OOF3D:Materials Page:Pane')

def propertyTreeCheck(proppath):
    treeview = gtklogger.findWidget(
        'OOF3D:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
    selection = treeview.get_selection()
    model, iter = selection.get_selected()
    if iter is None:
        return proppath is None
    labeltreenode = model[iter][1]
    result = labeltreenode.path() == proppath
    if not result:
        print >> sys.stderr, "found", labeltreenode.path(), "expected", proppath
    return result

def materialListCheck(*names):
    return chooserCheck('OOF3D:Materials Page:Pane:Material:MaterialList', names)

def currentMaterialCheck(name):
    return chooserStateCheck('OOF3D:Materials Page:Pane:Material:MaterialList',
                             name)

def materialPropertyListCheck(*props):
    return chooserCheck(
        'OOF3D:Materials Page:Pane:Material:PropertyListScroll:PropertyList',
        props)

def materialPropertyCheck(name):
    if name:
        return chooserListStateCheck(
            'OOF3D:Materials Page:Pane:Material:PropertyListScroll:PropertyList',
            [name])
    return chooserListStateCheck(
            'OOF3D:Materials Page:Pane:Material:PropertyListScroll:PropertyList',
            [])
    
def currentMaterialPropertyCheck(name):
    return propertyTreeCheck(name) and materialPropertyCheck(name)

def checkTBMaterial(name='<No material>'):
    entry = gtklogger.findWidget(
        'OOF3D Graphics 1:Pane0:Pane2:ToolboxFrame:TBScroll:Voxel Info:material')
    return entry.get_text() == name
