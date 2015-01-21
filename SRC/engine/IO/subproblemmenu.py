# -*- python -*-
# $RCSfile: subproblemmenu.py,v $
# $Revision: 1.62.2.10 $
# $Author: fyc $
# $Date: 2014/07/31 21:27:41 $

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
from ooflib.common import debug
from ooflib.common import enum
from ooflib.common import labeltree
from ooflib.common import parallel_enable
from ooflib.common.IO import automatic
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import reporter
from ooflib.common.IO import whoville
from ooflib.common.IO import xmlmenudump
from ooflib.engine import materialmanager
from ooflib.engine import meshstatus
from ooflib.engine import solvermode
from ooflib.engine import subproblemtype
from ooflib.engine.IO import meshparameters
import ooflib.engine.mesh
import ooflib.engine.subproblemcontext
import copy

SyncMeshParameter = ooflib.engine.mesh.SyncMeshParameter

if parallel_enable.enabled():
    from ooflib.engine.IO import subproblemIPC
    ipcsubpmenu=subproblemIPC.ipcsubproblemmenu

subproblemMenu = mainmenu.OOF.addItem(oofmenu.OOFMenuItem(
    'Subproblem',
    help="Tools for creating and solving sections of meshes",
    cli_only=1))

# Look for an enclosing subproblem parameter -- if not found, use the
# enclosing mesh parameter.  SubProblem copying needs the first case,
# new SubProblem construction needs the second.

def subproblemNameResolver(param, startname):
    if param.automatic():
        basename = 'subproblem'
    else:
        basename = startname
    meshname = param.group['mesh'].value
    if meshname is not None:
        meshpath = labeltree.makePath(meshname)
        return ooflib.engine.subproblemcontext.subproblems.uniqueName(meshpath +
                                                                    [basename])

#############

def _new_subproblem(menuitem, name, mesh, subproblem):
##    if parallel_enable.enabled():
##        ## TODO MER: very out of date!
##        ipcsubpmenu.New(name=name, mesh=mesh, subproblem=subproblem)
##        return
    meshcontext = ooflib.engine.mesh.meshes[mesh]
    # 'subproblem' is a SubProblemType instance
    subpobj = subproblem.create()
    meshcontext.newSubProblem(subpobj,
                              subproblem,
                              labeltree.makePath(mesh)+[name])

subproblemMenu.addItem(oofmenu.OOFMenuItem(
    'New',
    callback=_new_subproblem,
    threadable=oofmenu.THREADABLE,
    params=parameter.ParameterGroup(
    whoville.AutoWhoNameParameter('name', value=automatic.automatic,
                                  resolver=subproblemNameResolver,
                                  tip="Name of the new SubProblem"),
    SyncMeshParameter('mesh', tip=parameter.emptyTipString),
    parameter.RegisteredParameter('subproblem',
                                  subproblemtype.SubProblemType,
                                  tip=parameter.emptyTipString)
    ),
    help="Define a new subproblem",
    discussion="""<para>

    Create a new &subproblem; in the given &mesh;.  If the given name
    is not unique in the &mesh;, <userinput>&lt;x&gt;</userinput> will
    be appended to it, where <userinput>x</userinput> is an integer
    chosen to make the name unique.  </para>
    """
    ))

#############

## TODO MER: A lot of code is shared between _copy_subproblem and
## _edit_subproblem and could possibly be shared.

def _copy_subproblem(menuitem, subproblem, mesh, name):
    if parallel_enable.enabled():
        ipcsubpmenu.Copy(name=name, mesh=mesh, subproblem=subproblem)
        return
    meshctxt = ooflib.engine.mesh.meshes[mesh]
    sourcectxt = ooflib.engine.subproblemcontext.subproblems[subproblem]
    if not sourcectxt.consistency():
       raise ooferror.ErrUserError('Subproblem being copied is not consistent!')
    sourceobj = sourcectxt.getObject()
    #Retrieving the tree of dependencies order for the less dependent subproblem to the most dependent one
    links = []
    sourcectxt.tree(links)
    links_update = []
    #Looping around the path of each subproblem from the ordered list
    for link in links:
        # Retrieve the path, the name and the context of the current subproblem
        subp_path = labeltree.makePath(link)
        subp_name = subp_path[-1]
        subp_ctxt = ooflib.engine.subproblemcontext.subproblems[link]
        create = False #Should the subproblem be created?
        if subp_ctxt != sourcectxt:
	   for subp in meshctxt.subproblems():
	       #Check that the subproblem has the same name and subptype 
	       if subp_name == subp.name():
		  if subp_ctxt.subptype.__class__ == subp.subptype.__class__:
		     create = True
		     links_update.append(subp.path())#Update with the path
		     break
	
	# If the subproblem does not exist in the target mesh subproblem
	# Copy the subproblem and update its dependencies since they might probably have
	# different paths if the target mesh is another one.
	# Create the subproblem copy all the original subproblem content 
	# Finally update the dependencies dependents and propagate the consistency.
	if create == False:
	   subptype_copy = copy.deepcopy(subp_ctxt.subptype)
	   
	   for dependency in  subptype_copy.get_dependencies():
	       dep_index = links.index(dependency)
	       update_path = links_update[dep_index]
	       subptype_copy.sync_dependency(dependency, update_path)
	       
	   copyobj = subptype_copy.create() # new CSubProblem
	   sourcectxt.begin_reading()
	   try:
	      fields = sourcectxt.all_compound_fields()
	      activefields = [field for field in fields
			      if sourcectxt.getObject().is_active_field(field)]
	      equations = sourceobj.all_equations()
	   finally:
	      sourcectxt.end_reading()
	   if subp_ctxt != sourcectxt:
	      copyctxt = meshctxt.newSubProblem(copyobj, subptype_copy,
					    mesh+':'+subp_name) # new context
	   else:
	      copyctxt = meshctxt.newSubProblem(copyobj, subptype_copy,
					    mesh+':'+name) # new context
	   copyname = copyctxt.path()
	   links_update.append(copyname)#Update with the new path

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
	  
	   #Update the dependencies dependents
	   for dependency in  copyctxt.subptype.get_dependencies():
	       dependencysubp = ooflib.engine.subproblemcontext.subproblems[dependency]
	       dependencysubp.subptype.remove_dependent(link)
	       dependencysubp.subptype.add_dependent(copyname)
	      
	   for dep in copyctxt.subptype.get_dependencies():
	       ooflib.engine.subproblemcontext.subproblems[dep].update_consistency()
        
           copyctxt.propagate_consistency([copyname])
	      

subproblemMenu.addItem(oofmenu.OOFMenuItem(
    'Copy',
    callback=_copy_subproblem,
    threadable=oofmenu.THREADABLE,
    params=parameter.ParameterGroup(
    whoville.WhoParameter('subproblem',
                          ooflib.engine.subproblemcontext.subproblems,
                          tip='The subproblem to be copied.'),
    SyncMeshParameter('mesh', tip='The copy will be in this mesh.'),
    whoville.AutoWhoNameParameter('name', value=automatic.automatic,
                                  resolver=subproblemNameResolver,
                                  tip="Name to give to the copy")
    ),
    help="Copy a subproblem.",
    discussion="""<para>
    Copy a &subproblem;, possibly to another &mesh;.  If the original
    &subproblem; is defined in terms of objects (&pixelgroups;,
    &materials;, <foreignphrase>etc.</foreignphrase> that don't exist
    in the destination &mesh;, then the copied &subproblem; will
    contain no &elems;.
    </para>"""
    ))

#############

def _edit_subproblem(menuitem, name, subproblem):
##    if parallel_enable.enabled():
##        ## TODO MER: out of date
##        ipcsubpmenu.Edit(name=name, subproblem=subproblem)
##        return
    oldsubp = ooflib.engine.subproblemcontext.subproblems[name]
    if oldsubp.name() == ooflib.engine.mesh.defaultSubProblemName:
        raise ooferror.ErrUserError("You can't edit the default Subproblem!")
    meshctxt = oldsubp.getParent()
    # Get the old dependents and dependencies for updates
    old_dependents = oldsubp.subptype.get_dependents()
    old_dependencies = oldsubp.subptype.get_dependencies()
    old_path = oldsubp.path()
       
    oldsubp.reserve()
    oldsubp.begin_writing()
    try:
        oldsubpobj = oldsubp.getObject()
        # Save lists of fields, etc, so that they can be restored in
        # the new subproblem.
        oldfields = oldsubp.all_compound_fields() # only CompoundFields
        oldactivefields = [field for field in oldfields
                           if oldsubpobj.is_active_field(field)]
        oldeqns = oldsubp.all_equations()
        oldsubp.clean()
    finally:
        oldsubp.end_writing()
        oldsubp.cancel_reservation()

    # Create the new subproblem object
    newsubpobj = subproblem.create()
    
    #Remove the path from the dependencies dependents:
    for dependency in old_dependencies:
        if old_path in ooflib.engine.subproblemcontext.subproblems[dependency].subptype.get_dependents():
           ooflib.engine.subproblemcontext.subproblems[dependency].subptype.remove_dependent(old_path)
    
    # Create context for new subproblem.
    newsubp = meshctxt.newSubProblem(newsubpobj, subproblem, name)
    meshctxt.reserve()
    meshctxt.begin_writing()
    # Gather switchboard messages and send them all after the lock has
    # been released.
    notifications = []
    try:
        # Restore field and equation state saved from old subproblem.
        for field in oldfields:
            newsubpobj.define_field(field)
            notifications.append(("field defined", name, field.name(), 1))
        for field in oldactivefields:
            newsubpobj.activate_field(field)
            notifications.append(("field activated", name, field.name(), 1))
        for eqn in oldeqns:
            newsubpobj.activate_equation(eqn)
            notifications.append(("equation activated", name, eqn.name(), 1))
    finally:
        meshctxt.end_writing()
        meshctxt.cancel_reservation()
    newsubp.autoenableBCs()
    
    #Update the dependents with the new object
    for dependent in old_dependents:
        dependentsubp = ooflib.engine.subproblemcontext.subproblems[dependent]
        newsubp.subptype.add_dependent(dependent)
        dependentsubp.reserve()
        dependentsubp.begin_writing()
        try:
	  dependentsubp.subptype.update_dependency(dependentsubp.getObject(), old_path, newsubp.getObject())
	finally:
	  dependentsubp.end_writing()
          dependentsubp.cancel_reservation()
    for dep in newsubp.subptype.get_dependencies():
        ooflib.engine.subproblemcontext.subproblems[dep].update_consistency()
        
    newsubp.propagate_consistency([old_path])
        
    for notice in notifications:
        switchboard.notify(*notice)
    newsubp.changed("Subproblem redefined.")

subproblemMenu.addItem(oofmenu.OOFMenuItem(
    'Edit',
    callback=_edit_subproblem,
    threadable=oofmenu.THREADABLE,
    params=[
    # This used to be just a StringParameter.  Why?
    whoville.WhoParameter('name', ooflib.engine.subproblemcontext.subproblems,
                          value=None,
                          tip='The name of the subproblem being edited.'),
    parameter.RegisteredParameter('subproblem', subproblemtype.SubProblemType,
                                  tip='The new value of the subproblem.')],
    help="Replace a subproblem with a new one.",
    discussion="""<para>

    This command changes the portion of a &mesh; that is contained in
    a given &subproblem;.  What it actually does is replace the
    &subproblem; with a new &subproblem; with the same name.  The
    &fields; and &equations; defined in the old &subproblem; are
    copied to the new one.

    </para>"""
    ))

#############

def _rename_subproblem(menuitem, subproblem, name):
    if parallel_enable.enabled():
        ipcsubpmenu.Rename(name=name, subproblem=subproblem)
        return
    oldpath = labeltree.makePath(subproblem)
    newpath = labeltree.makePath(subproblem)[:-1]+[name]
    subprob = ooflib.engine.subproblemcontext.subproblems[oldpath]
    old_dependents = subprob.subptype.get_dependents()
    if subprob.name() == ooflib.engine.mesh.defaultSubProblemName:
        raise ooferror.ErrUserError("You can't rename the default Subproblem!")
    for dependent in old_dependents:
        dependentsubp = ooflib.engine.subproblemcontext.subproblems[dependent]
        dependentsubp.subptype.sync_dependency(":".join(oldpath), ":".join(newpath))
    subprob.reserve()
    subprob.begin_writing()
    try:
        subprob.rename(name, exclude=oldpath[-1])
    finally:
        subprob.end_writing()
        subprob.cancel_reservation()

subproblemMenu.addItem(oofmenu.OOFMenuItem(
    'Rename',
    callback=_rename_subproblem,
    threadable=oofmenu.THREADABLE,
    params=[whoville.WhoParameter('subproblem',
                                  ooflib.engine.subproblemcontext.subproblems,
                                  tip=parameter.emptyTipString),
            whoville.WhoNameParameter('name', value='',
                                       tip='New name for the subproblem.')],
    help='Rename a Subproblem.',
    discussion="<para> Assign a new name to a &subproblem;</para>"))

#############

def _delete_subproblem(menuitem, subproblem):
    if parallel_enable.enabled():
        ipcsubpmenu.Delete(subproblem=subproblem)
        return
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

subproblemMenu.addItem(oofmenu.OOFMenuItem(
    'Delete',
    callback=_delete_subproblem,
    threadable=oofmenu.THREADABLE,
    params=[whoville.WhoParameter('subproblem',
                                  ooflib.engine.subproblemcontext.subproblems,
                                  tip=parameter.emptyTipString)],
    help='Delete a Subproblem.',
    discussion="<para>Delete the given &subproblem; from its &mesh;.</para>"
    ))


#############

#TODO 3.1: Interface branch, show edgement info
def _info_subproblem(menuitem, subproblem):
    if parallel_enable.enabled():
        ipcsubpmenu.Info(subproblem=subproblem)
        return
    subpctxt = ooflib.engine.subproblemcontext.subproblems[subproblem]
    subpctxt.begin_reading()
    if config.dimension() == 2:
        spanname = "area"
    else:
        spanname = "volume"
    try:
        reporter.report(
"""*** Subproblem Info ***
%s
%d elements
%d nodes
%s = %s""" % (subpctxt.subptype, subpctxt.nelements(), subpctxt.nnodes(),
              spanname, subpctxt.span()))
    finally:
        subpctxt.end_reading()

subproblemMenu.addItem(oofmenu.OOFMenuItem(
    'Info',
    callback=_info_subproblem,
    threadable=oofmenu.THREADABLE,
    params=[whoville.WhoParameter('subproblem',
                                  ooflib.engine.subproblemcontext.subproblems,
                                  tip=parameter.emptyTipString)],
    help="Print information about a subproblem",
    discussion="""<para>

    Print information about the given &subproblem;.  In graphics mode,
    the information appears in the message window.

    </para>"""))

###################################

fieldmenu = subproblemMenu.addItem(oofmenu.OOFMenuItem(
    'Field',
    help='Define and activate Fields.',
    discussion="""<para>
    The <command>Field</command> menu contains the commands that
    define and set the properties of &fields; on &meshes;.
    </para>"""))

def _defineField(menuitem, subproblem, field):
    if parallel_enable.enabled():
        ipcsubpmenu.Field.Define(subproblem=subproblem, field=field)
    else:
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
                    initializer.apply(subpcontext.getParent().getObject(),
                                      field, singleFieldDef=True)
                meshctxt.update_fields()
                didsomething = True
        finally:
            subpcontext.end_writing()
            subpcontext.cancel_reservation()
        if didsomething:
            subpcontext.autoenableBCs()
            subpcontext.changed("Field defined.")
            switchboard.notify("field defined", subproblem, field.name(), 1)
            switchboard.notify("redraw")

fieldmenu.addItem(oofmenu.OOFMenuItem(
    'Define',
    threadable=oofmenu.THREADABLE,
    callback=_defineField,
    params=[whoville.WhoParameter('subproblem',
                                  ooflib.engine.subproblemcontext.subproblems,
                                  tip=parameter.emptyTipString),
            meshparameters.FieldParameter('field', tip=parameter.emptyTipString)
    ],
    help="Define a Field on a Subproblem. Only defined Fields may be given values.",
    ## TODO 3.1: Fix discussion
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/definefield.xml')
    ))


def _undefineField(menuitem, subproblem, field):
    if parallel_enable.enabled():
        ipcsubpmenu.Field.Undefine(subproblem=subproblem,field=field)
    else:
        subpcontext = ooflib.engine.subproblemcontext.subproblems[subproblem]
        subpcontext.reserve()
        subpcontext.begin_writing()
        try:
            subpcontext.getObject().undefine_field(field)
            subpcontext.getParent().update_fields()
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
        switchboard.notify("field defined", subproblem, field.name(), 0)
        switchboard.notify("redraw")

fieldmenu.addItem(oofmenu.OOFMenuItem(
    'Undefine',
    threadable=oofmenu.THREADABLE,
    callback=_undefineField,
    params=[whoville.WhoParameter('subproblem',
                                  ooflib.engine.subproblemcontext.subproblems,
                                  tip=parameter.emptyTipString),
            meshparameters.FieldParameter('field', tip=parameter.emptyTipString)
            ],
    help="Undefine a Field on a Subproblem.  Only defined Fields may be given values.",
    discussion="""<para>

    Undefine a &field; on a &subproblem;.  This frees the memory used
    to store the &field; components and destroys their values, unless
    other &subproblems; are using the &field;.  See <xref
    linkend='MenuItem-OOF.Subproblem.Field.Define'/>.

    </para>"""
    ))

def _activateField(menuitem, subproblem, field):
    activation = False
    if parallel_enable.enabled():
        ipcsubpmenu.Field.Activate(subproblem=subproblem,field=field)
    else:
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
            subpcontext.changed("Field activated.")

def _deactivateField(menuitem, subproblem, field):
    deactivation = False
    if parallel_enable.enabled():
        ipcsubpmenu.Field.Deactivate(subproblem=subproblem,field=field)
    else:
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
            subpcontext.changed("Field deactivated.")

fieldmenu.addItem(oofmenu.OOFMenuItem(
    "Activate",
    threadable=oofmenu.THREADABLE,
    callback=_activateField,
    params=[whoville.WhoParameter('subproblem',
                                  ooflib.engine.subproblemcontext.subproblems,
                                  tip=parameter.emptyTipString),
            meshparameters.FieldParameter('field', tip=parameter.emptyTipString)
    ],
    help="Activate a Field.  The solver finds the values of active Fields.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/activatefield.xml')
    ))

fieldmenu.addItem(oofmenu.OOFMenuItem(
    'Deactivate',
    threadable=oofmenu.THREADABLE,
    callback=_deactivateField,
    params=[whoville.WhoParameter('subproblem',
                                  ooflib.engine.subproblemcontext.subproblems,
                                  tip=parameter.emptyTipString),
            meshparameters.FieldParameter('field', tip=parameter.emptyTipString)
            ],
    help="Deactivate a Field.  The solver finds the values of active Fields.",
    discussion="""<para>

    Deactivating a &field; means that its values will not be found
    when the &subproblem; is <link
    linkend="MenuItem-OOF.Mesh.Solve">solved</link>.  See <xref
    linkend='MenuItem-OOF.Subproblem.Field.Activate'/>.

    </para>"""
    ))


############################

eqnmenu = subproblemMenu.addItem(oofmenu.OOFMenuItem(
    'Equation', help='Activate equations.'))

def _activateEquation(menuitem, subproblem, equation):
    if parallel_enable.enabled():
        ipcsubpmenu.Equation.Activate(subproblem=subproblem,
                                          equation=equation)
    else:
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
        subpcontext.changed("Equation activated.")

def _deactivateEquation(menuitem, subproblem, equation):
    if parallel_enable.enabled():
        ipcsubpmenu.Equation.Deactivate(subproblem=subproblem,
                                            equation=equation)
    else:
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
        subpcontext.changed("Equation deactivated.")

eqnmenu.addItem(oofmenu.OOFMenuItem(
    'Activate',
    callback=_activateEquation,
    threadable=oofmenu.THREADABLE,
    params=[whoville.WhoParameter('subproblem',
                                  ooflib.engine.subproblemcontext.subproblems,
                                  tip=parameter.emptyTipString),
            meshparameters.EquationParameter('equation',
                                             tip=parameter.emptyTipString)
    ],
    help="Activate an Equation.  The Solver solves the active Equations.",
    discussion="""<para>

    Activate the given &equation; on the given &subproblem;. Activated
    &equations; are the ones that will be <link
    linkend='MenuItem-OOF.Mesh.Solve'>solved</link>.  For a solution
    to be possible, the active &equations; must involve &fluxes; that
    are produced by &properties; in the &mesh;, and those &properties;
    must couple to <link
    linkend='MenuItem-OOF.Subproblem.Field.Define'>defined</link> &fields;.
    There must be as many active &equations; as there are <link
    linkend='MenuItem-OOF.Subproblem.Field.Activate'>active</link> &fields;


    </para>"""
    ))

eqnmenu.addItem(oofmenu.OOFMenuItem(
    'Deactivate',
    callback=_deactivateEquation,
    threadable=oofmenu.THREADABLE,
    params=[whoville.WhoParameter('subproblem',
                                  ooflib.engine.subproblemcontext.subproblems,
                                  tip=parameter.emptyTipString),
            meshparameters.EquationParameter('equation',
                                             tip=parameter.emptyTipString)
    ],
    help="Deactivate an Equation.  The Solver solves the active Equations.",
    discussion="""<para>

    Deactivate the given &equation; on the given &subproblem;.  See <xref
    linkend='MenuItem-OOF.Subproblem.Equation.Deactivate'/>.

    </para>"""

    ))

#################################

# Copy the field state (definitions, active-ness, planarity) of one
# subproblem into another.

def _copyFieldState(menuitem, source, target):
    if source == target:
        raise ooferror.ErrUserError('Source and target must differ!')
    if parallel_enable.enabled():
        ipcsubpmenu.Copy_Field_State(source=source,target=target)
        return

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

            if config.dimension() == 2:
                # Planarity is really a mesh attribute, not a
                # subproblem attribute
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

    target_subp.changed("Fields changed.")
    switchboard.notify("redraw")



subproblemMenu.addItem(oofmenu.OOFMenuItem(
    'Copy_Field_State',
    callback=_copyFieldState,
    threadable=oofmenu.THREADABLE,
    params=[whoville.WhoParameter('source',
                                  ooflib.engine.subproblemcontext.subproblems,
                                  tip=parameter.emptyTipString),
            whoville.WhoParameter('target',
                                  ooflib.engine.subproblemcontext.subproblems,
                                  tip=parameter.emptyTipString)],
    help="Copy the Field state (defined, active, etc) from one Subproblem to another.",
    discussion="""<para>

    This command copies the &field; state from one &subproblem; to
    another, meaning that the same &fields; will be defined, active,
    and in-plane in the <varname>target</varname> &subproblem; as in
    the <varname>source</varname> &subproblem;.  If &fields; were
    explicitly <link
    linkend='MenuItem-OOF.Mesh.Set_Field_Initializer'>initialized</link>
    in the source &subproblem;, the initializers will be copied, but
    the command does <emphasis>not</emphasis> copy the &field; values.
    (This is because the source and target meshes might have quite
    different geometries.)

    </para>"""
                        ) )



# Likewise for equation state.

def _copyEquationState(menuitem, source, target):
    if source == target:
        raise ooferror.ErrUserError('Source and target must differ!')
    if parallel_enable.enabled():
        ipcsubpmenu.Copy_Equation_State(source=source,target=target)
        return

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
    target_subp.changed("Equations changed.")


subproblemMenu.addItem(oofmenu.OOFMenuItem(
    'Copy_Equation_State',
    callback=_copyEquationState,
    threadable=oofmenu.THREADABLE,
    params=[whoville.WhoParameter('source',
                                  ooflib.engine.subproblemcontext.subproblems,
                                  tip=parameter.emptyTipString),
            whoville.WhoParameter('target',
                                  ooflib.engine.subproblemcontext.subproblems,
                                  tip=parameter.emptyTipString)],
    help="Copy the set of active Equations from one Subproblem to another.",
    discussion="""<para>

    This command copies the &equation; state from one &subproblem; to
    another, meaning that the same &equations; will be active in the
    <varname>target</varname> &subproblem; as in the
    <varname>source</varname> &subproblem;.

    </para>"""

    ) )

######################################

# Time-dependent solver stuff

def _setSolvable(menuitem, subproblem):
    subpctxt = ooflib.engine.subproblemcontext.subproblems[subproblem]
    subpctxt.begin_writing()
    try:
        subpctxt.solveFlag = True
        fieldsdefined = subpctxt.define_timederiv_fields()
    finally:
        subpctxt.end_writing()
    switchboard.notify("subproblem solvability changed", subproblem)
    for fld in fieldsdefined:
        switchboard.notify("field defined", subproblem, fld.name(), 1)
    subpctxt.getParent().setStatus(
        meshstatus.Unsolved("Solvability changed"))

def _unsetSolvable(menuitem, subproblem):
    subpctxt = ooflib.engine.subproblemcontext.subproblems[subproblem]
    subpctxt.begin_writing()
    try:
        subpctxt.solveFlag = False
    finally:
        subpctxt.end_writing()
    switchboard.notify("subproblem solvability changed", subproblem)
    subpctxt.getParent().setStatus(
        meshstatus.Unsolved("Solvability changed"))

subproblemMenu.addItem(oofmenu.OOFMenuItem(
    'Enable_Solution',
    callback=_setSolvable,
    threadable=oofmenu.THREADABLE,
    params=[whoville.WhoParameter('subproblem',
                                  ooflib.engine.subproblemcontext.subproblems,
                                  tip=parameter.emptyTipString)],
    help="Enable a subproblem's solution by the next Solve command.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/enablesoln.xml')))

subproblemMenu.addItem(oofmenu.OOFMenuItem(
    'Disable_Solution',
    callback=_unsetSolvable,
    threadable=oofmenu.THREADABLE,
    params=[whoville.WhoParameter('subproblem',
                                  ooflib.engine.subproblemcontext.subproblems,
                                  tip=parameter.emptyTipString)],
    help="Prevent a subproblem's solution by the next Solve command.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/disablesoln.xml')))

################

def _setSolver(menuitem, subproblem, solver_mode):
    subpctxt = ooflib.engine.subproblemcontext.subproblems[subproblem]
    subpctxt.begin_writing()
    try:
        subpctxt.solver_mode = solver_mode
        fieldsdefined = subpctxt.define_timederiv_fields()
    finally:
        subpctxt.end_writing()
    switchboard.notify("subproblem solver changed", subproblem)
    for fld in fieldsdefined:
        switchboard.notify("field defined", subproblem, fld.name(), 1)
    subpctxt.getParent().setStatus(meshstatus.Unsolved("Solver changed"))

subproblemMenu.addItem(oofmenu.OOFMenuItem(
        'Set_Solver',
        callback=_setSolver,
        threadable=oofmenu.THREADABLE,
        params=[
            whoville.WhoParameter('subproblem',
                                  ooflib.engine.subproblemcontext.subproblems,
                                  tip=parameter.emptyTipString),
            parameter.RegisteredParameter(
                'solver_mode',
                solvermode.SolverMode,
                tip="Various ways to set time-stepping parameters.")
            ],
        help="Specify the solution method for a subproblem.",
        discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/setsolver.xml')
        ))

################

def _copySolver(menuitem, source, target):
    sourceCtxt = ooflib.engine.subproblemcontext.subproblems[source]
    targetCtxt = ooflib.engine.subproblemcontext.subproblems[target]
    sourceCtxt.begin_reading()
    try:
        solver = sourceCtxt.solver_mode.clone()
    finally:
        sourceCtxt.end_reading()
    _setSolver(menuitem, target, solver)

subproblemMenu.addItem(oofmenu.OOFMenuItem(
        'Copy_Solver',
        callback=_copySolver,
        params=[
            whoville.WhoParameter('source',
                                  ooflib.engine.subproblemcontext.subproblems,
                                  tip="Subproblem to copy the solver from."),
            whoville.WhoParameter('target',
                                  ooflib.engine.subproblemcontext.subproblems,
                                  tip="Subproblem to which to copy the solver.")
            ],
        help="Copy a solver from one subproblem to another.",
        discussion=xmlmenudump.loadFile(
            'DISCUSSIONS/engine/menu/copysolver.xml')
        ))

################

def _removeSolver(menuitem, subproblem):
    subpctxt = ooflib.engine.subproblemcontext.subproblems[subproblem]
    subpctxt.begin_writing()
    try:
        subpctxt.solver_mode = None
    finally:
        subpctxt.end_writing()
    switchboard.notify("subproblem solver changed", subproblem)
    subpctxt.getParent().setStatus(meshstatus.Unsolved("Solver removed"))

subproblemMenu.addItem(oofmenu.OOFMenuItem(
    'Remove_Solver',
    callback=_removeSolver,
    threadable=oofmenu.THREADABLE,
    params=[whoville.WhoParameter('subproblem',
                                  ooflib.engine.subproblemcontext.subproblems,
                                  tip=parameter.emptyTipString)],
    help="Unspecify the solution method for a subproblem.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/removesolver.xml')
    ))


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# The SymmetryTest menu is for testing and debugging.  It doesn't
# appear in the GUI.  The commands in it are called by the regression
# test.  The functions can't be called directly (without using menu
# commands) because they acquire locks, which can't be used on the
# main thread.  Using menu commands is an easy way to move the locks
# to subthreads.

_symmetryTestMenu = subproblemMenu.addItem(oofmenu.OOFMenuItem(
        'SymmetryTest',
        help='Testing tools for checking matrix symmetry',
        secret=1))

def _checkSymmetry(subproblem, material, fn, symmetric):
    subpctxt = ooflib.engine.subproblemcontext.subproblems[subproblem]
    mat = materialmanager.getMaterial('material')
    if fn(subpctxt, mat) != symmetric:
        raise ooferror.ErrPyProgrammingError("symmetry check failed")

def _checkSymmetryK(menuitem, subproblem, material, symmetric):
    _checkSymmetry(subproblem,
                   material,
                   lambda sub, mat: mat.is_symmetric_K(sub),
                   symmetric)

def _checkSymmetryC(menuitem, subproblem, material, symmetric):
    _checkSymmetry(subproblem,
                   material,
                   lambda sub, mat: mat.is_symmetric_C(sub),
                   symmetric)

def _checkSymmetryM(menuitem, subproblem, material, symmetric):
    _checkSymmetry(subproblem,
                   material,
                   lambda sub, mat: mat.is_symmetric_M(sub),
                   symmetric)

_symTestParams = [
    whoville.WhoParameter('subproblem',
                          ooflib.engine.subproblemcontext.subproblems),
    parameter.StringParameter('material'),
    parameter.BooleanParameter('symmetric')
    ]

_symmetryTestMenu.addItem(oofmenu.OOFMenuItem(
        'K',
        callback=_checkSymmetryK,
        params=_symTestParams,
        help="Check K matrix symmetry.",
        secret=True, no_doc=True))

_symmetryTestMenu.addItem(oofmenu.OOFMenuItem(
        'C',
        callback=_checkSymmetryC,
        params=_symTestParams,
        help="Check K matrix symmetry.",
        secret=True, no_doc=True))

_symmetryTestMenu.addItem(oofmenu.OOFMenuItem(
        'M',
        callback=_checkSymmetryM,
        params=_symTestParams,
        help="Check K matrix symmetry.",
        secret=True, no_doc=True))
