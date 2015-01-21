# -*- python -*-
# $RCSfile: meshmenu.py,v $
# $Revision: 1.178.2.9 $
# $Author: langer $
# $Date: 2014/11/07 20:31:07 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.SWIG.common import config
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.engine import elementshape
from ooflib.SWIG.engine import masterelement
from ooflib.common import debug
from ooflib.common import enum
from ooflib.common import labeltree
from ooflib.common import microstructure
from ooflib.common import parallel_enable
from ooflib.common import utils
from ooflib.common.IO import automatic
from ooflib.common.IO import datafile
from ooflib.common.IO import filenameparam
from ooflib.common.IO import mainmenu
from ooflib.common.IO import microstructureIO
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import reporter
from ooflib.common.IO import whoville
from ooflib.common.IO import xmlmenudump
from ooflib.engine import bdycondition
from ooflib.engine import evolve
from ooflib.engine import fieldinit
from ooflib.engine import meshcrosssection
from ooflib.engine import meshmod
from ooflib.engine import meshstatus
from ooflib.engine import outputschedule
from ooflib.engine import skeletoncontext
from ooflib.engine import subproblemcontext
from ooflib.engine.IO import meshparameters
from ooflib.engine.IO import skeletonIO


if parallel_enable.enabled():
    from ooflib.engine.IO import meshIPC
import ooflib.engine.mesh
import types
import string

SyncMeshParameter = ooflib.engine.mesh.SyncMeshParameter

OOF = mainmenu.OOF
meshmenu = mainmenu.OOF.addItem(oofmenu.OOFMenuItem(
    'Mesh',
    cli_only=1,
    help='Tools for creating and manipulating Meshes.',
    discussion="""<para>
    The <command>Mesh</command> menu contains tools for creating and
    manipulating finite element &meshes;, including methods for
    defining &fields; and determining which &equations; to <link
    linkend='MenuItem-OOF.Mesh.Solve'>solve</link>.
    </para>"""))

settingsmenu = mainmenu.OOF.Settings.addItem(oofmenu.OOFMenuItem(
    'Mesh_Defaults',
    help='Default values for Mesh parameters'))

####################

# Look for an enclosing mesh parameter -- if not found, use the
# enclosing skeleton parameter.  Mesh copying needs the first case,
# new mesh construction needs the second.

def meshNameResolver(param, startname):
    if param.automatic():
        basename = 'mesh'
    else:
        basename = startname

    try:
        meshname = param.group['mesh'].value
    except IndexError:
        skelname = param.group['skeleton'].value
        skelpath = labeltree.makePath(skelname)
    else:
        skelpath = labeltree.makePath(meshname)[:-1]

    return ooflib.engine.mesh.meshes.uniqueName(skelpath + [basename])

###################################

def newMesh(menuitem, name, skeleton, element_types):
    # if parallel_enable.enabled():
    #     # skeleton is a string!
    #     # The following ASSUMES there are exactly three element_types:
    #     #(D_typename, T_typename and Q_typename, for edgement, Tri and Quad)
    #     meshIPC.parallel_newMesh(name,skeleton,
    #                              element_types[0].name,
    #                              element_types[1].name,
    #                              element_types[2].name)
    # else:
    edict = {}
    for eltype in element_types:
        el = masterelement.getMasterElementFromEnum(eltype)
        edict[el.shape().name()] = el
    skelpath = labeltree.makePath(skeleton)
    skel = skeletoncontext.skeletonContexts[skelpath].getObject()
    femesh = skel.femesh(edict)
    if femesh is not None:
        meshctxt = ooflib.engine.mesh.meshes.add(
            skelpath+[name], femesh,
            parent=skeletoncontext.skeletonContexts[skelpath],
            skeleton=skel,
            elementdict=edict,
            materialfactory=None)
        meshctxt.createDefaultSubProblem()

        meshctxt.setStatus(meshstatus.Unsolved("New mesh."))
    switchboard.notify("redraw")

class MasterElementTypesParameter(enum.ListOfEnumsParameter):
    def __init__(self, name, value=None, default=None, tip=None):
        enum.ListOfEnumsParameter.__init__(
            self, name, 
            elementshape.enumClasses.values(),
            #masterelement.getMasterElementEnumClasses(),
            value, default, tip)
    def clone(self):
        return self.__class__(self.name, self.value, self.default, self.tip)
    def valueDesc(self):
        return "A list of element types."


newmeshcmd = meshmenu.addItem(oofmenu.OOFMenuItem(
    'New',
    callback=newMesh,
    params=parameter.ParameterGroup(
    whoville.AutoWhoNameParameter('name', value=automatic.automatic,
                                  resolver=meshNameResolver,
                                  tip="Name of the new Mesh"),
    whoville.WhoParameter('skeleton', skeletoncontext.skeletonContexts,
                          tip=parameter.emptyTipString),
    MasterElementTypesParameter('element_types',
                                tip='A list of finite element types'),
##    parameter.BooleanParameter('split_interface', value=0,
##                               tip='Split the mesh along interfaces?')
    ),
    help='Create a new Mesh from a Skeleton.',
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/newmesh.xml')
    ))

# The element_types parameter in the New Mesh menu item needs to be
# recreated whenever new MasterElement types are defined.

def buildNewMeshCmd():
    params = parameter.ParameterGroup(
        newmeshcmd.get_arg('name'),
        newmeshcmd.get_arg('skeleton'),
        MasterElementTypesParameter('element_types'))
    newmeshcmd.replace_args(params)

switchboard.requestCallback("new master element", buildNewMeshCmd)

#####################################

def renameMesh(menuitem, mesh, name):
    if parallel_enable.enabled():
        meshIPC.ipcmeshmenu.Rename(mesh=mesh,name=name)
        return

    oldmeshpath = labeltree.makePath(mesh)
    themesh = ooflib.engine.mesh.meshes[oldmeshpath]
    themesh.reserve()
    themesh.begin_writing()
    try:
        themesh.rename(name, exclude=oldmeshpath[-1])
    finally:
        themesh.end_writing()
        themesh.cancel_reservation()

meshmenu.addItem(oofmenu.OOFMenuItem(
    'Rename',
    callback=renameMesh,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString),
            whoville.WhoNameParameter('name', value='',
                                      tip='New name for the mesh.')
            ],
    help="Rename a Mesh.",
    discussion="<para> Assign a new name to a &mesh;. </para>"))

#######################################

def deleteMesh(menuitem, mesh):
    if parallel_enable.enabled():
        meshIPC.ipcmeshmenu.Delete(mesh=mesh)
        return

    meshctxt = ooflib.engine.mesh.meshes[mesh]

    subproblems = meshctxt.subproblems()
    for subproblem in subproblems:
        subproblem.begin_writing()
        try:
            subproblem.destroy()
        finally:
            subproblem.end_writing()

    meshctxt.reserve()
    meshctxt.begin_writing()
    try:
        meshctxt.destroy()         # removes mesh from ooflib.engine.mesh.meshes
    finally:
        meshctxt.end_writing()
        meshctxt.cancel_reservation()

meshmenu.addItem(oofmenu.OOFMenuItem(
    'Delete',
    callback=deleteMesh,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString)
    ],
    help="Delete a Mesh.",
    discussion="""<para>
    Delete a &mesh;.  Its &skel; and &micro; are
    <emphasis>not</emphasis> deleted.
    </para>"""
    ))

#######################################

def copyMesh(menuitem, mesh, name, copy_field, copy_equation, copy_bc):
    if parallel_enable.enabled():
        meshIPC.ipcmeshmenu.Copy(mesh=mesh,name=name,
                                 copy_field=copy_field,
                                 copy_equation=copy_equation, copy_bc=copy_bc)
        return

    notifications = set()
    basemesh = ooflib.engine.mesh.meshes[mesh]
    basemesh.begin_reading()
    try:
        edict = basemesh.elementdict
        copiedmeshname = name

        skel = basemesh.getSkeleton()
        skelpath = labeltree.makePath(basemesh.path())[:-1]

        #Interface branch, pass skeleton path to femesh
        copiedfemesh = skel.femesh(edict, basemesh.materialfactory)
        newmesh = ooflib.engine.mesh.meshes.add(
            skelpath+[copiedmeshname],
            copiedfemesh,
            parent=skeletoncontext.skeletonContexts[skelpath],
            skeleton=skel, elementdict=edict,
            materialfactory=basemesh.materialfactory)
        newmesh.reserve()
        newmesh.begin_writing()
        try:
            copiedmesh = skelpath+[copiedmeshname]
            copiedmeshfullname = string.join(copiedmesh,":")
            for subpctxt in basemesh.subproblems():
                newsubpctxt = subpctxt.clone(newmesh, copy_field, copy_equation,
                                             notifications)
                if copy_field:
                    for field in subpctxt.all_compound_fields():
                        newsubpctxt.getObject().acquire_field_data(
                            field, subpctxt.getObject())
            # end loop over subproblems
            newmesh.getObject().setCurrentTime(
                basemesh.getObject().getCurrentTime())
            if copy_field:
                for field in newmesh.all_subproblem_fields():
                    if (config.dimension() == 2 and 
                        basemesh.femesh().in_plane(field)):
                        newmesh.set_in_plane_field(field, 1)
                        notifications.add(("field inplane",
                                           copiedmeshfullname, field.name(), 1))
                    try:
                        initializer = basemesh.initializers[field]
                    except KeyError:
                        pass
                    else:
                        newmesh.set_field_initializer(field, initializer)
                        notifications.add(("field initialized"))
            if copy_bc:
                for (bcname, bc) in basemesh.allBoundaryConds():
                    #Interface branch
                    #Don't copy the invisible Float BCs associated with
                    #interfaces. (see femesh.spy)
                    if bcname.find('_cntnty_')==0:
                        continue
                    copied = bc.copy(bc.boundary)
                    copied.add_to_mesh(bcname, copiedmesh)
            if copy_field and copy_bc and copy_equation:
                newmesh.setStatus(basemesh.status)
            else:
                newmesh.setStatus(meshstatus.Unsolved("New copy"))
        finally:
            newmesh.end_writing()
            newmesh.cancel_reservation()
    finally:
        basemesh.end_reading()

    for n in notifications:
        ## TODO OPT: remove duplicate notifications
        switchboard.notify(*n)


meshmenu.addItem(oofmenu.OOFMenuItem(
    'Copy', callback=copyMesh,
    params= parameter.ParameterGroup(
    whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                          tip=parameter.emptyTipString),
    whoville.AutoWhoNameParameter('name', value=automatic.automatic,
                                  resolver=meshNameResolver,
                                  tip="Name of the copied Mesh. Use automatic selection, or type in a name."),
    parameter.BooleanParameter('copy_field', value=1, tip='Copy fields?'),
    parameter.BooleanParameter('copy_equation', value=1, tip='Copy equation?'),
    parameter.BooleanParameter('copy_bc', value=1,
                               tip='Copy boundary conditions?') ),
    help="Copy a Mesh.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/copymesh.xml')
    ))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Copy the field state (definitions, active-ness, planarity) of one
# mesh into another.  This is the backwards-compatible deprecated
# version that uses the Mesh's default subproblem.  The preferred
# version is in subproblemmenu.py.

def _copyFieldState(menuitem, source, target):
    if source == target:
        raise ooferror.ErrUserError('Source and target must differ!')
    if parallel_enable.enabled():
        meshIPC.ipcmeshmenu.Copy_Field_State(source=source,target=target)
        return

    notifications = []
    source_mesh = ooflib.engine.mesh.meshes[source]
    target_mesh = ooflib.engine.mesh.meshes[target]
    source_subp = source_mesh.get_default_subproblem()
    target_subp = target_mesh.get_default_subproblem()
    source_subp.begin_reading()
    target_subp.reserve()
    target_subp.begin_writing()
    try:
        source_obj = source_subp.getObject()
        target_obj = target_subp.getObject()
        source_fields = source_subp.all_compound_fields()
        target_fields = target_subp.all_compound_fields()



        # Undefine all the fields in the target that are not in the source.
        for f in target_fields:
            if not source_obj.is_defined_field(f):
                target_obj.undefine_field(f)
                notifications.append(
                    ("field defined", target_subp.path(), f.name(), 0))

        for f in source_fields:
            # Definition.
            if not target_obj.is_defined_field(f):
                target_obj.define_field(f)
                notifications.append(
                    ("field defined", target_subp.path(), f.name(), 1))

            # Activation.
            if source_obj.is_active_field(f):
                if not target_obj.is_active_field(f):
                    target_obj.activate_field(f)
                    notifications.append(
                        ("field activated", target_subp.path(), f.name(), 1))
            else:
                if target_obj.is_active_field(f):
                    target_obj.deactivate_field(f)
                    notifications.append(
                        ("field activated", target_subp.path(), f.name(), 0))

            # Planarity.
            if config.dimension() == 2:
                inplane = source_mesh.femesh().in_plane(f)
                if target_mesh.femesh().in_plane(f) != inplane:
                    target_mesh.set_in_plane_field(f, inplane)
                    notifications.append(("field inplane", target, f.name(),
                                          inplane))
            try:
                initializer = source_mesh.initializers[f]
            except KeyError:
                pass
            else:
                target_mesh.set_field_initializer(f, initializer)
                notifications.append(("field initialized"))
    finally:
        source_subp.end_reading()
        target_subp.end_writing()
        target_subp.cancel_reservation()

    # Make all the switchboard notifications outside the locked region.
    for n in notifications:
        switchboard.notify(*n)

    # Update BCs
    target_subp.autoenableBCs()

    target_subp.changed("Field state changed.")
    switchboard.notify("redraw")

    target_mesh.setStatus(meshstatus.Unsolved("Copied fields"))


meshmenu.addItem(oofmenu.OOFMenuItem(
    'Copy_Field_State',
    callback=_copyFieldState,
    params=[whoville.WhoParameter('source',ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString),
            whoville.WhoParameter('target',ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString)],
    help="Copy the Field state (defined, active, etc) from one Mesh to another.",
    discussion="""<para>

    This command copies the &field; state from the default
    &subproblem; in one &mesh; to another, meaning that the same
    &fields; will be defined, active, and in-plane in the
    <varname>target</varname> &mesh; as in the
    <varname>source</varname> &mesh;.  If &fields; were explicitly
    <link linkend='MenuItem-OOF.Mesh.Set_Field_Initializer'>initialized</link>
    in the source &mesh;, the initializers will be copied, but the
    command does <emphasis>not</emphasis> copy the &field; values.
    (This is because the source and target meshes might have quite
    different geometries.)</para>

    <para>DEPRECATED.  Use <xref
    linkend='MenuItem-OOF.Subproblem.Copy_Field_State'/> instead.

    </para>"""
                        ) )



# Likewise for equation state.  This is also deprecated. See
# subproblemmenu.py for the preferred version.

def _copyEquationState(menuitem, source, target):
    if source == target:
        raise ooferror.ErrUserError('Source and target must differ!')
    if parallel_enable.enabled():
        meshIPC.ipcmeshmenu.Copy_Equation_State(source=source,target=target)
        return

    notifications = []
    source_subp = ooflib.engine.mesh.meshes[source].get_default_subproblem()
    target_subp = ooflib.engine.mesh.meshes[target].get_default_subproblem()
    source_subp.begin_reading()
    target_subp.reserve()
    target_subp.begin_writing()
    try:
        source_obj = source_subp.getObject()
        target_obj = target_subp.getObject()
        source_eqns = source_obj.all_equations()
        target_eqns = target_obj.all_equations()

        for e in target_eqns:
            if not source_obj.is_active_equation(e):
                target_obj.deactivate_equation(e)
                notifications.append(
                    ("equation activated", target_subp.path(), e.name(), 0))
            if config.devel()>=1:
                if not source_obj.is_kinetically_active_equation(e):
                    target_obj.kinetic_deactivate_equation(e)
                    notifications.append(
                        ('kinetics activated', target_subp.path(), e.name(), 0))
                if not source_obj.is_dynamically_active_equation(e):
                    target_obj.deactivate_dynamics(e)
                    notifications.append(
                        ('dynamics activated', target_subp.path(), e.name(), 0))
        for e in source_eqns:
            if not target_obj.is_active_equation(e):
                target_obj.activate_equation(e)
                notifications.append(
                        ("equation activated", target_subp.path(), e.name(), 1))
            if config.devel()>=1:
                if not target_obj.is_kinetically_active_equation(e):
                    target_obj.kinetic_activate_equation(e)
                    notifications.append(
                        ('kinetics activated', target_subp.path(), e.name(), 1))
                if not target_obj.is_dynamically_active_equation(e):
                    target_obj.activate_dynamics(e)
                    notifications.append(
                        ('dynamics activated', target_subp.path(), e.name(), 1))
    finally:
        source_subp.end_reading()
        target_subp.end_writing()
        target_subp.cancel_reservation()

    for n in notifications:
        switchboard.notify(*n)

    target_subp.autoenableBCs()
    target_subp.changed("Equations changed.")


meshmenu.addItem(oofmenu.OOFMenuItem(
    'Copy_Equation_State',
    callback=_copyEquationState,
    params=[whoville.WhoParameter('source',ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString),
            whoville.WhoParameter('target',ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString)],
    help="Copy the set of active Equations from one Mesh to another.",
    discussion="""<para>

    This command copies the &equation; state from the default
    &subproblem; in one &mesh; to the default &subproblem; in another,
    meaning that the same &equations; will be active in the
    <varname>target</varname> &subproblem; as in the
    <varname>source</varname> &subproblem;.

    </para>"""

    ) )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Field definition and activation

fieldmenu = meshmenu.addItem(oofmenu.OOFMenuItem(
    'Field',
    help='Define and activate Fields.',
    discussion="""<para>
    The <command>Field</command> menu contains the commands that
    define and set the properties of &fields; on &meshes;.
    </para>"""))


def _defineField(menuitem, mesh, field):
    ## This has been rewritten to use the default subproblem, for
    ## backwards compatibility.  The menuitem is deprecated -- use
    ## Subproblem.Field.Define instead.
    if parallel_enable.enabled():
        meshIPC.ipcfieldmenu.Define(mesh=mesh,field=field)
    else:
        meshcontext = ooflib.engine.mesh.meshes[mesh]
        subpcontext = meshcontext.get_default_subproblem()
        subpcontext.reserve()
        subpcontext.begin_writing()
        try:
            subpcontext.getObject().define_field(field)
        finally:
            subpcontext.end_writing()
            subpcontext.cancel_reservation()

        switchboard.notify("field defined", subpcontext.path(), field.name(), 1)
        subpcontext.autoenableBCs()
        subpcontext.changed("Field defined.")
        meshcontext.setStatus(meshstatus.Unsolved("New fields defined"))

def _undefineField(menuitem, mesh, field):
    ## Also deprecated.  Use Subproblem.Field.Undefine instead.
    if parallel_enable.enabled():
        meshIPC.ipcfieldmenu.Undefine(mesh=mesh,field=field)
    else:
        meshcontext = ooflib.engine.mesh.meshes[mesh]
        subpcontext = meshcontext.get_default_subproblem()
        subpcontext.reserve()
        subpcontext.begin_writing()
        try:
            subpcontext.getObject().undefine_field(field)
            # After undefining a Field, the data cache in the mesh has
            # the wrong number of dofs in it.  We could in principle
            # delete the correct dofs from each cache entry, but it
            # might be slow (especially for a disk cache).  The
            # simpler thing to do is to just delete the whole cache.
            subpcontext.getParent().clearDataCache()
        finally:
            subpcontext.end_writing()
            subpcontext.cancel_reservation()

        subpcontext.autoenableBCs()
        subpcontext.changed("Field undefined.")
        switchboard.notify("field defined", subpcontext.path(), field.name(), 0)
        meshcontext.setStatus(meshstatus.Unsolved("New fields defined"))

fieldmenu.addItem(oofmenu.OOFMenuItem(
    'Define',
    callback=_defineField,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString),
            meshparameters.FieldParameter('field', tip=parameter.emptyTipString)
    ],
    help="Define a Field on a Mesh. Only defined Fields may be given values.",
    ## TODO: Fix discussion
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/definefield.xml')
    ))

fieldmenu.addItem(oofmenu.OOFMenuItem(
    'Undefine',
    callback=_undefineField,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString),
            meshparameters.FieldParameter('field', tip=parameter.emptyTipString)
            ],
    help="Undefine a Field on a Mesh.  Only defined Fields may be given values.",
    discussion="""<para>

    Undefine a &field; on a &mesh;'s default &subproblem;.  This frees
    the memory used to store the &field; components and destroys their
    values, unless other &subproblems; are using the &field;.  See <xref
    linkend='MenuItem-OOF.Mesh.Field.Define'/>. DEPRECATED.

    </para>"""
    ))


def _activateField(menuitem, mesh, field):
    activation = False
    if parallel_enable.enabled():
        meshIPC.ipcfieldmenu.Activate(mesh=mesh,field=field)
    else:
        meshcontext = ooflib.engine.mesh.meshes[mesh]
        subpcontext = meshcontext.get_default_subproblem()
        subpcontext.reserve()
        subpcontext.begin_writing()
        try:
            subp = subpcontext.getObject()
            if subp.is_defined_field(field):
                subp.activate_field(field)
                activation = True
            else:
                reporter.report(
                    "You must define a Field before you can activate it.")
        finally:
            subpcontext.end_writing()
            subpcontext.cancel_reservation()

        if activation:
            subpcontext.autoenableBCs()
            switchboard.notify("field activated", subpcontext.path(),
                               field.name(), 1)
            subpcontext.changed("Field activated.")
            meshcontext.setStatus(meshstatus.Unsolved("Field activated"))

def _deactivateField(menuitem, mesh, field):
    deactivation = False
    if parallel_enable.enabled():
        meshIPC.ipcfieldmenu.Deactivate(mesh=mesh,field=field)
    else:
        meshcontext = ooflib.engine.mesh.meshes[mesh]
        subpcontext = meshcontext.get_default_subproblem()
        subpcontext.reserve()
        subpcontext.begin_writing()
        try:
            subp = subpcontext.getObject()
            if subp.is_active_field(field):
                subp.deactivate_field(field)
                deactivation = True
            else:
                reporter.report(
                    "You must define and activate a Field before you can deactivate it.")
        finally:
            subpcontext.end_writing()
            subpcontext.cancel_reservation()

        if deactivation:
            subpcontext.autoenableBCs()
            switchboard.notify("field activated", subpcontext.path(),
                               field.name(), 0)
            subpcontext.changed("Field deactivated.")
            meshcontext.setStatus(meshstatus.Unsolved("Field deactivated"))

fieldmenu.addItem(oofmenu.OOFMenuItem(
    "Activate",
    callback=_activateField,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString),
            meshparameters.FieldParameter('field', tip=parameter.emptyTipString)
    ],
    help="Activate a Field.  The solver finds the values of active Fields.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/activatefield.xml')
    ))

fieldmenu.addItem(oofmenu.OOFMenuItem(
    'Deactivate',
    callback=_deactivateField,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString),
            meshparameters.FieldParameter('field', tip=parameter.emptyTipString)
            ],
    help="Deactivate a Field.  The solver finds the values of active Fields.",
    discussion="""<para>

    Deactivating a &field; means that its values will not be found
    when the &mesh; is <link
    linkend="MenuItem-OOF.Mesh.Solve">solved</link>.  See <xref
    linkend='MenuItem-OOF.Mesh.Field.Activate'/>.

    </para>"""
    ))

def _inPlaneField(menuitem, mesh, field):
    if parallel_enable.enabled():
        meshIPC.ipcfieldmenu.In_Plane(mesh=mesh,field=field)
    else:
        meshcontext = ooflib.engine.mesh.meshes[mesh]
        meshcontext.reserve()
        meshcontext.begin_writing()
        try:
            meshcontext.set_in_plane_field(field, 1)
        finally:
            meshcontext.end_writing()
            meshcontext.cancel_reservation()
        switchboard.notify("field inplane", meshcontext.path(), field.name(), 1)
        meshcontext.changed("Field planarity changed.")
#         meshcontext.setStatus(meshstatus.Unsolved("Field planarity changed"))

def _outOfPlaneField(menuitem, mesh, field):
    if parallel_enable.enabled():
        meshIPC.ipcfieldmenu.Out_of_Plane(mesh=mesh,field=field)
    else:
        meshcontext = ooflib.engine.mesh.meshes[mesh]
        meshcontext.reserve()
        meshcontext.begin_writing()
        try:
            meshcontext.set_in_plane_field(field, 0)
        finally:
            meshcontext.end_writing()
            meshcontext.cancel_reservation()
        switchboard.notify("field inplane", meshcontext.path(),
                           field.name(), 0)
        meshcontext.changed("Field planarity changed.")
#         meshcontext.setStatus(meshstatus.Unsolved("Field planarity changed"))

if config.dimension() == 2:
    fieldmenu.addItem(oofmenu.OOFMenuItem(
        'In_Plane',
        callback=_inPlaneField,
        params=[
            whoville.WhoParameter(
                'mesh', ooflib.engine.mesh.meshes,
                tip=parameter.emptyTipString),
            meshparameters.FieldParameter(
                'field', tip=parameter.emptyTipString)
        ],
        help="In-plane Fields are constrained to have no z-components.",
        discussion="""<para>

        This command invokes <link
        linkend='Section-Concepts-Mesh-3D'>generalized plane-strain</link>
        for the given &field; on all &subproblems; on the given &mesh;.
        The out-of-plane derivatives of the &field; are taken to be zero.
        See <xref linkend='MenuItem-OOF.Mesh.Field.Out_of_Plane'/>.>

        </para>"""
        ))

    fieldmenu.addItem(oofmenu.OOFMenuItem(
        'Out_of_Plane',
        callback=_outOfPlaneField,
        params=[
            whoville.WhoParameter(
                'mesh', ooflib.engine.mesh.meshes,
                tip=parameter.emptyTipString),
            meshparameters.FieldParameter(
                'field', tip=parameter.emptyTipString)
        ],
        help="Out-of-plane Fields are allowed to have z-components.",
        discussion="""<para>

        This command disables <link
        linkend='Section-Concepts-Mesh-3D'>generalized plane-strain</link>
        for the given &field; on all &subproblems; on the given &mesh;.
        The out-of-plane derivatives of the &field; will be computed.
        Generally, it's necessary to <link
        linkend='MenuItem-OOF.Mesh.Equation.Activate'>activate</link> a
        <link
        linkend='Section-Concepts-Mesh-Equation-PlaneFlux'>plane-flux
        equation</link> in order to solve for the out-of-plane derivatives
        of a &field;.

        </para>"""
        ))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Field initialization

# Field initialization often involves FloatBC initialization, which is
# really just another type of Field initialization.

## Assign an initializer to a field.  This doesn't actually *apply*
## the initializer, so field values at nodes aren't changed.

def initField(menuitem, mesh, field, initializer):
    # This routine is repeated almost verbatim in meshIO.py, where
    # it's used to initialize meshes loaded from files.
    meshcontext = ooflib.engine.mesh.meshes[mesh]
    meshcontext.reserve()
    meshcontext.begin_writing()
    try:
        meshcontext.set_field_initializer(field, initializer)
    finally:
        meshcontext.end_writing()
        meshcontext.cancel_reservation()
    switchboard.notify("field initializer set")

#     for subproblem in meshcontext.subproblems():
#         if field in subproblem.all_fields():
#             subproblem.changed()
#     switchboard.notify("redraw")

meshmenu.addItem(oofmenu.OOFMenuItem(
    'Set_Field_Initializer',
    callback = initField,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString),
            meshparameters.FieldParameter('field',
                                          tip=parameter.emptyTipString,
                                          outofplane=True),
            fieldinit.FieldInitParameter('initializer',
                                         tip=parameter.emptyTipString)
    ],
    help="Determine how to assign values to a Field on a Mesh.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/initfield.xml')
    ))


# When using subproblems, the field initializers have to be copied
# separately from the Field state, because the initializers live
# in the mesh and the state flags live in the subproblems.

def _copyFieldInits(menuitem, source, target):
    if source == target:
        return
    if parallel_enable.enabled():
        meshIPT.ipcmeshmenu.Copy_Field_Initializers(source=source,target=target)
        return
    notifications=[]
    source_mesh = ooflib.engine.mesh.meshes[source]
    target_mesh = ooflib.engine.mesh.meshes[target]
    source_mesh.begin_reading()
    target_mesh.reserve()
    target_mesh.begin_writing()
    try:
        # Copy Field initializers
        source_fields = source_mesh.all_subproblem_fields()
        target_fields = target_mesh.all_subproblem_fields()
        for f in source_fields:
            if f in target_fields:
                try:
                    initializer=source_mesh.initializers[f]
                except KeyError:
                    pass
                else:
                    target_mesh.set_field_initializer(f, initializer)
                    notifications.append(("field initialized"))
        # Copy FloatBC inititalizers
        for bcname in source_mesh.allBndyCondNames():
            initializer = source_mesh.get_bc_initializer(bcname)
            debug.fmsg("initializer=", initializer)
            if initializer: 
                # Check that the target mesh has a FloatBC with this name
                try:
                    targetbc = target_mesh.getBdyCondition(bcname)
                except KeyError:
                    pass
                else:
                    if isinstance(targetbc, bdycondition.FloatBC):
                        target_mesh.set_bc_initializer(bcname, initializer)
        
    finally:
        source_mesh.end_reading()
        target_mesh.end_writing()
        target_mesh.cancel_reservation()
    for n in notifications:
        switchboard.notify(*n)

meshmenu.addItem(oofmenu.OOFMenuItem(
    'Copy_Field_Initializers',
    callback=_copyFieldInits,
    params=[whoville.WhoParameter('source', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString),
            whoville.WhoParameter('target', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString)],
    help="Copy all of the relevant Field initializers from one Mesh to another.",
    discussion="""<para>

    Copy all of the &field; initialization functions from the source
    &mesh; to the target &mesh;.  This does <emphasis>not</emphasis> actually
    initialize the &fields; in the target &mesh;.  If a &field; is not
    defined in the target &mesh;, its initializer will not be copied.

    </para>"""
    ))


def _clearFieldInit(menuitem, mesh, field):
    themesh = ooflib.engine.mesh.meshes[mesh]
    themesh.reserve()
    themesh.begin_writing()
    try:
        themesh.remove_initializer(field)
    finally:
        themesh.end_writing()
        themesh.cancel_reservation()
    switchboard.notify("field initializer set")

meshmenu.addItem(oofmenu.OOFMenuItem(
    'Clear_Field_Initializer',
    callback=_clearFieldInit,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString),
            meshparameters.FieldParameter('field',
                                          outofplane=True,
                                          tip=parameter.emptyTipString)],
    help="Remove the initializer for the given Field.",
    discussion="""<para>
    Remove the initializer for the given &field; from the given
    &mesh;.  This does not change the values of the &field; itself,
    but prevents it from being reinitialized later.
    </para>"""
    ))

def _clearFieldInits(menuitem, mesh):
    themesh = ooflib.engine.mesh.meshes[mesh]
    themesh.reserve()
    themesh.begin_writing()
    try:
        for fld in themesh.all_subproblem_fields():
            themesh.remove_initializer(fld)
        themesh.remove_all_bc_initializers()
    finally:
        themesh.end_writing()
        themesh.cancel_reservation()
    switchboard.notify("field initializer set")

meshmenu.addItem(oofmenu.OOFMenuItem(
    'Clear_Field_Initializers',
    callback=_clearFieldInits,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString)],
    help="Remove all Field initializers from the current Mesh.",
    discussion="""<para>

    Remove all the &field; and boundary condition initializers from
    the given &mesh;.  This does not change the values of the &fields;
    themselves, but prevents them from being reinitialized later.

    </para>"""
    ))

def applyFieldInits(menuitem, mesh):
    themesh = ooflib.engine.mesh.meshes[mesh]
    themesh.reserve()
    themesh.begin_writing()
    try:
        themesh.initialize_fields(themesh.getObject().getCurrentTime())
        themesh.initialize_bcs(themesh.getObject().getCurrentTime())
    finally:
        themesh.end_writing()
        themesh.cancel_reservation()
    switchboard.notify("mesh data changed", themesh)
    themesh.setStatus(meshstatus.Unsolved("Fields initialized."))
    switchboard.notify("redraw")

meshmenu.addItem(oofmenu.OOFMenuItem(
    'Apply_Field_Initializers',
    callback=applyFieldInits,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString)],
    help="Initialize all Fields.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/applyinit.xml')
))

def _applyFieldInitsAtTime(menuitem, mesh, time):
    themesh = ooflib.engine.mesh.meshes[mesh]
    themesh.reserve()
    themesh.begin_writing()
    try:
        themesh.initialize_fields(time)
        themesh.initialize_bcs(time)
    finally:
        themesh.end_writing()
        themesh.cancel_reservation()
    switchboard.notify("mesh data changed", themesh)
    themesh.setStatus(meshstatus.Unsolved("Fields initialized."))
    switchboard.notify("draw at time", time)

meshmenu.addItem(oofmenu.OOFMenuItem(
    'Apply_Field_Initializers_at_Time',
    callback=_applyFieldInitsAtTime,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString),
            parameter.FloatParameter('time', 0.0,
                                     tip=parameter.emptyTipString)],
    help="Initialize all Fields and reset the Mesh's time.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/applyinittime.xml')
))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Equations

eqnmenu = meshmenu.addItem(oofmenu.OOFMenuItem('Equation',
                                               help='Activate equations.'))

def _activateEquation(menuitem, mesh, equation):
    if parallel_enable.enabled():
        meshIPC.ipceqnmenu.Activate(mesh=mesh,equation=equation)
    else:
        meshcontext = ooflib.engine.mesh.meshes[mesh]
        subpcontext = meshcontext.get_default_subproblem()
        subpcontext.reserve()
        subpcontext.begin_writing()
        try:
            subpcontext.getObject().activate_equation(equation)
        finally:
            subpcontext.end_writing()
            subpcontext.cancel_reservation()

        subpcontext.autoenableBCs()
        switchboard.notify('equation activated', subpcontext.path(),
                           equation.name(), 1)
        subpcontext.changed("Equation activated.")

def _deactivateEquation(menuitem, mesh, equation):
    if parallel_enable.enabled():
        meshIPC.ipceqnmenu.Deactivate(mesh=mesh,equation=equation)
    else:
        meshcontext = ooflib.engine.mesh.meshes[mesh]
        subpcontext = meshcontext.get_default_subproblem()
        subpcontext.reserve()
        subpcontext.begin_writing()
        try:
            subpcontext.getObject().deactivate_equation(equation)
        finally:
            subpcontext.end_writing()
            subpcontext.cancel_reservation()

        switchboard.notify('equation activated', subpcontext.path(),
                           equation.name(), 0)
        subpcontext.autoenableBCs()
        subpcontext.changed("Equation deactivated.")

eqnmenu.addItem(oofmenu.OOFMenuItem(
    'Activate',
    callback=_activateEquation,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString),
            meshparameters.EquationParameter('equation',
                                             tip=parameter.emptyTipString)
    ],
    help="Activate an Equation.  The Solver solves the active Equations.",
    discussion="""<para>

    Activate the given &equation; on the default &subproblem; on the
    given &mesh;. Activated &equations; are the ones that will be
    <link linkend='MenuItem-OOF.Mesh.Solve'>solved</link>.  For a
    solution to be possible, the active &equations; must involve
    &fluxes; that are produced by &properties; in the &mesh;, and
    those &properties; must couple to <link
    linkend='MenuItem-OOF.Mesh.Field.Define'>defined</link> &fields;.
    There must be as many active &equations; as there are <link
    linkend='MenuItem-OOF.Mesh.Field.Activate'>active</link> &fields;</para>

    <para> DEPRECATED. Use <xref
    linkend="MenuItem-OOF.Subproblem.Equation.Activate"/> instead.

    </para>"""
    ))

eqnmenu.addItem(oofmenu.OOFMenuItem(
    'Deactivate',
    callback=_deactivateEquation,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString),
            meshparameters.EquationParameter('equation',
                                             tip=parameter.emptyTipString)
    ],
    help="Deactivate an Equation.  The Solver solves the active Equations.",
    discussion="""<para>

    Deactivate the given &equation; on the default &subproblem; on the
    given &mesh;.  See <xref
    linkend='MenuItem-OOF.Mesh.Equation.Deactivate'/>.</para>

    <para> DEPRECATED.  USE <xref
    linkend="MenuItem-OOF.Subproblem.Equation.Deactivate"/> instead.

    </para>"""

    ))

###########################################

# Cross sections

csmenu = meshmenu.addItem(oofmenu.OOFMenuItem(
    'Cross_Section',
    help="Create and manipulate Mesh cross sections for plotting.",
    discussion=xmlmenudump.loadFile("DISCUSSIONS/engine/menu/cross_section.xml")
    ))

def csnameresolver(param, name):
    if param.automatic():
        basename = 'cs'
    else:
        basename = name
    meshname = param.group['mesh'].value
    if meshname is not None:
        meshpath = labeltree.makePath(meshname)
        meshctxt = ooflib.engine.mesh.meshes[meshpath]
        return meshctxt.uniqueCSName(basename)

csnameparam = parameter.AutomaticNameParameter(
    'name', value=automatic.automatic, tip="Name of the cross section.",
    resolver=csnameresolver)

csmeshparam = whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                    tip=parameter.emptyTipString)

csparamgroup = parameter.ParameterGroup(csnameparam, csmeshparam)

def _newCS(menuitem, mesh, name, cross_section):
    meshctxt = ooflib.engine.mesh.meshes[mesh]
    meshctxt.reserve()
    meshctxt.begin_writing()
    try:
        meshctxt.addCrossSection(name, cross_section)
    finally:
        meshctxt.end_writing()
        meshctxt.cancel_reservation()
    switchboard.notify("cross sections changed")
    switchboard.notify("redraw")

csmenu.addItem(oofmenu.OOFMenuItem(
    'New',
    callback=_newCS,
    params=csparamgroup + [
    parameter.RegisteredParameter('cross_section',
                                  meshcrosssection.MeshCrossSection,
                                  tip="New cross section object.") ],
    help="Create a new cross section on a Mesh.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/new_cross_section.xml')
    ))

def _delCS(menuitem, mesh, name):
    meshctxt = ooflib.engine.mesh.meshes[mesh]
    meshctxt.reserve()
    meshctxt.begin_writing()
    try:
        meshctxt.removeCrossSection(name)
    finally:
        meshctxt.end_writing()
        meshctxt.cancel_reservation()
    switchboard.notify("cross sections changed")
    switchboard.notify("redraw")

csmenu.addItem(oofmenu.OOFMenuItem(
    'Remove',
    callback=_delCS,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString),
            parameter.StringParameter('name', tip='Cross section to remove.')],
    help='Delete a cross section from a mesh.',
    discussion="""<para>
    Delete the cross section named <varname>name</varname> from the &mesh;
    named <varname>mesh</varname>.
    </para>"""))

def _selectCS(menuitem, mesh, cross_section):
    meshctxt = ooflib.engine.mesh.meshes[mesh]
    meshctxt.reserve()
    meshctxt.begin_writing()
    try:
        meshctxt.selectCrossSection(cross_section)
    finally:
        meshctxt.end_writing()
        meshctxt.cancel_reservation()

    switchboard.notify("cross sections changed")
    switchboard.notify("redraw")

csmenu.addItem(oofmenu.OOFMenuItem(
    'Select',
    callback=_selectCS,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString),
    parameter.StringParameter('cross_section', tip='Cross section to select.')],
    help="Select a cross section on a mesh.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/select_cs.xml')
    ))

def _deselectCS(menuitem, mesh):
    meshctxt = ooflib.engine.mesh.meshes[mesh]
    meshctxt.reserve()
    meshctxt.begin_writing()
    try:
        meshctxt.deselectCrossSection()
    finally:
        meshctxt.end_writing()
        meshctxt.cancel_reservation()
    switchboard.notify("cross sections changed")
    switchboard.notify("redraw")

csmenu.addItem(oofmenu.OOFMenuItem(
    'Deselect',
    callback=_deselectCS,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString)],
    help="Deselect all cross sections on a mesh.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/deselect_cs.xml')
    ))

def _renameCS(menuitem, mesh, cross_section, name):
    meshctxt = ooflib.engine.mesh.meshes[mesh]
    meshctxt.reserve()
    meshctxt.begin_writing()
    try:
        meshctxt.renameCrossSection(cross_section, name)
    finally:
        meshctxt.end_writing()
        meshctxt.cancel_reservation()
    switchboard.notify("cross sections changed")

csmenu.addItem(oofmenu.OOFMenuItem(
    'Rename',
    callback=_renameCS,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString),
            parameter.StringParameter('cross_section',
                                      tip='Cross section to rename.'),
            parameter.StringParameter('name',
                                      tip='New name for the cross section.')
            ],
    help="Rename a cross section on a mesh.",
    discussion="<para>Assign a new name to a cross section.</para>"))

def _editCS(menuitem, mesh, name, cross_section):
    meshctxt = ooflib.engine.mesh.meshes[mesh]
    meshctxt.reserve()
    meshctxt.begin_writing()
    try:
        meshctxt.replaceCrossSection(name, cross_section)
    finally:
        meshctxt.end_writing()
        meshctxt.cancel_reservation()
    switchboard.notify("cross sections changed")
    switchboard.notify("redraw")
        
csmenu.addItem(oofmenu.OOFMenuItem(
    'Edit',
    callback=_editCS,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString),
            parameter.StringParameter('name', tip='Cross section to edit.'),
            parameter.RegisteredParameter('cross_section',
                                          meshcrosssection.MeshCrossSection,
                                          tip='New value for the cross section.')
    ],
    help="Reparametrize a cross section on a mesh.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/edit_cs.xml')
    ))

def _copyCS(menuitem, current, cross_section, mesh, name):
    sourcemesh = ooflib.engine.mesh.meshes[current]
    sourcemesh.begin_reading()
    try:
        cs = sourcemesh.getCrossSection(cross_section).clone()
    finally:
        sourcemesh.end_reading()

    targetmesh = ooflib.engine.mesh.meshes[mesh]
    targetmesh.reserve()
    targetmesh.begin_writing()
    try:
        targetmesh.addCrossSection(name,cs)
    finally:
        targetmesh.end_writing()
        targetmesh.cancel_reservation()
    switchboard.notify("cross sections changed")

csmenu.addItem(oofmenu.OOFMenuItem(
    'Copy',
    callback=_copyCS,
    params=[whoville.WhoParameter('current', ooflib.engine.mesh.meshes,
                                  tip='Mesh to copy the cross section from.'),
            parameter.StringParameter('cross_section',
                                      tip='Cross section to copy.')
            ]
    + parameter.ParameterGroup(
    whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                          tip='Mesh to copy the cross section to.'),
    parameter.AutomaticNameParameter('name',
                                     value=automatic.automatic,
                                     resolver=csnameresolver,
                                     tip='Name of the copied cross section.')),
    help="Copy a cross section, possibly to a different Mesh.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/copy_cs.xml')
    ))


#######################################

def saveMesh(menuitem, filename, mode, format, mesh):
    from ooflib.engine.IO import meshIO # avoids import loop
    meshcontext = ooflib.engine.mesh.meshes[mesh]
    meshcontext.begin_reading()
    try:
        if meshcontext.outOfSync():
            raise ooferror.ErrUserError(
                "The Mesh must be rebuilt before it can be saved.")
        meshpath = labeltree.makePath(mesh)
        skelpath = meshpath[:2]
        skelcontext = skeletoncontext.skeletonContexts[skelpath]
        if format==datafile.ABAQUS:
            meshIO.writeABAQUSfromMesh(filename, mode.string(), meshcontext)
        else:
            dfile = datafile.writeDataFile(filename, mode.string(), format)
            microstructureIO.writeMicrostructure(dfile,
                                                 skelcontext.getParent())
            skeletonIO.writeSkeleton(dfile, skelcontext)
            meshIO.writeMesh(dfile, meshcontext)
            dfile.close()
    finally:
        meshcontext.end_reading()

OOF.File.Save.addItem(oofmenu.OOFMenuItem(
    'Mesh',
    callback = saveMesh,
    ordering=80,
    params = [
    filenameparam.WriteFileNameParameter('filename', tip="Name of the file."),
    filenameparam.WriteModeParameter(
                'mode', tip="'w' to (over)write and 'a' to append."),
    enum.EnumParameter('format', datafile.DataFileFormatExt, datafile.ASCII,
                       tip="Format of the file."),
    SyncMeshParameter('mesh', tip='Name of the Mesh.')],
    help="Save a Mesh to a file.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/savemesh.xml')
    ))

def _fixmenu(*args):
    if ooflib.engine.mesh.meshes.nActual() == 0:
        OOF.File.Save.Mesh.disable()
    else:
        OOF.File.Save.Mesh.enable()

_fixmenu()

switchboard.requestCallback(('new who', 'Mesh'), _fixmenu)
switchboard.requestCallback(('remove who', 'Mesh'), _fixmenu)

##########################

def modifyMesh(menuitem, mesh, modifier):
    # The structure is same as "skeletonmenu._modify()"
    meshcontext = ooflib.engine.mesh.meshes[mesh]
    meshcontext.reserve()
    meshcontext.begin_writing()
    try:
        modifier.apply(meshcontext)
    finally:
        meshcontext.end_writing()
        meshcontext.cancel_reservation()
    modifier.signal(meshcontext)
    modifier.setStatus(meshcontext)
    switchboard.notify('Mesh modified', mesh, modifier)

OOF.Mesh.addItem(oofmenu.OOFMenuItem(
    'Modify',
    callback=modifyMesh,
    params=[
    whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes, tip=parameter.emptyTipString),
    parameter.RegisteredParameter('modifier', meshmod.MeshModification,
                                  tip="Mesh modifier.")
    ],
    help="Make changes to a Mesh.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/modify_mesh.xml')
    ))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# SC Patch Recovery

if config.devel()>=1:
    def recoverFluxes(menuitem, mesh):
        meshcontext = ooflib.engine.mesh.meshes[mesh]
        skel = meshcontext.getSkeleton()
        femesh = meshcontext.femesh()
        femesh.create_scpatch(skel)
        femesh.flux_recovery()

    OOF.Mesh.addItem(oofmenu.OOFMenuItem(
        'SCPRecovery',
        callback=recoverFluxes,
        params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                      tip=parameter.emptyTipString)],
        help="Superconvergent Patch Recovery."))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Putting this item in meshdatacache.spy causes a nasty import loop.

from ooflib.SWIG.engine import meshdatacache

def _dummy(*args, **kwargs): pass

settingsmenu.addItem(oofmenu.OOFMenuItem(
    'Data_Cache_Type',
    callback=_dummy,              # Just setting the parameter is enough.
    params = [meshdatacache.cacheTypeParam],
    help="Set the storage method for time step data in new Meshes.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/datacachetype.xml')
))

def _consistencyTolerance(menuitem, tolerance, max_iterations):
    subproblemcontext.consistencyTolerance = tolerance
    evolve.maxconsistencysteps = max_iterations

settingsmenu.addItem(oofmenu.OOFMenuItem(
        "SelfConsistency",
        callback=_consistencyTolerance,
        params=[
            parameter.FloatParameter(
                "tolerance",
                subproblemcontext.consistencyTolerance,
                tip="Relative tolerance for consistency."),
            parameter.IntParameter(
                "max_iterations",
                evolve.maxconsistencysteps,
                tip="Maximum number of iterations to perform.")
                ],
        help="Set the tolerance and iteration limit used when self-consistently solving multiple subproblems simultaneously.",
        discussion=xmlmenudump.loadFile(
            'DISCUSSIONS/engine/menu/selfconsistency.xml')))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#


from ooflib.SWIG.engine import properties

def _numericalDiff(menuitem, epsilon):
    properties.cvar.deriv_eps = epsilon

settingsmenu.addItem(oofmenu.OOFMenuItem(
        "Numerical_Differentiation",
        callback=_numericalDiff,
        params=[
            parameter.FloatParameter(
                "epsilon",
                properties.cvar.deriv_eps,
                tip="Increment for numerical differentiation")],
        help="Set the increment used for approximate derivatives when exact derivatives are not available.",
        discussion=xmlmenudump.loadFile(
            'DISCUSSIONS/engine/menu/numericaldiff.xml')
        ))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

def _removeAllSolvers(menuitem, mesh):
    meshctxt = ooflib.engine.mesh.meshes[mesh]
    for subprob in meshctxt.subproblems():
        subprob.begin_writing()
        try:
            subprob.solver_mode = None
        finally:
            subprob.end_writing()
    switchboard.notify("subproblem solvers changed")

OOF.Mesh.addItem(oofmenu.OOFMenuItem(
    'Remove_All_Solvers',
    callback=_removeAllSolvers,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString)],
    help='Remove the Solvers from all Subproblems.',
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/removesolvers.xml')
    ))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

def _copyAllSolvers(menuitem, source, target):
    sourceMesh = ooflib.engine.mesh.meshes[source]
    targetMesh = ooflib.engine.mesh.meshes[target]
    sourceMesh.begin_reading()
    solvers = {}
    try:
        for subp in sourceMesh.subproblems():
            solvers[subp.name()] = subp.solver_mode.clone()
    finally:
        sourceMesh.end_reading()
    meshpath = targetMesh.path()
    for name, solver in solvers.items():
        subppath = meshpath + ":" + name
        try:
            targetsubp = ooflib.engine.subproblemcontext.subproblems[subppath]
        except KeyError:
            pass
        else:
            _setSolver(menuitem, subppath, solver)

OOF.Mesh.addItem(oofmenu.OOFMenuItem(
        'Copy_All_Solvers',
        callback=_copyAllSolvers,
        params=[
            whoville.WhoParameter('source',
                                  ooflib.engine.mesh.meshes,
                                  tip="Mesh to copy the solvers from."),
            whoville.WhoParameter('target',
                                  ooflib.engine.mesh.meshes,
                                  tip="Mesh to which to copy the solvers.")
            ],
        help="Copy all solvers from one mesh to another.",
        discussion=xmlmenudump.loadFile(
            'DISCUSSIONS/engine/menu/copyallsolvers.xml')
        ))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

def _setSubproblemOrder(menuitem, mesh, subproblems):
    meshctxt = ooflib.engine.mesh.meshes[mesh]
    for order,subprobname in enumerate(subproblems):
        subprob = meshctxt.get_subproblem(subprobname)
        subprob.solveOrder = order
    switchboard.notify("subproblems reordered", meshctxt)

OOF.Mesh.addItem(oofmenu.OOFMenuItem(
        'ReorderSubproblems',
        callback=_setSubproblemOrder,
        params=[whoville.WhoParameter(
                    'mesh', ooflib.engine.mesh.meshes,
                    tip=parameter.emptyTipString),
                parameter.ListOfStringsParameter(
                    'subproblems',
                    tip='A list of Subproblem names in the order in which they should be solved.')
                ],
        help="Set the order in which subproblems will be solved.",
        discussion=xmlmenudump.loadFile(
                'DISCUSSIONS/engine/menu/reordersubp.xml')
        ))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

import time

def _solve(menuitem, mesh, endtime):
    meshctxt = ooflib.engine.mesh.meshes[mesh]
    meshctxt.reserve()
    meshctxt.begin_writing()
    try:
        if not meshctxt.status.solvable:
            raise ooferror.ErrUserError('Mesh is not solvable! '
                                        + meshctxt.status.getDetails())
        t = time.clock()
        evolve.evolve(meshctxt, endtime)
        reporter.report("Elapsed time:", time.clock()-t, "seconds")
    finally:
        meshctxt.end_writing()
        meshctxt.cancel_reservation()

    switchboard.notify("mesh solved", meshctxt)
    switchboard.notify("draw at time", meshctxt.getCurrentTime())

OOF.Mesh.addItem(oofmenu.OOFMenuItem(
   'Solve',
   callback=_solve,
   params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                 tip=parameter.emptyTipString),
           parameter.FloatParameter('endtime', tip='Ending time.')
           ],
   help='Solve or evolve the mesh.',
   discussion=xmlmenudump.loadFile("DISCUSSIONS/engine/menu/solve.xml")
   ))

