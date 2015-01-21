# -*- python -*-
# $RCSfile: interfacemenu.py,v $
# $Revision: 1.5.12.1 $
# $Author: langer $
# $Date: 2013/11/08 20:44:58 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.SWIG.common import ooferror
from ooflib.common import utils
from ooflib.common.IO import oofmenu
from ooflib.common.IO import whoville
from ooflib.common.IO import parameter
from ooflib.common.IO import automatic
from ooflib.common.IO import microstructuremenu
from ooflib.common.IO import microstructureIO
from ooflib.engine import interfaceplugin
import ooflib.common.microstructure
from ooflib.common import runtimeflags

_interfacemenu = oofmenu.OOFMenuItem(
    'Interface',
    help="Create and manipulate named interfaces.",
    cli_only=1
)

if runtimeflags.surface_mode:
    microstructuremenu.micromenu.addItem(_interfacemenu)

def _newInterfaceCB(menuitem,microstructure,name,interface_type):
    msobj = ooflib.common.microstructure.microStructures[microstructure].getObject()
    interfacemsplugin=msobj.getPlugIn("Interfaces")
    errmsg=interface_type.check()
    if errmsg:
        raise ooferror.ErrUserError(errmsg)
    else:
        interface_type.addToMS(interfacemsplugin,name)

def interfaceNameResolver(param, startname):
    if param.automatic():
        basename = 'interface'
    else:
        basename = startname
    msname = param.group['microstructure'].value
    msobj = ooflib.common.microstructure.microStructures[msname].getObject()
    interfacemsplugin=msobj.getPlugIn("Interfaces")
    return utils.uniqueName(basename, interfacemsplugin.getCurrentReservedNames())

_interfacemenu.addItem(oofmenu.OOFMenuItem(
    'New',
    callback=_newInterfaceCB,
    params=parameter.ParameterGroup(
    whoville.WhoParameter('microstructure',
                          ooflib.common.microstructure.microStructures,
                          tip=parameter.emptyTipString),
    parameter.AutomaticNameParameter('name',
                                     resolver=interfaceNameResolver,
                                     value=automatic.automatic,
                                     tip="Name of the interface."),
    parameter.RegisteredParameter('interface_type',
                                  interfaceplugin.InterfaceDef,
                                  tip=parameter.emptyTipString)
    ),
    help="Create a named interface in a Microstructure.",
    discussion="""<para>
    Create an interface definition with the given name in the &micros;.
    This action should trigger a rebuild of the &mesh;,
    if it exists.
    </para>"""
    ))

def _renameCB(menuitem, microstructure, interface, name):
    msobj = ooflib.common.microstructure.microStructures[microstructure].getObject()
    interfacemsplugin=msobj.getPlugIn("Interfaces")
    interfacemsplugin.renameInterface(interface,name)

_interfacemenu.addItem(oofmenu.OOFMenuItem(
    "Rename",
    callback=_renameCB,
    help="Rename an interface.",
    params=[
    whoville.WhoParameter('microstructure',
                          ooflib.common.microstructure.microStructures,
                          tip=parameter.emptyTipString),
    parameter.StringParameter('interface', tip="Interface to be renamed."),
    parameter.StringParameter('name', tip="New name.")
    ],
    discussion="""<para>
    Give the interface definition another name.
    </para>"""
    ))

def _deleteCB(menuitem, microstructure, interface):
    msobj = ooflib.common.microstructure.microStructures[microstructure].getObject()
    interfacemsplugin=msobj.getPlugIn("Interfaces")
    interfacemsplugin.removeInterface(interface)

_interfacemenu.addItem(oofmenu.OOFMenuItem(
    "Delete",
    callback=_deleteCB,
    help="Delete a named interface from a Microstructure.",
    params=[
    whoville.WhoParameter('microstructure',
                          ooflib.common.microstructure.microStructures,
                          tip=parameter.emptyTipString),
    parameter.StringParameter('interface', tip="Interface to be removed.")
    ],
    discussion="""<para>
    Delete the interface. This action should trigger a rebuild of the &mesh;,
    if any exist.
    </para>"""
    ))

_interfaceloaddatamenu = microstructureIO.micromenu.addItem(
    oofmenu.OOFMenuItem(
    'Interface',
    help="Create named interfaces used in data files.",
    ))


#OOF.LoadData.Microstructure.Interface.New
_interfaceloaddatamenu.addItem(oofmenu.OOFMenuItem(
    'New',
    callback=_newInterfaceCB, #Use the same callback as OOF.Microstructure.Interface.New
    params=[
    whoville.WhoParameter('microstructure',
                          ooflib.common.microstructure.microStructures,
                          tip=parameter.emptyTipString),
    parameter.StringParameter('name',
                              tip="Name of the interface."),
    parameter.RegisteredParameter('interface_type',
                                  interfaceplugin.InterfaceDef,
                                  tip=parameter.emptyTipString)
    ],
    help="Create a named interface in a Microstructure. Used internally in Mesh data files.",
    ))
