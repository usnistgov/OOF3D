# -*- python -*-
# $RCSfile: skeletongroups.py,v $
# $Revision: 1.43.2.14 $
# $Author: fyc $
# $Date: 2014/08/06 21:39:44 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common import timestamp
from ooflib.SWIG.engine import cskeletongroups
from ooflib.common import debug
from ooflib.common import utils
import weakref

# GenericGroupSet is the base class for NodeGroupSet, ElementGroupSet,
# and SegmentGroupSet (ie, sets of groups of SkeletonSelectable
# objects).  It contains and manages all the groups of that type of
# object in a SkeletonContext.  GroupSets contain a list of *names* of
# groups, and a dictionary of GroupTrackers, one for each CSkeleton in
# the SkeletonContext.  Given the name of a group, a tracker returns
# the members of the group that are in the associated Skeleton.

# There is a single instance of each type of GroupSet in each
# SkeletonContext.  There is *no* object corresponding to a NodeGroup
# per se.  The members of a group can be retrieved by
# GenericGroupSet.get_group(groupname), which returns the objects
# belonging to the group in the current Skeleton in the
# SkeletonContext to which the GenericGroupSet belongs.

# All of the SkeletonSelectable groups have the same set of
# operations, given by the methods here.  Individual type-groups are
# nearly-trivial subclasses of this class.  Instances live in the
# SkeletonContext class.

# A minor complication arises from the existence of DeputySkeletons,
# which share their Nodes, Elements, and Segments with another
# (sheriff) Skeleton.  Since the objects are shared, there isn't the
# usual parent-child relationship between objects in one Skeleton and
# objects in the next Skeleton in the context's stack.  Furthermore,
# there can be no difference in group membership between a
# DeputySkeleton and its sheriff.  Therefore the way that group
# membership is propagated from one Skeleton to another depends on the
# type of Skeleton.  This is accomplished by having a different kind
# of tracker, a DeputyGroupTracker, for DeputySkeletons, and letting
# the tracker help out with the propagation.

# Skeleton groups are very similar to selections.  Could the selection
# just be a special kind of group?  It's probably difficult to do
# that, because selections need an undo/redo mechanism, and groups
# don't.

## TODO OPT: GenericGroupSet should be moved to C++.  Possibly there
## should be a core CGenericGroupSet class from which a Python
## GenericGroupSet is derived.  SelectionSetBase and Selection should
## be treated the same way, at the same time.  The current scheme
## sometimes requires loops over possibly long lists in Python.

class GenericGroupSet(object):
    def __init__(self, skeletoncontext, groupset=[]):
        self.skeletoncontext = skeletoncontext
        self.groups = utils.OrderedSet(groupset)

        # The "tracker" maintains data about group membership on a
        # skeleton-by-skeleton basis, eliminating (some) searches.
        # Keys are skeletons in the context, values are CGroupTracker
        # objects.
        self.tracker = weakref.WeakKeyDictionary()

        self.sbcallbacks = [
            switchboard.requestCallback(('whodoundo push', 'Skeleton'),
                                        self.new_skeleton)
            ]

    def destroy(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        # Break circular references
        ## TODO 3.1: Is this really necessary?
        del self.groups 

    # When new skeletons are pushed on, create the required groups.
    # This is the switchboard callback for "whodoundo push", and is
    # analogous to SelectionBase.whoChanged0 +
    # SelectionSet.implied_select. 
    ## (Why does this use the switchboard?  Can't pushModification
    ## call it directly?  Using the switchboard means there's less
    ## work to do if a new type of group is added.)
    def new_skeleton(self, context, oldskeleton, newskeleton):
        if context==self.skeletoncontext:
            # newGroupTracker() returns a new CGroupTracker instance if
            # newskeleton is a CSkeleton, but returns the existing
            # sheriff's CGroupTracker if newskeleton is a deputy.
            newtracker = newskeleton.newGroupTracker(self)
            self.tracker[newskeleton] = newtracker
            ## TODO 3.1: Use appropriate virtual functions instead of
            ## isinstance() here.  add_group() is a no-op for
            ## DeputyGroupTrackers, and impliedAddDown() should not be
            ## done either.  
            if not isinstance(newtracker, cskeletongroups.DeputyGroupTracker):
                for g in self.groups:
                    newtracker.add_group(g)
                self.impliedAddDown(newtracker)  

    # Add a name or names to the list of known groups. 
    def addGroup(self, *names):
        if names:
            for name in names:
                self.groups.add(name)
                for t in self.tracker.values():
                    t.add_group(name)
            switchboard.notify("groupset member added", self.skeletoncontext,
                               self, names[-1])

    # Remove a name or names from the list of known groups.
    def removeGroup(self, *names):
        if names:
            for name in names:
                if name in self.groups:
                    # Tracker's remove_group removes the selectables
                    # from the group.
                    for t in self.tracker.values():
                        t.remove_group(name)
                    self.groups.remove(name)
            switchboard.notify("groupset changed",
                               self.skeletoncontext, self)
                

    # Query whether the given name is known.
    def isGroup(self, name):
        return name in self.groups

    def nGroups(self):
        return len(self.groups)
    
    # "name" must exist, or an index error will be raised.
    def sizeOfGroup(self, name):
        current_tracker = self.tracker[self.skeletoncontext.getObject()]
        return current_tracker.get_group_size(name)

    # Set your list of known names from another group object.
    def nameCopy(self, other):
        self.groups = other.groups.copy()

    # Access the list of group names -- GUI will want this.
    def allGroups(self):
        return self.groups

    # Special extractor function -- gets the current members in the
    # current skeleton of the named group.
    def get_group(self, name):
        return self.tracker[self.skeletoncontext.getObject()].get_group(name)

    # current skeleton of the named group.
    def get_group_size(self, name):
        return self.tracker[self.skeletoncontext.getObject()].get_group_size(name)

    def get_groupFromSkeleton(self, name, skeleton):
        return self.tracker[skeleton].get_group(name)

    def getTracker(self, skeleton):
        return self.tracker[skeleton]

    def trackerlist(self):
        clist = [self.tracker[x]
                 for x in self.skeletoncontext.getChildList()]
        plist = [self.tracker[x]
                 for x in self.skeletoncontext.getParentList()]
        # Make sure that the starting tracker isn't a DeputyGroupTracker.
        while clist[0].sheriff() != clist[0]:
            clist[0:0] = [plist[1]]
            del plist[0]
        return (clist, plist)
        
    
    # Add the current selection to the indicated group.  Get the list
    # of skeletons from the skeletoncontext, convert it to a list of
    # trackers, and pass those on to the selectables.
    def addSelectionToGroup(self, name):
        if name in self.groups:
            clist, plist = self.trackerlist()
            for o in self.get_selection():
                o.add_to_group(name, clist, plist)
            switchboard.notify("groupset member resized",
                               self.skeletoncontext, self)

    def removeSelectionFromGroup(self, name):
        if name in self.groups:
            clist, plist = self.trackerlist()
            for o in self.get_selection():
                o.remove_from_group(name, clist, plist)
            switchboard.notify("groupset member resized",
                               self.skeletoncontext, self)

    # Add objects to a bunch of groups.  The argument is a dictionary
    # keyed by group name.  The values are lists of objects to add to
    # each group.  Used by skeletonIO.
    def addToGroup(self, **gdict):
        nontrivial = False
        for name, objects in gdict.items():
            if name in self.groups and len(objects) > 0:
                clist, plist = self.trackerlist()
                nontrivial = True
                for o in objects:
                    o.add_to_group(name, clist, plist)
        if  nontrivial:
            switchboard.notify("groupset member resized",
                               self.skeletoncontext, self)

    # Modify a group name, retaining membership info.
    def renameGroup(self, oldname, newname):
        if oldname in self.groups:
            for t in self.tracker.values():
                newname = utils.uniqueName(newname, list(self.groups),
                                           exclude=oldname)
                t.rename_group(oldname, newname)
            if oldname != newname:
                self.groups.replace(oldname, newname)
            switchboard.notify("groupset member renamed",
                               self.skeletoncontext, self, newname)

    # Make a new name with the same members as an old name.
    def copyGroup(self, oldname, newname):
        if oldname in self.groups:
            for t in self.tracker.values():
                t.add_group(newname)
                for e in t.get_group(oldname):
                    e.add_group_to_local(newname)
                    t.add(newname,e) 
            self.groups.add(newname)
            switchboard.notify("groupset member added",
                               self.skeletoncontext, self, newname)

    # Remove all members from the named group(s), but do not remove the groups.
    def clearGroup(self, *names):
        if names:
            for name in names:
                if name in self.groups:
                    for t in self.tracker.values():
                        t.clear_group(name)
            switchboard.notify("groupset member resized",
                               self.skeletoncontext, self)

class GenericMaterialGroupSet(GenericGroupSet):
    # Base class for GroupSets that can have Materials assigned to
    # them.
    def __init__(self, *args, **kwargs):
        GenericGroupSet.__init__(self, *args, **kwargs)
        self.materials = {}
        switchboard.requestCallback("remove_material", self.removeMatlCB)
    def assignMaterial(self, groupname, material):
        ts = timestamp.TimeStamp()
        ts.increment()
        self.materials[groupname] = (material, ts)
        switchboard.notify("materials changed in skeleton",
                           self.skeletoncontext)
        for mesh in self.skeletoncontext.getMeshes():
            mesh.refreshMaterials(self.skeletoncontext)
        switchboard.notify("redraw")
        
    def removeMaterial(self, groupname):
        del self.materials[groupname]
        switchboard.notify("materials changed in skeleton",
                           self.skeletoncontext)
        for mesh in self.skeletoncontext.getMeshes():
            mesh.refreshMaterials(self.skeletoncontext)
        switchboard.notify("redraw")
    def removeMatlCB(self, material):
        for grpname, (matl, ts) in self.materials.items():
            if matl is material.actual:
                self.removeMaterial(grpname)
    def getMaterialAndTime(self, group):
        try:
            return self.materials[group]
        except KeyError:
            return (None, None)
    def getMaterial(self, group):
        try:
            return self.materials[group][0]
        except KeyError:
            return None
    def getAllMaterials(self):
        # Returns a list of (groupname, materialname) tuples in the
        # order in which the materials were assigned.
        stuff = [(t, (g, m)) for (g, (m,t)) in self.materials.items()]
        stuff.sort()            # sorts by timestamp t
        return [x[1] for x in stuff]


# The GroupTracker object.  Within the GroupSet, there is one
# GroupTracker per Skeleton of the GroupSet's associated
# SkeletonContext.  The GroupTracker object itself contains a
# dictionary indexed by group names, and value'd by Sets of the
# selectables which are members of the group.  When objects are added
# to or removed from groups via the GroupSet calls addSelectionToGroup
# or removeSelectionFromGroup, lists of grouptrackers are passed in to
# the selectable's group-propagation routines.  These lists are in
# skeleton order corresponding to the child and parent skeletons of
# the selectable, respectively.  The selectable keeps the trackers up
# to date, and passes the appropriate sublist to its parents and
# children when it recursively calls them.

# class GroupTracker:
#     def __init__(self):
#         self.data = {}
#     def add_group(self, name):
#         self.data[name]=set()
#     def clear_group(self, name):
#         for e in self.data[name]:
#             e.remove_group_from_local(name)
#         self.data[name].clear()
#     def remove_group(self, name):
#         for e in self.data[name]:
#             e.remove_group_from_local(name)
#         del self.data[name]
#     def rename_group(self, oldname, newname):
#         elist = self.data[oldname]
#         del self.data[oldname]
#         self.data[newname] = elist
#         for e in elist:
#             e.remove_group_from_local(oldname)
#             e.add_group_to_local(newname)
#     def add(self, name, object):
#         self.data[name].add(object)
#     def remove(self, name, object):
#         self.data[name].remove(object)
#     def addDown(self, group, selectable, clist):
#         selectable.addDown(group, clist)
#     def addUp(self, group, selectable, plist):
#         selectable.addUp(group, plist)
#     def removeDown(self, group, selectable, clist):
#         selectable.removeDown(group, clist)
#     def removeUp(self, group, selectable, plist):
#         selectable.removeUp(group, plist)
#     def sheriff(self):
#         return self
#     def promote(self):
#         return self
#     def __repr__(self):
#         return "GroupTracker"

#     # Data retrieval functions.
#     def get_group_size(self, name):
#         return len(self.data[name])
#     def get_group(self, name):
#         return self.data[name]
    

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        
# Node group operations.

class NodeGroupSet(GenericGroupSet):
    def __init__(self, skeletoncontext):
        GenericGroupSet.__init__(self, skeletoncontext)

    def get_selection(self):
        return self.skeletoncontext.nodeselection.retrieve()

    def displayString(self, name):
        if self.isGroup(name):
            s = self.sizeOfGroup(name)
            return "%s (%d node%s)" % (name, s, "s"*(s!=1))

    def impliedAddDown(self, tracker):
        # Having created a new Skeleton, add it to all the trackers
        # for all the nodes.  This is called *before* the new
        # CSkeleton is pushed, so getObject() returns the previous
        # CSkeleton, but tracker is the *new* CSkeleton's tracker.
        self.skeletoncontext.getObject().nodesAddGroupsDown([tracker])

# Segment...

class SegmentGroupSet(GenericGroupSet):
    def __init__(self, skeletoncontext):
        GenericGroupSet.__init__(self, skeletoncontext)

    def get_selection(self):
        return self.skeletoncontext.segmentselection.retrieve()

    def displayString(self, name):
        if self.isGroup(name):
            s = self.sizeOfGroup(name)
            return "%s (%d segment%s)" % (name, s, "s"*(s!=1))

    def impliedAddDown(self, tracker):
        self.skeletoncontext.getObject().segmentsAddGroupsDown([tracker])
# Face...

class FaceGroupSet(GenericGroupSet):
    def __init__(self, skeletoncontext):
        GenericGroupSet.__init__(self, skeletoncontext)

    def get_selection(self):
        return self.skeletoncontext.faceselection.retrieve()

    def displayString(self, name):
        if self.isGroup(name):
            s = self.sizeOfGroup(name)
            return "%s (%d face%s)" % (name, s, "s"*(s!=1))
        
    def impliedAddDown(self, tracker):
        self.skeletoncontext.getObject().facesAddGroupsDown([tracker])

# ...and of course Element...

class ElementGroupSet(GenericMaterialGroupSet):
    def __init__(self, skeletoncontext):
        GenericMaterialGroupSet.__init__(self, skeletoncontext)

    def get_selection(self):
        return self.skeletoncontext.elementselection.retrieve()

    def displayString(self, name):
        if self.isGroup(name):
            s = self.sizeOfGroup(name)
            m, t = self.materials.get(name, (None, None))
            if m:
                return "%s (%d element%s, material=%s)" % (name, s, "s"*(s!=1),
                                                           m.name())
            else:
                return "%s (%d element%s)" % (name, s, "s"*(s!=1))

    def impliedAddDown(self, tracker):
        self.skeletoncontext.getObject().elementsAddGroupsDown([tracker])
