#!/usr/bin/env python
import sys, time, os
from math import *
##
## ############### DOCUMENTATION ############### ##
##
## For generalities, check latency.py
##
##
sys.path.append("")
os.chdir("/u/home3/reida/work/OOF2/mpi_build")
## MPI Initialization overhead.
import oofcppc ## import this ALWAYS before any swig-generated modules
from ooflib.SWIG.common import mpitools
from ooflib.SWIG.engine.PETSc import petsc_solver

mpitools.mpi_initialize(sys.argv)
numproc = mpitools.size()
rank =    mpitools.rank()
name =    mpitools.get_processor_name()
mpitools.mpi_barrier() ## All processes wait each other here.

## Collection  of test functions/menuitem callbacks


def f(x=None): ## function to be executed by all threads
  if rank == 0:
    print "long job on process=", rank
    sys.stdout.flush()
    for i in range(5000000):
      pass ## do something a little long and tedious
  else:
    print "short job on process=", rank
    sys.stdout.flush()
    for i in range(50):
      pass ## do something longer and much more tedious
  
  mpitools.mpi_barrier() ## all processes just wait each othere here
  
  

def  g(x=None):
  return petsc_solver.create_matrix()



def h(x=None):
  try:
    if rank == 0:
      pass
    else:
      raise mpitools.MPIException()
  finally:
    mpitools.mpi_barrier() ## all  process wait each other here


def front_end():
  ##
  ## front end imports only modules and functions that will need.
  ## The front end runs on threads, so that GUI never gets
  ## cloged. The actual work is executed on a thread (Clerk).
  ## 
  from ooflib.common.EXTRA import mpiGUI
  localGUI = mpiGUI.MpiBroadcastAndTGUI() ## creates a threaded GUI
  localGUI.add_function(g) ## adds callback function
  localGUI.mainloop() ## setup mainloop

def parallel_quit():
  sys.stdout.flush()
  mpitools.mpi_barrier() ## --"all together, now!"-- Lennon and McCartney 
  sys.exit()

def back_end():
  ## back end waits for commands from front end, and blocks whenever
  ## a new instruction is received.
  ## the new command is executed right away, and the system returns
  ## to its previous waiting state as soon as the command is executed.
  while 1:
    msg = mpitools.recieve_broadcast_string(0) ## waiting messages from GUI
    if msg == "quit": ## quit "menuitem"
      print "quitting process", rank
      parallel_quit()
    elif msg == "apply function": ## apply menuitem callback
      g()

    
def run():    
  if rank == 0:
    front_end()
  else:
    back_end()
    


if __name__ == '__main__': ## All the processes have their own main
  run()


