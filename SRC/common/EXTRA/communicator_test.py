#!/usr/bin/env python
#   mpirun -np 4 communicator_test.py
import sys, time, os
from math import *
##
## Note:
## This script will NOT work for a parallel application if your local
## PYTHONPATH in your .cshrc file is not set to be wherever this code
## and oof.py is.
## Also, do not forget to put a soft link from wherever
## this program lives to the PYTHONPATH.
## For example, in my .cshr file I wrote:
## setenv PYTHONPATH $PYTHONPATH':/Users/edwin/NIST/OOF2/MPIBUILD'
##


import oofcppc ## import this ALWAYS before any swig-generated modules
from ooflib.SWIG.common import mpitools

start_time = time.time()


mpitools.mpi_initialize(sys.argv)
## no need to use mpi_finalize. The modele  at_exit takes care of that.


numproc = mpitools.size()
myid =    mpitools.rank()
node =    mpitools.get_processor_name()
lag = 0
print "I am proc %d of %d on node %s" %(myid+1, numproc, node)
mpitools.mpi_barrier() ## synchronizes all the processes


  
if numproc < 2:
  print "Demo must run on at least 2 processors to continue"      
  mpitools.mpi_abort()
  ## sys.exit()
  
if myid == 0:
  proc_0_time = time.time()
  msg = "%f"%proc_0_time  
  print 'Processor 1 sending message "%s" to processor %d' %(msg, 2)
  print  start_time, proc_0_time
  mpitools.send_string(msg, 1)
  mpitools.mpi_barrier()
  msg = mpitools.recieve_string(numproc-1)
  print 'Processor 1 received message "%s" from processor %d' %(msg, numproc)
  ## print 'Size of msg was %d bytes' %(SWIG.common.mpitools.bytes())


else:
  source = myid-1
  destination = (myid+1)%numproc
  mpitools.mpi_barrier()
  msg = mpitools.recieve_string(source)
  
  print 'Processor %d received message "%s" from processor %d'\
        %(myid+1, msg, source+1)
  ## print 'Size of msg was %d bytes' %(SWIG.common.mpitools.bytes())  
  proc_time = time.time()
  msg = msg + '->P' + str(myid) + '->%f'%proc_time #Update message     
  print 'Processor %d sending msg "%s" to %d' %(myid+1, msg, destination+1)
  print start_time, proc_time
  time.sleep(lag)
  mpitools.send_string(msg, destination)

## mpitools.mpi_finalize() ## no need to use mpi_finalize. at_exit takes care of that.





