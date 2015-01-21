# -*- python -*-
# $RCSfile: boundaryconditionIPC.py,v $
# $Revision: 1.8.12.1 $
# $Author: langer $
# $Date: 2014/09/27 22:34:19 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.SWIG.common import switchboard
from ooflib.common.IO import oofmenu
#from ooflib.SWIG.common import mpitools
from ooflib.common.IO import parallelmainmenu
from ooflib.common.IO import automatic
from ooflib.common.IO import parameter
from ooflib.engine import bdycondition
from ooflib.common.IO import whoville
from ooflib.engine.IO import meshparameters
import ooflib.engine.mesh
import ooflib.engine.profile
from ooflib.common import debug

## OOF.LoadData.IPC.Boundary_Conditions
ipcbcmenu = parallelmainmenu.ipcmenu.addItem(
    oofmenu.OOFMenuItem('Boundary_Conditions', secret=1, no_log=1)
    )

#boundarycondition.py has this. Don't know yet what the IPC counterpart should do
#meshmenu.meshmenu.addItem(bcmenu)

def parallel_buildbc(menuitem,name,mesh,condition):
    condition.add_to_mesh(name, mesh)
    switchboard.notify("mesh changed", ooflib.engine.mesh.meshes[mesh])

## OOF.LoadData.IPC.Boundary_Conditions.buildbc
ipcbcmenu.addItem(oofmenu.OOFMenuItem(
    'buildbc',
    callback=parallel_buildbc,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params = parameter.ParameterGroup(
    parameter.StringParameter('name'),
    whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                          tip='Mesh to which to apply the boundary condition.'),
    parameter.RegisteredParameter("condition", bdycondition.BC,
                                  tip="The new boundary condition.")
    )
    ))


def parallel_bcrename(menuitem, mesh, bc, name):
    meshcontext = ooflib.engine.mesh.meshes[mesh]
    meshcontext.renameBdyCondition(bc, name)

ipcbcmenu.addItem(oofmenu.OOFMenuItem(
    "Rename",
    callback=parallel_bcrename,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params=parameter.ParameterGroup(
    whoville.WhoParameter("mesh", ooflib.engine.mesh.meshes,
                          tip=parameter.emptyTipString),
    parameter.StringParameter('bc', tip='Old name of the boundary condition'),
    parameter.StringParameter('name', tip='New name of the boundary condition')
    )
    ))

# Remove a boundary condition from the given mesh.
def parallel_bcremove(menuitem, mesh, name):
    meshcontext = ooflib.engine.mesh.meshes[mesh]
    meshcontext.rmBdyConditionByName(name)
    switchboard.notify("mesh changed", ooflib.engine.mesh.meshes[mesh])

ipcbcmenu.addItem(oofmenu.OOFMenuItem(
    "Delete",
    callback=parallel_bcremove,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params = [whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                    tip="Name of the mesh."),
              parameter.StringParameter('name', tip="Name of the boundary condition to be deleted.")]
    ))

# Copy a boundary condition to a new boundary (for possibly another mesh).
def parallel_bccopy(menuitem, current, mesh, bc, name, boundary):
    meshcontext = ooflib.engine.mesh.meshes[current]
    bndycond = meshcontext.getBdyCondition(bc)
    newbc = bndycond.copy(boundary)
    msg = newbc.check(mesh)
    if msg:
        raise ooferror.ErrSetupError(msg)
    else:
        newbc.add_to_mesh(name, mesh)
        switchboard.notify("mesh changed", ooflib.engine.mesh.meshes[mesh])

ipcbcmenu.addItem(oofmenu.OOFMenuItem(
    "Copy",
    callback=parallel_bccopy,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params=parameter.ParameterGroup(
    whoville.WhoParameter("current", ooflib.engine.mesh.meshes,
                          tip="Copy the boundary condition from this mesh."),
    whoville.WhoParameter("mesh", ooflib.engine.mesh.meshes,
                          tip="Copy the boundary condition to this mesh."),
    parameter.StringParameter("bc", tip="Boundary condition being copied"),
    parameter.StringParameter("name"),
    meshparameters.MeshBoundaryParameter("boundary",
                                         tip="Boundary to which the copied BC will apply.")
    )
    ))


# Copy all the boundary conditions from one mesh to another, copying
# them to the same boundaries, of course.
def parallel_bccopyall(menuitem, current, mesh):
    meshcontext = ooflib.engine.mesh.meshes[current]
    allbcs = meshcontext.allBoundaryConds()
    for (name, cond) in allbcs:
        msg = cond.check(mesh)
        if msg:
            raise ooferror.ErrSetupError(msg)
            return
    for (name, cond) in allbcs:
        newbc = cond.copy(cond.boundary)
        newbc.add_to_mesh(name, mesh)
    switchboard.notify("mesh changed", ooflib.engine.mesh.meshes[mesh])

ipcbcmenu.addItem(oofmenu.OOFMenuItem(
    "Copy_All",
    callback=parallel_bccopyall,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params=[
    whoville.WhoParameter("current", ooflib.engine.mesh.meshes,
                          tip="Copy boundary conditions from this mesh."),
    whoville.WhoParameter("mesh", ooflib.engine.mesh.meshes,
                          tip="Target mesh for the boundary conditions.")]
    ))


def parallel_bcedit(menuitem, name, mesh, condition):
    meshctxt = ooflib.engine.mesh.meshes[mesh]
    oldcond = meshctxt.getBdyCondition(name)
    msg = condition.check(mesh, exclude=oldcond)
    if msg:
        raise ooferror.ErrSetupError(msg)
    else:
        meshctxt.rmBdyConditionByName(name)
        condition.add_to_mesh(name, mesh)
        switchboard.notify("mesh changed", ooflib.engine.mesh.meshes[mesh])    

ipcbcmenu.addItem(oofmenu.OOFMenuItem(
    "Edit",
    callback=parallel_bcedit,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params = [parameter.StringParameter("name",
                                        tip="Name of the boundary condition."),
              # No resolver, name must exist
              whoville.WhoParameter("mesh", ooflib.engine.mesh.meshes,
                                    tip=parameter.emptyTipString),
              parameter.RegisteredParameter("condition", bdycondition.BC,
                                            tip=parameter.emptyTipString)]
    ))

def parallel_bcenable(menuitem, mesh, name):
    debug.fmsg()
    meshcontext = ooflib.engine.mesh.meshes[mesh]
    bndycond = meshcontext.getBdyCondition(name)
    bndycond.explicitly_enable()

def parallel_bcdisable(menuitem, mesh, name):
    debug.fmsg()
    meshcontext = ooflib.engine.mesh.meshes[mesh]
    bndycond = meshcontext.getBdyCondition(name)
    bndycond.explicitly_disable()

ipcbcmenu.addItem(oofmenu.OOFMenuItem(
    "Enable",
    callback=parallel_bcenable,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip="Name of the mesh."),
            parameter.StringParameter('name', tip="Boundary condition being enabled.")]
    ))

ipcbcmenu.addItem(oofmenu.OOFMenuItem(
    "Disable",
    callback=parallel_bcdisable,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip="Name of the mesh."),
            parameter.StringParameter('name', tip="Boundary condition being disabled.")]
    ))

##############################
### Similar for Profiles.
##############################

## OOF.LoadData.IPC.Profiles
ipcpfmenu = parallelmainmenu.ipcmenu.addItem(
    oofmenu.OOFMenuItem('Profiles', secret=1, no_log=1)
    )

#boundarycondition.py has this. Don't know yet what the IPC counterpart should do
#meshmenu.meshmenu.addItem(pfmenu)

def parallel_newNamedProfile(menuitem, name, profile):
    profile.set_name(name)

ipcpfmenu.addItem(oofmenu.OOFMenuItem(
    'New',
    callback=parallel_newNamedProfile,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params=[
    parameter.StringParameter('name'),
    parameter.RegisteredParameter('profile', ooflib.engine.profile.CoreProfile,
                                  tip='The new Profile.')
    ]
    ))


# Remove a profile from the profile manager.
def parallel_pfremove(menuitem, name):
    pf = ooflib.engine.profile.AllProfiles[name]
    if pf.deletable():
        del ooflib.engine.profile.AllProfiles[name]
    else:
        reporter.warn("Profile '%s' cannot be deleted because it is still being used." % name)
    
ipcpfmenu.addItem(oofmenu.OOFMenuItem(
    "Delete",
    help="Delete a profile from the system.",
    callback=parallel_pfremove,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params = [parameter.StringParameter('name', tip="Name of the profile to be deleted.")]
    ))


def parallel_pfrename(menuitem, profile, name):
    ooflib.engine.profile.AllProfiles.rename(profile, name)

ipcpfmenu.addItem(oofmenu.OOFMenuItem(
    "Rename",
    help="Rename a profile.",
    callback=parallel_pfrename,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params = [
    parameter.StringParameter('profile', tip="Old name of the profile."),
    parameter.StringParameter('name', tip='New name of the profile')]
    ))


def parallel_pfcopy(menuitem, profile, name):
    old_profile = ooflib.engine.profile.AllProfiles[profile]
    new_profile = old_profile.clone()
    new_profile.set_name(name)

ipcpfmenu.addItem(oofmenu.OOFMenuItem(
    "Copy",
    help="Make a copy of a profile.",
    callback=parallel_pfcopy,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params = [
    parameter.StringParameter('profile', tip="Name of the profile to be copied."),
    parameter.StringParameter('name') ]
    ))


def parallel_pfedit(menuitem, name, profile):
    ooflib.engine.profile.AllProfiles.replaceProfile(name, profile)

ipcpfmenu.addItem(oofmenu.OOFMenuItem(
    "Edit",
    help="Replace a profile with a new profile.",
    callback=parallel_pfedit,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params = [
    parameter.StringParameter("name", tip="Name of the profile to be replaced."),
    # No resolver, name must exist
    parameter.RegisteredParameter("profile", ooflib.engine.profile.CoreProfile,
                                  tip="The replacement profile.")]
    ))

