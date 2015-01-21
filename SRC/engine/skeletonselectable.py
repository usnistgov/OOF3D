# -*- python -*-
# $RCSfile: skeletonselectable.py,v $
# $Revision: 1.63.2.36 $
# $Author: langer $
# $Date: 2014/11/05 16:54:31 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.SWIG.common import config
from ooflib.SWIG.common import lock
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.engine import cskeletonselectable
from ooflib.common import debug
from ooflib.common import ringbuffer
from ooflib.common import utils
from ooflib.engine import skeletonselmodebase
import sys
import weakref

# A Selection object contains a RingBuffer of SelectionSets.  Undoing
# and redoing the selection changes the state of the RingBuffer and
# causes the newly current SelectionSet to be written into the
# SkeletonContext's stack of Skeletons (which is also a RingBuffer).
# A SelectionSet contains a dictionary of SelectionTrackers, one entry
# for each CSkeleton in the SkeletonContext's undo buffer.

# SelectionSet objects occupy the undo/redo stack of the various
# Selection objects.  Each SelectionSet contains a WeakKeyDictionary
# of SelectionTrackers, keyed by the Skeleton to which the tracker
# belongs.  The dictionary is weak so that the trackers go away when
# the Skeleton is destroyed.

# The base class doesn't contain any references to selection, so that
# the machinery can be used for pinned nodes and other such skeleton
# component attributes.  See SelectionSet (below) for the functions
# that a derived class must provide.

class SelectionSetBase:
    def __init__(self, skeletoncontext):
        self.skeletoncontext = skeletoncontext
        # Dictionary of Trackers, keyed by Skeletons
        self.selected = weakref.WeakKeyDictionary()

    def getTracker(self, skeleton):
        return self.selected[skeleton]

    # clearskeletons() is called when undoing or redoing a selection
    # operation.  It clears the selection state of all objects in the
    # selection set.  It does not change the trackers, just the
    # objects to which they refer. 
    def clearskeletons(self):
        for tracker in self.selected.values(): 
            tracker.clearskeleton()

    # Optimizing shortcut -- we know in advance that the correct
    # entries are empty SelectionTrackers corresponding to each key in
    # the selection's tracker dictionary.  Note that this actually
    # operates on the selectables.
    def clear(self):
        for tracker in self.selected.values():
            tracker.clear()                  

    def clearable(self):
        for tracker in self.selected.values():
            if not tracker.empty():
                return 1
        return 0

    def __repr__(self):
        return "%s(%d)" % (self.__class__.__name__, id(self))
    

class SelectionSet(SelectionSetBase):

    # Do implied-selections for new skeletons.  Creates a tracker and
    # copies the selection state from the old skeleton to the new
    # skeleton.
    def implied_select(self, oldskel, newskel):
        tracker = newskel.newSelectionTracker(self)
        self.selected[newskel] = tracker
        if oldskel != newskel:      # ie, not the initial skeleton
            oldtracker = self.selected[oldskel]
            tracker.implied_select(oldtracker)

    def clone(self):
        # SelectionSets are cloned by SelectionBase.start(), which is
        # called at the beginning of an undoable selection operation.
        # (That's undo-able, not un-doable.)
        flippo = self.__class__(self.skeletoncontext)

        # deputy trackers can't be cloned directly, since they have to
        # refer to non-deputy trackers in the new SelectionSetBase.
        # This first pass only clones the non-deputies, because
        # DeputySelectionTracker.clone() is a no-op.
        for (skel,tracker) in self.selected.items():
            flippo.selected[skel] = tracker.clone()

        # The second pass looks for trackers that weren't cloned in
        # the first pass and creates deputies referring to the correct
        # non-deputies.
        for (skel, tracker) in flippo.selected.items():
            if tracker is None:
                tracker = flippo.getTracker(skel.sheriffSkeleton())
                flippo.selected[skel] = \
                             cskeletonselectable.DeputySelectionTracker(tracker)
        return flippo

##++--++####++--++####++--++####++--++####++--++####++--++####++--++##

# The selection object for all the selections and the set of pinned
# nodes.  This is the master object, which lives at the
# SkeletonContext level, and holds the ringbuffer of SelectionSets.
# SelectionSets themselves have dictionaries of SelectionTrackers.

# SelectionBase doesn't contain any references to selection, so that
# its machinery can be used for pinning as well as selecting.  The
# derived classes must provide functions that actually do the
# selecting (or whatever).  Their __init__()s must call
# SelectionBase.__init__() and then push an appropriate SelectionSet
# object onto self.stack.

## TODO OPT: Move SelectionBase and Selection to C++.  Also PinnedNodeSet
## and PinnedNodeSelection in skeletonnode.py.

class SelectionBase:
    def __init__(self, skeletoncontext):
        self.skeletoncontext = skeletoncontext
        self.rwLock = lock.RWLock()

        self.sbcallbacks = [
            switchboard.requestCallback(('whodoundo push', 'Skeleton'),
                                        self.whoChanged0)
            ]

    def destroy(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        self.stack.clear()      # break circular references
        del self.skeletoncontext
        
    # "Start" should be called prior to operations which are
    # meant to be undoable.
    def start(self):
        self.stack.push(self.stack.current().clone())

    def whoChanged0(self, context, oldskeleton, newskeleton):
        if self.skeletoncontext is context:
            # Loop over SelectionSets in the RingBuffer.
            for selectionset in self.stack:
                # Create a Tracker for the new Skeleton and populate
                # its data array.
                selectionset.implied_select(oldskeleton, newskeleton)
            # Set the "selected" flag in the CSkeletonSelectable
            # objects.
            self.stack.current().selected[newskeleton].write()

    # Response to mesh modification events [('who changed', 'Skeleton') signal]
    def newSkeleton(self, skelcontext):
        if skelcontext is self.skeletoncontext:
            self.signal()

    # This returns a SelectionSet object, which has the current state
    # for the entire stack.  To get the current skeleton's current
    # selection, use "retrieve", below.
    def currentSelection(self):
        return self.stack.current()

    def currentSelectionTracker(self):
        return \
         self.stack.current().selected[self.skeletoncontext.getObject()]

    # Selection retrieval function -- returns the list of currently
    # selected elements in the current skeleton of the current
    # context.  This is what the user almost certainly understands to
    # be "the selection". 
    ## TODO OPT: Get rid of this function. Selection lists can be long and
    ## shouldn't be copied from C++ to Python.
    def retrieve(self):
        # self.stack.current().selected is a WeakKeyDict of
        # SelectionTrackers, keyed by Skeleton.
        return \
         self.stack.current().selected[self.skeletoncontext.getObject()].get()

    def retrieveFromSkeleton(self, skel):
        return self.stack.current().selected[skel].get()

    def retrieveSize(self):
        return \
         self.stack.current().selected[self.skeletoncontext.getObject()].size()

    def trackerlist(self):
        # Get trackers for all child and parent skeletons at the
        # current selection state.  The current skeleton's tracker is
        # element 0 of both lists.
        #
        # The Selection class redefines trackerlist() to ensure that
        # the first element of each list is not a deputy.
        # PinnedNodeSelection, which is also derived from
        # SelectionBase, doesn't need to do that, which is why it's
        # not done here in the base class.
        selectionset = self.stack.current()
        clist = [selectionset.selected[x]
                 for x in self.skeletoncontext.getChildList()]
        plist = [selectionset.selected[x]
                 for x in self.skeletoncontext.getParentList()]
        return clist, plist


    # Selection stack manipulation stuff.
    def undo(self):
        if self.undoable():
            self.stack.current().clearskeletons()
            self.stack.prev()
            skel = self.skeletoncontext.getObject()
            tracker = self.stack.current().selected[skel]
            #tracker.clearskeleton()
            tracker.write()

    def redo(self):
        if self.redoable():
            self.stack.current().clearskeletons()
            self.stack.next()
            skel = self.skeletoncontext.getObject()
            tracker = self.stack.current().selected[skel]
            #tracker.clearskeleton()
            tracker.write()
    
    def undoable(self):
        return not self.stack.atBottom()
    
    def redoable(self):
        return not self.stack.atTop()

    # Stack is clearable if there is any selection, even if it's invisible.
    def clearable(self):
        return self.stack.current().clearable()

    def invertable(self):
        return 1

    def clear(self):
        # Clear the current tracker set directly.  SelectionSet's
        # "clear" routine is a special exception that modifies the
        # selectables directly.
        self.stack.current().clear()

    # New size:  # of selected objects in the current skeleton.
    def size(self):
        skeleton = self.skeletoncontext.getObject()
        return self.stack.current().selected[skeleton].size()

    def setUndoBufferSizeCB(self, size):
        self.stack.resize(size)
        self.signal()

    def begin_reading(self):
        ## debug.fmsg()
        self.rwLock.read_acquire()
    def end_reading(self):
        ## debug.fmsg()
        self.rwLock.read_release()

    def begin_writing(self):
        ## debug.fmsg()
        self.rwLock.write_acquire()
    def end_writing(self):
        ## debug.fmsg()
        self.rwLock.write_release()

    def pause_writing(self):
        ## debug.fmsg()
        self.rwLock.write_pause()
    def resume_writing(self):           # a useful skill for job applicants
        ## debug.fmsg()
        self.rwLock.write_resume()
        

    def __repr__(self):
        return "%s(%d)" % (self.__class__.__name__, self.retrieveSize())

# Base class for selections, but not for the set of pinned nodes.

class Selection(SelectionBase):
    def __init__(self, skeletoncontext):
        SelectionBase.__init__(self, skeletoncontext)
        # Ringbuffer of SelectionSet objects -- these contain
        # selections for undo/redo.
        self.stack = ringbuffer.RingBuffer(self.mode().stacksize)
        self.stack.push(SelectionSet(self.skeletoncontext))
        self.sbcallbacks.append(switchboard.requestCallback(
            ('skelselection ringbuffer resize', self.mode().name),
            self.setUndoBufferSizeCB))

    def destroy(self):
        SelectionBase.destroy(self)
        del self.stack

    def trackerlist(self):
        clist, plist = SelectionBase.trackerlist(self)
        # Make sure that the starting point isn't a DeputyTracker.
        while clist[0].sheriff() != clist[0]:
            clist[0:0] = [plist[1]]
            del plist[0]
        return (clist, plist)

    # The Four Selection Operations. Which need to go away.
    ## TODO OPT: Move these to C++ and use couriers to avoid constructing
    ## lists of objects in Python and translating them to C++.
    def select(self, objlist):
        (clist, plist) = self.trackerlist()
        skeleton = self.skeletoncontext.getObject()
        for o in objlist:
            if o.active(skeleton):
                o.select(clist, plist) 

    def deselect(self, objlist):
        (clist, plist) = self.trackerlist()
        skeleton = self.skeletoncontext.getObject()
        for o in objlist:
            if o.active(skeleton):
                o.deselect(clist, plist)
        
    def toggle(self, objlist):
        (clist, plist) = self.trackerlist()
        skeleton = self.skeletoncontext.getObject()
        for o in objlist:
            if o.active(skeleton):
                if o.isSelected():
                    o.deselect(clist, plist)
                else:
                    o.select(clist, plist)

    def invert(self):
        # Invert the selection status of all objects.  Loop over all
        # elements is unavoidable in this case, since every object
        # must be operated on.
        (clist, plist) = self.trackerlist()
        skeleton = self.skeletoncontext.getObject()
        for o in self.get_objects():
            if o.active(skeleton):
                if o.isSelected():
                    o.deselect(clist, plist)
                else:
                    o.select(clist, plist)

    # Selects objects from already selected ones
    def selectSelected(self, objlist):
        (clist, plist) = self.trackerlist()
        skeleton = self.skeletoncontext.getObject()        
        for o in self.get_objects():
            if o.active(skeleton) and o.isSelected() and o not in objlist:
                o.deselect(clist, plist)

    def clear(self):
        # "Clear" needs to really clear the selection in all
        # CSkeletons, not just the current one.  There may be objects
        # selected in the other CSkeletons that don't correspond to
        # selected objects in the current CSkeleton.  Therefore this
        # doesn't simply deselect the currently selected objects.
        (clist, plist) = self.trackerlist()
        for tracker in clist:
            tracker.clear()
        for tracker in plist:
            tracker.clear()

    def signal(self):
        switchboard.notify(self.mode().changedselectionsignal, selection=self)
        ## TODO OPT: When a new Skeleton is created, this routine is
        ## called once for each type of selectable, resulting in more
        ## redraws than are strictly necessary. "redraw" should be
        ## sent only from the calling menuitem.
        switchboard.notify("redraw")

# Subclasses of Selection must have a "mode" function that returns the
# corresponding SkeletonSelectionMode object, so that the generic
# selection manipulation routines can send the correct switchboard
# signals.  They are also distinguished by their method for getting
# all of the objects in the current skeleton, which is needed by
# "invert".

class ElementSelection(Selection):
    def num_objects(self):
        return self.skeletoncontext.getObject().nelements()
    def get_objects(self):
        return self.skeletoncontext.getObject().getElements()
    def mode(self):
        return skeletonselmodebase.getMode("Element")

class SegmentSelection(Selection):
    def num_objects(self):
        return self.skeletoncontext.getObject().nsegments()
    def get_objects(self):
        return self.skeletoncontext.getObject().getSegments()
    def mode(self):
        return skeletonselmodebase.getMode("Segment")

if config.dimension() == 3:
    class FaceSelection(Selection):
        def num_objects(self):
            return self.skeletoncontext.getObject().nfaces()
        def get_objects(self):
            return self.skeletoncontext.getObject().getFaces()
        def mode(self):
            return skeletonselmodebase.getMode("Face")

class NodeSelection(Selection):
    def num_objects(self):
        return self.skeletoncontext.getObject().nnodes()
    def get_objects(self):
        return self.skeletoncontext.getObject().getNodes()
    def mode(self):
        return skeletonselmodebase.getMode("Node")

