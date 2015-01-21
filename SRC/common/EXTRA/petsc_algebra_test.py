#!/usr/bin/env python
#   mpirun -np 2 latency.py
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


def f(x=None): ## function to be executed by all threads
  if rank == 0:
    print "short job on process=", rank
    sys.stdout.flush()
    for i in range(50):
      pass ## do something a little long and tedious
  elif rank == 1:
    print "long an tedious job on process=", rank
    sys.stdout.flush()
    for i in range(500):
      pass ## do something longer and much more tedious
  
  print "waiting for completion", rank
  sys.stdout.flush()
  mpitools.mpi_barrier() ## any other process just waits
  print "Finished!", rank
  sys.stdout.flush()
  if x is not None:
    print x


def  g(x=None):
  return petsc_solver.create_matrix()


def run():    
  if numproc < 2:
    mpitools.mpi_abort() ## the whole point is to run in parallel!
    
  if rank == 0:
    ## front end
    ## import all modules and functions that it will need
    from ooflib.common.EXTRA import mpiGUI
    localGUI = mpiGUI.MpiGUI()
    localGUI.add_function(g)
    localGUI.mainloop() ## mainloop may execute other tasks too.
  else:
    while 1:
      msg = mpitools.recieve_string(0) ## waiting messages from GUI
      if msg == "quit":
        print "quitting process", rank
        sys.stdout.flush()
        sys.exit()
      elif msg == "apply function":
        g()
      mpitools.send_string(msg,0)

## no need to use mpi_finalize. at_exit takes care of this implicitly.


if __name__ == '__main__': ## All the processes have their own main
  run()


