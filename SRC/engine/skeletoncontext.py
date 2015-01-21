# -*- python -*-
# $RCSfile: skeletoncontext.py,v $
# $Revision: 1.146.2.64 $
# $Author: langer $
# $Date: 2014/12/02 21:52:40 $

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
from ooflib.SWIG.common import timestamp
from ooflib.SWIG.engine import cskeletonselectable
from ooflib.common import debug
from ooflib.common import labeltree
from ooflib.common import microstructure
from ooflib.common import parallel_enable
from ooflib.common import runtimeflags
from ooflib.common import utils
from ooflib.common.IO import placeholder
from ooflib.common.IO import reporter
from ooflib.common.IO import whoville
from ooflib.engine import materialmanager
from ooflib.engine import skeletonboundary
from ooflib.engine import skeletongroups
from ooflib.engine import skeletonnode # this still contains the pinned nodes
from ooflib.engine import skeletonselectable
from ooflib.engine.IO import movenode
import string
import sys

# When propagating boundaries, Deputies shouldn't be around - since they
# don't have nothing to do with boundaries!
# Takes a list of skeletons and removes Deputies.
def withoutDeputies(skels):
    # return [skel for skel in skels if not skel.isDeputy()]
    from ooflib.SWIG.engine import cskeleton2
    return [skel for skel in skels if isinstance(skel, cskeleton2.CSkeletonPtr)]

class SkeletonContext(whoville.WhoDoUndo):
    def __init__(self, name, classname, skel, parent):
        # All of the args have to be given, although not all are used.
        # This is because the constructor is called by WhoClass.add,
        # which assumes that the arguments are the same as those of
        # Who.__init__.  Probably a better solution using
        # RegisteredClasses could be found.

        # Keep track of node/segment/element index data (in that
        # order), so selectables can be uniquely identified within
        # this context, independently of which skeleton they're in.
        # This used to be done in the individual selectable classes,
        # but for repeatability reasons, it's desirable to restart the
        # indices in each context, ensuring that skeleton copies
        # really are absolutely identical in every respect.
        #self.next_indices = (0, 0, 0)

        if config.dimension() == 3:
            self.faceboundaries = utils.OrderedDict() 
        self.edgeboundaries = utils.OrderedDict() 
        self.pointboundaries = utils.OrderedDict()
        self.selectedBdyName = None
        # There are two boundary timestamps, one for keeping track of
        # changes in the currently selected boundary, and another for
        # keeping track of changes to the configuration of boundaries
        # in any of these skeletons.  They are queried by their
        # respective displays in skeletonbdydisplay.py.
        ## TODO 3.1: The second of these timestamps (bdytimestamp) is
        ## obsolete and has been removed.  Is the first also obsolete?
        self.bdyselected = timestamp.TimeStamp()

        # Various selection objects live here.  Instance the
        # selections from their constructors.  To get the current
        # selection, do "context.elementselection.retrieve()".
        self.nodeselection = skeletonselectable.NodeSelection(self)
        self.segmentselection = skeletonselectable.SegmentSelection(self)
        if config.dimension() == 3:
            self.faceselection = skeletonselectable.FaceSelection(self)
        self.elementselection = skeletonselectable.ElementSelection(self)
        self.pinnednodes = skeletonnode.PinnedNodeSelection(self)

        # These attribute names (nodegroups, segmentgroups,
        # elementgroups) are used in the generic menu callback in
        # IO/skeletongroupmenu.py.  Also in skeletonselectionmod.py.
        # Change them in all places (or none, of course.)
        self.nodegroups = skeletongroups.NodeGroupSet(self)
        self.segmentgroups = skeletongroups.SegmentGroupSet(self)
        self.facegroups = skeletongroups.FaceGroupSet(self)
        self.elementgroups = skeletongroups.ElementGroupSet(self)
        
        # WhoDoUndo.__init__ calls pushModification, so timing is
        # important.  pushModification calls implied_select for all
        # the selections, so the selection objects have to exist at
        # this point.
        whoville.WhoDoUndo.__init__(self, name, 'Skeleton', skel, parent,
                                    overwritefn=self.skeletonStackOverwrite)

        # # Overwrite function, gets called when an item in the stack is
        # # about to be overwritten. 
        # self.undobuffer.overwrite = self.skeletonStackOverwrite

        # When a skeleton with deputies is overwritten, a reference to
        # it must be kept as long any deputies exist.
        self.zombieSheriff = None

        # Ensure that the passed-in obj really does start a new "family."
        ## TODO OPT: Restore this, or delete this block if it's
        ## unnecessary.  In 2D, skel.disconnect() calls
        ## SkeletonSelectable.disconnect() for all selectables, which
        ## severs their parent/child relationships.  This is probably
        ## only necessary when copying a SkeletonContext.
        #skel.disconnect()

        # Ask the initial skel about any pre-existing boundaries.
        fbs = skel.getFaceBoundaries()
        for (name, bdy) in fbs.items():
            self.faceboundaries[name] = \
                bdy.makeContextBoundary(self, name, skel)
        
        ebs = skel.getEdgeBoundaries()
        for (name, bdy) in ebs.items():
            self.edgeboundaries[name] = \
                bdy.makeContextBoundary(self, name, skel)

        pbs = skel.getPointBoundaries()
        for name in pbs:
            self.pointboundaries[name] = \
              pbs[name].makeContextBoundary(self, name, skel)

        self.requestCallback("destroy pixel group", self.ms_grp_changed)
        self.requestCallback("changed pixel group", self.ms_grp_changed)
        self.requestCallback("changed pixel groups", self.ms_grps_changed)
        self.requestCallback('materials changed in microstructure',
                             self.materialsChanged)

    # Switchboard callback for "changed pixel group" or "destroy pixel
    # group".
    def ms_grp_changed(self, group, ms_name):
        skelobj=self.getObject()
        if skelobj and ms_name == skelobj.getMicrostructure().name():
            switchboard.notify("Skeleton changed", self.path())

    # Switchboard callback for "changed pixel groups", indicating that
    # multiple pixel groups have changed but "changed pixel group" has
    # *not* been sent for them, so that setHomogeneityIndex() won't be
    # called too often.
    def ms_grps_changed(self, ms_name):
        skelobj=self.getObject()
        if skelobj and ms_name == skelobj.getMicrostructure().name():
            switchboard.notify("Skeleton changed", self.path())

    def materialsChanged(self, ms): # switchboard "materials changed ..."
        if ms is self.parent.getObject():
            switchboard.notify("Skeleton changed", self.path())
            for mesh in self.getMeshes():
                mesh.refreshMaterials(self)

    # Comparison routine -- checks that the two skeletons have the
    # same element, segment, and node groups and group members, and
    # the same pinned nodes.  This function is in this context because
    # the skeletoncontext object is the one that knows about group
    # membership.  Returns 0 if comparison is successful, otherwise
    # returns a string explaining what happened.  Used only in the
    # regression test suite.
    def compare_groups(self, other):
        if self.elementgroups.allGroups() != other.elementgroups.allGroups():
            return "Element group names mismatch: %s != %s" % (
                self.elementgroups.allGroups(), other.elementgroups.allGroups())
        for g in self.elementgroups.allGroups():
            if [x.index for x in self.elementgroups.get_group(g)] != \
               [x.index for x in other.elementgroups.get_group(g)]:
                return "Element group membership mismatch."
        if (self.elementgroups.getAllMaterials() != 
            other.elementgroups.getAllMaterials()):
            return "Mismatch in Element group materials."
            
        if self.segmentgroups.allGroups() != other.segmentgroups.allGroups():
            return "Segment group names mismatch."
        for g in self.segmentgroups.allGroups():
            if [x.index for x in self.segmentgroups.get_group(g)] != \
               [x.index for x in other.segmentgroups.get_group(g)]:
                return "Segment group membership mismatch."

        if self.nodegroups.allGroups() != other.nodegroups.allGroups():
            return "Node group names mismatch."
        for g in self.nodegroups.allGroups():
            if [x.index for x in self.nodegroups.get_group(g)] != \
               [x.index for x in other.nodegroups.get_group(g)]:
                return "Node group membership mismatch."

        if self.pinnednodes.npinned() != other.pinnednodes.npinned():
            return "Pinned-node count mismatch."

        if [x.index for x in self.pinnednodes.retrieve()] != \
           [x.index for x in other.pinnednodes.retrieve()]:
            return "Pinned nodes mismatch."

        return 0


    def lockAndDelete(self):
        self.reserve()
        for mesh in self.getMeshes()[:]:
            mesh.lockAndDelete()
        try:
            self.begin_writing()
            try:
                skeletonContexts.remove(self.path())
            finally:
                self.end_writing()
        finally:
            ## Cancelling the reservation here is unnecessary and can
            ## cause problems if debug code is added to the deletion
            ## process.
            # self.cancel_reservation()
            pass
    
    def remove(self):
        ## TODO 3.1: 2D code was modified to call WhoDoUndo.remove() at
        ## the beginning of this method instead of at the end.  Should
        ## that be done here?  It seems wrong.  The cvs message for
        ## that change (1.150) says that it appeared to eliminate race
        ## conditions that caused a gui test failure on an Ubuntu VM
        ## on the Mac, but nowhere else.
        self.nodeselection.destroy()
        self.segmentselection.destroy()
        self.elementselection.destroy()
        self.nodegroups.destroy()
        self.segmentgroups.destroy()
        self.elementgroups.destroy()
        if config.dimension() == 3:
            self.faceselection.destroy()
            self.facegroups.destroy()
        self.pinnednodes.destroy()
        # WhoDoUndo.remove destroys all the objects in the undobuffer.
        whoville.WhoDoUndo.remove(self)
        self.zombieSheriff = None

    def pushModification(self, skeleton):
        skeleton = self.resolveCSkeleton(skeleton)
        old = self.getObject()
        skeleton.activate()
        # Call the parent pushModification without emitting the "who
        # changed" switchboard signal.  "whodoundo push" *is* emitted,
        # though.
        whoville.WhoDoUndo.pushModification(self, skeleton, signal=False)

        ## TODO 3.1: The "whodoundo push" signal invokes
        ## SelectionBase.whoChanged0, which calls implied_select on
        ## all of the SelectionBase subclasses.  Is there a reason to
        ## do that via the switchboard?  Shouldn't this function just
        ## call implied_select directly?

        # Propagate the boundaries.  This must be done before the
        # boundaries are drawn, which is why the "who changed" signal
        # was suppressed.
        for f in self.faceboundaries.values():
            skeleton.mapBoundary(f, old) # Default direction is child-ward.
        for e in self.edgeboundaries.values():
            skeleton.mapBoundary(e, old) # Default direction is child-ward.
        for p in self.pointboundaries.values():
            skeleton.mapBoundary(p, old) # Default direction is child-ward.
            
        # This call's activity used to be done by the "'who changed',
        # 'Skeleton'" switchboard signal, but this signal was getting
        # into a race condition with callbacks for "new who", leading
        # to inconsistent checkpointing.  We can do the direct call
        # here, because there's no GUI activity involved.  It's
        # encapsulated in a function, because skeletonIO needs to do
        # it also.
        self.pause_writing()
        try:
            self.updateGroupsAndSelections()
        finally:
            self.resume_writing()
       
        # Now emit the "who changed" signal.
        self.pushModificationSignal()
        # Boundaries may have changed, too.
        switchboard.notify("new boundary configuration", self)

        self.unSyncMeshes()

    def resolveCSkeleton(self, cskel):
        # The wrapped CSkeletonBase* object returned from C++ by swig
        # is a different Python object each time it's returned.  This
        # makes it impossible to use as a key in a WeakKeyDictionary.
        # The SkeletonContext's undobuffer, however, already contains
        # a wrapped CSkeletonBase* object that refers to the same
        # CSkeletonBase.  This function finds that object and returns
        # it.  It's safe to use it as a weak key because it will
        # persist until the CSkeleton is destroyed.
        uid = cskel.getUid()
        for skel in self.undobuffer:
            if skel.getUid() == uid:
                return skel
        # The CSkeleton isn't in the undobuffer.  That means that this
        # is the first time that it's been returned to Python, and
        # we're about to put it in the buffer.  It also means that
        # Python needs to take ownership of it, so that it will be
        # destroyed properly when the undobuffer is cleared.
        cskel.thisown = 1
        return cskel

    def unSyncMeshes(self):
        # Tell all Meshes that they're out of sync with the Skeleton.
        for meshctxt in self.getMeshes():
            meshctxt.skeletonChanged(self.getObject())

    def updateGroupsAndSelections(self):
        switchboard.notify("groupset changed", self, None)
        self.nodeselection.newSkeleton(self)
        self.segmentselection.newSkeleton(self)
        self.elementselection.newSkeleton(self)
        self.pinnednodes.newSkeleton(self)
        if config.dimension() == 3:
            self.faceselection.newSkeleton(self)
    
    def undoModification(self):
        whoville.WhoDoUndo.undoModification(self)
        ## TODO 3.1: Can unSyncMeshes be called from undoHookFn? Then
        ## undoModification wouldn't need to be overridden here.  Same
        ## for redoModification, below.
        self.unSyncMeshes()
        
    def redoModification(self):
        whoville.WhoDoUndo.redoModification(self)
        self.unSyncMeshes()

    # Extra operations during WhoDoUndo undo and redo.  If either the
    # old object or the new one is a DeputySkeleton, the positions of
    # the nodes must be updated.  Also, the number of edges/nodes in
    # the current boundary can be changed.
    
    def undoHookFn(self, oldskel, newskel):
        newskel.activate()
        self.pause_writing()
        try:
            self.updateGroupsAndSelections()
        finally:
            self.resume_writing()

    def redoHookFn(self, oldskel, newskel):
        newskel.activate()
        self.pause_writing()
        try:
            self.updateGroupsAndSelections()
        finally:
            self.resume_writing()

    def skeletonStackOverwrite(self, skeleton):
        # This function is passed a reference to a CSkeleton or
        # CDeputySkeleton that is about to be overwritten in the
        # stack.
        if skeleton.nDeputies() > 0:
            # Prevent the destruction of a skeleton that is still
            # being used in the Trackers' weak key dictionary.
            self.zombieSheriff = skeleton
        skeleton.destroy()

        
    # ## ### #### ##### ###### ####### ####### ###### ##### #### ### ## #

    # Simple utilities used when operating on groups and selections.
    # These return a list of the actual objects in the group or
    # selection.
    ## TODO OPT: All functions that use them probably should be using
    ## couriers and not dealing with python lists of swigged objects.

    def nodes_from_node_aggregate(self, group):
        if group == placeholder.selection:
            return self.nodeselection.retrieve()
        return self.nodegroups.get_group(group)

    def segments_from_seg_aggregate(self, group):
      if group == placeholder.selection:
          return self.segmentselection.retrieve()
      return self.segmentgroups.get_group(group)

    def faces_from_face_aggregate(self, group):
        if group == placeholder.selection:
            return self.faceselection.retrieve()
        return self.facegroups.get_group(group)

    def elements_from_el_aggregate(self, group):
        if group == placeholder.selection:
            return self.elementselection.retrieve()
        return self.elementgroups.get_group(group)

    # ## ### #### ##### ###### ####### ####### ###### ##### #### ### ## #

    # Functions to extract the boundaries of sets of skeleton objects.

    ## TODO MER: Write the 2D equivalents of these methods and use them in
    ## boundarybuilder.py and skeletonselectionmod.py.

    # Get the faces on the exterior of a set of elements.
    def exteriorFacesOfElementSet(self, elements):
        # A face is on the exterior of a set of elements if it belongs to
        # only one of the elements in the set.
        skel = self.getObject()
        facecounts = {}
        for element in elements:
            for face in skel.getElementFaces(element):
                facecounts[face] = facecounts.get(face, 0) + 1
        bdyfaces = set(face for face, count in facecounts.items() if count==1)
        return bdyfaces
    
    def exteriorFacesOfSelectedElements(self):
        return self.exteriorFacesOfElementSet(self.elementselection.retrieve())

    def exteriorSegmentsOfElementSet(self, elements):
        # A segment is on the exterior of a set of elements if it's on
        # an exterior face of the set.
        faces = self.exteriorFacesOfElementSet(elements)
        skel = self.getObject()
        segs = set()
        for face in faces:
            segs.update(skel.getFaceSegments(face))
        return segs

    def exteriorSegmentsOfSelectedElements(self):
        return self.exteriorSegmentsOfElementSet(
            self.elementselection.retrieve())

    # Get the nodes on the exterior of a given set of elements.
    def exteriorNodesOfElementSet(self, elements):
        nodes = set()
        # A node is on the exterior of the element set if it's on a
        # exterior face of the element set. 
        bdyfaces = self.exteriorFacesOfElementSet(elements)
        for face in bdyfaces:
            nodes.update(face.getNodes())
        return nodes

    def exteriorSegmentsOfFaceSet(self, faces):
        # A segment is on the exterior of the face set if only one of
        # the segment's faces is in the set.
        skel = self.getObject()
        segcounts = utils.OrderedDict()
        for face in faces:
            for seg in skel.getFaceSegments(face):
                segcounts[seg] = segcounts.get(seg, 0) + 1
        return utils.OrderedSet(seg for seg,count in segcounts.items()
                                if count == 1)

    def exteriorSegmentsOfSelectedFaces(self):
        return self.exteriorSegmentsOfFaceSet(self.faceselection.retrieve())
        
    # Like the above, but for all objects, not just the boundaries, of
    # the given set.

    def allFacesOfElementSet(self, elements):
        faces = set()
        skel = self.getObject()
        for element in elements:
            faces.update(skel.getElementFaces(element))
        return faces

    def allNodesOfElementSet(self, elements):
        nodes = set()
        for element in elements:
            nodes.update(element.getNodes())
        return nodes

    # ## ### #### ##### ###### ####### ####### ###### ##### #### ### ## #

    # Boundary functions -- create, destroy, eventually edit.
    # To create a boundary, create it in the current skeleton, then
    # propagate it upward and downward.  Likewise to destroy.
    def createFaceBoundary(self, name, orientedsurface, 
                           exterior=False, autoselect=1):
        bdy = self.getObject().makeFaceBoundary(name, orientedsurface, exterior)

        # makeContextBoundary returns a SkelContextFaceBoundary, or
        # equivalent, depending on what type of boundary bdy is.
        context_bdy = bdy.makeContextBoundary(self, name, self.getObject())
        self.faceboundaries[name] = context_bdy

        #Interface branch
        #TODO 3.1: Add skeleton boundary to list of interfaces somehow
        #interfacemsplugin=self.getMicrostructure().getPlugIn("Interfaces")
        
        # Propagation up and down.
        # Unfortunate nomenclature -- in the context, mapping "down"
        # is towards the children, which is the direction of
        # increasing index in the undobuffer, and is therefore towards
        # the top.
        sheriff = self.resolveCSkeleton(self.getObject().sheriffSkeleton())
        current = sheriff
        children = self.undobuffer.getToTop(start=sheriff)
        for c in withoutDeputies(children[1:]):
            c.mapBoundary(context_bdy, current,
                          direction=cskeletonselectable.MAP_DOWN)
            current = c

        current = sheriff
        parents = self.undobuffer.getToBottom(start=sheriff)
        for p in withoutDeputies(parents[1:]):
            p.mapBoundary(context_bdy, current,
                          direction=cskeletonselectable.MAP_UP)
            current = p

        switchboard.notify("new boundary created", self)
        if autoselect:
            self.selectBoundary(name)
        # self.bdytimestamp.increment()
        switchboard.notify("new boundary configuration", self)

    def createEdgeBoundary(self, name, segment_set, startnode,
                           exterior=False, autoselect=1):
        ## TODO 3.1: exterior and autoselect are never passed explicitly.
        ## Why are they args?
        bdy = self.getObject().makeEdgeBoundary(
            name, segment_set, startnode, exterior)
        self._createEdgeBoundary(name, bdy, autoselect)

    def createEdgeBoundary3D(self, name, segmentsequence,
                             exterior=False, autoselect=1):
        # Called only by boundarybuilder functions.
        ## TODO 3.1: exterior and autoselect are never passed explicitly.
        ## Why are they args?
        bdy = self.getObject().makeEdgeBoundary3D(
            name, segmentsequence, exterior)
        self._createEdgeBoundary(name, bdy, autoselect)

    def _createEdgeBoundary(self, name, bdy, autoselect):
        # Utility function for createEdgeBoundary and
        # createEdgeBoundary3D.  After merging 2D and 3D code, this
        # can be incorporated into createEdgeBoundary again.

        context_bdy = bdy.makeContextBoundary(self, name, self.getObject())
        self.edgeboundaries[name] = context_bdy

        #Interface branch
        #TODO 3.1: Add skeleton boundary to list of interfaces somehow
        #interfacemsplugin=self.getMicrostructure().getPlugIn("Interfaces")
        
        # Propagation up and down.
        # Unfortunate nomenclature -- in the context, mapping "down"
        # is towards the children, which is the direction of
        # increasing index in the undobuffer, and is therefore towards
        # the top.
        sheriff = self.resolveCSkeleton(self.getObject().sheriffSkeleton())
        current = sheriff
        children = self.undobuffer.getToTop(start=sheriff)
        for c in withoutDeputies(children[1:]):
            c.mapBoundary(context_bdy, current,
                          direction=cskeletonselectable.MAP_DOWN)
            current = c

        current = sheriff
        parents = self.undobuffer.getToBottom(start=sheriff)
        for p in withoutDeputies(parents[1:]):
            p.mapBoundary(context_bdy, current,
                          direction=cskeletonselectable.MAP_UP)
            current = p

        switchboard.notify("new boundary created", self)
        if autoselect:
            self.selectBoundary(name)
        # self.bdytimestamp.increment()
        switchboard.notify("new boundary configuration", self)
        
    #Interface branch
    def createNonsequenceableEdgeBoundary(self, name, segment_set,
                                          direction_set,
                                          exterior=False, autoselect=1):
        ## TODO 3.1: makeNonsequenceableEdgeBoundary is not yet written for 3D
        bdy = self.getObject().makeNonsequenceableEdgeBoundary(name,
                                                               segment_set,
                                                               direction_set,
                                                               exterior)
        for mesh in self.getMeshes():
            mesh.newEdgeBoundary(name, bdy)

        context_bdy = bdy.makeContextBoundary(self, name, self.getObject())
        self.edgeboundaries[name] = context_bdy
        
        # Propagation up and down.
        # Unfortunate nomenclature -- in the context, mapping "down"
        # is towards the children, which is the direction of
        # increasing index in the undobuffer, and is therefore towards
        # the top.
        current = self.getObject()
        children = self.undobuffer.getToTop()
        for c in withoutDeputies(children[1:]):
            c.mapBoundary(context_bdy, current,
                          direction=cskeletonselectable.MAP_DOWN)
            current = c

        current = self.getObject()
        parents = self.undobuffer.getToBottom()
        for p in withoutDeputies(parents[1:]):
            p.mapBoundary(context_bdy, current,
                          direction=cskeletonselectable.MAP_UP)
            current = p

        switchboard.notify("new boundary created", self)
        if autoselect:
            self.selectBoundary(name)
        # self.bdytimestamp.increment()
        switchboard.notify("new boundary configuration", self)

    def createPointBoundary(self, name, node_set,
                            exterior=False, autoselect=1):

        # TODO OPT: get rid of call to list, needs typemap for sets
        bdy = self.getObject().makePointBoundary(name, list(node_set), exterior)

        context_bdy = bdy.makeContextBoundary(self, name, self.getObject())
        self.pointboundaries[name] = context_bdy
        
        # Propagation up and down.
        # See routine above for nomenclature lament.
        # DeputySkeleton.mapBoundary is a no-op.
        sheriff = self.resolveCSkeleton(self.getObject().sheriffSkeleton())
        current = sheriff
        children = self.undobuffer.getToTop(start=sheriff)
        for c in withoutDeputies(children[1:]):
            c.mapBoundary(context_bdy, current,
                          direction=cskeletonselectable.MAP_DOWN)
            current = c

        current = sheriff
        parents = self.undobuffer.getToBottom(start=sheriff)
        for p in withoutDeputies(parents[1:]):
            p.mapBoundary(context_bdy, current,
                          direction=cskeletonselectable.MAP_UP)
            current = p

        switchboard.notify("new boundary created", self)
        if autoselect:
            self.selectBoundary(name)
        # self.bdytimestamp.increment()
        switchboard.notify("new boundary configuration", self)

    # The edgeboundaries[name] or pointboundaries[name] objects here
    # are SkelContextBoundary objects -- their "remove" methods remove
    # the corresponding Skeleton[Point|Edge|Face]Boundary objects from
    # the skeletons.
    def removeBoundary(self, name):
        # Actual removal from skeletons happens in
        # SkelContextBoundary.remove().

        self.unSyncMeshes()
        # for mesh in self.getMeshes():
        #     mesh.removeBoundary(name)

        ## TODO 3.1: Use virtual methods in the boundary classes instead
        ## of this ugly if/elif.  There should be just one dict for
        ## the name lookup.
        if name in self.faceboundaries:
            self.faceboundaries[name].remove()
            del self.faceboundaries[name]
        elif name in self.edgeboundaries:
            self.edgeboundaries[name].remove()
            del self.edgeboundaries[name]
        elif name in self.pointboundaries:
            self.pointboundaries[name].remove()
            del self.pointboundaries[name]
        else:
            raise ooferror.ErrUserError(
                "Cannot remove boundary %s, no such boundary." % name)
        if name == self.selectedBdyName:
            self.unselectBoundary()
        # self.bdytimestamp.increment()
        switchboard.notify("boundary removed", self)
        switchboard.notify("new boundary configuration", self)

    def renameBoundary(self, oldname, newname):
        if oldname==newname:
            return

        if newname in self.allBoundaryNames():
            raise ooferror.ErrSetupError("Name %s already in use." % newname)

        if config.dimension() == 2 and runtimeflags.surface_mode:
            if newname in self.allInterfaceNames():
                raise ooferror.ErrSetupError(
                    "Name %s is already in use as an interface name." % newname)

        ## TODO 3.1: Use virtual methods in the boundary classes instead
        ## of this ugly if/elif.  There should be just one dict for
        ## the name lookup.
        if oldname in self.faceboundaries:
            bdydict = self.faceboundaries
        elif oldname in self.edgeboundaries:
            bdydict = self.edgeboundaries
        elif oldname in self.pointboundaries:
            bdydict = self.pointboundaries
        else: 
            raise ooferror.ErrPyProgrammingError(
                "Boundary name %s not found." % oldname)

        bdydict[newname]=bdydict[oldname]
        del bdydict[oldname]

        # SkelContextBoundary.rename calls Skeleton.renameBoundary
        bdydict[newname].rename(newname)

        # Maintain consistency in Meshes
        for mesh in self.getMeshes():
            mesh.renameBoundary(oldname, newname)

        switchboard.notify("boundary renamed", self)
        # self.bdytimestamp.increment()
        self.selectBoundary(newname)
        switchboard.notify("new boundary configuration", self)

    # Retrieval routine -- returns the SkeletonContextBoundary object.
    def getBoundary(self, name):
        ## TODO 3.1: There should be just one dict for the name lookup.
        try:
            return self.edgeboundaries[name]
        except KeyError:
            try:
                return self.pointboundaries[name]
            except KeyError:
                return self.faceboundaries[name]

    # The selected boundary isn't actually used for anything directly,
    # but it's displayed in the GUI and its name is passed in as an
    # argument to commands that operate on boundaries.  
    def selectBoundary(self, bdyname):
        self.selectedBdyName = bdyname
        self.bdyselected.increment()    # timestamp
        switchboard.notify("boundary selected", self, bdyname)
        switchboard.notify('redraw')
    def unselectBoundary(self):
        if self.selectedBdyName is not None:
            self.selectedBdyName = None
            self.bdyselected.increment()
            switchboard.notify("boundary unselected", self)
            switchboard.notify('redraw')
    def getSelectedBoundaryName(self):
        return self.selectedBdyName
    def getSelectedBoundary(self):      # returns SkeletonContextBoundary object
        if self.selectedBdyName is not None:
            return self.getBoundary(self.selectedBdyName)
            

    # ## ### #### ##### ###### ####### ####### ###### ##### #### ### ## #

    # Routines that modify a boundary in place.  All of them exit via
    # the "bdyPropagate", which propagates the modified boundaries up
    # and down the stack.  All of these routines call
    # SkelContextBoundary objects which actually operate on the
    # sheriff of the current skeleton, not the current skeleton
    # itself.


    # Function to determine whether or not the requested modification
    # will result in a legal, sequence-able boundary.
    def try_appendSegsToBdy(self, name, seg_set):
        try:
            bdy = self.edgeboundaries[name]
        except KeyError:
            raise ooferror.ErrSetupError(
                "Boundary %s is not an edge boundary." % name)
        return bdy.try_appendSegs(seg_set)
        
    def appendSegsToBdy(self, name, seg_set):
        try:
            bdy = self.edgeboundaries[name]
        except KeyError:
            raise ooferror.ErrSetupError(
                "Boundary %s is not an edge boundary." % name)
        bdy.appendSegs(seg_set)
        self.bdyPropagate(name, bdy)

    def try_appendFacesToBdy(self, name, faces):
        try:
            bdy = self.faceboundaries[name]
        except KeyError:
            raise ooferror.ErrSetupError(
                "Boundary %s is not a face boundary." % name)
        return bdy.try_appendFaces(faces)

    def appendFacesToBdy(self, name, faces):
        try:
            bdy = self.faceboundaries[name]
        except KeyError:
            raise ooferror.ErrSetupError(
                "Boundary %s is not a face boundary." % name)
        bdy.appendFaces(faces)
        self.bdyPropagate(name, bdy)

    def try_removeFacesFromBdy(self, name, faces):
        try:
            bdy = self.faceboundaries[name]
        except KeyError:
            raise ooferror.ErrSetupError(
                "Boundary %s is not a face boundary." % name)
        return bdy.try_removeFaces(faces)

    def removeFacesFromBdy(self, name, faces):
        try:
            bdy = self.faceboundaries[name]
        except KeyError:
            raise ooferror.ErrSetupError(
                "Boundary %s is not a face boundary." % name)
        bdy.removeFaces(faces)
        self.bdyPropagate(name, bdy)

    def reverseBoundary(self, name):
        try:
            bdy = self.edgeboundaries[name] # SkelContextEdgeBoundary
        except KeyError:
            try:
                bdy = self.faceboundaries[name] # SkelContextFaceBoundary
            except KeyError:
                raise ooferror.ErrSetupError(
                    "Boundary %s is not an edge or face boundary." % name)
        bdy.reverse()
        self.bdyPropagate(name, bdy)

    def addNodesToBdy(self, name, node_list):
        try:
            bdy = self.pointboundaries[name]
        except KeyError:
            raise ooferror.ErrSetupError(
                "Boundary %s is not a point boundary." % name)
        bdy.appendNodes(node_list)
        self.bdyPropagate(name, bdy)

    # Function to determine whether or not the requested modification
    # will result in a legal, sequence-able boundary.
    def try_removeSegsFromBdy(self, name, seg_set):
        try:
            bdy = self.edgeboundaries[name]
        except KeyError:
            raise ooferror.ErrSetupError(
                "Boundary %s is not an edge Boundary." % name)

        return bdy.try_removeSegs(seg_set)
        
    # Function to actually do it.
    def removeSegsFromBdy(self, name, seg_set):
        try:
            bdy = self.edgeboundaries[name]
        except KeyError:
            raise ooferror.ErrSetupError(
                "Boundary %s is not an edge boundary." % name)

        bdy.removeSegs(seg_set)
        self.bdyPropagate(name, bdy)
        # self.bdytimestamp.increment()
        
    def removeNodesfromBdy(self, name, node_list):
        try:
            bdy = self.pointboundaries[name]
        except KeyError:
            raise ooferror.ErrSetupError(
                "Boundary %s is not a point boundary." % name)

        bdy.removeNodes(node_list)

        self.bdyPropagate(name, bdy)
        # self.bdytimestamp.increment()

    def bdyPropagate(self, name, contextbdy):
        # Replace the boundaries up and down the stack with a suitably
        # mapped version of the modified boundary.  Operate only
        # on sheriffs, and don't re-operate on the original object.

        # Then, ensure that the modifications get to the meshes --
        # in this case, we need to run over the whole stack, because
        # although deputy skeletons don't have boundaries, their
        # meshes nevertheless do.

        # Get the current sheriff
        start = self.resolveCSkeleton(self.getObject().sheriffSkeleton()) 
        children = self.undobuffer.getToTop()

        current = start
        for c in withoutDeputies(children[1:]):
            if not c is start:
                contextbdy.remove(c)
                contextbdy.map(current, c,
                               direction=cskeletonselectable.MAP_DOWN)
                current = c

        current = start
        parents = self.undobuffer.getToBottom()
        for p in withoutDeputies(parents[1:]):
            if not p is start:
                contextbdy.remove(p)
                contextbdy.map(current, p, direction=cskeletonselectable.MAP_UP)
                current = p

        # Since the boundaries have changed, the Meshes need to be
        # rebuilt.  There are subdimensional elements on Mesh
        # boundaries.
        self.unSyncMeshes()

    # ## ### #### ##### ###### ####### ####### ###### ##### #### ### ## #

    def allEdgeBoundaryNames(self):
        return self.edgeboundaries.keys()
    
    def allBoundaryNames(self):
        if config.dimension() == 2:
            return self.edgeboundaries.keys() + self.pointboundaries.keys()
        elif config.dimension() == 3:
            return (self.edgeboundaries.keys() + self.pointboundaries.keys() + 
                    self.faceboundaries.keys())

    def allBoundaryNamesSorted(self):
        pnames = self.pointboundaries.keys()
        pnames.sort()
        enames = self.edgeboundaries.keys()
        enames.sort()
        if config.dimension() == 2:
            return enames + pnames
        fnames = self.faceboundaries.keys()
        fnames.sort()
        return fnames + enames + pnames

    #Interface branch
    def allInterfaceNames(self):
        msobj=self.getMicrostructure()
        if runtimeflags.surface_mode:
            interfacemsplugin=msobj.getPlugIn("Interfaces")
            return interfacemsplugin.getInterfaceNames()
        else:
            return []
        
    def uniqueBoundaryName(self, name):
        if config.dimension() == 2:
            return utils.uniqueName(
                name, self.allBoundaryNames()+self.allInterfaceNames())
        if config.dimension() == 3:
            return utils.uniqueName(name, self.allBoundaryNames())

    # Get information about the named boundary, i.e. type, size, and
    # return it as a string, with newlines as appropriate.
    def boundaryInfo(self, boundaryname):
        outlist = []
        bdytype = "Edge"
        bdy = None
        try:
            bdy = self.edgeboundaries[boundaryname]
#             if bdy.sequenceableflag(self.getObject())==0:
#                 bdytype+=", not sequenceable"
        except KeyError:
            bdytype = "Point"
            try:
                bdy = self.pointboundaries[boundaryname]
            except KeyError:
                bdytype = "Face"
                try: 
                    bdy = self.faceboundaries[boundaryname]
                except KeyError:
                    bdytype = "Unknown"

        outlist.append("Type: %s" % bdytype)

        if bdy:
            outlist.append("Size: %i" % bdy.current_size())
            # outlist.append("Size: %i" % bdy.size(self.getObject()))
        
        return string.join(outlist,"\n")
        
                
    #Called by C++ edgement function refreshInterfaceMaterial() (element.C)
    def getInterfaceMaterial(self, edgementname):
        if edgementname in self.allEdgeBoundaryNames():
            interfacematname=self.getBoundary(edgementname)._interfacematerial
        else:
            interfacemsplugin=self.getMicrostructure().getPlugIn("Interfaces")
            interfacematname=interfacemsplugin.getInterfaceMaterialName(
                edgementname)
        if interfacematname:
            return materialmanager.materialmanager[interfacematname].actual
        else:
            return None
                

    # ## ### #### ##### ###### ####### ####### ###### ##### #### ### ## #

    # Copy over the group data from another skeletoncontext.
    def groupCopy(self, other):
        mygroups = [self.nodegroups, self.segmentgroups, self.elementgroups]
        othergroups = [other.nodegroups, other.segmentgroups,
                       other.elementgroups] 
        for (g, og) in map(None, mygroups, othergroups):
            g.nameCopy(og)

    # ## ### #### ##### ###### ####### ####### ###### ##### #### ### ## #

    # List retrievers, from here to the end of the undo buffer,
    # including (in both cases) the current skeleton.

    def getChildList(self):
        return self.undobuffer.getToTop()

    def getParentList(self):
        parents = self.undobuffer.getToBottom()
        if self.zombieSheriff:
            parents.append(self.zombieSheriff)
        return parents

    # ## ### #### ##### ###### ####### ####### ###### ##### #### ### ## #    


    def getMicrostructure(self):
        return self.getObject().getMicrostructure()
    
##    def removeWho(self, whopath):
##        ## if whopath[-1] == self.getObject().getMicrostructure().name():  # used to be this
##        if len(whopath)==1 and whopath[0]==self.getObject().getMicrostructure().name():
##            # Our Microstructure has been removed.  Remove ourself.
##            skeletonContexts.remove(self.path())

    def getSelectionContext(self, mode):
        return mode.getSelectionContext(self)

    def getMeshes(self):
        from ooflib.engine import mesh # avoid import loop
        path = labeltree.makePath(self.path())
        if not path:
            # path can be None if we're still in the process o
            # building a new SkeletonContext.  In that case, there are
            # no Meshes.
            return []
        meshnames = mesh.meshes.keys(
            path, condition=lambda x: not isinstance(x, whoville.WhoProxy))
        return [mesh.meshes[path + name] for name in meshnames]
            
    def __repr__(self):
        return 'SkeletonContext("%s")' % self.name()

    def sanity_check(self):
        # Check basic skeleton connections: the leg bone connected to
        # the knee bone, etc.

        diagnosis = self.getObject().sanityCheck() # returns string
        sane = not diagnosis
        if not sane:
            reporter.report(diagnosis)

        ## Old way, doing more of the check in python.
        # sane = self.getObject().sanity_check_old() # in cskeleton2.spy

        # Check that the predefined face boundaries have the right
        # area and the edge boundaries have the right length.
        x, y, z = self.getParent().getObject().size()
        areas = {"Ymax" : x*z, "Ymin" : x*z,
                 "Zmax" : x*y, "Zmin" : x*y,
                 "Xmin" : y*z, "Xmax" : y*z}
        for bdyname in areas:
            bdy = self.getBoundary(bdyname)
            bdyarea = bdy.current_boundary().area()
            if abs(bdyarea - areas[bdyname])/areas[bdyname] > 1.e-6:
                reporter.report(
                    "Area mismatch for boundary '%s'.  Expected %g, got %g."
                    % (bdyname, areas[bdyname], bdyarea))
                sane = False
        for bdyname in ("XmaxYmax", "XmaxYmin", "XmaxZmax", "XmaxZmin", 
                        "XminYmax", "XminYmin", "XminZmax", "XminZmin",
                        "YmaxZmax", "YmaxZmin", "YminZmax", "YminZmin",):
            if "Z" not in bdyname:
                length = z
            elif "X" not in bdyname:
                length = x
            elif "Y" not in bdyname:
                length = y
            bdy = self.getBoundary(bdyname)
            bdylength = bdy.current_boundary().length()
            if abs(bdylength - length)/length > 1.e-6:
                reporter.report(
                    "Length mismatch for boundary '%s'. Expected %g, got %g."
                    % (bdyname, length, bdylength))
                sane = False
        if sane:
            reporter.report("*** Skeleton Sanity Check passed. ***")
        else:
            reporter.report("*** Skeleton sanity check failed. ***")
        return sane


skeletonContexts = whoville.WhoDoUndoClass(
    'Skeleton',
    ordering=200,
    parentClass=microstructure.microStructures,
    instanceClass=SkeletonContext,
    proxyClasses=['<topmost>'])

utils.OOFdefine('skeletonContexts', skeletonContexts)

def getSkeleton(ms, name):
    # ms is a Microstructure.  Returns a SkeletonContext
    return skeletonContexts[[ms.name(), name]]

def extractSkeletonPath(somepath):
    #Calling labeltree.makePath may be a more formal way to do this.
    pathlist=string.split(somepath,":")
    if len(pathlist)<2:
        #Shouldn't happen
        return somepath
    return pathlist[0]+':'+pathlist[1]
