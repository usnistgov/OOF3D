# -*- python -*-
# $RCSfile: meshIPC.py,v $
# $Revision: 1.21.10.3 $
# $Author: langer $
# $Date: 2014/09/27 22:34:19 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

#
# Allocate nodes and submesh for a process
#

from ooflib.common.IO import oofmenu
from ooflib.SWIG.common import mpitools
from ooflib.common.IO import parallelmainmenu
from ooflib.engine import skeletonelement
from ooflib.common.IO import automatic
from ooflib.common.IO import parameter
from ooflib.SWIG.engine import masterelement
from ooflib.common import labeltree
from ooflib.engine import skeletoncontext
from ooflib.engine.IO import meshparameters
from ooflib.common.IO import whoville
from ooflib.SWIG.common import switchboard
from ooflib.common.IO import reporter
import ooflib.engine.mesh
import string
from ooflib.common import primitives
from ooflib.common import debug

StringParameter = parameter.StringParameter

## General definitions
_rank = mpitools.Rank()
_size = mpitools.Size()

## OOF.LoadData.IPC.Mesh
ipcmeshmenu = parallelmainmenu.ipcmenu.addItem(
    oofmenu.OOFMenuItem('Mesh', secret=1, no_log=1)
    )

#
# This is the callback for OOF.LoadData.IPC.Mesh.femesh
# This is run in every processor.
#
def parallel_femesh(menuitem,name,skeleton,
                    D_typename,T_typename,Q_typename):
    # Build edict map. Access masterelement dictionary directly
    MEdict=masterelement.getMasterElementDict()
    edict = {
        MEdict[D_typename].nsides(): MEdict[D_typename],
        MEdict[T_typename].nsides(): MEdict[T_typename],
        MEdict[Q_typename].nsides(): MEdict[Q_typename]
        }
    skelpath = labeltree.makePath(skeleton)
    skel = skeletoncontext.skeletonContexts[skelpath].getObject()
    femesh = skel.femesh_shares(edict, skeletonelement.SkeletonElement.realmaterial)
    if _rank == 0:
        femesh.all_meshskeletons = skel.all_skeletons
    #collect_pieces(femesh)
    if femesh is not None:
        meshctxt = ooflib.engine.mesh.meshes.add(
            skelpath+[name], femesh,
            parent=skeletoncontext.skeletonContexts[skelpath],
            skeleton=skel,
            elementdict=edict,
            materialfactory=skeletonelement.SkeletonElement.realmaterial)
        meshctxt.createDefaultSubProblem()

#
# This menu command called by parallel_newMesh in this file
#
## OOF.LoadData.IPC.Mesh.femesh
# secret and no_log inherited from ipcmeshmenu (above)?
ipcmeshmenu.addItem(oofmenu.OOFMenuItem(
    'femesh',
    callback = parallel_femesh,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params =
    [
    StringParameter('name'),
    StringParameter('skeleton'),
    StringParameter('D_typename'),
    StringParameter('T_typename'),
    StringParameter('Q_typename')
    ]
    ))

#
# This function called in meshmenu.py
#
def parallel_newMesh(name, skeleton,
                     elem_typename0, elem_typename1, elem_typename2):
    ipcmeshmenu.femesh(name=name,
                       skeleton=skeleton,
                       D_typename=elem_typename0,
                       T_typename=elem_typename1,
                       Q_typename=elem_typename2)


# This method based on the one with the same name from skeletonIPC.py
# A function to collect partitioned mesh skeleton -- not to be used in the end
def collect_pieces(femesh):

    # Build dictionary (instead of using the mesh assigned indices (via index() or get_index())
    #  which are unique but may have gaps)
    nodedict = {}
    i = 0
    for node in femesh.node_iterator():
        nodedict[node.index()] = i
        i += 1

    global _rank
    global _size
    # Gather minimal info for element polygons (to display mesh Skeleton at #0)
    # Only the #0 will store the reconstituted information.

    #RCL: Collect number of nodes from each process into an array.
    # One gets this for nnodes: [nnodes0, nnodes1, ...]
    nnodes = mpitools.Allgather_Int(femesh.nnodes())
    
    #RCL: Same for the elements.
    # One gets this for nelems: [nelems0, nelems1, ...]
    nelems = mpitools.Allgather_Int(femesh.nelements())
    myCoords = reduce(
        lambda x,y: x+y, [[nd.position().x,
                           nd.position().y]
                          for nd in femesh.node_iterator()]
        )
    
    coordSizes = [i*2 for i in nnodes]
    #RCL: Collect (x,y) coordinates of nodes from each process
    # coordSizes contains the array of number of coordinates (counting x and y separately) from each process
    # The return value is a 2-D array, indexed first by the process number(?)
    # One gets this for allCoords: [[x0,y0,x1,y1,...], [x0',y0',x1',y1',...], ...]
    allCoords = mpitools.Allgather_DoubleVec(myCoords,
                                             size_known=coordSizes)

    #RCL: One gets the following format after the list comprehension operations
    # allCoords = [[(x0,y0),(x1,y1), ...], [...], ...]
    allCoords = [ [(allCoords[i][2*j],allCoords[i][2*j+1])
                   for j in range(nnodes[i])]
                  for i in range(_size) ]
    
    # element connectivity signature
    myEConSigs = [len(el.perimeter()) for el in femesh.element_iterator()]
    #RCL: One gets this for allEConSigs: [[elnnodes0,elnnodes1,...],[elnnodes0',elnnodes1',...],...]
    allEConSigs = mpitools.Allgather_IntVec(myEConSigs, size_known=nelems)

    # element connectivity
    #RCL: nodedict must be a map to the 0-based indices of the nodes
    myECons = [ [nodedict[nd.index()] for nd in el.node_iterator()]
                for el in femesh.element_iterator()]
    myECons = reduce(lambda x,y: x+y, myECons)

    #RCL: conSizes looks like [[elnnodes0+elnnodes1+...],[elnnodes0'+elnnodes1'+...],...]
    conSizes = [reduce(lambda x,y: x+y, aECS) for aECS in allEConSigs]

    #RCL: temp looks like
    # [[el0_nodeindex1,el0_nodeindex2,...el1_nodeindex1,el1_nodeindex2,...],[el0'_nodeindex1,el0'_nodeindex2,...,el1'_nodeindex1,el1'_nodeindex2,...],...]
    temp = mpitools.Allgather_IntVec(myECons, size_known=conSizes)
    
    #RCL: The connectivity information could still be shrunk, but its hard...
    # If we store the nodes for each element, duplicate nodes results. Storage becomes ~4*(number of (double x and double y))

    def listrize(list, signature):
        #RCL: nsig is the number of elements if allEConsigs[i] is passed as signature
        nsig = len(signature)
        count = 0
        output = [[] for i in range(nsig)]
        for i in range(nsig):
            for j in range(signature[i]):
                output[i].append(list[count])
                count += 1
        return output

    #RCL: allECons looks like [[[nodeindex1,nodeindex2,...],[nodeindex1',nodeindex2',...],...], [], ...]
    allECons = [listrize(temp[i], allEConSigs[i]) for i in range(_size)]
    if _rank == 0:
        femesh.all_meshskeletons = {"nodes": allCoords,
                              "elements": allECons}

#####################################

def renameMesh_parallel(menuitem, mesh, name):
    oldmeshpath = labeltree.makePath(mesh)
    themesh = ooflib.engine.mesh.meshes[oldmeshpath]
    themesh.reserve()
    themesh.begin_writing()
    try:
        themesh.rename(name, exclude=oldmeshpath[-1])
    finally:
        themesh.end_writing()
        themesh.cancel_reservation()

ipcmeshmenu.addItem(oofmenu.OOFMenuItem(
    'Rename',
    callback=renameMesh_parallel,
    threadable=oofmenu.PARALLEL_THREADABLE,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString),
            parameter.StringParameter('name', '', tip='New name for the mesh.')
            ]
    ))

#######################################

def deleteMesh_parallel(menuitem, mesh):
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

ipcmeshmenu.addItem(oofmenu.OOFMenuItem(
    'Delete',
    threadable=oofmenu.PARALLEL_THREADABLE,
    callback=deleteMesh_parallel,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString)
    ]
    ))

#######################################

def copyMesh_parallel(menuitem, mesh, name,
             copy_field, copy_equation, copy_bc):
    notifications = []
    basemesh = ooflib.engine.mesh.meshes[mesh]
    basemesh.begin_reading()
    try:
        edict = basemesh.elementdict
        copiedmeshname = name

        skel = basemesh.getSkeleton()
        skelpath = labeltree.makePath(basemesh.path())[:-1]

        copiedfemesh = skel.femesh_shares(edict, basemesh.materialfactory)
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
                subp = subpctxt.getObject()
                newsubp = subpctxt.getObject().clone() # CSubProblem object
                newsubpctxt = newmesh.newSubProblem(
                    newsubp, copiedmesh+[subpctxt.name()])
                newsubpfullname = newsubpctxt.path()
                if copy_field:
                    for field in subpctxt.all_compound_fields():
                        newsubp.define_field(field)
                        notifications.append(
                            ("field defined", newsubpfullname, field.name(), 1))
                        newsubp.acquire_field_data(field, subp)
                        if subp.is_active_field(field):
                            newsubp.activate_field(field)
                            notifications.append(
                                ("field activated", newsubpfullname,
                                 field.name(), 1))
                if copy_equation:
                    for eqn in subpctxt.all_equations():
                        newsubp.activate_equation(eqn)
                        notifications.append(
                            ("equation activated",
                             newsubpfullname, eqn.name(), 1))
            # end loop over subproblems
            if copy_field:
                for field in newmesh.all_compound_subproblem_fields():
                    if basemesh.femesh().in_plane(field):
                        newmesh.set_in_plane_field(field, 1)
                        notifications.append(("field inplane",
                                              copiedmeshfullname, field.name(),
                                              1))
            if copy_bc:
                for (bcname, bc) in basemesh.allBoundaryConds():
                    copied = bc.copy(bc.boundary)
                    copied.add_to_mesh(bcname, copiedmesh)
        finally:
            newmesh.end_writing()
            newmesh.cancel_reservation()
    finally:
        basemesh.end_reading()

    for n in notifications:
        switchboard.notify(*n)

ipcmeshmenu.addItem(oofmenu.OOFMenuItem(
    'Copy', callback=copyMesh_parallel,
    threadable=oofmenu.PARALLEL_THREADABLE,
    params= parameter.ParameterGroup(
    whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                          tip=parameter.emptyTipString),
    parameter.StringParameter('name'),
    parameter.BooleanParameter('copy_field', value=1, tip='Copy fields?'),
    parameter.BooleanParameter('copy_equation', value=1, tip='Copy equation?'),
    parameter.BooleanParameter('copy_bc', value=1,
                               tip='Copy boundary conditions?') )
    ))


########################################################################
# Field (Define/Undefine, Activate/Deactivate, In_Plane/Out_of_Plane)
########################################################################

## OOF.LoadData.IPC.Field
ipcfieldmenu = parallelmainmenu.ipcmenu.addItem(
    oofmenu.OOFMenuItem('Field', secret=1, no_log=1)
    )

#TODO 3.1: Mimick the other menus in meshmenu.py. Add initField? Check if buttons/checkboxes are active for the background processes?

def parallel_defineField(menuitem, mesh, field):
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
    subpcontext.changed()

def parallel_undefineField(menuitem, mesh, field):
    meshcontext = ooflib.engine.mesh.meshes[mesh]
    subpcontext = meshcontext.get_default_subproblem()
    subpcontext.reserve()
    subpcontext.begin_writing()
    try:
        subpcontext.getObject().undefine_field(field)
    finally:
        subpcontext.end_writing()
        subpcontext.cancel_reservation()

    subpcontext.autoenableBCs()
    subpcontext.changed()
    switchboard.notify("field defined", subpcontext.path(), field.name(), 0)

ipcfieldmenu.addItem(oofmenu.OOFMenuItem(
    'Define',
    threadable=oofmenu.PARALLEL_THREADABLE,
    callback=parallel_defineField,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString),
            meshparameters.FieldParameter('field', tip=parameter.emptyTipString)
    ]
    ))

ipcfieldmenu.addItem(oofmenu.OOFMenuItem(
    'Undefine',
    threadable=oofmenu.PARALLEL_THREADABLE,
    callback=parallel_undefineField,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString),
            meshparameters.FieldParameter('field', tip=parameter.emptyTipString)
            ]
    ))

def parallel_activateField(menuitem, mesh, field):
    activated = False
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
        subpcontext.changed()

def parallel_deactivateField(menuitem, mesh, field):
    deactivated = False
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
        subpcontext.changed()

ipcfieldmenu.addItem(oofmenu.OOFMenuItem(
    "Activate",
    threadable=oofmenu.PARALLEL_THREADABLE,
    callback=parallel_activateField,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString),
            meshparameters.FieldParameter('field', tip=parameter.emptyTipString)
    ]
    ))

ipcfieldmenu.addItem(oofmenu.OOFMenuItem(
    'Deactivate',
    threadable=oofmenu.PARALLEL_THREADABLE,
    callback=parallel_deactivateField,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString),
            meshparameters.FieldParameter('field', tip=parameter.emptyTipString)
            ]
    ))

def parallel_inPlaneField(menuitem, mesh, field):
    meshcontext = ooflib.engine.mesh.meshes[mesh]
    meshcontext.reserve()
    meshcontext.begin_writing()
    try:
        meshcontext.set_in_plane_field(field, 1)
    finally:
        meshcontext.end_writing()
        meshcontext.cancel_reservation()
    switchboard.notify("field inplane", meshcontext.path(), field.name(), 1)
    meshcontext.changed()
    
def parallel_outOfPlaneField(menuitem, mesh, field):
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
    meshcontext.changed()

ipcfieldmenu.addItem(oofmenu.OOFMenuItem(
    'In_Plane',
    threadable=oofmenu.PARALLEL_THREADABLE,
    callback=parallel_inPlaneField,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString),
            meshparameters.FieldParameter('field', tip=parameter.emptyTipString)
            ]
    ))

ipcfieldmenu.addItem(oofmenu.OOFMenuItem(
    'Out_of_Plane',
    threadable=oofmenu.PARALLEL_THREADABLE,
    callback=parallel_outOfPlaneField,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString),
            meshparameters.FieldParameter('field', tip=parameter.emptyTipString)
            ]
    ))

#####################################################################
# Equation (Activate/Deactivate)
#####################################################################

## OOF.LoadData.IPC.Equation
ipceqnmenu = parallelmainmenu.ipcmenu.addItem(
    oofmenu.OOFMenuItem('Equation', secret=1, no_log=1)
    )

def parallel_activateEquation(menuitem, mesh, equation):
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
    subpcontext.changed()
    
def parallel_deactivateEquation(menuitem, mesh, equation):
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
    subpcontext.changed()

ipceqnmenu.addItem(oofmenu.OOFMenuItem(
    'Activate',
    callback=parallel_activateEquation,
    threadable=oofmenu.PARALLEL_THREADABLE,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString),
            meshparameters.EquationParameter('equation',
                                             tip=parameter.emptyTipString)
    ]
    ))

ipceqnmenu.addItem(oofmenu.OOFMenuItem(
    'Deactivate',
    callback=parallel_deactivateEquation,
    threadable=oofmenu.PARALLEL_THREADABLE,
    params=[whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString),
            meshparameters.EquationParameter('equation',
                                             tip=parameter.emptyTipString)
    ]
    ))


##########################################################

# Copy the field state (definitions, active-ness, planarity) of one
# mesh into another.
def parallel_copyFieldState(menuitem, source, target):
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

    # Update BCs in both meshes.
    target_subp.autoenableBCs()

    target_subp.changed()
    switchboard.notify("redraw")


ipcmeshmenu.addItem(oofmenu.OOFMenuItem(
    'Copy_Field_State',
    callback=parallel_copyFieldState,
    threadable=oofmenu.PARALLEL_THREADABLE,
    params=[whoville.WhoParameter('source',ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString),
            whoville.WhoParameter('target',ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString)]
                        ) )




# Likewise for equation state.

def parallel_copyEquationState(menuitem, source, target):
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
        for e in source_eqns:
            if not target_obj.is_active_equation(e):
                target_obj.activate_equation(e)
                notifications.append(
                        ("equation activated", target_subp.path(), e.name(), 1))
    finally:
        source_subp.end_reading()
        target_subp.end_writing()
        target_subp.cancel_reservation()

    for n in notifications:
        switchboard.notify(*n)

    target_subp.autoenableBCs()
    target_subp.changed()


ipcmeshmenu.addItem(oofmenu.OOFMenuItem(
    'Copy_Equation_State',
    callback=parallel_copyEquationState,
    threadable=oofmenu.PARALLEL_THREADABLE,
    params=[whoville.WhoParameter('source',ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString),
            whoville.WhoParameter('target',ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString)]
    ) )

# Present in meshmenu.py (and absent here) are menus for Initialize,
# cross sections, etc.


####################################################################
# menus for querying information on the node or element
# that a user has clicked on in the graphics window,
# invoked in meshinfo.py.

def parallel_mesh_info_query(menuitem, targetname, position, mesh):
    debug.fmsg()
    meshcontext = ooflib.engine.mesh.meshes[mesh]
    skelobj = meshcontext.getSkeleton()
    femesh = meshcontext.getObject()

    if targetname=="Node":
        fnode = femesh.closestNode(position.x, position.y)
        reportstring=""
        distance2=-1
        if fnode:
            distance2=(fnode.position()-position)**2
            reportstring="""
    index=%d
    type=%s
    position=(%g,%g)
    displaced_position=(%g,%g)
    fields=%s\n""" % (fnode.index(),
                      fnode.classname(),
                      fnode.position().x,fnode.position().y,
                      fnode.displaced_position(femesh).x,
                      fnode.displaced_position(femesh).y,
                      ', '.join(fnode.fieldNames()))
            #Get the subproblems defined on the mesh that contains the node,
            #get the active fields in each subproblem, and find the values
            #of the fields at the node.
            reportsubpfields=["    subproblems and field values:"]
            for subpctxt in meshcontext.subproblems():
                subp=subpctxt.getObject()
                if subp.containsNode(fnode):
                    reportsubpfields.append(8*" "+subpctxt.name())
                    for field in subpctxt.all_compound_fields():
                        if subp.is_active_field(field):
                            reportsubpfields.append(12*" "+`field`)
                            #The hasField check is redundant because of containsNode above.
                            if fnode.hasField(field):
                                for i in range(field.ndof()):
                                    reportsubpfields.append(16*" "+("%g" % field.value(fnode,i)))
            reportstring+=string.join(reportsubpfields,"\n")

        if _rank==0:
            #Get list of squares of distance of node to the click point
            distance2list=[distance2]
            #Get list of reportstring(s) from each process
            reportstringlist=[reportstring]
            dmin=-1
            dmin_proc=-1
            msg="Mesh Info Query Node IPC/MPI:\n"
            #Get report from other processes
            for proc in range(_size):
                if proc!=0:
                    reportstringlist.append(mpitools.Recv_String(proc))
                    distance2list.append(mpitools.Recv_Double(proc))
                if distance2list[proc]>=0:
                    dmin=distance2list[proc]
                    dmin_proc=proc
            #Find closest node among those "nominated" by each process
            for proc in range(_size):
                if distance2list[proc]>=0:
                    if distance2list[proc]<dmin:
                        dmin=distance2list[proc]
                        dmin_proc=proc
            if dmin_proc!=-1:
                msg+="The closest node to the point clicked at (%g,%g) is from process %d:%s\n" % \
                (position.x,position.y,dmin_proc,reportstringlist[dmin_proc])
            reporter.report(msg)
        else:
            #Backend sends report to front end
            mpitools.Send_String(reportstring,0)
            mpitools.Send_Double(distance2,0)
    ################################################################################
    elif targetname=="Element":
        selem = skelobj.enclosingElement(position)
        reportstring=""
        distance2=-1
        if selem:
            felem = femesh.getElement(selem.meshindex)
            if felem:
                distance2=(selem.center()-position)**2

                mat = felem.material()
                if mat:
                    matname = mat.name()
                else:
                    matname = "<No material>"

                reportstring="""
    index=%s
    type=%d
    nodes=%s
    material=%s\n""" % (felem.masterelement().name(),
                        felem.get_index(),
                        string.join(["%s %d at (%g, %g)" % 
                                     (obj.classname(), obj.index(),
                                      obj.position().x, obj.position().y)
                                     for obj in felem.node_iterator()],","),
                        matname)
                #Get the subproblems defined on the mesh,
                #get the active fields in each subproblem, and find the values
                #of the fields at the position inside the element.
                reportsubpfields=["    subproblems and field values:"]
                for subpctxt in meshcontext.subproblems():
                    subp=subpctxt.getObject()
                    reportsubpfields.append(8*" "+subpctxt.name())
                    for field in subpctxt.all_compound_fields():
                        if subp.is_active_field(field):
                            reportsubpfields.append(12*" "+`field`)
                            masterpos=felem.to_master(position)
                            o=felem.outputField(field,masterpos)
                            valuelist=o.valuePtr().value_list()
                            for val in valuelist:
                                reportsubpfields.append(16*" "+`val`)
                reportstring+=string.join(reportsubpfields,"\n")

        if _rank==0:
            distance2list=[distance2]
            #Get list of reportstring(s) from each process
            reportstringlist=[reportstring]
            dmin=-1
            dmin_proc=-1
            msg="Mesh Info Query Element IPC/MPI:\n"
            #Get report from other processes
            for proc in range(_size):
                if proc!=0:
                    reportstringlist.append(mpitools.Recv_String(proc))
                    distance2list.append(mpitools.Recv_Double(proc))
                if distance2list[proc]>=0:
                    dmin=distance2list[proc]
                    dmin_proc=proc
            #Find closest element among those "nominated" by each process
            for proc in range(_size):
                if distance2list[proc]>=0:
                    if distance2list[proc]<dmin:
                        dmin=distance2list[proc]
                        dmin_proc=proc
            if dmin_proc!=-1:
                msg+="From process %d:" % dmin_proc
                msg+=reportstringlist[dmin_proc]
                reporter.report(msg)
            else:
                reporter.report("No enclosing element found!\n")
        else:
            #Backend sends report to front end
            mpitools.Send_String(reportstring,0)
            mpitools.Send_Double(distance2,0)


ipcmeshmenu.addItem(oofmenu.OOFMenuItem(
    'Mesh_Info_Query',
    callback=parallel_mesh_info_query,
    threadable=oofmenu.PARALLEL_THREADABLE,
    params=[StringParameter('targetname'),
            primitives.PointParameter('position', tip='Target point.'),
            whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                                  tip=parameter.emptyTipString)]
    ))
