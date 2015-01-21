# -*- python -*-
# $RCSfile: excepthook.py,v $
# $Revision: 1.12.2.2 $
# $Author: fyc $
# $Date: 2014/07/21 18:08:27 $


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# A module for managing the Python exception hook.  sys.excepthook is
# called when an exception is not caught by the program.  Here we
# replace it by a function that calls a thread-specific exception
# handler.  The handler is manipulated by assign_excepthook and
# remove_excepthook, which keep a stack of excepthooks for each
# thread.  assign_excepthook(handler) pushes a handler onto the stack.
# remove_excepthook(handler) removes the given handler and any others
# that may have been pushed after the argument was pushed.

from ooflib.SWIG.common import lock
from ooflib.SWIG.common import ooferror
from ooflib.common import debug
import sys, traceback

def printTraceBack(e_type, e_value, tblist):
    from ooflib.common.IO import reporter # avoid import loop
    for line in traceback.format_exception_only(e_type, e_value):
        reporter.error(line.rstrip())
    if isinstance(e_value, ooferror.ErrErrorPtr):
        moreinfo = e_value.details()
        if moreinfo:
            reporter.error(moreinfo)
    if tblist:
        for line in traceback.format_list(tblist):
            reporter.error(line.rstrip())

# displayTraceBack is overridden by reporter_GUI.py, so that in GUI mode
# it brings up a pop-up window.
displayTraceBack = printTraceBack

# OOFexceptHook is a class with a __call__ method instead of a simple
# function so that the getTraceBackList method can be overridden in
# derived classes.  See scriptloader.py.

class OOFexceptHook(object):
    def getTraceBackList(self, tback): # may be redefined in derived classes
        return traceback.extract_tb(tback)
    def __call__(self, e_type, e_value, tback):
        tblist = self.getTraceBackList(tback)
        displayTraceBack(e_type, e_value, tblist)
        # Now that we've handled the exception, clear it.  The system's
        # exception data keeps a reference to the local dictionary of the
        # frame in which the exception occurred, and this can prevent
        # garbage collection.  TODO OPT: One can imagine circumstances in
        # which this isn't the right thing to do, but those circumstances
        # should probably assign a new excepthook function.
        sys.exc_clear()
    def __cmp__(self, other):
        return cmp(id(self), id(other))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

from ooflib.SWIG.common import threadstate
_exceptStacks = {}
_exceptLock = lock.SLock()

def assign_excepthook(newhook=sys.__excepthook__):
#     debug.fmsg("adding hook", id(newhook))
    _exceptLock.acquire()
    threadno = threadstate.findThreadNumber()
    try:
        hookstack = _exceptStacks[threadno]
    except KeyError:
        hookstack = _exceptStacks[threadno] = []
    hookstack.append(newhook)
    _exceptLock.release()
    return newhook

# remove_excepthook() and get_excepthook() are called during exception
# handling, and need to be careful not to raise an exception
# themselves.  Therefore they can't use try/except at all.

def remove_excepthook(hook):
    _exceptLock.acquire()
    threadno = threadstate.findThreadNumber()

#     hookstack = _exceptStacks[threadno]
# #     debug.fmsg("stack=", [id(h) for h in hookstack], "hook=", id(hook))
#     assert hookstack[-1] is hook
#     oldhook = hookstack.pop()
#     if not hookstack:
#         del _exceptStacks[threadno]
## The preceding block of code used to be much more cautious, but the
## caution was inserted when debugging a problem that turned out to be
## elsewhere.  Here's the cautious version, in case returning to the
## incautious version was a mistake:
    oldhook = None
    if threadno in _exceptStacks:
        hookstack = _exceptStacks[threadno]
        if hook in hookstack:
            oldhook = hookstack.pop()
            while oldhook is not hook:
                oldhook = hookstack.pop()
            if not hookstack:
                del _exceptStacks[threadno]

    _exceptLock.release()
    return oldhook

def get_excepthook():
    threadno = threadstate.findThreadNumber()
    if threadno not in _exceptStacks:
        return sys.__excepthook__
    hookstack = _exceptStacks[threadno]
    if hookstack:
        return hookstack[-1]
    return None

def _oofExceptHook(e_type, e_value, tback):
    _exceptLock.acquire()
    hook = get_excepthook()
    _exceptLock.release()
    if hook is not None:
        hook(e_type, e_value, tback)
        # If this function has been called, it means that an exception
        # has not been caught, and therefore that a Worker or
        # MiniThread has finished without removing its excepthook from
        # the stack.  Do it now.
        remove_excepthook(hook)
    else:
        sys.__excepthook__(e_value, e_value, tback)

sys.excepthook = _oofExceptHook

def exceptHookDepth():
    threadno = threadstate.findThreadNumber()
    if threadno not in _exceptStacks:
        return 0
    return len(_exceptStacks[threadno])
