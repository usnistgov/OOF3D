# -*- python -*-
# $RCSfile: memorycheck.py,v $
# $Revision: 1.1.2.8 $
# $Author: langer $
# $Date: 2014/11/07 20:28:05 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Define a decorator so that all test methods check that
# Microstructure, Skeleton, and Mesh objects are deallocated properly,
# and that all Workers are destroyed.  These tests have to be done
# after the Microstructure is deleted, but they can't be put in the
# tearDown method because UnitTest.assertXXXX doesn't work there.  The
# tearDown operations are done here, instead.

import sys
import gc

def check(*_microstructures):
    def decorator(func):
        def checktest(self, *args, **kwargs):
            # Run the test function.
            val = func(self, *args, **kwargs)
            # After running the function, delete the microstructures.
            from ooflib.common.IO.mainmenu import OOF
            for msname in _microstructures:
                OOF.Microstructure.Delete(microstructure=msname)
            # Exceptions can hold references to data.  Since this file
            # tests for exceptions as well as memory leaks, it's
            # important to clear the exception state before checking
            # for leaks.
            sys.exc_clear()
            gc.collect()

            from ooflib.common.worker import allWorkers, allWorkerCores
            from ooflib.common.IO import whoville
            from ooflib.SWIG.common import config
            from ooflib.SWIG.common import cmicrostructure
            from ooflib.SWIG.common import threadstate
            if config.dimension() == 2:
                from ooflib.SWIG.engine.cskeleton import get_globalNodeCount
                from ooflib.SWIG.engine.cskeleton import get_globalElementCount
            else:
                from ooflib.SWIG.engine.cskeletonnode2 import get_globalNodeCount
                from ooflib.SWIG.engine.cskeletonface import get_globalFaceCount, get_globalOrientedFaceCount
                from ooflib.SWIG.engine.cskeletonelement import get_globalElementCount
                from ooflib.SWIG.engine.cskeletonselectable import getTrackerCount
            from ooflib.SWIG.engine import csubproblem
            from ooflib.SWIG.engine import femesh
            from ooflib.SWIG.engine import linearizedsystem
            from ooflib.SWIG.engine import sparsemat

            self.assertEqual(whoville.getClass("Microstructure").nActual(), 0)
            self.assertEqual(whoville.getClass("Image").nActual(), 0)
            self.assertEqual(whoville.getClass("Skeleton").nActual(), 0)
            self.assertEqual(whoville.getClass("Mesh").nActual(), 0)
            self.assertEqual(whoville.getClass("SubProblem").nActual(), 0)
            self.assertEqual(linearizedsystem.get_globalLinSysCount(),0)
            self.assertEqual(cmicrostructure.get_globalMicrostructureCount(), 0)
            self.assertEqual(get_globalNodeCount(), 0) # skeleton nodes
            self.assertEqual(get_globalFaceCount(), 0) # skeleton faces
            self.assertEqual(get_globalOrientedFaceCount(), 0)
            self.assertEqual(get_globalElementCount(), 0) # skeleton elements
            self.assertEqual(femesh.get_globalFEMeshCount(), 0)
            self.assertEqual(csubproblem.get_globalCSubProblemCount(), 0)
            self.assertEqual(getTrackerCount(), 0)
            self.assertEqual(sparsemat.nSparseMatCores(), 0)
            self.assertEqual(len(allWorkers), 0)
            ## TODO 3.1: For some reason, on some systems there is
            ## occasionally a leftover WorkerCore when this check is
            ## run.  It doesn't seem to have any references,
            ## though... Since there are no extra ThreadStates, we're
            ## ignoring the leftover WorkerCore for now.
#             if len(allWorkerCores) > 0:
#                 from ooflib.common import debug
#                 debug.set_debug_mode()
#                 print >> sys.stderr, "Referrers for", allWorkerCores.keys()[0],\
#                     "id=", id(allWorkerCores.keys()[0])
#                 debug.dumpReferrers(allWorkerCores.keys()[0], 2)
#             self.assertEqual(len(allWorkerCores), 0)

            # The main thread still exists, but all subthreads should
            # have finished.
            self.assertEqual(threadstate.nThreadStates(), 1)
            print >> sys.stderr, "Memory leak check passed."
            return val
        return checktest
    return decorator

