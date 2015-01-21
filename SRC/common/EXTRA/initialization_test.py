#!/usr/bin/env python
#   mpirun -np 4 startup_test.py
import sys
## print sys.path
sys.path.append('/u/home4/redwing/OOF2/BUILD')
import oofcppc ## import this ALWAYS before any swig-generated modules
import ooflib.SWIG.common.mpitools
ooflib.SWIG.common.mpitools.mpi_initialize(sys.argv)
numproc = ooflib.SWIG.common.mpitools.size()
myid =    ooflib.SWIG.common.mpitools.rank()
node =    ooflib.SWIG.common.mpitools.get_processor_name()

print "I am proc %d of %d on node %s" %(myid, numproc, node)

ooflib.SWIG.common.mpitools.mpi_finalize()



