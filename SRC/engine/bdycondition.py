# -*- python -*-
# $RCSfile: bdycondition.py,v $
# $Revision: 1.120.2.12 $
# $Author: langer $
# $Date: 2014/11/05 16:54:17 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# A new, leaner, meaner, boundary condition class.  For the
# point-like ones, the iteration over nodes and point evaluation,
# as required, will be done elsewhere.  All we need to be able
# to do here is take a node and a profile result, and apply it.

## TODO 3.1: Allow Field dependent boundary conditions.  Will need a way
## to evaluate a Field at a point in an XYStrFunction.

from ooflib.SWIG.common import config
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.engine import boundarycond
from ooflib.SWIG.engine import equation
from ooflib.SWIG.engine import ooferror2
from ooflib.common import debug
from ooflib.common import labeltree
from ooflib.common import registeredclass
from ooflib.common import utils
from ooflib.common.IO import automatic
from ooflib.common.IO import parameter
from ooflib.common.IO import reporter
from ooflib.common.IO import whoville
from ooflib.common.IO import xmlmenudump
from ooflib.engine import boundary
from ooflib.engine import profile
from ooflib.engine import skeletoncontext
from ooflib.engine.IO import meshparameters
import ooflib.engine.mesh
import string

# It's useful in the editor if all the BC's have shared
# parameters, to the greatest degree possible.

bc_field_param_group = parameter.ParameterGroup(
    meshparameters.FieldParameter('field', tip=parameter.emptyTipString),
    meshparameters.FieldIndexParameter('field_component',
                                       tip=parameter.emptyTipString))

bc_equation_param_group = parameter.ParameterGroup(
    meshparameters.EquationBCParameter('equation',
                                       tip=parameter.emptyTipString),
    meshparameters.FieldIndexParameter('eqn_component',
                                       tip=parameter.emptyTipString))

bc_boundary_param = meshparameters.MeshBoundaryParameter(
    "boundary", tip="Boundary to which this condition applies.")

bc_edge_bdy_param = meshparameters.MeshEdgeBdyParameter(
    "boundary", tip="Edge boundary to which this condition applies.")

bc_periodic_edge_bdy_param = meshparameters.MeshPeriodicEdgeBdyParameter(
    "boundary",
    tip="Pair of periodic edge boundaries to which this condition applies")

bc_point_bdy_param = meshparameters.MeshPointBdyParameter(
    "boundary", tip="Point boundary to which this condition applies.")

bc_face_bdy_param = meshparameters.MeshFaceBdyParameter(
    "boundary", tip="Face boundary to which this condition applies.")


# Boundary conditions are constructed in association with a particular
# profile and boundary, and can't really exist without these.
# Boundary conditions cannot be shared between profiles or between
# boundaries.
class BC(registeredclass.RegisteredClass):
    registry = []
    def __init__(self, profile, boundary, user_enable=True, visible=True,
                 subordinate=False):
        self.profile = profile     # Profile object.
        self.boundary = boundary   # Name of the boundary.

        # These variables are set by add_to_mesh.
        self.boundary_obj = None
        self._name = None
        self.meshctxt = None    # mesh context
        self.mesh = None        # mesh name

        # BC's start out inactive, but are auto-activated at
        # add-to-mesh time.  If they are ever explicitly inactivated
        # by the user, the explicit_inactive flag gets set, and
        # auto_activate will not make them active.
        self.computableDict = {}
        self.explicit_disable = not user_enable

        # The former "promotion" flag is now the visible flag.
        self.visible = visible
        # Subordinate boundary conditions are ones created by another
        # condition, such as the FloatBCs that are used to implement
        # PeriodicBCs.  It's possible that subordinate==visible.
        self.subordinate = subordinate

        self.initializer = None

    def __eq__(self, other):
        return self is other
    def name(self):
        return self._name

    def femesh(self):
        # self.meshctxt is set, when "add_to_mesh" is called.
        return self.meshctxt.femesh()

    # Status-setting function -- enables the BC if it's possible to do
    # so and the user has never said not to.  This function should be
    # called whenever the fields/equations/flux activation info in the
    # mesh changes.  Subclasses must have the "computable" function,
    # which answers the "do you make sense" question, independently of
    # whether the BC will actually be enabled.
    def auto_enable(self, subpcontext):
        subproblem = subpcontext.getObject()
        self.computableDict[subproblem] = self.computable(subproblem)

    # Functions for explicit enabling or disabling of BCs by users.

    def toggle_explicit_disable(self):
        self.explicit_disable = not self.explicit_disable
        self.meshctxt.bdys_changed()
        switchboard.notify("boundary conditions toggled",
                           self.meshctxt, self._name, self.isVisible())

    def explicitly_enable(self):
        if self.is_explicitly_disabled():
            self.toggle_explicit_disable()

    def explicitly_disable(self):
        if not self.is_explicitly_disabled():
            self.toggle_explicit_disable()

    def is_explicitly_disabled(self):
        return self.explicit_disable

    def is_disabled(self, subproblem):
        return self.explicit_disable or not self.computableDict[subproblem]

    # Some BCs will not be visible in the GUI.  For instance if
    # they're the result of promoting other BCs or the auxiliary
    # floatBC's used by periodicBC's
    def isVisible(self):
        return self.visible

    def __eq__(self, other):
        return id(self)==id(other)
    
    # Add_to_mesh is separate from the construction process for the
    # convenience of the boundary-condition editing, which is
    # accomplished by creating a new boundary condition and adding it
    # to the mesh with the name of a recently-removed one. 
    def add_to_mesh(self, name, mesh):
        self._name = name 
        self.mesh = mesh # Mesh name.
        
        self.meshctxt = ooflib.engine.mesh.meshes[mesh] # Who object.
        self.boundary_obj = self.meshctxt.getBoundary(self.boundary)
        self.profile.addCondition(self)
        self.boundary_obj.addCondition(self)

        # Auto-enable must precede the meshctxt add call below, which
        # builds the display string, which depends on side-effects of
        # auto_enable. (Really?)
        for subproblem in self.meshctxt.subproblems():
            self.auto_enable(subproblem)
        self.meshctxt.addBdyCondition(name, self)
        self.meshctxt.changed("Boundary conditions changed")

    def remove_from_mesh(self):
        # rmBdyCondition calls disconnect, below.
        meshctxt = self.meshctxt 
        self.meshctxt.rmBdyCondition(self) # unsets self.meshctxt
        meshctxt.changed("Boundary conditions changed")

    # Called prior to deletion, undo the additions we did on __init__.
    # Because of the circular references, as well as control over the
    # timing, these operations are unsuitable for a __del__ operation.
    def disconnect(self):
        self.profile.removeCondition(self)
        self.removeFromBoundary()
        self.boundary_obj = None
        self.mesh = None
        self.meshctxt = None
        self.computableDict = {}

    # Some types of boundary conditions are implemented by adding
    # auxiliary BCs to the Mesh. (For example, PeriodicBCs are
    # implemented by sets of pairwise FloatBCs.)  That should be done
    # by redefining create_auxiliary_BCs.
    def create_auxiliary_BCs(self):
        pass
    def remove_auxiliary_BCs(self):
        pass
        
    def rename(self, newname):
        if self.boundary_obj:
            self.boundary_obj.renameCondition(self._name, newname)
        self._name = newname

    def isTimeDependent(self):
        return self.profile.isTimeDependent()

    # Used by the GUI.
    def display_string(self):
        return "%s / %s" % (self.display(), self.profile.description())
    def bdy_string(self):
        return self.boundary_obj.name()

    # Check whether or not a DoF is already fixed.  If it is already
    # fixed, log an error if its value is not the same as the
    # given value.  Return True if the DoF is fixed, False otherwise.
    def checkFixedVal(self, linsys, node, dof, value):
        if linsys.is_fixed(dof):
            oldval = dof.value(self.meshctxt.getObject())
            # Make sure that the relative difference between the new
            # and old values is not bigger than the machine epsilon,
            mach_eps = utils.machine_epsilon
            if abs(oldval-value) > mach_eps*(0.5*(abs(oldval) + abs(value))):
                reporter.warn(
                    "Conflicting boundary conditions at %s: %s != %s (diff=%s)"
                    % (node.position(), value, oldval, value-oldval))
            return True
        return False

    # The initialization functions are used to set initial values for
    # time evolutions.  They may only be needed for FloatBCs, but are
    # called for all BC types, just in case. 
    ## TODO 3.1: If other BC types use initializers, their copy methods
    ## need to remember to copy them.
    def set_initializer(self, how):
        self.initializer = how
    def remove_initializer(self):
        self.initializer = None
    def get_initializer(self):
        return self.initializer
    def preinitialize(self):
        pass
    def initialize(self, time, intersections):
        pass
    def initializable(self, mesh):
        return False

    tip = "Different kinds of boundary conditions."
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/bc.xml')

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Individual boundary condition classes take the field and equation
# data in the form of a component object, which they must then change
# to a separate field and component for actual evaluation.  Boundary
# conditions are also specific to a particular mesh and boundary.
# They also know about a profile -- the object passed in may either be
# an existing profile in the current mesh, or a new unnamed profile.
# In either case, the passed in object is the appropriate subclass of
# ProfileFinder.

class DirichletBC(BC):
    def __init__(self, field, field_component, equation, eqn_component,
                 profile, boundary, 
                 user_enable=True, visible=True, #promoted=False,
                 subordinate=False):
        self.field = field
        self.field_component = field_component
        self.equation = equation
        self.eqn_component = eqn_component

        # Parent class __init__ needs to be last, because it does
        # collision detection on the boundary, which means the field
        # and equation have to already be set.
        BC.__init__(self, profile, boundary, user_enable=user_enable,
                    visible=visible, subordinate=subordinate)
    
    # "Copy" makes a new BC with a new name on a new boundary, but
    # with the same other parameters, except explicit-enabling.
    def copy(self, boundary):
        return DirichletBC(self.field, self.field_component,
                           self.equation, self.eqn_component,
                           self.profile, boundary,
                           user_enable=not self.explicit_disable)

    # Dispatch routine to call the right boundary-addition gizmo.
    def addToBoundary(self, boundary):
        boundary.addFixedCondition(self)

    def removeFromBoundary(self):
        self.boundary_obj.removeFixedCondition(self)

    def conflictsWith(self, other):
        return other.conflictsWithDirichlet(self)

    def conflictsWithDirichlet(self, other):
        return conflictDirichletDirichlet(self, other)

    def conflictsWithFloat(self, other):
        return conflictDirichletFloat(self, other)

    def conflictsWithPeriodic(self, other):
        return conflictDirichletPeriodic(self, other)

    def conflictsWithForce(self, other):
        return conflictDirichletForce(self, other)

    def conflictsWithNeumann(self, other):
        return conflictDirichletNeumann(self, other)

    def conflictsWithOutOfPlane(self, other):
        return conflictOutOfPlaneDirichlet(self, other)

    # Am I computable on the given subproblem of the current mesh?
    def computable(self, subproblem):
        if not self.meshctxt:
            return False
        return (subproblem.is_defined_field(self.field) and 
                subproblem.is_active_field(self.field) and 
                subproblem.is_active_equation(self.equation))
        
    # intersect() is called by FEMesh.fix_float_bcs to see if a
    # FloatBC is fixed by a DirichletBC, and by
    # FEMesh.fixedBCConsistency when checking the consistency of BCs
    # on geometrically intersecting boundaries.
    def intersect(self, other):
        # Other should be another DirichletBC or FloatBC
        return (self.field == other.field and
                self.field_component == other.field_component and
                self.equation == other.equation and
                self.eqn_component == other.eqn_component)
        
    # BC is applied through its "applyBC" method, which just sets the
    # value of the appropriate DoF to the passed-in value, and marks
    # the corresponding equation as dependent.  This is called by the
    # invokeFixed() methods of the Boundary classes in boundary.py.
    def applyBC(self, subproblem, linsys, node, location):
        if self.is_disabled(subproblem):
            return
        fldcomp = self.field.getIndex(self.field_component).integer()
        try:
            # If the field isn't defined at this node (because bcs are
            # applied to Meshes but fields are handled on
            # SubProblems), then Field.dof() will fail.  In that case,
            # there's nothing to do -- the bc can't be applied.
            dof = self.field.dof(node, fldcomp)
        except ooferror2.ErrNoSuchField:
            return

        value = self.profile(location)

        # checkFixedVal returns True if the DoF is already fixed, and
        # False if it's not.  It issues a warning if the DoF is
        # already fixed but has the wrong value.  (It doesn't raise an
        # exception, because insignificant round-off error can make
        # compatible boundary conditions appear to be incompatible.)
        if not self.checkFixedVal(linsys, node, dof, value):
            # Dof is not already fixed.

            # Field.setvalue() sets the value in the FEMesh's
            # dofvalues array.
            self.field.setvalue(subproblem.mesh, node, fldcomp, value)

            eqncomp = self.equation.getIndex(self.eqn_component).integer()
            nodalEqn = self.equation.nodaleqn(node, eqncomp)

            # Mark the DegreeOfFreedom and its time derivative as 'fixed'.
            linsys.fixdof(self.field.dof(node, fldcomp))
            linsys.fixeqn(nodalEqn)

    def reapply(self, subproblem, node, location):
        if self.is_disabled(subproblem):
            return
        fldcomp = self.field.getIndex(self.field_component).integer()
        try:
            dof = self.field.dof(node, fldcomp)
        except ooferror2.ErrNoSuchField:
            return
        value = self.profile(location)
        self.field.setvalue(subproblem.mesh, node, fldcomp, value)

    def setDerivatives(self, subproblem, linsys, node, location):
        if self.is_disabled(subproblem):
            return
        fldcomp = self.field.getIndex(self.field_component).integer()
        tdvalue = self.profile.evalTimeDerivative(location)
        tdvalue2 = self.profile.evalTimeDerivative2(location)
        linsys.setDirichletDerivatives(node, self.field, fldcomp,
                                       tdvalue, tdvalue2)

    def display(self):
        return "Dirichlet / %s[%s] / %s[%s]" % (
            `self.field`, self.field_component,
            `self.equation`, self.eqn_component)
    
registeredclass.Registration(
    "Dirichlet",
    BC,
    DirichletBC,
    ordering=1,
    params = (bc_field_param_group +
              bc_equation_param_group + [ 
            parameter.RegisteredParameter(
                'profile',
                reg=profile.ProfileXTd,
                value=None,
                tip='Profile describing how this condition varies.'),
            bc_boundary_param
            ]),
    tip="Fix the values of a Field along a boundary.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/dirichlet.xml')
    ) 

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class ForceBC(BC):
    def __init__(self, equation, eqn_component, profile, boundary,
                 user_enable=True):
        self.equation = equation
        self.eqn_component = eqn_component

        BC.__init__(self, profile, boundary,user_enable=user_enable)

    def copy(self, boundary):
        return ForceBC(self.equation, self.eqn_component,
                       self.profile, boundary,
                       user_enable=not self.explicit_disable)

    def addToBoundary(self, boundary):
        boundary.addForceCondition(self)

    def removeFromBoundary(self):
        self.boundary_obj.removeForceCondition(self)

    def conflictsWith(self, other):
        return other.conflictsWithForce(self)

    def conflictsWithDirichlet(self, other):
        return conflictDirichletForce(other, self)

    def conflictsWithFloat(self, other):
        return conflictForceFloat(self, other)

    def conflictsWithPeriodic(self, other):
        return conflictForcePeriodic(self, other)

    def conflictsWithForce(self, other):
        return conflictForceForce(self, other)

    def conflictsWithNeumann(self, other):
        return conflictForceNeumann(self, other)

    def conflictsWithOutOfPlane(self, other):
        return conflictOutOfPlaneForce(self, other)

    def computable(self, subproblem):
        if not self.meshctxt:
            return None
        return subproblem.is_active_equation(self.equation)

    def applyBC(self, subproblem, linsys, node, location):
        if self.is_disabled(subproblem):
            return
        eqnindex = self.equation.getIndex(self.eqn_component).integer()
        try:
            value = self.profile(location)
            boundarycond.applyForceBC(subproblem, linsys, self.equation,
                                      node, eqnindex, value)
        except ooferror2.ErrNoSuchField: # eqn not active at that node
            pass
    def display(self):
        return "Force / %s" % `self.equation`


registeredclass.Registration(
    "Generalized Force",
    BC,
    ForceBC,
    ordering=2,
    params = bc_equation_param_group + [
        parameter.RegisteredParameter(
            'profile',
            reg=profile.ProfileXT,
            value=None,
            tip='Profile describing how this condition varies in space and time.'),
        bc_point_bdy_param],
    tip="Apply a force to all nodes on a boundary.  A force is a divergence of a flux (eg, stress, heat flux).  The condition is applied independently at each node, and is therefore sensitive to node density.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/forcebc.xml')
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

## Float boundary condition -- similar to a DirichletBC in basic
## structure, but with major differences in the apply function.  What
## 'apply' does is go through the mapping lists passed to the mesh by
## the matrix extraction routine, and set them up so that all the rows
## and columns corresponding to the DOFs and nodalequations of the
## floating boundary condition are remapped to a single row/colum,
## respectively, of the new mapping.

## They also have an unravelling routine which unmaps the DOFs
## after solution.

## The 'profile' function has the same structure but a different
## meaning here -- it's an offset, the true fully-solved value of the
## DOF is the profile value plus another value, such that the sum
## equals the sum arrived at by the solver.  Time-dependent profiles
## are not allowed, because they'd be a pain.  When expanding a
## profile, you want to expand at a given time, but the profile
## offsets were computed at some other time.  The upshot is that
## time-dependent floating BC profiles are a bad idea.

# FloatBCs come in two flavors, the unmodified "FloatBC", which is
# historically the original version, can be created by users, and (in
# 2D) the "OutOfPlaneBC", whose "field" is the out-of-plane part of a
# compound field.  These BCs differ in their strategy for retrieving
# the time derivative.


class FloatBCBase(BC):
    def __init__(self, field, field_component, equation, eqn_component,
                 profile, boundary, user_enable=True, visible=True,
                 subordinate=False):
        self.field = field
        self.field_component = field_component
        self.equation = equation
        self.eqn_component = eqn_component
        BC.__init__(self, profile, boundary, user_enable=user_enable,
                    visible=visible, subordinate=subordinate)
        self.reset()

    def copy(self, boundary):
        bozo = FloatBC(self.field, self.field_component,
                       self.equation, self.eqn_component,
                       self.profile, boundary,
                       user_enable=not self.explicit_disable)
        if self.initializer:
            bozo.initializer = self.initializer.clone()
        return bozo

    # This function can be called either by init or from the boundary,
    # when it wants to reset stateful boundary conditions.  This
    # provides a handy way of pretend-encapsulating the state variables.
    # FloatBCs are stateful because intersecting combinations of them
    # need to aggregate their degrees of freedom in a sensible way,
    # with consistent profiles and without double-counting.  This is
    # what the traversal process does.
    def reset(self):
        # Below here are the "stateful" data members.  
        self.applicator = None # C applicator -- "None" means first-call.
        self.dofmappingIndex = None # Set either locally or by parents
        self.eqnmappingIndex = None #    on the intersection tree.
        self.dofIndex = None
        
        # profileStart is the value of the profile function at the DoF
        # that is the "master" DoF for this FloatBC tree containing
        # this FloatBC.  Its value is set by the master FloatBC when
        # the BC is applied, in FloatBC.applyBC), and also by
        # FloatBC.setMeshValue() when it's applied to the master.
        self.profileStart = None

        # Cumulative total offset from intersections, set by
        # FEMesh.floatBCResolve().
        self.profileOffset = 0.0

        self.intersectors = {}     # key=BC, value=offset
        self.parent = None
        self.root = None
        self.ownNodes = set()
        self.fixed = False

    def disconnect(self):
        # These might not all be necessary, but they can't hurt.
        self.intersectors = {}  # FloatBCs that intersect this one
        self.parent = None
        self.root = None
        self.ownNodes.clear()
        self.intersected = None
        del self.applicator
        BC.disconnect(self)

    # Dispatch routine, called from the boundary, calls back to the
    # correct boundary-addition routine.
    def addToBoundary(self, boundary):
        boundary.addFloatCondition(self)

    def removeFromBoundary(self):
        self.boundary_obj.removeFloatCondition(self)

    # conflictsWith() and friends check for superficial conflicts
    # between boundary conditions on the *same* boundary.  They don't
    # check numerical consistency between conditions on intersecting
    # boundaries.
    def conflictsWith(self, other):
        return other.conflictsWithFloat(self)
    def conflictsWithDirichlet(self, other):
        return conflictDirichletFloat(other, self)
    def conflictsWithFloat(self, other):
        return conflictFloatFloat(self, other)
    def conflictsWithPeriodic(self, other):
        return conflictFloatPeriodic(self, other)
    def conflictsWithForce(self, other):
        return conflictForceFloat(other, self)
    def conflictsWithNeumann(self, other):
        return conflictFloatNeumann(self, other)
    def conflictsWithOutOfPlane(self, other):
        return conflictOutOfPlaneFloat(self, other)
    

    # intersect() is called by floatBCResolve (in femesh.spy) when
    # checking numerical consistency of FloatBCs on geometrically
    # intersecting boundaries.
    def intersect(self, other): # other is another Float or DirichletBC.
        return (self.field == other.field and
                self.field_component == other.field_component and
                self.equation == other.equation and
                self.eqn_component == other.eqn_component)

    def computable(self, subproblem):
        if not self.meshctxt:
            return None
        return (subproblem.is_defined_field(self.field) and
                subproblem.is_active_field(self.field) and
                subproblem.is_active_equation(self.equation))

    # setRootDoFIndex just sets dofIndex in the root FloatBC of this
    # FloatBC's tree.  dofIndex is the Mesh DoF index of the reference
    # DoF for the whole tree.  It has to be set before
    # FloatBC.setMeshValue is called. 
    def setRootDoFIndex(self, bdy, subproblem):
        if self.root.dofIndex is not None:
            return
        fldcomp = self.field.getIndex(self.field_component).integer()
        for (node, location) in bdy.locations():
            if subproblem.containsNode(node) and node in self.ownNodes:
                try:
                    self.root.dofIndex = \
                        self.field.dof(node, fldcomp).dofindex()
                    return
                except ooferror2.ErrNoSuchField:
                    pass
                    
    #=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

    # preApply is called for all FloatBCs before the BCs are applied
    # to any boundaries.

    def preApply(self):
        self.applicator = None
        
    def applyBC(self, subproblem, linearsystem, node, location):
        if (self.is_disabled(subproblem) or node not in self.ownNodes
            or self.isFixed()):
            return

        value = self.profile(location) + self.profileOffset
        fldcomp = self.field.getIndex(self.field_component).integer()

        eqncomp = self.equation.getIndex(self.eqn_component).integer()


        if self.root.applicator is None:  
            # This FloatBC has not yet been applied to any node.  Try
            # to apply it to this node.
            try:
                # dofmappingIndex is the mapped index of the reference
                # dof (the free dof that will be actually solved for).
                # All other dofs in this FloatBC refer to it.
                self.root.dofmappingIndex = linearsystem.getSubproblemDoFIndex(
                    node, self.field, fldcomp)
            except ooferror2.ErrNoSuchField:
                # Field doesn't exist at this node -- just go on as if
                # nothing had happened.  *Don't* set
                # self.root.applicator!  Let some other node be the
                # first one.
                pass
            else:      
                # Field exists at this node, and this is the first
                # time this FloatBC has been applied to a node in this
                # boundary.

                # dofIndex is the *unmapped* index of the reference
                # dof.  It's already been set by setRootDoFIndex().
                assert (self.root.dofIndex ==
                        self.field.dof(node, fldcomp).dofindex())
                # eqnmappingIndex is the mapped index of the nodal
                # equation corresponding to the reference dof.  (It's
                # the conjugate equation, if there is one.)  All
                # equations for the FloatBC will be summed into this
                # one.
                self.root.eqnmappingIndex = linearsystem.getSubproblemEqnIndex(
                    node, self.equation, eqncomp)

                # For user-provided FloatBCs, constraining the field
                # and its derivative is sufficient, this is the only
                # input the user can provide, and so the provided
                # field must be a CompoundField, which means we can
                # meaningfully ask about its time derivative.
                
                ## TODO MER: For periodic BCs and the automatic
                ## float BCs created for internal boundaries, we want
                ## to also constrain the out-of-plane parts of the
                ## field.
                # To get these bits for this topological case:
                # self.field.out_of_plane()
                # self.field.out_of_plane_time_derivative()
                # If these are defined, use them.
                # Also, you'll need a root applicator.
                tdf = self.field_time_derivative()
                if subproblem.is_defined_field(tdf):
                    self.root.derivmappingIndex = (
                        linearsystem.getSubproblemDoFIndex(
                            node, tdf, fldcomp))
                else:
                    self.root.derivmappingIndex = -1
                self.root.applicator = boundarycond.FloatBCApp()
                self.root.profileStart = value
        else:   # root.applicator is not None
            # This is not the first application of this FloatBC to
            # a node in this boundary. 
            try:
                self.root.applicator.editmap(linearsystem, value, node,
                                             self.field, fldcomp,
                                             self.equation, eqncomp,
                                             self.root.dofmappingIndex,
                                             self.root.eqnmappingIndex,
                                             self.root.derivmappingIndex,
                                             self.root.profileStart)
            except ooferror2.ErrNoSuchField:
                # Field or Eqn isn't defined at the node
                pass

    #=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

    def getMeshValue(self, node):
        # This was once used for debugging, and may be still useful.
        fldcomp = self.field.getIndex(self.field_component).integer()
        return self.field.dof(node, fldcomp).value(self.meshctxt.getObject())

    def fixFloatTree(self, linsys, val, locations, time):
        # Fix the DoFs in this boundary condition, and propagate the
        # fix to the bc's children in the tree of intersecting
        # FloatBCs.
        fcomp = self.field.getIndex(self.field_component).integer()
        eqncomp = self.equation.getIndex(self.eqn_component).integer()
        for node, location in locations:
            try:
                dof = self.field.dof(node, fcomp)
            except ooferror2.ErrNoSuchField:
                pass
            else:
                location.set_time(time)
                localval = val + self.profile(location) + self.profileOffset
                if not self.checkFixedVal(linsys, node, dof, localval):
                    # DoF is not already fixed.
                    self.field.setvalue(self.meshctxt.getObject(), node, fcomp, 
                                        localval)
                    linsys.fixdof(dof)
                    linsys.fixeqn(self.equation.nodaleqn(node, eqncomp))
        for intersector in self.intersectors:
            intersector.boundary_obj.fixFloatTree(intersector, linsys,
                                                  val, time)
        self.root.fixed = True

    def checkConsistency(self, linsys, val, locations, time):
        fcomp = self.field.getIndex(self.field_component).integer()
        eqncomp = self.equation.getIndex(self.eqn_component).integer()
        for node, location in locations:
            try:
                dof = self.field.dof(node, fcomp)
            except ooferror2.ErrNoSuchField:
                pass
            else:
                location.set_time(time)
                localval = val + self.profile(location) + self.profileOffset
                self.checkFixedVal(linsys, node, dof, localval)


    def isFixed(self):
        return self.root.fixed
    def isRoot(self):
        return self.root is self
                           
    def contrib_rhs(self, subproblem, linearsystem):
        # Called by Boundary.contribRHS() in boundary.py, which is
        # called by FEMesh.float_contrib_rhs() in femesh.spy.  This
        # will be called for each FloatBC, but it should be done only
        # once per FloatBCApp, so here we don't do anything if this
        # isn't a root.  TODO 3.1: Probably that means that the class
        # structure is wrong.
        if self.root is self:
            if not (self.is_disabled(subproblem) or self.applicator is None):
                linearsystem.profile_rhs(self.applicator);

    #=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

    # After finding the values of the unknowns, we need to fill in the
    # DOF values according to the profile function.  This routine is
    # called for every DOF in the set by EdgeBoundary.expandFloat() or
    # PointBoundary.expandFloat().  Those are called by
    # FEMesh.expand_float_bcs(), which is called by
    # SubProblemContext.set_mesh_dofs() whenever values are copied
    # from the SubProblemContext's dof value lists back into the
    # FEMesh's DegreeOfFreedom objects.

    def setMeshValue(self, subproblem, node, location):
        # This is sort of like expand, but it doesn't increment the
        # DoF value, it simply sets it from the value of the master
        # DoF for this FloatBC.  This is called *before* solving.
        if (not self.is_disabled(subproblem) and node in self.ownNodes):
            if self.root.profileStart is None:
                # If the nodes are being addressed in the right order,
                # which is necessary if self.dofIndex is to refer to
                # the correct reference DoF, then the first call to
                # this routine for a FloatBC tree should be at the
                # reference node.
                assert self.root is self
                self.profileStart = self.profile(location) + self.profileOffset
            else:
                mesh = subproblem.meshcontext.getObject()
                rootvalue = mesh.get_dofvalue(self.root.dofIndex)
                value = (self.profile(location) + self.profileOffset + rootvalue
                         - self.root.profileStart)
                comp = self.field.getIndex(self.field_component).integer()
                self.field.setvalue(mesh, node, comp, value)

    ## Boundary.expandFloat used to call this routine instead of
    ## setMeshValue:
    # def expand(self, subproblem, node, location):
    #     # Before calling expand(), LinearizedSystem::set_meshdofs()
    #     # set all of the entries in LinearizedSystem::dofvalues
    #     # corresponding to a FloatBC to the value of the DoF that was
    #     # actually solved for.  That DoF's profile value is
    #     # root.profileStart.  All DoF's deviate from their profiles by
    #     # the same amount, so we just have to adjust each value by the
    #     # difference between its profile and profileStart.

    #     if (not self.is_disabled(subproblem) and node in self.ownNodes):
    #         correction = (self.profile(location) + self.profileOffset
    #                       - self.root.profileStart)
    #         comp = self.field.getIndex(self.field_component).integer()
    #         self.field.dof(node, comp).increment(
    #             subproblem.mesh, correction)

    #=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

    def display(self):
        # Exclamations, because it shouldn't ever be displayed.
        return "FloatBCBase!!! / %s[%s] / %s[%s]" % (`self.field`,
                                                     self.field_component,
                                                     `self.equation`,
                                                     self.eqn_component)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class FloatBC(FloatBCBase):
    def __init__(self, field, field_component, equation, eqn_component,
                 profile, boundary, user_enable=True, visible=True,
                 subordinate=False):
        FloatBCBase.__init__(self, field, field_component, equation,
                             eqn_component, profile, boundary,
                             user_enable, visible, subordinate)

    def field_time_derivative(self):
        return self.field.time_derivative()

    def display(self):
        return "Float / %s[%s] / %s[%s]" % (`self.field`,
                                            self.field_component,
                                            `self.equation`,
                                            self.eqn_component)
    def preinitialize(self):
        self.initialized = False

    def initialize(self, time, intersections):
        # Initialization could possibly be done using the machinery
        # used to resolve and expand FloatBCs, but it's sufficiently
        # different that it might not be worth the effort.  For one
        # thing, initialization is independent of the Subproblems, so
        # many of the routines used for expanding and resolving aren't
        # useful.

        if self.is_explicitly_disabled() or self.initializer is None:
            return

        # If this boundary condition has already been initialized
        # because it intersects another one which also has an
        # initializer, just make sure that the values are compatible.
        # This can be done by checking just one DoF, but it's possible
        # that the relevant Field isn't defined at all nodes, so more
        # than one has to be examined.  However, because roundoff
        # error can make it seem that compatible conditions are
        # incompatible, we don't raise an exception here; we just give
        # a warning instead.  Since we don't want to overwhelm the
        # user with warnings, we look for and only report the most
        # incompatible point on the boundary.
        if self.initialized:
            worstdiff = 0
            worst = None
            for (node, location) in self.boundary_obj.locations():
                fldcomp = self.field.getIndex(self.field_component).integer()
                try:
                    dof = self.field.dof(node, fldcomp)
                except ooferror2.ErrNoSuchField:
                    continue
                location.set_time(time)
                val = (self.profile(location) +
                       self.initializer.getOffset(self, time))
                dofval = dof.value(self.femesh())
                diff = abs(dofval - val)
                avg = 0.5*(abs(dofval) + abs(val))
                scaleddiff = diff/avg
                if scaleddiff > worstdiff:
                    worstdiff = scaleddiff
                    worst = (node, val, dofval)
            if worstdiff > utils.machine_epsilon*avg:
                node, val, dofval = worst
                reporter.warn(
                    "Conflicting floating boundary condition"
                    " initialization at %s: %s != %s (diff=%s)"
                    % (node.position(), val, dofval, val-dofval))
            return 
        else:
            # Set the values of the DoFs in this boundary.
            offset0 = self.initializer.getOffset(self, time)
            fldcomp = self.field.getIndex(self.field_component).integer()
            for (node, location) in self.boundary_obj.locations():
                location.set_time(time)
                val = self.profile(location)
                try:
                    self.field.setvalue(
                        self.femesh(), node, fldcomp, val+offset0)
                    td = self.initializer.getTimeDeriv()
                    if td is not None:
                        self.field.time_derivative().setvalue(
                            self.femesh(), node, fldcomp, td)
                except ooferror2.ErrNoSuchField:
                    pass
            self.initialized = True
            # Set the values of DoFs in FloatBCs that intersect this
            # one, recursively.  All of those FloatBCs are guaranteed
            # to be uninitialized at the start of this process.
            # "intersections" is a dict of lists of FloatBCs that
            # intersect this one.  Each list entry is a (bc, offset)
            # tuple.
            for (bc, offset) in intersections.get(self, []):
                bc._initialize_recursive(offset0+offset, time, intersections)

    def _initialize_recursive(self, offset0, time, intersections):
        if self.initialized or self.is_explicitly_disabled():
            return
        fldcomp = self.field.getIndex(self.field_component).integer()
        for (node, location) in self.boundary_obj.locations():
            location.set_time(time)
            val = self.profile(location) + offset0
            try:
                self.field.setvalue(self.femesh(), node, fldcomp, val)
                td = self.initializer.getTimeDeriv()
                if td is not None:
                    self.field.time_derivative().setvalue(
                        self.femesh(), node, fldcomp, td)
            except ooferror2.ErrNoSuchField:
                pass
        self.initialized = True
        for (bc, offset) in intersections[self]:
            bc._initialize_recursive(offset0+offset, time, intersections)
    def initializable(self, mesh):
        return self.field in mesh.all_initializable_fields()

registeredclass.Registration(
    "Floating",
    BC,
    FloatBC,
    ordering=3,
    params= bc_field_param_group + bc_equation_param_group + [
        parameter.RegisteredParameter(
            'profile',
            reg=profile.ProfileX, # No time dependence allowed!
            value=None,
            tip='Profile describing how this condition varies in space.'),
        bc_boundary_param
        ],
    tip="Fix the values of Fields on the boundary, up to an unspecified offset.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/floating.xml')
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class FloatBCInitMethod(registeredclass.RegisteredClass):
    registry = []
    tip="Ways of initializing a floating boundary condition."
    def __init__(self, value):
        self.value = value
    def getOffset(self, bc, time):
        self.reset()
        for (node, location) in bc.boundary_obj.locations():
            location.set_time(time)
            profileval = bc.profile(location)
            self.accumulate(profileval)
        return self.value - self.accumulant()
    def getTimeDeriv(self):
        pass

# Two versions of each FloatBCInitMethod are created when a subclass
# is registered.  The second version also initializes the time
# derivative.

def registerFloatBCInitMethod(name, subclass, ordering=0, params=[], secret=0,
                              tip=None, discussion=None, **kwargs):
    # Normal registration
    registeredclass.Registration(name,
                                 FloatBCInitMethod,
                                 subclass,
                                 ordering=ordering,
                                 params=params,
                                 secret=secret,
                                 tip=tip,
                                 discussion=discussion,
                                 time_derivative=False,
                                 **kwargs)

    # Create a subclass that also initializes the time derivative field.
    class FloatBCInitIncludingTimeDeriv(subclass):
        def __init__(self, time_derivative,*args, **kwargs):
            subclass.__init__(self, *args, **kwargs)
            self.time_derivative = time_derivative
        def shortrepr(self):
            return (super(FloatBCInitIncludingTimeDeriv, self).shortrepr() +
                    " time_derivative=%s" % self.time_derivative)
        def getTimeDeriv(self):
            return self.time_derivative
    tdname = subclass.__name__ + "_td"
    FloatBCInitIncludingTimeDeriv.__name__ = tdname
    # For consistency with the original subclass, insert the new
    # subclass in this module's dict.  Registration defines the new
    # subclass in the main OOF namespace, but not in this module.
    globals()[tdname] = FloatBCInitIncludingTimeDeriv
    tparams = params + [
        parameter.FloatParameter(
            'time_derivative', value=0.0,
            tip="The initial value of the time derivative of the boundary condition.")]
    registeredclass.Registration(
        name, 
        FloatBCInitMethod,
        FloatBCInitIncludingTimeDeriv,
        ordering=ordering+0.5,
        params=tparams,
        secret=secret,
        time_derivative=True,
        tip="Like %s, with time derivative." % subclass.__name__,
        **kwargs)        

class FloatBCInitMin(FloatBCInitMethod):
    # Return the offset that will cause the minimum value of the
    # given FloatBC to be 'value'.
    def reset(self):
        self.minval = None
    def accumulate(self, val):
        if self.minval is None or val < self.minval:
            self.minval = val
    def accumulant(self):
        return self.minval
    def shortrepr(self):
        return "min=%s" % self.value

registerFloatBCInitMethod(
    "Minimum",
    FloatBCInitMin,
    params=[
        parameter.FloatParameter(
            'value', 0.0,
            tip='The initial value of the BC at the minimum of its profile.')],
    ordering=1)

class FloatBCInitMax(FloatBCInitMethod):
    # Return the offset that will cause the maximum value of the
    # given FloatBC to be 'value'.
    def reset(self):
        self.maxval = None
    def accumulate(self, val):
        if self.maxval is None or val > self.maxval:
            self.maxval = val
    def accumulant(self):
        return self.maxval
    def shortrepr(self):
        return "max=%s" % self.value

registerFloatBCInitMethod(
    "Maximum",
    FloatBCInitMax,
    params=[
        parameter.FloatParameter(
            'value', 0.0,
            tip='The initial value of the BC at the maximum of its profile.')],
    ordering=2)

class FloatBCInitAverage(FloatBCInitMethod):
    def reset(self):
        self.n = 0
        self.sum = 0
    def accumulate(self, val):
        self.sum += val
        self.n += 1
    def accumulant(self):
        return self.sum/self.n
    def shortrepr(self):
        return "average=%d" % self.value

registerFloatBCInitMethod(
    "Average",
    FloatBCInitAverage,
    params=[
        parameter.FloatParameter(
            'value', 0.0,
            tip="The initial value of the average of the BC's profile.")],
    ordering=3)

class FloatBCInitParameter(parameter.RegisteredParameter):
    def __init__(self, name, value=None, default=None, tip=None, auxData={}):
        parameter.RegisteredParameter.__init__(
            self, name, FloatBCInitMethod,
            value=value, default=default, tip=tip, auxData=auxData)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

if config.dimension() == 2:

    # Out of plane boundary conditions.  These are like floating
    # boundary conditions, but have trivial profiles.  They tie
    # together pairs of nodes, typically across interfaces.
    # Operationally, they work like FloatBCs, in that they manipulate
    # the DOF maps, making them many-to-one.

    # Helper function -- takes a field and an equation, and builds all
    # the OOP boundary conditions appropriate to them.  Silently
    # returns an empty list if it can't find an appropriate plane-flux
    # equation.  Throws an exception if it finds multiple candidate
    # plane-flux equations.

    def _build_oops(field, eqn, boundary):

        res = []

        oop_field = field.out_of_plane()

        oop_eqn = None
        # TODO: Later on, there will be non-flux equations -- when
        # that happens, this ".flux" de-reference should be made more
        # robust.
        dflux = eqn.flux()
        for e in equation.allEquations:
            if isinstance(e, equation.PlaneFluxEquationPtr):
                if e.flux()==dflux:
                    if not oop_eqn:
                        oop_eqn = e
                    else:
                        raise ooferror2.ErrSetupError(
                            "Equation %s has multiple plane-flux equations." % \
                            `eqn`)

        if not oop_eqn:
            # If no plane-flux equation can be found, silently fail.
            return []

        field_itr = oop_field.iterator_all()
        eqn_itr = oop_eqn.iterator_all()

        while not field_itr.end():
            new_oop = OutOfPlaneBC(field, oop_field, field_itr.shortstring(),
                                   oop_eqn, eqn_itr.shortstring(),
                                   boundary)
            res.append(new_oop)
            field_itr.next()
            eqn_itr.next()

        return res



    # Actual OutOfPlaneBC class.  

    class OutOfPlaneBC(FloatBCBase):
        def __init__(self, compound_field, field, field_comp,
                     equation, eqn_comp, boundary, user_enable=True):

            trivial_profile = profile.ConstantProfile(0)
            self.compound_field = compound_field
            FloatBCBase.__init__(self, field, field_comp,
                                 equation, eqn_comp,
                                 trivial_profile, boundary,
                                 user_enable=True,
                                 visible=False, subordinate=True)

        def field_time_derivative(self):
            return self.compound_field.out_of_plane_time_derivative()


        def display(self):
            # Exclamation marks again, because this should never be displayed.
            return "OutOfPlaneBC!!!! / %s[%s] %s[%s]" %  (`self.field`,
                                                          self.field_component,
                                                          `self.equation`,
                                                          self.eqn_component)

        # OutOfPlaneBC objects don't have registrations, because there's
        # no parameter class for the out-of-plane fields, and because they
        # don't correspond to menu items and can't be created directly by
        # users.  However, they need to be hashable, because they get
        # included as index objects in sets of boundary conditions -- so,
        # they have their own local hash function.  TODO 3.1: This is ugly,
        # and should be fixed at some point.
        def __hash__(self):
            return hash(self.compound_field) ^ \
                   hash(self.field) ^ hash(self.equation)


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

## PeriodBCs are currently not allowed in 3D, since we don't have
## periodic meshes.  The Registration is 2D only.

# PeriodicBC's are special in that they don't contain a profile object
# and refer to two boundaries, not just one.  They are also special in
# that they have only a field, and not field components.

## TODO OPT: There might be interesting ways of using profiles with
## PeriodicBC's.  For instance, a user might want to specify that
## boundaries are periodic up to an offset.


class PeriodicBC(BC):
    def __init__(self, field, equation, boundary, user_enable=True):
        ## TODO: There is a good reason that PeriodicBC is derived
        ## from BC but doesn't call PeriodicBC's __init__.  If anyone
        ## remembers the reason, please add a comment explaining it.

        self.field = field
        self.equation = equation

        self.boundary = boundary
        # Periodic boundary conditions must keep track of exactly two
        # boundaries. The string returned by the widget will be two
        # names separated by a space
        self.boundaries = string.splitfields(self.boundary)

        self.boundary_obj = None
        self._name = None
        self.meshctxt = None
        self.floatBCs = []

        self.computableDict = {} # Used to activate at mesh-addition time.
        self.explicit_disable = not user_enable
        self.visible = True
        self.subordinate = False

        self.initializer = None

        # needed for meshIO
        self.profile = None

    def isTimeDependent(self):
        return False

    def copy(self, boundary):
        return PeriodicBC(self.field, 
                          self.equation, 
                          boundary,
                          user_enable=not self.explicit_disable)

    def toggle_explicit_disable(self):
        BC.toggle_explicit_disable(self)
        for bc in self.floatBCs:
            bc.toggle_explicit_disable()

    def conflictsWith(self, other):
        return other.conflictsWithPeriodic(self)

    def conflictsWithDirichlet(self, other):
        return conflictDirichletPeriodic(other, self)

    def conflictsWithFloat(self, other):
        return conflictFloatPeriodic(other, self)

    def conflictsWithPeriodic(self, other):
        return conflictPeriodicPeriodic(self, other)

    def conflictsWithForce(self, other):
        return conflictForcePeriodic(other, self)

    def conflictsWithNeumann(self, other):
        return conflictPeriodicNeumann(self, other)

    def conflictsWithOutOfPlane(self, other):
        return conflictOutOfPlanePeriodic(self, other)

    def add_to_mesh(self, name, mesh):
        self._name = name
        self.mesh = mesh # Mesh name.
        
        self.meshctxt = ooflib.engine.mesh.meshes[mesh] # Who object.

        self.boundary_obj0 = self.meshctxt.getBoundary(self.boundaries[0])
        self.boundary_obj1 = self.meshctxt.getBoundary(self.boundaries[1])

        self.boundary_obj0.addCondition(self)
        self.boundary_obj1.addCondition(self)
        
        # Auto-enable must precede the meshctxt add call below, which
        # builds the display string, which depends on side-effects of
        # auto_enable. (Really?)
        for subproblem in self.meshctxt.subproblems():
            self.auto_enable(subproblem)
        self.meshctxt.addBdyCondition(name, self)
        self.meshctxt.changed("Boundary conditions changed")

    def create_auxiliary_BCs(self):
        # Create the FloatBCs and point boundaries that actually
        # implement the periodic boundary condition.

        # This bc is assigned to two boundaries, but should be
        # converted into FloatBCs only once.
        if self.floatBCs:
            return

        # Point boundaries for each pair of mesh nodes along the
        # boundary are stored in the mesh.  If this is the first time
        # getPeriodicPointBoundaries is called, it creates them.
        # Otherwise it just returns the stored list of point
        # boundaries.
        periodicPointBoundaries = \
            self.meshctxt.getPeriodicPointBoundaries(self.boundary)

        self.floatBCs = []
        for bdy in periodicPointBoundaries:

            # Create floatBC with constant profile

            field_comp_itr = self.field.iterator_all()
            eqn_comp_itr = self.equation.iterator_all()
            while (not field_comp_itr.end()):
                
                # TODO OPT: There's a slight storage efficiency to be
                # gained by sharing the trivial profile between all
                # subsdiary BCs, not only between components but also
                # among the sets of node-pairs, but there may be
                # ownership issues associated with BC deletion.  If we
                # decide this is safe, just move the "newprofile"
                # assignment statement outside these two loops.

                newprofile = profile.ConstantProfile(0)
                newbc = FloatBC(self.field, field_comp_itr.shortstring(),
                                self.equation, eqn_comp_itr.shortstring(),
                                newprofile, bdy.name(),
                                visible=False, subordinate=True)

                # Need unique name.  Note that the "aux_pointbdy"
                # string is checked for as part of the BC-copying
                # routine in engine/IO/boundaryconditionmenu.py, where
                # there is a todo about maybe having a more robust
                # check.
                aux_bc_name = self.meshctxt.uniqueBCName("aux_pointbdy")
                newbc.add_to_mesh(aux_bc_name, self.mesh)
                self.floatBCs.append(newbc)
                
                field_comp_itr.next()
                eqn_comp_itr.next()

                
            if config.dimension() == 2:
                # Add the out-of-plane BCs, via the handy helper function.
                oopbcs = _build_oops(self.field, self.equation, bdy.name())

            # In pathological cases, oopbcs can be empty.
            for bc in oopbcs:
                oop_name = self.meshctxt.uniqueBCName("aux_pointbdy")
                bc.add_to_mesh(oop_name, self.mesh)

            self.floatBCs += oopbcs
            

    def remove_auxiliary_BCs(self):
        for bc in self.floatBCs:
            bc.remove_from_mesh()
        self.floatBCs = []

    def disconnect(self):
        self.removeFromBoundary()
        self.boundary_obj0 = None
        self.boundary_obj1 = None
        self.meshctxt = None
        self.mesh = None
        self.computableDict = {}
        for bc in self.floatBCs:
            bc.remove_from_mesh()
        # Don't call BC.disconnect... it assumes just one boundary_obj.
            
    def intersect(self, other): # Other should be another PeriodicBC.
        # This is *not* the same as _fieldEqnConflict().  That has an
        # 'or' in it.
        return (self.field == other.field and
                self.equation == other.equation)


    # Used by the GUI.
    def display_string(self):
        return self.display()
    def bdy_string(self):
        return "%s %s" % (self.boundary_obj0.name(), self.boundary_obj1.name())
#         if self.boundary_obj0 and self.boundary_obj1:
#             resstr = (self.boundary_obj0.name( ) + " "
#                       + self.boundary_obj1.name( ) 
#                       + " / " + self.display())
#         else:
#             resstr = "Unassigned / " + self.display()

#         # If there's no Mesh, or if the BC isn't computable on any of
#         # the Mesh's subproblems, then mark the BC as "disabled".
#         if self.meshctxt:
#             for s in self.meshctxt.subproblems():
#                 if not self.is_disabled(s.getObject()): 
#                     return resstr
#                 elif self.explicit_disable:
#                     disstr = "(user disabled) "
#                 else:
#                     disstr = "(incomputable) " #better description?
#         return disstr + resstr

    
    def addToBoundary(self, boundary):
        boundary.addPeriodicCondition(self)

    def removeFromBoundary(self):
        self.boundary_obj0.removePeriodicCondition(self)
        self.boundary_obj1.removePeriodicCondition(self)

    def computable(self, subproblem):
        if not self.meshctxt:
            return None
        return subproblem.is_defined_field(self.field) and \
               subproblem.is_active_field(self.field) and \
               subproblem.is_active_equation(self.equation)

    def display(self):
        return "Periodic / %s / %s" % (`self.field`,`self.equation`)

      
## TODO 3.1: Change to a regular Registration when periodic BCs are
## implemented in 3D.
registeredclass.TwoDOnlyRegistration(
    "Periodic",
    BC,
    PeriodicBC,
    ordering=5,
    params = [
    meshparameters.FieldParameter('field',
                                  tip=parameter.emptyTipString),
    meshparameters.EquationBCParameter('equation',
                                       tip=parameter.emptyTipString),
    bc_periodic_edge_bdy_param
    ],
    tip="Set the values of a field to be equal along two opposite boundaries.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/periodic.xml')
    )

########################################################################
# # # # # # # # # # NEUMANN BOUNDARY CONDITION # # # # # # # # # # # # #
########################################################################

from ooflib.engine.profile import Location
from ooflib.SWIG.common import coord

# Wrapper function for flux boundary profiles.  Takes a number of
# floating-point values provided from within C++, translates them into
# a Location object, and calls the profile object with the location.
# OPT: If this is too slow, the Location construction process can be
# moved into the interior of the flux class's BCCallback routines,
# defined in boundarycond.swg.

if config.dimension() == 2:
    def flux_locator(profile, posx, posy, time, normx, normy,
                     distance, fraction):
        pos = coord.Coord(posx, posy)
        norm = coord.Coord(normx, normy)
        loc = Location(pos, normal=norm, s=distance, alpha=fraction, time=time)
        return profile(loc)
else:
    def flux_locator(profile, posx, posy, posz, time, normx, normy, normz):
        pos = coord.Coord(posx, posy, posz)
        norm = coord.Coord(normx, normy, normz)
        loc = Location(pos, normal=norm, time=time)
        return profile(loc)


# Actual flux boundary condition.  Simpler than the others, because
# most of the action happens in C++.

class NeumannBC(BC):
    def __init__(self, flux, profile, boundary, normal = None,
                 user_enable=True):
        self.flux = flux
        self.normal = normal  
        BC.__init__(self, profile, boundary, user_enable=user_enable)

    def copy(self, boundary):
        return NeumannBC(self.flux, self.profile, boundary,
                         normal=self.normal,
                         user_enable=not self.explicit_disable)
    
    def write(self, file, indent):
        from ooflib.engine import problem # delayed import to avoid a loop
        file.write(indent+"NeumannBC("+problem.inversedict[self.flux]+")")

    def addToBoundary(self, boundary):
        boundary.addFluxCondition(self)

    def removeFromBoundary(self):
        self.boundary_obj.removeFluxCondition(self)

    def conflictsWith(self, other):
        return other.conflictsWithNeumann(self)

    def conflictsWithDirichlet(self, other):
        return conflictDirichletNeumann(other, self)

    def conflictsWithFloat(self, other):
        return conflictFloatNeumann(other, self)

    def conflictsWithPeriodic(self, other):
        return conflictPeriodicNeumann(other, self)

    def conflictsWithForce(self, other):
        return conflictForceNeumann(other, self)

    def conflictsWithNeumann(self, other):
        return conflictNeumannNeumann(self, other)

    def conflictsWithOutOfPlane(self, other):
        return conflictOutOfPlaneNeumann(self, other)

    def computable(self, subproblem):
        if not self.meshctxt:
            return None
        return subproblem.is_active_flux(self.flux)
    
    #
    # Invoke means to do the integral over the appropriate
    # boundary, and make the contributions to the RHS.
    def applyBC(self, subproblem, linearsystem, edgeset, time):
        if self.is_disabled(subproblem):
            return
        if subproblem.is_active_flux(self.flux):
            applicator = boundarycond.NeumannBCApp(subproblem,
                                                   linearsystem,
                                                   self.flux,
                                                   edgeset)
            # For this call, "profile" must be a Python callable.
            if config.dimension() == 2:
                applicator.integrate(flux_locator, self.profile,
                                     self.normal, time)
            else:
                applicator.integrate(flux_locator, self.profile, time);
        else:
            raise ErrSetupError('Attempt to invoke NeumannBC on inactive flux.')
    def display(self):
        return "Neumann / %s" % `self.flux`

# NeumannBC doesn't make sense to apply point-wise (or edge-wise, in
# 3D), use the ForceBC for that.  ForceBC's are specified in terms of
# equations and components, rather than fluxes, because it makes more
# sense.
# Also, specifying the boundary condition in a coordinate system defined by
# the local tangent and normal doesn't make sense in 3D.

neumannparams = [
    meshparameters.FluxParameter(
        "flux",
        tip="Flux whose value is specified across this boundary."),
    profile.FluxProfileSetParameter(
    "profile",
        tip="Profiles describing the prescribed flux.")]
if config.dimension() == 3:
    neumannparams.append(bc_face_bdy_param)
else:
    neumannparams.extend(
        [bc_edge_bdy_param,
        parameter.BooleanParameter(
            "normal",
            tip=
            "If true, the boundary condition is given in a local"
            " right-handed coordinate system where x is the outward normal"
            " to the boundary and y is the tangent direction.  If false,"
            " x and y are lab coordinates."
        )])
    
registeredclass.Registration(
    "Neumann",
    BC,
    NeumannBC,
    ordering=4,
    params = neumannparams,
    tip=
    "Set the normal component of a Flux (eg, stress, heat flux)"
    " along the boundary.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/neumann.xml'))

########################################################################
#Interface branch

## TODO 3.1: Update JumpBC for 3D.  It'll have to apply only to face bcs.
## The registration is currently commented out for both 2D and 3D.

#No addToBoundary method.
#No addJumpCondition or checkJumpCondition methods in EdgeBoundary class.
class JumpBC(BC):
    def __init__(self, field, field_component,
                 jump_value, independent,
                 boundary, #This may be an interfacename
                 user_enable=True):
        self.field = field
        self.field_component = field_component
        self.jump_value=jump_value
        self.independent=independent

        BC.__init__(self,
                    profile.LinearProfile(0,jump_value),
                    boundary, user_enable=user_enable)

    def copy(self, boundary):
        return JumpBC(self.field, self.field_component,
                      self.jump_value, self.independent,
                      boundary,
                      user_enable=not self.explicit_disable)
##    def addToBoundary(self, boundary):
##        boundary.addForceCondition(self)
##    def checkBoundary(self, boundary, exclude):
##        return boundary.checkForceCondition(self, exclude)

    def computable(self, subproblem):
        if not self.meshctxt:
            return None
        return subproblem.is_active_field(self.field)
    #
    # Applied via "applyBC" method, just creates an applicator if it
    # doesn't already have one, and calls it with the node and
    # equation component, and the value to set.  
    #
    def applyBC(self, subproblem, node, value):
        pass
##        if self.is_disabled(subproblem):
##            return
##        eqnindex = self.equation.getIndex(self.eqn_component).integer()
##        try:
##            boundarycond.applyForceBC(subproblem, self.equation,
##                                      node, eqnindex, value)
##        except ooferror2.ErrNoSuchField: # eqn not active at that node
##            pass
    def display(self):
        return ("JumpBC / %s[%s] / jumpvalue=%s / independent=%s" 
                % (`self.field`,
                   self.field_component,
                   self.jump_value,
                   self.independent))
                
    #Override the one from the parent BC class
    def add_to_mesh(self, name, mesh):
        self._name = name 
        self.mesh = mesh # Mesh name.
        
        self.meshctxt = ooflib.engine.mesh.meshes[mesh] # Who object.

        femeshobj=self.meshctxt.getObject()
        femeshobj.addInterfaceBC(name)

##        try:
##            self.boundary_obj = self.meshctxt.getBoundary(self.boundary)
##        except KeyError:
##            raise

        self.profile.addCondition(self)
##        self.boundary_obj.addCondition(self)

        # Auto-enable must precede the meshctxt add call below, which
        # builds the display string, which depends on side-effects of
        # auto_enable. (Really?)
        for subproblem in self.meshctxt.subproblems():
            self.auto_enable(subproblem)
        self.meshctxt.addBdyCondition(name, self)

    #Override the one from the parent BC class
    def remove_from_mesh(self):
        self.meshctxt.rmBdyCondition(self)

    #Override the one from the parent BC class
    def disconnect(self):
        self.profile.removeCondition(self)
        self.meshctxt = None
        self.mesh = None
        self.computableDict = {}
        #self.boundary_obj.removeCondition(self)
        #self.boundary_obj = None

        # Break circular references, but leave in the ones
        # corresponding to parameters.
        
        # self.boundary = None
        # self.profile=None
        # Clean up callbacks.

    def intersect(self, other):
        # Other should be another JumpBC.
        return (self.field == other.field and
                self.field_component == other.field_component)

    #Override the one from the parent BC class
    def check(self, mesh, exclude=None):
        # Check that this bc doesn't conflict with any other bc on
        # this mesh. This doesn't check the *values* of the boundary
        # conditions.  It only checks that two Dirichlet or floating
        # boundary conditions don't apply to the same degrees of
        # freedom on the same boundary.
        # If the 'exclude' variable is equal to some other bc, then
        # conflicts with that bc aren't counted.

        try:
            meshctxt = ooflib.engine.mesh.meshes[mesh]                
        except:
            return "There is no mesh named '%s'!" % mesh

        meshobj=meshctxt.getObject()
        for jumpbcname in meshobj.listInterfaceBC():
            jumpbc=meshctxt.getBdyCondition(jumpbcname)
            if jumpbc.boundary==self.boundary and \
                   jumpbc is not exclude and \
                   jumpbc.intersect(self) and \
                   not jumpbc.is_explicitly_disabled():
                return "Jump BC collision on interface"
##        try:
##            boundary_obj = meshctxt.getBoundary(self.boundary)
##        except:
##            return "There is no boundary named '%s'!" % self.boundary
##        return boundary_obj.checkCondition(self, exclude=exclude)
        return ""

# registeredclass.Registration("Field Discontinuity",
#                              BC,
#                              JumpBC,
#                              ordering=6,
#                              params = bc_field_param_group + [
# ##    parameter.RegisteredParameter(
# ##    'profile', reg=profile.Profile, value=None,
# ##    tip='Profile describing how this condition varies.'),
#     parameter.FloatParameter('jump_value', 0.0,
#                              tip='Value for the field jump or discontinuity'),
#     parameter.BooleanParameter('independent', 0,
#                                tip='Ignore jump value?'),
# ##    meshparameters.MeshEdgeBdyInterfaceParameter('boundary',
# ##                                                 tip='Edge boundary or interface to which this condition applies.')
#     bc_edge_bdy_param],
#                              tip="Jump in a field value across a boundary",
#                              discussion = 
# """<para>

# This boundary condition imposes a finite jump in the value of a field
# across an interface or boundary. The 'sense' of the jump refers to the
# field value on the node to the right of the boundary relative to the
# field value on the node to the left of the boundary. If independent is
# set to True, then no constraints are specified between the field
# values.  When no boundary conditions for the field are specified
# across an interface, hidden Floating boundary conditions are
# automatically created that keep the field value continuous across the
# boundary when the finite element system is solved.

# </para>"""
#                              )


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#




# Boundary condition compatibility functions.  These are implemented
# as functions and not as class methods to ensure that
# A.conflictsWithB is compatible with B.conflictsWithA.

def _fieldEqnConflict(bc0, bc1):
    return ((bc0.field == bc1.field and
            bc0.field_component == bc1.field_component) or
            (bc0.equation == bc1.equation and
             bc0.eqn_component == bc1.eqn_component))

def _nocomponentFieldEqnConflict(bc0,bc1):
    return (bc0.field == bc1.field) or (bc0.equation == bc1.equation)

def conflictDirichletDirichlet(bc0, bc1):
    return _fieldEqnConflict(bc0, bc1)

def conflictDirichletForce(bc0, bc1):
    return False

def conflictDirichletFloat(bc0, bc1):
    return _fieldEqnConflict(bc0, bc1)

def conflictDirichletPeriodic(bc0, bc1):
    return False

def conflictDirichletNeumann(bc0, bc1):
    return False

def conflictForceForce(bc0, bc1):
    return (bc0.equation == bc1.equation and 
            bc0.eqn_component == bc1.eqn_component)

def conflictForceFloat(bc0, bc1):
    return False

def conflictForcePeriodic(bc0, bc1):
    return False

def conflictForceNeumann(bc0, bc1):
    return False

def conflictFloatFloat(bc0, bc1):
    return _fieldEqnConflict(bc0, bc1)

def conflictFloatPeriodic(bc0, bc1):
    return False

def conflictFloatNeumann(bc0, bc1):
    return False

def conflictPeriodicPeriodic(bc0, bc1):
    return _nocomponentFieldEqnConflict(bc0, bc1)

def conflictPeriodicNeumann(bc0, bc1):
    return False

def conflictNeumannNeumann(bc0, bc1):
    return bc0.flux == bc1.flux



def conflictOutOfPlaneOutOfPlane(bc0,bc1):
    return _nocomponentFieldEqnConflict(bc0,bc1)

def conflictOutOfPlaneDirichlet(bc0,bc1):
    return False

def conflictOutOfPlaneNeumann(bc0,bc1):
    return False

def conflictOutOfPlaneForce(bc0,bc1):
    return False

def conflictOutOfPlaneFlux(bc0,bc1):
    return False

def conflictOutOfPlaneFloat(bc0,bc1):
    return False

def conflictOutOfPlanePeriodic(bc0,bc1):
    return False
