# -*- python -*-
# $RCSfile: subproblemIPC.py,v $
# $Revision: 1.7.10.3 $
# $Author: langer $
# $Date: 2014/09/27 22:34:20 $

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
from ooflib.SWIG.engine import csubproblem
from ooflib.SWIG.engine import field
from ooflib.SWIG.engine import solverdriver
from ooflib.common import debug
from ooflib.common import labeltree
from ooflib.common import parallel_enable
from ooflib.common.IO import automatic
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import reporter
from ooflib.common.IO import whoville
from ooflib.common.IO import xmlmenudump
from ooflib.engine import fieldinit
from ooflib.engine.IO import meshparameters
import ooflib.engine.mesh
import ooflib.engine.subproblemcontext
from ooflib.common.IO import parallelmainmenu
from ooflib.SWIG.common import mpitools

## OOF.LoadData.IPC.Subproblem
ipcsubproblemmenu = parallelmainmenu.ipcmenu.addItem(
    oofmenu.OOFMenuItem('Subproblem', secret=1, no_log=1)
    )

#############

def parallel_new_subproblem(menuitem, name, mesh, subproblem):
    debug.fmsg()
    meshcontext = ooflib.engine.mesh.meshes[mesh]
    meshcontext.newSubProblem(subproblem, labeltree.makePath(mesh)+[name])

ipcsubproblemmenu.addItem(oofmenu.OOFMenuItem(
    'New',
    callback=parallel_new_subproblem,
    threadable=oofmenu.PARALLEL_THREADABLE,
    params=
    [
    parameter.StringParameter('name'),
    whoville.WhoParameter('mesh', ooflib.engine.mesh.meshes,
                          tip=parameter.emptyTipString),
    parameter.RegisteredParameter('subproblem',
                                  csubproblem.CSubProblemPtr,
                                  tip=parameter.emptyTipString)
    ]
    ))

#############

## TODO MER: The code in _copy_subproblem and _edit_subproblem is
## virtually identical and should be shared.

def parallel_copy_subproblem(menuitem, subproblem, mesh, name):
    debug.fmsg()
    sourcectxt = ooflib.engine.subproblemcontext.subproblems[subproblem]
    sourceobj = sourcectxt.getObject()
    # Make a copy of the CSubProblem object, using the clone function
    # (added to the class by registerCClass).
    copyobj = sourceobj.clone() # new CSubProblem

    sourcectxt.begin_reading()
    try:
        fields = sourcectxt.all_compound_fields()
        activefields = [field for field in fields
                        if sourcectxt.getObject().is_active_field(field)]
        equations = sourceobj.all_equations()
    finally:
        sourcectxt.end_reading()
    
    meshctxt = ooflib.engine.mesh.meshes[mesh]
    copyctxt = meshctxt.newSubProblem(copyobj, mesh+':'+name) # new context
    copyname = copyctxt.path()

    # Set Fields and Equations in the copy
    copyctxt.reserve()
    copyctxt.begin_writing()
    notifications = []
    try:
        for field in fields:
            copyobj.define_field(field)
            notifications.append(("field defined", copyname, field.name(), 1))
        for field in activefields:
            copyobj.activate_field(field)
            notifications.append(("field activated", copyname, field.name(), 1))
        for eqn in sourceobj.all_equations():
            copyobj.activate_equation(eqn)
            notifications.append(("equation activated", copyname, eqn.name(), 1))
    finally:
        copyctxt.end_writing()
        copyctxt.cancel_reservation()
    copyctxt.autoenableBCs()

    for notice in notifications:
        switchboard.notify(*notice)

ipcsubproblemmenu.addItem(oofmenu.OOFMenuItem(
    'Copy',
    callback=parallel_copy_subproblem,
    threadable=oofmenu.PARALLEL_THREADABLE,
    params=
    [
    whoville.WhoParameter('subproblem',
                          ooflib.engine.subproblemcontext.subproblems,
                          tip='The subproblem to be copied.'),
    whoville.WhoParameter('mesh',
                          ooflib.engine.mesh.meshes,
                          tip='The copy will be in this mesh.'),
    parameter.StringParameter('name')
    ]
    ))

#############

def parallel_edit_subproblem(menuitem, name, subproblem):
    debug.fmsg()
    oldsubp = ooflib.engine.subproblemcontext.subproblems[name]
    if oldsubp.name() == ooflib.engine.mesh.defaultSubProblemName:
        raise ooferror.ErrUserError("You can't edit the default Subproblem!")
    meshctxt = oldsubp.getParent()
    oldsubp.reserve()
    oldsubp.begin_writing()
    try:
        oldsubpobj = oldsubp.getObject()
        # Save lists of fields, etc, so that they can be restored in
        # the new subproblem.
        oldfields = oldsubp.all_compound_fields() # should be only CompoundFields
        oldactivefields = [field for field in oldfields
                           if oldsubpobj.is_active_field(field)]
        oldeqns = oldsubp.all_equations()
        oldsubp.destroy()
    finally:
        oldsubp.end_writing()
        oldsubp.cancel_reservation()
        
    # Create context for new subproblem.
    newsubp = meshctxt.newSubProblem(subproblem, name)

    meshctxt.reserve()
    meshctxt.begin_writing()
    # Gather switchboard messages and send them all after the lock has
    # been released.
    notifications = []
    try:
        # Restore field and equation state saved from old subproblem.
        for field in oldfields:
            subproblem.define_field(field)
            notifications.append(("field defined", name, field.name(), 1))
        for field in oldactivefields:
            subproblem.activate_field(field)
            notifications.append(("field activated", name, field.name(), 1))
        for eqn in oldeqns:
            subproblem.activate_equation(eqn)
            notifications.append(("equation activated", name, eqn.name(), 1))
    finally:
        meshctxt.end_writing()
        meshctxt.cancel_reservation()
    newsubp.autoenableBCs()
    for notice in notifications:
        switchboard.notify(*notice)
    

ipcsubproblemmenu.addItem(oofmenu.OOFMenuItem(
    'Edit',
    callback=parallel_edit_subproblem,
    threadable=oofmenu.PARALLEL_THREADABLE,
    params=
    [
    parameter.StringParameter('name'),
    parameter.RegisteredParameter('subproblem', csubproblem.CSubProblemPtr,
                                  tip='The new value of the subproblem.')
    ]
    ))

#############

def parallel_rename_subproblem(menuitem, subproblem, name):
    debug.fmsg()
    oldpath = labeltree.makePath(subproblem)
    subprob = ooflib.engine.subproblemcontext.subproblems[oldpath]
    if subprob.name() == ooflib.engine.mesh.defaultSubProblemName:
        raise ooferror.ErrUserError("You can't rename the default Subproblem!")
    subprob.reserve()
    subprob.begin_writing()
    try:
        subprob.rename(name, exclude=oldpath[-1])
    finally:
        subprob.end_writing()
        subprob.cancel_reservation()
        
ipcsubproblemmenu.addItem(oofmenu.OOFMenuItem(
    'Rename',
    callback=parallel_rename_subproblem,
    threadable=oofmenu.PARALLEL_THREADABLE,
    params=
    [
    whoville.WhoParameter('subproblem',
                          ooflib.engine.subproblemcontext.subproblems,
                          tip=parameter.emptyTipString),
    parameter.StringParameter('name')
    ]
    ))

#############

def parallel_delete_subproblem(menuitem, subproblem):
    debug.fmsg()
    subpctxt = ooflib.engine.subproblemcontext.subproblems[subproblem]
    if subpctxt.name() == ooflib.engine.mesh.defaultSubProblemName:
        raise ooferror.ErrUserError("You can't delete the default Subproblem!")
    subpctxt.reserve()
    subpctxt.begin_writing()
    try:
        subpctxt.destroy()
    finally:
        subpctxt.end_writing()
        subpctxt.cancel_reservation()

ipcsubproblemmenu.addItem(oofmenu.OOFMenuItem(
    'Delete',
    callback=parallel_delete_subproblem,
    threadable=oofmenu.PARALLEL_THREADABLE,
    params=
    [
    whoville.WhoParameter('subproblem',
                          ooflib.engine.subproblemcontext.subproblems,
                          tip=parameter.emptyTipString)
    ]
    ))
    

#############

def parallel_info_subproblem(menuitem, subproblem):
    subpctxt = ooflib.engine.subproblemcontext.subproblems[subproblem]
    subpctxt.begin_reading()
    reportstring=""
    nGatherNodes=0
    nElements=0
    TotalArea=0
    try:
        nElements=subpctxt.nelements()
        TotalArea=subpctxt.area()
        reportstring="""*** Subproblem Info ***
%s
%d elements
%d nodes
area = %g\n""" % (subpctxt.getObject(), nElements, subpctxt.nnodes(),
                        TotalArea)
        nGatherNodes=subpctxt.getObject().GatherNumNodes()
    finally:
        subpctxt.end_reading()

    if mpitools.Rank()==0:
        #Get output from other processes
        for proc in range(mpitools.Size()):
            if proc!=0:
                reportstring+="(From remote process %d:)\n" % proc
                reportstring+=mpitools.Recv_String(proc)
                nElements+=mpitools.Recv_Int(proc)
                TotalArea+=mpitools.Recv_Double(proc)
        reportstring+="""***** Totals (union) *****
%d elements
%d unique nodes
Total Area = %g""" % (nElements,nGatherNodes,TotalArea)
        reporter.report(reportstring)
    else:
        mpitools.Send_String(reportstring,0)
        mpitools.Send_Int(nElements,0)
        mpitools.Send_Double(TotalArea,0)

ipcsubproblemmenu.addItem(oofmenu.OOFMenuItem(
    'Info',
    callback=parallel_info_subproblem,
    threadable=oofmenu.PARALLEL_THREADABLE,
    params=
    [
    whoville.WhoParameter('subproblem',
                          ooflib.engine.subproblemcontext.subproblems,
                          tip=parameter.emptyTipString)
    ]
    ))

###################################

ipcfieldsubproblemmenu = ipcsubproblemmenu.addItem(oofmenu.OOFMenuItem('Field'))

def parallel_defineField(menuitem, subproblem, field):
    debug.fmsg()
    # subproblem is a name, not an object
    subpcontext = ooflib.engine.subproblemcontext.subproblems[subproblem]
    subpcontext.reserve()
    subpcontext.begin_writing()
    didsomething = False
    try:
        if not subpcontext.is_defined_field(field):
            subpcontext.getObject().define_field(field)
            meshctxt = subpcontext.getParent()
            initializer = meshctxt.get_initializer(field)
            if initializer:
                initializer.apply(subpcontext.getObject(), field)
            meshctxt.update_fields()
            didsomething = True
    finally:
        subpcontext.end_writing()
        subpcontext.cancel_reservation()
    if didsomething:
        subpcontext.autoenableBCs()
        subpcontext.changed()
        switchboard.notify("field defined", subproblem, field.name(), 1)
        switchboard.notify("redraw")

ipcfieldsubproblemmenu.addItem(oofmenu.OOFMenuItem(
    'Define',
    threadable=oofmenu.PARALLEL_THREADABLE,
    callback=parallel_defineField,
    params=
    [
    whoville.WhoParameter('subproblem',
                          ooflib.engine.subproblemcontext.subproblems,
                          tip=parameter.emptyTipString),
    meshparameters.FieldParameter('field', tip=parameter.emptyTipString)
    ]
    ))


def parallel_undefineField(menuitem, subproblem, field):
    debug.fmsg()
    subpcontext = ooflib.engine.subproblemcontext.subproblems[subproblem]
    subpcontext.reserve()
    subpcontext.begin_writing()
    try:
        subpcontext.getObject().undefine_field(field)
        subpcontext.getParent().update_fields()
    finally:
        subpcontext.end_writing()
        subpcontext.cancel_reservation()

    subpcontext.autoenableBCs()
    subpcontext.changed()
    switchboard.notify("field defined", subproblem, field.name(), 0)
    switchboard.notify("redraw")

ipcfieldsubproblemmenu.addItem(oofmenu.OOFMenuItem(
    'Undefine',
    threadable=oofmenu.PARALLEL_THREADABLE,
    callback=parallel_undefineField,
    params=
    [
    whoville.WhoParameter('subproblem',
                          ooflib.engine.subproblemcontext.subproblems,
                          tip=parameter.emptyTipString),
    meshparameters.FieldParameter('field', tip=parameter.emptyTipString)
    ]
    ))

def parallel_activateField(menuitem, subproblem, field):
    debug.fmsg()
    activation = False
    subpcontext = ooflib.engine.subproblemcontext.subproblems[subproblem]
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
        switchboard.notify("field activated", subproblem, field.name(), 1)
        subpcontext.changed()
    
def parallel_deactivateField(menuitem, subproblem, field):
    debug.fmsg()
    deactivation = False
    subpcontext = ooflib.engine.subproblemcontext.subproblems[subproblem]
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
        switchboard.notify("field activated", subproblem, field.name(), 0)
        subpcontext.changed()
    
ipcfieldsubproblemmenu.addItem(oofmenu.OOFMenuItem(
    "Activate",
    threadable=oofmenu.PARALLEL_THREADABLE,
    callback=parallel_activateField,
    params=
    [
    whoville.WhoParameter('subproblem',
                          ooflib.engine.subproblemcontext.subproblems,
                          tip=parameter.emptyTipString),
    meshparameters.FieldParameter('field', tip=parameter.emptyTipString)
    ]
    ))

ipcfieldsubproblemmenu.addItem(oofmenu.OOFMenuItem(
    'Deactivate',
    threadable=oofmenu.PARALLEL_THREADABLE,
    callback=parallel_deactivateField,
    params=
    [
    whoville.WhoParameter('subproblem',
                          ooflib.engine.subproblemcontext.subproblems,
                          tip=parameter.emptyTipString),
    meshparameters.FieldParameter('field', tip=parameter.emptyTipString)
    ]
    ))


############################

ipceqnsubproblemmenu = ipcsubproblemmenu.addItem(oofmenu.OOFMenuItem('Equation'))

def parallel_activateEquation(menuitem, subproblem, equation):
    debug.fmsg()
    subpcontext = ooflib.engine.subproblemcontext.subproblems[subproblem]
    subpcontext.reserve()
    subpcontext.begin_writing()
    try:
        subpcontext.getObject().activate_equation(equation)
    finally:
        subpcontext.end_writing()
        subpcontext.cancel_reservation()

    subpcontext.autoenableBCs()
    switchboard.notify('equation activated', subproblem, equation.name(), 1)
    subpcontext.changed()
    
def parallel_deactivateEquation(menuitem, subproblem, equation):
    debug.fmsg()
    subpcontext = ooflib.engine.subproblemcontext.subproblems[subproblem]
    subpcontext.reserve()
    subpcontext.begin_writing()
    try:
        subpcontext.getObject().deactivate_equation(equation)
    finally:
        subpcontext.end_writing()
        subpcontext.cancel_reservation()

    switchboard.notify('equation activated', subproblem, equation.name(), 0)
    subpcontext.autoenableBCs()
    subpcontext.changed()

ipceqnsubproblemmenu.addItem(oofmenu.OOFMenuItem(
    'Activate',
    callback=parallel_activateEquation,
    threadable=oofmenu.PARALLEL_THREADABLE,
    params=
    [
    whoville.WhoParameter('subproblem',
                          ooflib.engine.subproblemcontext.subproblems,
                          tip=parameter.emptyTipString),
    meshparameters.EquationParameter('equation',
                                     tip=parameter.emptyTipString)
    ]
    ))

ipceqnsubproblemmenu.addItem(oofmenu.OOFMenuItem(
    'Deactivate',
    callback=parallel_deactivateEquation,
    threadable=oofmenu.PARALLEL_THREADABLE,
    params=
    [
    whoville.WhoParameter('subproblem',
                          ooflib.engine.subproblemcontext.subproblems,
                          tip=parameter.emptyTipString),
    meshparameters.EquationParameter('equation',
                                     tip=parameter.emptyTipString)
    ]
    ))

#################################

# Copy the field state (definitions, active-ness, planarity) of one
# subproblem into another.

def parallel_copyFieldState(menuitem, source, target):
    debug.fmsg()
    # Let the front-end/pre-IPC call to check this
    #if source == target:
    #    raise ooferror.ErrUserError('Source and target must differ!')

    notifications = []
    source_subp = ooflib.engine.subproblemcontext.subproblems[source]
    target_subp = ooflib.engine.subproblemcontext.subproblems[target]
    source_subp.begin_reading()
    target_subp.reserve()
    target_subp.begin_writing()
    try:
        source_obj = source_subp.getObject()
        target_obj = target_subp.getObject()
        source_fields = source_obj.all_compound_fields()
        target_fields = target_obj.all_compound_fields()

        # Undefine all the fields in the target that are not in the source.
        for f in target_fields:
            if not source_obj.is_defined_field(f):
                target_obj.undefine_field(f)
                notifications.append( ("field defined", target, f.name(), 0) )

        for f in source_fields:
            # Definition.
            if not target_obj.is_defined_field(f):
                target_obj.define_field(f)
                notifications.append( ("field defined", target, f.name(), 1) )

            # Activation.
            if source_obj.is_active_field(f):
                if not target_obj.is_active_field(f):
                    target_obj.activate_field(f)
                    notifications.append(
                        ("field activated", target, f.name(), 1) )
            else:
                if target_obj.is_active_field(f):
                    target_obj.deactivate_field(f)
                    notifications.append(
                        ("field activated", target, f.name(), 0) )

            # Planarity is really a mesh attribute, not a subproblem attribute
            source_mesh = source_subp.getParent().femesh()
            target_meshctxt = target_subp.getParent()
            target_mesh = target_meshctxt.femesh()
            target_meshname = target_meshctxt.path()
            inplane = source_mesh.in_plane(f)
            if target_mesh.in_plane(f) != inplane:
                target_meshctxt.set_in_plane_field(f, inplane)
                notifications.append(
                    ("field inplane", target_meshname, f.name(), inplane))

## Copying initializers has to be done separately, since it's a
## Mesh operation, not a SubProblem operation.
##            try:
##                initializer = source_subp.initializers[f]
##            except KeyError:
##                pass
##            else:
##                target_subp.initialize_field(f, initializer)
##                notifications.append( ("field initialized") )

                    
    finally:
        source_subp.end_reading()
        target_subp.end_writing()
        target_subp.cancel_reservation()

    # Make all the switchboard notifications outside the locked region.
    for n in notifications:
        switchboard.notify(*n)

    # Update BCs
    target_subp.autoenableBCs()

    target_subp.changed()
    switchboard.notify("redraw")
        


ipcsubproblemmenu.addItem(oofmenu.OOFMenuItem(
    'Copy_Field_State',
    callback=parallel_copyFieldState,
    threadable=oofmenu.PARALLEL_THREADABLE,
    params=
    [
    whoville.WhoParameter('source',
                          ooflib.engine.subproblemcontext.subproblems,
                          tip=parameter.emptyTipString),
    whoville.WhoParameter('target',
                          ooflib.engine.subproblemcontext.subproblems,
                          tip=parameter.emptyTipString)
    ]
    ))

    

# Likewise for equation state.

def parallel_copyEquationState(menuitem, source, target):
    debug.fmsg()
    # Let the front-end/pre-IPC call to check this
    #if source == target:
    #    raise ooferror.ErrUserError('Source and target must differ!')

    notifications = []
    source_subp = ooflib.engine.subproblemcontext.subproblems[source]
    target_subp = ooflib.engine.subproblemcontext.subproblems[target]
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
                    ("equation activated", target, e.name(), 0) )
        for e in source_eqns:
            if not target_obj.is_active_equation(e):
                target_obj.activate_equation(e)
                notifications.append(
                        ("equation activated", target, e.name(), 1) )
    finally:
        source_subp.end_reading()
        target_subp.end_writing()
        target_subp.cancel_reservation()

    for n in notifications:
        switchboard.notify(*n)

    target_subp.autoenableBCs()
    target_subp.changed()
    

ipcsubproblemmenu.addItem(oofmenu.OOFMenuItem(
    'Copy_Equation_State',
    callback=parallel_copyEquationState,
    threadable=oofmenu.PARALLEL_THREADABLE,
    params=
    [
    whoville.WhoParameter('source',
                          ooflib.engine.subproblemcontext.subproblems,
                          tip=parameter.emptyTipString),
    whoville.WhoParameter('target',
                          ooflib.engine.subproblemcontext.subproblems,
                          tip=parameter.emptyTipString)
    ]
    ))
