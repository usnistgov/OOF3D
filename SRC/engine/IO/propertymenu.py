# -*- python -*-
# $RCSfile: propertymenu.py,v $
# $Revision: 1.24.10.2 $
# $Author: langer $
# $Date: 2014/05/14 20:55:29 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

# Menu for operations related to the PropertyTree.  Provides
# for the selection and deselection of properties in the tree,
# creation and deletion of instances, incorporation into
# properties materials, and parametrization.  Saving and loading
# are handled by the main OOF "File" submenu.

# These menu operations need not correspond to entries
# in a menu bar -- they're triggered from the GUI by operations
# on the non-menubar buttons of the MaterialsPane.

from ooflib.SWIG.common import ooferror 
from ooflib.SWIG.common import switchboard
from ooflib.common import enum
from ooflib.common import parallel_enable
from ooflib.common.IO import automatic
from ooflib.common.IO import datafile
from ooflib.common.IO import filenameparam
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter

# This file adds ".Property" to "OOF".
from ooflib.engine import propertyregistration
AllProperties = propertyregistration.AllProperties


from ooflib.common.IO.mainmenu import OOF # The root of all menus.

def propertyNameResolver(param, startname):
    if param.automatic():
        basename='instance'
    else:
        basename=startname
    contextname = param.group['property'].value
    return AllProperties.uniqueName(contextname, basename)


def _copywrapper(menuitem, property, new_name):
    if parallel_enable.enabled():
        from ooflib.engine.IO import propertymenuIPC
        propertymenuIPC.ipcpropmenu.Copy(property=property,new_name=new_name)
    else:
        try:
            AllProperties.new_prop(property, new_name)
        except ooferror.ErrUserError, e:
            print e

OOF.Property.addItem(oofmenu.OOFMenuItem(
    'Copy',
    callback=_copywrapper,
    params=parameter.ParameterGroup(
    parameter.StringParameter('property', tip="Name of the source Property."),
    parameter.RestrictedAutomaticNameParameter('new_name',
                                               exclude=':',
                                               resolver=propertyNameResolver,
                                               value=automatic.automatic,
                                               tip="Name for the new Property.")
    ),
    help="Copy a Property.",
    discussion="""<para>

    Make a copy of an existing &property;, with the same parameters.
    The source &property; can be a named &property; or one of the
    predefined unnamed &properties;.

    </para>"""))


def _deletewrapper(menuitem, property):
    if parallel_enable.enabled():
        from ooflib.engine.IO import propertymenuIPC
        propertymenuIPC.ipcpropmenu.Delete(property=property)
    else:
        try:
            AllProperties.delete(property)
        except ooferror.ErrUserError, e:
            print e
    switchboard.notify("redraw")


OOF.Property.addItem(oofmenu.OOFMenuItem(
    'Delete',
    callback=_deletewrapper,
    params=[parameter.StringParameter(
                'property', tip="Name of the property to be deleted.")],
    help="Delete a Property.",
    discussion="""<para>

    Delete a &property;.  It will be removed from the master list of
    &properties; and from any &materials; that use it.  It's not
    possible to delete the predefined unnamed &properties;.

    </para>"""))

# Delete_All is used in the regression tests.  There may not be a GUI
# button for it.

def _deleteAll(menuitem):
    AllProperties.deleteAll()
    switchboard.notify("redraw")

OOF.Property.addItem(oofmenu.OOFMenuItem(
    'Delete_All',
    callback=_deleteAll,
    help="Delete all but the predefined Properties."))

####################################

# Save Properties to a data file.  The corresponding menu items for
# reading them are constructed by the PropertyManager.

def saveProperty(menuitem, filename, mode, format, property):
    dfile = datafile.writeDataFile(filename, mode.string(), format)
    propertyreg = AllProperties[property]
    propertyreg.writeData(dfile)
    dfile.close()

OOF.File.Save.addItem(oofmenu.OOFMenuItem(
    'Property',
    callback=saveProperty,
    ordering=50,
    gui_only=1,
    params=[
            filenameparam.WriteFileNameParameter('filename', tip="File name."),
            filenameparam.WriteModeParameter(
                'mode', tip="'w' to (over)write and 'a' to append."),
            enum.EnumParameter(
                'format', datafile.DataFileFormat, datafile.ASCII,
                tip="File format."),
            parameter.StringParameter(
                'property', tip="Name of the property to be saved.")
            ],
    help="Save the indicated Property to a file.",
    discussion="""<para>

    Save the given &property; to a data file.  The file can be read
    either by <xref linkend='MenuItem-OOF.File.Load.Script'/> or <xref
    linkend='MenuItem-OOF.File.Load.Data'/>, depending on the
    <varname>format</varname>.  File formats are discussed in <xref
    linkend='Section-Concepts-FileFormats'/>.

    </para>"""))

