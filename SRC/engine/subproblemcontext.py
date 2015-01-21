# -*- python -*-
# $RCSfile: subproblemcontext.py,v $
# $Revision: 1.78.2.19 $
# $Author: fyc $
# $Date: 2015/01/07 15:53:12 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.SWIG.common import config
from ooflib.SWIG.common import doublevec
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common import timestamp
from ooflib.SWIG.engine import field
from ooflib.SWIG.engine import flux
from ooflib.SWIG.engine import ooferror2
from ooflib.SWIG.engine import sparsemat
from ooflib.common import debug
from ooflib.common import utils
from ooflib.common.IO import parameter
from ooflib.common.IO import whoville
from ooflib.engine import mesh
from ooflib.engine import symstate
from ooflib.engine import meshstatus
from ooflib.engine import nonlinearsolver
from ooflib.engine import timestepper
from ooflib.engine import solverstats
import string
import sys

class SubProblemContext(whoville.Who):
    def __init__(self, name, classname, obj, parent, subptype, secretFlag=0):
        whoville.Who.__init__(self, name, classname, obj, parent, secretFlag)
        obj.set_rwlock(self.rwLock)
        # Obj is a CSubProblem.

	consistencyFlag = True
	
	# Checking the direct dependency of the newly created
	# subproblem. If one of its dependencies is not consistent
	# then the newly created subproblem will not be consistent.
	for sub in subptype.get_dependencies():
	    consistencyFlag = consistencyFlag and subproblems[sub].consistency()
	    if consistencyFlag == False:
	       break

	obj.consistency = consistencyFlag

        obj.set_mesh(parent.getObject())
        obj.set_nnodes(self.nfuncnodes())

        # These shouldn't be accessed directly.  They store the values
        # of properties defined below..
        self._solver_mode = None
        self._time_stepper = None
        self._nonlinear_solver = None
        self._symmetric_solver = None
        self._asymmetric_solver = None

        self.stepperSet = timestamp.TimeStamp()

        self.startTime = 0.0
        self.endTime = None
        self.installedTime = None
        self.fieldsInstalled = timestamp.TimeStamp()
        self.startValues = doublevec.DoubleVec(0)
        self.endValues = doublevec.DoubleVec(0)
        self.subptype = subptype
        self._precomputing = False
        self._timeDependent = False
        self._second_order_fields = set()

        # solveOrder determines the order in which subproblems are to
        # be solved.
        self.solveOrder = parent.nSubproblems()
        # solveFlag indicates whether or not the subproblem is to be
        # solved at all.
        self.solveFlag = True

        self.defnChanged = timestamp.TimeStamp() # fields or eqns changed
        self.solutiontimestamp = timestamp.TimeStamp() # last "solve" command
        self.solutiontimestamp.backdate()

        self.solverStats = solverstats.SolverStats()
        self.newMatrixCount = 0 # no. of time matrices have been rebuilt.

        self.requestCallback(("preremove who", "SubProblem"),
                             self.preremoveCB)
        self.requestCallback("subproblem redefined", self.redefinedCB)

        self.matrix_symmetry_K = symstate.SymState()
        self.matrix_symmetry_C = symstate.SymState()
        self.matrix_symmetry_M = symstate.SymState()

        # If a SubProblemType's Registration has a callable 'startup'
        # member, it's invoked here.  This can be used to set up
        # switchboard signals, for instance.  A corresponding
        # 'cleanup' function is called when the subproblem is
        # destroyed.
        try:
            startupfn = self.subptype.getRegistration().startup
        except AttributeError:
            pass
        else:
            startupfn(self)
        
        for dependency in subptype.get_dependencies():
	    path = self.getParent().path()+":"+name 
	    if path not in subproblems[dependency].subptype.get_dependents():
	       subproblems[dependency].subptype.add_dependent(path)
	       
	## We needed to check that nothing else is changing the
	## secrecy of subproblemcontext.  For now it is. But if any
	## change has to change this flag we will have to proceed in
	## fixing the TODO about Who secretFlag in Whoville.py which
	## means also WhoClass secret.
	if self.consistency():
	   self.secretFlag = 0
	else:
	   self.secretFlag = 1

    # solver_mode, time_stepper, nonlinear_solver, symmetric_solver,
    # and asymmetric_solver are implemented as python properties,
    # mostly so that old code that expected time_stepper and
    # nonlinear_solver to be data members of SubProblemContext doesn't
    # have to be changed.  time_stepper and nonlinear_solver, as well
    # as symmetric_solver and asymmetric_solver are actually retrieved
    # from solver_mode, which is either a BasicSolverMode or an
    # AdvancedSolverMode (for users who want to control everything
    # themselves).  The SubProblemContext, of course, doesn't need to
    # know which type of SolverMode is being used.
    def _setSolverMode(self, mode):
        self._solver_mode = mode
        self.stepperSet.increment()
        if mode is not None:
            # Tell the CSubProblem whether or not the stepper is
            # static.
            stepper = mode.get_time_stepper(self, self._time_stepper)
            if stepper is not None:
                self.getObject().setStaticStepper(stepper.derivOrder()==0)
        self.getObject().requirePrecompute()
        self.findTimeDependent()
        self.find_second_order_fields()
    def _getSolverMode(self):
        return self._solver_mode
    def _getTimeStepper(self):
        if self._solver_mode:
            self._time_stepper = self._solver_mode.get_time_stepper(
                self, self._time_stepper)
            return self._time_stepper
    def _getNonlinearSolver(self):
        if self._solver_mode:
            self._nonlinear_solver = self._solver_mode.get_nonlinear_solver(
                self, self._nonlinear_solver)
            self._nonlinear_solver.subproblem = self
            return self._nonlinear_solver
    def _getSymmetricSolver(self):
        if self._solver_mode:
            self._symmetric_solver = self._solver_mode.get_symmetric_solver(
                self, self._symmetric_solver)
            return self._symmetric_solver
    def _getAsymmetricSolver(self):
        if self._solver_mode:
            self._asymmetric_solver = self._solver_mode.get_asymmetric_solver(
                self, self._asymmetric_solver)
            return self._asymmetric_solver

    solver_mode = property(_getSolverMode, _setSolverMode)
    time_stepper = property(_getTimeStepper)
    nonlinear_solver = property(_getNonlinearSolver)
    symmetric_solver = property(_getSymmetricSolver)
    asymmetric_solver = property(_getAsymmetricSolver)

    def matrix_method(self, asympredicate, *args, **kwargs):
        # Use the given asympredicate to decide whether to return the
        # symmetric or asymmetric matrix solver. 

        # Call solver_precompute here, because whether or not a solver
        # requires a symmetric solver depends on which matrices are
        # being solved, which can depend on whether or not there are
        # second order time derivatives, which can only be determined
        # after precomputing.
        self.solver_precompute()

        # MatrixSolverWrapper wraps the solver's "solve" command so
        # that the subproblem can accumulate statistics on the
        # solution process.
        if asympredicate(*args, **kwargs):
            result = MatrixSolverWrapper(self, self.asymmetric_solver)
        else:
            result = MatrixSolverWrapper(self, self.symmetric_solver)
        return result

    # asymmetricK and asymmetricC can be used as arguments to
    # matrix_method().
    def asymmetricK(self):
        return self.matrix_symmetry_K == symstate.ASYMMETRIC
    def asymmetricC(self):
        return self.matrix_symmetry_C == symstate.ASYMMETRIC
        
    # Generate the tree of dependencies from the less dependent subproblem to the most dependent one.
    # We ensure no duplicate
    def tree(self, links):
        for dependency in self.subptype.get_dependencies():
	    if dependency not in links:
	       subproblems[dependency].tree(links)
	if self.path() not in links:
	   links.append(self.path())
	for dependent in self.subptype.get_dependents():
	    if dependent not in links:
	       subproblems[dependent].tree(links)
        

    def clone(self, newmesh, copy_field, copy_equation, notifications):
        # Create a copy of this subproblem in the given mesh, which is
        # either our mesh or a copy of it.  'notifications' is a set
        # of switchboard messages which will be sent by the calling
        # function when all the cloning is complete.
        subp = self.getObject()
        newsubptype = self.subptype.clone()
        newsubpobj = newsubptype.create()
        # create new subproblem context with a temporary name so that
        # it won't overwrite an old subproblem until we're done with
        # the old one (in case we're recreating an old subproblem, as
        # in the Revert mesh modifier).  It's up to the caller to
        # delete the original subproblems and rename the new ones.
        desiredname = newmesh.path() + ':' + self.name()
        temppath = newmesh.path() + ":" + subproblems.uniqueName(desiredname)
        newsubpctxt = newmesh.newSubProblem(newsubpobj, newsubptype, temppath)
        oldmesh = self.getParent()
        # CSubProblem.set_mesh() must have been called with the new
        # meshctxt *before* this point, or new DoFs and NodalEqns
        # won't be stored in the right object.  Mesh.setFEMesh must be
        # called *before* calling CSubProblem.set_mesh() because it
        # uses Mesh.getObject() to get the FEMesh.  But if we do that,
        # then the field planarities won't be retrieved correctly from
        # the Mesh, because it will use the wrong FEMesh.  Therefore,
        # this routine does not set the planarity at all. Planarity
        # isn't really a subproblem responsibility anyway.
        if copy_field:
            for field in self.all_compound_fields():
                newsubpobj.define_field(field)
                notifications.add(
                    ("field defined", desiredname, field.name(), 1))
                if subp.is_active_field(field):
                    newsubpobj.activate_field(field)
                    notifications.add(("field activated",
                                       desiredname, field.name(), 1))
        if copy_equation:
            for eqn in self.all_equations():
                newsubpobj.activate_equation(eqn)
                notifications.add(
                    ("equation activated", desiredname, eqn.name(), 1))
        if self.solver_mode is not None:
            newsubpctxt.solver_mode = self.solver_mode.clone()
        
        # The times and dof values, etc, will be reset when the fields
        # are initialized, which isn't done here. installedTime,
        # startValues, and endValues don't have to be set here at all.
        newsubpctxt.startTime = 0.0
        newsubpctxt.endTime = None

        newsubpctxt.solveFlag = self.solveFlag
        return newsubpctxt

    def preremoveCB(self, path):
        #debug.dumpTrace()
        # If one of our dependencies is being removed, we're done for.
        # We might as well end it all right now.
        path = string.join(path, ':')
        if path in self.subptype.get_dependents():
	   self.subptype.remove_dependent(path)
        if path in self.subptype.get_dependencies():
	    if self.getObject() != None:
	      if self.consistency():
		  self.reserve()
		  self.begin_writing()
		  try:
		      self.destroy()
		  finally:
		      self.end_writing()
		      self.cancel_reservation()
	      else:
		  self.reserve()
		  self.begin_writing()
		  try:
		    self.clean()
		  finally:
		      self.end_writing()
		      self.cancel_reservation()

    def destroy(self):
        #debug.dumpTrace()
        # See 'startup' comment in __init__.
        if hasattr(self.subptype, 'cleanup'):
           self.subptype.cleanup()
            
        # Undefine all of our fields and deactivate equations, so that
        # they'll be removed from the Mesh if they're no longer
        # needed.
        for fld in self.all_compound_fields():
            self.getObject().undefine_field(fld)
        for eqn in self.all_equations():
            self.getObject().deactivate_equation(eqn)
        self.getObject().mesh = None
        subproblems.remove(self.path())
        from ooflib.engine import evolve
        evolve.removeSubProblem(self)

        # Clear startValues and endValues.  If the SubProblemContext
        # is garbage-collected properly, this shouldn't be necessary,
        # but if it ever again acquires a base class with a __del__
        # method, there's a chance that garbage collection will fail,
        # and startValues and endValues can be large objects.
        self.startValues = []
        self.endValues = []
        
    def consistency(self):
        return self.getObject().consistency
        
    def update_consistency(self):
        consistencyFlag = True
	for sub in self.subptype.get_dependencies():
	    consistencyFlag = consistencyFlag and subproblems[sub].consistency()
	    if sub in self.subptype.get_dependents():
	       consistencyFlag = False
	       break
	self.getObject().consistency = consistencyFlag
	if self.consistency():
	   self.secretFlag = 0
	else:
	   self.secretFlag = 1
	      
    def propagate_consistency(self, paths):
        #print "propagate_consistency: " + self.path()
        filter_paths = paths
        self.update_consistency()
	for sub in self.subptype.get_dependents():
	    if sub not in filter_paths:
	       filter_paths.append(self.path())
	       subproblems[sub].propagate_consistency(filter_paths)
    
    def clean(self):
        #debug.dumpTrace()
        # See 'startup' comment in __init__.
        if hasattr(self.subptype, 'cleanup'):
            self.subptype.cleanup()
        # Undefine all of our fields and deactivate equations, so that
        # they'll be removed from the Mesh if they're no longer
        # needed.
        for fld in self.all_compound_fields():
            self.getObject().undefine_field(fld)
        for eqn in self.all_equations():
            self.getObject().deactivate_equation(eqn)
        self.getObject().mesh = None
        subproblems.clean(self.path())
        from ooflib.engine import evolve
        evolve.removeSubProblem(self)

    def getMicrostructure(self):
        return self.getParent().getMicrostructure()

    def nelements(self):
        return self.getObject().nelements()

    def nnodes(self):
        return self.getObject().nnodes()

    def nfuncnodes(self):
        return self.getObject().nfuncnodes()

    def span(self):             # area in 2D and volume in 3D
        a = 0.0
        for element in self.getObject().elements():
            a += element.span()
        return a

    def solved(self):
        switchboard.notify("subproblem changed", self)

    def changed(self, message):
        # Called when fields, equations, or materials have changed.
        self.defnChanged.increment()    # timestamp
        self.getObject().requirePrecompute()
        self.findTimeDependent()
        self.find_second_order_fields()
        switchboard.notify("subproblem changed", self)
        self.parent.setStatus(meshstatus.Unsolved("mesh changed"))

        fieldsdefined = self.define_timederiv_fields()
        for fld in fieldsdefined:
            switchboard.notify("field defined", self.path(), fld.name(), 1)

        self.getParent().setStatus(meshstatus.Unsolved(message))

    def redefined(self):
        # Called when the things affecting the subproblem definition
        # itself have changed.  For example, a MaterialSubProblem is
        # redefined when its Material is assigned to or removed from
        # pixels.
        self.getObject().redefined()
        switchboard.notify("subproblem redefined", self.path())

    def redefinedCB(self, subppath):
        for dep in self.subptype.get_dependencies():
            if dep == subppath:
                self.redefined()

    def has_solution(self):
        return self.solutiontimestamp > max(self.defnChanged,
                                            self.parent.getOwnTimeStamp())

    def getTimeStamp(self):
        # This does *not* check the timestamp of the parent
        # meshcontext, because the mesh's getTimeStamp function checks
        # the timestamps of all of its subproblems.  That's because
        # changes in a subproblem must cause a mesh to be redrawn.
        return max(self.defnChanged, self.solutiontimestamp)

    def all_compound_fields(self):
        return self.getObject().all_compound_fields()

    def all_fields(self):
        compound_fields = self.all_compound_fields()
        if config.dimension() == 2:
            zfields = [fld.out_of_plane() for fld in compound_fields]
        else:
            zfields = []
        tfields = [fld.time_derivative() for fld in compound_fields]
        tfields = [t for t in tfields if self.is_defined_field(t)]
        return compound_fields + zfields + tfields

    def all_active_fields(self):
        return [f for f in self.all_fields() if self.is_active_field(f)]

    def all_equations(self):    # all *active* equations
        return self.getObject().all_equations()
    def all_equations_bc(self):
        eqns =  [eq for eq in self.getObject().all_equations()
                if eq.allow_boundary_conditions()]
        return eqns
    def is_active_equation(self, eqn):
        return self.getObject().is_active_equation(eqn)

    def all_fluxes(self):
        fluxes = self.getObject().all_fluxes()
        return [flux.allFluxes[f.name()] for f in fluxes]

    def is_defined_field(self, fld):
        return fld.is_defined(self.getObject())
    def is_active_field(self, fld):
        csub = self.getObject()
        return fld.is_defined(csub) and fld.is_active(csub)
    def is_second_order_field(self, fld):
        # Does the second time derivative of the given field appear in
        # the subproblem's active equations?
        self.solver_precompute()
        if self.is_active_field(fld):
            for material in self.getObject().getMaterials():
                if material.is_second_order_field(self.getObject(), fld,
                                                  self.all_equations()):
                    return True
        return False

    def find_second_order_fields(self):
        self._second_order_fields = set()
        for fld in self.all_compound_fields():
            if self.is_second_order_field(fld):
                self._second_order_fields.add(fld)
    def second_order_fields(self):
        return self._second_order_fields

    def define_timederiv_fields(self):
        # Make sure that the time derivative fields are defined if
        # needed.  They're possibly needed if a non-static solver is
        # being used.  Some solvers require time derivatives for all
        # fields.  Others need them just for fields whose second
        # derivatives appear in the equations.

        # Time derivatives are required for all fields if they're
        # required for any.

        # Called by OOF.Subproblem.Set_Solver,
        # OOF.Subproblem.Schedule_Solution, and
        # SubProblemContext.changed().
        newfields = set()
        if (self.solveFlag and self.solver_mode and
            self.time_stepper.derivOrder() > 0):
            tdrequired = self.time_stepper.require_timederiv_field()
            if tdrequired:
                fields = self.all_compound_fields()
            else:
                fields = self.second_order_fields()
            for fld in fields:
                td = fld.time_derivative()
                if self.getObject().define_field(td):
                    newfields.add(td)
                if config.dimension() == 2:
                    oop = fld.out_of_plane()
                    if self.is_defined_field(oop): # and tdrequired:
                        td = fld.out_of_plane_time_derivative()
                        if self.getObject().define_field(td):
                            newfields.add(td)
        return newfields

    def solver_precompute(self, solving=False):
        # Called before time-stepping.  This routine precomputes
        # things that can't possibly be time-dependent.  Called by
        # Mesh.solver_precompute(), which is called by the Solve
        # menuitem callback before calling evolve().
        debug.subthreadTest()
        if self._precomputing:
            return
        if self.solveFlag and self.solver_mode is not None:
            subprob = self.getObject()
            subprob.precomputeLock.acquire()
            self._precomputing = True
            try:
                if subprob.precomputeRequired:
                    # Check that materials are well defined, etc.
                    # Being badly defined isn't an error unless we're
                    # actually trying to solve a problem now.  If
                    # we're just precomputing to find out if the Solve
                    # button should be sensitized, or something like
                    # that, it's ok to simply bail out without raising
                    # an exception.
                    unsolvable = self.checkSolvability()
                    if unsolvable:
                        if solving:
                            raise ooferror2.ErrUserError(unsolvable)
                        else:
                            return

                    self.precomputeMaterials(lock=False)

                    # Find mapping for symmetrization.
                    # find_equation_mapping calls
                    # CSubProblem::set_equation_mapping, which is a
                    # fairly expensive operation, since it loops over
                    # all nodal equations.
                    from ooflib.engine import conjugate # avoid import loop
                    conjugate.listofconjugatepairs.find_equation_mapping(self)
                    conjugate.check_symmetry(self.path())
                    subprob.precomputeRequired = False
            finally:
                self._precomputing = False
                subprob.precomputeLock.release()

    def precomputeMaterials(self, lock=True):
        subprob = self.getObject()
        if lock:
            subprob.precomputeLock.acquire()
        try:
            fields = self.all_active_fields()
            ## TODO 3.1: does getMaterials include interface materials?
            for mat in subprob.getMaterials():
                if mat:
                    mat.precompute(subprob, fields)
        finally:
            if lock:
                subprob.precomputeLock.release()

    def solver_postcompute(self):
        # Called after time-stepping, to balance solver_precompute.
        pass

    # This function must be called after fields or equations are added
    # to or removed from this subproblem -- BCs which have become
    # incomputable will shut themselves off, and those which have
    # become computable will switch themselves on.
    def autoenableBCs(self):
        self.reserve()
        self.begin_writing()
        try:
            for (name, bc) in self.parent.allBoundaryConds():
                bc.auto_enable(self)
        finally:
            self.end_writing()
            self.cancel_reservation()
        # Mild abuse of this switchboard callback, with placeholder args.
        switchboard.notify("boundary conditions changed", self, None, True)

    def timeDependent(self):
        return self._timeDependent

    def findTimeDependent(self):
        debug.subthreadTest()
        self._timeDependent = (self.solveFlag and self.solver_mode is not None
                               and self.time_stepper.derivOrder() != 0)

    # Find the lowest time derivative in all equations.  That is,
    # return 2 if *all* active equations have second time derivative
    # terms in *all* materials, or 1 if all have at least first
    # derivatives, or 0 if any are static.  This is used to determine
    # if there are equations whose order is less than the order of
    # their solver, and therefore need special initialization.
    def lowestTimeDerivative(self):
        minorder = None
        for eqn in self.all_equations():
            if self.is_active_equation(eqn):
                for mat in self.getObject().getMaterials():
                    order = 0
                    for prop in mat.properties():
                        reg = prop.registration()
                        if reg.second_order_fields(eqn):
                            order = 2
                        elif reg.first_order_fields(eqn):
                            order = max(order, 1)
                    if order == 0:
                        return 0 # can't get any lower than this
                    if minorder is None or order < minorder:
                        minorder = order
        return minorder


    # Function to assess the well-posedness of the current state.
    # Returns None if the problem is well-posed or not being solved,
    # or returns a message string indicating what's wrong.

    def checkSolvability(self):
        if self.solver_mode is not None and self.solveFlag:
            status = []
            badmatls = self.getObject().check_materials()
            badeqns = self.getObject().check_equations()
            neqns = self.getObject().nEquations()
            ndofs = self.getObject().nDoFs()

            if badmatls or badeqns or neqns!=ndofs: # or badstepper:
                status.append("Subproblem '%s' is ill-posed!" % self.name())
                if ndofs == 0:
                    status.append("There are no active fields.")
                elif neqns == 0:
                    status.append("There are no active equations.")
                elif neqns > ndofs:
                    status.append(
                        "There are too few active fields (%d)"
                        " or too many active equations (%d)." % (ndofs, neqns))
                elif ndofs > neqns:
                    status.append(
                        "There are too few active equations (%d)"
                        " or too many active fields (%d)." % (neqns, ndofs))
                if badmatls:
                    status.append("Badly defined material%s!" %
                                  ("s"*(len(badmatls)>1)))
                    for matl in badmatls:
                        status.extend("  " + msg
                                      for msg in matl.consistency_messages())
                if badeqns:
                    for eqn in badeqns:
                        ## TODO 3.1: Equations should generate their
                        ## own error messages, since this one applies
                        ## only to FluxEquations.  This will be
                        ## important for plasticity.
                        status.append("Equation '%s' has no flux contributions"
                                      % eqn.name())
            status.extend(self.getParent().checkBdyConditions())
            return "\n   ".join(status)

    def materialsConsistent(self):
        # check_materials returns a list of inconsistent materials
        return ((not self.getObject().check_materials()) and
                (not self.getObject().check_equations()))

    def nonlinear(self, fields):
        # Must be called after Material.precompute
        for material in self.getObject().getMaterials():
            if material.nonlinear(self.getObject(), fields):
                return True
        return False

    def nonlinear_activefields(self):
        return self.nonlinear(self.all_active_fields())

    def timeDependentProperties(self, fields):
        for material in self.getObject().getMaterials():
            if material.timeDependent(self.getObject(), fields):
                return True
        return False

    def timeDependentBCs(self):
        # TODO OPT: This is too general.  Only query bcs that affect
        # *this* subproblem.
        mesh = self.getParent()
        return mesh.timeDependentBCs()

    def solver_string(self):
        return self.solver_mode.shortrepr()

    def resetStats(self):
        self.solverStats.reset()
        self.newMatrixCount = 0

    def all_materials(self):
        return self.getObject().getMaterials()

    #=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

    def make_linear_system(self, time, linsys):
        # Construct a LinearizedSystem object containing the
        # globally-indexed K, C, and M matrices, and the rhs vectors,
        # and the maps that extract submatrices and subvectors.

        # The linsys argument is either a LinearizedSystem object
        # previously created by this SubProblemContext, or None.  If
        # it's not None, it will be updated and reused.

        mesh    = self.getParent()
        femesh  = mesh.getObject()
        subpobj = self.getObject()
        mesh.restoreLatestData()
        try:
            # Ask every *other* subproblem to interpolate its DoFs to the
            # given time.  Our boundary conditions and/or material
            # properties may depend on them.
            for subproblem in mesh.subproblems():
                if (subproblem is not self and subproblem.installedTime!=time):
                    vals = subproblem.interpolateValues(time)
                    # This requires that the LinearizedSystem for the
                    # other subproblem has already been computed.
                    # However, it's never needed on the first call to
                    # make_linear_system, so that's ok.
                    subproblem.set_mesh_dofs(vals, time)

            ## TODO OPT: Be more sophisticated here. Instead of
            ## recomputing everything, only recompute the matrices and
            ## vectors that may have changed.

            ## TODO OPT: Recompute if nonlinear *and* relevant fields
            ## have changed, not just if nonlinear.  Need field-specific
            ## timestamps in the Mesh? 

            femesh.setCurrentSubProblem(self.getObject())

            # Figure out which parts of the calculation have to be redone.
            # If always is set, all steps of the calculation will be
            # peformed, even if they're otherwise unnecessary.  This can
            # be useful when debugging.

            # 'always' can be set with the command line option 
            ##     --command "always=True".
            always = False   
            try:
                always = utils.OOFeval('always')
            except NameError:
                pass

            # If Properties depend nonlinearly on Fields, and if those
            # Fields have changed, the matrices need to be recomputed.
            # The relevant Fields are *all* the Fields defined in the
            # SubProblem's Elements, whether or not those Fields are
            # active in *this* SubProblem.
            flds = self.getParent().all_active_subproblem_fields()

            if linsys is not None:
                linsysComputed = linsys.computed
            else:
                linsysComputed = timestamp.timeZero

            newDefinition = self.defnChanged > linsysComputed or always
            newFieldValues = (max(self.fieldsInstalled, mesh.fieldsInitialized)
                              > linsysComputed) or always
            newTime = linsys is None or linsys.time() != time or always
            newBdys = (mesh.boundariesChanged > linsysComputed
                       or (newTime and self.timeDependentBCs())
                       ## TODO 3.1: Check for field dependent boundary
                       ## conditions
                       # or (newFieldValues and self.fieldDependentBCs(flds))
                       or always)

            newLinSys = (linsys is None) or newDefinition

            newMaterials = mesh.materialsChanged > linsysComputed or always
            rebuildMatrices = (
                newLinSys or newMaterials
                or (self.nonlinear(flds) and (newBdys or newFieldValues))
                or (newFieldValues and self.nonlinear_solver.needsResidual())
                or (self.nonlinear_solver.needsJacobian() and 
                    self.nonlinear_solver.jacobianRequirementChanged() >
                    linsysComputed)
                or (self.nonlinear_solver.needsResidual() and
                    (newFieldValues or 
                     (self.nonlinear_solver.residualRequirementChanged() >
                      linsysComputed)))
                or (newTime and self.timeDependentProperties(flds))
                or always)

            if newDefinition:
                self.getObject().mapFields()

            # Create a new linearized system object if necessary
            if newLinSys:
                linsys = self.getObject().new_linear_system(time)
                linsys.computed = timestamp.TimeStamp()
            
            if newTime:
                linsys.set_time(time)


            # Apply boundary conditions to the linearized system object.
            # This has to be done before the matrix and rhs values are
            # computed. The matrix and rhs may be nonlinear and therefore
            # depend on field values, which may be determined by boundary
            # conditions.

            bcsReset = newLinSys or newBdys
            if bcsReset:
                # reset_bcs() calls Boundary.reset for all Boundaries in
                # the mesh, which resets all FloatBCs on the boundaries.
                femesh.reset_bcs()

                femesh.createAuxiliaryBCs() # convert PeriodicBCs --> FloatBCs

                ## TODO 3.1: Restore this after split nodes are implemented on
                ## interface elements.  Search for SPLIT NODES to find
                ## related TODOs that have to be done at the same time.
                #femesh.createInterfaceFloatBCs(self) # jump conds --> FloatBCs

                # Find intersecting floating boundary conditions, and
                # arrange them into a tree structure.  This must be done
                # *before* fixed boundary conditions are applied so that
                # intersecting fixed and floating bcs are treated
                # correctly.
                femesh.floatBCResolve(subpobj, time)

                # LinearizedSystem::force_bndy_rhs is used by
                # invoke_flux_bcs and invoke_force_bcs, and must be
                # cleared before either of them is called.
                linsys.clearForceBndyRhs()

                femesh.invoke_flux_bcs(subpobj, linsys, time)

            # Apply Dirichlet BCs.  If new values have been assigned to
            # the Fields, the old Dirichlet BCs may have been overwritten,
            # so they have to be reapplied.
            if bcsReset or newFieldValues:
                linsys.resetFieldFlags()
                femesh.invoke_fixed_bcs(subpobj, linsys, time)

            if bcsReset:
                femesh.invoke_force_bcs(subpobj, linsys, time)
                # Set initial values of DoFs used in FloatBCs that
                # intersect fixedBCs.
                femesh.fix_float_bcs(subpobj, linsys, time)

            if rebuildMatrices:
                # Assemble vectors and matrices of the linearized system.
                linsys.clearMatrices()
                linsys.clearBodyRhs() # allocates space if needed
                if self.nonlinear_solver.needsResidual():
                    linsys.clearResidual() # allocates space if needed
                if self.nonlinear_solver.needsJacobian():
                    linsys.clearJacobian()

                # **** This is the cpu intensive step: ****
                self.getObject().make_linear_system(linsys, 
                                                    self.nonlinear_solver)
                self.newMatrixCount += 1

            if bcsReset or rebuildMatrices or newFieldValues:
                linsys.build_submatrix_maps()
                # Apply floating boundary conditions by modifying maps in
                # the LinearizedSystem.  This must follow
                # build_submatrix_maps() and precede build_MCK_maps().
                femesh.invoke_float_bcs(subpobj, linsys, time)
                linsys.build_MCK_maps()
                # Construct vectors of first and second time derivatives
                # of the time-dependent Dirichlet boundary conditions.
                linsys.initDirichletDerivatives()
                femesh.setDirichletDerivatives(subpobj, linsys, time)

            if bcsReset:
                # Compute the part of the rhs due to fixed fields or fixed
                # time derivatives in boundary conditions.
                linsys.find_fix_bndy_rhs(self.getObject().get_meshdofs())

                # Add the floating boundary condition profiles'
                # contributions to the rhs.  This must come after
                # find_fix_bndy_rhs(), and must always be called if
                # find_fix_bndy_rhs() is called.
                ## TODO OPT: Only call float_contrib_rhs if solver needs
                ## to know the rhs explicitly.
                femesh.float_contrib_rhs(self.getObject(), linsys)

            femesh.clearCurrentSubProblem()
            linsys.computed.increment()

        finally:
            mesh.releaseLatestData()

        # ## Don't remove this block.  Comment it out instead.  It's
        # ## likely to be needed later.
        # global debugcount
        # debugcount += 1
        # if debugcount==3:
        #     if always:
        #         dumpfile = "dump-always"
        #     else:
        #         dumpfile = "dump"
        #     linsys.dumpAll(dumpfile, time, "")
        #     sys.exit()
        return linsys

    #=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

    # initializeStaticFields computes the static field values and
    # stores them in the FEMesh.  It's called by evolve.py before time
    # stepping.  computeStaticFields computes the fields but just
    # stores the values in the given vector of unknowns.  It's called
    # by initializeStaticFields and by time steppers, such as
    # ForwardEuler and RK, that need to solve the static equations
    # explicitly.

    def initializeStaticFields(self, linsys):
        # This is called by initializeStaticFields in evolve.py.  It
        # won't ever be called if solver_mode or time_stepper is None.
        derivOrder = self.time_stepper.derivOrder()
        if derivOrder == 0 or self.lowestTimeDerivative() < derivOrder:
            unknowns = self.get_unknowns(linsys)
            self.computeStaticFields(linsys, unknowns)
            self.installValues(linsys, unknowns, linsys.time())

    def computeStaticFields(self, linsys, unknowns):
        # Initialize "static" fields.  "static" fields are active
        # fields whose time derivatives don't appear in the equations,
        # or whose highest time derivative is of lower order than the
        # time stepper's order.  That is, if the time stepper is
        # second order, computeStaticFields has to compute the values
        # of the fields that have no time derivatives, and the values
        # and first derivatives of those that have a first derivative
        # in the equations, but not a second derivative.
        derivOrder = self.time_stepper.derivOrder()
        if derivOrder == 0 or self.lowestTimeDerivative() < derivOrder:
            # Call either computeStaticFieldsL or
            # computeStaticFieldsNL depending on whether or not we're
            # using a nonlinear solver and whether or not the
            # FluxProperties provide the K matrix.
            self.nonlinear_solver.computeStaticFields(self, linsys, unknowns)
                
    def computeStaticFieldsL(self, linsys, unknowns):
        # Initialize "static" fields for linear problems. 
        if linsys.n_unknowns_part('K')==0 and linsys.n_unknowns_part('C')==0:
            return
        if self.nonlinear_activefields():
            raise ooferror2.ErrSetupError(
                "A nonlinear solver is required for subproblem '%s'." 
                % self.name())

        # u2 = fields that have second time derivative terms in the
        # equations. These correspond to nonempty columns in M.

        # u1 = fields that have first time derivative terms, but not
        # second.  These correspond to empty columns in M but not C.

        # u0 = fields that have no time derivative terms.  These
        # correspond to empty columns in both M and C.

        # u1, u2, and u2dot are set by initial conditions.  We're
        # solving for u0 and u1dot.

        u2 = self.time_stepper.get_unknowns_part('M', linsys, unknowns)
        u1 = self.time_stepper.get_unknowns_part('C', linsys, unknowns)
        u0 = self.time_stepper.get_unknowns_part('K', linsys, unknowns)

        if len(u0) > 0:
            # Find u0 by solving
            #       K00 u0 + K01 u1 + K02 u2 = f0
            # which is the derivative-free part of the full set of
            # equations.
            K00 = self.time_stepper.K_submatrix(linsys, 'K', 'K')
            # rhs = f0 - K01*u1 - K02*u2, written out to avoid temporaries
            rhs = self.time_stepper.rhs_ind_part('K', linsys) # f0 copy
            if len(u1) > 0:
                K01 = self.time_stepper.K_submatrix(linsys, 'K', 'C')
                rhs -= K01*u1
            if len(u2) > 0:
                K02 = self.time_stepper.K_submatrix(linsys, 'K', 'M')
                rhs -= K02*u2
            self.matrix_method(self.asymmetricK).solve(K00, rhs, u0)
            self.time_stepper.set_unknowns_part('K', linsys, u0, unknowns)

        if len(u1) > 0 and self.time_stepper.derivOrder() > 1:
            # Find u1dot by solving
            #      C11 u1dot + C12 u2dot + K10 u0 + K11 u1 + K12 u2 + f1 = 0
            u1dot = self.time_stepper.get_derivs_part('C', linsys, unknowns)
            u2dot = self.time_stepper.get_derivs_part('M', linsys, unknowns)

            # rhs = f1 - C12*u2dot - K10*u0 - K11*u1 - K12*u2
            rhs = self.time_stepper.rhs_ind_part('C', linsys) # copy of f1
            K11 = self.time_stepper.K_submatrix(linsys, 'C', 'C')
            rhs -= K11*u1       # -= might avoid a copy
            if len(u2dot) > 0:
                C12 = self.time_stepper.C_submatrix(linsys, 'C', 'M')
                rhs -= C12*u2dot
            if len(u0) > 0:
                K10 = self.time_stepper.K_submatrix(linsys, 'C', 'K')
                rhs -= K10*u0
            if len(u2) > 0:
                K12 = self.time_stepper.K_submatrix(linsys, 'C', 'M')
                rhs -= K12*u2
            C11 = self.time_stepper.C_submatrix(linsys, 'C', 'C')
            self.matrix_method(self.asymmetricC).solve(C11, rhs, u1dot)
            self.time_stepper.set_derivs_part('C', linsys, u1dot, unknowns)

    def computeStaticFieldsNL(self, linsys, unknowns):
        # Initialize "static" fields for nonlinear problems. 
        if linsys.n_unknowns_part('K')==0 and linsys.n_unknowns_part('C')==0:
            return

        data = timestepper.NLData(self, linsys, linsys.time())

        u0 = self.time_stepper.get_unknowns_part('K', linsys, unknowns)
        u1 = self.time_stepper.get_unknowns_part('C', linsys, unknowns)

        if len(u0) > 0:
            # Solve for u0 -- static dofs that don't appear in C or M.
            nlfuncs = StaticNLFuncs(unknowns)
            self.nonlinear_solver.solve(
                self.matrix_method(self.asymmetricK),
                nlfuncs.precompute,
                nlfuncs.compute_residual,
                nlfuncs.compute_jacobian,
                nlfuncs.compute_linear_coef_mtx,
                data, u0)
            self.time_stepper.set_unknowns_part('K', linsys, u0, unknowns)

        if len(u1) > 0 and self.time_stepper.derivOrder() > 1:
            # Find u1dot (dof derivatives that appear in C but not M)
            # by solving C11 u1dot + C12 u2dot + F(u) = 0
            u1dot = self.time_stepper.get_derivs_part('C', linsys, unknowns)
            u2dot = self.time_stepper.get_derivs_part('M', linsys, unknowns)

            C11 = linsys.C_submatrix('C', 'C')
            C12 = linsys.C_submatrix('C', 'M')
            # rhs = -F(u) - C12*u2dot
            rhs = -linsys.static_residual_ind_part('C')
            C12.axpy(-1.0, u2dot, rhs)
            self.matrix_method(self.asymmetricC).solve(C11, rhs, u1dot)
            self.time_stepper.set_derivs_part('C', linsys, u1dot, unknowns)

    ## Time stepping utilities

    def startStep(self, linsys, time):
        self.startTime = time
        self.getParent().restoreLatestData()
        self.startValues = self.getObject().get_meshdofs()
        self.getParent().releaseLatestData()

    def get_unknowns(self, linsys):
        unknowns = self.time_stepper.get_unknowns(linsys, self.startValues)
        return unknowns

    def endStep(self, linsys, stepResult):
        # Called by evolve after successfully taking a time step.
        # Merges the vector of solved values (unknowns) with the
        # subproblem's vector of all values, and stores the result as
        # endValues.  It's *not* stored as startValues until the step
        # is accepted and moveOn is called (which may not happen
        # immediately if there are other subproblems).
        #
        # stepResult is a timestepper.StepResult instance.
        # set_unknowns injects stepResult.endValues (the final values
        # of the unknowns) into a copy of self.startValues, and
        # returns the result.
        ## TODO OPT: reuse self.endValues if possible
        self.endValues = self.time_stepper.set_unknowns(
            linsys, stepResult.endValues, self.startValues)
        self.endTime = stepResult.endTime
        self.solutiontimestamp.increment()

    def installValues(self, linsys, knowns, time):
        # Copy dof values from the given knowns (the vector formerly
        # known as 'unknowns') into the FEMesh, and expand the
        # floating BCs.  This does *not* set any values in the
        # SubProblemContext except for self.installedTime.

        # set_unknowns() inserts the known values into a copy of
        # startValues, and returns the result.  Note that if there are
        # time-dependent boundary conditions, their values in
        # startValues are not correct!  set_mesh_dofs corrects for
        # this, though.

        allvals = self.time_stepper.set_unknowns(linsys, knowns,
                                                 self.startValues)
        self.set_mesh_dofs(allvals, time)

    def set_mesh_dofs(self, vals, time):
        # set_mesh_dofs() is like installValues(), but it starts with
        # the full list of subproblem values (such as startValues or
        # endValues) instead of a list of unknowns.
        self.installedTime = time

        self.getParent().restoreLatestData()

        # Copy from vals into the mesh.  After this, all dofs in the
        # same FloatBC have the value of that BC's reference point.
        changed = self.getObject().set_meshdofs(vals)
        # Apply the FloatBC profiles, giving the dofs in the FloatBCs
        # their true values.
        self.getParent().getObject().expand_float_bcs(self.getObject(), time)

        # If there are time-dependent Dirichlet boundary conditions,
        # vals may contain the wrong values for them.  Fix this by
        # re-applying the boundary conditions.
        if self.timeDependentBCs():
            self.getParent().getObject().reinvoke_fixed_bcs(
                self.getObject(), time)
        if changed:
            self.fieldsInstalled.increment()

        self.getParent().releaseLatestData()

    def interpolateValues(self, time):
        ## TODO 3.1: The interpolation order should depend on the
        ## stepper.  High order steppers will need to somehow store
        ## more information.
        if self.endTime is None:
            return self.startValues
        f = (time - self.startTime)/(self.endTime - self.startTime)
        vals = self.startValues.clone()
        vals.scale(1-f)
        vals.axpy(f, self.endValues)
        return vals

    def cmpDoF(self, vals0, vals1):
        # Do two sets of DoF values agree with each other?
        if vals0.size() != vals1.size():
            return False
        norm0 = vals0.norm()
        norm1 = vals1.norm()
        if norm0 == norm1 == 0.0:
            return True
        diff = vals1 - vals0
        return diff.norm() < consistencyTolerance*(norm0 + norm1)

    def moveOn(self):           # Get ready for the next time step
        self.set_mesh_dofs(self.endValues, self.endTime)
        self.startValues = self.endValues.clone()
        self.startTime = self.endTime
        self.endTime = None

    def cacheConstraints(self, linsys, time):
        # print "Inside cacheConstraints at time ", time
        # Called by the evolve_to function after the initial linear
        # system has been built, i.e. after the integrals have all
        # been computed, but before the linear system has been solved,
        # and so obviously before any steps have been taken.  The
        # passed-in "time" is the start time for the current step.

        ## TODO 3.1: CONSTRAINTS Write this.
        pass

    def applyConstraints(self, dofvalues, time):
#         print "Inside applyConstraints at time ", time
        sb = self.getObject()
#         print sb
        # Use a new "evaluate_constraints" call chain.
        ## TODO 3.1: CONSTRAINTS Write this.
        # At this point, a candidate linearized-system has been
        # solved, and the DOF values resulting from that operation are
        # passed in as "dofvalues", along with the time at which they
        # apply.  Note that this function should return "true" if
        # constraints were removed, as well aos if they were applied.
        # The passed-in time is the time actually reached by the
        # stepper for this step.  It might not be equal to the target
        # time for this step.

        # Applying constraints, operationally speaking, means
        # activating constraint equations, and defining and activating
        # the associated DOFs, which might mean invalidating the DOF
        # list.

        # The property knows which constraint equations it contributes
        # to -- the set of all equations with contributions is the set
        # of equations we want to evaluate.
        return False            # False ==> no constraints applied

    def restoreConstraints(self):
        # print "Inside restoreConstraints at time ", time
        # Called on a subproblem if consistency was not achieved in
        # the solver loop -- the step is going to be retried, so the
        # constraints need to be reset to their starting values.
        # Probably what you want to do is set the constraint state to
        # the state you cached when cacheConstraints was called, at
        # the start of this step.

        ## TODO 3.1: CONSTRAINTS Write this.
        pass

    def finalizeConstraints(self, time):
        # print "Inside finalizeConstraints at time ", time
        # Called on the subproblems when the evolve_to function has
        # achieved consistency between all the subproblems at the
        # achieved, passed-in time.  When this function is called,
        # it's safe to discard the cached constraints from
        # cacheConstraints, you are now guaranteed that the step will
        # not be retried.

        ## TODO 3.1: CONSTRAINTS Write this.
        pass

## debugcount is used by the "Don't remove this" block in
## make_linear_system.  Uncomment this if you uncomment that.
# debugcount = 0


#####################################################

## TODO 3.1: TDEP Should this be derived from timestepper.NLData?

class StaticNLFuncs(object):
    def __init__(self, unknowns):
        self.unknowns = unknowns

    def precompute(self, data, values, solver):
        # debug.fmsg("requireJacobian=", solver.needsJacobian(),
        #            "requireResidual=", solver.needsResidual())
        data.subproblem.time_stepper.set_unknowns_part('K', data.linsys, values,
                                                       self.unknowns)
        data.subproblem.installValues(data.linsys, self.unknowns, data.time)
        data.linsys = data.subproblem.make_linear_system(data.time, data.linsys)

    def compute_residual(self, data, soln, nlsolver):
        # debug.fmsg()
        return data.linsys.static_residual_ind_part('K')

    def compute_jacobian(self, data, nlsolver):
        # debug.fmsg()
        return data.linsys.J_submatrix('K', 'K')

    def compute_linear_coef_mtx(self, data, nlsolver):
        # debug.fmsg()
        return data.linsys.K_submatrix('K', 'K')


#####################################################

subproblems = whoville.WhoClass(
    'SubProblem',
    instanceClass=SubProblemContext,
    ordering=400,
    secret=True,
    parentClass=mesh.meshes)

#####################################################

# SubProblemParameters are used instead of WhoParameters in cases in
# which only the subproblem name, and not its full path, needs to be
# specified.  The associated gui widget lists only the subproblems
# belonging to the mesh that's in the same scope.

# TODO 3.1: It would be good to use a variant of the WhoParameter for
# this.  The difficulty with that is that its checker() method would
# have to find the correct Mesh to know which SubProblem names were
# valid.  But for creating compound subproblems, the Mesh is given not
# in the SubProblem constructor arguments, but one level up:
##  OOF.Subproblem.New(mesh, UnionSubProblem('subOne', 'subTwo'))

class SubProblemParameter(parameter.StringParameter):
    pass

#####################################################

# consistencyTolerance is used when solving multiple subproblems
# simultaneously.  Each subproblem is solved in turn, repeating until
# the norm of the solution is within consistencyTolerance of the norm
# of the solution on the previous iteration.  It's set from the
# Settings menu.
consistencyTolerance = 1.e-6

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# MatrixSolverWrapper wraps a MatrixMethod's "solve" method,
# intercepting its return values and using them to accumulate
# statistics.  Doing it this way simplifies the calling sequence for
# the MatrixMethod, because we don't have to make sure that the
# SubProblemContext is available whenever the solver is used, and we
# can use the MatrixMethod classes independently of the
# SubProblemContext if necessary.

class MatrixSolverWrapper(object):
    def __init__(self, subproblemcontext, solver):
        self.subprobctxt = subproblemcontext
        self.solver = solver
    def solve(self, matrix, rhs, solution):
        niters, residual = self.solver.solve(matrix, rhs, solution)
        self.subprobctxt.solverStats.matrixSolution(
            matrix.nrows(), niters, residual)


