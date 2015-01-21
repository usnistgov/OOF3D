# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:11:39 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

from generics import *

def sensitization0():
    return (sensitizationCheck({"Temperature defined" : 0,
                                "Temperature active" : 0,
                                "Temperature in-plane" : 0,
                                "Displacement defined" : 0,
                                "Displacement active" : 0,
                                "Displacement in-plane" : 0,
                                "Voltage defined" : 0,
                                "Voltage active" : 0,
                                "Voltage in-plane" : 0},
                               base="OOF2:Fields & Equations Page:HPane:Fields")
            and
            sensitizationCheck({"Heat_Eqn active" : 0,
                                "Plane_Heat_Flux active" : 0,
                                "Force_Balance active" : 0,
                                "Plane_Stress active" : 0,
                                "Coulomb_Eqn active" : 0,
                                "InPlanePolarization active" : 0},
                               base="OOF2:Fields & Equations Page:HPane:Equations")
            and
            sensitizationCheck({"CopyField" : 0,
                                "CopyEquation" : 0},
                               base="OOF2:Fields & Equations Page:HPane"))

def sensitization1():
    return (sensitizationCheck({"Temperature defined" : 1,
                                "Temperature active" : 0,
                                "Temperature in-plane" : 0,
                                "Displacement defined" : 1,
                                "Displacement active" : 0,
                                "Displacement in-plane" : 0,
                                "Voltage defined" : 1,
                                "Voltage active" : 0,
                                "Voltage in-plane" : 0},
                               base="OOF2:Fields & Equations Page:HPane:Fields")
            and
            sensitizationCheck({"Heat_Eqn active" : 1,
                                "Plane_Heat_Flux active" : 1,
                                "Force_Balance active" : 1,
                                "Plane_Stress active" : 1,
                                "Coulomb_Eqn active" : 1,
                                "InPlanePolarization active" : 1},
                               base="OOF2:Fields & Equations Page:HPane:Equations")
            and
            sensitizationCheck({"CopyField" : 1,
                                "CopyEquation" : 1},
                               base="OOF2:Fields & Equations Page:HPane"))

def sensitization2():
    return (sensitizationCheck({"Temperature defined" : 1,
                                "Temperature active" : 1,
                                "Temperature in-plane" : 1,
                                "Displacement defined" : 1,
                                "Displacement active" : 0,
                                "Displacement in-plane" : 0,
                                "Voltage defined" : 1,
                                "Voltage active" : 0,
                                "Voltage in-plane" : 0},
                               base="OOF2:Fields & Equations Page:HPane:Fields")
            and
            sensitizationCheck({"Heat_Eqn active" : 1,
                                "Plane_Heat_Flux active" : 1,
                                "Force_Balance active" : 1,
                                "Plane_Stress active" : 1,
                                "Coulomb_Eqn active" : 1,
                                "InPlanePolarization active" : 1},
                               base="OOF2:Fields & Equations Page:HPane:Equations")
            and
            sensitizationCheck({"CopyField" : 1,
                                "CopyEquation" : 1},
                               base="OOF2:Fields & Equations Page:HPane"))

def sensitization3():
    return (sensitizationCheck({"Temperature defined" : 1,
                                "Temperature active" : 1,
                                "Temperature in-plane" : 1,
                                "Displacement defined" : 1,
                                "Displacement active" : 1,
                                "Displacement in-plane" : 1,
                                "Voltage defined" : 1,
                                "Voltage active" : 0,
                                "Voltage in-plane" : 0},
                               base="OOF2:Fields & Equations Page:HPane:Fields")
            and
            sensitizationCheck({"Heat_Eqn active" : 1,
                                "Plane_Heat_Flux active" : 1,
                                "Force_Balance active" : 1,
                                "Plane_Stress active" : 1,
                                "Coulomb_Eqn active" : 1,
                                "InPlanePolarization active" : 1},
                               base="OOF2:Fields & Equations Page:HPane:Equations")
            and
            sensitizationCheck({"CopyField" : 1,
                                "CopyEquation" : 1},
                               base="OOF2:Fields & Equations Page:HPane"))

def sensitization4():
    return (sensitizationCheck({"Temperature defined" : 1,
                                "Temperature active" : 0,
                                "Temperature in-plane" : 0,
                                "Displacement defined" : 1,
                                "Displacement active" : 1,
                                "Displacement in-plane" : 1,
                                "Voltage defined" : 1,
                                "Voltage active" : 0,
                                "Voltage in-plane" : 0},
                               base="OOF2:Fields & Equations Page:HPane:Fields")
            and
            sensitizationCheck({"Heat_Eqn active" : 1,
                                "Plane_Heat_Flux active" : 1,
                                "Force_Balance active" : 1,
                                "Plane_Stress active" : 1,
                                "Coulomb_Eqn active" : 1,
                                "InPlanePolarization active" : 1},
                               base="OOF2:Fields & Equations Page:HPane:Equations")
            and
            sensitizationCheck({"CopyField" : 1,
                                "CopyEquation" : 1},
                               base="OOF2:Fields & Equations Page:HPane"))


def fieldButtonCheck(defined, active, inplane):
    b1=gtklogger.findWidget('OOF2:Fields & Equations Page:HPane:Fields:Temperature defined')
    b2=gtklogger.findWidget('OOF2:Fields & Equations Page:HPane:Fields:Temperature active')
    b3=gtklogger.findWidget('OOF2:Fields & Equations Page:HPane:Fields:Temperature in-plane')
    return b1.get_active()==defined and b2.get_active()==active and b3.get_active()==inplane

def eqnButtonCheck(active):
    return (gtklogger.findWidget('OOF2:Fields & Equations Page:HPane:Equations:Heat_Eqn active').get_active()
            == active)

# def fieldListCheck(*fieldnames):
#     from ooflib.SWIG.engine import field
#     return treeViewColCheck('OOF2:Fields & Equations Page:Pane:InitScroll:Initializers',
#                             0,  map(field.getCompoundField, fieldnames))
