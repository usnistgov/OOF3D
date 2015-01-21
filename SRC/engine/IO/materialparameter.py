# -*- python -*-
# $RCSfile: materialparameter.py,v $
# $Revision: 1.11.12.1 $
# $Author: langer $
# $Date: 2011/11/09 15:13:30 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.


from ooflib.common import debug
from ooflib.common.IO import parameter
from ooflib.engine import materialmanager
import types
#Interface branch
from ooflib.engine.IO import interfaceparameters

# MaterialParameter can be set to any existing Material name.

class MaterialParameter(parameter.StringParameter):
    def checker(self, x):
        if x not in materialmanager.getMaterialNames():
            raise TypeError("Expected a Material name!")

# AnyMaterialParameter can be set to any existing Material name, or
# '<Any>' or '<None>'.

class AnyMaterialParameter(parameter.StringParameter):
    extranames = ['<Any>', '<None>']
    def checker(self, x):
        if (x not in materialmanager.getMaterialNames() and
            x not in self.extranames):
            raise TypeError("Expected a Material name, or '<Any>' or '<None>'")

# ListOfMaterialsParameter can be set to a list of existing Material
# names.

class ListOfMaterialsParameter(parameter.ListOfStringsParameter):
    def checker(self, x):
        if type(x) is not types.ListType:
            raise TypeError("Expected a list of Material names!")
        names = materialmanager.getMaterialNames()
        for n in x:
            if n not in names:
                raise TypeError("Expected a list of Material names!")


# MeshMaterialParameter can be set to any Material that's used in a
# Mesh.  The Parameter class itself doesn't enforce this, but the
# associated Widget does.

class MeshMaterialParameter(MaterialParameter):
    pass

##########################################################################
# Interface branch
class InterfaceMaterialParameter(parameter.StringParameter):
    def checker(self, x):
        if x not in materialmanager.getInterfaceMaterialNames():
            raise TypeError("Expected an Interface Material name!")

#This one has "<Any>" and "<None>" included in the list of
#names of interface materials.
class InterfaceAnyMaterialParameter(parameter.StringParameter):
    extranames = ['<Any>', '<None>']
    def checker(self, x):
        if x not in materialmanager.getInterfaceMaterialNames() and \
               x not in self.extranames:
            raise TypeError("Expected an Interface Material name!")

#This one includes "<No material>" in the list
class BulkMaterialParameterExtra(parameter.StringParameter):
    extranames=[interfaceparameters.NO_MATERIAL_STR,
                interfaceparameters.ANY_STR,
                interfaceparameters.NORTH_STR,
                interfaceparameters.SOUTH_STR,
                interfaceparameters.EAST_STR,
                interfaceparameters.WEST_STR]
    def checker(self, x):
        #The checker gets called before the BulkMaterialWidget gets initialized
        #when the parameter is part of a registeredclass. Have to supress
        #the exception in this case when the material gets deleted.
        if x in materialmanager.getMaterialNames():
            if x not in materialmanager.getBulkMaterialNames():
                raise TypeError("Expected a Bulk Material name!")

class BulkMaterialParameter(parameter.StringParameter):
    def checker(self, x):
        #The checker gets called before the BulkMaterialWidget gets initialized
        #when the parameter is part of a registeredclass. Have to supress
        #the exception in this case when the material gets deleted.
        if x in materialmanager.getMaterialNames():
            if x not in materialmanager.getBulkMaterialNames():
                raise TypeError("Expected a Bulk Material name!")
