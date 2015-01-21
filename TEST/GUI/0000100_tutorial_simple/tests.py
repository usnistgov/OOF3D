# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:10:18 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

from generics import *
from ooflib.common.IO.GUI import gtklogger
import sys

def _getMScontext():
    from ooflib.common.IO import whoville
    return whoville.getClass('Microstructure')['cyallow.png']

def checkGroupSizes():
    ms = _getMScontext().getObject()
    cyan = ms.findGroup('RGBColor(red=0.00000,green=1.00000,blue=1.00000)')
    yellow = ms.findGroup('RGBColor(red=1.00000,green=1.00000,blue=0.00000)')
    return ms.nGroups() == 2 and len(cyan) == 2160 and len(yellow) == 1440

def checkNewGroupNames():
    ms = _getMScontext().getObject()
    cyan = ms.findGroup('cyan')
    yellow = ms.findGroup('yellow')
    godot = ms.findGroup('harvey')
    return cyan is not None and yellow is not None and godot is None

def matlPageSensitizationCheck0():
    # initial sensitization of the materials page
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
        base='OOF2:Materials Page:Pane')

def matlPageSensitizationCheck1():
    # sensitization after a material has been created
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
        base='OOF2:Materials Page:Pane')

def matlPageSensitizationCheck2():
    # sensitization after a material has been created and a built-in
    # property selected, but not added to the material
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
        base='OOF2:Materials Page:Pane')

def matlPageSensitizationCheck3():
    # sensitization after a material has been created and a built-in
    # property selected and copied, but not added to the material
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
        base='OOF2:Materials Page:Pane')

def matlPageSensitizationCheck4():
    # sensitization after a material has been created, and a built-in
    # property selected, copied, and added to the material.
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
        base='OOF2:Materials Page:Pane')

def selectedPropertyCheck(propertypath):
    # Check that the given Property is selected in the Property Pane.
    from ooflib.engine.IO.GUI import materialsPage
    propertyTree = materialsPage.materialspage.propertypane.propertytree
    prop = propertyTree.tree[propertypath]

    treeview = gtklogger.findWidget(
        'OOF2:Materials Page:Pane:Property:PropertyScroll:PropertyTree')
    selection = treeview.get_selection()
    model, iter = selection.get_selected()
    return model[iter][1] is prop

def materialCheck(materialname, propertypaths):
    # Check that given Material contains the given Properties.
    from ooflib.engine import materialmanager
    from ooflib.engine import propertyregistration
    matl = materialmanager.getMaterial(materialname)
    regs = [prop.registration() for prop in matl.properties()]
    if len(propertypaths) != len(regs):
        return False
    for path in propertypaths:
        if propertyregistration.AllProperties[path] not in regs:
            print >> sys.stderr, "Property", path, "not found in", materialname
            return False
    return True
    
def selectedMatlPropertyCheck(propertypath):
    # Check that the given Property is selected in the list of
    # Properties in the Material Pane.  propertypath should be None if
    # no Property is selected.
    matproplist = gtklogger.findWidget(
        'OOF2:Materials Page:Pane:Material:PropertyListScroll:PropertyList')
    selection = matproplist.get_selection()
    model, iter = selection.get_selected()
    if not iter and propertypath is None:
        return True
    if model[iter][0] == propertypath:
        return True
    print "Selected property is %s. Expected %s." \
          % (model[iter][0], propertypath)
    return False

def layerEditorSensitivityCheck0():
    # initial state of the Layer Editor, set to Nothing/Nobody
    return sensitizationCheck(
        {
        'ObjectScroll:category' : 1,
        'ObjectScroll:object:Nothing' : 1,
        'DisplayMethods:New' : 0,
        'DisplayMethods:Edit' : 0,
        'DisplayMethods:Copy' : 0,
        'DisplayMethods:Delete' : 0,
        'NewLayer' : 1,
        'Destination' : 1,
        'Send' : 0
        },
        base='OOF2 Graphics Layer Editor')
    
def layerEditorSensitivityCheck1():
    # layer editor with a Microstructure selected, but no display methods
    return sensitizationCheck(
        {
        'ObjectScroll:category' : 1,
        'ObjectScroll:object:Microstructure' : 1,
        'DisplayMethods:New' : 1,
        'DisplayMethods:Edit' : 0,
        'DisplayMethods:Copy' : 0,
        'DisplayMethods:Delete' : 0,
        'NewLayer' : 1,
        'Destination' : 1,
        'Send' : 0
        },
        base='OOF2 Graphics Layer Editor')
    
def layerEditorSensitivityCheck2():
    # layer editor with a Microstructure selected and some layers in the list
    return sensitizationCheck(
        {
        'ObjectScroll:category' : 1,
        'ObjectScroll:object:Microstructure' : 1,
        'DisplayMethods:New' : 1,
        'DisplayMethods:Edit' : 1,
        'DisplayMethods:Copy' : 1,
        'DisplayMethods:Delete' : 1,
        'NewLayer' : 1,
        'Destination' : 1,
        'Send' : 1
        },
        base='OOF2 Graphics Layer Editor')
    
def skeletonPageSensitivityCheck0():
    # skeleton page with a Microstructure defined but no Skeleton
    return sensitizationCheck(
        {
        'Microstructure' : 1,
        'Skeleton' : 0,
        'New' : 1,
        'Simple' : 1,
        'Rename' : 0,
        'Copy' : 0,
        'Delete' : 0,
        'Save' : 0,
        },
        base='OOF2:Skeleton Page') and \
        sensitizationCheck(
        {
        'Method:Chooser' : 1,
        'OK' : 0,
        'Prev' : 0,
        'Next' : 0,
        'Undo' : 0,
        'Redo' : 0
        },
        base='OOF2:Skeleton Page:Pane:Modification')

def skeletonPageSensitivityCheck1():
    # skeleton page with a Microstructure and a Skeleton selected
    return sensitizationCheck(
        {
        'Microstructure' : 1,
        'Skeleton' : 1,
        'New' : 1,
        'Simple' : 1,
        'Rename' : 1,
        'Copy' : 1,
        'Delete' : 1,
        'Save' : 1,
        },
        base='OOF2:Skeleton Page') and \
        sensitizationCheck(
        {
        'Method:Chooser' : 1,
        'OK' : 1,
        'Prev' : 0,
        'Next' : 0,
        'Undo' : 0,
        'Redo' : 0
        },
        base='OOF2:Skeleton Page:Pane:Modification')

def skeletonPageSensitivityCheck2():
    # after modifying the skeleton the first time
    return sensitizationCheck(
        {
        'Microstructure' : 1,
        'Skeleton' : 1,
        'New' : 1,
        'Simple' : 1,
        'Rename' : 1,
        'Copy' : 1,
        'Delete' : 1,
        'Save' : 1,
        },
        base='OOF2:Skeleton Page') and \
        sensitizationCheck(
        {
        'Method:Chooser' : 1,
        'OK' : 1,
        'Prev' : 0,
        'Next' : 0,
        'Undo' : 1,
        'Redo' : 0
        },
        base='OOF2:Skeleton Page:Pane:Modification')

def meshPageSensitivityCheck0():
    # Skeleton, but no Mesh yet.
    return sensitizationCheck(
        {
        'Microstructure' : 1,
        'Skeleton' : 1,
        'Mesh' : 0,
        'New' : 1,
        'Rename' : 0,
        'Copy' : 0,
        'Delete' : 0,
        'Save' : 0,
        'Pane:ElementOps:Method:Chooser' : 1,
        'Pane:ElementOps:Prev' : 0,
        'Pane:ElementOps:OK' : 0,
        'Pane:ElementOps:Next' : 0
        },
        base='OOF2:FE Mesh Page')

def meshPageSensitivityCheck1():
    # After creating a Mesh.
    return sensitizationCheck(
        {
        'Microstructure' : 1,
        'Skeleton' : 1,
        'Mesh' : 1,
        'New' : 1,
        'Rename' : 1,
        'Copy' : 1,
        'Delete' : 1,
        'Save' : 1,
        'Pane:ElementOps:Method:Chooser' : 1,
        'Pane:ElementOps:Prev' : 0,
        'Pane:ElementOps:OK' : 1,
        'Pane:ElementOps:Next' : 0
        },
        base='OOF2:FE Mesh Page')

def fieldPageSensitivityCheck0():
    return sensitizationCheck(
        {
        'Microstructure' : 1,
        'Skeleton' : 1,
        'Mesh' : 1,
        },
        base='OOF2:Fields & Equations Page') and \
        sensitizationCheck(
        {
        'Temperature defined' : 1,
        'Temperature active' : 0,
        'Temperature in-plane' : 0,
        'Displacement defined' : 1,
        'Displacement active' : 0,
        'Displacement in-plane' : 0,
        },
        base='OOF2:Fields & Equations Page:HPane:Fields')

def fieldPageSensitivityCheck1():
    # after defining temperature
    return sensitizationCheck(
        {
        'Microstructure' : 1,
        'Skeleton' : 1,
        'Mesh' : 1,
        },
        base='OOF2:Fields & Equations Page') and \
        sensitizationCheck(
        {
        'Temperature defined' : 1,
        'Temperature active' : 0,
        'Temperature in-plane' : 0,
        'Displacement defined' : 1,
        'Displacement active' : 1,
        'Displacement in-plane' : 1,
        },
        base='OOF2:Fields & Equations Page:HPane:Fields')

def bcPageSensitivityCheck0():
    return sensitizationCheck(
        {
        'Microstructure' : 1,
        'Skeleton' : 1,
        'Mesh' : 1
        },
        base='OOF2:Boundary Conditions Page') and \
        sensitizationCheck(
        {
        'New' : 1,
        'Rename' : 0,
        'Edit' : 0,
        'Copy' : 0,
        'Save' : 0,
        'Delete' : 0
        },
        base='OOF2:Boundary Conditions Page:Pane:Profile') and \
        sensitizationCheck(
        {
        'New' : 1,
        'Rename' : 0,
        'Edit' : 0,
        'Copy' : 0,
        'CopyAll' : 0,
        'Delete' : 0
        },
        base='OOF2:Boundary Conditions Page:Pane:Condition')
    
def bcPageSensitivityCheck1():
    # after defining a BC
    return sensitizationCheck(
        {
        'Microstructure' : 1,
        'Skeleton' : 1,
        'Mesh' : 1
        },
        base='OOF2:Boundary Conditions Page') and \
        sensitizationCheck(
        {
        'New' : 1,
        'Rename' : 0,
        'Edit' : 0,
        'Copy' : 0,
        'Save' : 0,
        'Delete' : 0
        },
        base='OOF2:Boundary Conditions Page:Pane:Profile') and \
        sensitizationCheck(
        {
        'New' : 1,
        'Rename' : 1,
        'Edit' : 1,
        'Copy' : 1,
        'CopyAll' : 1,
        'Delete' : 1
        },
        base='OOF2:Boundary Conditions Page:Pane:Condition')
