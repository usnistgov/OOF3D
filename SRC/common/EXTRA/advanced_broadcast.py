#!/usr/bin/env python
import sys, time, os
from math import *
##
## ############### DOCUMENTATION ############### ##
##
## For generalities, check latency.py
##
##
print sys.argv[1:]
sys.path.append("")
os.chdir("/Users/edwin/NIST/OOF2/MPIBUILD")
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
    for i in range(500):
      mpitools.size()
      ## pass ## do something a little long and tedious
    
  else:
    print "short job on process=", rank
    sys.stdout.flush()
    for i in range(50):
      mpitools.rank()
      ## pass ## do something longer and much more tedious
    
  print "finished, process", rank
  sys.stdout.flush()
  mpitools.mpi_barrier() ## all processes just wait each othere here
  print "really finished, process", rank
  sys.stdout.flush()
  

def  g(x=None):
  print "started PETSc, process", rank
  sys.stdout.flush()
  petsc_solver.create_matrix()
  print "finished PETSc, process", rank
  sys.stdout.flush()



def h(x=None):
  try:
    if rank == 0:
      for i in range(10):
        msg = mpitools.receive_string(1)
        print msg
    else:
      for i in range(10):
        mpitools.send_string("this is a freakin test", 0);
  finally:
    mpitools.mpi_barrier() ## all  process wait each other here


def parallel_quit():
  sys.stdout.flush()
  mpitools.mpi_barrier() ## --"all together, now!"-- Lennon and McCartney 
  sys.exit()

  
def front_end(callback):
  ##
  ## front end imports only modules and functions that will need.
  ## The front end runs on threads, so that GUI never gets
  ## cloged. The actual work is executed on a thread (Clerk).
  ## 
  from ooflib.common.EXTRA import mpiGUI
  localGUI = mpiGUI.MpiBroadcastAndTGUI() ## creates a threaded GUI
  localGUI.add_function(callback) ## adds callback function
  localGUI.mainloop() ## setup mainloop


def back_end(callback):
  ## back end waits for commands from front end, and launches a thread
  ## whenever a new instruction is received.
  ## The requested command is executed right away, and the system returns
  ## to its previous waiting state as soon as the command is launched.
  from ooflib.common.EXTRA import clerk
  while 1:
    print "waiting for message", rank
    sys.stdout.flush()
    msg = mpitools.receive_broadcast_string(0) ## waiting messages from GUI
    print "message received", rank
    sys.stdout.flush()
    if msg == "quit": ## quit "menuitem"
      print "quitting process", rank
      parallel_quit()
    elif msg == "apply function": ## apply menuitem callback
      ## backBackEnd = clerk.Clerk(callback)
      ## backBackEnd.start()
      ##time.sleep(0.2)
      callback()
    
def run():    
  if rank == 0:
    front_end(g)
  else:
    back_end(g)
    


if __name__ == '__main__': ## All the processes have their own main
  run()


