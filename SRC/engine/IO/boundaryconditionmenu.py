# -*- python -*-
# $RCSfile: boundaryconditionmenu.py,v $
# $Revision: 1.5.4.3 $
# $Author: fyc $
# $Date: 2014/07/28 22:16:44 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common import ooferror
from ooflib.common import debug
from ooflib.common import labeltree
from ooflib.common import utils
from ooflib.common.IO import automatic
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import reporter
from ooflib.common.IO import whoville
from ooflib.common.IO import xmlmenudump
from ooflib.engine import bdycondition
from ooflib.engine import skeletoncontext
from ooflib.engine.IO import meshmenu
from ooflib.engine.IO import meshparameters
from ooflib.common import parallel_enable
if parallel_enable.enabled():
    from ooflib.engine.IO import boundaryconditionIPC
import ooflib.engine.mesh
import types

bcmenu = oofmenu.OOFMenuItem(
    'Boundary_Conditions',
    cli_only=1,
    help="Create and manipulate boundary conditions on Meshes.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/bc.xml')
    )

meshmenu.meshmenu.addItem(bcmenu)

# BCNameParameter is defined only so that it can have a special widget
# which can be searched for in a WidgetScope.  
class BCNameParameter(parameter.StringParameter):
    pass


def _buildbc(menuitem, name, mesh, condition):
    condition.add_to_mesh(name, mesh)
    switchboard.notify("mesh changed", ooflib.engine.mesh.meshes[mesh])

def bcnameResolver(param, name):
    if param.automatic():
        basename = 'bc'
    else:
        basename = name
    meshname = param.group['mesh'].value
    if meshname is not None:
        meshpath = labeltree.makePath(meshname)
        meshcontext = ooflib.engine.mesh.meshes[meshpath]
        return meshcontext.uniqueBCName(basename)

bcmenu.addItem(oofmenu.OOFMenuItem(
    'New',
    callback=_buildbc,
    params=parameter.ParameterGroup(
    parameter.AutomaticNameParameter('name',
                                     value=automatic.automatic,
                                     tip="Name of the new boundary condition",
                                     resolver=bcnameResolver),
    whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                          tip='Mesh to which to apply the boundary condition.'),
    parameter.RegisteredParameter("condition", bdycondition.BC,
                                  tip="The new boundary condition.")),
    help='Create a new boundary condition.',
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/new_bc.xml')
    ))


def _bcrename(menuitem, mesh, bc, name):
    if parallel_enable.enabled():
        boundaryconditionIPC.ipcbcmenu.Rename(mesh=mesh,bc=bc,name=name)
    else:
        meshcontext = ooflib.engine.mesh.meshes[mesh]
        meshcontext.renameBdyCondition(bc, name)

bcmenu.addItem(oofmenu.OOFMenuItem(
    "Rename",
    callback=_bcrename,
    params=parameter.ParameterGroup(
    whoville.WhoParameter("mesh", ooflib.engine.mesh.meshes,
                          tip=parameter.emptyTipString),
    BCNameParameter('bc', tip='Old name of the boundary condition'),
    parameter.StringParameter('name', tip='New name of the boundary condition')
    ),
    help="Give a boundary condition a new name.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/rename_bc.xml')
    ))

# Remove a boundary condition from the given mesh.
def _bcremove(self, mesh, name):
    if parallel_enable.enabled():
        boundaryconditionIPC.ipcbcmenu.Delete(mesh=mesh,name=name)
    else:
        meshcontext = ooflib.engine.mesh.meshes[mesh]
        meshcontext.rmBdyConditionByName(name)
        switchboard.notify("mesh changed", ooflib.engine.mesh.meshes[mesh])

bcmenu.addItem(oofmenu.OOFMenuItem(
    "Delete",
    callback=_bcremove,
    params = [
            whoville.WhoParameter(
                'mesh', ooflib.engine.mesh.meshes,
                tip="Name of the mesh."),
            BCNameParameter(
                'name',
                tip="Name of the boundary condition to be deleted.")],
    help="Remove this condition from the mesh.",
    discussion="<para>Remove this boundary condition from the &mesh;.</para>"
    ))

# Toggle whether BC is enabled

def _bcenable(self, mesh, name):
    if parallel_enable.enabled():
        boundaryconditionIPC.ipcbcmenu.Enable(mesh=mesh,name=name)
        return
    meshcontext = ooflib.engine.mesh.meshes[mesh]
    bndycond = meshcontext.getBdyCondition(name)
    bndycond.explicitly_enable()
    meshcontext.changed("Boundary conditions enabled")

def _bcdisable(self, mesh, name):
    if parallel_enable.enabled():
        boundaryconditionIPC.ipcbcmenu.Disable(mesh=mesh,name=name)
        return
    meshcontext = ooflib.engine.mesh.meshes[mesh]
    bndycond = meshcontext.getBdyCondition(name)
    bndycond.explicitly_disable()
    meshcontext.changed("Boundary conditions disabled")

bcmenu.addItem(oofmenu.OOFMenuItem(
    "Enable",
    callback=_bcenable,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip="Name of the mesh."),
            BCNameParameter('name', tip="Boundary condition being enabled.")],
    help="Enable an explicitly disabled boundary condition.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/enable_bc.xml')
    ))

bcmenu.addItem(oofmenu.OOFMenuItem(
    "Disable",
    callback=_bcdisable,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip="Name of the mesh."),
            BCNameParameter('name', tip="Boundary condition being disabled.")],
    help="Disable a boundary condition.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/disable_bc.xml')
    ))

# Copy a boundary condition to a new boundary (for possibly another mesh).
def _bccopy(self, current, mesh, bc, name, boundary):
    if parallel_enable.enabled():
        boundaryconditionIPC.ipcbcmenu.Copy(current=current,mesh=mesh,bc=bc,name=name,boundary=boundary)
    else:
        meshcontext = ooflib.engine.mesh.meshes[current]
        bndycond = meshcontext.getBdyCondition(bc)
        newbc = bndycond.copy(boundary)
        newbc.add_to_mesh(name, mesh)
        switchboard.notify("mesh changed", ooflib.engine.mesh.meshes[mesh])
    
bcmenu.addItem(oofmenu.OOFMenuItem(
    "Copy",
    callback=_bccopy,
    params=parameter.ParameterGroup(
    whoville.WhoParameter("current", ooflib.engine.mesh.meshes,
                          tip="Copy the boundary condition from this mesh."),
    ooflib.engine.mesh.SyncMeshParameter(
                "mesh", tip="Copy the boundary condition to this mesh."),
    BCNameParameter("bc", tip="Boundary condition being copied"),
    parameter.AutomaticNameParameter("name", value=automatic.automatic,
                                     resolver=bcnameResolver,
                                     tip="Name of the new boundary condition."),
    meshparameters.MeshBoundaryParameter("boundary",
                                         tip="Boundary to which the copied BC will apply.")
    ),
    help="Copy a boundary condition from one mesh to another.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/copy_bc.xml')
    ))

# Copy all the boundary conditions from one mesh to another, copying
# them to the same boundaries, of course.
def _bccopyall(self, current, mesh):
    if parallel_enable.enabled():
        boundaryconditionIPC.ipcbcmenu.Copy_All(current=current,mesh=mesh)
    else:
        meshcontext = ooflib.engine.mesh.meshes[current]
        allbcs = meshcontext.allBoundaryConds()
        for (name, cond) in allbcs:
            ## TODO 3.1: May need a better check later.
            #Interface branch, update.
            if name.startswith("aux_pointbdy") or name.startswith("_cntnty_"):
                continue
            newbc = cond.copy(cond.boundary)
            newbc.add_to_mesh(name, mesh)
        switchboard.notify("mesh changed", ooflib.engine.mesh.meshes[mesh])

bcmenu.addItem(oofmenu.OOFMenuItem(
    "Copy_All",
    callback=_bccopyall,
    params=[
    whoville.WhoParameter("current", ooflib.engine.mesh.meshes,
                          tip="Copy boundary conditions from this mesh."),
    ooflib.engine.mesh.SyncMeshParameter("mesh",
                          tip="Target mesh for the boundary conditions.")],
    help="Copy all the boundary conditions from one mesh to another.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/copyall_bc.xml')))


def _bcedit(menuitem, name, mesh, condition):
    if parallel_enable.enabled():
        boundaryconditionIPC.ipcbcmenu.Edit(name=name,mesh=mesh,condition=condition)
    else:
        meshctxt = ooflib.engine.mesh.meshes[mesh]
#         oldcond = meshctxt.getBdyCondition(name)
#         msg = condition.check(mesh, exclude=oldcond)
#         if msg:
#             raise ooferror.ErrSetupError(msg)
#         else:
        meshctxt.rmBdyConditionByName(name)
        condition.add_to_mesh(name, mesh)
        switchboard.notify("mesh changed", ooflib.engine.mesh.meshes[mesh])
    
bcmenu.addItem(oofmenu.OOFMenuItem(
    "Edit",
    callback=_bcedit,
    params = [BCNameParameter("name", tip="Name of the boundary condition."),
              # No resolver, name must exist
              whoville.WhoParameter("mesh", ooflib.engine.mesh.meshes,
                                    tip=parameter.emptyTipString),
              parameter.RegisteredParameter("condition", bdycondition.BC,
                                            tip=parameter.emptyTipString)],
    help="Change the attributes of a boundary condition.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/edit_bc.xml')))

                 
    


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Floating boundary condition initialization

# TODO 3.1: Allow time-dependent initializers for BCs?

def setBCInit(menuitem, mesh, bc, initializer):
    # This callback is used in meshIO.py too.
    meshcontext = ooflib.engine.mesh.meshes[mesh]
    meshcontext.reserve()
    meshcontext.begin_writing()
    try:
        meshcontext.set_bc_initializer(bc, initializer)
    finally:
        meshcontext.end_writing()
        meshcontext.cancel_reservation()
    switchboard.notify("field initializer set")

bcmenu.addItem(oofmenu.OOFMenuItem(
        'Set_BC_Initializer',
        callback=setBCInit,
        params=[
            whoville.WhoParameter(
                'mesh', ooflib.engine.mesh.meshes,
                tip=parameter.emptyTipString),
            BCNameParameter(
                'bc',
                tip="Name of the boundary condition to initialize"),
            bdycondition.FloatBCInitParameter(
                'initializer',
                tip='How the boundary condition is to be initialized.')]
        ))

def _clearBCInit(menuitem, mesh, bc):
    themesh = ooflib.engine.mesh.meshes[mesh]
    themesh.reserve()
    themesh.begin_writing()
    try:
        themesh.remove_bc_initializer(bc)
    finally:
        themesh.end_writing()
        themesh.cancel_reservation()
    switchboard.notify("field initializer set")

bcmenu.addItem(oofmenu.OOFMenuItem(
        'Clear_BC_Initializer',
        callback=_clearBCInit,
        params=[
            whoville.WhoParameter(
                'mesh', ooflib.engine.mesh.meshes,
                tip=parameter.emptyTipString),
            BCNameParameter(
                'bc',
                tip='The name of a floating boundary condition.')],
        help=
        'Remove the initializer for the given floating boundary condition.',
        discussion="""<para>
    Remove the initializer for the given floating boundary condition
    from the given &mesh;.  This does not change the values of the
    boundary condition itself, but prevents it from being
    reinitialized later. </para>"""
        ))

