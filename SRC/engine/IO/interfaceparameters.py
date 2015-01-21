# -*- python -*-
# $RCSfile: interfaceparameters.py,v $
# $Revision: 1.6.2.2 $
# $Author: fyc $
# $Date: 2014/07/28 22:16:53 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.common import enum
from ooflib.common import utils
from ooflib.common.IO import parameter
import types

#Might be able to combine the material type and compatibilty
#if we can imagine a material that accepts both bulk and interface
#types.

#These are used in PropertyRegistration.

class MatPropCompatibilityType(enum.EnumClass(
    ('bulk_only', 'The property can only be assigned to bulk materials.'),
    ('interface_only', 'The property can only be assigned to interface materials.'),
    ('bulk_interface', 'The property can be assigned to either bulk or interface materials.')
    )):
    tip = "Compatibility of &oof2; properties to &oof2; materials."
    discussion = """<para>
    
    Certain properties can only be assigned to certain types of materials.
    
    </para>"""

utils.OOFdefine('MatPropCompatibilityType', MatPropCompatibilityType)

COMPATIBILITY_BULK_ONLY = MatPropCompatibilityType('bulk_only')
COMPATIBILITY_INTERFACE_ONLY = MatPropCompatibilityType('interface_only')
COMPATIBILITY_BULK_INTERFACE = MatPropCompatibilityType('bulk_interface')

NO_MATERIAL_STR="<No material>"
NO_PIXELGROUP_STR="<No pixelgroup>"
NORTH_STR="<North>"
SOUTH_STR="<South>"
EAST_STR="<East>"
WEST_STR="<West>"
ANY_STR="<Any>"

class InterfacesParameter(parameter.StringParameter):
    def checker(self, x):
        #TODO 3.1:
        pass
class ListOfInterfacesParameter(parameter.ListOfStringsParameter):
    def checker(self, x):
        if type(x) is not types.ListType:
            raise TypeError("Expected a list of interfaces!")
        #TODO 3.1: More checking.
class ListOfInterfacesWithMaterialParameter(parameter.ListOfStringsParameter):
    def checker(self, x):
        if type(x) is not types.ListType:
            raise TypeError("Expected a list of interfaces!")
        #TODO 3.1: More checking.
#This parameter should present interface names and skeleton boundary names
#(prefixed with "skeletonname:")
class ListOfInterfacesSkelBdyParameter(parameter.ListOfStringsParameter):
    def checker(self, x):
        if type(x) is not types.ListType:
            raise TypeError("Expected a list of interfaces and skeleton boundaries!")
        #TODO 3.1: More checking.
class ListOfInterfacesSkelBdyWithMaterialParameter(parameter.ListOfStringsParameter):
    def checker(self, x):
        if type(x) is not types.ListType:
            raise TypeError("Expected a list of interfaces and skeleton boundaries!")
        #TODO 3.1: More checking.

class SkelAllParameter(parameter.StringParameter):
    extranames=['<All>']
    def checker(self, x):
        #TODO 3.1:
        pass
class ListOfInterfacesCombinedBdysParameter(parameter.ListOfStringsParameter):
    def checker(self, x):
        if type(x) is not types.ListType:
            raise TypeError("Expected a list of interfaces and skeleton boundaries!")
        #TODO 3.1: More checking.
