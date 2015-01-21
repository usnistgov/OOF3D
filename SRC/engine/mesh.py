# -*- python -*-
# $RCSfile: mesh.py,v $
# $Revision: 1.224.2.28 $
# $Author: langer $
# $Date: 2014/11/05 16:54:25 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

# The Mesh class is the Who class wrapper for the C++ FEMesh class,
# associating a Skeleton and miscellaneous bookkeeping information
# with it.  Mesh itself is a Who class, which means it can participate
# in the layer-display process.

from ooflib.SWIG.common import lock
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common import config
from ooflib.SWIG.common import timestamp
from ooflib.SWIG.engine import entiremeshsubproblem
from ooflib.SWIG.engine import material
from ooflib.SWIG.engine import meshdatacache
from ooflib.SWIG.engine import ooferror2
from ooflib.common import debug
from ooflib.common import labeltree
from ooflib.common import parallel_enable
from ooflib.common import ringbuffer
from ooflib.common import utils
from ooflib.common.IO import placeholder
from ooflib.common.IO import whoville
from ooflib.engine import meshstatus
from ooflib.engine import outputschedule

#Interface branch
from ooflib.engine import skeletoncontext
from ooflib.engine import bdycondition

import math, sys

# TODO 3.1: Move switchboard.notify calls out of this file and put
# them in menu items, or other appropriate places. 

## TODO 3.1: Add a Mesh modification method that detects regions which
## are insufficiently connected.  I.e, when solving an elasticity
## problem, there cannot be two regions of the Mesh connected by only
## a single node, unless boundary conditions are applied on both
## regions.  Detecting these regions can be done (in 2D) by extracting
## exterior segments and finding closed loops of exterior segments and
## nodes which contain more than two exterior segments.

# Helper class for keeping track of the cross-sections -- remembers
# what the most-recently-added one was by remembering the order.
class CrossSectionSet:
    def __init__(self):
        self.data = {}
        self.namelist = []
        self._selection = None
        # self.timestamp = timestamp.TimeStamp()
    def new(self, name, cs):
        self.data[name]=cs
        self.namelist.append(name)
        # self.timestamp.increment()
        self._selection = name           # always select new cross section
    def remove(self, name):
        del self.data[name]
        self.namelist.remove(name)
        # self.timestamp.increment()
        if self._selection == name:
            if self.namelist:
                self._selection = self.namelist[-1]
            else:
                self._selection = None
#     def destroy(self):
#         self.data = {}
#         self._selection = None
    def all_names(self):
        return self.namelist
    def __getitem__(self, key):
        return self.data[key]
    def selected(self):
        try:
            return self.data[self._selection]
        except KeyError:
            return None
    def selectedName(self):
        return self._selection
    def select(self, name):
        self._selection = name
        # self.timestamp.increment()
    def deselect(self):
        self._selection = None
        # self.timestamp.increment()
    def rename(self, oldname, newname):
        cs = self.data[oldname]
        newname = utils.uniqueName(newname, self.namelist, exclude=oldname)
        self.namelist[self.namelist.index(oldname)] = newname
        del self.data[oldname]
        self.data[newname] = cs
        if oldname == self._selection:
            self._selection = newname
        return newname
    def replace(self, name, cross_section):
        self.data[name] = cross_section
        # self.timestamp.increment()

######################

class Mesh(whoville.Who):
    def __init__(self, name, classname, femesh, parent,
                 skeleton=None, elementdict=None,
                 materialfactory=None):
        whoville.Who.__init__(self, name, classname, femesh, parent)
        # Share the mesh-level lock with the contained femesh.
        femesh.set_rwlock(self.rwLock)

        self.elementdict = elementdict
        self.materialfactory = materialfactory
        femesh.set_parent_mesh(self)

        # Cross-section stuff
        self.cross_sections = CrossSectionSet()

        # Cache for time step data. 
        self.setDataCache(meshdatacache.newMeshDataCache())
                
        # self.masterCacheLock = lock.Lock()
        # # pthreads condition variable that indicates when the cache
        # # isn't being read.
        # self.noCacheReadersCond = lock.Condition(self.masterCacheLock)
        # self.nCacheReaders = 0 # number of threads reading the current data

        # Timestamps.  BoundariesChanged is incremented whenever a
        # boundary or boundary condition is added or removed.
        self.boundariesChanged = timestamp.TimeStamp() # last bdy change
        self.fieldsInitialized = timestamp.TimeStamp()
        self.materialsChanged = timestamp.TimeStamp()

        self.initializers = {}  # Field initializers
        self.bdyconditions = {}

        # Point boundaries used by periodic boundary conditions
        self.periodicPointBoundaries = {}

        # solverDelta stores the size of the last time step taken by
        # Mesh.solve().
        self.solverDelta = None
        # timeDiff stores the last global time step used.  It lets the
        # GUI set a reasonable default end time for the next
        # evolution.
        self.timeDiff = None

        self.outputSchedule = outputschedule.OutputSchedule(self)

        self.status = meshstatus.Unsolved("New mesh.")

    def createDefaultSubProblem(self):
        subptype = entiremeshsubproblem.entiremeshreg()
        self.newSubProblem(subptype.create(), subptype,
                           self.path() + ":" + defaultSubProblemName)

    def rebuildMesh(self):
        # Recreate the FEMesh from the Skeleton, which is assumed to
        # have changed.  Fields, equations, boundary conditions,
        # subproblems, solvers, etc. will be transferred from the old
        # FEMesh to the new one.

        # The Mesh's write lock must be acquired before calling
        # rebuildMesh().
        old_femesh = self.femesh()
        old_skel = old_femesh.skeleton
        skelpath = labeltree.makePath(self.path())[:-1]
        new_skel = skeletoncontext.skeletonContexts[skelpath].getObject()
        new_femesh = new_skel.femesh(self.elementdict, self.materialfactory)
        new_femesh.set_rwlock(self.rwLock)

        if config.dimension() == 2:
            # Before doing anything else, retrieve the field planarity
            # data from the old mesh.
            planarity = {}
            for field in self.all_compound_subproblem_fields():
                planarity[field] = old_femesh.in_plane(field)

        # Call to setFEMesh() must precede calls to
        # CSubProblem.set_mesh(), which are made by the
        # SubProblemContext constructor.
        self.setFEMesh(new_femesh)

        self.setDataCache(meshdatacache.newMeshDataCache())

        subprobs = []
        notifications = set()
        for subpctxt in self.subproblems():
            name = subpctxt.name()
            # Subproblems will be created with uniquified names,
            # but we'll change the names back after deleting the
            # original subproblems.
            ## TODO OPT: Is it necessary to build new subproblems?
            ## Can't we just re-use the old ones?  Is it slow enough
            ## to matter?
            newsubpctxt = subpctxt.clone(
                self, copy_field=True, copy_equation=True,
                notifications=notifications)
            subprobs.append((subpctxt, newsubpctxt))
        new_femesh.setCurrentTime(old_femesh.getCurrentTime())

        if config.dimension() == 2:
            # SubProblemContext.clone didn't set the Field
            # planarities.  Do it now.
            for field, inplane in planarity.items():
                self.set_in_plane_field(field, inplane)
                notifications.add(('field inplane', self.path(),
                                   field.name(), inplane))

        # Copy Field values from the old FEMesh
        for field in self.all_subproblem_fields():
            new_femesh.init_field(old_skel, old_femesh, field)

        # Destroy old subproblems and give the new subproblems
        # their correct names.  (This has to happen *after* the
        # fields are copied because if the subproblems are deleted
        # from the old mesh, the field values will be destroyed.)
        for old_subpctxt, new_subpctxt in subprobs:
            oldname = labeltree.makePath(old_subpctxt.path())[-1]
            self.pause_writing()
            try:
                old_subpctxt.begin_writing()
                try:
                    old_subpctxt.destroy()
                finally:
                    old_subpctxt.end_writing()
                new_subpctxt.begin_writing()
                try:
                    new_subpctxt.rename(oldname)
                    new_subpctxt.getObject().set_mesh(self)
                finally:
                    new_subpctxt.end_writing()
            finally:
                self.resume_writing()

        # Copy BCs to the new FEMesh
        for name, bc in self.allBoundaryConds():
            # Interface branch.  Don't copy the invisible Float BCs
            # associated with interfaces.  See femesh.spy.
            if name.find("_cntnty_") == 0:
                pass
            # Jump BCs don't have an associated mesh boundary object.
            # TODO 3.1: Why not?
            elif isinstance(bc, bdycondition.JumpBC):
                new_femesh.addInterfaceBC(name)
            else:
                bc.boundary_obj = new_femesh.getBoundary(bc.boundary)
                new_femesh.boundaries[bc.boundary].addCondition(bc)

        self.setStatus(meshstatus.Unsolved("Newly rebuilt."), resync=True)

        self.pause_writing()
        try:
            for notification in notifications:
                switchboard.notify(*notification)
            for subproblem in self.subproblems():
                subproblem.autoenableBCs()
        finally:
            self.resume_writing()
        old_femesh.destroy()

    # # getTimeStamp has a gfxwindow arg so that it can work with
    # # WhoProxies.
    # def getTimeStamp(self, gfxwindow):
    #     subtimes = [sub.getTimeStamp() for sub in self.subproblems()]
    #     # 'max(self.getOwnTimeStamp(), *subtimes)' is a
    #     # syntax error if subtimes is an empty list, so we have to
    #     # check.
    #     if subtimes:
    #         return max(self.getOwnTimeStamp(), *subtimes)
    #     return self.getOwnTimeStamp()
    def getOwnTimeStamp(self):
        return max(self.materialsChanged, self.boundariesChanged,
                   self.fieldsInitialized)

    def femesh(self):
        return self.getObject()

    def size(self):
        return self.getMicrostructure().size()

    # utility function from "femesh"
    def nelements(self):
        return self.getObject().nelements()

    #Interface branch
    def nedgements(self):
        return self.getObject().nedgements()

    def nnodes(self):
        return self.getObject().nnodes()

    # Required for compatibility with Display objects which work for
    # both Mesh and Skeleton who classes.
    def mesh(self):
        return self.getObject()

    def getSkeleton(self):  # returns the current skeleton object (not context)
        return self._obj.skeleton

    def setFEMesh(self, femesh):
        time = self._obj.getCurrentTime()
        self._obj = femesh  # replace the old one with the new one
        self._obj.set_parent_mesh(self)
        self._obj.setCurrentTime(time)

    def getMicrostructure(self):
        return self.getParent().getParent().getObject()

    def getMasterElementType(self, geom):
        try:
            return self.elementdict[geom].name()
        except KeyError:
            return '---'

    def destroy(self):
        global meshes
        for bc in self.bdyconditions.values():
            if not bc.subordinate:
                self.rmBdyCondition(bc)
#         self.cross_sections.destroy()
        self.periodicPointBoundaries = {}
        self.bdyconditions = {}
        self.getObject().destroy()
        # Remove from the enclosing WhoClass.  This nulls out parent's "._obj".
        meshes.remove(self.path())
        self.datacache = None
#        self.datacache.clear()

    def lockAndDelete(self):
        self.reserve()
        try:
            # Delete subproblems.  Since some subproblems depend on
            # other subproblems, deleting one may trigger the deletion
            # of others.  Therefore we can't simply loop over
            # self.subproblems() with a "for" loop.
            while len(self.subproblems()) > 0:
                subproblem = self.subproblems()[0]
                subproblem.begin_writing()
                subproblem.destroy()
                subproblem.end_writing()
            self.begin_writing()
            try:
                self.destroy()
            finally:
                self.end_writing()
        finally:
            self.cancel_reservation()

    ##################

    # Subproblem management

    def newSubProblem(self, subproblem, subptype, path):
        # "subproblem" is a SubProblem object.  Adding it to the
        # SubProblem Who class creates a SubProblemContext.
        from ooflib.engine import subproblemcontext  # avoid import loop
        return subproblemcontext.subproblems.add(path, subproblem, self,
                                                 subptype=subptype)

    def subproblemNames(self):
        if self.defunct():
            return []
        from ooflib.engine import subproblemcontext
        path = self.path()
        if not path:
            raise ooferror2.ErrPyProgrammingError("No path to mesh '%s'!?"
                                                 % self.name())
        subpaths = subproblemcontext.subproblems.keys(base=path)
        ## subpaths is a list of relative paths of length 1.
        return [s[0] for s in subpaths]

    def subproblems(self):
        if self.defunct():
            return []
        return [self.get_subproblem(n) for n in self.subproblemNames()]

    def nSubproblems(self):
        from ooflib.engine import subproblemcontext
        return len(subproblemcontext.subproblems.keys(base=self.path()))

    def get_default_subproblem(self):
        return self.get_subproblem(defaultSubProblemName)

    def get_subproblem(self, name):
        from ooflib.engine import subproblemcontext
        return subproblemcontext.subproblems[self.path()+":"+name]

    #################

    # No equations are ever activated directly in a mesh, but the
    # boundary conditions need to know which equations are available.
    # So, this routine polls the subproblems and returns the set of
    # available equations.

    # "all_subproblem" prefix means they're for all subproblems.
    
    def all_subproblem_equations(self):
        eqns = utils.OrderedSet()
        for s in self.subproblems():
            for e in s.all_equations():
                eqns.add(e)
        return eqns
    def all_subproblem_equations_bc(self): # just eqns that can have bc's.
        eqns = utils.OrderedSet()
        for s in self.subproblems():
            for e in s.all_equations_bc():
                eqns.add(e)
        return eqns

    # Analysis can be done on any compound Field from any SubProblem.
    def all_compound_subproblem_fields(self):
        flds = utils.OrderedSet()
        for s in self.subproblems():
            for f in s.all_compound_fields():
                flds.add(f)
        return flds

    # Really all fields, including out-of-plane parts.
    def all_subproblem_fields(self):
        fields = utils.OrderedSet()
        for s in self.subproblems():
            for f in s.all_fields():
                fields.add(f)
        return fields

    def all_active_subproblem_fields(self):
        fields = utils.OrderedSet()
        for s in self.subproblems():
            for f in s.all_compound_fields():
                if s.is_active_field(f):
                    fields.add(f)
        return fields

    def all_initializable_fields(self):
        fields = utils.OrderedSet()
        for s in self.subproblems():
            for f in s.all_compound_fields():
                if self.is_defined_field(f):
                    fields.add(f)
                    if config.dimension() == 2:
                        if not f.in_plane(self.getObject()):
                            fields.add(f.out_of_plane())
                    if (s.time_stepper is not None
                        and s.time_stepper.derivOrder() > 0
                        and f in s.second_order_fields()):
                        fields.add(f.time_derivative())
        return fields

    # Analysis can be done on any Flux from any SubProblem
    def all_subproblem_fluxes(self):
        fluxes = utils.OrderedSet()
        for s in self.subproblems():
            for f in s.all_fluxes():
                fluxes.add(f)
        return fluxes

    def is_defined_field(self, field):
        for s in self.subproblems():
            if s.is_defined_field(field):
                return True
        return False

    if config.dimension() == 2:
        def set_in_plane_field(self, field, inplane):
            self.getObject().set_in_plane(field, inplane)
            ## Activate the out-of-plane field in all subproblems only if
            ## this field is active and not in-plane.
            zfield = field.out_of_plane()
            for s in self.subproblems():
                subp = s.getObject()
                if inplane:
                    subp.deactivate_field(zfield)
                else:
                    if subp.is_active_field(field):
                        subp.activate_field(zfield)

    def precompute_all_subproblems(self):
        for s in self.subproblems():
            ## TODO: Calling solver_precompute instead of
            ## precomputeMaterials here makes output_test.py fail.
            ## Why? [This TODO is from OOF2.  I don't know if its
            ## relevant in OOF3D]
            s.precomputeMaterials()

    # def precompute_all_materials(self):
    #     materials = material.getMaterials(self.getMicrostructure())
    #     for mat in materials:
    #         mat.precompute_all_properties(self.getObject())

    def allCrossSectionNames(self):
        return self.cross_sections.all_names()

    def addCrossSection(self, name, cs):
        self.cross_sections.new(name, cs)

    def removeCrossSection(self, name):
        self.cross_sections.remove(name)

    def uniqueCSName(self, name):
        return utils.uniqueName(name, self.cross_sections.all_names())

    def selectedCS(self):
        return self.cross_sections.selected()

    def selectedCSName(self):
        return self.cross_sections.selectedName()

    def getCrossSection(self, name):
        return self.cross_sections[name]

    def selectCrossSection(self, name):
        self.cross_sections.select(name)

    def deselectCrossSection(self):
        self.cross_sections.deselect()

    def renameCrossSection(self, oldname, newname):
        actualnewname = self.cross_sections.rename(oldname, newname)
        switchboard.notify(('cross section renamed', self),
                           oldname, actualnewname)

    def replaceCrossSection(self, name, cross_section):
        self.cross_sections.replace(name, cross_section)

    # Boundary retrieval functions -- the interface needs to know
    # the names.

    def getBoundary(self, name):
        return self.getObject().boundaries[name]

    # Names of nontrivial boundaries -- does not return a complete
    # list, only returns the names of those objects with size > 0.
    # This is the meaning of the "Finite" modifier.
    def boundaryNames(self):
        names= self.getObject().getFiniteBoundaryNames()
        return names

    def pointBoundaryNames(self):
        if parallel_enable.enabled():
            # RCL: This gives the list of point boundaries, including
            # boundaries with zero size (no nodes).  Do the same for
            # edge boundaries. We do this so that all the conventional
            # boundaries (left,right,bottom,top,
            # topleft,topright,bottomleft,bottomright) show up in the
            # BoundaryCondition (sub)pages (for process 0).  No need
            # to do this for boundaryNames (just above) because it
            # doesn't seem to be used.
            return self.getObject().pointbdynames
        else:
            return self.getObject().getFinitePointBdyNames()

    def visiblePointBoundaryNames(self):
        if parallel_enable.enabled():
            names = self.getObject().pointbdynames
        else:
            names = self.getObject().getFinitePointBdyNames()

        # make copy of original list because we will alter
        # it in the loop
        names_orig = names[:]
        for name in names_orig:
            if not self.getObject().boundaries[name].visible:
                names.remove(name)

        return names

    def visiblePointBoundaryNamesSorted(self):
        names = self.visiblePointBoundaryNames()
        names.sort()
        return names

    def edgeBoundaryNames(self):
        if parallel_enable.enabled():
            return self.getObject().edgebdynames
        else:
            return self.getObject().getFiniteEdgeBdyNames()

    def edgeBoundaryNamesSorted(self):
        names = self.edgeBoundaryNames()
        names.sort()
        return names

    def periodicEdgeBoundaryNames(self):
        if parallel_enable.enabled():
            names = self.getObject().edgebdynames
        else:
            names = self.getObject().getFiniteEdgeBdyNames()

        # Periodic boundary conditions apply to two mesh boundaries
        periodic_names = []
        for i in xrange(len(names)):
            edgeInfo0 = self.getBoundary(names[i]).whichPeriodicEdge(self)
            if edgeInfo0:
                # search rest of list for the opposite boundary with
                # opposite direction
                for j in xrange(i+1,len(names)):
                    edgeInfo1 = self.getBoundary(names[j]).whichPeriodicEdge(
                        self)
                    if (edgeInfo1 and edgeInfo0[0]==edgeInfo1[0] and
                        edgeInfo0[1]!=edgeInfo1[1] and
                        edgeInfo0[2]==-edgeInfo1[2]):
                        periodic_names.append(names[i]+" "+names[j])
        return periodic_names

    def faceBoundaryNames(self):
        return self.getObject().getFiniteFaceBdyNames()
    def faceBoundaryNamesSorted(self):
        names = self.faceBoundaryNames()
        names.sort()
        return names

    # Post-construction-time changes to the boundaries can also happen.

    #Interface branch
    def newEdgeBoundary(self, name, skeleton_bdy):
        realmesh = self.getObject()
        realbdy = realmesh.newEdgeBoundary(name)
        skel = self.femesh().skeleton
        for e in skeleton_bdy.getOrientedSegments():
            if config.dimension() == 2:
                skelel = e.getLeftElement()
            else:
                ## TODO OPT: There should be a better way to determine
                ## which element to use.  If the boundary contains
                ## split nodes, which subnode should be used?
                skelel = e.get_segment().getElement(skel, 0)

            realel = realmesh.getElement(skelel.getMeshIndex())

            # edge_nodes = e.get_nodes()
            #Interface branch: Get rid of meshindex for nodes
            #realn0 = realmesh.getNode( edge_nodes[0].meshindex )
            #realn1 = realmesh.getNode( edge_nodes[1].meshindex )
            realn0 = realel.getCornerNode(
                skelel.getNodeIndexIntoList(e.getNode(0)))
            realn1 = realel.getCornerNode(
                skelel.getNodeIndexIntoList(e.getNode(1)))
            realbdy.addEdge(realel.getBndyEdge(realn0, realn1))
##        realmesh.constructRealMeshEdgeBoundaries(name, skeleton_bdy)
        switchboard.notify("mesh boundaries changed", self)

    def newFaceBoundary(self, name, skeleton_bdy):
        realmesh = self.getObject()
        realbdy = realmesh.newFaceBoundary(name)
        skel = self.femesh().skeleton
        debug.fmsg("getFaces returns", type(skeleton_bdy.getFaces()))
        for f in skeleton_bdy.getFaces(): # really OrientedFaces
            skelel = f.get_face().getElement(skel, 0)
            realel = realmesh.getElement(skelel.getMeshIndex())
            realnodes = []
            for i in (0,1,2):
                realnodes.append(realel.getCornerNode(
                    skelel.getNodeIndexIntoList(f.getNode(i))))
            realbdy.addFace(realel.getBndyFace(*realnodes))
        switchboard.notify("mesh boundaries changed", self)

    def newPointBoundary(self, name, skeleton_bdy):
        realmesh = self.getObject()
        realbndy = realmesh.newPointBoundary(name)
        skelobj=self.getSkeleton()
        for node in skeleton_bdy.nodes:
            #Interface branch: Get rid of meshindex for nodes
####            realbndy.addNode(realmesh.getNode(node.meshindex))
##            #Update: Don't create multiple mesh nodes from one skeleton node.
##            try:
##                realnodelist=realmesh._fe_splitnode[node]
##                #TODO 3.1: Pick just one realmesh node?
##                #Would this work with profiles?
##                for realnode in realnodelist:
##                    realbndy.addNode(realnode)
##            except KeyError:
##                #Node is not part of an interface
##                skelel = node.neighborElements()[0]
##                realel = realmesh.getElement(skelel.meshindex)
##                realbndy.addNode(realel.getCornerNode(skelel.getNodeIndexIntoList(node)))
            skelel = node.neighborElements()[0]
            realel = realmesh.getElement(skelel.getMeshIndex())
            realbndy.addNode(realel.getCornerNode(
                    skelel.getNodeIndexIntoList(node)))
        switchboard.notify("mesh boundaries changed", self)


    # Periodic boundary conditions use point boundaries containing
    # partnered nodes.  We only want to create the point boundaries once.
    def getPeriodicPointBoundaries(self, name):

        try:
            ppb = self.periodicPointBoundaries[name]

        except KeyError:

            boundaries = name.split()

            try:
                boundary_obj0 = self.getBoundary(boundaries[0])
            except:
                raise ooferror2.ErrSetupError(
                    "There is no boundary named '%s'!" % boundaries[0])
            try:
                boundary_obj1 = self.getBoundary(boundaries[1])
            except:
                raise ooferror2.ErrSetupError(
                    "There is no boundary named '%s'!" % boundaries[1])

            realmesh = self.getObject()
            nodes0 = boundary_obj0.edgeset.nodes()[:]
            nodes1 = boundary_obj1.edgeset.nodes()[:]
            nodes1.reverse()
            self.periodicPointBoundaries[name] = []
            for i in xrange(len(nodes0)):
                ## TODO 3.1: Can this be done without using a tolerance?
                ## Using topological information from Skeleton and
                ## MasterElement instead?
                if ((math.fabs(nodes0[i].position().x -
                               nodes1[i].position().x) < 1e-14) or
                    (math.fabs(nodes0[i].position().y
                               - nodes1[i].position().y) < 1e-14)):
                    newname = name + "_" + str(i)
                    bdy = realmesh.newPointBoundary(newname,visible=False)
                    bdy.addNode(nodes0[i])
                    bdy.addNode(nodes1[i])
                    self.periodicPointBoundaries[name].append(bdy)
                else:
                    raise ooferror2.ErrSetupError(
                        "Nodes along periodic edge boundaries do not match up")

        return self.periodicPointBoundaries[name]


    # def removeBoundary(self, name):
    #     for (bcname, bc) in self.allBoundaryConds():
    #         if bc.boundary==name:
    #             bc.remove_from_mesh()
    #             self.bdys_changed()
    #     self.getObject().removeBoundary(name)
    #     switchboard.notify("mesh boundaries changed", self)


    def renameBoundary(self, oldname, newname):
        for (bcname, bc) in self.allBoundaryConds():
            if bc.boundary==oldname:
                bc.boundary=newname
        self.getObject().renameBoundary(oldname, newname)

        # #The interface elements are notified if the skeleton boundary
        # #is renamed, but not when the skeleton boundary is deleted,
        # #because removal of a skeleton boundary is not supposed to
        # #trigger a rebuild of the mesh. Perhaps the name of the
        # #skeleton boundary that gets deleted should be removed from
        # #its 'topmost' position in the list of names in the edgement?
        ## Actually, InterfaceElements are obsolete in 3D...
        # self.getObject().renameInterfaceElements(oldname, newname)

        switchboard.notify("mesh boundaries changed", self)

    #Interface branch
    #The collection of edge (skeleton) boundary names and interface names
    #are unique.
#     def removeInterface(self, name):
#         for (bcname, bc) in self.allBoundaryConds():
#             if bc.boundary==name:
#                 bc.remove_from_mesh()
#                 self.bdys_changed()
# ##        self.getObject().removeBoundary(name)
# ##        switchboard.notify("mesh boundaries changed", self)
    def renameInterface(self, oldname, newname):
        for (bcname, bc) in self.allBoundaryConds():
            if bc.boundary==oldname:
                bc.boundary=newname
        # #Change the names attribute of the edgements
        # self.getObject().renameInterfaceElements(oldname, newname)

##        self.getObject().renameBoundary(oldname, newname)
##        switchboard.notify("mesh boundaries changed", self)

    # def replacePointBoundary(self, name, new_skel_boundary):
    #     #del self.getObject().boundaries[name]
    #     self.getObject().removePointBoundary(name)
    #     self.newPointBoundary(name, new_skel_boundary)
    #     for (bcname, bc) in self.allBoundaryConds():
    #         if bc.boundary==name:
    #             bc.boundary_obj = self.getObject().boundaries[name]
    #             bc.boundary_obj.addCondition(bc)
    #             self.bdys_changed()
    #     ## TODO 3.1: This may be the wrong place for this switchboard
    #     ## notification, since one menu item can result in more than
    #     ## one boundary replacement (eg, skeleton refinement can
    #     ## change all boundaries).  The switchboard notification
    #     ## should occur at the menu command level.
    #     switchboard.notify("mesh boundaries changed", self)

    # def replaceEdgeBoundary(self, name, new_skel_boundary):
    #     #del self.getObject().boundaries[name]
    #     self.getObject().removeEdgeBoundary(name)
    #     self.newEdgeBoundary(name, new_skel_boundary)
    #     for (bcname, bc) in self.allBoundaryConds():
    #         if bc.boundary==name:
    #             #Interface branch
    #             if not isinstance(bc,bdycondition.JumpBC):
    #                 bc.boundary_obj = self.getObject().boundaries[name]
    #                 bc.boundary_obj.addCondition(bc)
    #             self.bdys_changed()
    #     switchboard.notify("mesh boundaries changed", self)

    # def replaceFaceBoundary(self, name, new_skel_boundary):
    #     self.getObject().removeFaceBoundary(name)
    #     self.newFaceBoundary(name, new_skel_boundary)
    #     for bcname, bc, in self.allBoundaryConds():
    #         if bc.boundary == name:
    #             if not isinstance(bc, bdycondition.JumpBC):
    #                 bc.boundary_obj = self.getObject().boundaries[name]
    #                 bc.boundary_ojb.addCondition(bc)
    #             self.bdys_changed()
    #     switchboard.notify("mesh boundaries changed", self)

    # Boundary condition manipulation functions.

    def addBdyCondition(self, name, bc):
        # This is called for every node pair in a periodic BC, so it
        # shouldn't do anything too expensive.
        if name in self.bdyconditions:
            raise ooferror2.ErrSetupError(
                "Duplicate boundary condition name %s." % name )
        else:
            self.bdyconditions[name]=bc
            # The visible flag handles any cases where we want to hide
            # a BC in the GUI.
            switchboard.notify("boundary conditions changed",
                               self, name, bc.isVisible())
            self.bdys_changed()

    def checkBdyConditions(self):
        # Check boundary conditions for consistency with other
        # conditions on the same boundary.  Called by
        # SubProblemContext.checkSolvability.
        errors = []
        for bdy in self.getObject().boundaries.values():
            errs = bdy.checkConditions()
            if errs is not None:
                errors.extend(errs)
        return errors

    def uniqueBCName(self, name):
        return utils.uniqueName(name, self.bdyconditions.keys())

    def renameBdyCondition(self, oldname, newname):
        try:
            bc = self.bdyconditions[oldname]
        except KeyError:
            raise ooferror2.ErrSetupError("Can't find boundary condition %s!"
                                         % oldname)
        newname = utils.uniqueName(newname, self.allBndyCondNames(),
                                   exclude = oldname)
        if newname != oldname:
            del self.bdyconditions[oldname]
            self.bdyconditions[newname] = bc
            bc.rename(newname)
            #Interface branch
            #If oldname is an interface BC, the interface BC list
            #will be modified
            self.getObject().renameInterfaceBC(oldname,newname)

#         self.boundariesChanged.increment()
        switchboard.notify("boundary conditions changed",
                           self, newname, bc.isVisible())

    def rmBdyConditionByName(self, name):
        # remove_from_mesh calls Mesh.rmBdyCondition, above.
        self.bdyconditions[name].remove_from_mesh()

    def rmBdyCondition(self, bc): # called by BC.remove_from_mesh()
        bc.disconnect()
        visible = bc.isVisible()
        del self.bdyconditions[bc.name()]
        self.getObject().removeInterfaceBC(bc.name()) # Interface branch
        switchboard.notify("boundary conditions changed", self, bc.name(),
                           visible)
        self.bdys_changed()

    def allBoundaryConds(self):
        return self.bdyconditions.items()

    def allBndyCondNames(self):
        return self.bdyconditions.keys()

    def getBdyCondition(self, name):
        return self.bdyconditions[name]

    # Make a copy of the boundary condition, but on the indicated
    # boundary.  Caller is responsible for adding it to the mesh,
    # because that operation should remain at the menu level.
    def copyBdyCondition(self, bc, boundary):
        return self.bdyconditions[bc].copy(boundary)


    def refreshMaterials(self, skelctxt):
        # Called by Skeleton.materialsChanged() and
        # GenericMaterialGroupSet.assignMaterial() & removeMaterial().
        self.reserve()
        self.begin_writing()
        try:
            meshobj = self.getObject()
            meshobj.refreshMaterials(skelctxt.getObject())
            self.materialsChanged.increment()
            for s in self.subproblems():
                s.getObject().requirePrecompute()
        finally:
            self.end_writing()
            self.cancel_reservation()

        msgs = []
        for subprob in self.subproblems():
            if subprob.time_stepper is not None:
                badmatls = subprob.getObject().check_materials()
                if badmatls:
                    for matl in badmatls:
                        msgs.extend(matl.consistency_messages())
        if msgs:
            self.setStatus(meshstatus.Unsolvable('\n'.join(msgs)))
        else:
            self.setStatus(meshstatus.Unsolved("Materials changed."))
        switchboard.notify("mesh changed", self)

    def materialsConsistent(self):
        for subctxt in self.subproblems():
            if not subctxt.materialsConsistent():
                return False
        return True

    def changed(self, message):
        for subproblem in self.subproblems():
            subproblem.changed(message)

    # For boundary/boundary-condition changes, which require the
    # mapdofeqs and the solver to be re-run, but which do not require
    # the stiffness matrix to be rebuilt.
    def bdys_changed(self):
        self.boundariesChanged.increment()
        # This used to send the switchboard "mesh changed" signal, but
        # that's done by the menu items instead.  The call here was
        # probably redundant.  It doesn't belong here anyway -- menu
        # items should do it so that the signal is sent only once,
        # after all changes have been made.

    ##################

    # Field and BC initialization.  Assigning an initializer to a
    # Field doesn't actually initialize the Field.  That's only done
    # when initialize_fields is called.

    def set_field_initializer(self, field, initializer):
        self.initializers[field] = initializer

    def remove_initializer(self, field):
        try:
            del self.initializers[field]
        except KeyError:
            pass

    def get_initializer(self, field):
        return self.initializers.get(field, None)

    def initialize_fields(self, time):
        # The data cache must be cleared *before* setting the current
        # time or applying initializers, because when the cache is
        # cleared it first sets the mesh to the latest data in the
        # cache.
        self.clearDataCache()
        self.setCurrentTime(time)
        for field, init in self.initializers.items():
            init.apply(self.getObject(), field, time=time)
        self.fieldsInitialized.increment() # timestamp

    def update_fields(self):
        # Field definitions have changed in a subproblem.  If a field
        # isn't defined in *any* subproblems, remove its initializer.
        definedfields = self.all_subproblem_fields()
        for field, initializer in self.initializers.items():
            if field not in definedfields:
                self.remove_initializer(field)

    def set_bc_initializer(self, bc, how):
        self.getBdyCondition(bc).set_initializer(how)

    def remove_bc_initializer(self, bc):
        self.getBdyCondition(bc).remove_initializer()

    def remove_all_bc_initializers(self):
        for (bcname, bc) in self.allBoundaryConds():
            bc.remove_initializer()

    def get_bc_initializer(self, bc):
        return self.getBdyCondition(bc).get_initializer()

    def initialize_bcs(self, time):
        for (bcname, bc) in self.allBoundaryConds():
            bc.preinitialize()
        intersections = self.getObject().intersectingFloatBCs(time)

        for (bcname, bc) in self.allBoundaryConds():
            bc.initialize(time, intersections)

    def initialized_bcs(self):
        for (bcname, bc) in self.allBoundaryConds():
            if bc.get_initializer():
                yield bc

    def n_initialized_bcs(self):
        return len(list(self.initialized_bcs()))

    ##############

    def enclosingElement(self, point):
        return self.getObject().enclosingElement(self.getSkeleton(), point)

    def compare(self, other, tolerance):
        tol2 = tolerance*tolerance
        mymesh = self.getObject()
        othermesh = other.getObject()

        # compare node positions
        for mynode, othernode in map(None, mymesh.nodes(), othermesh.nodes()):
            if mynode is None or othernode is None:
                return "Wrong number of nodes"
            if (mynode.position() - othernode.position())**2 > tol2:
                return ("Node outside of tolerance, %s" %
                        mynode.position() - othernode.position())
                
        # compare subproblems
        mysubprobs = self.subproblems()
        othersubprobs = other.subproblems()
        if len(mysubprobs) != len(othersubprobs):
            return "Wrong number of subproblems"
        # subproblem order may be different.  Check names before
        # comparing subproblems.
        subpnames = [s.name() for s in mysubprobs]
        osubpnames = [s.name() for s in othersubprobs]
        subpnames.sort()
        osubpnames.sort()
        if subpnames != osubpnames:
            return "Subproblem names don't match: %s!=%s" % (subpnames,
                                                             osubpnames)

        curtime = self.getCurrentTime()
        othertime = other.getCurrentTime()
        latest = self.atLatest()
        if curtime != othertime:
            return "Current times differ"

        times = set(self.cachedTimes())
        times.add(curtime)
        othertimes = set(other.cachedTimes())
        othertimes.add(othertime)
        if times != othertimes:
            print >> sys.stderr, "times=", times
            print >> sys.stderr, "othertimes=", othertimes
            return "Cached times differ"


        # Since this routine is only run by the test suite, it's safe
        # to disable locks here.  If we don't disable them,
        # restoreCachedData won't run because it's on the main thread
        # in the test suite.
        locked = lock.disableLocks()
        try:
            for time in times:
                self.restoreCachedData(time)
                other.restoreCachedData(time)
                try:
                    for subpname in subpnames:
                        # Many of these checks don't actually have to
                        # be done at each timestep, but it's simpler
                        # to just do them always.  They're not that
                        # slow.
                        subpctxt = self.get_subproblem(subpname)
                        osubpctxt = other.get_subproblem(subpname)
                        subp = subpctxt.getObject()
                        osubp = osubpctxt.getObject()
                        # Check that the same Fields are defined on
                        # the subproblems
                        fields = subpctxt.all_compound_fields()
                        ofields = osubpctxt.all_compound_fields()
                        fields.sort()
                        ofields.sort()
                        if fields != ofields:
                            return ("Fields don't match in subproblem "
                                + subpname)

                        # Check that the subproblems have the same
                        # sets of nodes. 
                        mynodes = list(subp.funcnodes())
                        othernodes = list(osubp.funcnodes())
                        if len(mynodes) != len(othernodes):
                            return (
                                "Different numbers of nodes in subproblem %s"
                                % subpname)
                        # Create a sorted list of nodes, because
                        # funcnodes() doesn't return them in a
                        # guaranteed order. (Really? Why?)
                        mynodes.sort(_nodesorter)
                        othernodes.sort(_nodesorter)

                        for field in fields:
                            # Check field state
                            if (subp.is_active_field(field)
                                != osubp.is_active_field(field)):
                                return ("Field activity differs for %s"
                                        " on subproblem %s" % 
                                        (`field`, subpname))
                            if config.dimension() == 2:
                                if (mymesh.in_plane(field)
                                    != othermesh.in_plane(field)):
                                    return (
                                        "Field planarity differs for %s on"
                                        " subproblem %s" % (`field`, subpname))
                                oop = (not mymesh.in_plane(field) and
                                       field.out_of_plane())

                            # Check that the field values agree at the
                            # nodes.  This is the only part of the
                            # loop over times that really has to be
                            # done on each pass.  It's not sufficient
                            # to simply compare the FEMeshes'
                            # dofvalues arrays, because the nodes may
                            # not be in the same order in the two
                            # meshes.
                            for mynode, othernode in zip(mynodes, othernodes):
                                if mynode.position() != othernode.position():
                                    return ("Bad node positions for"
                                            " subproblem %s: %s!=%s"
                                            % (subpname, mynode.position(),
                                               othernode.position()))
                                if _fielddiff(field, mymesh, mynode,
                                              othermesh, othernode) > tol2:
                                    debug.fmsg(mynode,
                                               [field.value(mymesh, mynode, i)
                                                for i in range(field.ndof())],
                                               othernode,
                                               [field.value(othermesh,
                                                            othernode, i)
                                                for i in range(field.ndof())])
                                    return ("%s values differ for"
                                            " subproblem %s" %
                                            (`field`, subpname))
                                if config.dimension() == 2:
                                    if (oop and (_fielddiff(oop, mymesh, mynode,
                                                           othermesh, othernode)
                                                 > tol2)):
                                        return ("Out-of-plane %s values"
                                                " differ for subproblem %s",
                                                (`field`, subpname))
                            # end loop over mynodes, othernodes
                        # end loop over fields
                    # end loop over subpnames
                finally:
                    self.releaseCachedData()
                    other.releaseCachedData()
        finally:
            if latest:
                self.restoreLatestData()
                self.releaseLatestData()
                other.restoreLatestData()
                other.releaseLatestData()
            else:
                self.restoreCachedData(curtime)
                self.releaseCachedData()
                other.restoreCachedData(curtime)
                other.releaseCachedData()
            if locked:
                lock.enableLocks()
        return 0                        # Success

    def solver_precompute(self, solving=False):
        # Called before time-stepping.  This routine precomputes
        # things that can't possibly be time-dependent.
        for subproblem in self.subproblems():
            subproblem.solver_precompute(solving)

    def solver_postcompute(self):
        for subproblem in self.subproblems():
            subproblem.solver_postcompute()

    ##########################

    # Data cache stuff.  The data cache stores values of the fields at
    # previous time steps.

    def setDataCache(self, cache):
        # Keep a reference to the cache object here so that it will
        # last as long as the femesh.  It was created in Python, in
        # meshdatacache.spy.
        self.datacache = cache
        self.getObject().setDataCache(cache)

    def getDataCacheType(self):
        return meshdatacache.getMeshDataCacheType(self.datacache)

    def replaceDataCache(self, cache):
        self.getObject().replaceDataCache(cache)
        self.datacache = cache

    def clearDataCache(self):
        self.getObject().clearDataCache();

    def cacheCurrentData(self):
        self.getObject().cacheCurrentData();

    def restoreCachedData(self, time):
        self.getObject().restoreCachedData(time)

    def restoreLatestData(self):
        self.getObject().restoreLatestData()

    def releaseCachedData(self):
        self.getObject().releaseCachedData()

    def releaseLatestData(self):
        self.releaseCachedData()

    def cachedTimes(self):
        return self.getObject().cachedTimes()
        # return self.datacache.times()
    def getCurrentTime(self):
        return self.getObject().getCurrentTime()
    def setCurrentTime(self, time, delta=None):
        self.getObject().setCurrentTime(time)
        if delta is not None:
            self.solverDelta = delta
        switchboard.notify("time changed", self) # caught by SolverPage
    def getTime(self, time):
        # Just a utility function to resolve the 'latest' placeholder.
        if time == placeholder.latest:
            return self.getObject().latestTime()
        if time == placeholder.earliest:
            return self.getObject().earliestTime()
        return time
    def cachedTime(self, time):
        # Is the given time explicitly contained in the cache?
        return (time is placeholder.latest or
                time is placeholder.earliest or
                time in self.cachedTimes())
    def boundedTime(self, time):
        # Is the given time in the range of times spanned by the cache?
        themesh = self.getObject()
        return (
            time is placeholder.latest or
            time is placeholder.earliest or
            themesh.earliestTime() <= time <= themesh.latestime()
            )
    def atLatest(self):
        return self.getObject().atLatest()
    def atEarliest(self):
        return self.getObject().atEarliest()
    def isEmptyCache(self):
        return self.getObject().empty()
    def dataCacheSize(self):
        return self.getObject().dataCacheSize()

    ########################

    def setStatus(self, statusobj, resync=False):
        # If the Mesh is out of sync with the Skeleton, it has to be
        # rebuilt before anything else can be done with it.
        # Mesh.rebuildMesh calls this function with resync=True after
        # rebuilding the Mesh.
        if self.outOfSync() and not resync:
            return
        self.status = statusobj # a MeshStatus object
        errors = filter(None, [subproblem.checkSolvability()
                               for subproblem in self.subproblems()
                               if  subproblem.time_stepper is not None])
        if errors:
            self.status = meshstatus.Unsolvable('\n'.join(errors))
        switchboard.notify("mesh status changed", self)

    def outOfSync(self):
        return isinstance(self.status, meshstatus.OutOfSync)

    def skeletonChanged(self, skel):
        self.setStatus(meshstatus.OutOfSync())

    def interfacesChanged(self):
        self.setStatus(meshstatus.OutOfSync())

    def timeDependent(self):
        for subproblem in self.subproblems():
            if subproblem.timeDependent():
                return True
        return False

    def timeDependentBCs(self):
        for bc in self.bdyconditions.values():
            if bc.isTimeDependent():
                return True
        return False

    def dumpDoFs(self, filename):
        self.getObject().dumpDoFs(filename)

#################

# Utility functions used by Mesh.compare
def _fielddiff(field, meshA, nodeA, meshB, nodeB):
    fieldA = field.output(meshA, nodeA).valueClone().value_list()
    fieldB = field.output(meshB, nodeB).valueClone().value_list()
    diffs = [x-y for x,y in zip(fieldA, fieldB)]
    sqdiffs = reduce(lambda x,y: x+y*y, diffs, 0.0)/len(diffs)
    return sqdiffs
def _nodesorter(nodeA, nodeB):
    return cmp(nodeA.position(), nodeB.position())

##################
defaultSubProblemName = "default"

from ooflib.engine.skeletoncontext import skeletonContexts

meshes = whoville.WhoClass(
    'Mesh',
    ordering=300,
    parentClass=skeletonContexts,
    instanceClass=Mesh,
    proxyClasses=['<topmost>','<contourable>'])

utils.OOFdefine('meshes', meshes)

#################

class SyncMeshParameter(whoville.WhoParameter):
    def __init__(self, name, value=None, default=None, tip=None):
        whoville.WhoParameter.__init__(self, name, meshes, value, default, tip)
