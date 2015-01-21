# -*- python -*-
# $RCSfile: parallelmainmenu.py,v $
# $Revision: 1.16.18.1 $
# $Author: langer $
# $Date: 2014/09/27 22:34:02 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 
import sys
from ooflib.common import debug
from ooflib.common import parallel_performance
from ooflib.common import quit
from ooflib.common.IO import parameter
from ooflib.common.IO import binarydata
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import socket2me
from ooflib.SWIG.common import mpitools


_rank = mpitools.Rank()
_size = mpitools.Size()
## Two main menus are created here, a public one and a secret one:


## --OOF.Windows.Parallel holds all the parallel menu items that the user can
## apply for his/her convenience. OOF.Parallel can call internally
## any OOF.Windows.


## --OOF.LoadData.IPC hosts all the Inter Processor Communication menu items
## which are used by the developer to coordinate interprocessor actions



## OOF.Windows.Parallel Menu
menusystem = mainmenu.OOF.Windows.addItem(oofmenu.OOFMenuItem('Parallel', secret=0, no_log=0))

## OOF.LoadData.IPC Menu
ipcmenu = mainmenu.OOF.LoadData.addItem(oofmenu.OOFMenuItem('IPC', secret=1, no_log=1))

## Add the MenuKey and ObjKey menus to keep the parser happy
ipcmenu.addItem(oofmenu.OOFMenuItem('MenuKey', callback = binarydata.menuKeyCB, secret=1, params=[parameter.StringParameter('path'), parameter.IntParameter('key')] ))
ipcmenu.addItem(oofmenu.OOFMenuItem('ObjKey', callback = binarydata.objectKeyCB, secret=1, params=[parameter.StringParameter('obj'), parameter.IntParameter('key')] ))


## OOF.LoadData.IPC.Quit
## Quit should never ever be run on a separate thread.
def _quit(menuitem):
    global _rank
    if _rank != 0:
##        print "quitting back-end"
##        sys.stdout.flush()
        debug.fmsg()
        quit.quit()
ipcmenu.addItem(oofmenu.OOFMenuItem('Quit', callback = _quit, secret=1, threadable = oofmenu.PARALLEL_UNTHREADABLE ))







## OOF.Windows.Parallel.ProfilePerformance
## ProfilePerformance estimates the communication cost between all processors,
## as well as the processing cost in each processors
## These quantities are used to distribute the load among processors when the
## microstructure is divided into subsections.
##
## The cost is saved inside virtualMachine object, which lives in the front
## end and knows the performance of each processor.

## OOF.LoadData.IPC.SetComputationPerformance
def _computation_cost(menuitem):
    debug.fmsg()
    parallel_performance.set_performance_cost()
    ## makes a crude estimate of the processing and memory speed
    mpitools.mpi_barrier()
ipcmenu.addItem(oofmenu.OOFMenuItem('SetComputationPerformance', callback = _computation_cost, secret=1, no_log=1, threadable = oofmenu.PARALLEL_THREADABLE ))

## OOF.LoadData.IPC.SetCommunicationPerformance
def _communication_cost(menuitem, processor_number):
    debug.fmsg()
    parallel_performance.set_communication_cost(processor_number)
    ## makes a crude estimate of the inherent communication latency
ipcmenu.addItem(oofmenu.OOFMenuItem('SetCommunicationPerformance', callback = _communication_cost, secret=1, no_log=1, threadable = oofmenu.PARALLEL_THREADABLE, params=[parameter.IntParameter('processor_number')] ))

## OOF.LoadData.IPC.GetComputationPerformance
def _get_computation_cost(menuitem, processor_number): 
    return parallel_performance.virtualMachineParameters.get_computation_cost(processor_number)
ipcmenu.addItem(oofmenu.OOFMenuItem('GetComputationPerformance', callback = _get_computation_cost, secret=1, no_log=1, threadable = oofmenu.PARALLEL_THREADABLE, params=[parameter.IntParameter('processor_number')] ))

## OOF.LoadData.IPC.GetCommunicationPerformance
def _get_communication_cost(menuitem, processor_number):
    parallel_performance.virtualMachineParameters.get_communication_cost(processor_number)
ipcmenu.addItem(oofmenu.OOFMenuItem('GetCommunicationPerformance', callback = _get_communication_cost, secret=1, no_log=1, threadable = oofmenu.PARALLEL_THREADABLE, params=[parameter.IntParameter('processor_number')] ))

## This callback summarizes all the internal (IPC) callbacks into a public menuitem (OOF.Windows.ProfilePerformance)
def _profile_performance(menuitem):
## _profile_performance sets and asks all the machines for its
## computation and communication costs. Aterwards, establishes the 
## work load weights. These weights are used by the front-end to distribute
## sub-skeletons, sub-meshes, etc., to the back-end.
    global _size
    ipcmenu.SetComputationPerformance()
    ## debug.fmsg ("finished estimating computation performance")
    ## estimates the speed of the machines
    for p_number in range(_size):
        ipcmenu.SetCommunicationPerformance(processor_number = p_number)
        ## debug.fmsg(socket2me.socketPort.getData(p_number))
        ## estimates communication latency
    ## debug.fmsg("finished estimating communication latency")
    for p_number in range(_size):
        ipcmenu.GetComputationPerformance(processor_number = p_number)
    ## debug.fmsg("finished grabbing computation speed")
    for p_number in range(_size):
        ipcmenu.GetCommunicationPerformance(processor_number = p_number)
    ## debug.fmsg("finished grabbing latency dictionary")
    parallel_performance.virtualMachineParameters.setRelativeLoad()
    ## debug.fmsg("finished setting relative loads")

menusystem.addItem(oofmenu.OOFMenuItem('ProfilePerformance', callback = _profile_performance, secret=0, no_log=0, threadable = oofmenu.THREADABLE))

## TODO LATER: Create graphic window to set the processor relative loads
