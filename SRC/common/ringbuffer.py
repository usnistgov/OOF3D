# -*- python -*-
# $RCSfile: ringbuffer.py,v $
# $Revision: 1.16.2.3 $
# $Author: langer $
# $Date: 2014/03/05 17:00:09 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

# A finite stack which accepts (but does not hold) an infinite amount
# of data.  If too many items have been pushed onto the stack, the
# oldest items are overwritten.  There are next(), prev(), first(),
# and last() methods for moving around in the stack (each of which
# raises IndexError if necessary).  Pushing a new entry when not at
# the top of the stack will delete all entries above the current one.
# Popping an old entry when not at the top deletes all entries from
# the current one to the top.

# Constructor args are:
#    n  -- max number of objects to retain
#    overwritefunc -- a function called when an object is removed (optional).
#                     The object is passed as the argument.

# Functions:
#   clear()
# The following 5 functions change the current position:
#   push(obj)		inserts obj above current position and makes it current
#   pop()		removes & returns obj at current position
#   next()		goes to next object and returns it
#   prev()		goes to previous object and returns it
#   first()		goes to oldest remaining object and returns it
#   last()		goes to latest object and returns it

#   current()		returns entry at the current position
#   nextPeek()          returns entry at next position, without changing current
#   prevPeek()          

#   resize(n)		changes the number of retained objects, keeping
#			the most recent ones if the new size is less than
#			the old size

# __getitem__ and __len__ are defined so that looping over a
# RingBuffer returns the retained objects from oldest to newest.
# That is, stack[0] is the same as stack.first() and stack[-1] is the
# same as stack.last(), except that using __getitem__ doesn't change
# the current position.

# Also has special slice-like functions getToTop and getToBottom,
# which return lists of the objects from the current position to the
# top, inclusive, and from the current position to the bottom,
# inclusive.  If c is the current position, then getToTop is the slice
# buffer[c:], and getToBottom is the result of the delightfully
# baroque (buffer[:c].append(buffer[c])).reverse(), i.e. a list like
# [buffer[c], buffer[c-1], buffer[c-2], ... buffer[0]] These functions
# handle wraparound correctly, so they're not necessarily contiguous
# sublists of self.data.

import string
from ooflib.common import debug

class RingBuffer:
    """
    A finite stack which accepts an unlimited number of items. If the
    stack is full, new items overwrite older ones.
    """
    def __init__(self, n, overwritefunc=None, data=[]):
        self.data = [None]*n
        self.currentpos = 0             # current entry
        self.top = 0                    # next available slot
        self.bottom = 0                 # oldest entry
        self.ndata = 0                  # number of entries
        self.overwrite = overwritefunc
        for datum in data:
            self.push(datum)

    # Clears data in range [lo, hi), wrapping around if necessary.
    # Resets self.ndata, but not self.top or self.bottom.
    def clearRange(self, lo, hi):
        # top == bottom if the buffer is either full or empty, so we
        # need first to explicitly check for emptiness.
        if self.ndata == 0:
            return
        nclear = hi - lo                # how many items to remove
        if nclear <= 0:
            nclear += len(self.data)
        # Erase in reverse order, so that overwrite() is called on
        # newest objects first.
        for i in range(nclear-1, -1, -1):
            j = (lo + i) % len(self.data)
            if self.overwrite:
                self.overwrite(self.data[j])
            self.data[j] = None
        self.ndata -= nclear
        
    def clear(self):
        self.clearRange(self.bottom, self.top)
        self.top = 0
        self.bottom = 0
        self.currentpos = 0
        # assert all([x is None for x in self.data])

    def __contains__(self, obj):
        if self.bottom < self.top:
            return obj in self.data[self.bottom:self.top]
        if self.top < self.bottom:
            return obj in self.data[self.bottom:] or obj in self.data[:self.top]
        return False

    def push(self, obj):
        nextpos = (self.currentpos + 1) % len(self.data)
        if self.ndata == 0:
            self.data[0] = obj
            self.top = 1
            self.currentpos = 0
            self.ndata = 1
        elif nextpos != self.top: # not at top of stack
            self.currentpos = nextpos
            self.clearRange(self.currentpos, self.top) # delete to top
            self.ndata += 1
            self.top = (nextpos + 1) % len(self.data)
            self.data[self.currentpos] = obj
        elif self.top == self.bottom:   # at top, but have to overwrite oldest
            if self.overwrite:
                self.overwrite(self.data[self.top])
            self.data[self.top] = obj
            self.currentpos = self.top
            self.top = (self.top + 1) % len(self.data)
            self.bottom = self.top
        else:                           # at top, space is available
            self.data[self.top] = obj
            self.currentpos = self.top
            self.top = (self.top + 1) % len(self.data)
            self.ndata += 1

## pop() is commented out because it's not used, and it's not clear
## whether or not it ought to call overwrite() on the datum that is
## being popped.  Perhaps if there's a need to use it, there will be a
## way of deciding the issue.
##            
##    def pop(self):
##        if self.ndata == 0:
##            raise IndexError
##        obj = self.current()
##        if self.currentpos == self.bottom:
##            obj = self.current()
##            self.clear()
##        else:
##            self.prev()
##            newtop = (self.currentpos+1) % len(self.data)
##            self.clearRange(newtop, self.top)  # calls overwrite
##            self.top = newtop
##        return obj

    def current(self):
        if self.ndata == 0:
            raise IndexError
        return self.data[self.currentpos]
    def prev(self):
        if self.currentpos == self.bottom or self.ndata == 0:
            raise IndexError
        self.currentpos = (self.currentpos - 1)%len(self.data)
        return self.current()
    def prevPeek(self):
        # Return the previous object, without altering the current position.
        if self.currentpos == self.bottom or self.ndata == 0:
            return None
        return self.data[(self.currentpos - 1) % len(self.data)]
    def next(self):
        if self.ndata == 0 or self.currentpos == (self.top - 1)%len(self.data):
            raise IndexError
        self.currentpos = (self.currentpos + 1) % len(self.data)
        return self.current()
    def nextPeek(self):
        # Return the next object, without altering the current position.
        if self.ndata == 0 or self.currentpos == (self.top-1)%len(self.data):
            return None
        return self.data[(self.currentpos + 1) % len(self.data)]
    def first(self):
        self.currentpos = self.bottom
        return self.current()
    def last(self):
        if len(self) > 0:
            self.currentpos = self.top-1
        return self.current()
    def atBottom(self):
        return self.currentpos == self.bottom or self.ndata == 0
    def atTop(self):
        return self.ndata == 0 or \
               self.currentpos == (self.top - 1)%len(self.data) \


    # Return a list of the items in the stack from the current point
    # to the top, inclusive.  "self.top" points to the next unoccupied
    # slot in the stack.
    def getToTop(self, start=None):
        if self.ndata == 0:
            return []
        if start is None:
            i = self.currentpos
        else:
            i = self.data.index(start)
        # Special case when current position is at the bottom of the stack. 
        if i == self.bottom:
            return map(self.__getitem__, range(self.ndata))
        # General case
        rlist = []
        while i!=self.top:
            rlist.append(self.data[i])
            i = (i+1)%len(self.data)
        return rlist

    # Similar, from the current point to the bottom, inclusive.  Note
    # that the returned list starts at the current point and ends
    # at the bottom, i.e. is reversed relative to self.data.
    # "self.bottom" points to the lowest occupied slot.
    def getToBottom(self, start=None):
        if start is None:
            i = self.currentpos
        else:
            i = self.data.index(start)
        rlist = [self.data[i]]
        while i!=self.bottom:
            i = (i-1)%len(self.data)
            rlist.append(self.data[i])
        return rlist
        
    def __getitem__(self, i):
        if i >= self.ndata or i < -self.ndata:
            raise IndexError
        if i >= 0:                      # count from bottom up
            return self.data[(self.bottom + i) % len(self.data)]
        # i < 0. Count from top down.
        return self.data[(self.top + i + len(self.data)) % len(self.data)]
    def __len__(self):
        return self.ndata
    def __repr__(self):
        # repr =  'RingBuffer(' + `len(self.data)`
        # if self.overwrite:
        #     repr += ', overwritefunc=' + self.overwrite.__name__
        # if self.ndata > 0:
        #     repr += ', data=[' + string.join([`obj` for obj in self], ',')+']'
        # repr += ')'
        # return repr
        return "RingBuffer(%d, %s)" % (id(self), [x for x in self.data
                                                  if x is not None])

    def resize(self, newsize):
        if newsize == len(self.data):
            return
        
        newdata = [None]*newsize
        depth = self.top - self.currentpos # try to maintain this
        if depth <= 0:
            depth += len(self.data)     # wrap around

        # If the data won't fit in the new size, discard the oldest
        # data, unless that would mean discarding the current
        # position.
        if self.ndata <= newsize:
            # Don't have to eliminate any data
            ncopy = self.ndata          # number to copy to new data array
            copystart = self.bottom     # where to start copying
            deleterange = []            # data to delete
            self.currentpos = ncopy - depth # new value
        else:
            ncopy = newsize
            # Have to eliminate some data
            ndelete = self.ndata - newsize # number to delete
            if depth <= newsize:
                # eliminate old data only
                copystart = (self.bottom + ndelete) % len(self.data)
                deleterange = [(self.bottom, copystart)]
                self.currentpos = ncopy - depth
            else:
                # eliminate some new data too, so that we don't
                # delete the current datum
                copystart = self.currentpos
                deleterange = [(self.bottom, copystart),
                               ((self.bottom+ncopy)%len(self.data), self.top)]
                self.currentpos = 0

        for i in range(ncopy):
            newdata[i] = self.data[(copystart + i) % len(self.data)]

        for min,max in deleterange:
            self.clearRange(min, max)
            
        self.bottom = 0
        self.top = ncopy % newsize
        self.ndata = ncopy
        self.data = newdata
        
        
if __name__ == '__main__':
    def f(obj):
        print 'removing', obj
    c = RingBuffer(5, overwritefunc=f, data=['a', 'b'])
    print 'initial', c, c.data
    c.clear()
    print 'clear() ndata=', c.ndata, c.data
    c.clear()
    print 'clear() ndata=', c.ndata, c.data
    c.push(1)
    c.push(2)
    c.push(3)
    c.push(4)
    c.push(5)
    print c.ndata, c.data, 'current=', c.current()
    c.push(6)
    print c.ndata, c.data, 'current=', c.current()
    print '--- prev(), prev() ---'
    c.prev()
    c.prev()
    print c.ndata, c.data, 'current=', c.current()
    print '--- resize(3) ---'
    c.resize(3)
    print c.ndata, c.data, 'current=', c.current(), 'top=', c.atTop(), 'bottom=', c.atBottom()
    print '--- resize(5) ---'
    c.resize(5)
    print c.ndata, c.data, 'current=', c.current(), 'top=', c.atTop(), 'bottom=', c.atBottom()
    print '--- push(6), push(7) ---'
    c.push(6)
    c.push(7)
    print c.ndata, c.data, 'current=', c.current()
    print '--- push(8), push(9) ---'
    c.push(8)
    c.push(9)
    print c.ndata, c.data, 'current=', c.current()
    print '--- prev(), prev() ---'
    c.prev()
    c.prev()
    print c.ndata, c.data, 'current=', c.current()
    print "--- resize(2) ---"
    c.resize(2)
    print c.ndata, c.data, 'current=', c.current(), 'top=', c.atTop(), 'bottom=', c.atBottom()
