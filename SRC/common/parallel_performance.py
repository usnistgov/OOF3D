# -*- python -*-
# $RCSfile: parallel_performance.py,v $
# $Revision: 1.12.18.1 $
# $Author: langer $
# $Date: 2014/09/27 22:33:54 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

import sys, time
from ooflib.common import debug
from ooflib.common import parallel_enable
from ooflib.common.IO import socket2me
from ooflib.SWIG.common import mpitools

_rank = mpitools.Rank()
_size = mpitools.Size()

class MachinePerformance:
    def __init__(self):
        ## The machine performance is known by the static instance of the
        ## VirtualMachine which makes decisions on how to balance the work load
        self.computational = 0
        ## knows computational time to do a simple operation
        self.memory = 0 ## knows computational time for accessing memory
        self.communication = {}
        ## communication lag is known by pairs
        ## for the i-th processor entries are j:ij-latency
        ## knows computational time for communicating with its neighbors
        self.number_of_iterations = 1000000

    def get_computational(self):
        return self.computational

    def get_communication(self):
        return self.communication
    
    def estimate_computational(self):
        ## initialization

        ## everyone: front-end + back-end
        startTime = time.time()
        for i in range(self.number_of_iterations):
            i = 1
        endTime = time.time()
        self.computational = endTime - startTime
        
        ## post-processing
        return self.computational
    def estimate_communication(self, org):
        ## all machines receive this command
        ## org machine 'talks' to the rest of
        ## the machines and
        ## reports completion to front end.

        
        global _rank
        global _size
        msg = "oofing the world"
        startTime = 0
        if org == _rank:
            for dest in range(_size):
                if dest != _rank:## do not try to talk to yourself
                    startTime = time.time()
                    mpitools.send_string(msg, dest)
                    mpitools.receive_string(dest)
                    endTime = time.time()
                    self.communication[dest] = str(endTime - startTime)
            socket2me.socketWrite("live chickens")
        else:
            msg2 = mpitools.receive_string(org)
            mpitools.send_string(msg2,org) 
        

                    
    def estimate_memory_cost(self):
        ## here, amount of available memory should be estimated
        pass
    

performance = MachinePerformance() ## unique for each machine




def set_performance_cost():
    if parallel_enable.enabled():
        ## initialization
        global performance
        ## everyone: back-end + front-end
        performance.estimate_computational()

def set_communication_cost(pn):
    if parallel_enable.enabled():
        ## back-end + front-end
        performance.estimate_communication(pn)
        
    

class VirtualMachineParameters:
    def __init__(self):
        global _size
        self.size = _size
        
        ## stores a list of machines ranks in an optimized order
        self.computation = {}
        self.fractionPLoad = []
        
        self.latency = {} ## dictionary of latency dictionaries
        self.fractionCLoad = {}

    def get_computation_cost(self, target):
        global _rank
        global  performance
        ## performance is a MachinePerformance object
        ## which  holds the performance parameters if the
        ## target-th processor.
        if _rank == target:
            if target == 0: ## if local data just grab it
                self.computation[target] = performance.get_computational()
                return
            ## if data not local, send it to process zero
            msg = str(performance.get_computational())
            mpitools.send_string(msg, 0)
        if _rank == 0:
            ## process zero waits for data
            self.computation[target] = float(mpitools.receive_string(target))
        
    
    def get_communication_cost(self, target):
        global _rank
        global performance
        if _rank == target:
            if target == 0:
                 self.latency[target] = performance.get_communication()
                 return
            msg = repr(performance.get_communication())
            mpitools.send_string(msg, 0)
        if _rank == 0:
            self.latency[target] = eval(mpitools.receive_string(target))
        
            
    def setRelativeLoad(self):
        ## this function is local to process zero
        ld = 0
        for processor in range(self.size):
            ld += self.computation[processor]
        for processor in range(self.size):
            self.fractionPLoad.append(self.computation[processor]/ld)
            print self.computation[processor]/ld





## virtualMachineParameters = None

## front end of virtual machine
##if _rank == 0:
virtualMachineParameters = VirtualMachineParameters()

## back-end of virtual machine
    ## virtual machine has NO back-end
## end of back-end of virtual machine
