# -*- python -*-
# $RCSfile: solvermenuIPC.py,v $
# $Revision: 1.5.10.1 $
# $Author: langer $
# $Date: 2014/09/27 22:34:20 $

OBSOLETE

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.common.IO import parallelmainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import whoville
from ooflib.SWIG.engine import solverdriver
from ooflib.engine import timedrivers
import ooflib.engine.mesh

## OOF.LoadData.IPC.Solver
ipcsolvermenu = parallelmainmenu.ipcmenu.addItem(
    oofmenu.OOFMenuItem('Solver', secret=1, no_log=1)
    )

def parallel_solve(menuitem, subproblem, solver):
    from ooflib.common import debug
    debug.fmsg()
    subpcontext = ooflib.engine.subproblemcontext.subproblems[subproblem]
    subpcontext.reserve()
    timedriver = timedrivers.Null()
    try:
        try:
            # null timedriver.apply just calls solverdriver.apply
            timedriver.apply(solver, subpcontext)
        except ooferror.ErrProcessAborted:
            pass
        ## solved flag is set even if solution did NOT
        ## converge in order to show how far the solution
        ## went.
        subpcontext.solved()

    finally:
        subpcontext.cancel_reservation()


## OOF.LoadData.IPC.Solver.Solve
ipcsolvermenu.addItem(oofmenu.OOFMenuItem(
    'Solve',
    callback = parallel_solve,
    threadable = oofmenu.PARALLEL_THREADABLE,
    params =
    [
##    whoville.WhoParameter('subproblem',
##                          ooflib.engine.subproblemcontext.subproblems,
##                          tip=parameter.emptyTipString),
    parameter.StringParameter('subproblem'),
##    whoville.WhoParameter('mesh',
##                          ooflib.engine.mesh.meshes,
##                          tip="Deprecated.  Use subproblem instead."),
    parameter.RegisteredParameter('solver', solverdriver.Driver,
                                  tip=parameter.emptyTipString)
    ]
    ))
