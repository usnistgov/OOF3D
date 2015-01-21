# -*- python -*-
# $RCSfile: DIR.py,v $
# $Revision: 1.6.10.1 $
# $Author: langer $
# $Date: 2013/11/08 20:45:27 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

dirname   = 'elasticity'
if not DIM_3:
    clib = 'oof2engine'
else:
    clib = 'oof3dengine'
subdirs   = ['aniso', 'iso', 'thermo', 'nonlinear', 'visco', 'largestrain']

cfiles    = ['cijkl.C', 'elasticity.C']
hfiles    = ['cijkl.h', 'elasticity.h'] #, 'homogeneous.h']
swigfiles = ['cijkl.swg', 'elasticity.swg'] #, 'homogeneous.swg']
swigpyfiles   = ['cijkl.spy']
pyfiles = ['pyelasticity.py']
