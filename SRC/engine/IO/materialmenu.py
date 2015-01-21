# -*- python -*-
# $RCSfile: materialmenu.py,v $
# $Revision: 1.79.2.6 $
# $Author: fyc $
# $Date: 2014/07/28 22:16:55 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

# Menu for operations related to the MaterialsManager.  Provides
# for the selection and deselection of materials and properties,
# creation and deletion of new materials, and the population of
# materials with properties.  Parametrization of properties themselves
# is handled by the corresponding propertymenu, and saving and loading
# are handled by the "File" submenu of the main OOF menu. 

# These menu operations need not correspond to entries
# in a menu bar -- they're triggered from the GUI by operations
# on the non-menubar buttons of the MaterialsPane.

from ooflib.SWIG.common import pixelgroup
from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import enum
from ooflib.common import parallel_enable
from ooflib.common import pixelselection
from ooflib.common import primitives
from ooflib.common import runtimeflags
from ooflib.common import utils
from ooflib.common.IO import automatic
from ooflib.common.IO import datafile
from ooflib.common.IO import filenameparam
from ooflib.common.IO import microstructureIO
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import pixelgroupparam
from ooflib.common.IO import placeholder
from ooflib.common.IO import whoville
from ooflib.common.IO import mainmenu
from ooflib.common.IO import xmlmenudump
from ooflib.engine import materialmanager
from ooflib.engine.propertyregistration import AllProperties
from ooflib.engine.IO import materialparameter
import ooflib.SWIG.engine.material
import ooflib.common.microstructure

MATERIALTYPE_BULK = ooflib.SWIG.engine.material.MATERIALTYPE_BULK

if runtimeflags.surface_mode:
    MATERIALTYPE_INTERFACE = ooflib.SWIG.engine.material.MATERIALTYPE_INTERFACE

MaterialType = ooflib.SWIG.engine.material.MaterialType

#Interface branch
from ooflib.engine.IO import interfaceparameters

if parallel_enable.enabled():
    from ooflib.engine.IO import materialmenuIPC

import types

StringParameter = parameter.StringParameter
OOFMenuItem = oofmenu.OOFMenuItem
matmanager = materialmanager.materialmanager


###################

_materialmenu = OOFMenuItem(
    'Material',
    cli_only=1,
    help='Create Materials and assign them to pixels.')

mainmenu.OOF.addItem(_materialmenu)


# Add a new material, with a name.

#Interface branch
def _newmaterial(menuitem, name, material_type=None):
    # Backward compatibility with old version without a material_type parameter
    material_type = material_type or MATERIALTYPE_BULK
    matmanager.add(name,material_type)
    if parallel_enable.enabled():
        try:
            from ooflib.SWIG.common import mpitools
            if mpitools.Rank() == 0:
                materialmenuIPC.ipcmaterialmenu.New(name = name)
        except ImportError:
            pass

def materialNameResolver(param, startname):
    if param.automatic():
        #Interface branch
        material_type = param.group['material_type'].value

        # Slightly convoluted conditional -- in surface mode, you have
        # to check to see if you have an interface material.  Outside
        # of surface mode, this is impossible, and
        # MATERIALTYPE_INTERFACE is not defined, so checking for it is
        # an error.
        if runtimeflags.surface_mode:
            if material_type==MATERIALTYPE_INTERFACE:
                basename = 'interfacematerial'
            else:
                basename = 'material'
        else:
            basename = 'material'
    else:
        basename = startname
    return utils.uniqueName(basename, materialmanager.getMaterialNames())

#Interface branch
_materialmenu.addItem(OOFMenuItem(
    'New',
    callback=_newmaterial,
    params=parameter.ParameterGroup(
    parameter.AutomaticNameParameter('name',
                                     resolver=materialNameResolver,
                                     value=automatic.automatic,
                                     tip="Name of the material."),
    enum.EnumParameter('material_type',
                       MaterialType,
                       value=MATERIALTYPE_BULK,
                       tip="Type of the material.")
    ),
    help="Create a new Material.",
    discussion="""<para>
    Create a new &material; containing no &properties;.  If another
    &material; with the same <varname>name</varname> already exists,
    <userinput>&lt;x&gt;</userinput> will be appended to the new
    <varname>name</varname>, where <userinput>x</userinput> is an
    integer chosen to make the new name unique.
    </para>"""))


# Rename an existing material.
def _renamematerial(menuitem, material, name):
    if parallel_enable.enabled():
        materialmenuIPC.ipcmaterialmenu.Rename(material=material,name=name)
    else:
        matmanager.rename(material, name)

_materialmenu.addItem(OOFMenuItem(
    'Rename',
    callback=_renamematerial,
    params=[parameter.StringParameter('material',
                                      tip='Old name of the material.'),
            parameter.AutomaticNameParameter(
    'name', resolver=materialNameResolver, value=automatic.automatic,
    tip='New name for the material.')],
    help='Rename a Material.',
    discussion="""<para>
    Rename the indicated &material;.  It will remain present in any
    &micros; in which it occurs, but will get a new name.
    </para>"""
    ))

# Delete the named material.
def _deletematerial(menuitem, name):
    matmanager.delete(name)
    if parallel_enable.enabled():
        try:
            from ooflib.SWIG.common import mpitools
            if mpitools.Rank() == 0:
                materialmenuIPC.ipcmaterialmenu.Delete(name = name)
        except ImportError:
            pass

_materialmenu.addItem(OOFMenuItem(
    'Delete',
    callback=_deletematerial,
    params=[parameter.StringParameter('name', tip="Name of the material.")],
    help="Delete a Material.",
    discussion="""<para>

    Delete the given &material;.  It will be removed from any &micros;
    in which it is being used.

    </para>"""))

def _deleteAllMaterials(menuitem):
    materials = matmanager.materials.keys()
    for matl in materials:
        matmanager.delete(matl)

_materialmenu.addItem(OOFMenuItem(
    'Delete_All',
    callback=_deleteAllMaterials,
    help="Delete all Materials"))


# Makes a copy of the current material, with a new name.

#Interface branch
#Check the type of the material being copied.
#This is different from materialNameResolver where the
#material type is provided as input.
def copymaterialNameResolver(param, startname):
    if param.automatic():
        matactual=materialmanager.getMaterial(param.group['name'].value)
        # Outside of surface_mode, MATERIALTYPE_INTERFACE is not defined.
        if runtimeflags.surface_mode:
            if matactual.type()==MATERIALTYPE_INTERFACE:
                basename = 'interfacematerial'
            else:
                basename = 'material'
        else:
            basename = 'material'
    else:
        basename = startname
    return utils.uniqueName(basename, materialmanager.getMaterialNames())

def _copymaterial(menuitem, name, new_name):
    matmanager.copy(name, new_name)
    if parallel_enable.enabled():
        try:
            from ooflib.SWIG.common import mpitools
            if mpitools.Rank() == 0:
                materialmenuIPC.ipcmaterialmenu.Copy(name = name, new_name = new_name)
        except ImportError:
            pass
    
_materialmenu.addItem(OOFMenuItem(
    'Copy',
    callback=_copymaterial,
    params=parameter.ParameterGroup(
    parameter.StringParameter('name',
                              tip="Name of the source material."),
    parameter.AutomaticNameParameter('new_name',
                                     resolver=copymaterialNameResolver,
                                     value=automatic.automatic,
                                     tip="Name of the new material.")
    ),
    help="Copy a Material.",
    discussion="""<para>

    Make a copy of a &material;.  The new &material;
    <emphasis>shares</emphasis> its &properties; with the original, so
    changing parameters in a &property; in one &material; also changes
    them in the other.  To create independent &properties;, it is
    necessary to replace the &properties; in one of the &materials;

    </para>"""
    ))



# Property operations.  Properties can be added or removed.

# "property" is actually the name of the property.  It's done
# this way so it looks sensible to the user.
def _addprop(menuitem,name,property):
    matmanager.add_prop(name, property)
    switchboard.notify("material changed", name)
    switchboard.notify("prop_added_to_material", name, property)
    switchboard.notify("redraw")
    if parallel_enable.enabled() == 1:
        try:
            from ooflib.SWIG.common import mpitools
            if mpitools.Rank() == 0:
                materialmenuIPC.ipcmaterialmenu.Add_property(
                    name=name, property=property)
        except ImportError:
            pass

_materialmenu.addItem(OOFMenuItem(
    'Add_property',
    callback=_addprop,
    params=[parameter.StringParameter('name', tip="Name of the material."),
            parameter.StringParameter('property', tip="Name of the property.")],
    help='Add a Property to a Material.',
    discussion = """<para>

    Add the given &property; to the given &material;.  The
    <varname>property</varname> parameter is the <link
    linkend='Section-Concepts-Property-Path'>path</link> to the
    &property;.  A single &property; can be added to more than one
    &material;.
    
    </para>"""
    ))

# Remove the named property from the named material.
def _removeprop(menuitem, name, property):
    matmanager.remove_prop(name, property)
    if parallel_enable.enabled() == 1:
        try:
            from ooflib.SWIG.common import mpitools
            if mpitools.Rank() == 0:
                materialmenuIPC.ipcmaterialmenu.Remove_property(
                    name=name, property=property)
        except ImportError:
            pass
    switchboard.notify("material changed", name)
    switchboard.notify("redraw")

_materialmenu.addItem(OOFMenuItem(
    'Remove_property',
    callback=_removeprop,
    params = [parameter.StringParameter('name', tip="Name of the material."),
              parameter.StringParameter('property',
                                        tip="Name of the property.")],
    help="Remove a Property from a Material.",
    discussion = """<para>

    Remove the given &property; from the given &material; The
    <varname>property</varname> parameter is the <link
    linkend='Section-Concepts-Property-Path'>path</link> to the
    &property;.

    </para>"""
    ))
                      
# Saving and loading are done via the "file" menu, so they're not here.

#####################

## TODO OPT: Assigning and removing materials should be done with couriers
## so that lists of voxels don't have to be created in Python and
## passed to C++.

def _wrapped_assignmat(menuitem, material, microstructure, pixels):
    _assignmat(material, microstructure, pixels)
    if parallel_enable.enabled():
        try:
            from ooflib.SWIG.common import mpitools
            if mpitools.Rank() == 0:
                materialmenuIPC.ipcmaterialmenu.Assign(material = material, microstructure = microstructure, pixels = pixels)
        except ImportError:
            pass

## _assignmat is the actual callback, but it is wrapped through
## _wrapped_assignedmat in order to be able to execute the same
## command in the back end through the use of the same function
def _assignmat(material, microstructure, pixels):
    themat = materialmanager.getMaterial(material)
    ms = ooflib.common.microstructure.microStructures[microstructure].getObject()
    pxls = placeholder.getPlaceHolderFromString(pixels)
    if pxls == placeholder.every:
        themat.assignToAllPixels(ms)
    else:
        if pxls == placeholder.selection:
            group = ms.pixelselection.getSelectionAsGroup()
        else:
            group = ms.findGroup(pixels)
        if group:
            themat.assignToPixelGroup(ms, group)
    switchboard.notify("materials changed in microstructure", ms)
    switchboard.notify("redraw")

_materialmenu.addItem(OOFMenuItem(
    'Assign',
    callback=_wrapped_assignmat,
    params=[materialparameter.MaterialParameter('material',
                                                tip="Material to be assigned."),
            whoville.WhoParameter('microstructure',
                                  ooflib.common.microstructure.microStructures,
                                  tip=parameter.emptyTipString),
            pixelgroupparam.PixelAggregateParameter('pixels',
                                                    tip="Target pixels.")],
    help="Assign a Material to pixels in a Microstructure.",
    discussion=xmlmenudump.loadFile(
            'DISCUSSIONS/engine/menu/assignmaterial.xml')
    ))

def _removemat(menuitem, microstructure, pixels):
    ms = ooflib.common.microstructure.microStructures[microstructure].getObject()
    if pixels == placeholder.every:
        ooflib.SWIG.engine.material.removeAllMaterials(ms)
    else:
        if pixels == placeholder.selection:
            group = ms.pixelselection.getSelectionAsGroup()
        else:
            group = ms.findGroup(pixels)
        if group:
            ooflib.SWIG.engine.material.removeMaterialFromPixels(ms, group)
    switchboard.notify("materials changed in microstructure", ms)
    switchboard.notify("redraw")


_materialmenu.addItem(OOFMenuItem(
    'Remove',
    callback=_removemat,
    params=[whoville.WhoParameter('microstructure',
                                  ooflib.common.microstructure.microStructures,
                                  tip=parameter.emptyTipString),
            pixelgroupparam.PixelAggregateParameter('pixels',
                                                    tip="Target pixels.")],
    help="Remove Material assignments from pixels in a Microstructure.",
    discussion = """<para>

    This command undoes the &material; assignments made with <xref
    linkend='MenuItem-OOF.Material.Assign'/>.  There's really no need
    to do this, since new &materials; may be assigned to pixels
    without removing the old assignments, and in the end all pixels
    should have a &material;.

    </para>"""
    ))

#############################

# Read and write a Microstructure's MaterialAttributes in a data file.

def _writeData(self, dfile, microstructure, pixel):
    material = ooflib.SWIG.engine.material.getMaterialFromPoint(microstructure,
                                                                pixel)
    if material is not None:
        dfile.argument('material', material.name())
        return 1
    return 0
    
ooflib.SWIG.engine.material.MaterialAttributeRegistrationPtr.writeData = \
    _writeData

def _readMSMaterial(menuitem, microstructure, category, material):
    if material is not None:
        mscontext = ooflib.common.microstructure.microStructures[microstructure]
        ms = mscontext.getObject()
        mscontext.begin_writing()
        try:
            mat = materialmanager.getMaterial(material)
            pxls = microstructureIO.getCategoryPixels(microstructure, category)
            mat.assignToPixels(ms, pxls)
        finally:
            mscontext.end_writing()

def _writeGlobalData(self, dfile, microstructure):
    # Write the material definitions to the data file, so that they're
    # available when the pixel attributes are written.
    materials = ooflib.SWIG.engine.material.getMaterials(microstructure)
    writeMaterials(dfile, materials)

ooflib.SWIG.engine.material.MaterialAttributeRegistrationPtr.writeGlobalData = \
                                                              _writeGlobalData
        
microstructureIO.categorymenu.addItem(OOFMenuItem(
    ooflib.SWIG.engine.material.attributeReg.name(),
    callback=_readMSMaterial,
    params=[
    whoville.WhoParameter("microstructure",
                          ooflib.common.microstructure.microStructures,
                          tip=parameter.emptyTipString),
    parameter.IntParameter('category', tip="Category of pixels."),
    parameter.StringParameter('material', tip="Name of the Material.")
    ],
    help=
    "Assign a Material to a pixel category. Used internally in data files.",
    discussion=xmlmenudump.loadFile(
            'DISCUSSIONS/engine/menu/materialcategory.xml')
    ))

###############################

# Read and write a Material and its Properties in a data file.

def writeMaterials(dfile, materials, excludeProps={}):
    # Make sure to save each property only once, even if it's in more
    # than one Material.  Properties in excludeProps have already been
    # written, and should be omitted. excludeProps is a dictionary
    # whose keys are property paths.
    props = {}           # dictionary of all properties used in the Materials
    for material in materials:
        for prop in material.properties():
            props[prop.registration().name()] = prop
    # Sort the properties by name.
    paths = props.keys()
    paths.sort()
    # Write the properties.
    for path in paths:
        if path not in excludeProps:
            props[path].registration().writeData(dfile)
    # Write the materials.
    for material in materials:
        dfile.startCmd(mainmenu.OOF.LoadData.MaterialandType)
        dfile.argument('name', material.name())
        dfile.argument('properties', [prop.registration().name()
                                      for prop in material.properties()])
        #Interface branch
        dfile.argument('materialtype',material.type())
        dfile.endCmd()

def saveMaterials(menuitem, filename, mode, format, materials):
    dfile = datafile.writeDataFile(filename, mode.string(), format)
    writeMaterials(dfile,
                   [materialmanager.getMaterial(m) for m in materials])
    dfile.close()

mainmenu.OOF.File.Save.addItem(oofmenu.OOFMenuItem(
    'Materials',
    callback = saveMaterials,
    ordering=60,
    params=[
    filenameparam.WriteFileNameParameter('filename', tip="Name of the file."),
    filenameparam.WriteModeParameter(
                'mode', tip="'w' to (over)write, 'a' to append."),
    enum.EnumParameter('format', datafile.DataFileFormat, datafile.ASCII,
                       tip="Format of the file."),
    materialparameter.ListOfMaterialsParameter('materials', tip="Material(s) to be saved.")
    ],
    help="Save Materials to a file.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/savematerial.xml')
    ))

def _fixmenu(*args):
    if materialmanager.nMaterials() == 0:
        mainmenu.OOF.File.Save.Materials.disable()
    else:
        mainmenu.OOF.File.Save.Materials.enable()

_fixmenu()

switchboard.requestCallback("new_material", _fixmenu)
switchboard.requestCallback("remove_material", _fixmenu)

## Optional arguments don't work in binary data files, so for
## backwards compatibility we need to retain the menuitem "Material"
## that does not have the materialtype parameter and another menuitem
## "MaterialandType" that does.

def loadMaterial(menuitem, name, properties):
    props = [AllProperties[propname]()  # create instances
             for propname in properties]
    materialmanager.materialmanager.new_material(
        name, MATERIALTYPE_BULK, *props)


mainmenu.OOF.LoadData.addItem(oofmenu.OOFMenuItem(
    'Material',
    callback = loadMaterial,
    params=[
    parameter.StringParameter('name', tip="Name of the material."),
    parameter.ListOfStringsParameter('properties',
                                     tip="Properties for the material.")
    ],
    help="Load Materials from a data file.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/loadmaterial.xml')
    ))

#Interface branch.
def loadMaterialandType(menuitem, name, properties, materialtype):
    props = [AllProperties[propname]()  # create instances
             for propname in properties]
    if materialtype is None:
        materialtype=MATERIALTYPE_BULK
    materialmanager.materialmanager.new_material(name,
                                                 materialtype,
                                                 *props)


mainmenu.OOF.LoadData.addItem(oofmenu.OOFMenuItem(
    'MaterialandType',
    callback = loadMaterialandType,
    params=[
    parameter.StringParameter('name', tip="Name of the material."),
    parameter.ListOfStringsParameter('properties',
                                     tip="Properties for the material."),
    enum.EnumParameter('materialtype', MaterialType,
                       value=MATERIALTYPE_BULK,
                       tip="Type of the material.")
    ],
    help="Load Materials from a data file.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/loadmaterial.xml')
    ))

######################################################################
#Interface branch

_interfacemenu=_materialmenu.addItem(OOFMenuItem('Interface'))

def _assigninterfacemat(menuitem, microstructure, material,
                        skeleton,interfaces):
    ms = ooflib.common.microstructure.microStructures[microstructure].getObject()
    interfacemsplugin=ms.getPlugIn("Interfaces")
    interfacemsplugin.assignMaterialToInterfaces(material,interfaces,skeleton)
    switchboard.notify("materials changed in microstructure", ms)
##        switchboard.notify("redraw")

_interfacemenu.addItem(OOFMenuItem(
    'Assign',
    callback=_assigninterfacemat,
    params=[whoville.WhoParameter('microstructure',
                                  ooflib.common.microstructure.microStructures,
                                  tip=parameter.emptyTipString),
            materialparameter.InterfaceMaterialParameter('material',
                                                         tip="Interface material to be assigned."),
            interfaceparameters.SkelAllParameter("skeleton",
                                                 tip="Skeleton name"),
            interfaceparameters.ListOfInterfacesCombinedBdysParameter("interfaces",
                                                                      tip="Current list of named interfaces and boundaries defined in this microstructure.")
##            interfaceparameters.ListOfInterfacesSkelBdyParameter("interfaces",
##                                                                 tip="Current list of named interfaces and boundaries defined in this microstructure.")
            ],
    help="Assign material to interfaces in a Microstructure.",
    discussion = """<para>

This command assigns a &material; to a list of interfaces and skeleton
boundaries in the microstructure. When the &mesh; is created, an
element is created for every edge belonging to an interface or
skeleton boundary, and each element is assigned the material that was
assigned to the interface or skeleton boundary.

    </para>"""
    ))

#OOF.LoadData.Material.Interface
#Note that OOF.LoadData.Material has a callback
_loadmatinterfacemenu=mainmenu.OOF.LoadData.Material.addItem(oofmenu.OOFMenuItem('Interface'))
#OOF.LoadData.Material.Interface.Assign
_loadmatinterfacemenu.addItem(oofmenu.OOFMenuItem(
    'Assign',
    callback=_assigninterfacemat,
    params=[whoville.WhoParameter('microstructure',
                                  ooflib.common.microstructure.microStructures,
                                  tip=parameter.emptyTipString),
            parameter.StringParameter('material',
                                      tip="Interface material to be assigned."),
            parameter.StringParameter("skeleton",
                                      tip="Skeleton name"),
            parameter.ListOfStringsParameter("interfaces",
                                             tip="Current list of named interfaces defined in this microstructure.")
            ],
    help="Assign material to interfaces in a Microstructure.",
    discussion = """<para>

    This command assigns a &material; to a list of interfaces and skeleton boundaries
    in the microstructure. When the &mesh; is created, an element is created for every
    edge belonging to an interface or skeleton boundary, and each element is assigned
    the material that was assigned to the interface or skeleton boundary.

    </para>"""
    ))

def _removeinterfacemat(menuitem, microstructure,
                        skeleton, interfaces):
    ms = ooflib.common.microstructure.microStructures[microstructure].getObject()
    interfacemsplugin=ms.getPlugIn("Interfaces")
    interfacemsplugin.removeMaterialFromInterfaces(interfaces,skeleton)
    switchboard.notify("materials changed in microstructure", ms)
##        switchboard.notify("redraw")

_interfacemenu.addItem(OOFMenuItem(
    'Remove',
    callback=_removeinterfacemat,
    params=[whoville.WhoParameter('microstructure',
                                  ooflib.common.microstructure.microStructures,
                                  tip=parameter.emptyTipString),
            #The material parameter is used only to group the list of interfaces
            #in the parameter dialog.
##            materialparameter.InterfaceMaterialParameter('material',
##                                                         tip="Interface material."),
##            interfaceparameters.ListOfInterfacesSkelBdyWithMaterialParameter("interfaces",
##                                                                             tip="Current list of interfaces and boundaries, with materials assigned, defined in this microstructure."),
            interfaceparameters.SkelAllParameter("skeleton",
                                                 tip="Skeleton name"),
            interfaceparameters.ListOfInterfacesCombinedBdysParameter("interfaces",
                                                                      tip="Current list of named interfaces and boundaries defined in this microstructure.")
            ],
    help="Remove material from interfaces in a Microstructure.",
    discussion = """<para>

    This command undoes the &material; assignments made with <xref
    linkend='MenuItem-OOF.Material.Interface.Assign'/> on a list of
    interfaces and boundaries.

    </para>"""
    ))
