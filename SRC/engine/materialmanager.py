# -*- python -*-
# $RCSfile: materialmanager.py,v $
# $Revision: 1.60.2.5 $
# $Author: fyc $
# $Date: 2014/07/24 21:36:33 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.SWIG.common import config
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import pixelgroup
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.engine import material
from ooflib.common import debug
from ooflib.common import utils
from ooflib.common.IO import reporter
from ooflib.common import runtimeflags
from ooflib.common.microstructure import microStructures
from ooflib.engine.propertyregistration import AllProperties
import string
import sys

# "MaterialProps" is a collection of properties which make up a
# material.  It contains the actual material instance, which has
# within it actual property instances, suitable for importation into a
# mesh.

# Data entries are property-registration entries corresponding to
# nodes in the PropertyManager.

class MaterialProps:
    #Interface branch
    def __init__(self, name, materialtype):
        self.name = name
        self.data = {}
        self.actual = material.Material(name, materialtype)
    def __repr__(self):
        return "MaterialProps('%s')" % self.name
    
    # Detect name collisions, and check against existing props
    # for category collisions.
    # For starters, "key" is the fully qualified property name,
    # and "value" is the associated PropertyRegistration object.
    # Store a reference to a copy of the property instance.
    #
    # Materials do not own their properties, they have pointers to the
    # property instances, which live in the property registration
    # object's "materials" dictionary, indexed by material name.  The
    # registration updates these properties when the Property's
    # parameters change.  When materials are destroyed, these
    # properties must also be destroyed -- material manager calls the
    # delete_all_props routine below to accomplish this.
    def __setitem__(self, key, value):
        if key in self.data:
            raise KeyError("Collision in Material Property List, key %s."
                           % key)
        propcopy = value()          # instantiate Property from registration
        self.data[key]=value        # prop. registrations, keyed by path
        self.actual.addProperty(propcopy)
        value.add_material(self.name, (self, propcopy))

    # Add a propertyregistration entry to the dict without adding the
    # property to the "actual" Material.  Used when loading a material
    # from a script, in which case the material already has the
    # property.
    def add_prop_ref(self, key, value):
        self.data[key]=value
        switchboard.notify("prop_added_to_material", self.name, key)
        
    def __getitem__(self,key):
        return self.data[key]

    # Remove the named property from this material, if it occurs.
    # Property should *not* be current by this time.
    def delete_prop(self,name):
        try:
            reg = self.data[name]
        except KeyError:
            pass
        else:
            self.actual.removeProperty(reg.materials[self.name][1])
            switchboard.notify("prop_removed_from_material", self, name, reg)
            reg.remove_material(self.name)
            del self.data[name]

    # Called prior to material removal.  
    def delete_all_props(self):
        for (name, reg) in self.data.items():
            self.actual.removeProperty(reg.materials[self.name][1])
            reg.remove_material(self.name)
        self.data = {}

    def rename_material(self,newname,oldname):
        for reg in self.data.values():
            reg.rename_material(newname,oldname)

    # When a property gets new parameters, we need to update the
    # "actual" entry, but nothing else really changes.  "actual"
    # properties are Python-wrapped Property instances.
    def new_params(self, old_prop, new_prop):
        self.actual.removeProperty(old_prop)
        self.actual.addProperty(new_prop)

        
class MaterialManager:
    def __init__(self):
        self.materials={}       # dict of MaterialProps keyed by matl name
        self.secretmaterials = {} # ditto, for matls not listed in the UI

    # Useful for returning a material to a script.
    def __getitem__(self, name):
        try:
            return self.materials[name]
        except KeyError:
            return self.secretmaterials[name]
    
    # Delete this property from each material in which it occurs.
    # "Deletion" means it's been deleted from the property manager,
    # and all instances need to go. 
    def delete_prop(self,name):
        for m in self.materials.values()+self.secretmaterials.values():
            m.delete_prop(name)
            
    # Add a property to the named material.
    # This function does *not* send switchboard signals, because it's
    # used in situations in which the signal shouldn't be set (ie,
    # when copying a Material).  The Add_property menu item sends
    # signals instead.
    def add_prop(self, matname, propname):
        prop_reg = AllProperties[propname]
        mat = self[matname]
        if prop_reg: # Can be None for nonparametrizable properties.
            mat[propname]=prop_reg 
        else:
            reporter.report("Nonparametrizable property is not loadable.")

        
    # Remove a property.  "Removal" means remove this particular property
    # from this material -- the property continues to exist in the
    # propertymanager, and possibly in other materials.
    def remove_prop(self, matname, propname):
        mat = self[matname]
        prop = AllProperties[propname]
        if mat and prop:
            mat.delete_prop(propname)
        else:
            # Report a sensible error.
            pass
        

    # Add a material.
    #Interface branch
    def add(self, name, materialtype=material.MATERIALTYPE_BULK):
        try:
            collision = self.materials[name]
        except KeyError:        # material doesn't already exist
            self.materials[name] = MaterialProps(name, materialtype)
            switchboard.notify("new_material", name) #, self.materials[name])
            return self.materials[name]
        else:
            raise KeyError("Collision in MaterialManager, key %s." % name)

    # Remove the named material.
    # Menu item checks/reports on current material.
    def delete(self, name):
        doomed = self.materials[name]

        if config.dimension() == 2 and runtimeflags.surface_mode:
            #Interface branch
            material_type = doomed.actual.type()
            #Do the following before the switchboard call to remove_material
            for ms in microStructures.actualMembers():
                interfacemsplugin=ms.getObject().getPlugIn("Interfaces")
                interfacemsplugin.deleteMaterial(name,material_type)

        if doomed:
            doomed.delete_all_props()
            del self.materials[doomed.name]
            switchboard.notify("remove_material",doomed)
            
        # Ensure that all MaterialAttribute objects which refer to
        # this material are notified of its untimely demise.
        for ms in microStructures.actualMembers():
            # cleanAttributes forces microstructure recategorization
            # only if the doomed material is actually used in the
            # microstructure.  It returns True if the material is
            # used.
            if doomed.actual.cleanAttributes(ms.getObject()):
                switchboard.notify("materials changed in microstructure",
                                   ms.getObject())
        switchboard.notify("redraw")

    # "secret" materials are ones that don't appear in the user
    # interface at all. Currently, they're only used by the Relax
    # SkeletonModifier, which assigns a secret Material directly to
    # Mesh elements.  This means that the functions here can get away
    # with skipping all of the bookkeeping and signalling that is done
    # for non-secret Materials.  TODO 3.1: If secret Materials are used
    # for other purposes, then add_secret and delete_secret may need
    # to be more thorough.
    def add_secret(self, name,
                   materialtype=material.MATERIALTYPE_BULK):
        try:
            collision=self.secretmaterials[name]
        except KeyError:
            self.secretmaterials[name] = MaterialProps(name, materialtype)
            return self.secretmaterials[name]
        else:
            raise KeyError("Collision in MaterialManager, key %s." % name)

    def delete_secret(self, name):
        del self.secretmaterials[name]


    # Rename the old-named material to the new name.  It's safe to
    # just leave the microstructure attributes alone, because there is
    # only one instance of the C material -- microstructure attributes
    # use pointers to refer to it.
    def rename(self, oldname, newname):
        mat_prop = self.materials[oldname]
        c_mat = mat_prop.actual

        mat_prop.name = newname
        #Also change the names in the propertyregistration
        mat_prop.rename_material(newname,oldname)
        del self.materials[oldname]
        self.materials[newname]=mat_prop

        #Interface branch
        material_type=c_mat.type()
        #Do the following before the switchboard call to remove_material
        if runtimeflags.surface_mode:
            for ms in microStructures.actualMembers():
                interfacemsplugin=ms.getObject().getPlugIn("Interfaces")
                interfacemsplugin.renameMaterial(oldname,newname,material_type)

        c_mat.rename(newname)
        switchboard.notify("remove_material", oldname)
        switchboard.notify("new_material", newname)

    # Material-manager function for loading a material and properties
    # together from a file.  Creates the Material instance, the
    # MatProps object, and adds it to the materialmanager dictionary,
    # bypassing the functionality used by materialmanager.add, and
    # subsequent add_properties calls.  That set of operations is
    # intended for constructing new materials with no properties.
    def new_material(self, name,
                     materialtype=material.MATERIALTYPE_BULK,
                     *props):
        # If a Material already exists with the same name, just
        # redefine it by deleting its old Properties and adding the
        # new ones.  *Don't* try deleting the Material entirely and
        # recreating it from scratch, which seems like the easy way to
        # go. Deleting the Material would delete it from any
        # Microstructures and Meshes that use it.
        try:
            matprop = self.materials[name]
        except KeyError:
            matprop = MaterialProps(name, materialtype)
            self.materials[name] = matprop
        else:
            matprop.delete_all_props()

        mat = matprop.actual
        for p in props:
            mat.addProperty(p)
            reg = p.registration()
            path = AllProperties.data.reverse_dict[reg].path()
            matprop.add_prop_ref(path, reg)
            reg.materials[name]=(matprop, p)

        switchboard.notify("new_material", name)
        for ms in microStructures.actualMembers():
            if mat in material.getMaterials(ms.getObject()):
                switchboard.notify("materials changed in microstructure",
                                   ms.getObject())
    
    # Makes a copy of material 'name', and names it 'newname'.
    def copy(self, name, newname):
        mat = self.materials[name] 
        if mat:
            newmat = self.add(newname,mat.actual.type()) #Interface branch
            for k in mat.data:
                # add_prop takes care of setting prop.materials.
                self.add_prop(newname, k)
            switchboard.notify("new_material", newname)
                
        
materialmanager = MaterialManager()
AllProperties.materialmanager = materialmanager

def getMaterialNames():
    return materialmanager.materials.keys()

def getMaterial(name):
    # getMaterial is called by the Material* out-typemap when the
    # swigged Material constructor is returning.  In that case, the
    # Material isn't yet in the MaterialManager's lists, so
    # getMaterial will raise an exception.  That's ok.  The typemap
    # catches the exception and knows what to do with it.
    try:
        return materialmanager.materials[name].actual
    except KeyError:
        return materialmanager.secretmaterials[name].actual

def nMaterials():
    return len(materialmanager.materials)

utils.OOFdefine('getMaterial', getMaterial)
utils.OOFdefine("AllMaterials", materialmanager)

###################################################################

def getInterfaceMaterialNames():
    return [matname for matname,mat in materialmanager.materials.items()
            if material.MATERIALTYPE_INTERFACE == mat.actual.type()]

def getBulkMaterialNames():
    return [matname for matname,mat in materialmanager.materials.items()
            if material.MATERIALTYPE_BULK == mat.actual.type()]

