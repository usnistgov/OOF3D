# -*- python -*- 
# $RCSfile: DIR.py,v $
# $Revision: 1.6.18.1 $
# $Author: langer $
# $Date: 2014/09/27 22:34:21 $


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modifed
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

## Unless there is a good reason to add default files to be compiled in this
## directory, which is a PETSc files directory, please only add files within
## the ifdef parenthesis.

dirname = 'PETSc'
if not DIM_3:
    clib = 'oof2engine'
else:
    clib = 'oof3dengine'

cfiles = ['petsc_solver.C','petsc_preconditioner.C','petsc_solverdriver.C']
swigfiles= ['petsc_solver.swg','petsc_preconditioner.swg','petsc_solverdriver.swg']
swigpyfiles = ['petsc_solver.spy','petsc_preconditioner.spy','petsc_solverdriver.spy']
hfiles = ['petsc_solver.h','petsc_preconditioner.h','petsc_solverdriver.h']

def set_clib_flags(clib):
    # *************
    # PETScII
    # *************
    clib.externalLibs.append('petsc')
    clib.externalLibs.append('petscmat')
    clib.externalLibs.append('petscvec')
    clib.externalLibs.append('petscdm')
    clib.externalLibs.append('petscksp')
    clib.externalLibDirs.append('/usr/lib/petsc/lib/libO/linux')
    clib.includeDirs.append('/usr/include/petsc')
    clib.includeDirs.append('/usr/include/mpi')
