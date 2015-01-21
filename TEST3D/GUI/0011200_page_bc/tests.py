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


def sensitization0():
    return (sensitizationCheck({"New" : 0,
                                "Edit" : 0,
                                "Rename" : 0,
                                "Copy" : 0,
                                "CopyAll" : 0,
                                "Delete" : 0},
                               base="OOF3D:Boundary Conditions Page:Condition"))
                                                              
def sensitization1():
    return (sensitizationCheck({"New" : 1,
                                "Edit" : 0,
                                "Rename" : 0,
                                "Copy" : 0,
                                "CopyAll" : 0,
                                "Delete" : 0},
                               base="OOF3D:Boundary Conditions Page:Condition"))
                               
def sensitization2():
    return (sensitizationCheck({"New" : 1,
                                "Edit" : 1,
                                "Rename" : 1,
                                "Copy" : 1,
                                "CopyAll" : 1,
                                "Delete" : 1},
                               base="OOF3D:Boundary Conditions Page:Condition"))
                               
def sensitization3():
    return (sensitizationCheck({"New" : 1,
                                "Edit" : 0,
                                "Rename" : 0,
                                "Copy" : 0,
                                "CopyAll" : 1,
                                "Delete" : 0},
                               base="OOF3D:Boundary Conditions Page:Condition"))
                               
def ConditionNewDialogCheck0():
    okbutton = gtklogger.findWidget('Dialog-New Boundary Condition:gtk-ok')
    return ((okbutton.get_property('sensitive') == True) and
           chooserCheck('Dialog-New Boundary Condition:condition:Chooser', ('Dirichlet','Generalized Force', 'Floating', 'Neumann',)) and
           chooserCheck('Dialog-New Boundary Condition:condition:Dirichlet:profile:Chooser', ('Constant Profile','Continuum Profile',)) and
           chooserCheck('Dialog-New Boundary Condition:condition:Dirichlet:boundary', ('Xmax','Xmin','Ymax','Ymin','Zmax','Zmin','----------','XmaxYmax','XmaxYmin','XmaxZmax','XmaxZmin','XminYmax','XminYmin','XminZmax','XminZmin','YmaxZmax','YmaxZmin','YminZmax','YminZmin','----------','XmaxYmaxZmax','XmaxYmaxZmin','XmaxYminZmax','XmaxYminZmin','XminYmaxZmax','XminYmaxZmin','XminYminZmax','XminYminZmin',)))
           
          
def ConditionEditDialogCheck0():
    okbutton = gtklogger.findWidget('Dialog-Edit Boundary Condition:gtk-ok')
    return ((okbutton.get_property('sensitive') == True) and
           chooserCheck('Dialog-Edit Boundary Condition:condition:Chooser', ('Dirichlet','Generalized Force', 'Floating', 'Neumann',)) and
           chooserCheck('Dialog-Edit Boundary Condition:condition:Dirichlet:profile:Chooser', ('Constant Profile','Continuum Profile',)) and
           chooserCheck('Dialog-Edit Boundary Condition:condition:Dirichlet:boundary', ('Xmax','Xmin','Ymax','Ymin','Zmax','Zmin','----------','XmaxYmax','XmaxYmin','XmaxZmax','XmaxZmin','XminYmax','XminYmin','XminZmax','XminZmin','YmaxZmax','YmaxZmin','YminZmax','YminZmin','----------','XmaxYmaxZmax','XmaxYmaxZmin','XmaxYminZmax','XmaxYminZmin','XminYmaxZmax','XminYmaxZmin','XminYminZmax','XminYminZmin',)))

def ConditionCopyDialogCheck0():
    okbutton = gtklogger.findWidget('Dialog-Choose a name and boundary.:gtk-ok')
    return ((okbutton.get_property('sensitive') == True) and
           chooserCheck('Dialog-Choose a name and boundary.:mesh:Microstructure', ('two_walls',)) and
           chooserCheck('Dialog-Choose a name and boundary.:mesh:Skeleton', ('skeleton',)) and
	   chooserCheck('Dialog-Choose a name and boundary.:mesh:Mesh', ('mesh','mesh<2>',)) and
           chooserCheck('Dialog-Choose a name and boundary.:boundary', ('Xmax','Xmin','Ymax','Ymin','Zmax','Zmin','----------','XmaxYmax','XmaxYmin','XmaxZmax','XmaxZmin','XminYmax','XminYmin','XminZmax','XminZmin','YmaxZmax','YmaxZmin','YminZmax','YminZmin','----------','XmaxYmaxZmax','XmaxYmaxZmin','XmaxYminZmax','XmaxYminZmin','XminYmaxZmax','XminYmaxZmin','XminYminZmax','XminYminZmin',)))
           
def ConditionCopyAllDialogCheck0():
    okbutton = gtklogger.findWidget('Dialog-Choose the target mesh.:gtk-ok')
    return ((okbutton.get_property('sensitive') == True) and
           chooserCheck('Dialog-Choose the target mesh.:mesh:Microstructure', ('two_walls',)) and
           chooserCheck('Dialog-Choose the target mesh.:mesh:Skeleton', ('skeleton',)) and
	   chooserCheck('Dialog-Choose the target mesh.:mesh:Mesh', ('mesh','mesh<2>',)))
          
