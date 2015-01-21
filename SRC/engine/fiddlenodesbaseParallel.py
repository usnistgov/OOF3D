# -*- python -*-
# $RCSfile: fiddlenodesbaseParallel.py,v $
# $Revision: 1.44.2.2 $
# $Author: langer $
# $Date: 2014/09/27 22:34:18 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

## TODO 3.1: This file has not been updated to use new (April 2009)
## Progress objects.

from ooflib.SWIG.common import mpitools
from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import primitives
from ooflib.common import registeredclass
from ooflib.common import utils
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import reporter

from ooflib.SWIG.engine import cfiddlenodesbaseParallel
from ooflib.engine import  skeletoncontext
from ooflib.engine import deputy
from ooflib.engine import skeletonmodifier
from ooflib.engine.IO import skeletonIPC
from ooflib.engine.IO import skeletonmenu

import math
import random
import string
import sys
import time

cfiddler = cfiddlenodesbaseParallel
_rank = mpitools.Rank()
_size = mpitools.Size()


def _apply(self, oldskeleton, context):
    if _rank == 0:
        pBar = progressbar.getProgress()
        pBar.set_message(self.intro)
    return oldskeleton.deputyCopy()

def _postProcess(self, context):
    if _rank == 0:
        pBar = progressbar.getProgress()
        pBar.set_message(self.header)

    skeleton = context.getObject()
    before = mpitools.Allreduce_DoubleSum(
        skeleton.energyTotal(self.criterion.alpha))

    if _rank == 0:
        if self.pbar_type == "continuous":
            n = self.iteration.iterations

    self.count = 0
    while self.iteration.goodToGo():
        self.count += 1
        # the context to acquires the writing persmissions
        # inside coreProcess.
        
        mpitools.Barrier()
        self.coreProcess_parallel(context)
        self.updateIteration_parallel()

        if _rank == 0:
            if pBar.query_stop():
                pBar.set_failure()
                pBar.set_message("Failed")
                # Sending a break signal
                mpitools.Isend_Bool(False, range(1,_size))
                break
            else:
                if self.pbar_type == "continuous":
                    pBar.set_progress(1.0*self.count/n)
                    # does this ever get displayed?
                    pBar.set_message("%s%d/%d"
                                 % (self.header, self.count, n))
                    # Sending a continue signal
                    mpitools.Isend_Bool(True, range(1,_size))
        else:
            if not mpitools.Recv_Bool(0):
                break

    switchboard.notify("skeleton nodes moved", context)

    if _rank == 0:
        if pBar.query_stop():  # or pBar.get_success() <0:
            pBar.set_failure()
            pBar.set_message("Failed")
            mpitools.Isend_Bool(False, range(1,_size))
            return
        else:
            mpitools.Isend_Bool(True, range(1,_size))
    else:
        if not mpitools.Recv_Bool(0):
            return

    mpitools.Barrier()
    after = mpitools.Allreduce_DoubleSum(
        skeleton.energyTotal(self.criterion.alpha))

    # Reporting to the message window
    if _rank == 0:
        if before:
            rate = 100.0*(before-after)/before
        else:
            rate = 0.0
        diffE = after - before
        reporter.report("%s deltaE = %10.4e (%6.3f%%)"
                        % (self.outro, diffE, rate))

#################################################################

##def _coreProcess(self, context):
##    global _rank
    
##    fiddler = FiddleNodesParallel(context,
##                                  self.criterion,
##                                  self.targets,
##                                  self.T,
##                                  self.movedPosition)
    
##    context.begin_writing()
##    try:
##        fiddler.play()
##        # Information for upate
##        self.deltaE = fiddler.deltaE
##        self.totalE = fiddler.totalE
##        self.nok = fiddler.nok
##        self.nbad = fiddler.nbad
##    finally:
##        context.end_writing()
##        if _rank == 0:
##            switchboard.notify("redraw")

#################################################################

def _annealCoreProcess(self, context):
    fiddler = AnnealParallel(context,
                             self.criterion,
                             self.targets,
                             self.T,
                             self.movedPosition)
    _commonCoreProcess(self, context, fiddler)

def _smoothCoreProcess(self, context):
    fiddler = SmoothParallel(context,
                             self.criterion,
                             self.targets,
                             self.T,
                             self.movedPosition)
    _commonCoreProcess(self, context, fiddler)

def _snapCoreProcess(self, context):
    fiddler = SnapParallel(context,
                           self.criterion,
                           self.targets,
                           self.T,  #trivial
                           self.movedPosition)
    _commonCoreProcess(self, context, fiddler)

def _commonCoreProcess(method, context, fiddler):
    global _rank
    context.begin_writing()
    try:
        fiddler.play()
        # Information for upate
        method.deltaE = fiddler.deltaE
        method.totalE = fiddler.totalE
        method.nok = fiddler.nok
        method.nbad = fiddler.nbad
    finally:
        context.end_writing()
        if _rank == 0:
            switchboard.notify("redraw")

#################################################################

def _updateIteration(self):
    deltaE = mpitools.Allreduce_DoubleSum(self.deltaE)
    totalE = mpitools.Allreduce_DoubleSum(self.totalE)
    nok = mpitools.Allreduce_IntSum(self.nok)
    nbad = mpitools.Allreduce_IntSum(self.nbad)
    if nok+nbad > 0:
        self.iteration.update(deltaE, totalE,
                              (1.0*nok)/(nok+nbad),
                              self.count)
    else:
        self.iteration.update(None, None, None, self.count)
        
# Custom debug message function with message ID
report_id = 0
def REPORT(*args):
    global _rank
    global report_id
    report_id += 1
    values =["###"]+[_rank]+["("]+[report_id]+[")"]+[":"]+list(args)
    print string.join(map(str, values), ' ')
    sys.stdout.flush()

#################################################################

# Now the schedule
class Scheduler:
    def __init__(self, nnodes, allnodes, allshared, fiddler):
        global _size
        self.nnodes = nnodes
        self.allnodes = allnodes
        self.allshared = allshared
        self.fiddler = fiddler
        
        self.works = [[] for i in range(_size)]
        self.pointers = [0]*_size  # Current node (list) index
        self.completed = [False]*_size  # Current work size

    def done(self, i):
        return self.pointers[i] == self.nnodes[i]

    def completedTurn(self, i):
        return self.completed[i]

    def completedTurns(self, ii):  # True, if any.
        for i in ii:
            if self.completedTurn(i):
                return True
        return False

    def __call__(self, rank):
        global _rank
        global _size
        while self.pointers != self.nnodes:
            for i in range(_size):
                if self.done(i) or self.completedTurn(i):
                    continue
                # Add something to the queue
                node = self.allnodes[i][self.pointers[i]]
                shared = self.allshared[i][self.pointers[i]]
                # Shared or not
                if shared:
                    # Do the share-holders first
                    if self.completedTurns(shared):
                        # If any of shared holders finished its turn,
                        # the node should be done in the later turn.
                        continue
                    for s in shared:  # passive work
                        self.works[s].append((self.fiddler.passiveProcess, i))
                        self.completed[s] = True
                    self.works[i].append((self.fiddler.activeProcess, node))
                else:
                    self.works[i].append((self.fiddler.soloProcess, node))
                self.completed[i] = True
                self.pointers[i] += 1
            # Filling the void
            for i in range(_size):
                if not self.completedTurn(i):
                    self.works[i].append(None)
            self.completed = [False]*_size
        return self.works[rank]

#################################################################

# FiddleNodesParallel class will do the majority of fiddling
class FiddleNodesParallel:
    def __init__(self, context, criterion, targets, T, mover):
        self.context = context
        self.skeleton = context.getObject()
        self.criterion = criterion
        self.targets = targets
        self.T = T
        self.mover = mover

        self.alpha = criterion.alpha
        self.totalE = self.skeleton.energyTotal(self.alpha)  # initial E
        self.deltaE = 0.  # improvement
        self.nok = 0  # successful ones
        self.nbad = 0  # unsuccessful ones

        # Data communication
        self.move_channel = 1
        self.illegal_channel = 2
        self.report_channel = 3
        self.verdict_channel = 4

        # Initialize MPI datatype for communication
        cfiddler.tuneFiddle()
        
    def ownNode(self, node):
        global _rank
        return _rank == node.master()
    
    def passiveProcess(self, stopper):
        self.mover.passive(self.skeleton, stopper)  # Non-trivial for Smooth
        moveData = cfiddler.Recv_MoveData(stopper, tag=self.move_channel)
        node = self.skeleton.getNodeWithIndex(moveData.index)
##        REPORT("HELPING", stopper, "FOR NODE #", node.remoteIndex(stopper))
        
        # recording energy-before (should this use periodic neighbor Elements?)
        neighbors = node.aperiodicNeighborElements(self.skeleton)
        reportData = [el.energyHomogeneity(self.skeleton) for el in neighbors]
        reportData += [el.energyShape() for el in neighbors]
        # move to the position -- self.skeleton is a DeputySkeleton
        self.skeleton.moveNodeTo(
            node, primitives.Point(moveData.x, moveData.y))
        # Check & send illegality
        mpitools.Send_Bool(bool(node.illegal()),
                           stopper,
                           tag=self.illegal_channel)

        # if illegal in any processes, it should be aborted
        if mpitools.Recv_Bool(
            stopper, tag=self.verdict_channel):  # True:continue, False:abort
            # recording energy-after
            reportData += [el.energyHomogeneity(self.skeleton)
                            for el in neighbors]
            reportData += [el.energyShape() for el in neighbors]
            # reporting
            mpitools.Send_DoubleVec(reportData,
                                    stopper,
                                    tag=self.report_channel)
            # receiving verdivt, True:stay, False:move back
            if not mpitools.Recv_Bool(stopper, self.verdict_channel):
                self.skeleton.moveNodeBack(node)
        else:  # Illegal!
            self.skeleton.moveNodeBack(node)
##        REPORT("DONE HELPING", moveData.master, " ON NODE #",
##               node.remoteIndex(moveData.master))
        
    def activeProcess(self, index):
        node = self.skeleton.getNodeWithIndex(index)
        
        change = deputy.DeputyProvisionalChanges()
        move_to = self.mover(self.skeleton, node)
        change.moveNode(node,
                        move_to,
                        self.skeleton)  # moved the node

        # Building data to be sent to sharers.
        shared = node.sharedWith()
        nodeMoves = []
        for s in shared:
            nodeMoves.append(
                cfiddler.create_movedata(
                _rank,  # master process
                node.remoteIndex(s),  # remote index
                move_to.x,  # x
                move_to.y   # y
                ))
        # Sending move data to shared processes
        cfiddler.Isend_MoveData(nodeMoves, shared,
                                tag=self.move_channel)
##        REPORT("STARTED WORKING ON NODE #", index, "WITH", shared)
        # receiving illegality from shared processes
        illegal = mpitools.Irecv_Bools(shared,
                                       tag=self.illegal_channel)
        if True in illegal or change.illegal(self.skeleton):
            self.moveBack(node)
            return
        else:  # continue
            mpitools.Isend_Bool(True, shared, tag=self.verdict_channel)

        # Receiving report from shared processes
        reports = mpitools.Irecv_DoubleVecs(shared, tag=self.report_channel)

        homog0 = []
        shape0 = []
        homog1 = []
        shape1 = []
        for r in reports:
            n = len(r)/4
            homog0 += r[:n]
            shape0 += r[n:2*n]
            homog1 += r[2*n:3*n]
            shape1 += r[3*n:4*n]
        change.augmentData(homog0, homog1, shape0, shape1)

        # Now, the decision time
        bestchange = self.criterion([change], self.skeleton)
        if bestchange is not None:
            self.stay(node, bestchange)
        elif self.T > 0. and not self.criterion.hopeless():
            diffE = change.deltaE(self.skeleton, self.alpha)
            if math.exp(-diffE/self.T) > random.random():
                self.stay(node, change)
            else:
                self.moveBack(node)
        else:
            self.moveBack(node)
##        REPORT("DONE WORKING ON NODE #", index, "WITH", shared)
        
    def stay(self, node, change):
        self.nok += 1
        self.deltaE += change.deltaE(self.skeleton, self.alpha)
        change.accept(self.skeleton)
        if node.isShared():
            mpitools.Isend_Bool(True, node.sharedWith(),
                                tag=self.verdict_channel)

    def moveBack(self, node):
        self.nbad += 1
        if node.isShared():
            mpitools.Isend_Bool(False, node.sharedWith(),
                                tag=self.verdict_channel)

    def soloProcess(self, index):
##        REPORT("WORKING SOLO ON NODE #", index)
        node = self.skeleton.getNodeWithIndex(index)
        change = deputy.DeputyProvisionalChanges()
        change.moveNode(node,
                        self.mover(self.skeleton, node),
                        self.skeleton)  # moved
        # Now, the decision time
        bestchange = self.criterion([change], self.skeleton)
        if bestchange is not None:
            self.stay(node, bestchange)
        elif self.T > 0. and not self.criterion.hopeless():
            diffE = change.deltaE(self.skeleton, self.alpha)
            if math.exp(-diffE/self.T) > random.random():
                self.stay(node, change)
            else:
                self.moveBack(node)
        else:
            self.moveBack(node)
##        REPORT("DONE SOLO ON NODE #", index)

    def createWorkOrder(self, activeNodes):
        global _rank
        global _size
        
        # First the data collection
        nnodes = mpitools.Allgather_Int(len(activeNodes))
        allnodes = mpitools.Allgather_IntVec(
            [n.getIndex() for n in activeNodes], size_known=nnodes)
        allsignatures = mpitools.Allgather_IntVec(
            [n.nshared() for n in activeNodes], size_known=nnodes)
        nshared = [reduce(lambda x,y: x+y, s) for s in allsignatures]
        myshared = [n.sharedWith() for n in activeNodes]
        myshared = reduce(lambda x,y: x+y, myshared)
        allshared = mpitools.Allgather_IntVec(myshared,
                                              size_known=nshared)
            
        def listrize(list, signature):
            nsig = len(signature)
            count = 0
            output = [[] for i in range(nsig)]
            for i in range(nsig):
                for j in range(signature[i]):
                    output[i].append(list[count])
                    count += 1
            return output

        for i in range(len(allshared)):
            allshared[i] = listrize(allshared[i], allsignatures[i])

        scheduler = Scheduler(nnodes, allnodes, allshared, self)
        self.mywork = scheduler(_rank)
            
    def play(self):
        global _rank
        global _size
        
        # Get the nodes & shuffle them
        activeNodes = self.targets(self.context)
        activeNodes = filter(self.ownNode, activeNodes)
        random.shuffle(activeNodes)

        self.createWorkOrder(activeNodes)
        mpitools.Barrier()

        for work in self.mywork:
            if work is not None:  # work = (callback function, arguments)
                work[0](work[1])
        mpitools.Barrier()

        skeletonIPC.collect_pieces(self.skeleton)
        self.skeleton.timestamp.increment()

#################################################################

class AnnealParallel(FiddleNodesParallel):    
    pass

#################################################################

class SmoothParallel(FiddleNodesParallel):    
    pass

#################################################################

class SnapParallel(FiddleNodesParallel):
    def passiveProcess(self, stopper):
        # the node to move
        myindex = mpitools.Recv_Int(stopper, tag=self.move_channel)
        node = self.skeleton.getNodeWithIndex(myindex)
        self.mover.passive(self.skeleton, node, stopper)

        # getting no. of move candidates
        nmoves = mpitools.Recv_Int(stopper, tag=self.move_channel)

        for i in range(nmoves):
            moveData = cfiddler.Recv_MoveData(stopper, tag=self.move_channel)
##            REPORT("HELPING", stopper, "FOR NODE #", node.remoteIndex(stopper))

            # recording energy-before
            neighbors = node.aperiodicNeighborElements(self.skeleton)
            reportData = [el.energyHomogeneity(self.skeleton) for el in neighbors]
            reportData += [el.energyShape() for el in neighbors]
            # move to the position -- self.skeleton is a DeputySkeleton
            self.skeleton.moveNodeTo(
                node, primitives.Point(moveData.x, moveData.y))
            # Check & send illegality
            mpitools.Send_Bool(bool(node.illegal()),
                               stopper,
                               tag=self.illegal_channel)

            # if illegal in any processes, it should be aborted
            if mpitools.Recv_Bool(
                stopper, tag=self.verdict_channel):  # True:continue, False:abort
                # recording energy-after
                reportData += [el.energyHomogeneity(self.skeleton)
                                for el in neighbors]
                reportData += [el.energyShape() for el in neighbors]
                # reporting
                mpitools.Send_DoubleVec(reportData,
                                        stopper,
                                        tag=self.report_channel)
            # reset for the next one
            self.skeleton.moveNodeBack(node)
##            REPORT("DONE HELPING", moveData.master, " ON NODE #",
##                   node.remoteIndex(moveData.master))

        # receiving verdivt, True:stay, False:move back
        if mpitools.Recv_Bool(stopper, self.verdict_channel):
            x, y = mpitools.Recv_DoubleVec(stopper,
                                           tag=self.move_channel,
                                           size=2)
            self.skeleton.moveNodeTo(node, primitives.Point(x, y))
    
    def activeProcess(self, index):
        node = self.skeleton.getNodeWithIndex(index)
        shared = node.sharedWith()
        # send the node (remote) index
        for s in shared:
            mpitools.Send_Int(node.remoteIndex(s), s, self.move_channel)
        
        move_candidates = self.mover.active(self.skeleton, node)
        mpitools.Isend_Int(len(move_candidates), shared, tag=self.move_channel)

        changes = []
        for mc in move_candidates:
            change = deputy.DeputyProvisionalChanges()
            change.moveNode(node, mc, self.skeleton)  # moved the node

            # Building data to be sent to sharers.
            nodeMoves = []
            for s in shared:
                nodeMoves.append(
                    cfiddler.create_movedata(
                    _rank,  # master process
                    node.remoteIndex(s),  # remote index
                    mc.x,  # x
                    mc.y   # y
                    ))
            # Sending move data to shared processes
            cfiddler.Isend_MoveData(nodeMoves, shared,
                                    tag=self.move_channel)
            
##            REPORT("STARTED WORKING ON NODE #", index, "WITH", shared)
            # receiving illegality from shared processes
            illegal = mpitools.Irecv_Bools(shared,
                                           tag=self.illegal_channel)
            legal = True not in illegal and not change.illegal(self.skeleton)
            mpitools.Isend_Bool(legal, shared, tag=self.verdict_channel)
            if not legal:
                continue
            
            # Receiving report from shared processes
            reports = mpitools.Irecv_DoubleVecs(shared, tag=self.report_channel)
            homog0 = []
            shape0 = []
            homog1 = []
            shape1 = []
            for r in reports:
                n = len(r)/4
                homog0 += r[:n]
                shape0 += r[n:2*n]
                homog1 += r[2*n:3*n]
                shape1 += r[3*n:4*n]
            change.augmentData(homog0, homog1, shape0, shape1)
            changes.append(change)

        # Now, the decision time
        bestchange = self.criterion(changes, self.skeleton)
        if bestchange is not None:
            self.nok += 1
            self.deltaE += bestchange.deltaE(self.skeleton, self.alpha)
            bestchange.accept(self.skeleton)
            mpitools.Isend_Bool(True, shared, tag=self.verdict_channel)
            theindex = changes.index(bestchange)
            x = move_candidates[theindex].x
            y = move_candidates[theindex].y
            mpitools.Isend_DoubleVec([x, y], shared, tag=self.move_channel, size=2)
        else:
            self.nbad += 1
            mpitools.Isend_Bool(False, shared, tag=self.verdict_channel)
##        REPORT("DONE WORKING ON NODE #", index, "WITH", shared)

    def soloProcess(self, index):
##        REPORT("WORKING SOLO ON NODE #", index)
        node = self.skeleton.getNodeWithIndex(index)
        move_candidates = self.mover(self.skeleton, node)  # list of points
        move_candidates = [mc for mc in move_candidates if mc]  # removes "None"
        changes = []

        for mc in move_candidates:
            change = deputy.DeputyProvisionalChanges()
            change.moveNode(node, mc, self.skeleton)  # moved the node
            changes.append(change)

        # Now, the decision time
        bestchange = self.criterion(changes, self.skeleton)
        if bestchange is not None:
            self.nok += 1
            self.deltaE += bestchange.deltaE(self.skeleton, self.alpha)
            bestchange.accept(self.skeleton)
        else:
            self.nbad += 1
##        REPORT("DONE SOLO ON NODE #", index)
