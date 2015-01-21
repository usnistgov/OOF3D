# -*- python -*-
# $RCSfile: historian.py,v $
# $Revision: 1.15.2.5 $
# $Author: langer $
# $Date: 2014/07/31 18:32:50 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

# The Historian class is used by GUI code to record and revisit
# previously executed commands (or other historical objects, but we'll
# call them 'commands' here).  It does not actually contain any GUI
# code itself, but it provides callbacks to be installed in GUI
# objects.

# Outside the Historian, the GUI must have a way of displaying
# commands and choosing between them, eg, with a
# RegisteredClassFactory.  The widget that does this must have a
# callback function called when its state is changed.  That callback
# must call (or be) Historian.stateChangeCB.  The GUI must also have
# 'Next' and 'Prev' buttons (or the equivalent) used to move through
# the historical commands, and the callbacks for those buttons must
# call (or be) Historian.nextCB and Historian.prevCB.

# The constructor takes some callbacks as arguments.  Only the first
# is required:
#
#  setCB is called when a historical object should be displayed.  The
#  object to be displayed is its first argument.  setCBkwargs, if any,
#  are passed to it as well.  (If setCB is a RegisteredClassFactory's
#  set() function, then setCBkwargs should be {'interactive':1}.
#
#  sensitizeCB (optional) is called when something has happened to
#  change the availability of the Next and Prev operations.  It should
#  call a function that uses Historian.nextSensitive() and
#  Historian.prevSensitive() to sensitize or desensitize the Next and
#  Prev buttons.
#
#  compareCB is called to determine if an object being stored matches
#  the previously stored object.  If compareCB returns True, the new
#  object is not stored.  The arguments to compareCB are the two
#  objects being compared.  If compareCB is None (the default value),
#  no comparison is done and new objects are always stored.

# Historian.record() must be used to put new objects in the history.
# These are the same objects that will be passed to setCB() later.

# Historian.__len__() returns the number of objects stored, and
# Historian.current() returns the current object, if the history is
# being edited, and None otherwise.

# History entries can be invalidated, eg. if I've selected the members
# of a group, but the group is later deleted, then going "previous" to
# that entry will result in an invalid display.  (This isn't really
# the historian's problem, though.  The widget displaying the
# operation should be able to display something sensible, or know that
# it's in an invalid state if it can't.)

from ooflib.common import debug
from ooflib.common import ringbuffer
from ooflib.common import mainthread

class Historian:
    def __init__(self, setCB, sensitizeCB=None, compareCB=None, 
                 bufsiz=50, setCBkwargs={}):
        self.editingHistory = False
        self.setCB = setCB
        self.setCBkwargs = setCBkwargs
        self.historyBuffer = ringbuffer.RingBuffer(bufsiz)
        self.sensitizeCB = sensitizeCB
        self.compareCB = compareCB
        self.inhibit = False

    ### Functions to examine/change the state of the Historian

    def record(self, obj):              # Add obj to the recorded history
        try:
            last = self.historyBuffer.last()
        except IndexError:
            last = None
        if (self.compareCB is None or last is None
            or not self.compareCB(obj, last)):
            self.historyBuffer.push(obj)
            self.editingHistory = True

        # TODO 3.1: When historians are changed programmatically,
        # from scripts for example, the widgets they refer to don't
        # reflect the last-issued command.  It's wrong to just always
        # revert the widgets here, because "record" may not be called
        # in a timely manner, and you might end up post-empting user
        # changes.  What should be done eventually is to detect
        # programmatic changes and update the widgets in that case,
        # and only in that case.
        # if self.setCB:
        #     self.setCB(obj, **self.setCBkwargs)

        if self.sensitizeCB:
            mainthread.runBlock(self.sensitizeCB)

    def nextSensitive(self):            # Is there a "next" history item?
        return not self.historyBuffer.atTop()

    def prevSensitive(self):            # Is there a "previous" history item?
        if self.editingHistory:
            return not self.historyBuffer.atBottom()
        return len(self.historyBuffer) > 0

    def __len__(self):
        return len(self.historyBuffer)

    def current(self):
        # This used to return None if self.editingHistory was false.
        # That was wrong, because it prevented the user from changing
        # the selector and repeating. (For example, using a different
        # pixel selection method with old mouse coordinates.)  The
        # question is, why did this function ever check
        # editingHistory?
        return self.historyBuffer.current()

    def clear(self):
        self.historyBuffer.clear()
        self.editingHistory = False
        self.inhibit = False

    # Find out what the next or previous value is, without actually
    # going to it.
    def nextVal(self):
        return self.historyBuffer.nextPeek()
    def prevVal(self):
        return self.historyBuffer.prevPeek()
        
    ### Callbacks to be installed in the GUI objects ###

    def stateChangeCB(self, *args):     # call this when the selector changes
        if self.inhibit:
            return
        self.editingHistory = False
        try:
            self.historyBuffer.last()
        except IndexError:
            pass
        if self.sensitizeCB:
            mainthread.runBlock(self.sensitizeCB)

    def nextCB(self, *args):            # go to the next history item
        self.historyBuffer.next()
        self.inhibit = True
        self.setCB(self.historyBuffer.current(), **self.setCBkwargs)
        self.inhibit = False
        self.editingHistory = True
        if self.sensitizeCB:
            mainthread.runBlock(self.sensitizeCB)

    def prevCB(self, *args):            # go to the previous history item
        if self.editingHistory:
            self.historyBuffer.prev()
        self.inhibit = True
        self.setCB(self.historyBuffer.current(), **self.setCBkwargs)
        self.inhibit = False
        self.editingHistory = True
        if self.sensitizeCB:
            mainthread.runBlock(self.sensitizeCB)

