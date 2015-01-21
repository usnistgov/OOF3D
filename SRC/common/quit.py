# -*- python -*-
# $RCSfile: quit.py,v $
# $Revision: 1.46.2.5 $
# $Author: langer $
# $Date: 2014/10/09 02:50:29 $


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 


from ooflib.SWIG.common import lock
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common import threadstate
from ooflib.common import debug
from ooflib.common import excepthook
from ooflib.common import mainthread
from ooflib.common import parallel_enable
from ooflib.common import subthread
from ooflib.common import threadmanager
from ooflib.common import utils
from ooflib.common.IO import mainmenu
import gc                       # debugging
import sys

def quit(*args, **kwargs):
    # Called in text mode only, and on the main thread.  In GUI mode,
    # use common.IO.GUI.quit.quit instead.  *args allows this to be
    # used as a menu callback.
    exitstatus = kwargs.get('exitstatus', 0)
    if mainmenu.OOF.logChanged() and not quiet():
        answer = utils.OOFeval('raw_input("*Save log file? [Yn]: ")')
        if answer in ('','Y','y','yes','Yes', 'YES'):  # Oh, yes!
            mainmenu.OOF.File.Save.Python_Log()
            mainmenu.cleanlog()
    cleanup(shutdown, exitstatus)          # doesn't return!

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Other parts of the code can call atShutDown() to specify a function
# to be called before quitting.

_cleanUpActions = []

def atShutDown(fn):
    _cleanUpActions.append(fn)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

def cleanup(shutdownfn, exitstatus):
    # Turn off logging, so that window closing, etc. won't be logged.
    mainmenu.OOF.haltLog()
    
    for fn in _cleanUpActions:
        fn()

    if parallel_enable.enabled():
        try:
            from ooflib.SWIG.common import mpitools
            if mpitools.Rank() == 0:
                # tell back-end to start quit process
                mainmenu.OOF.LoadData.IPC.Quit()
        except ImportError:
            pass
    
    # Wait on a subthread for threads to finish, then call shutdownfn
    # on the main thread.  When called from the GUI callback for the
    # Quit command, shutdownfn is common.IO.GUI.quit.shutdown.
    subthread.execute_immortal(waitForThreads, (shutdownfn, exitstatus))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

def waitForThreads(shutdownfn, exitstatus):
    switchboard.notify("shutdown")
    subthread.miniThreadManager.quit()
    threadmanager.threadManager.quit()
    mainthread.run(shutdownfn, (exitstatus,))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

def shutdown(exitstatus):
    # In GUI mode, this is called after the GUI exits.

    # Restore the default exception handler, in case something goes
    # wrong during shutdown, and the machinery to display OOF
    # exceptions has already been dismantled.  This call must come
    # before mainthread_delete().
    excepthook.assign_excepthook()

    # On some systems (at least OS X 10.5.7) it's important to delete
    # the main thread's ThreadState object explicitly before calling
    # sys.exit().  If called implicitly by sys.exit, the ThreadState
    # destructor crashes.  This must come after the GUI has been
    # stopped, or else subthreads used in stopping the GUI will fail.
    threadstate.mainthread_delete()

    ## gc.garbage is a list of objects which couldn't be deleted,
    ## because they have circular references *and* __del__ methods.
    ## Python can't use garbage collection on such objects because it
    ## doesn't know the order in which to call the __del__ methods.
    if gc.garbage:
        debug.fmsg("garbage=", gc.garbage)
        # for g in gc.garbage:
        #     from ooflib.SWIG.common import doublevec
        #     if isinstance(g, doublevec.DoubleVecPtr):
        #         debug.dumpReferrers(g, levels=2)

    sys.stdout.flush()
    sys.exit(exitstatus)

    # If additional actions are required, call them
    # explicitly. Switchboard calls are unreliable here.

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

_quiet = 0

def quiet():
    return _quiet

def set_quiet():
    global _quiet
    _quiet = 1
