# -*- python -*-
# $RCSfile: boundary.py,v $
# $Revision: 1.77.2.15 $
# $Author: langer $
# $Date: 2014/09/10 21:28:42 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

# A note on EdgeBoundary, PointBoundary, and Profile classes.
#
# A Profile is an as-generic-as-possible way of getting values of some
# function out, given some indiciation of where to evaluate.  The
# indiciation is given in several forms at once -- the index of the
# current node (conventionaly denoted by i), the (x,y) location of the
# current evaluation, the distance (conventionally denoted s) along
# the current boundary, and the fractional distance (conventionally,
# alpha) along the current boundary.  The location information may
# include orientation information about the current normal direction
# of the boundary, (nx, ny).  (x,y) and "alpha" will always be
# provided.  "i" will be provided by PointBoundaries, and "s" and (nx,
# ny) will be provided by EdgeBoundaries.
#
# EdgeBoundaries are smooth sets of edges, and expect to be able
# to evaluate their corresponding conditions' profiles by passing
# in (x,y), (nx, ny), s, and alpha.
#

# PointBoundaries are sets of nodes, and expect to evaluate their
# profiles by passing the integer index i of the node within the
# boundary, along with its (x,y) location and "alpha".  The meaning of
# "alpha" in this context is that it is 0 for the first node, 1 for
# the last node, and progresses linearly with nodes, except for a
# PointBoundary with exactly one node, where it is 0.
#
# As currently instantiated, it's not possible to convert
# continuum boundaries into point boundaries, even though
# continuum boundaries have a nodal representation.  In
# principle, a flux boundary condition can be expressed in
# terms of equivalent forces at nodes, which we might want to
# do later.


from ooflib.SWIG.common import config
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.engine import edgeset
from ooflib.common import debug
from ooflib.common import registeredclass
from ooflib.common import utils
from ooflib.engine import profile
import copy
import ooflib.engine.mesh
ErrSetupError = ooferror.ErrSetupError


# This class describes the value of a profile (associated with a
# condition) at a particular node.  It's primarily used for
# intersection checking, and allows the actual evaluation of the
# profile function (presumed to be expensive) to be deferred until a
# coincidence of location and field are certain.  The associated
# boundary may be either Edge or Point, this class doesn't care.


class LocatedCondition:
    def __init__(self, bc, here = None):
        self.condition = bc
        self.here = here # "Location" object, promises .position member.
    def __call__(self):  # TODO 3.1: Give this a real method name.
        if self.here:
            return self.condition.profile(self.here)
        else:
            raise ErrSetupError("No location specified in LocatedCondition.")
        

#*=-=*##*=-=*##*=-=*##*=-=#*=-=*##*=-=*##*=-=*##*=-=*##*=-=*##*=-=*##*=-=*#

# Parent class of EdgeBoundary and PointBoundary, has a few simple
# global operations.  Fixed and float conditions are stored explicitly
# because they need to be checked for collisions.
class Boundary:
    def __init__(self, name, mesh, visible=True):
        self._name = name
        self.mesh = mesh # C Femesh instance.
        self.floatConditions = []
        self.fixedConditions = []
        self.allConditions = {}
        self.visible = visible
    #
    # Redefine "size" in subclasses.
    def size(self):
        pass
    
    def empty(self):
        return self.size() == 0

    def name(self):
        return self._name

    def rename(self, name):
        self._name = name

    def addCondition(self, condition):
        self.allConditions[condition.name()]=condition
        condition.addToBoundary(self)

    def renameCondition(self, oldname, newname):
        self.allConditions[newname] = self.allConditions[oldname]
        del self.allConditions[oldname]

    def addFloatCondition(self, condition):
        self.floatConditions.append(condition)

    def addFixedCondition(self, condition):
        self.fixedConditions.append(condition)

    def removeFixedCondition(self, condition):
        self.fixedConditions.remove(condition)
        del self.allConditions[condition.name()]

    def removeFloatCondition(self, condition):
        self.floatConditions.remove(condition)
        del self.allConditions[condition.name()]

    def createAuxiliaryBCs(self):
        allconds = self.allConditions.values()[:]
        for bc in allconds:
            bc.create_auxiliary_BCs()

    def removeAuxiliaryBCs(self):
        allconds = self.allConditions.values()[:]
        for bc in allconds:
            bc.remove_auxiliary_BCs()

    def invokeFixed(self, subproblem, linearsystem, time):
        if self.fixedConditions:
            for (node, location) in self.locations():
                if subproblem.containsNode(node):
                    location.set_time(time)
                    for bc in self.fixedConditions:
                        # bc is a BC subclass (DirichletBC, probably)
                        # instance from bdycondition.py.
                        # DirichletBC.applyBC sets the Field value and
                        # the fixed and dependent flags for the DoF
                        # and nodal eqn in the linearsystem object.
                        bc.applyBC(subproblem, linearsystem, node, location)

    def reinvokeFixed(self, subproblem, time):
        if self.fixedConditions:
            for (node, location) in self.locations():
                if subproblem.containsNode(node):
                    location.set_time(time)
                    for bc in self.fixedConditions:
                        bc.reapply(subproblem, node, location)

    def setDirichletDerivatives(self, subproblem, linearsystem, time):
        # Evaluate the time derivatives of the fixed (Dirichlet) bcs
        # and store them in the linearsystem.
        if self.fixedConditions:
            for (node,location) in self.locations():
                if subproblem.containsNode(node):
                    location.set_time(time)
                    for bc in self.fixedConditions:
                        if bc.isTimeDependent():
                            bc.setDerivatives(subproblem, linearsystem,
                                              node, location)
    def invokeFloat(self, subproblem, linearsystem, time, bc):
        for (node, location) in self.locations():
            if subproblem.containsNode(node):
                location.set_time(time)
                bc.applyBC(subproblem, linearsystem, node, location)

    def fixFloatTree(self, bc, linsys, val, time):
        # Called by FloatBC.fixIfFixed() to fix all of the DoFs in a
        # FloatBC and intersecting FloatBCs, once it's known that at
        # least one of the DoFs is fixed by an intersecting condition.
        bc.fixFloatTree(linsys, val, self.locations(), time)

    def expandFloat(self, subproblem, time):
        # expandFloat() is called by FEMeshPtr.expand_float_bcs()
        # which is called by SubProblemContext.set_mesh_dofs().  It
        # operates on the FEMesh's dofvalues vector.
        if self.floatConditions:
            for (node, location) in self.locations():
                if subproblem.containsNode(node):
                    location.set_time(time)
                    for bc in self.floatConditions:
                        if not (bc.is_disabled(subproblem) or bc.isFixed()):
                            # See bdycondition.py
                            bc.setMeshValue(subproblem, node, location)
                            # bc.expand(subproblem, node, location)

    # Provide benign implementations of the optional invocations.
    def invokeFlux(self, subproblem, linearsystem, time):
        pass

    def invokeForce(self, subproblem, linearsystem, time):
        pass
    
    # Functions that help out with intersection-detection.
    # Return a dictionary of nodes whose values are lists of
    # LocatedCondition objects.  A "LocatedCondition" knows how
    # to evaluate the condition's profile at this node.
    
    def getFixedGeometry(self, subproblem, time):
        redict = {}
        if self.fixedConditions:
            for (node, location) in self.locations():
                location.set_time(time)
                reslist = []
                for fixedbc in self.fixedConditions:
                    # do not include disabled bc's
                    if not fixedbc.is_disabled(subproblem):
                        reslist.append(
                            LocatedCondition(fixedbc, location))
                redict[node] = reslist
        return redict
    
    def getFloatGeometry(self, subproblem, time):
        redict = {}
        if self.floatConditions:
            for (node, location) in self.locations():
                location.set_time(time)
                reslist = []
                for floatbc in self.floatConditions:
                    # do not include disabled bc's
                    if not floatbc.is_disabled(subproblem):
                        reslist.append(LocatedCondition(floatbc, location))
                redict[node] = reslist
        return redict

    def getUnconditionalFloatGeometry(self, time):
        redict = {}
        if self.floatConditions:
            for (node, location) in self.locations():
                location.set_time(time)
                reslist = []
                for floatbc in self.floatConditions:
                    if not floatbc.is_explicitly_disabled():
                        reslist.append(LocatedCondition(floatbc, location))
                redict[node] = reslist
        return redict

    def checkConditions(self):
        # Check for incompatibilities between boundary conditions.
        # Returns a list of error messages.
        errors = []
        for (bc0, bc1) in utils.unique_pairs(self.allConditions.values()):
            if not (bc0.is_explicitly_disabled()
                    or bc1.is_explicitly_disabled()):
                if bc0.conflictsWith(bc1):
                    errors.append(
                        "Boundary conditions %s and %s conflict on %s" %
                        (bc0.name(), bc1.name(), self.name()))
        return errors

    # Reset function for stateful boundary conditions.
    def reset(self):
        for floatbc in self.floatConditions[:]:
            floatbc.reset()
        self.removeAuxiliaryBCs()

    # Make FloatBCs' contribution to the rhs vector for linear
    # problems.  Called by FEMesh.float_contrib_rhs() in femesh.spy.
    def contribRHS(self, subproblem, linearsystem):
        for bc in self.floatConditions:
            bc.contrib_rhs(subproblem, linearsystem)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Face Boundaries

class FaceBoundary(Boundary):
    def __init__(self, name, mesh, fset = None):
        Boundary.__init__(self, name, mesh)
        self.faceset = fset or edgeset.FaceSet(self.mesh)
        self.fluxConditions = []
        self.periodicConditions = []
    def parts(self):
        return self.faceset
    def size(self):
        return self.faceset.size()
    # TODO MER: We should probably consolidate some of this code with the
    # Edge Boundary class

    def __repr__(self):
        outstr = "FaceBoundary(" 
        for floatcnd in self.floatConditions:
            outstr += floatcnd.__repr__()
        for fixed in self.fixedConditions:
            outstr += fixed.__repr__()
        for flux in self.fluxConditions:
            outstr += flux.__repr__()
        outstr += ")"
        return outstr
    #
    def clearConditions(self):
        self.floatConditions = []
        self.fixedConditions = []
        self.fluxConditions = []
        self.periodicConditions = []

    # AddFace, gateway to the FaceSet.
    def addFace(self, boundaryface, reverse):
        self.faceset.add(boundaryface, reverse)

    def addFluxCondition(self, condition):
        self.fluxConditions.append(condition)

    def removeFluxCondition(self, condition):
        self.fluxConditions.remove(condition)

    def addForceCondition(self, condition):
        raise ErrSetupError("Face boundaries do not support force conditions.")

    def invokeFlux(self, subproblem, linearsystem, time):
        for bc in self.fluxConditions:
            bc.applyBC(subproblem, linearsystem, self.faceset, time)

    def locations(self):
        return self.faceset.locations()

    def getNodes(self):
        return self.faceset.getNodes()

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
   
# An EdgeBoundary object has as its geometry an Edgeset.

# See comments at PointBoundary for info about maintaining consistency.

class EdgeBoundary(Boundary):
    def __init__(self, name, mesh, eset=None):
        Boundary.__init__(self, name, mesh)
        self.edgeset = eset or edgeset.EdgeSet(self.mesh)
        self.fluxConditions = []
        self.periodicConditions = [] 
    def parts(self):
        return self.edgeset
    def size(self):
        return self.edgeset.size()
    def __repr__(self):
        outstr = "\nEdgeBoundary(" # TODO 3.1: Why the \n?
        for float in self.floatConditions:
            outstr += float.__repr__()
        for fixed in self.fixedConditions:
            outstr += fixed.__repr__()
        for flux in self.fluxConditions:
            outstr += flux.__repr__()
        outstr += ")"
        return outstr

    def clearConditions(self):
        self.floatConditions = []
        self.fixedConditions = []
        self.fluxConditions = []
        self.periodicConditions = []

    # AddEdge, gateway to the EdgeSet.
    def addEdge(self, bdyelement, reverse):
        # Don't use EdgeSet.add() here.  addEdge operates on the node cache
        self.edgeset.addEdge(bdyelement, reverse)

    def whichPeriodicEdge(self, meshctxt):
        # Helper function returns which periodic outer edge this
        # boundary spans and it's direction.  If the edge boundary in
        # question does not span a periodic outer edge, the function
        # returns 0.
        ## TODO 3.1: Update this for 3D when PBCs are implemented.
        skel = meshctxt.getObject().skeleton
        nodes = self.edgeset.nodes()
        if (nodes[0].position().x == nodes[1].position().x and
            skel.x_periodicity):
            if (nodes[0].position().y == 0 and
                nodes[-1].position().y == skel.MS.size()[1]):
                direction = 1
            elif (nodes[-1].position().y == 0 and
                  nodes[0].position().y == skel.MS.size()[1]):
                direction = -1
            else:
                return 0
            for i in xrange(2,len(nodes)):
                if not nodes[i].position().x == nodes[i-1].position().x:
                    return 0
            return ('x',nodes[0].position().x,direction)
        if (nodes[0].position().y == nodes[1].position().y and
            skel.y_periodicity):
            if (nodes[0].position().x == 0 
                and nodes[-1].position().x == skel.MS.size()[0]):
                direction = 1
            elif (nodes[-1].position().x == 0 and
                  nodes[0].position().x == skel.MS.size()[0]):
                direction = -1
            else:
                return 0
            for i in xrange(2,len(nodes)):
                if not nodes[i].position().y == nodes[i-1].position().y:
                    return 0
            return ('y',nodes[0].position().y,direction)

    def addPeriodicCondition(self, condition):
        self.periodicConditions.append(condition)

    def removePeriodicCondition(self, condition):
        self.periodicConditions.remove(condition)

    def addFluxCondition(self, condition):
        # Flux (Neumann) boundary conditions don't make sense on edge
        # boundaries in 3D.
        assert config.dimension() == 2
        self.fluxConditions.append(condition)

    def removeFluxCondition(self, condition):
        self.fluxConditions.remove(condition)

    def addForceCondition(self, condition):
        raise ErrSetupError("Edge boundaries do not support force conditions.")

    def invokeFlux(self, subproblem, linearsystem, time):
        for bc in self.fluxConditions:
            bc.applyBC(subproblem, linearsystem, self.edgeset, time)

    def locations(self):
        return self.edgeset.locations()

    def getNodes(self):
        return set(self.edgeset.nodes())

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class PointBoundary(Boundary):
    def __init__(self, name, mesh, nodeset=None, visible=True):
        Boundary.__init__(self, name, mesh, visible)
        if nodeset:
            self.nodeset = nodeset
        else:
            self.nodeset = NodeSet(mesh)
        self.forceConditions = []
    # Generic "addNode" capability might be useful -- if you just want
    # to group nodes, e.g. corners, and then do the same thing to all
    # of them, it may not be necessary to distinguish between individual
    # nodes on the basis of keys.  For this case, auto-generate a key
    # and use it to insert into the dictionary.  

    def size(self):
        return len(self.nodeset)
    def __repr__(self):
        outstr = "PointBoundary("
        for float in self.floatConditions:
            outstr += float.__repr__()
        for fixed in self.fixedConditions:
            outstr += fixed.__repr__()
        for force in self.forceConditions:
            outstr += force.__repr__()
        outstr += ")"
        return outstr

    def clearConditions(self):
        self.floatConditions = []
        self.fixedConditions = []
        self.forceConditions = []

    def addNode(self, node):
        self.nodeset.addNode(node)

    def addFluxCondition(self, condition):
        raise ErrSetupError("Point boundaries do not support flux BC's.")

    def addPeriodicCondition(self, condition):
        raise ErrSetupError("Point boundaries do not support periodic BC's.")

    def addForceCondition(self, condition):
        self.forceConditions.append(condition)

    def removeForceCondition(self, condition):
        self.forceConditions.remove(condition)
        del self.allConditions[condition.name()]

    def invokeForce(self, subproblem, linearsystem, time):
        if self.forceConditions:
            for (node, location) in self.nodeset.locations():
                location.set_time(time)
                for bc in self.forceConditions:
                    bc.applyBC(subproblem, linearsystem, node, location)

    def locations(self):
        return self.nodeset.locations()

    def getNodes(self):
        return set(self.nodeset.data)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# BoundaryObjectSet class -- provides an ordered list of nodes or
# faces, and knows their indices.

class BoundaryObjectSet:
    def __init__(self, mesh):
        self.mesh = mesh
        self.data = []
    # Since data is a list, key must be an integer.
    def __getitem__(self, key):
        return self.data[key]
    def __len__(self):
        return len(self.data)


# Node set can also provide a "location" service, which returns the
# appropriate object. 
class NodeSet(BoundaryObjectSet):
    def addNode(self, node):
        self.data.append(node)
    def removeNode(self, node):
        self.data.remove(node)
        
    # Return a list of location objects, one for each node, in sequence.
    # For the moment, location objects are just tuples, in the order
    # "(x,y), i, s, alpha, (nx, ny)".
    def locations(self):
        # In the one-element list case, you can't divide by len-1.
        if len(self.data)==1:
            return [ (self.data[0], profile.Location(self.data[0].position(),
                                                     index=0, alpha=0.0) ) ]
        # We used to pass alpha=i*1.0/(len(self.data)-1) to the
        # Location constructor, but it seems wrong to allow
        # profiles to depend on alpha for a discrete set of
        # points.
        return [(node, profile.Location(node.position(), index=i))
                for (i, node) in enumerate(self.data)]

        # result = []
        # for i in range(0, len(self.data)):
        #     node = self.data[i]
        #     result.append(
        #         (node, profile.Location(node.position(), index=i)))
        # return result

